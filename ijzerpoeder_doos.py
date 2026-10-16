# Gesloten doosje voor ijzerpoeder (magnetische veldlijnen zichtbaar maken).
# Twee plaatjes van 2 mm (OFFCUP, 10,2 x 15,2 cm, PET) schuiven van de korte kant in groeven;
# daartussen zit een kamer van 4 mm met een paar gram ijzerpoeder. Een eindkap sluit de
# open kant af. Magneet eronder of erop leggen en zachtjes tikken.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD ijzerpoeder_doos.py
# Printen: frame plat (zoals getekend), eindkap plat met de plug omhoog; geen support.
# Afdichten: fijn poeder kruipt door kieren. Zet een dun randje lijm (secondelijm of
# transparante siliconenkit, geschikt voor PET) in de groeven of plak de randen af met tape,
# en lijm de eindkap vast nadat het poeder erin zit.

import os

import FreeCAD as App
import Part
from FreeCAD import Vector as V

KLEUR = (0.04, 0.16, 0.54)  # Bambu PLA Basic Blue (#0A2989)

PLAAT_L = 152.4         # productpagina: 10,2 x 15,2 cm, 2 mm dik
PLAAT_B = 102.4
PLAAT_D = 2.0
SPELING_B = 0.2         # per kant in de breedte
GROEF_H = PLAAT_D + 0.4 # ruim: het plafond van de groef zakt bij het printen iets door
GROEF_DIEPTE = 4.0      # zoveel valt de plaat in het frame (ook de rand van het venster)
KAMER = 4.0             # ruimte tussen de plaatjes voor het poeder
RAND = 1.2              # rand boven en onder over de plaatjes
WAND = 3.0              # zijwanden en gesloten kopse kant
R_HOEK = 3.0
KAP_D = WAND + GROEF_DIEPTE   # eindkap: even breed als de rand rondom het venster
PLUG_DIEPTE = 4.0
PLUG_SPELING = 0.2

HOOG = 2 * RAND + 2 * GROEF_H + KAMER
HB = PLAAT_B / 2 + WAND
L = WAND + PLAAT_L
VENSTER_HB = PLAAT_B / 2 - GROEF_DIEPTE
Z_G1 = RAND
Z_KAMER = RAND + GROEF_H
Z_G2 = Z_KAMER + KAMER


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def afgerond(vorm, radius, x):
    """Rond de verticale ribben op hoogte-lijn x af (de buitenhoeken aan die kant)."""
    ribben = [e for e in vorm.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1
              and abs(e.Vertexes[0].Point.x - x) < 1e-6]
    return vorm.makeFillet(radius, ribben)


def maak_frame():
    frame = afgerond(doos(0, -HB, L, HB, 0, HOOG), R_HOEK, 0)   # de open kant krijgt de kap
    # venster aan boven- en onderkant (en de kamer ertussen), open aan de rechterkant
    frame = frame.cut(doos(WAND + GROEF_DIEPTE, -VENSTER_HB, L + 1, VENSTER_HB, -1, HOOG + 1))
    # twee groeven, van rechts tot tegen de gesloten kopse kant
    gb = PLAAT_B / 2 + SPELING_B
    for z in (Z_G1, Z_G2):
        frame = frame.cut(doos(WAND, -gb, L + 1, gb, z, z + GROEF_H))
    return frame.removeSplitter()


def maak_eindkap():
    kap = afgerond(doos(L, -HB, L + KAP_D, HB, 0, HOOG), R_HOEK, L + KAP_D)
    plug = doos(L - PLUG_DIEPTE, -VENSTER_HB + PLUG_SPELING, L + 0.1, VENSTER_HB - PLUG_SPELING,
                Z_KAMER + 0.15, Z_G2 - 0.15)
    return kap.fuse(plug).removeSplitter()


def maak_plaatjes():
    delen = []
    for z in (Z_G1 + 0.2, Z_G2 + 0.2):
        delen.append(doos(WAND + 0.1, -PLAAT_B / 2, L, PLAAT_B / 2, z, z + PLAAT_D))
    return delen[0].fuse(delen[1])


MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc = App.newDocument("IJzerpoederDoos")
onderdelen = [("Frame", maak_frame(), KLEUR), ("Eindkap", maak_eindkap(), KLEUR),
              ("Plaatjes", maak_plaatjes(), (0.85, 0.92, 1.0))]
for naam, vorm, kleur in onderdelen:
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
        if naam == "Plaatjes":
            obj.ViewObject.Transparency = 60
    print(naam, "geldig:", vorm.isValid(), "volume: %.0f mm3" % vorm.Volume)
doc.recompute()
bb = doc.Frame.Shape.BoundBox
print("Frame: %.1f x %.1f x %.1f mm; venster %.1f x %.1f mm; kamer %.1f mm"
      % (bb.XLength, bb.YLength, bb.ZLength, L - WAND - GROEF_DIEPTE, 2 * VENSTER_HB, KAMER))
for a, b in (("Frame", "Plaatjes"), ("Eindkap", "Plaatjes"), ("Frame", "Eindkap")):
    print("Overlap %s/%s: %.3f mm3" % (a, b, doc.getObject(a).Shape.common(doc.getObject(b).Shape).Volume))

doc.saveAs(os.path.join(MAP, "IJzerpoeder_Doos.FCStd"))
Part.export([doc.Frame], os.path.join(MAP, "IJzerpoeder_Doos-Frame.step"))
Part.export([doc.Eindkap], os.path.join(MAP, "IJzerpoeder_Doos-Eindkap.step"))

if App.GuiUp:
    import FreeCADGui as Gui
    view = Gui.ActiveDocument.ActiveView
    view.setAnimationEnabled(False)
    doc.Eindkap.ViewObject.Visibility = False
    doc.Eindkap.Placement.Base = V(25, 0, 0)        # alleen voor het plaatje: kap los ernaast
    doc.Eindkap.ViewObject.Visibility = True
    view.viewIsometric()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(MAP, "IJzerpoeder_Doos.png"), 1400, 1000, "White")
    doc.Eindkap.Placement.Base = V(0, 0, 0)
    doc.save()
