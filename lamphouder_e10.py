# Houder voor een E10-lampfitting met beugel (41 mm, 2 schroefgaten) en twee 4 mm
# paneelbussen (12 mm montagegat); onderkant klikt op een LEGO-bouwplaat (8 x 8 noppen).
# Vierkant, zodat je van onderaf met je vingers bij de moeren en soldeerlippen kunt.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD lamphouder_e10.py
# Alle maten in mm. Beugellengte 41, fitting 10 x 18 en montagegat 12 komen van de
# productfoto's; de gatafstand van de beugel (32) en de busmaten zijn geschat: meet ze na.
# Printen: ondersteboven (bovenvlak op het bed), dan is er geen support nodig.

import os

import FreeCAD as App
import Part
from FreeCAD import Vector as V

# ---------------------------------------------------------------- LEGO
LEGO = True             # False = gewone open onderkant met rechte wand
NOP_STEEK = 8.0
NOP_D = 4.8
NOP_H = 1.7
KLEM = 0.10             # extra ruimte per kant rond de nop; kleiner = strakker klemmen
BUITEN_SPELING = 0.1    # buitenwand ligt zoveel binnen het raster
SLEUF_DIEPTE = NOP_H + 0.3
BAND_H = 4.0            # hoogte van de klemrand onderin

# ---------------------------------------------------------------- maten
NOPPEN_L = 8            # 64 mm
NOPPEN_B = 8            # 64 mm
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
R_HOEK = 3.0

BEUGEL_L = 41.0         # productfoto
BEUGEL_B = 10.0         # geschat
SCHROEF_AFSTAND = 32.0  # hart-op-hart van de twee beugelgaten, geschat van de foto
SCHROEF_GAT_D = 2.5     # voorboorgat voor zelftappende schroef 2,9 of M3
SCHROEF_DIEPTE = 8.0
NOK_D = 7.0             # verdikking onder de plaat rond het schroefgat
DOORVOER_L = 18.0       # sleuf onder de fitting voor klinknagel en draden (dwars op de beugel)
DOORVOER_B = 6.0
FITTING_D = 10.0        # productfoto
FITTING_H = 18.0        # productfoto
FITTING_Y = 12.0        # fitting achteraan, bussen vooraan

BUS_AFSTAND = 24.0      # hart-op-hart van de twee bussen
BUS_Y = -13.0
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
BUSSEN = [("rood", -BUS_AFSTAND / 2, (0.85, 0.10, 0.10)),
          ("zwart", BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]
SCHROEVEN = (-SCHROEF_AFSTAND / 2, SCHROEF_AFSTAND / 2)

RASTER = Part.Face(Part.makePolygon([V(*p) for p in (
    (-HL, -HB), (HL, -HB), (HL, HB), (-HL, HB), (-HL, -HB))]))


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def binnen(d, z0, z1):
    """Rasteromtrek, d naar binnen verschoven (scherpe hoeken), van z0 tot z1."""
    vlak = RASTER.makeOffset2D(-d, 2)
    vlak.translate(V(0, 0, z0))
    return vlak.extrude(V(0, 0, z1 - z0))


def maak_houder():
    blok = binnen(BUITEN_SPELING, 0, HOOGTE)
    ribben = [e for e in blok.Edges
              if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1]
    blok = blok.makeFillet(R_HOEK, ribben)

    if LEGO:
        # noppensleuf rondom, open midden, 45 graden verloop naar de dunne wand
        sleuf = binnen(SLEUF_BUITEN, -1, SLEUF_DIEPTE).cut(
            binnen(SLEUF_BINNEN, -2, SLEUF_DIEPTE + 1))
        delen = [binnen(RIB_BINNEN, -1, BAND_H)]
        stap, d, z = 0.4, RIB_BINNEN, BAND_H
        while d - stap > WAND:
            d -= stap
            delen.append(binnen(d, z, z + stap))
            z += stap
        delen.append(binnen(WAND, z, HOOGTE - PLAAT))
        houder = blok.cut(sleuf.fuse(delen))
    else:
        houder = blok.cut(binnen(WAND, -1, HOOGTE - PLAAT))

    # schroefnokken onder de plaat, met voorboorgat vanaf de bovenkant
    for x in SCHROEVEN:
        houder = houder.fuse(Part.makeCylinder(NOK_D / 2, SCHROEF_DIEPTE + 1 - PLAAT,
                                               V(x, FITTING_Y, HOOGTE - SCHROEF_DIEPTE - 1)))
    for x in SCHROEVEN:
        houder = houder.cut(Part.makeCylinder(SCHROEF_GAT_D / 2, SCHROEF_DIEPTE + 1,
                                              V(x, FITTING_Y, HOOGTE - SCHROEF_DIEPTE)))
    # doorvoer onder de fitting
    r = DOORVOER_B / 2
    doorvoer = doos(-r, -DOORVOER_L / 2 + r, r, DOORVOER_L / 2 - r, HOOGTE - PLAAT - 1, HOOGTE + 1)
    for sy in (-1, 1):
        doorvoer = doorvoer.fuse(Part.makeCylinder(
            r, PLAAT + 2, V(0, sy * (DOORVOER_L / 2 - r), HOOGTE - PLAAT - 1)))
    doorvoer.translate(V(0, FITTING_Y, 0))
    houder = houder.cut(doorvoer)
    for _, x, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(x, BUS_Y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_fitting():
    """Vereenvoudigde E10-fitting met beugel, alleen ter controle van de passing."""
    dikte, brug = 0.6, 4.0
    voet = (BEUGEL_L - 16) / 2
    delen = []
    for sx in (-1, 1):
        x0, x1 = sorted((sx * BEUGEL_L / 2, sx * (BEUGEL_L / 2 - voet)))
        delen.append(doos(x0, -BEUGEL_B / 2, x1, BEUGEL_B / 2, HOOGTE, HOOGTE + dikte))
        x0, x1 = sorted((sx * 8, sx * (8 - dikte)))
        delen.append(doos(x0, -BEUGEL_B / 2, x1, BEUGEL_B / 2, HOOGTE, HOOGTE + brug))
    delen.append(Part.makeCylinder(FITTING_D / 2 + 0.8, FITTING_H - brug, V(0, 0, HOOGTE + brug)))
    beugel = doos(-8, -BEUGEL_B / 2, 8, BEUGEL_B / 2, HOOGTE + brug - dikte, HOOGTE + brug)
    beugel = beugel.fuse(delen)
    for x in SCHROEVEN:
        beugel = beugel.cut(Part.makeCylinder(1.6, 3, V(x, 0, HOOGTE - 1)))
    beugel = beugel.cut(Part.makeCylinder(FITTING_D / 2 - 0.3, FITTING_H,
                                          V(0, 0, HOOGTE + brug + 2)))
    beugel.translate(V(0, FITTING_Y, 0))
    return beugel


def maak_bouwplaat():
    """Stuk LEGO-bouwplaat met noppen, alleen ter controle van de passing."""
    nx, ny = NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H,
                                V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


def maak_bus(x):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(x, 0, HOOGTE))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, PLAAT + 16, V(x, 0, HOOGTE - PLAAT - 16))
    lip = doos(x - 3, -0.4, x + 3, 0.4, HOOGTE - BUS_ACHTER, HOOGTE - PLAAT - 16)
    gat = Part.makeCylinder(2.0, 20, V(x, 0, HOOGTE + BUS_KRAAG_H - 20))
    bus = kraag.fuse(schacht).fuse(lip).cut(gat)
    bus.translate(V(0, BUS_Y, 0))
    return bus


def maak_moer(x):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(x, 0, HOOGTE - PLAAT - 5))
    moer = moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(x, 0, HOOGTE - PLAAT - 6)))
    moer.translate(V(0, BUS_Y, 0))
    return moer


doc = App.newDocument("LamphouderE10")
onderdelen = [("Houder", maak_houder(), (0.15, 0.85, 0.20)),
              ("Fitting_E10", maak_fitting(), (0.78, 0.78, 0.80)),
              ("Bouwplaat_controle", maak_bouwplaat(), (0.75, 0.75, 0.75))]
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
bb = doc.Houder.Shape.BoundBox
print("Houder buitenmaten: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
for obj in doc.Objects:
    if obj.Name != "Houder" and (LEGO or obj.Name != "Bouwplaat_controle"):
        print("Overlap houder/%s: %.3f mm3" % (obj.Name, doc.Houder.Shape.common(obj.Shape).Volume))
print("Vrije opening onderkant: %.1f x %.1f mm" % (2 * (HL - RIB_BINNEN), 2 * (HB - RIB_BINNEN)))
print("Afstand bus-moer tot schroefnok: %.1f mm" % doc.Moer_rood.Shape.distToShape(
    Part.makeCylinder(NOK_D / 2, 10, V(SCHROEVEN[0], FITTING_Y, HOOGTE - 12)))[0])

map_ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc.saveAs(os.path.join(map_, "Lamphouder_E10.FCStd"))
Part.export([doc.Houder], os.path.join(map_, "Lamphouder_E10-Houder.step"))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Lamphouder_E10.png"), 1400, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name == "Houder"
    view.viewBottom()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Lamphouder_E10_onderaanzicht.png"), 1000, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Lamphouder_E10_bovenaanzicht.png"), 1000, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
