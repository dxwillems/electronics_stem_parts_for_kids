# Electronics STEM parts for kids

3D-printable modules for teaching kids the basics of electronics: a lamp, an LED, a solar panel, a coil and more, each in its own sturdy holder with proper 4 mm banana sockets.

The ready-made school experiment parts from China turned out to be too small and too fragile for children's hands, and they use tiny binding posts instead of real connectors. These are redrawn from scratch in FreeCAD: bigger, tougher, and built around standard 4 mm panel-mount banana sockets so normal lab leads plug straight in.

As a bonus, the modules are designed to click onto a LEGO-compatible baseplate, so a circuit stays put on the table.

![E10 lamp holder](Lamphouder_E10.png)

## Modules

Every module clicks onto a LEGO-compatible baseplate; only the iron powder viewer is a loose part.

| Module | Files | Size (mm) | LEGO base | Status |
|---|---|---|---|---|
| E10 lamp holder | `Lamphouder_E10.*` | 63.8 × 63.8 × 35.2 | yes, 8 × 8 studs | printed and working |
| 5 mm LED holder | `Ledhouder_5mm.*` | 95.8 × 47.8 × 35.2 | yes, 12 × 6 studs | printed and working |
| Push button holder | `Drukknophouder.*` | 63.8 × 63.8 × 35.2 | yes, 8 × 8 studs | printed and working |
| Hand crank generator | `Handgenerator.*` | 127.8 × 79.8 × 35.2 | yes, 16 × 10 studs | printed and working |
| Motor with propeller | `Motorhouder.*`, `Propeller.*` | box 63.8 × 63.8 × 35.2, stand 69.5 high | yes, 8 × 8 studs | printed and working |
| Iron powder viewer | `IJzerpoeder_Doos.*` | 162.4 × 108.4 × 11.2 (with end cap) | no | printed and working |
| Solar panel holder | `Zonnepaneel_Houder_Lego.*` | 151.8 × 71.8 × 35.2 | yes, 19 × 9 studs | printed and working |

The file names are Dutch: *lamphouder* = lamp holder, *zonnepaneel* = solar panel, *spoel* = coil, *houder* = holder, *bovenaanzicht* / *onderaanzicht* / *onderkant* = top view / bottom view / underside.

### E10 lamp holder

A square block with an E10 bulb base screwed on top and a red and a black banana socket in front of it.

| Top | Bottom |
|---|---|
| ![Top view](Lamphouder_E10_bovenaanzicht.png) | ![Bottom view](Lamphouder_E10_onderaanzicht.png) |

- The bulb base is fixed from above with two small screws (2.9 mm self-tapping or M3, 6–8 mm long) into 2.5 mm pilot holes. Under each hole the top plate is thickened so the screw has 8 mm of material.
- The slot under the bulb base leaves room for its rivet and lets both wires drop into the box. One wire goes to the solder tag (centre contact), the other to the bracket itself, for example under a screw head.
- The block is square on purpose: the opening underneath is 45 × 45 mm, so you can reach the socket nuts and solder tags with your fingers.

### 5 mm LED holder

A box for a standard 5 mm LED with its series resistor, made to connect straight to a 5 V supply. The top shows the circuit between the two banana sockets: red (plus), resistor, LED, black (minus), with the resistor value printed under it.

| View | Top |
|---|---|
| ![LED holder](Ledhouder_5mm.png) | ![Top view with circuit](Ledhouder_5mm_bovenaanzicht.png) |

- The LED goes in from underneath through a 5.2 mm hole; its collar sits in a recess under the top plate, so the dome sticks out about 5 mm. A drop of glue behind it stops it being pushed back in.
- The resistor lies on top, behind its symbol, with its legs through two 1.2 mm holes 10.16 mm apart (the usual pitch for a 1/4 W resistor). Solder the wires to the legs inside the box.
- Resistor value for a red LED on 5 V: R = (5 V − 2.0 V) / I. 150 Ω gives 20 mA, the LED's rated maximum; **220 Ω** gives about 14 mA, still bright, and leaves margin for a supply slightly above 5 V or an LED with a lower forward voltage.- Wiring: red socket → resistor → long LED leg (anode); short LED leg (cathode) → black socket. The triangle in the symbol points the same way.
- Both socket nuts sit straight above the open underside (77 × 29 mm).

### Push button holder

A box the same size as the lamp holder for a 12 mm momentary push button (PBS-33B, normally open), with the push-button symbol drawn between the two banana sockets and the button.

| View | Top |
|---|---|
| ![Push button holder](Drukknophouder.png) | ![Top view with push-button symbol](Drukknophouder_bovenaanzicht.png) |

- The button hole is 11.6 mm. The button only allows a 3 mm panel, so the top plate is thinned to 2.4 mm under the button (a 20 mm recess from below) and its nut still fits on the 6 mm thread.
- The symbol shows two contacts with a bridge above them that the button pushes down; a line runs from each contact to a socket.
- The button and both socket nuts sit straight above the 45 × 45 mm opening underneath.

### Hand crank generator

A box for a small hand crank generator (blue gearbox with a motor). The gearbox stands in a well in the top with the motor pointing down into the box and the crank turning on top; the generator symbol (a circle with a G) sits next to the two banana sockets.

| View | Top |
|---|---|
| ![Hand crank generator](Handgenerator.png) | ![Top view with generator symbol](Handgenerator_bovenaanzicht.png) |

- The gearbox block (50 × 25.5 × 17.8 mm) sits 8 mm deep in a well with 0.4 mm clearance per side, so it stays upright and cannot twist when you crank.
- The floor of the well is shaped to the underside of the gearbox: a round opening for the blue collar around the motor, a slot for the 2.2 mm rib that runs along the motor side, and below that a slitted collar around the 24.35 mm motor. A cable tie around that collar clamps the motor. The motor hangs about 3.5 mm past the end of the gearbox, so the well is open at that end.
- The box is wide (16 × 10 studs) so there is room for your fingers: 33 mm between the motor cup and the socket nuts, and both nuts sit well inside the opening underneath.
- The crank arm is about 52 mm long; the sockets are placed beyond its reach so plugged-in leads do not get hit.
- Measured on the real part: block size, collar height, motor diameter and length, how far the motor hangs past the end, rib thickness and crank axis position. Still estimated: the diameter of the blue collar (28 mm; the opening is 29 mm) and the height of the rib.
- Fast cranking can give well over 6 V, which is too much for the LED module with its 220 Ω resistor; crank gently or use the lamp.

### Motor with propeller

A box with the motor symbol (a circle with an M) and the two banana sockets, plus an upright stand that holds a Sol Expert SOL300 solar motor with its shaft horizontal, so the propeller blows air sideways.

| View | Top of the box |
|---|---|
| ![Motor with propeller](Motorhouder.png) | ![Top view with motor symbol](Motorhouder_bovenaanzicht.png) |

- Three parts to print: the box (`Motorhouder-Print.3mf`, upside down with the white symbol), the stand (`Motorhouder_Standaard-Print.3mf`, lying flat on its side) and the propeller (`Propeller-Print.3mf`). None need support.
- The stand is a 7 mm plate with a 24.5 mm hole; three small ribs in the hole squeeze the 24.2 mm motor. A 24 × 7 mm tab under the stand goes 11 mm deep into a slot in the box; fix it with a drop of glue. The motor wires go down behind the stand through a 6 mm hole.
- The motor axis is 42 mm above the box, so a 70 mm propeller clears the top by 7 mm.
- The propeller has three blades at 28°, 70 mm across, and a 2 mm hole that presses onto the motor shaft. The blades stand on their lower edge on the bed, so it prints without support.
- The SOL300 starts at 8 mA, so it runs from the solar panel, the hand crank generator, batteries or 5 V. Swapping the leads reverses the motor, and the propeller then blows the other way.
- Not yet measured on the real motor: its length and the length of its shaft.

### Iron powder viewer

A sealed box for iron powder to show magnetic field lines: two clear 2 mm sheets with a 4 mm chamber between them, held in a blue frame. Lay a magnet under or on top of it and tap gently.

![Iron powder viewer](IJzerpoeder_Doos.png)

- Both sheets slide into grooves from the open short side; an end cap closes that side. The end cap is 7 mm wide, the same as the frame border on the other sides.
- To fill: slide both sheets in, stand the box on its closed end and pour 5–10 g of iron powder through the open side with a paper funnel. More is not needed, and with more the powder cannot move freely.
- Seal it: fine powder creeps through small gaps. Put a thin line of glue in the grooves or tape the edges of the window, and glue the end cap on. The sheets are PET, so use super glue or clear silicone sealant, not a solvent-based glue.
- Print the frame flat and the end cap flat with its plug facing up; no support. The grooves are 2.4 mm high for 2 mm sheets, because the 4 mm overhang above them sags a little when printed.
- Never put a magnet straight into loose iron powder: fine powder sticks to it and is very hard to get off.

### Solar panel holder

A long rectangle for a 110 × 60 × 3 mm panel, with the two sockets side by side next to the panel.

| Top | Underside |
|---|---|
| ![Solar panel holder](Zonnepaneel_Houder_Lego.png) | ![Bottom view](Zonnepaneel_Houder_Lego_onderaanzicht.png) |

- The panel goes in from underneath and rests against a 2.5 mm lip that covers its black border. In the LEGO version it clicks in without glue: the back long side has three fixed hooks, the front long side has two catches on flexible tongues (the L-shaped slots you see next to the panel). Tilt the panel, tuck its back edge above the hooks, then press the front edge up until the tongues click. A first version with fixed catches on both sides was too stiff: the panel did not go in. The pocket is 110.7 × 60.8 mm for a panel measured at 110.0 × 60.1 mm, with square corners to match the panel.
- Both socket holes sit straight above the open underside, clear of the LEGO clamp rim, so the sockets and nuts can be fitted from below. An earlier version with the sockets on ears made that impossible.

## Circuit symbols

Each box has the schematic symbol of its part between the two banana sockets, inlaid flush in the top surface for printing in white: a circle with a cross for the lamp, a resistor and a diode triangle with two arrows for the LED, a circle with an M for the motor, a circle with a cell and two light arrows for the solar panel, and a row of bumps for the coil.

| Lamp | LED | Solar panel | Coil |
|---|---|---|---|
| ![Lamp symbol](Lamphouder_E10_bovenaanzicht.png) | ![LED symbol](Ledhouder_5mm_bovenaanzicht.png) | ![Solar cell symbol](Zonnepaneel_Houder_Lego_bovenaanzicht.png) | ![Coil](Spoelhouder_V3.png) |

- The symbol is 0.4 mm deep, two layers at 0.2 mm layer height.
- Easiest way to print in two colours: open the `-Print.3mf` file of the module in OrcaSlicer or Bambu Studio. Do not load the holder and the symbol as two separate objects: the slicer then reports g-code path conflicts, because they occupy the same space.
- Single-colour printer: use the STL files in `STL/`. `<module>.stl` is the holder with the symbol engraved 0.4 mm deep; `<module>-Symbool.stl` is the symbol as a separate part, for slicers that combine STL parts.
- The lamp and solar panel holders print upside down, so the symbol is in the first two layers on the bed.
- The symbols are small (the lamp symbol is 9 mm across, lines 1.0 to 1.2 mm wide) because the space between the sockets is limited. They print cleanly as two white layers.

## More modules

All modules in this README have been printed and work, except the battery module, which is drawn but not yet printed.

| Module | Files | Notes |
|---|---|---|
| Push button | `Drukknophouder.*` | 12 mm PBS-33B button |
| Potentiometer | `Potmeterhouder.*` | 100 Ω 4 W wirewound potentiometer, sunk in a recess; separate knob (`Potmeterhouder_Knop-Print.3mf`) clamps with an M3 set screw; shorten the long shaft to about 22 mm |
| LDR | `LDRhouder.*` | LDR in a small pocket on top; always in series with a consumer |
| Battery 2 × AA (3 V) | `Batterijhouder_2xAA.*` | not yet printed; open 2 × AA holder in a recess; the crocodile clips can clip onto the socket tabs inside |
| Coil v3 | `Spoelhouder_V3.*` | 30 mm coil on a 10.4 mm core with room for an M6 × 35 bolt as iron core. Use it lying in the shallow pocket (iron powder box on the flanges, field from pole to pole) or upright in the well (powder box over one pole, about three times more field at the powder). Sockets in the front, three compass pockets |
| Winding aid | `Wikkelhulp_V3.*` | one piece with a 1/4" hex shank: wind the coil tube with a cordless screwdriver, no bolt needed |

## Role labels

`labels/` holds three SVG labels for a Cricut (print then cut, or vinyl):
**1 BRON** (yellow, "max. 1 bron aansluiten"), **2 REGELAAR** (white, "nooit zonder verbruiker") and **3 VERBRUIKER** (green, "min. 1 verbruiker aansluiten"). A circuit always needs at least one source and one consumer; a controller is optional.

## Parts to buy

### Parts for the finished modules

| Part | Used in | Link |
|---|---|---|
| E10 bulb base with bracket (41 mm long, two screw holes) | lamp holder | https://amzn.eu/d/00OeK9Ge |
| E10 bulbs | lamp holder | https://amzn.eu/d/08Ck8Mhr |
| Red 5 mm LED and a 220 Ω 1/4 W resistor | LED holder | – |
| Enamelled copper wire 0.3 mm, 100 m (50 m is enough) | coil v3 | https://amzn.eu/d/0dwjVQfA |
| Gebildet 2 × AA battery holders with crocodile clips | battery module | https://amzn.eu/d/0gKbiuqp |
| Iron powder, 200 g | iron powder viewer | https://amzn.eu/d/0hN4Aijz |
| OFFCUP clear sheets, 2 mm, 10.2 × 15.2 cm (pack of 11) | iron powder viewer, two per box | https://amzn.eu/d/03hC4ULd |
| Sol Expert SOL300 solar motor (0.18–6 V, Ø 24.2 mm) | motor with propeller | https://www.conrad.nl/nl/p/sol-expert-90002l-sol300-solarmotor-1371438.html |
| Hand crank generator kit, 3–6 V | hand crank generator | https://amzn.eu/d/02YDxxYm |
| Red push button 12 mm, PBS-33B | push button holder | https://www.tinytronics.nl/nl/schakelaars/manuele-schakelaars/drukknoppen-en-schakelaars/rode-drukknop-12mm-reset-pbs-33b |
| Dewin solar panel 6 V 1 W, 110 × 60 mm | solar panel holder | https://amzn.eu/d/03TlLYnt |
| 4 mm panel-mount banana sockets, red and black, 12 mm mounting hole (Cleqee, pack of 10) | all modules, two each | https://amzn.eu/d/09S5gH5t |
| Screws 2.9 mm self-tapping or M3, 6–8 mm | lamp holder, two | – |

### Conrad order for the next modules

Ordered from Conrad for the dimmer and light sensor modules, and for the motor module. The dimmer uses one wirewound potentiometer for both the E10 lamp and the LED module. Prices are what Conrad charged at the time of ordering, including VAT.

| Qty | Part | Conrad nr. | For | Unit price | Link |
|---|---|---|---|---|---|
| 1 | KYOCERA/AVX 3104604002 wirewound potentiometer, 100 Ω, 4 W, linear, 6 mm shaft, M10 thread | 2827033 | dimmer: dims the E10 lamp and, a little, the LED module (max 0.2 A) | € 12.99 | https://www.conrad.nl/nl/p/kyocera-avx-3104604002-3104604002-draadpotmeter-mono-4-w-100-1-stuk-s-2827033.html |
| 3 | LUNA Optoelectronics PDV-P8103 light dependent resistor (LDR), 16–33 kΩ at 10 lux | 1762910 | light sensor module | € 1.79 | https://www.conrad.nl/nl/p/luna-optoelectronics-pdv-p8103-fotoweerstand-ldr-tht-1-stuk-s-150-v-max-l-x-b-x-h-4-29-x-5-08-x-2-mm-1762910.html |
| 4 | Sol Expert SOL300 solar motor, 0.18–6 V, starts at 8 mA, Ø 24.2 mm | 1371438 | motor with propeller | € 2.29 | https://www.conrad.nl/nl/p/sol-expert-90002l-sol300-solarmotor-1371438.html |

Notes:
- The 100 Ω wirewound potentiometer can carry about 0.2 A (√(4 W / 100 Ω)). Use E10 bulbs of 0.2 A or less with it; for 0.3 A bulbs the 50 Ω version (Conrad 444782) is the safe choice.
- Put the LDR in series with something (for example the LED module), never straight across the supply.

## Printing

- The underside of every box carries the engraved text "designed by d-x.nl" on the inside of the top plate, mirrored so it reads correctly from below.

- Every printable part is available as a ready-to-print `-Print.3mf` (already in its print position, two colours where there is a symbol) and as STL in the `STL/` folder. The `-Pastest.stl` files are the bottom 6 mm of a box, to check the LEGO fit quickly.
- Lamp holder, solar panel holder and the other boxes: print **upside down** (top face on the bed). No support needed; the LEGO clamp rim blends into the wall at 45°.
- Coil v3: the box prints upside down; the coil tube prints on its side with support only under the tube.
- All parts are printed in Bambu Lab PLA Basic Blue, and the models and pictures use that colour (#0A2989). Any rigid filament works. The coil dissipates little power at sensible currents, but PLA softens around 60 °C, so do not leave a coil running at high current.

### LEGO fit

The underside has a channel that grips the outer row of studs between the outer wall and an inner rib. The channel leaves 0.05 mm clearance per side around a 4.8 mm stud, and small crush ribs on the inner wall each squeeze 0.2 mm into a stud.

A first print of the lamp holder with a plain, slightly wider channel slid over the studs but did not hold, which is why the ribs were added. The lamp holder has a rib at every stud along its sides (24 ribs). The LEGO solar panel holder is much larger and has one at every second stud (26 ribs), so it does not become too hard to press on.

The fit depends on your printer. Print the test slice first (for example `STL/Lamphouder_E10-Pastest.stl`): it is only the bottom 6 mm and prints quickly. If the fit is too loose or too tight for your printer, open an issue and the clamp ribs can be adjusted.

## Measure before you print

Only some dimensions come from product listings; the rest are estimates from photos. Check these against the real parts:

| Dimension | Value in the model | Source |
|---|---|---|
| Socket mounting hole | 12.2 mm | listing: 12 mm, panel up to 6 mm thick |
| Socket depth below the top plate | 28 mm | estimated |
| Socket collar and nut diameter | 16 mm and 17 mm | estimated |
| Solar panel | 110.0 × 60.1 × 3 mm, 0.35 mm clearance all round, square corners | measured |
| E10 bracket length | 41 mm | listing |
| E10 bracket hole spacing | 32 mm centre to centre | estimated from the photo |

## Safety

These modules are for low-voltage experiments only: batteries, small solar panels and current-limited bench supplies. Never connect them to mains voltage.

## Licence

The designs and documentation in this repository are © Dave Willems and licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You may copy, print, change and share them, also commercially, as long as you give credit and share your changes under the same licence. The full text is in [LICENSE](LICENSE).

---

LEGO® is a trademark of the LEGO Group, which does not sponsor, authorise or endorse this project.
