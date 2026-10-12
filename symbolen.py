# Schakelsymbolen als dunne plaatjes, om in een tweede kleur in het bovenvlak te printen.
# Elk symbool ligt plat in het XY-vlak rond de oorsprong, van z = 0 tot z = diepte,
# met de aansluitdraden langs de X-as van -lengte/2 tot +lengte/2.
# Wordt gebruikt door lamphouder_e10.py, zonnepaneel_houder_lego.py en spoel_bananenbus.py.

import math

import Part
from FreeCAD import Vector as V


def lijn(p, q, breedte, diepte, rond=True):
    """Rechte streep van p naar q (2D-punten), eventueel met ronde uiteinden."""
    (x0, y0), (x1, y1) = p, q
    lengte = math.hypot(x1 - x0, y1 - y0)
    vorm = Part.makeBox(lengte, breedte, diepte, V(0, -breedte / 2, 0))
    vorm.rotate(V(0, 0, 0), V(0, 0, 1), math.degrees(math.atan2(y1 - y0, x1 - x0)))
    vorm.translate(V(x0, y0, 0))
    if rond:
        for x, y in (p, q):
            vorm = vorm.fuse(Part.makeCylinder(breedte / 2, diepte, V(x, y, 0)))
    return vorm


def ring(x, y, straal, breedte, diepte):
    """Cirkel met hartlijn-straal `straal` en lijndikte `breedte`."""
    buiten = Part.makeCylinder(straal + breedte / 2, diepte, V(x, y, 0))
    return buiten.cut(Part.makeCylinder(straal - breedte / 2, diepte + 2, V(x, y, -1)))


def pijl(staart, punt, breedte, diepte, kop=2.6):
    """Pijl van staart naar punt met een driehoekige kop."""
    (x0, y0), (x1, y1) = staart, punt
    lengte = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / lengte, (y1 - y0) / lengte
    bx, by = x1 - ux * kop, y1 - uy * kop           # voet van de kop
    driehoek = Part.Face(Part.makePolygon([
        V(x1, y1, 0), V(bx - uy * kop / 2, by + ux * kop / 2, 0),
        V(bx + uy * kop / 2, by - ux * kop / 2, 0), V(x1, y1, 0)])).extrude(V(0, 0, diepte))
    return lijn(staart, (bx, by), breedte, diepte).fuse(driehoek)


def lamp(lengte, diepte, breedte=1.2, diameter=8.0):
    """Lamp: cirkel met een kruis, draad links en rechts."""
    r = diameter / 2
    k = r * math.sqrt(0.5)
    delen = [lijn((-k, -k), (k, k), breedte, diepte, False),
             lijn((-k, k), (k, -k), breedte, diepte, False),
             lijn((-lengte / 2, 0), (-r, 0), breedte, diepte, False),
             lijn((r, 0), (lengte / 2, 0), breedte, diepte, False)]
    return ring(0, 0, r, breedte, diepte).fuse(delen)


def spoel(lengte, diepte, breedte=1.0, bochten=3, straal=2.0):
    """Spoel: rij halve bogen, draad links en rechts."""
    half = bochten * straal
    delen = []
    for i in range(bochten):
        x = -half + (2 * i + 1) * straal
        boog = ring(x, 0, straal, breedte, diepte)
        delen.append(boog.cut(Part.makeBox(4 * straal, 2 * straal, diepte + 2,
                                           V(x - 2 * straal, -2 * straal - breedte / 2, -1))))
    delen.append(lijn((half, 0), (lengte / 2, 0), breedte, diepte, False))
    return lijn((-lengte / 2, 0), (-half, 0), breedte, diepte, False).fuse(delen)


def zonnecel(lengte, diepte, breedte=1.0, diameter=11.0, pijlkant=-1):
    """Zonnecel: cirkel met een cel erin (lange plaat = plus, aan de +X-kant),
    draad links en rechts, en twee lichtpijlen die schuin van boven (+Y) op de cirkel
    wijzen; pijlkant -1 = van linksboven, +1 = van rechtsboven."""
    r = diameter / 2
    plaat = 1.6                                      # afstand van de platen tot het midden
    delen = [lijn((plaat, -0.6 * r), (plaat, 0.6 * r), breedte, diepte),         # lange plaat (+)
             lijn((-plaat, -0.32 * r), (-plaat, 0.32 * r), breedte * 1.4, diepte),  # korte plaat (-)
             lijn((plaat, 0), (lengte / 2, 0), breedte, diepte, False),
             lijn((-lengte / 2, 0), (-plaat, 0), breedte, diepte, False)]
    s = math.sqrt(0.5)
    for zij in (-1.9, 1.9):                          # twee evenwijdige pijlen
        tx = pijlkant * ((r + 1.6) * s + zij * s)
        ty = (r + 1.6) * s - zij * s
        delen.append(pijl((tx + pijlkant * 5.5 * s, ty + 5.5 * s), (tx, ty), breedte, diepte))
    return ring(0, 0, r, breedte, diepte).fuse(delen)


def led(lengte, diepte, breedte=1.0, hoogte=9.0):
    """LED: driehoek (anode links, stroom loopt naar +X) met een streep aan de punt,
    draad links en rechts, en twee pijlen die schuin naar rechtsboven van de diode af wijzen."""
    h = hoogte / 2
    b = hoogte * 0.45                                # halve lengte van de driehoek
    delen = [lijn((-b, h), (-b, -h), breedte, diepte),
             lijn((-b, -h), (b, 0), breedte, diepte),
             lijn((b, 0), (-b, h), breedte, diepte),
             lijn((b + breedte / 2, -h), (b + breedte / 2, h), breedte, diepte),   # kathodestreep
             lijn((b + breedte / 2, 0), (lengte / 2, 0), breedte, diepte, False)]
    s = math.sqrt(0.5)
    for x, y in ((-b + 2.2, h + 1.2), (-b + 5.8, h - 0.2)):   # staarten, net boven de schuine zijde
        delen.append(pijl((x, y), (x + 5.5 * s, y + 5.5 * s), breedte, diepte))
    return lijn((-lengte / 2, 0), (-b, 0), breedte, diepte, False).fuse(delen)


def weerstand(lengte, diepte, breedte=1.0, lang=10.0, hoog=3.6):
    """Weerstand (Europees symbool): rechthoekje, draad links en rechts."""
    l, h = lang / 2, hoog / 2
    delen = [lijn((-l, h), (l, h), breedte, diepte),
             lijn((l, h), (l, -h), breedte, diepte),
             lijn((l, -h), (-l, -h), breedte, diepte),
             lijn((-l, -h), (-l, h), breedte, diepte),
             lijn((l, 0), (lengte / 2, 0), breedte, diepte, False)]
    return lijn((-lengte / 2, 0), (-l, 0), breedte, diepte, False).fuse(delen)


LETTERTYPE = ("/System/Library/Fonts/Supplemental/", "Arial Bold.ttf")


def tekst(inhoud, hoogte, diepte, lettertype=LETTERTYPE):
    """Tekst als plaatje, gecentreerd rond de oorsprong; hoogte = hoogte van de hoofdletters."""
    vlakken = []
    for teken in Part.makeWireString(inhoud, lettertype[0], lettertype[1], 10.0, 0):
        delen = sorted((Part.Face(w) for w in teken), key=lambda f: -f.Area)
        if not delen:
            continue
        letter = delen[0]
        for deel in delen[1:]:
            binnenin = letter.common(deel).Area > 1e-6
            letter = letter.cut(deel) if binnenin else letter.fuse(deel)
        vlakken.append(letter)
    vorm = vlakken[0].fuse(vlakken[1:]) if len(vlakken) > 1 else vlakken[0]
    box = vorm.BoundBox
    vorm.translate(V(-(box.XMin + box.XMax) / 2, -(box.YMin + box.YMax) / 2, 0))
    vorm.scale(hoogte / box.YLength)
    return vorm.extrude(V(0, 0, diepte))


def drukknop(lengte, diepte, breedte=1.0, opening=7.0):
    """Drukknop (maakcontact): twee contactpunten met een brug erboven die je omlaag drukt,
    draad links en rechts. De draden liggen op y = 0, de knop steekt naar +Y uit."""
    o = opening / 2
    brug = 2.6                                       # hoogte van de brug boven de contacten
    delen = [Part.makeCylinder(breedte, diepte, V(-o, 0, 0)),          # contactpunten
             Part.makeCylinder(breedte, diepte, V(o, 0, 0)),
             lijn((-o - 1.2, brug), (o + 1.2, brug), breedte, diepte),  # brug
             lijn((0, brug), (0, brug + 2.6), breedte, diepte),         # steel
             lijn((-1.8, brug + 2.6), (1.8, brug + 2.6), breedte, diepte),   # knop
             lijn((o, 0), (lengte / 2, 0), breedte, diepte, False)]
    return lijn((-lengte / 2, 0), (-o, 0), breedte, diepte, False).fuse(delen)


def plaats(vorm, x, y, z, hoek=0.0):
    """Draai het symbool om de Z-as en zet het op zijn plek; z is de onderkant."""
    vorm = vorm.copy()
    vorm.rotate(V(0, 0, 0), V(0, 0, 1), hoek)
    vorm.translate(V(x, y, z))
    return vorm
