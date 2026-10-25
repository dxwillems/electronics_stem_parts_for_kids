# Maakt drie labels (SVG) voor de rol van een module: BRON, REGELAAR, VERBRUIKER.
# Voor Cricut Design Space: "Print then Cut" (gekleurd) of per kleur uitsnijden uit vinyl.
# Alle letters zijn omgezet naar vormen, dus Cricut hoeft geen lettertype te hebben.
# Uitvoeren: /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd maak_labels.py

import math
import os

import Part
from FreeCAD import Vector as V

MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd(), "labels")
B, H, R = 44.0, 16.0, 3.0           # label in mm
LETTERTYPE = ("/System/Library/Fonts/Supplemental/", "Arial Bold.ttf")
LABELS = [            # woord, kleur, icoon, extra regel (leeg = geen)
    ("BRON", "#F5C400", "bliksem", "max. 1 bron aansluiten"),
    ("REGELAAR", "#FFFFFF", "knop", "nooit zonder verbruiker"),
    ("VERBRUIKER", "#3DAE4E", "lamp", "min. 1 verbruiker aansluiten"),
]
EXTRA_H = 5.0           # zoveel wordt een label hoger met een extra regel


def vlak_rechthoek(x0, y0, x1, y1, r):
    doos = Part.makeBox(x1 - x0, y1 - y0, 1, V(x0, y0, 0))
    ribben = [e for e in doos.Edges if abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 0.5]
    doos = doos.makeFillet(r, ribben)
    return [f for f in doos.Faces if abs(f.CenterOfMass.z) < 1e-6][0]


def tekst(inhoud, hoogte, x_links, y_midden, max_breedte):
    vlakken = []
    for teken in Part.makeWireString(inhoud, LETTERTYPE[0], LETTERTYPE[1], 10.0, 0):
        delen = sorted((Part.Face(w) for w in teken), key=lambda f: -f.Area)
        if not delen:
            continue
        letter = delen[0]
        for deel in delen[1:]:
            letter = letter.cut(deel) if letter.common(deel).Area > 1e-6 else letter.fuse(deel)
        vlakken.append(letter)
    vorm = vlakken[0].fuse(vlakken[1:]) if len(vlakken) > 1 else vlakken[0]
    bb = vorm.BoundBox
    schaal = min(hoogte / bb.YLength, max_breedte / bb.XLength)
    vorm.translate(V(-bb.XMin, -(bb.YMin + bb.YMax) / 2, 0))
    vorm.scale(schaal)
    vorm.translate(V(x_links, y_midden, 0))
    return vorm


def icoon(soort, cx, cy):
    if soort == "bliksem":
        p = [(1.5, 6), (-3.5, -0.5), (-0.3, -0.5), (-1.5, -6), (3.5, 1.0), (0.3, 1.0), (1.5, 6)]
        return Part.Face(Part.makePolygon([V(cx + x, cy + y, 0) for x, y in p]))
    if soort == "knop":                      # draaiknop met wijzer en streepjes
        r = 4.2
        knop = Part.Face(Part.Wire(Part.makeCircle(r, V(cx, cy, 0))))
        wijzer = Part.Face(Part.makePolygon([V(cx - 0.6, cy, 0), V(cx + 0.6, cy, 0), V(cx + 0.6, cy + r - 0.8, 0),
                                             V(cx - 0.6, cy + r - 0.8, 0), V(cx - 0.6, cy, 0)]))
        vorm = knop.cut(wijzer)
        for hoek in (-60, -30, 0, 30, 60):
            a = math.radians(90 + hoek)
            x0, y0 = cx + (r + 1.0) * math.cos(a), cy + (r + 1.0) * math.sin(a)
            x1, y1 = cx + (r + 2.4) * math.cos(a), cy + (r + 2.4) * math.sin(a)
            nx, ny = -math.sin(a) * 0.35, math.cos(a) * 0.35
            vorm = vorm.fuse(Part.Face(Part.makePolygon([V(x0 + nx, y0 + ny, 0), V(x1 + nx, y1 + ny, 0),
                                                         V(x1 - nx, y1 - ny, 0), V(x0 - nx, y0 - ny, 0),
                                                         V(x0 + nx, y0 + ny, 0)])))
        return vorm
    # lampje: bol met voetje en straaltjes
    bol = Part.Face(Part.Wire(Part.makeCircle(3.3, V(cx, cy + 1.2, 0))))
    voet = Part.Face(Part.makePolygon([V(cx - 1.6, cy - 4.8, 0), V(cx + 1.6, cy - 4.8, 0), V(cx + 1.6, cy - 1.5, 0),
                                       V(cx - 1.6, cy - 1.5, 0), V(cx - 1.6, cy - 4.8, 0)]))
    vorm = bol.fuse(voet)
    for hoek in (0, 45, 90, 135, 180):
        a = math.radians(hoek)
        x0, y0 = cx + 4.2 * math.cos(a), cy + 1.2 + 4.2 * math.sin(a)
        x1, y1 = cx + 5.6 * math.cos(a), cy + 1.2 + 5.6 * math.sin(a)
        nx, ny = -math.sin(a) * 0.35, math.cos(a) * 0.35
        vorm = vorm.fuse(Part.Face(Part.makePolygon([V(x0 + nx, y0 + ny, 0), V(x1 + nx, y1 + ny, 0),
                                                     V(x1 - nx, y1 - ny, 0), V(x0 - nx, y0 - ny, 0),
                                                     V(x0 + nx, y0 + ny, 0)])))
    return vorm


def pad(vorm):
    """SVG-pad van alle vlakken (buiten- en binnenranden), y omgedraaid voor SVG."""
    delen = []
    for f in vorm.Faces:
        for w in f.Wires:
            punten = w.discretize(Deflection=0.01)
            delen.append("M " + " L ".join("%.3f %.3f" % (p.x, H - p.y) for p in punten) + " Z")
    return " ".join(delen)


for nummer, (woord, kleur, soort, extra) in enumerate(LABELS, start=1):
    H = 16.0 + (EXTRA_H if extra else 0.0)
    boven = EXTRA_H if extra else 0.0          # hoofdregel schuift omhoog
    achtergrond = vlak_rechthoek(0, 0, B, H, R)
    ico = icoon(soort, 7.5, boven + 8.0)
    txt = tekst(woord, 5.5, 14.0, boven + 8.0, B - 27.5)   # ruimte tot het nummer
    # nummer rechts: zwart rondje met het cijfer uitgespaard
    rx, ry, rr = B - 5.5, boven + 8.0, 4.2
    rondje = Part.Face(Part.Wire(Part.makeCircle(rr, V(rx, ry, 0))))
    cijfer = tekst(str(nummer), 5.0, 0, 0, 10)
    bb = cijfer.BoundBox
    cijfer.translate(V(rx - (bb.XMin + bb.XMax) / 2, ry, 0))
    txt = txt.fuse(rondje.cut(cijfer))
    if extra:
        txt = txt.fuse(tekst(extra, 3.0, 3.0, 3.3, B - 6.0))
    rand = 'stroke="#222222" stroke-width="0.3"' if kleur == "#FFFFFF" else 'stroke="none"'
    svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<svg xmlns="http://www.w3.org/2000/svg" width="%gmm" height="%gmm" viewBox="0 0 %g %g">\n'
           '  <g id="snijlijn"><path d="%s" fill="%s" %s/></g>\n'
           '  <g id="icoon"><path d="%s" fill="#111111" fill-rule="evenodd"/></g>\n'
           '  <g id="tekst"><path d="%s" fill="#111111" fill-rule="evenodd"/></g>\n'
           '</svg>\n') % (B, H, B, H, pad(achtergrond), kleur, rand, pad(ico), pad(txt))
    naam = os.path.join(MAP, "Label_%s.svg" % woord.capitalize())
    open(naam, "w").write(svg)
    print("geschreven:", naam)
