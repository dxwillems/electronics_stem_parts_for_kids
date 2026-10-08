# Houder voor zonnepaneel 110 x 60 x 3 mm met twee 4 mm paneelbussen (12 mm montagegat),
# onderkant klemt met ribben op een LEGO-bouwplaat (19 x 9 noppen).
# Langwerpige rechthoek: paneel links, de twee bussen rechts ernaast, zodat je er van
# onderaf recht bij kunt zonder dat de LEGO-klemrand in de weg zit.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD zonnepaneel_houder_lego.py
# Alle maten in mm. Paneel en montagegat komen van de productfoto's en eigen meting,
# de overige busmaten zijn geschat: meet ze na voor je print.
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
KLEMRIB_OM_DE = 2       # een rib bij elke zoveelste nop langs de rand (1 = bij elke nop)
KLEMRIB_R = 0.6         # straal van de klemribben (verticale halve cilinders in de sleuf)
KLEMRIB_INLOOP = 0.5    # schuine aanloop onderaan, zodat de noppen erin glijden
BUITEN_SPELING = 0.1    # buitenwand ligt zoveel binnen het raster
SLEUF_DIEPTE = NOP_H + 0.3
BAND_H = 4.0            # hoogte van de klemrand onderin

# ---------------------------------------------------------------- maten
NOPPEN_L = 19           # 152 mm
NOPPEN_B = 9            # 72 mm
HOOGTE = 35.2           # 11 LEGO-platen; ruimte voor de achterkant van de bussen
WAND = 2.4              # wanddikte boven de klemrand
R_HOEK = 3.0            # afronding buitenhoeken (groter botst met de hoeknoppen)

PANEEL_L = 110.0
PANEEL_B = 60.0
PANEEL_D = 3.0          # gemeten
PANEEL_RADIUS = 4.0     # afgeronde hoeken van het paneel: geschat, meet na
SPONNING_RADIUS = 2.0   # hoekronding van de uitsparing; moet kleiner blijven dan PANEEL_RADIUS
VENSTER_RADIUS = 3.0    # hoekronding van het zichtvenster
SPELING = 0.25          # rondom het paneel
RAND_LINKS = 8.0        # frame links van het paneel
RAND_OVERLAP = 2.5      # zoveel dekt de bovenrand het paneel af
RAND_DIKTE = 1.5        # dikte van die bovenrand
KLIK = 0.7              # zoveel steken de kliknokjes onder het paneel uit; 0 = geen nokjes (lijmen)
KLIK_ZONE = 1.0         # hoogte van de schuine aanloop van de nokjes, onder het paneel
KLIK_B = 6.0            # breedte van een nokje
KLIK_X = (-36.0, 0.0, 36.0)   # plekken langs beide lange zijden, vanaf het midden van het paneel

BUS_AFSTAND = 34.0      # hart-op-hart van de twee bussen (dwars op de lengte)
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm, plaatdikte max 6 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0

# ---------------------------------------------------------------- afgeleid
PLAAT = RAND_DIKTE + PANEEL_D + KLIK_ZONE               # 5,5: dikte bovenplaat
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM           # binnenkant buitenwand
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM           # buitenkant klemrib
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1  # 9,5: vrij van de tweede rij noppen
SL = PANEEL_L / 2 + SPELING                             # halve sponning
SB = PANEEL_B / 2 + SPELING
PANEEL_X = -HL + RAND_LINKS + SL                        # midden van het paneel
# bus: moer vrij van de sponning en recht boven de vrije opening in de klemrand
BUS_X_MIN = PANEEL_X + SL + BUS_MOER_D / 2 + 2
BUS_X_MAX = HL - RIB_BINNEN - BUS_MOER_D / 2 - 1
BUS_X = (BUS_X_MIN + BUS_X_MAX) / 2
BUSSEN = [("rood", BUS_AFSTAND / 2, (0.85, 0.10, 0.10)),
          ("zwart", -BUS_AFSTAND / 2, (0.08, 0.08, 0.08))]

HOEKEN = [V(*p) for p in ((-HL, -HB), (HL, -HB), (HL, HB), (-HL, HB))]   # tegen de klok in
RASTER = Part.Face(Part.makePolygon(HOEKEN + [HOEKEN[0]]))


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def ronde_doos(hl, hb, radius, z0, z1):
    """Doos van 2*hl x 2*hb rond het midden van het paneel, verticale ribben afgerond."""
    vorm = doos(PANEEL_X - hl, -hb, PANEEL_X + hl, hb, z0, z1)
    ribben = [e for e in vorm.Edges
              if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1e-6]
    return vorm.makeFillet(radius, ribben)


def binnen(d, z0, z1):
    """Rasteromtrek, d naar binnen verschoven (scherpe hoeken), van z0 tot z1."""
    vlak = RASTER.makeOffset2D(-d, 2)
    vlak.translate(V(0, 0, z0))
    return vlak.extrude(V(0, 0, z1 - z0))


def maak_klemribben():
    """Smalle ribben op de binnenwand van de sleuf; ze vervormen en klemmen de nop vast.
    Alleen waar de binnenwand langs de nop loopt, dus niet bij de buitenhoeken."""
    r, uitsteek = KLEMRIB_R, KLEM + KLEMRIB_OVERMAAT
    binnenwand = RASTER.makeOffset2D(-SLEUF_BINNEN, 2)
    ribben = []
    for a, b in zip(HOEKEN, HOEKEN[1:] + HOEKEN[:1]):
        langs = (b - a).normalize()
        naar_binnen = V(-langs.y, langs.x, 0)
        for k in range(int(round((b - a).Length / NOP_STEEK))):
            if k % KLEMRIB_OM_DE != KLEMRIB_OM_DE - 1 and KLEMRIB_OM_DE > 1:
                continue
            as_ = a + langs * (k + 0.5) * NOP_STEEK + naar_binnen * (SLEUF_BINNEN + r - uitsteek)
            if not binnenwand.isInside(as_, 1e-3, True):
                continue
            ribben.append(Part.makeCone(r - uitsteek, r, KLEMRIB_INLOOP, as_))
            ribben.append(Part.makeCylinder(r, SLEUF_DIEPTE - KLEMRIB_INLOOP + 0.2,
                                            as_ + V(0, 0, KLEMRIB_INLOOP)))
    return ribben


def maak_kliknokjes():
    """Wigjes op de lange wanden van de sponning: het paneel klikt er van onderaf langs
    en rust er daarna op. Schuin aan de inschuifkant, vlak aan de paneelkant."""
    z_paneel = HOOGTE - RAND_DIKTE - PANEEL_D - 0.1
    z_onder = HOOGTE - PLAAT
    nokjes = []
    for sy in (-1, 1):
        y = sy * SB
        driehoek = Part.Face(Part.makePolygon([
            V(0, y, z_paneel), V(0, y - sy * KLIK, z_paneel), V(0, y, z_onder), V(0, y, z_paneel)]))
        for x in KLIK_X:
            nok = driehoek.extrude(V(KLIK_B, 0, 0))
            nok.translate(V(PANEEL_X + x - KLIK_B / 2, 0, 0))
            nokjes.append(nok)
    return nokjes


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
    if KLEMRIB_OVERMAAT > 0:
        houder = houder.fuse(maak_klemribben())

    # venster en sponning: het paneel klikt er van onderaf in, tegen de bovenrand
    houder = houder.cut(ronde_doos(PANEEL_L / 2 - RAND_OVERLAP, PANEEL_B / 2 - RAND_OVERLAP,
                                   VENSTER_RADIUS, HOOGTE - PLAAT - 1, HOOGTE + 1))
    houder = houder.cut(ronde_doos(SL, SB, SPONNING_RADIUS, HOOGTE - PLAAT - 1, HOOGTE - RAND_DIKTE))
    if KLIK > 0:
        houder = houder.fuse(maak_kliknokjes())
    for _, y, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(BUS_X, y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_symbool():
    """Zonnecelsymbool tussen de twee bussen, verzonken in het bovenvlak; plus naar rood."""
    ruimte = BUS_AFSTAND - BUS_KRAAG_D
    # 90 graden gedraaid: de draden lopen van bus naar bus, de pijlen komen van de paneelkant
    vorm = symbolen.zonnecel(ruimte + 1.0, SYMBOOL_DIEPTE, SYMBOOL_LIJN, ruimte - 4.0, pijlkant=1)
    return symbolen.plaats(vorm, BUS_X, 0, HOOGTE - SYMBOOL_DIEPTE, 90)


def maak_bouwplaat():
    """Stuk LEGO-bouwplaat met noppen, alleen ter controle van de passing."""
    nx, ny = NOPPEN_L + 2, NOPPEN_B + 2
    x0, y0 = -nx * NOP_STEEK / 2, -ny * NOP_STEEK / 2
    noppen = [Part.makeCylinder(NOP_D / 2, NOP_H,
                                V(x0 + (i + 0.5) * NOP_STEEK, y0 + (j + 0.5) * NOP_STEEK, 0))
              for i in range(nx) for j in range(ny)]
    return doos(x0, y0, -x0, -y0, -1.5, 0).fuse(noppen)


def maak_paneel():
    return ronde_doos(PANEEL_L / 2, PANEEL_B / 2, PANEEL_RADIUS,
                      HOOGTE - RAND_DIKTE - PANEEL_D, HOOGTE - RAND_DIKTE)


def maak_bus(y):
    kraag = Part.makeCylinder(BUS_KRAAG_D / 2, BUS_KRAAG_H, V(BUS_X, y, HOOGTE))
    schacht = Part.makeCylinder(BUS_GAT_D / 2 - 0.1, PLAAT + 16, V(BUS_X, y, HOOGTE - PLAAT - 16))
    lip = doos(BUS_X - 3, y - 0.4, BUS_X + 3, y + 0.4, HOOGTE - BUS_ACHTER, HOOGTE - PLAAT - 16)
    gat = Part.makeCylinder(2.0, 20, V(BUS_X, y, HOOGTE + BUS_KRAAG_H - 20))
    return kraag.fuse(schacht).fuse(lip).cut(gat)


def maak_moer(y):
    moer = Part.makeCylinder(BUS_MOER_D / 2, 5, V(BUS_X, y, HOOGTE - PLAAT - 5))
    return moer.cut(Part.makeCylinder(BUS_GAT_D / 2 - 0.1, 7, V(BUS_X, y, HOOGTE - PLAAT - 6)))


doc = App.newDocument("ZonnepaneelHouderLego")
houder = maak_houder()
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, (0.04, 0.16, 0.54)),
              ("Zonnepaneel", maak_paneel(), (0.02, 0.02, 0.05)),
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
botsing = doc.Houder.Shape.common(doc.Bouwplaat_controle.Shape)
# hier hoort alleen de klemoverlap van de ribben te zitten
print("Overlap houder/bouwplaat: %.3f mm3, klemplekken: %d, grootste per plek: %.4f mm3"
      % (botsing.Volume, len(botsing.Solids), max([v.Volume for v in botsing.Solids] or [0])))
for naam in ("Bus_rood", "Bus_zwart", "Moer_rood", "Moer_zwart", "Zonnepaneel"):
    print("Overlap houder/%s: %.3f mm3" % (naam, doc.Houder.Shape.common(doc.getObject(naam).Shape).Volume))
print("Vrije opening onderkant: x %.1f tot %.1f, y +/- %.1f" % (-HL + RIB_BINNEN, HL - RIB_BINNEN, HB - RIB_BINNEN))
print("Moeren: x %.1f tot %.1f, y +/- %.1f  (bus op x = %.1f, toegestaan %.1f tot %.1f)"
      % (BUS_X - BUS_MOER_D / 2, BUS_X + BUS_MOER_D / 2, BUS_AFSTAND / 2 + BUS_MOER_D / 2,
         BUS_X, BUS_X_MIN, BUS_X_MAX))
print("Bovenplaat %.1f mm (bus max 6), ruimte eronder %.1f mm (bus %.1f)" % (PLAAT, HOOGTE - PLAAT, BUS_ACHTER))

map_ = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc.saveAs(os.path.join(map_, "Zonnepaneel_Houder_Lego.FCStd"))
# een bestand met twee delen: in de slicer het symbool een andere kleur geven
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []),
            os.path.join(map_, "Zonnepaneel_Houder_Lego-Houder.step"))
# alleen de onderste 6 mm: snelle proefprint om de klemming op een bouwplaat te testen
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(map_, "Zonnepaneel_Houder_Lego-Pastest.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder_Lego.png"), 1400, 1000, "White")
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder_Lego_bovenaanzicht.png"), 1800, 900, "White")
    for naam in ("Zonnepaneel", "Bus_rood", "Bus_zwart", "Moer_rood", "Moer_zwart", "Symbool"):
        if doc.getObject(naam):
            doc.getObject(naam).ViewObject.Visibility = False
    view.viewBottom()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder_Lego_onderaanzicht.png"), 1800, 900, "White")
    view.setCameraOrientation(App.Rotation(V(1, 0.25, 0), 145))
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Zonnepaneel_Houder_Lego_onderkant.png"), 1400, 1000, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
