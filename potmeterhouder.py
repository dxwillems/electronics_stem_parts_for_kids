# Houder voor een draadpotmeter (KYOCERA/AVX 3104604002: 100 ohm, 4 W, lineair, as 6 mm,
# schroefdraad M10) met twee 4 mm paneelbussen (12 mm montagegat) en het symbool van een
# regelbare weerstand; onderkant klemt op een LEGO-bouwplaat (8 x 10 noppen).
# De potmeter zit verzonken in een kom, zodat de lange as minder uitsteekt; de knop (apart
# printen) klemt met een M3-stelschroefje op de as van 6 mm.
# Sluit de middelste aansluiting (loper) en een buitenste aan op de twee bussen. Max 0,2 A.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD potmeterhouder.py
# Gat en asmaten van de productpagina; de maten van het potmeterhuis zijn geschat.
# Printen: ondersteboven (bovenvlak op het bed), dan is er geen support nodig.

import math
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

# ---------------------------------------------------------------- LEGO
NOP_STEEK = 8.0
NOP_D = 4.8
NOP_H = 1.7
KLEM = 0.05             # ruimte per kant tussen nop en de vlakke sleufwanden
KLEMRIB_OVERMAAT = 0.20 # zoveel knijpt elke klemrib in de nop; groter = vaster, 0 = geen ribben
KLEMRIB_R = 0.6         # straal van de klemribben (verticale halve cilinders in de sleuf)
KLEMRIB_INLOOP = 0.5    # schuine aanloop onderaan, zodat de noppen erin glijden
BUITEN_SPELING = 0.1    # buitenwand ligt zoveel binnen het raster
SLEUF_DIEPTE = NOP_H + 0.3
BAND_H = 4.0            # hoogte van de klemrand onderin

# ---------------------------------------------------------------- maten
NOPPEN_L = 8            # 64 mm
NOPPEN_B = 10           # 80 mm: ruimte voor de verzonken potmeter
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
R_HOEK = 3.0

POT_GAT_D = 10.2        # M10-bus van de potmeter
POT_Y = 15.0
POT_HUIS_D = 30.0       # geschat: diameter van het potmeterhuis onder de plaat
POT_HUIS_H = 22.0       # geschat
AS_L = 20.5             # lengte van de as vanaf het montagevlak (productpagina)
KOM_D = 30.0            # verzonken kom rond de potmeter
KOM_DIEPTE = 6.0
KOM_WAND = 2.0
KNOP_D = 26.0           # knop (apart printen)
KNOP_H = 16.0
KNOP_GAT_D = 6.0 + 0.15 # as van 6 mm
KNOP_GAT_DIEPTE = 13.0
KNOP_VRIJ = 1.5         # knop zweeft zoveel boven de doos
STELSCHROEF_D = 2.5     # voorboorgat voor een M3-stelschroefje (of zelftappend 2,9 mm)
ONDERDEEL_Y = POT_Y
ONDERDEEL_D = 16.0   # moer op de M10-bus
WAARDE = "100 \u03a9"    # op de doos; leeg = geen tekst

BUS_AFSTAND = 26.0      # hart-op-hart van de twee bussen
BUS_Y = -16.0
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0
SYMBOOL_Y = -7.0        # hoogte van de draad van het symbool, tussen bussen en knop

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
BUSSEN = [("rood", -BUS_AFSTAND / 2, (0.85, 0.10, 0.10)),
          ("zwart", BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]

RASTER = Part.Face(Part.makePolygon([V(*p) for p in (
    (-HL, -HB), (HL, -HB), (HL, HB), (-HL, HB), (-HL, -HB))]))


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def binnen(d, z0, z1):
    """Rasteromtrek, d naar binnen verschoven (scherpe hoeken), van z0 tot z1."""
    vlak = RASTER.makeOffset2D(-d, 2)
    vlak.translate(V(0, 0, z0))
    return vlak.extrude(V(0, 0, z1 - z0))


def maak_klemribben():
    """Een smalle rib per nop op de binnenwand van de sleuf; die vervormt en klemt de nop vast.
    De hoeknoppen krijgen er geen: daar loopt de binnenwand niet langs."""
    r, uitsteek = KLEMRIB_R, KLEM + KLEMRIB_OVERMAAT
    plekken = []       # (x, y) van de ribas: uitsteek buiten de binnenwand, de rest erin
    for i in range(1, NOPPEN_L - 1):
        x = -HL + (i + 0.5) * NOP_STEEK
        for sy in (-1, 1):
            plekken.append((x, sy * (HB - SLEUF_BINNEN - (r - uitsteek))))
    for j in range(1, NOPPEN_B - 1):
        y = -HB + (j + 0.5) * NOP_STEEK
        for sx in (-1, 1):
            plekken.append((sx * (HL - SLEUF_BINNEN - (r - uitsteek)), y))
    ribben = []
    for x, y in plekken:
        ribben.append(Part.makeCone(r - uitsteek, r, KLEMRIB_INLOOP, V(x, y, 0)))
        ribben.append(Part.makeCylinder(r, SLEUF_DIEPTE - KLEMRIB_INLOOP + 0.2,
                                        V(x, y, KLEMRIB_INLOOP)))
    return ribben


def maak_houder():
    blok = binnen(BUITEN_SPELING, 0, HOOGTE)
    ribben = [e for e in blok.Edges
              if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1]
    blok = blok.makeFillet(R_HOEK, ribben)

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
    if KLEMRIB_OVERMAAT > 0:
        houder = houder.fuse(maak_klemribben())

    # verzonken kom met de potmeter in de bodem
    z_bodem = HOOGTE - KOM_DIEPTE
    houder = houder.fuse(Part.makeCylinder(KOM_D / 2 + KOM_WAND, KOM_DIEPTE + PLAAT, V(0, POT_Y, z_bodem - PLAAT)))
    houder = houder.cut(Part.makeCylinder(KOM_D / 2, KOM_DIEPTE + 1, V(0, POT_Y, z_bodem)))
    houder = houder.cut(Part.makeCylinder(POT_GAT_D / 2, PLAAT + 2, V(0, POT_Y, z_bodem - PLAAT - 1)))
    for _, x, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(x, BUS_Y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_symbool():
    """Symbool tussen de bussen en het onderdeel, met een draad omlaag naar elke bus."""
    z = HOOGTE - SYMBOOL_DIEPTE
    vorm = symbolen.plaats(symbolen.regelweerstand(BUS_AFSTAND, SYMBOOL_DIEPTE, SYMBOOL_LIJN), 0, SYMBOOL_Y, z)
    for _, x, _ in BUSSEN:
        draad = symbolen.lijn((x, SYMBOOL_Y), (x, BUS_Y + BUS_KRAAG_D / 2 - 0.5), SYMBOOL_LIJN, SYMBOOL_DIEPTE)
        vorm = vorm.fuse(symbolen.plaats(draad, 0, 0, z))
    if WAARDE:
        vorm = vorm.fuse(symbolen.plaats(symbolen.tekst(WAARDE, 4.0, SYMBOOL_DIEPTE), 0, -(HB - WAND - 4.5), z))
    return vorm


def maak_deel():
    """Draadpotmeter vereenvoudigd: huis onder de plaat, bus en as erboven, met moer."""
    z = HOOGTE - KOM_DIEPTE                     # montagevlak = bodem van de kom
    huis = Part.makeCylinder(POT_HUIS_D / 2, POT_HUIS_H, V(0, POT_Y, z - PLAAT - POT_HUIS_H))
    bus = Part.makeCylinder(POT_GAT_D / 2 - 0.1, PLAAT + 7, V(0, POT_Y, z - PLAAT))
    a = Part.makeCylinder(3.0, AS_L, V(0, POT_Y, z))
    moer = Part.makeCylinder(8.0, 2.5, V(0, POT_Y, z)).cut(Part.makeCylinder(5.0, 4, V(0, POT_Y, z - 1)))
    return huis.fuse(bus).fuse(a).fuse(moer)


def maak_knop():
    """Knop met ribbels en een wijzergleuf; klemt met een stelschroefje op de as."""
    z_top_as = HOOGTE - KOM_DIEPTE + AS_L
    z0 = max(HOOGTE + KNOP_VRIJ, z_top_as - KNOP_GAT_DIEPTE)
    knop = Part.makeCylinder(KNOP_D / 2, KNOP_H, V(0, POT_Y, z0))
    for i in range(24):                                   # ribbels voor grip
        a = math.radians(360.0 * i / 24)
        knop = knop.cut(Part.makeCylinder(0.9, KNOP_H - 3, V(KNOP_D / 2 * math.cos(a), POT_Y + KNOP_D / 2 * math.sin(a), z0)))
    knop = knop.cut(Part.makeBox(1.6, KNOP_D / 2 - 2, 1.2, V(-0.8, POT_Y + 2, z0 + KNOP_H - 1.2)))   # wijzer
    knop = knop.cut(Part.makeCylinder(KNOP_GAT_D / 2, KNOP_GAT_DIEPTE, V(0, POT_Y, z0 - 0.01)))
    knop = knop.cut(Part.makeCylinder(STELSCHROEF_D / 2, KNOP_D, V(0, POT_Y, z0 + KNOP_GAT_DIEPTE / 2), V(1, 0, 0)))
    return knop


def maak_bouwplaat():
    """Stuk LEGO-bouwplaat met noppen, alleen ter controle van de passing."""
    nx, ny = NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H,
                                V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


def maak_bus(x):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(x, BUS_Y, HOOGTE))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, PLAAT + 16, V(x, BUS_Y, HOOGTE - PLAAT - 16))
    lip = doos(x - 3, BUS_Y - 0.4, x + 3, BUS_Y + 0.4, HOOGTE - BUS_ACHTER, HOOGTE - PLAAT - 16)
    gat = Part.makeCylinder(2.0, 20, V(x, BUS_Y, HOOGTE + BUS_KRAAG_H - 20))
    return kraag.fuse(schacht).fuse(lip).cut(gat)


def maak_moer(x):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(x, BUS_Y, HOOGTE - PLAAT - 5))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(x, BUS_Y, HOOGTE - PLAAT - 6)))


doc = App.newDocument("Potmeterhouder")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (0, HB - WAND - 6, 0), (0, -(HB - WAND - 6), 0), (0, 0, 0),
    (-(HL - WAND - 6), 0, 90), (HL - WAND - 6, 0, 90)])
print("Handtekening op", plek)
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, (0.04, 0.16, 0.54)),
              ("Potmeter", maak_deel(), (0.7, 0.7, 0.7)),
              ("Knop", maak_knop(), (0.04, 0.16, 0.54)),
              ("Bouwplaat_controle", maak_bouwplaat(), (0.75, 0.75, 0.75))]
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
bb = doc.Houder.Shape.BoundBox
print("Houder buitenmaten: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
for obj in doc.Objects:
    if obj.Name != "Houder":
        overlap = doc.Houder.Shape.common(obj.Shape)
        print("Overlap houder/%s: %.3f mm3" % (obj.Name, overlap.Volume))
        if obj.Name == "Bouwplaat_controle":   # hier hoort alleen de klemoverlap van de ribben te zitten
            print("  klemplekken: %d, grootste overlap per plek: %.4f mm3"
                  % (len(overlap.Solids), max([v.Volume for v in overlap.Solids] or [0])))
print("Vrije opening onderkant: x +/- %.1f, y +/- %.1f" % (HL - RIB_BINNEN, HB - RIB_BINNEN))
print("Moeren bussen: x tot +/- %.1f, y %.1f tot %.1f; onderdeel y tot %.1f"
      % (BUS_AFSTAND / 2 + BUS_MOER_D / 2, BUS_Y - BUS_MOER_D / 2, BUS_Y + BUS_MOER_D / 2, ONDERDEEL_Y + 7.5))
if symbool:
    sb = symbool.BoundBox
    print("Symbool: x %.1f tot %.1f, y %.1f tot %.1f; onderdeel vanaf y %.1f"
          % (sb.XMin, sb.XMax, sb.YMin, sb.YMax, ONDERDEEL_Y - ONDERDEEL_D / 2))
    print("Afstand symbool tot onderdeel: %.2f mm"
          % symbool.distToShape(Part.makeCylinder(ONDERDEEL_D / 2, 1, V(0, ONDERDEEL_Y, HOOGTE - 0.5)))[0])

map_ = MAP
doc.saveAs(os.path.join(map_, "Potmeterhouder.FCStd"))
# een bestand met twee delen: houder en symbool
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []),
            os.path.join(map_, "Potmeterhouder-Houder.step"))
# alleen de onderste 6 mm: snelle proefprint om de klemming op een bouwplaat te testen
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(map_, "Potmeterhouder-Pastest.step"))
Part.export([doc.Knop], os.path.join(map_, "Potmeterhouder-Knop.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Potmeterhouder.png"), 1400, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Potmeterhouder_bovenaanzicht.png"), 1000, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name == "Houder"
    view.viewBottom()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Potmeterhouder_onderaanzicht.png"), 1000, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
