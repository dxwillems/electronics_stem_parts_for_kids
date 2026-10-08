# Vierkante spoelkoker met aansluitkastje voor twee 4 mm paneelbussen (12 mm montagegat)
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD spoel_bananenbus.py
# Alle maten in mm. Montagegat 12 mm komt van de productpagina van de bussen,
# de overige busmaten zijn geschat: meet ze na voor je print.

import os

# Kleur van de geprinte delen in het model: Bambu PLA Basic Blue (#0A2989)

import importlib
import sys

import FreeCAD as App
import Part
from FreeCAD import Vector as V

MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
sys.path.insert(0, MAP)
import symbolen
importlib.reload(symbolen)

# ---------------------------------------------------------------- maten spoelkoker
FLENS = 35.0            # vierkante flens
FLENS_DIKTE = 1.5
FLENS_RADIUS = 4.0
WIKKEL_HOOGTE = 6.0     # ruimte tussen de flenzen
GAT = 23.0              # vierkant gat door de kern
GAT_RADIUS = 2.0
KERN_WAND = 2.0
DRAAD = 0.8             # draaddiameter
LAGEN = 5               # 5 lagen van 7 = ca. 35 windingen

# ---------------------------------------------------------------- maten aansluitkastje
KAST_B = 54.0           # breedte (X)
KAST_D = 24.0           # diepte (Y)
KAST_H = 34.0           # hoogte; ruimte voor de achterkant van de bussen
KAST_RADIUS = 3.0
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
BUS_AFSTAND = 30.0      # hart-op-hart; ruimte voor het symbool tussen de bussen
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip
DRAADSLEUF = 2.0        # doorvoer voor de draadeinden naar het kastje

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0

# ---------------------------------------------------------------- afgeleid
KERN = GAT + 2 * KERN_WAND
KERN_RADIUS = GAT_RADIUS + KERN_WAND
Z_KERN = FLENS_DIKTE
Z_BOVEN = FLENS_DIKTE + WIKKEL_HOOGTE
Z_TOP = Z_BOVEN + FLENS_DIKTE
WIKKEL_DIKTE = DRAAD * (1 + (LAGEN - 1) * 0.866)    # lagen vallen in elkaar
WIKKEL = KERN + 2 * WIKKEL_DIKTE
WIKKEL_RADIUS = KERN_RADIUS + WIKKEL_DIKTE
KAST_Y1 = -FLENS / 2                    # kastwand tegen de flenzen
KAST_Y0 = KAST_Y1 - KAST_D
BUS_Y = (KAST_Y0 + KAST_Y1) / 2
BUSSEN = [("rood", BUS_AFSTAND / 2, (0.85, 0.10, 0.10)),
          ("zwart", -BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def afgerond(vorm, radius):
    """Rond alle verticale ribben af."""
    ribben = [e for e in vorm.Edges
              if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1e-6]
    return vorm.makeFillet(radius, ribben)


def vierkant(b, radius, z0, z1):
    return afgerond(doos(-b / 2, -b / 2, b / 2, b / 2, z0, z1), radius)


def maak_spoelkoker():
    koker = vierkant(FLENS, FLENS_RADIUS, 0, FLENS_DIKTE)
    koker = koker.fuse(vierkant(KERN, KERN_RADIUS, Z_KERN, Z_BOVEN))
    koker = koker.fuse(vierkant(FLENS, FLENS_RADIUS, Z_BOVEN, Z_TOP))
    # flenzen recht doortrekken tot tegen het kastje
    for z0, z1 in ((0, FLENS_DIKTE), (Z_BOVEN, Z_TOP)):
        koker = koker.fuse(doos(-FLENS / 2, KAST_Y1, FLENS / 2, KAST_Y1 + FLENS_RADIUS, z0, z1))
    koker = koker.cut(vierkant(GAT, GAT_RADIUS, -1, Z_TOP + 1))

    kast = afgerond(doos(-KAST_B / 2, KAST_Y0, KAST_B / 2, KAST_Y1, 0, KAST_H), KAST_RADIUS)
    kast = kast.cut(doos(-KAST_B / 2 + WAND, KAST_Y0 + WAND,
                         KAST_B / 2 - WAND, KAST_Y1 - WAND, -1, KAST_H - PLAAT))
    for _, x, _ in BUSSEN:
        kast = kast.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                          V(x, BUS_Y, KAST_H - PLAAT - 1)))
    for sx in (-1, 1):
        x = sx * (FLENS / 2 - 5)
        kast = kast.cut(doos(x - DRAADSLEUF / 2, KAST_Y1 - WAND - 1,
                             x + DRAADSLEUF / 2, KAST_Y1 + 1, Z_KERN, Z_BOVEN))
    return koker.fuse(kast).removeSplitter()


def maak_symbool():
    """Spoelsymbool tussen de twee bussen, verzonken in het dak van het kastje."""
    ruimte = BUS_AFSTAND - BUS_KRAAG_D
    vorm = symbolen.spoel(ruimte + 1.0, SYMBOOL_DIEPTE, SYMBOOL_LIJN, 3, (ruimte - 2.0) / 6)
    return symbolen.plaats(vorm, 0, BUS_Y, KAST_H - SYMBOOL_DIEPTE)


def maak_wikkeling():
    blok = vierkant(WIKKEL, WIKKEL_RADIUS, Z_KERN, Z_BOVEN)
    blok = blok.cut(vierkant(KERN, KERN_RADIUS, Z_KERN - 1, Z_BOVEN + 1))
    # buitenste laag als losse windingen, zodat het er als draad uitziet
    vlak = [f for f in vierkant(WIKKEL, WIKKEL_RADIUS, 0, 1).Faces
            if abs(f.CenterOfMass.z) < 1e-6][0]
    pad = vlak.OuterWire
    rand = pad.Edges[0]
    profiel = Part.Wire(Part.makeCircle(DRAAD / 2, rand.valueAt(rand.FirstParameter),
                                        rand.tangentAt(rand.FirstParameter)))
    winding = Part.Wire(pad.Edges).makePipeShell([profiel], True, True)
    windingen = []
    for i in range(int(WIKKEL_HOOGTE / DRAAD)):
        w = winding.copy()
        w.translate(V(0, 0, Z_KERN + DRAAD / 2 + i * DRAAD))
        windingen.append(w)
    return blok.fuse(windingen)


def maak_bus(x):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(x, BUS_Y, KAST_H))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, PLAAT + 16, V(x, BUS_Y, KAST_H - PLAAT - 16))
    lip = doos(x - 3, BUS_Y - 0.4, x + 3, BUS_Y + 0.4, KAST_H - BUS_ACHTER, KAST_H - PLAAT - 16)
    gat = Part.makeCylinder(2.0, 20, V(x, BUS_Y, KAST_H + BUS_KRAAG_H - 20))
    return kraag.fuse(schacht).fuse(lip).cut(gat)


def maak_moer(x):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(x, BUS_Y, KAST_H - PLAAT - 5))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(x, BUS_Y, KAST_H - PLAAT - 6)))


doc = App.newDocument("SpoelBananenbus")
koker = maak_spoelkoker()
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Spoelkoker", koker.cut(symbool) if symbool else koker, (0.04, 0.16, 0.54)),
              ("Koperwikkeling", maak_wikkeling(), (0.80, 0.50, 0.25))]
if symbool:
    onderdelen.insert(1, ("Symbool", symbool, (0.96, 0.96, 0.96)))
for naam, x, kleur in BUSSEN:
    onderdelen.append(("Bus_" + naam, maak_bus(x), kleur))
    onderdelen.append(("Moer_" + naam, maak_moer(x), (0.6, 0.6, 0.6)))
for naam, vorm, kleur in onderdelen:
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
    print(naam, "geldig:", vorm.isValid(), "volume: %.0f mm3" % vorm.Volume)
doc.recompute()
bb = doc.Spoelkoker.Shape.BoundBox
print("Spoelkoker buitenmaten: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
print("Wikkeling tot %.1f mm, flens %.1f mm" % (WIKKEL, FLENS))

map_ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc.saveAs(os.path.join(map_, "Spoel_Electromagneet_Bananenbus.FCStd"))
# een bestand met twee delen: in de slicer het symbool een andere kleur geven
Part.export([doc.Spoelkoker] + ([doc.Symbool] if symbool else []),
            os.path.join(map_, "Spoel_Electromagneet_Bananenbus-Spoelkoker.step"))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Spoel_Electromagneet_Bananenbus.png"), 1400, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Spoel_Electromagneet_Bananenbus_bovenaanzicht.png"), 1000, 1000, "White")
    view.viewIsometric()
    view.fitAll()
    doc.save()
