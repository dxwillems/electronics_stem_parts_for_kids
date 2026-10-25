# Wikkelhulp voor de koker van spoelhouder versie 2 (gat 6,4 mm).
# Een M6-bout van 70 mm gaat van boven door de koker en dit voetje en draait vast in een M6-moer
# die in de onderkant valt. De flens zakt in de uitsparing, dus de koker draait mee. Klem het
# uitstekende stuk bout in de boorkop van de schroefmachine.
# Printen: plat, uitsparing naar boven; geen support.

import os

import FreeCAD as App
import Part
from FreeCAD import Vector as V

FLENS_B = 26.5 + 0.8    # flens van spoelhouder_v2 (vierkant, 2 x (wikkeling/2 + 0,6)) + speling
FLENS_H = 26.5 + 0.8
UITSPARING = 2.0
STOMP_D = 10.0
STOMP_L = 5.0
VLOER = 3.0
RAND = 4.0
BOUT_D = 6.4
MOER_SW = 10.0 + 0.3    # M6-moer, sleutelwijdte 10 mm
MOER_H = 5.2


def maak():
    h = VLOER + STOMP_L + UITSPARING
    voet = Part.makeBox(FLENS_B + 2 * RAND, FLENS_H + 2 * RAND, h,
                        V(-(FLENS_B / 2 + RAND), -(FLENS_H / 2 + RAND), 0))
    voet = voet.cut(Part.makeBox(FLENS_B, FLENS_H, UITSPARING + 1, V(-FLENS_B / 2, -FLENS_H / 2, h - UITSPARING)))
    voet = voet.cut(Part.makeCylinder(STOMP_D / 2 + 0.3, STOMP_L + 1, V(0, 0, VLOER)))
    voet = voet.cut(Part.makeCylinder(BOUT_D / 2, h + 2, V(0, 0, -1)))
    import math
    r = MOER_SW / math.sqrt(3)
    zes = Part.Face(Part.makePolygon([V(r * math.cos(math.radians(60 * i)), r * math.sin(math.radians(60 * i)), -1)
                                      for i in range(7)])).extrude(V(0, 0, MOER_H + 1))
    return voet.cut(zes)


MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc = App.newDocument("WikkelhulpV2")
obj = doc.addObject("Part::Feature", "Wikkelhulp")
obj.Shape = maak()
print("Wikkelhulp v2 geldig:", obj.Shape.isValid())
doc.recompute()
doc.saveAs(os.path.join(MAP, "Wikkelhulp_V2.FCStd"))
Part.export([obj], os.path.join(MAP, "Wikkelhulp_V2.step"))
