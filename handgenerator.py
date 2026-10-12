# Houder voor een handslinger-generator (blauw tandwielkastje met motor, TICFOX-HG-3V6V)
# met twee 4 mm paneelbussen (12 mm montagegat) en het generatorsymbool; onderkant klemt
# op een LEGO-bouwplaat (16 x 10 noppen).
# Het kastje staat met de motor omlaag in een put in het bovenvlak: de motor steekt door de
# bodem van de put de doos in, de slinger draait bovenop. De put houdt het kastje rechtop en
# vangt het draaimoment op. Onder de putbodem zit een geslitste kraag om de motor; een
# kabelbinder daaromheen klemt de motor vast.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD handgenerator.py
#
# Gemeten (schuifmaat en foto's): kastje 50 x 25,5 mm en 17,79 mm dik; aan de motorkant een
# blauwe kraag (samen 23,28 mm) en dan de motor van 24,35 mm rond die 12,85 mm uitsteekt;
# de motor steekt ca. 3,5 mm voorbij het uiteinde van het kastje (53,2-53,75 tegen 49,9-50);
# een ribbe van 2,19 mm dik over de lengte aan
# de motorkant; slingeras 12,5 mm van het andere uiteinde, slingerarm ca. 52 mm.
# Geschat: diameter van de blauwe kraag (ca. 28 mm) en de hoogte van de ribbe.
# Printen: ondersteboven (bovenvlak op het bed), zonder support; de bodem van de put wordt
# dan als brug geprint.

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
NOPPEN_L = 16           # 128 mm
NOPPEN_B = 10           # 80 mm; breed genoeg om de bussen makkelijk te monteren
HOOGTE = 35.2           # 11 LEGO-platen
WAND = 2.4
PLAAT = 3.5             # bovenplaat (bus kan max 6 mm aan)
R_HOEK = 3.0

# generator: kastje met zijn lange kant langs X, motor aan de rechterkant (naar het midden)
KAST_L = 50.0           # gemeten
KAST_B = 25.5           # gemeten
KAST_D = 17.79          # gemeten: dikte van het blauwe blok
KAST_X0 = -50.0         # linker uiteinde van het kastje
BLAUWE_KRAAG_H = 5.49   # gemeten: 23,28 - 17,79, blauwe kraag tussen blok en motor
BLAUWE_KRAAG_D = 28.0   # geschat: diameter van die kraag
BLAUWE_KRAAG_SPELING = 0.5
MOTOR_D = 24.35         # gemeten
MOTOR_SPELING = 0.5     # rondom de motor; de kabelbinder knijpt de kraag dicht
MOTOR_UITSTEEK = 3.5    # gemeten: zoveel steekt de motor voorbij het rechter uiteinde van het kastje
MOTOR_VAN_EIND = MOTOR_D / 2 - MOTOR_UITSTEEK   # hart van de motor tot dat uiteinde
EIND_OPENING = 12.0     # de put is aan de motorkant zo ver open, voor wat daar nog uitsteekt
MOTOR_UIT_MIDDEN = 0.0  # hart van de motor naast de hartlijn van het kastje (+ = naar +Y)
MOTOR_H = 12.85         # gemeten: lengte van de motor onder de blauwe kraag
RIB_D = 2.19            # gemeten: dikte van de ribbe over de lengte aan de motorkant
RIB_SLEUF = 3.2         # sleuf in de putbodem waar die ribbe doorheen steekt
PUT_DIEPTE = 8.0        # zo diep staat het blok in het bovenvlak
PUT_SPELING = 0.4       # per kant naast het blok
PUT_WAND = 3.0
PUT_BODEM = 2.0
KRAAG_H = 6.0           # geslitste kraag om de motor, voor een kabelbinder
KRAAG_WAND = 1.6
KRAAG_SLEUF = 2.5
SLINGER_VAN_EIND = 12.5 # gemeten: as van de slinger tot het linker uiteinde van het kastje
SLINGER_L = 52.0        # van de foto: as tot knop

BUS_X = 45.0            # beide bussen rechts, buiten het bereik van de slinger
BUS_AFSTAND = 34.0      # hart-op-hart van de twee bussen (langs Y)
BUS_GAT_D = 12.2        # montagegat (opgave: 12 mm)
BUS_KRAAG_D = 16.0      # geschat
BUS_KRAAG_H = 5.5       # geschat
BUS_MOER_D = 17.0       # geschat
BUS_ACHTER = 28.0       # geschat: lengte onder de plaat incl. soldeerlip

# ---------------------------------------------------------------- symbool
# Schakelsymbool in het bovenvlak, in een tweede kleur te printen (wit).
SYMBOOL_DIEPTE = 0.4    # 2 lagen van 0,2 mm; 0 = geen symbool
SYMBOOL_LIJN = 1.0
SYMBOOL_X = 21.0        # tussen het kastje en de bussen
SYMBOOL_D = 14.0        # diameter van de cirkel

# ---------------------------------------------------------------- afgeleid
HL = NOPPEN_L * NOP_STEEK / 2
HB = NOPPEN_B * NOP_STEEK / 2
SLEUF_BUITEN = (NOP_STEEK - NOP_D) / 2 - KLEM
SLEUF_BINNEN = (NOP_STEEK + NOP_D) / 2 + KLEM
RIB_BINNEN = NOP_STEEK + (NOP_STEEK - NOP_D) / 2 - 0.1
MOTOR_X = KAST_X0 + KAST_L - MOTOR_VAN_EIND
MOTOR_Y = MOTOR_UIT_MIDDEN
MOTOR_GAT_R = MOTOR_D / 2 + MOTOR_SPELING
SLINGER_X = KAST_X0 + SLINGER_VAN_EIND
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
    """Smalle ribben op de binnenwand van de sleuf; die vervormt en klemt de nop vast.
    De hoeknoppen krijgen er geen: daar loopt de binnenwand niet langs."""
    r, uitsteek = KLEMRIB_R, KLEM + KLEMRIB_OVERMAAT
    plekken = []       # (x, y) van de ribas: uitsteek buiten de binnenwand, de rest erin
    for i in range(1, NOPPEN_L - 1, KLEMRIB_OM_DE):
        x = -HL + (i + 0.5) * NOP_STEEK
        for sy in (-1, 1):
            plekken.append((x, sy * (HB - SLEUF_BINNEN - (r - uitsteek))))
    for j in range(1, NOPPEN_B - 1, KLEMRIB_OM_DE):
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

    # put voor het blok: wanden en bodem hangen onder de bovenplaat
    sp = PUT_SPELING
    x0, x1 = KAST_X0 - sp, KAST_X0 + KAST_L + sp
    y1 = KAST_B / 2 + sp
    z_bodem = HOOGTE - PUT_DIEPTE
    z_onder = z_bodem - PUT_BODEM
    r_blauw = BLAUWE_KRAAG_D / 2 + BLAUWE_KRAAG_SPELING
    houder = houder.fuse(doos(x0 - PUT_WAND, -y1 - PUT_WAND, x1 + PUT_WAND, y1 + PUT_WAND,
                              z_onder, HOOGTE))
    # beker onder de bodem: ruimte voor de blauwe kraag, daaronder een geslitste kraag om de motor
    overgang = r_blauw - MOTOR_GAT_R                  # 45 graden, zodat het zonder support print
    z_beker = z_onder - BLAUWE_KRAAG_H - overgang + PUT_BODEM
    z_kraag = z_beker - KRAAG_H
    midden = V(MOTOR_X, MOTOR_Y, 0)
    beker = Part.makeCylinder(r_blauw + KRAAG_WAND, z_onder - z_beker + 0.5, midden + V(0, 0, z_beker))
    kraag = Part.makeCylinder(MOTOR_GAT_R + KRAAG_WAND, KRAAG_H + 0.5, midden + V(0, 0, z_kraag))
    for hoek in (0, 90):
        snede = doos(-MOTOR_GAT_R - 3, -KRAAG_SLEUF / 2, MOTOR_GAT_R + 3, KRAAG_SLEUF / 2,
                     z_kraag - 1, z_beker)
        snede.rotate(V(0, 0, 0), V(0, 0, 1), hoek + 45)
        snede.translate(midden)
        kraag = kraag.cut(snede)
    houder = houder.fuse(beker).fuse(kraag)
    # uitsparingen: blok, blauwe kraag (ook door de putwanden heen), overgang, motor, ribbe
    houder = houder.cut(doos(x0, -y1, x1, y1, z_bodem, HOOGTE + 1))
    z_kraag_blauw = z_bodem - BLAUWE_KRAAG_H - 0.3
    houder = houder.cut(Part.makeCylinder(r_blauw, HOOGTE + 1 - z_kraag_blauw, midden + V(0, 0, z_kraag_blauw)))
    houder = houder.cut(Part.makeCone(MOTOR_GAT_R, r_blauw, overgang, midden + V(0, 0, z_kraag_blauw - overgang)))
    houder = houder.cut(Part.makeCylinder(MOTOR_GAT_R, HOOGTE, midden + V(0, 0, z_kraag - 1)))
    # aan de motorkant is de put open: motor, kraag en nokjes steken daar voorbij het uiteinde
    houder = houder.cut(doos(MOTOR_X, MOTOR_Y - r_blauw, KAST_X0 + KAST_L + EIND_OPENING, MOTOR_Y + r_blauw,
                             z_kraag_blauw, HOOGTE + 1))
    # de sleuf voor de ribbe loopt ook door de wand van de beker
    houder = houder.cut(doos(x0, -RIB_SLEUF / 2, MOTOR_X, RIB_SLEUF / 2, z_beker - 1, z_bodem + 1))
    for _, y, _ in BUSSEN:
        houder = houder.cut(Part.makeCylinder(BUS_GAT_D / 2, PLAAT + 2,
                                              V(BUS_X, y, HOOGTE - PLAAT - 1)))
    return houder.removeSplitter()


def maak_symbool():
    """Generatorsymbool (cirkel met G) links van de bussen, met een draad naar elke bus."""
    z = HOOGTE - SYMBOOL_DIEPTE
    vorm = symbolen.plaats(symbolen.generator(SYMBOOL_DIEPTE, SYMBOOL_LIJN, SYMBOOL_D), SYMBOOL_X, 0, z)
    for _, y, _ in BUSSEN:
        richting = 1 if y > 0 else -1
        draad = symbolen.lijn((SYMBOOL_X, richting * SYMBOOL_D / 2), (SYMBOOL_X, y),
                              SYMBOOL_LIJN, SYMBOOL_DIEPTE)
        draad = draad.fuse(symbolen.lijn((SYMBOOL_X, y), (BUS_X - BUS_KRAAG_D / 2 + 0.5, y),
                                         SYMBOOL_LIJN, SYMBOOL_DIEPTE))
        vorm = vorm.fuse(symbolen.plaats(draad, 0, 0, z))
    return vorm


def maak_generator():
    """Tandwielkastje met motor en slinger, vereenvoudigd; alleen ter controle van de passing."""
    z = HOOGTE - PUT_DIEPTE
    kast = doos(KAST_X0, -KAST_B / 2, KAST_X0 + KAST_L, KAST_B / 2, z, z + KAST_D)
    blauw = Part.makeCylinder(BLAUWE_KRAAG_D / 2, BLAUWE_KRAAG_H, V(MOTOR_X, MOTOR_Y, z - BLAUWE_KRAAG_H))
    motor = Part.makeCylinder(MOTOR_D / 2, MOTOR_H + 0.1,
                              V(MOTOR_X, MOTOR_Y, z - BLAUWE_KRAAG_H - MOTOR_H))
    rib = doos(KAST_X0 + 2, -RIB_D / 2, MOTOR_X - BLAUWE_KRAAG_D / 2, RIB_D / 2, z - BLAUWE_KRAAG_H, z)
    naaf = Part.makeCylinder(5.0, 5.0, V(SLINGER_X, 0, z + KAST_D))
    arm = doos(SLINGER_X - 6, -6, SLINGER_X + SLINGER_L + 5, 6, z + KAST_D + 5, z + KAST_D + 10)
    knop = Part.makeCylinder(5.0, 20.0, V(SLINGER_X + SLINGER_L, 0, z + KAST_D + 10))
    return kast.fuse(blauw).fuse(motor).fuse(rib).fuse(naaf).fuse(arm).fuse(knop)


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


doc = App.newDocument("Handgenerator")
houder = maak_houder()
symbool = maak_symbool() if SYMBOOL_DIEPTE > 0 else None
onderdelen = [("Houder", houder.cut(symbool) if symbool else houder, (0.04, 0.16, 0.54)),
              ("Generator", maak_generator(), (0.45, 0.65, 0.95)),
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
        if naam == "Generator":
            obj.ViewObject.Transparency = 50
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
print("Ruimte tussen put/beker en busmoeren: %.1f mm" % (BUS_X - BUS_MOER_D / 2 - (MOTOR_X + BLAUWE_KRAAG_D / 2 + BLAUWE_KRAAG_SPELING + KRAAG_WAND)))
print("Moeren: x %.1f tot %.1f, y tot +/- %.1f" % (BUS_X - BUS_MOER_D / 2, BUS_X + BUS_MOER_D / 2,
                                                 BUS_AFSTAND / 2 + BUS_MOER_D / 2))
print("Onderkant motor op z = %.1f (noppen tot %.1f); kastje steekt %.1f boven de doos uit"
      % (HOOGTE - PUT_DIEPTE - BLAUWE_KRAAG_H - MOTOR_H, NOP_H, KAST_D - PUT_DIEPTE))
print("Put: x %.1f tot %.1f, y +/- %.1f (buitenkant wand); binnenwand doos x +/- %.1f, y +/- %.1f"
      % (KAST_X0 - PUT_SPELING - PUT_WAND, KAST_X0 + KAST_L + PUT_SPELING + PUT_WAND,
         KAST_B / 2 + PUT_SPELING + PUT_WAND, HL - WAND, HB - WAND))
print("Slinger: as op x %.1f, bereik (incl. knop) tot x %.1f; buskraag begint op x %.1f; kastje tot x %.1f; symbool vanaf x %.1f"
      % (SLINGER_X, SLINGER_X + SLINGER_L + 5, BUS_X - BUS_KRAAG_D / 2, KAST_X0 + KAST_L,
         SYMBOOL_X - SYMBOOL_D / 2))

map_ = MAP
doc.saveAs(os.path.join(map_, "Handgenerator.FCStd"))
# een bestand met twee delen: houder en symbool
Part.export([doc.Houder] + ([doc.Symbool] if symbool else []),
            os.path.join(map_, "Handgenerator-Houder.step"))
# alleen de onderste 6 mm: snelle proefprint om de klemming op een bouwplaat te testen
proef = doc.Houder.Shape.common(doos(-HL, -HB, HL, HB, 0, 6.0))
Part.export([Part.show(proef, "Pastest")], os.path.join(map_, "Handgenerator-Pastest.step"))
doc.removeObject("Pastest")

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Bouwplaat_controle.ViewObject.Visibility = False
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Handgenerator.png"), 1400, 1000, "White")
    doc.Generator.ViewObject.Visibility = False
    view.viewTop()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Handgenerator_bovenaanzicht.png"), 1400, 900, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name == "Houder"
    view.viewBottom()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(map_, "Handgenerator_onderaanzicht.png"), 1400, 900, "White")
    for obj in doc.Objects:
        obj.ViewObject.Visibility = obj.Name != "Bouwplaat_controle"
    view.viewIsometric()
    view.fitAll()
    doc.save()
