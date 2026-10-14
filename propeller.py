# Propeller voor de motorhouder: past op de 2 mm as van een SOL300 / RF-300 zonnemotor.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD propeller.py
# Printen: zoals getekend, naaf rechtop op het bed; de bladen liggen met hun onderrand op het
# bed en staan schuin, dat lukt zonder support. Draait de motor de verkeerde kant op, dan
# blaast hij naar achteren: draai de draden om (mooi om te laten zien).

import math
import os

import FreeCAD as App
import Part
from FreeCAD import Vector as V

DIAMETER = 70.0         # van tip tot tip
BLADEN = 3
SPOED = 28.0            # hoek van het blad t.o.v. het draaivlak, in graden
BLAD_DIKTE = 1.2
BLAD_BREEDTE = 14.0     # koorde van het blad
NAAF_D = 9.0
AS_GAT_D = 2.0          # voor een 2 mm as; geprinte gaatjes vallen iets krapper uit = klemmend
KLEUR = (0.04, 0.16, 0.54)   # Bambu PLA Basic Blue (#0A2989)


def maak_propeller():
    """Propeller met de naaf rond de Z-as, onderkant op z = 0."""
    r = DIAMETER / 2
    p = math.radians(SPOED)
    hoogte = BLAD_BREEDTE * math.sin(p) + BLAD_DIKTE * math.cos(p)
    blad = Part.makeBox(r, BLAD_BREEDTE, BLAD_DIKTE, V(0, -BLAD_BREEDTE / 2, -BLAD_DIKTE / 2))
    blad = blad.common(Part.makeCylinder(r, 20, V(0, 0, -10)))           # ronde tip
    blad = blad.cut(Part.makeCylinder(NAAF_D / 2 - 0.5, 20, V(0, 0, -10)))
    blad.rotate(V(0, 0, 0), V(1, 0, 0), SPOED)
    blad.translate(V(0, 0, hoogte / 2))
    vorm = Part.makeCylinder(NAAF_D / 2, hoogte)
    for i in range(BLADEN):
        b = blad.copy()
        b.rotate(V(0, 0, 0), V(0, 0, 1), 360.0 * i / BLADEN)
        vorm = vorm.fuse(b)
    vorm = vorm.cut(Part.makeCylinder(AS_GAT_D / 2, hoogte + 2, V(0, 0, -1)))
    return vorm.removeSplitter()


# FreeCAD geeft een script dezelfde __name__ als een import; kijk daarom wie ons aanroept.
import inspect
if not any(f.filename.endswith("motorhouder.py") for f in inspect.stack()):
    MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
    doc = App.newDocument("Propeller")
    obj = doc.addObject("Part::Feature", "Propeller")
    obj.Shape = maak_propeller()
    if App.GuiUp:
        obj.ViewObject.ShapeColor = KLEUR
    bb = obj.Shape.BoundBox
    print("Propeller geldig:", obj.Shape.isValid(), "volume: %.0f mm3" % obj.Shape.Volume,
          "maten %.1f x %.1f x %.1f" % (bb.XLength, bb.YLength, bb.ZLength))
    doc.recompute()
    doc.saveAs(os.path.join(MAP, "Propeller.FCStd"))
    Part.export([obj], os.path.join(MAP, "Propeller.step"))
    if App.GuiUp:
        import FreeCADGui as Gui
        view = Gui.ActiveDocument.ActiveView
        view.setAnimationEnabled(False)
        view.viewIsometric()
        view.fitAll()
        Gui.updateGui()
        view.saveImage(os.path.join(MAP, "Propeller.png"), 1000, 800, "White")
        doc.save()
