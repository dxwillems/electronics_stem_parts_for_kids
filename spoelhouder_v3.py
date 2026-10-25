# Spoelhouder versie 3: dezelfde spoel liggend OF rechtop te gebruiken.
#  - Koker: wikkeling met twee vierkante flenzen, zonder uitstekende stompjes; los op te pakken.
#  - Liggend: koker in het ondiepe vak; het ijzerpoederdoosje ligt op de flenzen (veldlijnen van
#    pool naar pool, zoals een staafmagneet van opzij).
#  - Rechtop: koker 12 mm diep in de put; het doosje ligt op de bovenflens, recht boven de pool.
#    Ruim drie keer zoveel veld bij het poeder (een pool, sterpatroon).
#  - M6-bout als ijzeren kern (M6 x 35), los zodat je met en zonder kern kunt vergelijken: rechtop
#    staat hij op zijn kop in een kuiltje in de putbodem; liggend valt de kop in een uitsparing.
#  - Banaanbussen in de voorkant, drie kuiltjes voor mini-kompasjes (19,6 x 3 mm).
# Delen: Houder (doos, LEGO 18 x 10 noppen, 14 platen hoog) en Koker (op zijn kant printen met
# support onder de buis, bij voorkeur PETG). Wikkelen met Wikkelhulp_V2 en een M6-bout.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD spoelhouder_v3.py

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
NOPPEN_L = 18           # 144 mm
NOPPEN_B = 10           # 80 mm
HOOGTE = 44.8           # 14 LEGO-platen: diep genoeg voor de rechtopstaande koker
WAND = 2.4
PLAAT = 3.5
R_HOEK = 3.0

# ---------------------------------------------------------------- spoel
DRAAD_D = 0.3
DRAAD_M = 50.0
RUIMTE_PER_WINDING = 0.25   # mm2 per winding met de hand gewikkeld; meet je spoel na en pas aan
GAT_D = 6.4             # M6-bout als ijzeren kern
KERN_D = 10.4
WIKKEL_L = 30.0
FLENS_DIKTE = 2.5
FLENS_R = 2.0
FLENS_BOVEN = 0.6
DRAADGAATJE_D = 1.2
ANKERGAATJE_D = 1.6

# ---------------------------------------------------------------- vak, put, kompasjes, bussen
SPELING = 0.4           # rond de koker in vak en put
VAK_DIEPTE = 10.0       # liggend: zo diep zakt de koker weg
VAK_BODEM = 2.0
VAK_X = -20.0
PUT_X = 46.0            # rechtop
SPOEL_Y = -4.0
PUT_WAND = 2.0
PUT_DIEPTE = 12.0       # rechtop: zo diep staat de koker in de put
PUT_BODEM = 6.5         # dik genoeg voor het kuiltje waar de boutkop in staat
BOUT_GAT_D = 6.6
BOUTKOP_D = 11.5 + 1.0  # M6 zeskantkop (11,5 over de hoeken) of cilinderkop (10), plus speling
BOUTKOP_H = 4.0 + 1.0
DRAADGAT_D = 3.5        # twee per vak/put, in de bodem: voor elke aansluitdraad een
KOMPAS_D = 19.62 + 0.3
KOMPAS_DIEPTE = 2.5
BUS_AFSTAND = 30.0
BUS_Z = 22.0
BUS_GAT_D = 12.2
BUS_KRAAG_D = 16.0
BUS_KRAAG_H = 5.5
BUS_MOER_D = 17.0
SYMBOOL_DIEPTE = 0.4
SYMBOOL_LIJN = 1.0

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
RASTER = Part.Face(Part.makePolygon([V(*p) for p in (
    (-HL, -HB), (HL, -HB), (HL, HB), (-HL, HB), (-HL, -HB))]))


def wikkeling_berekenen():
    k = RUIMTE_PER_WINDING * DRAAD_M * 1000 / (WIKKEL_L * math.pi)
    t = (-KERN_D + math.sqrt(KERN_D ** 2 + 4 * k)) / 2
    windingen = DRAAD_M * 1000 / (math.pi * (KERN_D + t))
    weerstand = DRAAD_M * 0.0175 / (math.pi * (DRAAD_D / 2) ** 2)
    return int(windingen), KERN_D + 2 * t, weerstand


WINDINGEN, BUITEN_D, WEERSTAND = wikkeling_berekenen()
FLENS = 2 * (BUITEN_D / 2 + FLENS_BOVEN)            # vierkante flens
KOKER_L = WIKKEL_L + 2 * FLENS_DIKTE
F = FLENS / 2 + SPELING
PUT_BODEM_Z = HOOGTE - PUT_DIEPTE                 # bovenkant bodem = onderkant koker
BUSSEN = [("rood", -BUS_AFSTAND / 2, (0.85, 0.10, 0.10)), ("zwart", BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]
KOMPAS_AFSTAND = KOKER_L / 2 + SPELING + 5.0 + 2.5 + KOMPAS_D / 2   # voorbij de uitsparing voor de boutkop
KOMPASSEN = [(VAK_X - KOMPAS_AFSTAND, SPOEL_Y), (VAK_X + KOMPAS_AFSTAND, SPOEL_Y),
             (VAK_X, SPOEL_Y + F + 3 + KOMPAS_D / 2)]


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
    for i in range(1, NOPPEN_L - 1, 2):   # rib bij elke tweede nop: grote doos
        x = -HL + (i + 0.5) * NOP_STEEK
        for sy in (-1, 1):
            plekken.append((x, sy * (HB - SLEUF_BINNEN - (r - uitsteek))))
    for j in range(1, NOPPEN_B - 1, 2):
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
    # put voor de rechtopstaande koker: wanden en bodem hangen onder de bovenplaat
    houder = houder.fuse(doos(PUT_X - F - PUT_WAND, SPOEL_Y - F - PUT_WAND, PUT_X + F + PUT_WAND,
                              SPOEL_Y + F + PUT_WAND, PUT_BODEM_Z - PUT_BODEM, HOOGTE))
    houder = houder.cut(doos(PUT_X - F, SPOEL_Y - F, PUT_X + F, SPOEL_Y + F, PUT_BODEM_Z, HOOGTE + 1))
    # rechtop staat de bout op zijn kop in een kuiltje in de bodem; de koker staat eroverheen
    houder = houder.cut(Part.makeCylinder(BOUTKOP_D / 2, BOUTKOP_H - 0.5 + 1, V(PUT_X, SPOEL_Y, PUT_BODEM_Z - (BOUTKOP_H - 0.5))))
    houder = houder.cut(Part.makeCylinder(BOUT_GAT_D / 2, PUT_BODEM + 2, V(PUT_X, SPOEL_Y, PUT_BODEM_Z - PUT_BODEM - 1)))
    for dx in (-1, 1):            # twee draadgaatjes in de hoeken van de putbodem
        houder = houder.cut(Part.makeCylinder(DRAADGAT_D / 2, PUT_BODEM + 2,
                                              V(PUT_X + dx * (F - 3.5), SPOEL_Y - F + 3.5, PUT_BODEM_Z - PUT_BODEM - 1)))
    # ondiep vak voor de liggende koker, met een draadgat
    vx = KOKER_L / 2 + SPELING
    houder = houder.fuse(doos(VAK_X - vx - PUT_WAND, SPOEL_Y - F - PUT_WAND, VAK_X + vx + PUT_WAND,
                              SPOEL_Y + F + PUT_WAND, HOOGTE - VAK_DIEPTE - VAK_BODEM, HOOGTE))
    houder = houder.cut(doos(VAK_X - vx, SPOEL_Y - F, VAK_X + vx, SPOEL_Y + F, HOOGTE - VAK_DIEPTE, HOOGTE + 1))
    z_as_liggend = HOOGTE - VAK_DIEPTE + FLENS / 2
    for dx in (-1, 1):            # ruimte voor de boutkop aan beide uiteinden (de bout kan beide kanten op)
        x0 = VAK_X + dx * vx
        houder = houder.cut(Part.makeCylinder(BOUTKOP_D / 2, BOUTKOP_H, V(min(x0, x0 + dx * BOUTKOP_H), SPOEL_Y,
                                                                         z_as_liggend), V(1, 0, 0)))
    for dx in (-1, 1):            # twee draadgaatjes, onder elke flens een
        houder = houder.cut(Part.makeCylinder(DRAADGAT_D / 2, VAK_BODEM + 2,
                                              V(VAK_X + dx * (KOKER_L / 2 - FLENS_DIKTE / 2), SPOEL_Y - F + 3.5,
                                                HOOGTE - VAK_DIEPTE - VAK_BODEM - 1)))
    for x, y in KOMPASSEN:
        houder = houder.cut(Part.makeCylinder(KOMPAS_D / 2, KOMPAS_DIEPTE + 1, V(x, y, HOOGTE - KOMPAS_DIEPTE)))
    for _, x, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, 10, V(x, -HB - 1, BUS_Z), V(0, 1, 0)))
    return houder.removeSplitter()


def maak_symbool():
    ruimte = BUS_AFSTAND - 4
    vorm = symbolen.spoel(ruimte, SYMBOOL_DIEPTE, SYMBOOL_LIJN, 4, (ruimte - 4.0) / 8)
    return symbolen.plaats(vorm, 0, -(HB - WAND - 6), HOOGTE - SYMBOOL_DIEPTE)


def maak_koker(midden, rechtop):
    """Koker met de as langs X (liggend) of Z (rechtop); midden = hart van de koker."""
    koker = Part.makeCylinder(KERN_D / 2, WIKKEL_L, V(-WIKKEL_L / 2, 0, 0), V(1, 0, 0))
    h = FLENS / 2
    for x in (WIKKEL_L / 2, -WIKKEL_L / 2 - FLENS_DIKTE):
        flens = doos(x, -h, x + FLENS_DIKTE, h, -h, h)
        ribben = [e for e in flens.Edges if abs(e.Vertexes[0].Point.x - e.Vertexes[-1].Point.x) > 1]
        flens = flens.makeFillet(FLENS_R, ribben)
        for r in (KERN_D / 2 + 0.8, BUITEN_D / 2 - 0.4):
            flens = flens.cut(Part.makeCylinder(DRAADGAATJE_D / 2, FLENS_DIKTE + 2, V(x - 1, r, 0), V(1, 0, 0)))
        for dz in (-2.0, 2.0):
            flens = flens.cut(Part.makeCylinder(ANKERGAATJE_D / 2, FLENS_DIKTE + 2, V(x - 1, -h + 2.5, dz), V(1, 0, 0)))
        koker = koker.fuse(flens)
    koker = koker.cut(Part.makeCylinder(GAT_D / 2, KOKER_L + 2, V(-KOKER_L / 2 - 1, 0, 0), V(1, 0, 0)))
    koker = koker.removeSplitter()
    if rechtop:
        koker.rotate(V(0, 0, 0), V(0, 1, 0), -90)
    koker.translate(midden)
    return koker


def maak_wikkeling(midden, rechtop):
    w = Part.makeCylinder(BUITEN_D / 2, WIKKEL_L - 0.2, V(-WIKKEL_L / 2 + 0.1, 0, 0), V(1, 0, 0))
    w = w.cut(Part.makeCylinder(KERN_D / 2, WIKKEL_L + 2, V(-WIKKEL_L / 2 - 1, 0, 0), V(1, 0, 0)))
    if rechtop:
        w.rotate(V(0, 0, 0), V(0, 1, 0), -90)
    w.translate(midden)
    return w


def maak_bus(x):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(x, -HB - BUS_KRAAG_H, BUS_Z), V(0, 1, 0))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, WAND + 16, V(x, -HB, BUS_Z), V(0, 1, 0))
    return kraag.fuse(schacht).cut(Part.makeCylinder(2.0, 20, V(x, -HB - BUS_KRAAG_H - 1, BUS_Z), V(0, 1, 0)))


def maak_moer(x):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(x, -HB + WAND + 0.1, BUS_Z), V(0, 1, 0))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(x, -HB, BUS_Z), V(0, 1, 0)))


def maak_bouwplaat():
    nx, ny = NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H, V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


z_liggend = HOOGTE - VAK_DIEPTE + FLENS / 2
z_rechtop = PUT_BODEM_Z + KOKER_L / 2
doc = App.newDocument("SpoelhouderV3")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (VAK_X, SPOEL_Y + 22, 0), (-20, HB - WAND - 4, 0), (VAK_X, -(HB - WAND - 6), 0)])
print("Handtekening op", plek)
symbool = maak_symbool()
blauw = (0.04, 0.16, 0.54)
onderdelen = [("Houder", houder.cut(symbool), blauw), ("Symbool", symbool, (0.96, 0.96, 0.96)),
              ("Koker", maak_koker(V(VAK_X, SPOEL_Y, z_liggend), False), blauw),
              ("Wikkeling", maak_wikkeling(V(VAK_X, SPOEL_Y, z_liggend), False), (0.80, 0.50, 0.25)),
              ("Koker_rechtop", maak_koker(V(PUT_X, SPOEL_Y, z_rechtop), True), (0.30, 0.45, 0.85)),
              ("Wikkeling_rechtop", maak_wikkeling(V(PUT_X, SPOEL_Y, z_rechtop), True), (0.80, 0.50, 0.25)),
              ("Bout_M6", Part.makeCylinder(3.0, 35, V(PUT_X, SPOEL_Y, PUT_BODEM_Z - 0.5)).fuse(
                  Part.makeCylinder(5.75, 4.0, V(PUT_X, SPOEL_Y, PUT_BODEM_Z - 4.5))), (0.6, 0.6, 0.6)),
              ("Bout_M6_liggend", Part.makeCylinder(3.0, 35, V(VAK_X - KOKER_L / 2, SPOEL_Y, z_liggend), V(1, 0, 0)).fuse(
                  Part.makeCylinder(5.75, 4.0, V(VAK_X + KOKER_L / 2, SPOEL_Y, z_liggend), V(1, 0, 0))), (0.6, 0.6, 0.6)),
              ("Bouwplaat_controle", maak_bouwplaat(), (0.75, 0.75, 0.75))]
for i, (x, y) in enumerate(KOMPASSEN):
    onderdelen.append(("Kompas_%d" % (i + 1), Part.makeCylinder(19.62 / 2, 3.0, V(x, y, HOOGTE - KOMPAS_DIEPTE)), (0.1, 0.1, 0.1)))
for naam, x, kleur in BUSSEN:
    onderdelen.append(("Bus_" + naam, maak_bus(x), kleur))
    onderdelen.append(("Moer_" + naam, maak_moer(x), (0.6, 0.6, 0.6)))
for naam, vorm, kleur in onderdelen:
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
    if not vorm.isValid():
        print(naam, "ONGELDIG")
doc.recompute()
print("Wikkeling %.0f m: ca. %d windingen, buitendiameter %.1f mm, flens %.1f mm, koker %.1f mm lang, %.1f ohm"
      % (DRAAD_M, WINDINGEN, BUITEN_D, FLENS, KOKER_L, WEERSTAND))
for b in [o.Name for o in doc.Objects if o.Name not in ("Houder", "Symbool", "Bouwplaat_controle")]:
    v = doc.Houder.Shape.common(doc.getObject(b).Shape).Volume
    if v > 0.001:
        print("Overlap Houder/%s: %.3f" % (b, v))
kop_einde = KOKER_L / 2 + SPELING + BOUTKOP_H
print("Rand tussen boutkop-uitsparing en kompasje: %.1f mm; rechter kompas tot put: %.1f mm; linker kompas tot wand: %.1f mm"
      % (KOMPAS_AFSTAND - KOMPAS_D / 2 - kop_einde, (PUT_X - F - PUT_WAND) - (VAK_X + KOMPAS_AFSTAND + KOMPAS_D / 2),
         (VAK_X - KOMPAS_AFSTAND - KOMPAS_D / 2) - (-HL + WAND)))
print("Klemplekken op de bouwplaat:", len(doc.Houder.Shape.common(doc.Bouwplaat_controle.Shape).Solids))
print("Bout rechtop (op zijn kop in de bodem): bovenkant %.1f mm onder de bovenkant van de koker"
      % (doc.Koker_rechtop.Shape.BoundBox.ZMax - doc.Bout_M6.Shape.BoundBox.ZMax))
print("Rechtop: koker steekt %.1f mm boven de doos uit; bout %.1f tot %.1f (noppen tot %.1f)"
      % (doc.Koker_rechtop.Shape.BoundBox.ZMax - HOOGTE, doc.Bout_M6.Shape.BoundBox.ZMin, doc.Bout_M6.Shape.BoundBox.ZMax, NOP_H))
print("Liggend: bovenkant flenzen %.1f mm boven de doos" % (doc.Koker.Shape.BoundBox.ZMax - HOOGTE))

doc.saveAs(os.path.join(MAP, "Spoelhouder_V3.FCStd"))
Part.export([doc.Houder, doc.Symbool], os.path.join(MAP, "Spoelhouder_V3-Houder.step"))
Part.export([doc.Koker], os.path.join(MAP, "Spoelhouder_V3-Koker.step"))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(MAP, "Spoelhouder_V3.png"), 1400, 1000, "White")
    doc.save()
