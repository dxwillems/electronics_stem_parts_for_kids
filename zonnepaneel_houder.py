# Houder voor zonnepaneel 110 x 60 x 2 mm met twee 4 mm paneelbussen (12 mm montagegat)
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD zonnepaneel_houder.py
# Alle maten in mm. Paneel 110 x 60 x 2 en montagegat 12 mm komen van de productfoto's,
# de overige busmaten zijn geschat: meet ze na voor je print.
# Printen: ondersteboven (bovenvlak op het bed), dan is er geen support nodig.

import os

# Kleur van de geprinte delen in het model: Bambu PLA Basic Blue (#0A2989)

import FreeCAD as App
import Part
from FreeCAD import Vector as V

# ---------------------------------------------------------------- maten
PANEEL_L = 110.0
PANEEL_B = 60.0
PANEEL_D = 2.0
SPELING = 0.3           # rondom het paneel
RAND_OVERLAP = 2.5      # zoveel dekt de bovenrand het paneel af
RAND_DIKTE = 1.5        # dikte van die bovenrand
FRAME = 8.0             # breedte van het frame rond het paneel
WAND = 2.4              # wanddikte van de opstaande rand
HOOGTE = 34.0           # totale hoogte; ruimte voor de achterkant van de bussen

OOR_L = 20.0            # oor steekt zoveel uit voorbij de korte zijde
OOR_B = 28.0
R_BUITEN = 10.0         # afronding oor
R_HOEK = 6.0            # afronding overige hoeken

BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm, plaatdikte max 6 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- afgeleid
PLAAT = RAND_DIKTE + PANEEL_D           # dikte bovenplaat
HL = PANEEL_L / 2 + FRAME               # halve lengte hoofdrechthoek
HB = PANEEL_B / 2 + FRAME
BUS_X = HL + OOR_L - OOR_B / 2 + 2
BUS_Y = HB - OOR_B / 2
BUSSEN = [("rood", -BUS_X, BUS_Y, (0.85, 0.10, 0.10)),
          ("zwart", BUS_X, -BUS_Y, (0.08, 0.08, 0.08))]


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def omtrek_vlak():
    """Bovenaanzicht: rechthoek met twee oren op diagonaal tegenover elkaar liggende hoeken."""
    vorm = doos(-HL, -HB, HL, HB, 0, 1)
    vorm = vorm.fuse(doos(-HL - OOR_L, HB - OOR_B, -HL, HB, 0, 1))
    vorm = vorm.fuse(doos(HL, -HB, HL + OOR_L, -HB + OOR_B, 0, 1)).removeSplitter()
    for ribbe_x, radius in ((HL + OOR_L, R_BUITEN), (HL, R_HOEK)):
        ribben = [e for e in vorm.Edges
                  if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 0.5
                  and abs(abs(e.Vertexes[0].Point.x) - ribbe_x) < 1e-6]
        vorm = vorm.makeFillet(radius, ribben)
    return [f for f in vorm.Faces if abs(f.CenterOfMass.z) < 1e-6][0]


def maak_houder():
    vlak = omtrek_vlak()
    houder = vlak.extrude(V(0, 0, HOOGTE))
    binnen = vlak.makeOffset2D(-WAND).extrude(V(0, 0, HOOGTE - PLAAT))
    houder = houder.cut(binnen)
    # venster en sponning: het paneel gaat er van onderaf in, tegen de bovenrand
    vl, vb = PANEEL_L / 2 - RAND_OVERLAP, PANEEL_B / 2 - RAND_OVERLAP
    houder = houder.cut(doos(-vl, -vb, vl, vb, HOOGTE - PLAAT - 1, HOOGTE + 1))
    sl, sb = PANEEL_L / 2 + SPELING, PANEEL_B / 2 + SPELING
    houder = houder.cut(doos(-sl, -sb, sl, sb, HOOGTE - PLAAT - 1, HOOGTE - RAND_DIKTE))
    for _, x, y, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(x, y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


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


doc = App.newDocument("ZonnepaneelHouder")
onderdelen = [("Houder", maak_houder(), (0.04, 0.16, 0.54)),
              ("Zonnepaneel", maak_paneel(), (0.02, 0.02, 0.05))]
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

map_ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc.saveAs(os.path.join(map_, "Zonnepaneel_Houder.FCStd"))
Part.export([doc.Houder], os.path.join(map_, "Zonnepaneel_Houder-Houder.step"))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder.png"), 1400, 1000, "White")
    doc.save()
