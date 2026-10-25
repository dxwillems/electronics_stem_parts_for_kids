# Maakt van elk model een printklaar 3MF-bestand voor OrcaSlicer / Bambu Studio:
# een object met twee onderdelen (houder op filament 4 = blauw, symbool op filament 2 = wit),
# en al in de printstand gelegd. Zo hoef je in de slicer niets samen te voegen.
# Uitvoeren (na het draaien van de modelscripts):
#   /Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd maak_3mf.py

import os
import zipfile

import FreeCAD as App
from FreeCAD import Vector as V

MAP = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.getcwd()
NAUWKEURIGHEID = 0.02   # maximale afwijking van de driehoeken t.o.v. het model, in mm
FILAMENT_HOUDER = 4     # plek in de AMS: blauw
FILAMENT_SYMBOOL = 2    # plek in de AMS: wit

# (FreeCAD-bestand, onderdeel daarin, printstand, naam van het 3MF-bestand)
# printstand: "ondersteboven" (bovenvlak op het bed), "rechtop" (zoals getekend) of
# "plat" (een staande plaat met zijn dikte langs X op zijn zijkant gelegd)
MODELLEN = [
    ("Lamphouder_E10", "Houder", "ondersteboven", "Lamphouder_E10"),
    ("Ledhouder_5mm", "Houder", "ondersteboven", "Ledhouder_5mm"),
    ("Drukknophouder", "Houder", "ondersteboven", "Drukknophouder"),
    ("Batterijhouder_2xAA", "Houder", "ondersteboven", "Batterijhouder_2xAA"),
    ("Potmeterhouder", "Houder", "ondersteboven", "Potmeterhouder"),
    ("Potmeterhouder", "Knop", "ondersteboven", "Potmeterhouder_Knop"),
    ("LDRhouder", "Houder", "ondersteboven", "LDRhouder"),
    ("Handgenerator", "Houder", "ondersteboven", "Handgenerator"),
    ("Motorhouder", "Houder", "ondersteboven", "Motorhouder"),
    ("Motorhouder", "Standaard", "plat", "Motorhouder_Standaard"),
    ("Propeller", "Propeller", "rechtop", "Propeller"),
    ("Spoelhouder_Rond", "Houder", "ondersteboven", "Spoelhouder_Rond"),
    ("Spoelhouder_Rond", "Wieg", "rechtop", "Spoelhouder_Rond_Wieg"),
    ("Spoelhouder_Rond", "Koker", "rechtop", "Spoelhouder_Rond_Koker"),   # op zijn kant, support onder de buis
    ("Wikkelhulp", "Wikkelhulp", "rechtop", "Wikkelhulp"),
    ("Spoelhouder_V2", "Houder", "ondersteboven", "Spoelhouder_V2"),
    ("Spoelhouder_V2", "Wieg", "rechtop", "Spoelhouder_V2_Wieg"),
    ("Spoelhouder_V2", "Koker", "rechtop", "Spoelhouder_V2_Koker"),   # op zijn kant, support onder de buis
    ("Wikkelhulp_V2", "Wikkelhulp", "rechtop", "Wikkelhulp_V2"),
    ("Wikkelhulp_V3", "Wikkelhulp", "plat", "Wikkelhulp_V3"),   # op zijn kant, support onder pen en zeskant
    ("Spoelhouder_V3", "Houder", "ondersteboven", "Spoelhouder_V3"),
    ("Spoelhouder_V3", "Koker", "rechtop", "Spoelhouder_V3_Koker"),   # op zijn kant, support onder de buis
    ("IJzerpoeder_Doos", "Frame", "rechtop", "IJzerpoeder_Doos_Frame"),
    ("IJzerpoeder_Doos", "Eindkap", "plat", "IJzerpoeder_Doos_Eindkap"),
    ("Zonnepaneel_Houder_Lego", "Houder", "ondersteboven", "Zonnepaneel_Houder_Lego"),
    ("Spoel_Electromagneet_Bananenbus", "Spoelkoker", "rechtop", "Spoel_Electromagneet_Bananenbus"),
]

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>
"""
RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
"""


def mesh_xml(obj_id, vorm):
    punten, driehoeken = vorm.tessellate(NAUWKEURIGHEID)
    regels = ['  <object id="%d" type="model">\n   <mesh>\n    <vertices>\n' % obj_id]
    regels += ['     <vertex x="%.5f" y="%.5f" z="%.5f"/>\n' % (p.x, p.y, p.z) for p in punten]
    regels.append('    </vertices>\n    <triangles>\n')
    regels += ['     <triangle v1="%d" v2="%d" v3="%d"/>\n' % t for t in driehoeken]
    regels.append('    </triangles>\n   </mesh>\n  </object>\n')
    return "".join(regels), len(driehoeken)


def schrijf_3mf(pad, naam, delen):
    """delen: lijst van (naam, vorm, filamentnummer); het eerste deel is de houder."""
    objecten, onderdelen, instellingen = [], [], []
    for i, (deelnaam, vorm, filament) in enumerate(delen, start=1):
        xml, aantal = mesh_xml(i, vorm)
        objecten.append(xml)
        onderdelen.append('    <component objectid="%d"/>\n' % i)
        instellingen.append(
            '  <part id="%d" subtype="normal_part">\n'
            '   <metadata key="name" value="%s"/>\n'
            '   <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
            '   <metadata key="extruder" value="%d"/>\n'
            '   <mesh_stat face_count="%d" edges_fixed="0" degenerate_facets="0" facets_removed="0"'
            ' facets_reversed="0" backwards_edges="0"/>\n'
            '  </part>\n' % (i, deelnaam, filament, aantal))
    totaal = len(delen) + 1
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<model unit="millimeter" xml:lang="en-US"'
             ' xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"'
             ' xmlns:BambuStudio="http://schemas.bambulab.com/package/2021">\n'
             ' <metadata name="Application">BambuStudio-01.09.00.70</metadata>\n'
             ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
             ' <metadata name="Title">%s</metadata>\n'
             ' <resources>\n%s'
             '  <object id="%d" type="model">\n   <components>\n%s   </components>\n  </object>\n'
             ' </resources>\n'
             ' <build>\n  <item objectid="%d" printable="1"/>\n </build>\n'
             '</model>\n' % (naam, "".join(objecten), totaal, "".join(onderdelen), totaal))
    config = ('<?xml version="1.0" encoding="UTF-8"?>\n<config>\n'
              ' <object id="%d">\n'
              '  <metadata key="name" value="%s"/>\n'
              '  <metadata key="extruder" value="%d"/>\n%s'
              ' </object>\n'
              '</config>\n' % (totaal, naam, delen[0][2], "".join(instellingen)))
    with zipfile.ZipFile(pad, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("3D/3dmodel.model", model)
        z.writestr("Metadata/model_settings.config", config)


for naam, deelnaam, stand, uitvoer in MODELLEN:
    doc = App.openDocument(os.path.join(MAP, naam + ".FCStd"))
    delen = [(deelnaam, doc.getObject(deelnaam).Shape.copy(), FILAMENT_HOUDER)]
    if doc.getObject("Symbool") and deelnaam in ("Houder", "Spoelkoker"):
        delen.append(("Symbool", doc.Symbool.Shape.copy(), FILAMENT_SYMBOOL))
    box = delen[0][1].BoundBox
    midden = V((box.XMin + box.XMax) / 2, (box.YMin + box.YMax) / 2, (box.ZMin + box.ZMax) / 2)
    for _, vorm, _ in delen:
        vorm.translate(midden * -1)
        if stand == "ondersteboven":
            vorm.rotate(V(0, 0, 0), V(1, 0, 0), 180)
        elif stand == "plat":
            vorm.rotate(V(0, 0, 0), V(0, 1, 0), 90)
    zmin = min(d[1].BoundBox.ZMin for d in delen[:1])
    for _, vorm, _ in delen:
        vorm.translate(V(0, 0, -zmin))
    schrijf_3mf(os.path.join(MAP, uitvoer + "-Print.3mf"), uitvoer, delen)
    print(uitvoer, "->", uitvoer + "-Print.3mf", [(d[0], "filament %d" % d[2]) for d in delen],
          "z %.2f tot %.2f" % (delen[0][1].BoundBox.ZMin, delen[0][1].BoundBox.ZMax))
    App.closeDocument(doc.Name)
