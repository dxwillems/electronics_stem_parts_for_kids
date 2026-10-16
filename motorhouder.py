# Motormodule: SOL300 zonnemotor met propeller op een staander, de lucht blaast opzij.
# Twee delen om te printen:
#  - Houder: doos met twee 4 mm paneelbussen (12 mm montagegat), het motorsymbool (M) en een
#    sleuf voor de staander; onderkant klemt op een LEGO-bouwplaat (8 x 8 noppen).
#  - Standaard: rechtopstaande plaat met een gat waar de motor in klemt, en een tap onderaan
#    die in de sleuf van de doos steekt (vastzetten met een druppel lijm).
# De propeller is een apart model: propeller.py.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD motorhouder.py
# Motor: Sol Expert SOL300, 24,2 mm rond (productpagina Conrad); de lengte van de motor en
# van de as zijn niet nagemeten. De busmaten onder de plaat zijn geschat.
# Printen: de doos ondersteboven, de staander plat op zijn zijkant; beide zonder support.

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
import propeller
importlib.reload(propeller)

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

MOTOR_D = 24.2          # SOL300, productpagina
MOTOR_L = 14.0          # geschat: lengte van het motorhuis
MOTOR_GAT_D = 24.5      # gat in de staander
KLEMRIB_MOTOR = 0.3     # drie ribjes in het gat knijpen zoveel in de motor
AS_L = 10.0             # geschat: lengte van de as voor de motor

STAND_X = 14.0          # midden van de staander (dikte langs X; de lucht blaast naar +X)
STAND_DIKTE = 7.0
STAND_B = 34.0          # breedte van de staander
AS_HOOGTE = 42.0        # hart van de motor boven de doos: propeller van 70 mm blijft 7 mm vrij
TAP_B = 24.0            # tap onder de staander
TAP_DIEPTE = 11.0       # zo diep steekt de tap in de doos (plaat + koker)
TAP_SPELING = 0.2       # per kant
KOKER_WAND = 2.0
DRAADGAT_D = 6.0        # gat in de bovenplaat achter de staander voor de motordraden
DRAADGAT_Y = 9.0

BUS_X = -18.0           # bussen links, ver van de propeller
BUS_AFSTAND = 26.0      # hart-op-hart van de twee bussen (langs Y)
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0
SYMBOOL_X = -1.0        # tussen de bussen en de staander
SYMBOOL_D = 12.0

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
Z_AS = HOOGTE + AS_HOOGTE
BUSSEN = [("rood", BUS_AFSTAND / 2, (0.85, 0.10, 0.10)),
          ("zwart", -BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]

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

    # koker onder de plaat waar de tap van de staander in steekt
    tx, ty = STAND_DIKTE / 2 + TAP_SPELING, TAP_B / 2 + TAP_SPELING
    z_tap = HOOGTE - TAP_DIEPTE
    houder = houder.fuse(doos(STAND_X - tx - KOKER_WAND, -ty - KOKER_WAND, STAND_X + tx + KOKER_WAND,
                              ty + KOKER_WAND, z_tap, HOOGTE - PLAAT + 0.5))
    houder = houder.cut(doos(STAND_X - tx, -ty, STAND_X + tx, ty, z_tap - 1, HOOGTE + 1))
    houder = houder.cut(Part.makeCylinder(DRAADGAT_D / 2, PLAAT + 2,
                                          V(STAND_X - STAND_DIKTE / 2 - DRAADGAT_D / 2 - 2,
                                            DRAADGAT_Y, HOOGTE - PLAAT - 1)))
    for _, y, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(BUS_X, y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_standaard():
    """Rechtopstaande plaat (dikte langs X) met het motorgat en de tap onderaan."""
    x0, x1 = STAND_X - STAND_DIKTE / 2, STAND_X + STAND_DIKTE / 2
    plaat = doos(x0, -STAND_B / 2, x1, STAND_B / 2, HOOGTE, Z_AS)
    plaat = plaat.fuse(Part.makeCylinder(STAND_B / 2, STAND_DIKTE, V(x0, 0, Z_AS), V(1, 0, 0)))
    plaat = plaat.fuse(doos(x0, -TAP_B / 2, x1, TAP_B / 2, HOOGTE - TAP_DIEPTE + 0.5, HOOGTE + 0.1))
    plaat = plaat.cut(Part.makeCylinder(MOTOR_GAT_D / 2, STAND_DIKTE + 2, V(x0 - 1, 0, Z_AS), V(1, 0, 0)))
    # drie klemribjes in het motorgat
    r_rib = 0.6
    for hoek in (90, 210, 330):
        a = __import__("math").radians(hoek)
        afstand = MOTOR_GAT_D / 2 - KLEMRIB_MOTOR - (MOTOR_GAT_D - MOTOR_D) / 2 + r_rib
        rib = Part.makeCylinder(r_rib, STAND_DIKTE, V(x0, afstand * __import__("math").cos(a),
                                                     Z_AS + afstand * __import__("math").sin(a)), V(1, 0, 0))
        plaat = plaat.fuse(rib)
    return plaat.removeSplitter()


def maak_symbool():
    """Motorsymbool (cirkel met M) tussen bussen en staander, met een draad naar elke bus."""
    z = HOOGTE - SYMBOOL_DIEPTE
    vorm = symbolen.plaats(symbolen.generator(SYMBOOL_DIEPTE, SYMBOOL_LIJN, SYMBOOL_D, "M"), SYMBOOL_X, 0, z)
    for _, y, _ in BUSSEN:
        richting = 1 if y > 0 else -1
        draad = symbolen.lijn((SYMBOOL_X, richting * SYMBOOL_D / 2), (SYMBOOL_X, y),
                              SYMBOOL_LIJN, SYMBOOL_DIEPTE)
        draad = draad.fuse(symbolen.lijn((SYMBOOL_X, y), (BUS_X + BUS_KRAAG_D / 2 - 0.5, y),
                                         SYMBOOL_LIJN, SYMBOOL_DIEPTE))
        vorm = vorm.fuse(symbolen.plaats(draad, 0, 0, z))
    return vorm


def maak_motor():
    """SOL300 vereenvoudigd: motorhuis door de staander, as naar voren (+X)."""
    voor = STAND_X + STAND_DIKTE / 2 + 1.0
    huis = Part.makeCylinder(MOTOR_D / 2, MOTOR_L, V(voor - MOTOR_L, 0, Z_AS), V(1, 0, 0))
    lager = Part.makeCylinder(3.0, 1.5, V(voor, 0, Z_AS), V(1, 0, 0))
    a = Part.makeCylinder(1.0, AS_L, V(voor, 0, Z_AS), V(1, 0, 0))
    return huis.fuse(lager).fuse(a)


def maak_propeller_op_as():
    vorm = propeller.maak_propeller()
    vorm.rotate(V(0, 0, 0), V(0, 1, 0), 90)            # naaf langs +X
    vorm.translate(V(STAND_X + STAND_DIKTE / 2 + 1.0 + 2.0, 0, Z_AS))
    return vorm


def maak_bouwplaat():
    """Stuk LEGO-bouwplaat met noppen, alleen ter controle van de passing."""
    nx, ny = NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H,
                                V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


def maak_bus(y):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(BUS_X, y, HOOGTE))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, PLAAT + 16, V(BUS_X, y, HOOGTE - PLAAT - 16))
    lip = doos(BUS_X - 3, y - 0.4, BUS_X + 3, y + 0.4, HOOGTE - BUS_ACHTER, HOOGTE - PLAAT - 16)
    gat = Part.makeCylinder(2.0, 20, V(BUS_X, y, HOOGTE + BUS_KRAAG_H - 20))
    return kraag.fuse(schacht).fuse(lip).cut(gat)


def maak_moer(y):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(BUS_X, y, HOOGTE - PLAAT - 5))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(BUS_X, y, HOOGTE - PLAAT - 6)))


doc = App.newDocument("Motorhouder")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (0, HB - WAND - 6, 0), (0, -(HB - WAND - 6), 0), (0, 0, 0),
    (-(HL - WAND - 6), 0, 90), (HL - WAND - 6, 0, 90)])
print("Handtekening op", plek)
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, (0.04, 0.16, 0.54)),
              ("Standaard", maak_standaard(), (0.04, 0.16, 0.54)),
              ("Motor", maak_motor(), (0.75, 0.75, 0.78)),
              ("Propeller", maak_propeller_op_as(), (0.30, 0.45, 0.85)),
              ("Bouwplaat_controle", maak_bouwplaat(), (0.75, 0.75, 0.75))]
if symbool:
    onderdelen.insert(1, ("Symbool", symbool, (0.96, 0.96, 0.96)))
for naam, y, kleur in BUSSEN:
    onderdelen.append(("Bus_" + naam, maak_bus(y), kleur))
    onderdelen.append(("Moer_" + naam, maak_moer(y), (0.6, 0.6, 0.6)))
for naam, vorm, kleur in onderdelen:
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
    print(naam, "geldig:", vorm.isValid(), "volume: %.0f mm3" % vorm.Volume)
doc.recompute()
bb = doc.Houder.Shape.BoundBox
print("Houder buitenmaten: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
sb = doc.Standaard.Shape.BoundBox
print("Standaard: %.1f x %.1f x %.1f mm" % (sb.XLength, sb.YLength, sb.ZLength))
for obj in doc.Objects:
    if obj.Name not in ("Houder",):
        overlap = doc.Houder.Shape.common(obj.Shape)
        print("Overlap houder/%s: %.3f mm3" % (obj.Name, overlap.Volume))
        if obj.Name == "Bouwplaat_controle":   # hier hoort alleen de klemoverlap van de ribben te zitten
            print("  klemplekken: %d" % len(overlap.Solids))
for naam in ("Motor", "Propeller"):
    print("Overlap standaard/%s: %.3f mm3" % (naam, doc.Standaard.Shape.common(doc.getObject(naam).Shape).Volume))
pb = doc.Propeller.Shape.BoundBox
print("Propeller: laagste punt %.1f mm boven de doos, x %.1f tot %.1f" % (pb.ZMin - HOOGTE, pb.XMin, pb.XMax))

map_ = MAP
doc.saveAs(os.path.join(map_, "Motorhouder.FCStd"))
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []), os.path.join(map_, "Motorhouder-Houder.step"))
Part.export([doc.Standaard], os.path.join(map_, "Motorhouder-Standaard.step"))
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(map_, "Motorhouder-Pastest.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Motorhouder.png"), 1400, 1000, "White")
    for naam in ("Propeller", "Motor", "Standaard"):
        doc.getObject(naam).ViewObject.Visibility = False
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Motorhouder_bovenaanzicht.png"), 1000, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
