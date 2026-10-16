# Houder voor een 5 mm LED met serieweerstand en twee 4 mm paneelbussen (12 mm montagegat);
# onderkant klemt op een LEGO-bouwplaat (12 x 6 noppen). Direct aan te sluiten op 5 V.
# Bovenop staat het schema: rood (+) - weerstand - LED - zwart (-), met de waarde erbij.
# De LED gaat van onderaf door het gat; de kraag van de LED valt in een verzonken rand.
# De weerstand ligt bovenop, met zijn pootjes door twee kleine gaatjes; binnenin solderen.
#
# Weerstand voor een rode 5 mm LED op 5 V:  R = (5 V - 2,0 V) / I
#   150 ohm geeft 20 mA, het maximum van de LED; 220 ohm geeft ca. 14 mA en houdt marge
#   voor een voeding die iets boven 5 V zit of een LED met lagere doorlaatspanning.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD ledhouder.py
# Alle maten in mm. Montagegat 12 komt van de productpagina van de bussen; de overige
# busmaten en de LED-maten (standaard 5 mm LED) zijn niet nagemeten: meet ze na.
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
NOPPEN_L = 12           # 96 mm
NOPPEN_B = 6            # 48 mm
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
R_HOEK = 3.0

LED_D = 5.0             # standaard 5 mm LED
LED_GAT_D = 5.2         # gat in de plaat, iets ruimer omdat geprinte gaten krap uitvallen
LED_KRAAG_D = 6.4       # verzonken rand aan de onderkant voor de kraag van de LED (ca. 5,8)
LED_KRAAG_H = 1.2
LED_Y = 14.0            # LED achter zijn symbool

WEERSTAND_TEKST = "220 \u03a9"   # waarde op de doos; leeg = geen tekst
WEERSTAND_STEEK = 10.16 # afstand tussen de twee gaatjes (0,4 inch, voor een 1/4 W weerstand)
WEERSTAND_GAT_D = 1.2   # gaatje voor een pootje van 0,6 mm
WEERSTAND_Y = 13.0      # weerstand achter zijn symbool
TEKST_HOOGTE = 5.0
TEKST_Y = -13.5         # waarde onder het weerstandssymbool

BUS_AFSTAND = 58.0      # hart-op-hart van de twee bussen
BUS_Y = -3.0
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0
SYMBOOL_HOOGTE = 9.0    # hoogte van de diode-driehoek

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
# rood (plus) links = anode, zwart (min) rechts = kathode
DEEL = (BUS_AFSTAND - BUS_KRAAG_D + 1.0) / 2            # lengte van elk half schema
WEERSTAND_X = -DEEL / 2                                 # weerstand links, LED rechts
LED_X = DEEL / 2
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

    # LED-gat met verzonken rand voor de kraag aan de onderkant
    houder = houder.cut(Part.makeCylinder(LED_GAT_D / 2, PLAAT + 2, V(LED_X, LED_Y, HOOGTE - PLAAT - 1)))
    houder = houder.cut(Part.makeCylinder(LED_KRAAG_D / 2, LED_KRAAG_H + 1,
                                          V(LED_X, LED_Y, HOOGTE - PLAAT - 1)))
    # twee gaatjes voor de pootjes van de weerstand
    for sx in (-1, 1):
        houder = houder.cut(Part.makeCylinder(
            WEERSTAND_GAT_D / 2, PLAAT + 2,
            V(WEERSTAND_X + sx * WEERSTAND_STEEK / 2, WEERSTAND_Y, HOOGTE - PLAAT - 1)))
    for _, x, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(x, BUS_Y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_symbool():
    """Schema tussen de twee bussen, verzonken in het bovenvlak:
    rood - weerstand - LED (anode links) - zwart, met de weerstandswaarde eronder."""
    z = HOOGTE - SYMBOOL_DIEPTE
    vorm = symbolen.plaats(symbolen.weerstand(DEEL, SYMBOOL_DIEPTE, SYMBOOL_LIJN), WEERSTAND_X, BUS_Y, z)
    vorm = vorm.fuse(symbolen.plaats(
        symbolen.led(DEEL, SYMBOOL_DIEPTE, SYMBOOL_LIJN, SYMBOOL_HOOGTE), LED_X, BUS_Y, z))
    if WEERSTAND_TEKST:
        vorm = vorm.fuse(symbolen.plaats(
            symbolen.tekst(WEERSTAND_TEKST, TEKST_HOOGTE, SYMBOOL_DIEPTE), WEERSTAND_X, TEKST_Y, z))
    return vorm


def maak_weerstand():
    """1/4 W weerstand die bovenop ligt, alleen ter controle van de passing."""
    x0, x1 = WEERSTAND_X - WEERSTAND_STEEK / 2, WEERSTAND_X + WEERSTAND_STEEK / 2
    z = HOOGTE + 1.3
    lijf = Part.makeCylinder(1.2, 6.3, V(WEERSTAND_X - 3.15, WEERSTAND_Y, z), V(1, 0, 0))
    draad = Part.makeCylinder(0.3, x1 - x0, V(x0, WEERSTAND_Y, z), V(1, 0, 0))
    delen = [draad]
    for x in (x0, x1):
        delen.append(Part.makeCylinder(0.3, PLAAT + 4 + 1.3, V(x, WEERSTAND_Y, HOOGTE - PLAAT - 4)))
    return lijf.fuse(delen)


def maak_led():
    """Standaard 5 mm LED, alleen ter controle van de passing."""
    z_kraag = HOOGTE - PLAAT + LED_KRAAG_H - 1.0
    kraag = Part.makeCylinder(2.9, 1.0, V(LED_X, LED_Y, z_kraag))
    lijf = Part.makeCylinder(LED_D / 2, 5.1, V(LED_X, LED_Y, z_kraag + 1.0))
    bol = Part.makeSphere(LED_D / 2, V(LED_X, LED_Y, z_kraag + 6.1))
    return kraag.fuse(lijf).fuse(bol)


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


doc = App.newDocument("Ledhouder")
houder = maak_houder()
houder, plek = symbolen.handtekening(houder, HOOGTE - PLAAT, [
    (0, HB - WAND - 6, 0), (0, -(HB - WAND - 6), 0), (0, 0, 0),
    (-(HL - WAND - 6), 0, 90), (HL - WAND - 6, 0, 90)])
print("Handtekening op", plek)
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, (0.04, 0.16, 0.54)),
              ("LED", maak_led(), (0.90, 0.15, 0.10)),
              ("Weerstand", maak_weerstand(), (0.80, 0.68, 0.45)),
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
print("Moeren: x %.1f tot %.1f, y %.1f tot %.1f"
      % (BUS_AFSTAND / 2 - BUS_MOER_D / 2, BUS_AFSTAND / 2 + BUS_MOER_D / 2,
         BUS_Y - BUS_MOER_D / 2, BUS_Y + BUS_MOER_D / 2))
if symbool:
    sb = symbool.BoundBox
    print("Symbool: x %.1f tot %.1f, y %.1f tot %.1f; LED-gat vanaf y %.1f; wand binnen y +/- %.1f"
          % (sb.XMin, sb.XMax, sb.YMin, sb.YMax, LED_Y - LED_GAT_D / 2, HB - WAND))

map_ = MAP
doc.saveAs(os.path.join(map_, "Ledhouder_5mm.FCStd"))
# een bestand met twee delen: houder en symbool
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []),
            os.path.join(map_, "Ledhouder_5mm-Houder.step"))
# alleen de onderste 6 mm: snelle proefprint om de klemming op een bouwplaat te testen
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(map_, "Ledhouder_5mm-Pastest.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Ledhouder_5mm.png"), 1400, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Ledhouder_5mm_bovenaanzicht.png"), 1400, 900, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name == "Houder"
    view.viewBottom()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Ledhouder_5mm_onderaanzicht.png"), 1400, 900, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
