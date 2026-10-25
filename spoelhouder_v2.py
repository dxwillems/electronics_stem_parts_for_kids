# Spoelhouder versie 2: kleine, sterke spoel waar het ijzerpoederdoosje plat op ligt.
# Verbeteringen t.o.v. versie 1:
#  - dunne kern (10,4 mm) met een gat voor een M6-bout als ijzeren kern: met dezelfde draad
#    ca. twee keer zoveel windingen bij dezelfde weerstand, dus veel meer veld;
#  - flenzen boven en onder plat, net boven de wikkeling: het doosje ligt vlak op de spoel;
#  - banaanbussen in de voorkant: de stekkers zitten niet onder het doosje;
#  - drie kuiltjes voor mini-kompasjes (19,6 x 3 mm): links en rechts bij de polen, en achter.
# Delen: Houder (doos, LEGO 12 x 10 noppen), Wieg (met 4 schroefjes M3 x 8 vast), Koker (met
# flenzen, op zijn kant printen met support onder de buis). Koker en wieg bij voorkeur in PETG.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD spoelhouder_v2.py

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
NOPPEN_L = 12           # 96 mm
NOPPEN_B = 10           # 80 mm
HOOGTE = 35.2
WAND = 2.4
PLAAT = 3.5
R_HOEK = 3.0

# ---------------------------------------------------------------- spoel
DRAAD_D = 0.3
RUIMTE_PER_WINDING = 0.25   # mm2 doorsnede per winding met de hand gewikkeld (perfect: ca. 0,08;
                            # gelakt draad is ca. 0,34 mm dik en ligt niet perfect). Meet je spoel na en pas aan.
DRAAD_M = 50.0          # zoveel draad gaat erop (de flenzen worden er net hoog genoeg voor)
GAT_D = 6.4             # M6-bout als ijzeren kern
KERN_D = 10.4
STOMP_D = 10.0          # uiteinden die in de wieg klikken
WIKKEL_L = 30.0
FLENS_DIKTE = 2.5
FLENS_R = 2.0
FLENS_BOVEN = 0.6       # flens steekt zoveel boven de volle wikkeling uit
DRAADGAATJE_D = 1.2
ANKERGAATJE_D = 1.6

# ---------------------------------------------------------------- wieg
SPOEL_Y = -4.0          # hartlijn van de spoel (langs X)
VOET_D = 5.0
EINDPLAAT_D = 4.0
SPELING_FLENS = 1.0     # tussen flens en eindplaat
KLIK_OPENING = 9.2      # opening bovenin de eindplaat; kleiner dan de stomp = klikt vast
SCHROEF_GAT_D = 3.4
SCHROEF_KERN_D = 2.5
SCHROEF_DIEPTE = 4.5
DRAADGAT_D = 6.0

# ---------------------------------------------------------------- kompasjes, bussen, symbool
KOMPAS_D = 19.62 + 0.3  # gemeten 19,62 mm
KOMPAS_DIEPTE = 2.5     # kompasje is 3 mm dik: steekt 0,5 mm uit
BUS_AFSTAND = 30.0      # hart-op-hart (langs X), in de voorkant
BUS_Z = 20.0            # hoogte hart bus boven de onderkant
BUS_GAT_D = 12.2
BUS_KRAAG_D = 16.0
BUS_KRAAG_H = 5.5
BUS_MOER_D = 17.0
BUS_ACHTER = 28.0
SYMBOOL_DIEPTE = 0.4
SYMBOOL_LIJN = 1.0

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


def wikkeling_berekenen():
    """Dikte t van de wikkeling uit: wikkeldoorsnede (L x t) = windingen x ruimte per winding,
    met windingen = draadlengte / gemiddelde omtrek pi * (kern + t)."""
    k = RUIMTE_PER_WINDING * DRAAD_M * 1000 / (WIKKEL_L * math.pi)
    t = (-KERN_D + math.sqrt(KERN_D ** 2 + 4 * k)) / 2
    windingen = DRAAD_M * 1000 / (math.pi * (KERN_D + t))
    weerstand = DRAAD_M * 0.0175 / (math.pi * (DRAAD_D / 2) ** 2)
    return round(t / (DRAAD_D * 1.1)), int(windingen), KERN_D + 2 * t, weerstand


LAGEN, WINDINGEN, BUITEN_D, WEERSTAND = wikkeling_berekenen()
FLENS_HALF_H = BUITEN_D / 2 + FLENS_BOVEN            # flens boven en onder plat
FLENS_B = 2 * FLENS_HALF_H                           # flens vierkant, net groter dan de wikkeling
STOMP_L = FLENS_DIKTE + SPELING_FLENS + EINDPLAAT_D
KOKER_L = WIKKEL_L + 2 * STOMP_L
AS_HOOGTE = VOET_D + FLENS_HALF_H + 1.0               # hart spoel boven de doos
Z_AS = HOOGTE + AS_HOOGTE
VOET_HX, VOET_Y0, VOET_Y1 = KOKER_L / 2, SPOEL_Y - FLENS_B / 2 - 4, SPOEL_Y + FLENS_B / 2 + 4
SCHROEVEN = [(sx * (VOET_HX - 4), y) for sx in (-1, 1) for y in (VOET_Y0 + 4, VOET_Y1 - 4)]
KOMPASSEN = [(-(HL - WAND - KOMPAS_D / 2 - 1.5), SPOEL_Y), (HL - WAND - KOMPAS_D / 2 - 1.5, SPOEL_Y),
             (0, VOET_Y1 + 2 + KOMPAS_D / 2)]


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
    ribben = [e for e in blok.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1]
    blok = blok.makeFillet(R_HOEK, ribben)
    sleuf = binnen(SLEUF_BUITEN, -1, SLEUF_DIEPTE).cut(binnen(SLEUF_BINNEN, -2, SLEUF_DIEPTE + 1))
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
    houder = houder.cut(Part.makeCylinder(DRAADGAT_D / 2, PLAAT + 2, V(0, SPOEL_Y, HOOGTE - PLAAT - 1)))
    for x, y in KOMPASSEN:
        houder = houder.cut(Part.makeCylinder(KOMPAS_D / 2, KOMPAS_DIEPTE + 1, V(x, y, HOOGTE - KOMPAS_DIEPTE)))
    for _, x, _ in BUSSEN:            # bussen horizontaal in de voorkant
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, 10, V(x, -HB - 1, BUS_Z), V(0, 1, 0)))
    return houder.removeSplitter()


def maak_symbool():
    """Spoelsymbool vooraan op de bovenkant."""
    ruimte = BUS_AFSTAND - 4
    vorm = symbolen.spoel(ruimte, SYMBOOL_DIEPTE, SYMBOOL_LIJN, 4, (ruimte - 4.0) / 8)
    return symbolen.plaats(vorm, 0, -(HB - WAND - 6), HOOGTE - SYMBOOL_DIEPTE)


def maak_wieg():
    wieg = doos(-VOET_HX, VOET_Y0, VOET_HX, VOET_Y1, HOOGTE, HOOGTE + VOET_D)
    r_stomp = STOMP_D / 2 + 0.1
    top = Z_AS + r_stomp + 2.0
    for sx in (-1, 1):
        xa, xb = sorted((sx * VOET_HX, sx * (VOET_HX - EINDPLAAT_D)))
        plaat = doos(xa, VOET_Y0, xb, VOET_Y1, HOOGTE, top)
        uitsparing = Part.makeCylinder(r_stomp, EINDPLAAT_D + 2, V(xa - 1, SPOEL_Y, Z_AS), V(1, 0, 0))
        uitsparing = uitsparing.fuse(doos(xa - 1, SPOEL_Y - KLIK_OPENING / 2, xb + 1, SPOEL_Y + KLIK_OPENING / 2,
                                          Z_AS, top + 1))
        wieg = wieg.fuse(plaat.cut(uitsparing))
    for x, y in SCHROEVEN:
        wieg = wieg.cut(Part.makeCylinder(SCHROEF_KERN_D / 2, SCHROEF_DIEPTE, V(x, y, HOOGTE)))
    wieg = wieg.cut(Part.makeCylinder(DRAADGAT_D / 2, VOET_D + 2, V(0, SPOEL_Y, HOOGTE - 1)))
    return wieg.removeSplitter()


def maak_flens(sx):
    x = WIKKEL_L / 2 if sx > 0 else -WIKKEL_L / 2 - FLENS_DIKTE
    h = FLENS_HALF_H
    flens = doos(x, SPOEL_Y - FLENS_B / 2, x + FLENS_DIKTE, SPOEL_Y + FLENS_B / 2, Z_AS - h, Z_AS + h)
    ribben = [e for e in flens.Edges if abs(e.Vertexes[0].Point.x - e.Vertexes[-1].Point.x) > 1]
    flens = flens.makeFillet(FLENS_R, ribben)
    for r in (KERN_D / 2 + 0.8, BUITEN_D / 2 - 0.4):          # begin- en eindgaatje, schuin naast de as
        flens = flens.cut(Part.makeCylinder(DRAADGAATJE_D / 2, FLENS_DIKTE + 2,
                                            V(x - 1, SPOEL_Y + r, Z_AS), V(1, 0, 0)))
    for dz in (-2.0, 2.0):                                        # ankergaatjes aan de zijkant
        flens = flens.cut(Part.makeCylinder(ANKERGAATJE_D / 2, FLENS_DIKTE + 2,
                                            V(x - 1, SPOEL_Y - FLENS_B / 2 + 2.5, Z_AS + dz), V(1, 0, 0)))
    return flens


def maak_koker():
    koker = Part.makeCylinder(KERN_D / 2, WIKKEL_L, V(-WIKKEL_L / 2, SPOEL_Y, Z_AS), V(1, 0, 0))
    for sx in (-1, 1):
        start = -KOKER_L / 2 if sx < 0 else WIKKEL_L / 2
        koker = koker.fuse(Part.makeCylinder(STOMP_D / 2, STOMP_L, V(start, SPOEL_Y, Z_AS), V(1, 0, 0)))
        koker = koker.fuse(maak_flens(sx))
    koker = koker.cut(Part.makeCylinder(GAT_D / 2, KOKER_L + 2, V(-KOKER_L / 2 - 1, SPOEL_Y, Z_AS), V(1, 0, 0)))
    return koker.removeSplitter()


def maak_wikkeling():
    w = Part.makeCylinder(BUITEN_D / 2, WIKKEL_L - 0.2, V(-WIKKEL_L / 2 + 0.1, SPOEL_Y, Z_AS), V(1, 0, 0))
    return w.cut(Part.makeCylinder(KERN_D / 2, WIKKEL_L + 2, V(-WIKKEL_L / 2 - 1, SPOEL_Y, Z_AS), V(1, 0, 0)))


def maak_bout():
    return Part.makeCylinder(3.0, 60, V(-30, SPOEL_Y, Z_AS), V(1, 0, 0))


def maak_kompassen():
    return [Part.makeCylinder(19.62 / 2, 3.0, V(x, y, HOOGTE - KOMPAS_DIEPTE)) for x, y in KOMPASSEN]


def maak_doosje():
    """IJzerpoederdoosje (frame 11,2 mm) zoals het op de flenzen ligt."""
    z = Z_AS + FLENS_HALF_H
    return doos(-81, SPOEL_Y - 54, 81, SPOEL_Y + 54, z, z + 11.2)


def maak_bus(x):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(x, -HB - BUS_KRAAG_H, BUS_Z), V(0, 1, 0))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, WAND + 16, V(x, -HB, BUS_Z), V(0, 1, 0))
    gat = Part.makeCylinder(2.0, 20, V(x, -HB - BUS_KRAAG_H - 1, BUS_Z), V(0, 1, 0))
    return kraag.fuse(schacht).cut(gat)


def maak_moer(x):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(x, -HB + WAND + 0.1, BUS_Z), V(0, 1, 0))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(x, -HB, BUS_Z), V(0, 1, 0)))


def maak_bouwplaat():
    nx, ny = NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H, V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


doc = App.newDocument("SpoelhouderV2")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (0, 0, 0), (0, HB - WAND - 4, 0), (-(HL - WAND - 6), -20, 90), (HL - WAND - 6, -20, 90)])
print("Handtekening op", plek)
symbool = maak_symbool()
blauw = (0.04, 0.16, 0.54)
onderdelen = [("Houder", houder.cut(symbool), blauw), ("Symbool", symbool, (0.96, 0.96, 0.96)),
              ("Wieg", maak_wieg(), blauw), ("Koker", maak_koker(), blauw),
              ("Wikkeling", maak_wikkeling(), (0.80, 0.50, 0.25)), ("Bout_M6", maak_bout(), (0.6, 0.6, 0.6)),
              ("Doosje", maak_doosje(), (0.85, 0.92, 1.0)), ("Bouwplaat_controle", maak_bouwplaat(), (0.75, 0.75, 0.75))]
for i, k in enumerate(maak_kompassen()):
    onderdelen.append(("Kompas_%d" % (i + 1), k, (0.1, 0.1, 0.1)))
for naam, x, kleur in BUSSEN:
    onderdelen.append(("Bus_" + naam, maak_bus(x), kleur))
    onderdelen.append(("Moer_" + naam, maak_moer(x), (0.6, 0.6, 0.6)))
for naam, vorm, kleur in onderdelen:
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
        if naam == "Doosje":
            obj.ViewObject.Transparency = 70
    print(naam, "geldig:", vorm.isValid())
doc.recompute()
print("Wikkeling %.0f m: %d lagen, ca. %d windingen, buitendiameter %.1f mm, ca. %.1f ohm, %.2f A op 5 V, NI = %.0f"
      % (DRAAD_M, LAGEN, WINDINGEN, BUITEN_D, WEERSTAND, 5 / WEERSTAND, WINDINGEN * 5 / WEERSTAND))
print("Afstand wikkeling tot onderkant doosje: %.1f mm" % FLENS_BOVEN)
for a in ("Houder", "Wieg", "Koker"):
    for b in [o.Name for o in doc.Objects if o.Name not in ("Houder", "Wieg", "Koker", "Bouwplaat_controle", a)]:
        if a == "Houder" and b == "Symbool":
            continue
        v = doc.getObject(a).Shape.common(doc.getObject(b).Shape).Volume
        if v > 0.001 and not (a == "Koker" and b == "Bout_M6"):
            print("Overlap %s/%s: %.3f" % (a, b, v))
for a, b in (("Houder", "Wieg"), ("Houder", "Koker"), ("Wieg", "Koker")):
    print("Overlap %s/%s: %.3f" % (a, b, doc.getObject(a).Shape.common(doc.getObject(b).Shape).Volume))
dz = doc.Doosje.Shape.BoundBox.ZMin - max(doc.Wieg.Shape.BoundBox.ZMax, doc.Koker.Shape.BoundBox.ZMax)
print("Doosje ligt op de flenzen; ruimte tot wieg: %.1f mm" % (doc.Doosje.Shape.BoundBox.ZMin - doc.Wieg.Shape.BoundBox.ZMax))

doc.saveAs(os.path.join(MAP, "Spoelhouder_V2.FCStd"))
Part.export([doc.Houder, doc.Symbool], os.path.join(MAP, "Spoelhouder_V2-Houder.step"))
for naam in ("Wieg", "Koker"):
    Part.export([doc.getObject(naam)], os.path.join(MAP, "Spoelhouder_V2-%s.step" % naam))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    doc.Doosje.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(MAP, "Spoelhouder_V2.png"), 1400, 1000, "White")
    doc.Doosje.ViewObject.Visibility = True
    view.viewFront()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(MAP, "Spoelhouder_V2_met_doosje.png"), 1400, 900, "White")
    view.viewIsometric()
    view.fitAll()
    doc.save()
