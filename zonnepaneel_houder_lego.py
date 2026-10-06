# Houder voor zonnepaneel 110 x 60 x 2 mm met twee 4 mm paneelbussen (12 mm montagegat),
# onderkant klikt op een LEGO-bouwplaat (22 x 10 noppen).
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD zonnepaneel_houder_lego.py
# Alle maten in mm. Paneel en montagegat komen van de productfoto's, de overige
# busmaten zijn geschat: meet ze na voor je print.
# Printen: ondersteboven (bovenvlak op het bed), dan is er geen support nodig.

import os

# Kleur van de geprinte delen in het model: Bambu PLA Basic Blue (#0A2989)

import FreeCAD as App
import Part
from FreeCAD import Vector as V

# ---------------------------------------------------------------- LEGO
NOP_STEEK = 8.0
NOP_D = 4.8
NOP_H = 1.7
KLEM = 0.10             # extra ruimte per kant rond de nop; kleiner = strakker klemmen
BUITEN_SPELING = 0.1    # buitenwand ligt zoveel binnen het raster
SLEUF_DIEPTE = NOP_H + 0.3
BAND_H = 4.0            # hoogte van de klemrand onderin

# ---------------------------------------------------------------- maten
NOPPEN_L = 16           # hoofdrechthoek 16 x 10 noppen = 128 x 80
NOPPEN_B = 10
OOR_NOPPEN_L = 3        # oor 3 x 4 noppen = 24 x 32
OOR_NOPPEN_B = 4
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4              # wanddikte boven de klemrand
R_HOEK = 3.0            # afronding buitenhoeken (groter botst met de hoeknoppen)

PANEEL_L = 110.0
PANEEL_B = 60.0
PANEEL_D = 2.0
SPELING = 0.3           # rondom het paneel
RAND_OVERLAP = 2.5      # zoveel dekt de bovenrand het paneel af
RAND_DIKTE = 1.5        # dikte van die bovenrand

BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm, plaatdikte max 6 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- afgeleid
PLAAT = RAND_DIKTE + PANEEL_D
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
OL = OOR_NOPPEN_L * NOP_STEEK
OB = OOR_NOPPEN_B * NOP_STEEK
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM           # 1,5: binnenkant buitenwand
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM           # 6,5: buitenkant klemrib
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1  # 9,5: vrij van de tweede rij noppen
BUS_X = HL + OL / 2
BUS_Y = HB - OB / 2
BUSSEN = [("rood", -BUS_X, BUS_Y, (0.85, 0.10, 0.10)),
          ("zwart", BUS_X, -BUS_Y, (0.08, 0.08, 0.08))]

# omtrek op het noppenraster: rechthoek met twee oren diagonaal tegenover elkaar
RASTER = Part.Face(Part.makePolygon([V(*p) for p in (
    (-HL, -HB), (HL + OL, -HB), (HL + OL, -HB + OB), (HL, -HB + OB),
    (HL, HB), (-HL - OL, HB), (-HL - OL, HB - OB), (-HL, HB - OB), (-HL, -HB))]))


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

    # holte: noppensleuf rondom, open midden, 45 graden verloop naar de dunne wand
    sleuf = binnen(SLEUF_BUITEN, -1, SLEUF_DIEPTE).cut(binnen(SLEUF_BINNEN, -2, SLEUF_DIEPTE + 1))
    delen = [binnen(RIB_BINNEN, -1, BAND_H)]
    stap, d, z = 0.4, RIB_BINNEN, BAND_H
    while d - stap > WAND:
        d -= stap
        delen.append(binnen(d, z, z + stap))
        z += stap
    delen.append(binnen(WAND, z, HOOGTE - PLAAT))
    houder = blok.cut(sleuf.fuse(delen))

    # venster en sponning: het paneel gaat er van onderaf in, tegen de bovenrand
    vl, vb = PANEEL_L / 2 - RAND_OVERLAP, PANEEL_B / 2 - RAND_OVERLAP
    houder = houder.cut(doos(-vl, -vb, vl, vb, HOOGTE - PLAAT - 1, HOOGTE + 1))
    sl, sb = PANEEL_L / 2 + SPELING, PANEEL_B / 2 + SPELING
    houder = houder.cut(doos(-sl, -sb, sl, sb, HOOGTE - PLAAT - 1, HOOGTE - RAND_DIKTE))
    for _, x, y, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(x, y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_bouwplaat():
    """Stuk LEGO-bouwplaat met noppen, alleen ter controle van de passing."""
    nx, ny = NOPPEN_L + 2 * OOR_NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H,
                                V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


def maak_paneel():
    return doos(-PANEEL_L / 2, -PANEEL_B / 2, PANEEL_L / 2, PANEEL_B / 2,
                HOOGTE - PLAAT, HOOGTE - RAND_DIKTE)


def maak_bus(x, y):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(x, y, HOOGTE))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, PLAAT + 16, V(x, y, HOOGTE - PLAAT - 16))
    lip = doos(x - 3, y - 0.4, x + 3, y + 0.4, HOOGTE - BUS_ACHTER, HOOGTE - PLAAT - 16)
    gat = Part.makeCylinder(2.0, 20, V(x, y, HOOGTE + BUS_KRAAG_H - 20))
    return kraag.fuse(schacht).fuse(lip).cut(gat)


def maak_moer(x, y):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(x, y, HOOGTE - PLAAT - 5))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(x, y, HOOGTE - PLAAT - 6)))


doc = App.newDocument("ZonnepaneelHouderLego")
onderdelen = [("Houder", maak_houder(), (0.04, 0.16, 0.54)),
              ("Zonnepaneel", maak_paneel(), (0.02, 0.02, 0.05)),
              ("Bouwplaat_controle", maak_bouwplaat(), (0.75, 0.75, 0.75))]
for naam, x, y, kleur in BUSSEN:
    onderdelen.append(("Bus_" + naam, maak_bus(x, y), kleur))
    onderdelen.append(("Moer_" + naam, maak_moer(x, y), (0.6, 0.6, 0.6)))
for naam, vorm, kleur in onderdelen:
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
    print(naam, "geldig:", vorm.isValid(), "volume: %.0f mm3" % vorm.Volume)
doc.recompute()
bb = doc.Houder.Shape.BoundBox
print("Houder buitenmaten: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
botsing = doc.Houder.Shape.common(doc.Bouwplaat_controle.Shape).Volume
print("Overlap houder/bouwplaat: %.3f mm3" % botsing)
for naam in ("Bus_rood", "Bus_zwart", "Moer_rood", "Moer_zwart", "Zonnepaneel"):
    print("Overlap houder/%s: %.3f mm3" % (naam, doc.Houder.Shape.common(doc.getObject(naam).Shape).Volume))

map_ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc.saveAs(os.path.join(map_, "Zonnepaneel_Houder_Lego.FCStd"))
Part.export([doc.Houder], os.path.join(map_, "Zonnepaneel_Houder_Lego-Houder.step"))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder_Lego.png"), 1400, 1000, "White")
    for naam in ("Zonnepaneel", "Bus_rood", "Bus_zwart", "Moer_rood", "Moer_zwart"):
        doc.getObject(naam).ViewObject.Visibility = False
    view.setCameraOrientation(App.Rotation(V(1, 0.25, 0), 145))
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder_Lego_onderkant.png"), 1400, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
