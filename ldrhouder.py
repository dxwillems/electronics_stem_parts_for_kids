# Houder voor een LDR (lichtgevoelige weerstand, LUNA PDV-P8103, ca. 5 x 4,3 x 2 mm) met twee
# 4 mm paneelbussen (12 mm montagegat) en het LDR-symbool; onderkant klemt op een
# LEGO-bouwplaat (8 x 8 noppen). De LDR ligt in een ondiep kuiltje bovenop, de pootjes gaan
# door twee gaatjes naar binnen. Zet de LDR altijd in serie met iets (bijv. de LED-module).
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD ldrhouder.py
# Afstand tussen de pootjes (3,4 mm) is geschat: meet na.
# Printen: ondersteboven (bovenvlak op het bed), dan is er geen support nodig.

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
NOPPEN_B = 8            # 64 mm
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
R_HOEK = 3.0

LDR_Y = 14.0
LDR_KUIL_D = 6.9        # kuiltje voor het LDR-schijfje (5,08 x 4,29 mm, diagonaal 6,6 mm)
LDR_KUIL_H = 1.2        # LDR is 2 mm dik: steekt 0,8 mm uit
LDR_POOT_D = 1.2
LDR_STEEK = 3.4         # geschat: afstand tussen de pootjes
ONDERDEEL_Y = LDR_Y
ONDERDEEL_D = LDR_KUIL_D
WAARDE = ""             # geen tekst

BUS_AFSTAND = 26.0      # hart-op-hart van de twee bussen
BUS_Y = -13.0
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0
SYMBOOL_Y = -1.5        # hoogte van de draad van het symbool, tussen bussen en knop

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

    # kuiltje en twee pootjesgaatjes voor de LDR
    houder = houder.cut(Part.makeCylinder(LDR_KUIL_D / 2, LDR_KUIL_H + 1, V(0, LDR_Y, HOOGTE - LDR_KUIL_H)))
    for sx in (-1, 1):
        houder = houder.cut(Part.makeCylinder(LDR_POOT_D / 2, PLAAT + 2, V(sx * LDR_STEEK / 2, LDR_Y, HOOGTE - PLAAT - 1)))
    for _, x, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(x, BUS_Y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_symbool():
    """Symbool tussen de bussen en het onderdeel, met een draad omlaag naar elke bus."""
    z = HOOGTE - SYMBOOL_DIEPTE
    vorm = symbolen.plaats(symbolen.ldr(BUS_AFSTAND, SYMBOOL_DIEPTE, SYMBOOL_LIJN), 0, SYMBOOL_Y, z)
    for _, x, _ in BUSSEN:
        draad = symbolen.lijn((x, SYMBOOL_Y), (x, BUS_Y + BUS_KRAAG_D / 2 - 0.5), SYMBOOL_LIJN, SYMBOOL_DIEPTE)
        vorm = vorm.fuse(symbolen.plaats(draad, 0, 0, z))
    if WAARDE:
        vorm = vorm.fuse(symbolen.plaats(symbolen.tekst(WAARDE, 4.0, SYMBOOL_DIEPTE), 0, -(HB - WAND - 4.5), z))
    return vorm


def maak_deel():
    """LDR vereenvoudigd: schijfje in het kuiltje met twee pootjes."""
    schijf = Part.makeBox(5.08, 4.29, 2.0, V(-2.54, LDR_Y - 2.145, HOOGTE - LDR_KUIL_H))
    for sx in (-1, 1):
        schijf = schijf.fuse(Part.makeCylinder(0.25, 15, V(sx * LDR_STEEK / 2, LDR_Y, HOOGTE - LDR_KUIL_H - 15)))
    return schijf


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


doc = App.newDocument("LDRhouder")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (0, HB - WAND - 6, 0), (0, -(HB - WAND - 6), 0), (0, 0, 0),
    (-(HL - WAND - 6), 0, 90), (HL - WAND - 6, 0, 90)])
print("Handtekening op", plek)
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, (0.04, 0.16, 0.54)),
              ("LDR", maak_deel(), (0.7, 0.7, 0.7)),
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
doc.saveAs(os.path.join(map_, "LDRhouder.FCStd"))
# een bestand met twee delen: houder en symbool
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []),
            os.path.join(map_, "LDRhouder-Houder.step"))
# alleen de onderste 6 mm: snelle proefprint om de klemming op een bouwplaat te testen
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(map_, "LDRhouder-Pastest.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "LDRhouder.png"), 1400, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "LDRhouder_bovenaanzicht.png"), 1000, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name == "Houder"
    view.viewBottom()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "LDRhouder_onderaanzicht.png"), 1000, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
