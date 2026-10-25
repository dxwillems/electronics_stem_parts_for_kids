# Wikkelhulp: opsteekas om de koker van de ronde spoel met een accuschroefmachine te wikkelen.
# De koker schuift van bovenaf over de zeskant en de as tot hij in de voetplaat valt: de vierkante
# flens zakt in een uitsparing, dus de koker draait mee zonder te slippen. Klem de zeskant van
# 1/4" in de bithouder of boorkop. Begindraad door het gaatje in de BOVENSTE flens.
# Printen: rechtop zoals getekend (voetplaat op het bed), 100% vulling voor een sterke zeskant.
# Uitvoeren: FreeCAD > Macro > Macro's... of  FreeCAD wikkelhulp.py

import math
import os

import FreeCAD as App
import Part
from FreeCAD import Vector as V

FLENS = 40.0            # vierkante flens van de koker
FLENS_SPELING = 0.4     # per kant in de uitsparing
FLENS_R = 3.0
UITSPARING = 2.0        # zo diep zakt de flens in de voetplaat
STOMP_D = 23.6          # uiteinde van de koker onder de flens
STOMP_L = 5.0
VLOER = 1.5
VOET = FLENS + 2 * FLENS_SPELING + 2 * 4.0   # voetplaat met 4 mm rand
AS_D = 20.0             # koker heeft een gat van 20,4 mm
AS_RIB = 0.25           # drie ribjes knijpen zoveel in het gat van de koker
KOKER_L = 55.0
ZESKANT = 6.3           # 1/4" bit = 6,35 mm over de platte kanten; iets kleiner past makkelijker
ZESKANT_L = 25.0
KLEUR = (0.04, 0.16, 0.54)


def doos(x0, y0, x1, y1, z0, z1):
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def afgerond(vorm, r):
    ribben = [e for e in vorm.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1]
    return vorm.makeFillet(r, ribben)


def maak_wikkelhulp():
    hoogte_voet = VLOER + STOMP_L + UITSPARING
    v = VOET / 2
    voet = afgerond(doos(-v, -v, v, v, 0, hoogte_voet), 4.0)
    f = FLENS / 2 + FLENS_SPELING
    voet = voet.cut(afgerond(doos(-f, -f, f, f, hoogte_voet - UITSPARING, hoogte_voet + 1), FLENS_R + FLENS_SPELING))
    voet = voet.cut(Part.makeCylinder(STOMP_D / 2 + 0.3, STOMP_L + 1, V(0, 0, VLOER)))
    as_top = VLOER + KOKER_L + 1.5
    vorm = voet.fuse(Part.makeCylinder(AS_D / 2, as_top - VLOER, V(0, 0, VLOER)))
    for hoek in (90, 210, 330):          # klemribjes over de lengte van de koker
        a = math.radians(hoek)
        r = AS_D / 2 + AS_RIB - 0.6
        vorm = vorm.fuse(Part.makeCylinder(0.6, KOKER_L - 6, V(r * math.cos(a), r * math.sin(a), hoogte_voet + 3)))
    overgang = AS_D / 2 - ZESKANT / 2      # 45 graden kegel naar de zeskant
    vorm = vorm.fuse(Part.makeCone(AS_D / 2, ZESKANT / 2, overgang, V(0, 0, as_top)))
    r6 = ZESKANT / math.sqrt(3)            # hoekpunt-straal van de zeskant
    punten = [V(r6 * math.cos(math.radians(60 * i)), r6 * math.sin(math.radians(60 * i)), 0) for i in range(7)]
    zeskant = Part.Face(Part.makePolygon(punten)).extrude(V(0, 0, ZESKANT_L + overgang))
    zeskant.translate(V(0, 0, as_top))
    return vorm.fuse(zeskant).removeSplitter()


MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
doc = App.newDocument("Wikkelhulp")
obj = doc.addObject("Part::Feature", "Wikkelhulp")
obj.Shape = maak_wikkelhulp()
if App.GuiUp:
    obj.ViewObject.ShapeColor = KLEUR
bb = obj.Shape.BoundBox
print("Wikkelhulp geldig:", obj.Shape.isValid(), "maten %.1f x %.1f x %.1f mm" % (bb.XLength, bb.YLength, bb.ZLength))
doc.recompute()
doc.saveAs(os.path.join(MAP, "Wikkelhulp.FCStd"))
Part.export([obj], os.path.join(MAP, "Wikkelhulp.step"))
