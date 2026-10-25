# Wikkelhulp voor de koker van spoelhouder versie 3, zonder bout, uit een stuk:
#  - voet met een uitsparing waar de flens in valt (de koker draait mee);
#  - pen door het gat van de koker (6,4 mm), drie ribjes houden de koker vast;
#  - zeskant 1/4" (6,35 mm) aan de onderkant voor de bithouder van de accuschroefmachine.
# Printen: op zijn kant (in het 3MF-bestand al zo gelegd), met support onder pen en zeskant
# ("support alleen vanaf het printbed"). Zo lopen de lagen in de lengte van pen en zeskant en
# zijn die sterk. PETG of PLA, 100% vulling.
# Begin met de draad door het gaatje bij de kern in de BOVENSTE flens.

import math
import os

import FreeCAD as App
import Part
from FreeCAD import Vector as V

FLENS = 26.5 + 0.8      # vierkante flens van de koker (versie 3) + speling
UITSPARING = 2.5
VLOER = 8.0             # onder de uitsparing: ruimte voor het zeskantgat
RAND = 4.0
KOKER_L = 35.0
PEN_D = 6.0             # gat in de koker is 6,4 mm
PEN_RIB = 0.25          # ribjes knijpen zoveel in het gat van de koker
ZESKANT = 6.35          # 1/4" bit
SCHACHT_L = 28.0        # voor de bithouder


def zeskant(sw, lengte, plat_onder=False):
    """Zeskant met sleutelwijdte sw langs Z (of langs X met een platte kant onder)."""
    r = sw / math.sqrt(3)
    hoek0 = 30 if plat_onder else 0      # 0: platte kanten naar +X en -X (plat op het bed als hij op zijn kant ligt)
    punten = [V(r * math.cos(math.radians(hoek0 + 60 * i)), r * math.sin(math.radians(hoek0 + 60 * i)), 0)
              for i in range(7)]
    vorm = Part.Face(Part.makePolygon(punten)).extrude(V(0, 0, lengte))
    if plat_onder:
        vorm.rotate(V(0, 0, 0), V(0, 1, 0), 90)
        vorm.translate(V(0, 0, sw / 2))
    return vorm


def maak_voet():
    h = VLOER + UITSPARING
    b = FLENS / 2 + RAND
    voet = Part.makeBox(2 * b, 2 * b, h, V(-b, -b, 0))
    ribben = [e for e in voet.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1]
    voet = voet.makeFillet(3.0, ribben)
    voet = voet.cut(Part.makeBox(FLENS, FLENS, UITSPARING + 1, V(-FLENS / 2, -FLENS / 2, VLOER)))
    pen = Part.makeCylinder(PEN_D / 2, KOKER_L + 1, V(0, 0, VLOER))
    for hoek in (90, 210, 330):
        a = math.radians(hoek)
        r = PEN_D / 2 + PEN_RIB - 0.5
        pen = pen.fuse(Part.makeCylinder(0.5, KOKER_L - 6, V(r * math.cos(a), r * math.sin(a), VLOER + 4)))
    schacht = zeskant(ZESKANT, SCHACHT_L + 0.5)
    schacht.translate(V(0, 0, -SCHACHT_L))
    return voet.fuse(pen).fuse(schacht).removeSplitter()


MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc = App.newDocument("WikkelhulpV3")
kleur = (0.04, 0.16, 0.54)
for naam, vorm in (("Wikkelhulp", maak_voet()),):
    obj = doc.addObject("Part::Feature", naam)
    obj.Shape = vorm
    if App.GuiUp:
        obj.ViewObject.ShapeColor = kleur
    bb = vorm.BoundBox
    print(naam, "geldig:", vorm.isValid(), "maten %.1f x %.1f x %.1f" % (bb.XLength, bb.YLength, bb.ZLength))
doc.recompute()
doc.saveAs(os.path.join(MAP, "Wikkelhulp_V3.FCStd"))
Part.export([doc.Wikkelhulp], os.path.join(MAP, "Wikkelhulp_V3.step"))
