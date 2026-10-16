# Ronde spoel (buisspoel) op een LEGO-doos, voor 100 m gelakt koperdraad van 0,3 mm.
# Drie delen om te printen (koker en wieg bij voorkeur in PETG, dat kan meer warmte aan):
#  - Houder: doos met twee 4 mm paneelbussen (12 mm montagegat) en het spoelsymbool;
#    onderkant klemt op een LEGO-bouwplaat (10 x 10 noppen).
#  - Wieg: voetplaat met twee eindplaten; de koker klikt met zijn uiteinden in de eindplaten.
#  - Koker: buis met een gat van 20,4 mm (voor een staafmagneet of ijzeren staaf) en twee
#    vierkante flenzen eraan vast. Print hem op zijn kant (flensranden op het bed) met support
#    alleen onder de buis tussen de flenzen. In elke flens zitten gaatjes voor de draadeinden.
# De spoel klikt los uit de wieg. Door de vierkante flenzen ligt hij stabiel op tafel en kun je
# het ijzerpoederdoosje er plat op leggen of de spoel er met een vlakke kant tegenaan houden.
# Gebruik daarvoor soepele aansluitdraadjes van ca. 25 cm tussen spoel en bussen.
# Wieg en doos: vier schroefjes M3 x 8 (of plaatschroef 2,9 x 9,5) van binnenuit de doos.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD spoelhouder_rond.py
#
# Wikkeling: alle 100 m van 0,3 mm op een kern van 24,4 mm over 40 mm lengte geeft ongeveer
# 10 lagen, ca. 1200 windingen en ca. 24 ohm (0,3 mm koper: 0,243 ohm/m). Op 5 V loopt er dan
# ongeveer 0,2 A (1 W). De busmaten onder de plaat zijn geschat.

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

# ---------------------------------------------------------------- maten doos
NOPPEN_L = 10           # 80 mm
NOPPEN_B = 10           # 80 mm
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
R_HOEK = 3.0

# ---------------------------------------------------------------- spoel
GAT_D = 20.4            # doorgang voor een magneet of ijzeren staaf
KERN_D = 24.4           # buitenkant koker onder de wikkeling
STOMP_D = 23.6          # uiteinden van de koker: flens schuift erover tot tegen de rand
WIKKEL_L = 40.0
STOMP_L = 7.5           # per kant: flens (2,5) + stuk in de eindplaat
FLENS_D = 40.0          # vierkante flens, zijde
FLENS_R = 3.0           # afronding hoeken
FLENS_DIKTE = 2.5
FLENS_SPELING = 0.1     # boring van de flens t.o.v. de stomp (lijmen)
DRAADGAATJE_D = 1.2     # in de flens: begin (bij de kern) en einde (buiten de wikkeling)
ANKERGAATJE_D = 1.6     # twee gaatjes in een flenshoek om de soepele aansluitdraad vast te zetten
DRAAD_D = 0.3
DRAAD_M = 100.0

# ---------------------------------------------------------------- wieg
WIEG_Y = 12.0           # hartlijn van de spoel (langs X) ligt hier
WIEG_B = 44.0           # breedte van voetplaat en eindplaten (langs Y)
VOET_D = 5.0            # dikte voetplaat (dik genoeg voor de schroefjes)
EINDPLAAT_D = 4.0
AS_HOOGTE = 27.0        # hart van de spoel boven de doos: flens 2 mm vrij van de voetplaat
KLIK_OPENING = 22.6     # opening bovenin de eindplaat; kleiner dan de stomp = klikt vast
SCHROEF_GAT_D = 3.4     # doorgang in de bovenplaat van de doos
SCHROEF_KERN_D = 2.5    # voorboorgat in de voetplaat
SCHROEF_DIEPTE = 4.5
SCHROEVEN = [(-23.0, WIEG_Y - 18.0), (23.0, WIEG_Y - 18.0), (-23.0, WIEG_Y + 18.0), (23.0, WIEG_Y + 18.0)]
DRAADGAT_D = 6.0        # midden onder de spoel, door voetplaat en doos

# ---------------------------------------------------------------- bussen en symbool
BUS_AFSTAND = 40.0      # hart-op-hart (langs X)
BUS_Y = -21.0
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
KOKER_L = WIKKEL_L + 2 * STOMP_L
Z_AS = HOOGTE + AS_HOOGTE
BUSSEN = [("rood", -BUS_AFSTAND / 2, (0.85, 0.10, 0.10)),
          ("zwart", BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]

RASTER = Part.Face(Part.makePolygon([V(*p) for p in (
    (-HL, -HB), (HL, -HB), (HL, HB), (-HL, HB), (-HL, -HB))]))


def wikkeling_berekenen():
    """Lagen, windingen en buitendiameter als de hele rol op de koker gaat."""
    per_laag = WIKKEL_L / DRAAD_D
    laag_dikte = DRAAD_D * 0.9
    lengte, lagen, d = 0.0, 0, KERN_D
    while lengte < DRAAD_M * 1000:
        lengte += per_laag * math.pi * (d + laag_dikte)
        d += 2 * laag_dikte
        lagen += 1
    weerstand = DRAAD_M * 0.0175 / (math.pi * (DRAAD_D / 2) ** 2)
    return lagen, int(lagen * per_laag), d, weerstand


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


lagen, windingen, BUITEN_D, weerstand = wikkeling_berekenen()
buiten_d = BUITEN_D


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

    for x, y in SCHROEVEN:
        houder = houder.cut(Part.makeCylinder(SCHROEF_GAT_D / 2, PLAAT + 2, V(x, y, HOOGTE - PLAAT - 1)))
    houder = houder.cut(Part.makeCylinder(DRAADGAT_D / 2, PLAAT + 2, V(0, WIEG_Y, HOOGTE - PLAAT - 1)))
    for _, x, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2, V(x, BUS_Y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_symbool():
    """Spoelsymbool tussen de twee bussen."""
    ruimte = BUS_AFSTAND - BUS_KRAAG_D
    vorm = symbolen.spoel(ruimte + 1.0, SYMBOOL_DIEPTE, SYMBOOL_LIJN, 4, (ruimte - 4.0) / 8)
    return symbolen.plaats(vorm, 0, BUS_Y, HOOGTE - SYMBOOL_DIEPTE)


def maak_wieg():
    """Voetplaat met twee eindplaten; de uiteinden van de koker klikken in de eindplaten."""
    x1 = KOKER_L / 2
    y0, y1 = WIEG_Y - WIEG_B / 2, WIEG_Y + WIEG_B / 2
    wieg = doos(-x1, y0, x1, y1, HOOGTE, HOOGTE + VOET_D)
    r_stomp = STOMP_D / 2 + 0.1
    top = Z_AS + r_stomp + 3.0
    for sx in (-1, 1):
        xa, xb = sorted((sx * x1, sx * (x1 - EINDPLAAT_D)))
        plaat = doos(xa, y0, xb, y1, HOOGTE, top)
        uitsparing = Part.makeCylinder(r_stomp, EINDPLAAT_D + 2, V(xa - 1, WIEG_Y, Z_AS), V(1, 0, 0))
        uitsparing = uitsparing.fuse(doos(xa - 1, WIEG_Y - KLIK_OPENING / 2, xb + 1,
                                          WIEG_Y + KLIK_OPENING / 2, Z_AS, top + 1))
        wieg = wieg.fuse(plaat.cut(uitsparing))
    for x, y in SCHROEVEN:
        wieg = wieg.cut(Part.makeCylinder(SCHROEF_KERN_D / 2, SCHROEF_DIEPTE, V(x, y, HOOGTE)))
    wieg = wieg.cut(Part.makeCylinder(DRAADGAT_D / 2, VOET_D + 2, V(0, WIEG_Y, HOOGTE - 1)))
    return wieg.removeSplitter()


def maak_flens(sx):
    """Vierkante flens tegen het wikkelstuk, met gaatjes voor begin- en einddraad en twee
    ankergaatjes in een hoek."""
    x = WIKKEL_L / 2 if sx > 0 else -WIKKEL_L / 2 - FLENS_DIKTE
    h = FLENS_D / 2
    flens = doos(x, WIEG_Y - h, x + FLENS_DIKTE, WIEG_Y + h, Z_AS - h, Z_AS + h)
    ribben = [e for e in flens.Edges if abs(e.Vertexes[0].Point.x - e.Vertexes[-1].Point.x) > 1]
    flens = flens.makeFillet(FLENS_R, ribben)
    gaatjes = [(KERN_D / 2 + 1.0, DRAADGAATJE_D), (BUITEN_D / 2 + 1.5, DRAADGAATJE_D)]
    for r, d in gaatjes:
        flens = flens.cut(Part.makeCylinder(d / 2, FLENS_DIKTE + 2, V(x - 1, WIEG_Y, Z_AS - r), V(1, 0, 0)))
    for dy in (-2.5, 2.5):          # ankergaatjes onderin, naast elkaar
        flens = flens.cut(Part.makeCylinder(ANKERGAATJE_D / 2, FLENS_DIKTE + 2,
                                            V(x - 1, WIEG_Y + h - 6 + dy, Z_AS - h + 6), V(1, 0, 0)))
    return flens


def maak_koker():
    """Buis langs X met twee vierkante flenzen eraan vast; de stompen klikken in de wieg."""
    x0 = -KOKER_L / 2
    koker = Part.makeCylinder(KERN_D / 2, WIKKEL_L, V(-WIKKEL_L / 2, WIEG_Y, Z_AS), V(1, 0, 0))
    for sx in (-1, 1):
        start = -KOKER_L / 2 if sx < 0 else WIKKEL_L / 2
        koker = koker.fuse(Part.makeCylinder(STOMP_D / 2, STOMP_L, V(start, WIEG_Y, Z_AS), V(1, 0, 0)))
        koker = koker.fuse(maak_flens(sx))
    koker = koker.cut(Part.makeCylinder(GAT_D / 2, KOKER_L + 2, V(x0 - 1, WIEG_Y, Z_AS), V(1, 0, 0)))
    return koker.removeSplitter()


def maak_wikkeling(buiten_d):
    w = Part.makeCylinder(buiten_d / 2, WIKKEL_L - 0.2, V(-WIKKEL_L / 2 + 0.1, WIEG_Y, Z_AS), V(1, 0, 0))
    return w.cut(Part.makeCylinder(KERN_D / 2, WIKKEL_L + 2, V(-WIKKEL_L / 2 - 1, WIEG_Y, Z_AS), V(1, 0, 0)))


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



doc = App.newDocument("SpoelhouderRond")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (0, HB - WAND - 6, 0), (0, -(HB - WAND - 6), 0), (0, 0, 0),
    (-(HL - WAND - 6), 0, 90), (HL - WAND - 6, 0, 90)])
print("Handtekening op", plek)
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
blauw = (0.04, 0.16, 0.54)
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, blauw),
              ("Wieg", maak_wieg(), blauw),
              ("Koker", maak_koker(), blauw),
              ("Wikkeling", maak_wikkeling(buiten_d), (0.80, 0.50, 0.25)),
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
print("Wikkeling: %d lagen, ca. %d windingen, buitendiameter %.1f mm (flens %.0f), ca. %.0f ohm, %.2f A op 5 V"
      % (lagen, windingen, buiten_d, FLENS_D, weerstand, 5.0 / weerstand))
bb = doc.Houder.Shape.BoundBox
print("Houder buitenmaten: %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
paren = [("Houder", n) for n in ("Symbool", "Wieg", "Koker", "Bus_rood", "Moer_rood",
                                 "Bus_zwart", "Moer_zwart", "Bouwplaat_controle")]
paren += [("Wieg", "Koker"), ("Wieg", "Wikkeling"), ("Koker", "Wikkeling"), ("Wieg", "Bus_rood"),
          ("Wieg", "Bus_zwart")]
for a, b in paren:
    if doc.getObject(b):
        print("Overlap %s/%s: %.3f mm3" % (a, b, doc.getObject(a).Shape.common(doc.getObject(b).Shape).Volume))
print("Vrije opening onderkant: x +/- %.1f, y +/- %.1f; moeren y %.1f tot %.1f, x tot +/- %.1f"
      % (HL - RIB_BINNEN, HB - RIB_BINNEN, BUS_Y - BUS_MOER_D / 2, BUS_Y + BUS_MOER_D / 2,
         BUS_AFSTAND / 2 + BUS_MOER_D / 2))

doc.saveAs(os.path.join(MAP, "Spoelhouder_Rond.FCStd"))
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []), os.path.join(MAP, "Spoelhouder_Rond-Houder.step"))
for naam in ("Wieg", "Koker"):
    Part.export([doc.getObject(naam)], os.path.join(MAP, "Spoelhouder_Rond-%s.step" % naam))
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(MAP, "Spoelhouder_Rond-Pastest.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(MAP, "Spoelhouder_Rond.png"), 1400, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(MAP, "Spoelhouder_Rond_bovenaanzicht.png"), 1000, 1000, "White")
    view.viewIsometric()
    view.fitAll()
    doc.save()
