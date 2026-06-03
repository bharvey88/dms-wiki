# MichiganMightyMite

!!! note "Source"
    Mirrored from [MichiganMightyMite](https://dallasmakerspace.org/wiki/MichiganMightyMite) on the Dallas Makerspace wiki (CC BY-SA 3.0).

## Michigan Mighty Mite QRP CW (Morse Code) Transmitter

[![MichiganMightyMiteComplete.jpg](https://dallasmakerspace.org/w/images/thumb/e/ed/MichiganMightyMiteComplete.jpg/600px-MichiganMightyMiteComplete.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteComplete.jpg)

**80m Morse Code Transmitter**
Dallas Makerspace
Amateur Radio Special Interest Group
Build class

### The Rules

If you build the transmitter according to the directions provided here, you will be in compliance with FCC rules concerning experimental radio transmitters, even if you do not have an Amateur Radio license. If your interested in modifying the transmitter we produce in this class, and you have an Amateur Radio license, basic guidelines to do so will be included in an appendix. You can also contact myself or other members of the Amateur Radio special interest group to help you in testing your modified transmitter to ensure it complies with FCC regulations.

### Basic description of circuit

This transmitter is a basic Pierce crystal oscillator. The combination of the T1 primary and capacitor C1 form what is known as an LC (inductor-capacitor) tank circuit with a tuned frequency that matches the oscillation of the crystal provided. This crystal's oscillations have an amplified feedback through the base and collector (through the LC tank circuits connection to this junction). The momentary contact switch turns the oscillator on, by completing the circuit with ground. The continuous wave (CW) oscillations are fed into the primary of T1, through a tap that matches the impedance of the primary to the collector of the transistor. The oscillations (AC electrical power) induce a similar AC voltage at the output of the transformer. This signal is then fed to two 100 ohm resistors in parallel to form what is called a 50 ohm dummy load. This dummy load simulates the inductance expected from an antenna. By using this dummy load we minimize the radio frequency (RF) power radiated by the circuit. This prevents the transmitter for causing undue interference; however, there is still enough radiated RF so that the signal can be picked up from a nearby radio receiver.

### Schematic and Circuit Layout Diagrams

[![MichiganMightyMiteSchematic.jpg](https://dallasmakerspace.org/w/images/thumb/7/79/MichiganMightyMiteSchematic.jpg/628px-MichiganMightyMiteSchematic.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteSchematic.jpg)

### Assembly Instructions

1\. Bare board and parts

[![MichiganMightyMiteBareBoardAndParts.jpg](https://dallasmakerspace.org/w/images/thumb/5/55/MichiganMightyMiteBareBoardAndParts.jpg/800px-MichiganMightyMiteBareBoardAndParts.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteBareBoardAndParts.jpg)

2\. MePADS and Cap glued in place

[![MichiganMightyMitePadsAndCapGlued.jpg](https://dallasmakerspace.org/w/images/thumb/c/c7/MichiganMightyMitePadsAndCapGlued.jpg/800px-MichiganMightyMitePadsAndCapGlued.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMitePadsAndCapGlued.jpg)

3\. R1, 10k resistor installed

[![MichiganMightyMite10kInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/1/18/MichiganMightyMite10kInstalled.jpg/800px-MichiganMightyMite10kInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMite10kInstalled.jpg)

4\. Q1, transistor installed

[![MichiganMightyMiteTransistorInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/0/02/MichiganMightyMiteTransistorInstalled.jpg/800px-MichiganMightyMiteTransistorInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteTransistorInstalled.jpg)

5\. Install tie points for power and ground

[![MichiganMightyMiteTiePointsInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/e/ed/MichiganMightyMiteTiePointsInstalled.jpg/800px-MichiganMightyMiteTiePointsInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteTiePointsInstalled.jpg)

6\. Solder R2 between E & D (2 53 ohm resistors)

[![MichiganMightyMiteR2Installed.jpg](https://dallasmakerspace.org/w/images/thumb/e/e3/MichiganMightyMiteR2Installed.jpg/800px-MichiganMightyMiteR2Installed.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteR2Installed.jpg)

7\. Solder XTAL1, (crystal) to A & F

[![MichiganMightyMiteCrystalInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/f/ff/MichiganMightyMiteCrystalInstalled.jpg/800px-MichiganMightyMiteCrystalInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteCrystalInstalled.jpg)

8\. Solder C2 (blue capacitor) between B & ground plane

[![MichiganMightyMiteC2Installed.jpg](https://dallasmakerspace.org/w/images/thumb/4/47/MichiganMightyMiteC2Installed.jpg/800px-MichiganMightyMiteC2Installed.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteC2Installed.jpg)

9\. Install R3&R4 (large resistor replaces R3&R4) between H & ground plane

[![MichiganMightyMiteR3R4Installed.jpg](https://dallasmakerspace.org/w/images/thumb/4/43/MichiganMightyMiteR3R4Installed.jpg/800px-MichiganMightyMiteR3R4Installed.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteR3R4Installed.jpg)

10\. Install switch between D & ground plane

[![MichiganMightyMiteSwitchInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/4/4a/MichiganMightyMiteSwitchInstalled.jpg/800px-MichiganMightyMiteSwitchInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteSwitchInstalled.jpg)

11\. Use wire to connect two front connectors on variable capacitor to A

[![MichiganMightyMiteC1WireInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/b/b5/MichiganMightyMiteC1WireInstalled.jpg/800px-MichiganMightyMiteC1WireInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteC1WireInstalled.jpg)

12\. Use wire to connect rear connector on variable capaitor to B

[![MichiganMightyMiteC1-2WireInstalled.jpg](https://dallasmakerspace.org/w/images/thumb/1/1c/MichiganMightyMiteC1-2WireInstalled.jpg/800px-MichiganMightyMiteC1-2WireInstalled.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteC1-2WireInstalled.jpg)

13\. Apply glue to copper, just inside the circle marked on the board

[![MichiganMightyMiteSpplyGlueToCircle.jpg](https://dallasmakerspace.org/w/images/thumb/c/c7/MichiganMightyMiteSpplyGlueToCircle.jpg/800px-MichiganMightyMiteSpplyGlueToCircle.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteSpplyGlueToCircle.jpg)

14\. Glue coil form in place

[![MichiganMightyMiteCoilFormGlued.jpg](https://dallasmakerspace.org/w/images/thumb/f/f2/MichiganMightyMiteCoilFormGlued.jpg/800px-MichiganMightyMiteCoilFormGlued.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteCoilFormGlued.jpg)

15\. Solder the bottom of the secondary coil to the ground plane and the top of the secondary to H

[![MichiganMightyMiteSolderSecondaryCoil.jpg](https://dallasmakerspace.org/w/images/thumb/5/52/MichiganMightyMiteSolderSecondaryCoil.jpg/800px-MichiganMightyMiteSolderSecondaryCoil.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMiteSolderSecondaryCoil.jpg)

16\. Solder the lower primary coil to B

[![MichiganMightyMitePrimaryLowerConnection.jpg](https://dallasmakerspace.org/w/images/thumb/b/b8/MichiganMightyMitePrimaryLowerConnection.jpg/800px-MichiganMightyMitePrimaryLowerConnection.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMitePrimaryLowerConnection.jpg)

17\. Solder the middle connection of the primary coil to G

[![MichiganMightyMitePrimaryTapConnection.jpg](https://dallasmakerspace.org/w/images/thumb/a/a1/MichiganMightyMitePrimaryTapConnection.jpg/800px-MichiganMightyMitePrimaryTapConnection.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMitePrimaryTapConnection.jpg)

18\. Solder the top of the primary coil to A

[![MichiganMightyMitePrimaryTopConnection.jpg](https://dallasmakerspace.org/w/images/thumb/e/ec/MichiganMightyMitePrimaryTopConnection.jpg/800px-MichiganMightyMitePrimaryTopConnection.jpg)](https://dallasmakerspace.org/wiki/File:MichiganMightyMitePrimaryTopConnection.jpg)

### Parts List (80m Version) with links to sources for each part

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th>Code</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>C1</td>
<td><a href="http://qrpme.com/?p=parts">2 x 265 pF Polyvaricon capacitor</a>, wired in parallel</td>
</tr>
<tr>
<td>C2</td>
<td><a href="http://www.newark.com/multicomp/mccc250v503my5u/ceramic-capacitor-0-05uf-250v/dp/97M4051">0.05uF Capacitor</a></td>
</tr>
<tr>
<td>R1</td>
<td><a href="http://www.newark.com/multicomp/mcf-0-25w-10k/carbon-film-resistor-10kohm-250mw/dp/38K0328">10k ohm, 1/4 watt, 5% resistor</a></td>
</tr>
<tr>
<td>R2</td>
<td><a href="http://www.newark.com/vishay-bc-components/pr02000202709jr500/metal-film-resistor-27-ohm-2-w/dp/53M5232">27 ohm, 2W, 5% resistor</a></td>
</tr>
<tr>
<td>R3, R4</td>
<td><a href="http://www.newark.com/panasonic-electronic-components/erg-2sj101/resistor-100-ohm-2w-5-axial/dp/52W7322">100 ohm, 2W, 5% resistor</a></td>
</tr>
<tr>
<td>S1</td>
<td>Momentary pushbutton switch</td>
</tr>
<tr>
<td>T1</td>
<td>Primary, 45 turns, tapped at 15 turns; Secondary 6 turns. Use 22 awg enameled wire on 1 1/4" diameter form (33mm film canister)</td>
</tr>
<tr>
<td>Q1</td>
<td><a href="http://www.newark.com/multicomp/2n3053/bipolar-transistor-npn-40v-to/dp/35C0698">2N3053</a> NPN Transistor</td>
</tr>
<tr>
<td>XTAL</td>
<td><a href="http://qrpme.com/?p=parts">3.579MHz (HC49) Crystal</a></td>
</tr>
<tr>
<td>Coil form</td>
<td><a href="https://www.thingiverse.com/thing:2531134">Thingiverse files</a></td>
</tr>
<tr>
<td>Miscellaneous</td>
<td>Single sided PC board (FR4) about 70mm x 100mm x 1.5mm,<br />
<a href="http://qrpme.com/?p=product&amp;id=MES">8 MeSquares or other small pieces of PC board</a>,<br />
22 gauge enameled wire (16 feet for primary and 3 feet for secondary,<br />
hook-up wire, super glue, solder</td>
</tr>
</tbody>
</table>

### Low pass filter (by band)

[![LowPassFilterSchematic.png](https://dallasmakerspace.org/w/images/thumb/b/be/LowPassFilterSchematic.png/600px-LowPassFilterSchematic.png)](https://dallasmakerspace.org/wiki/File:LowPassFilterSchematic.png)

| Band | C1    | C2     | C3     | C4    | L1/L3        | L2           | Toroid         |
|------|-------|--------|--------|-------|--------------|--------------|----------------|
| 160  | 820pF | 2200pF | 2200pF | 820pF | 30T (4.44uH) | 34T (5.61uH) | T50-2 (red)    |
| 80   | 470pF | 1200pF | 1200pF | 470pF | 25T (2.42uH) | 27T (3.01uH) | T37-2 (red)    |
| 40   | 270pF | 680pF  | 680pF  | 270pF | 21T (1.38uH) | 24T (1.70uH) | T37-6 (yellow) |
| 30   | 270pF | 560pF  | 560pF  | 270pF | 19T (1.09uH) | 20T (1.26uH) | T37-6 (yellow) |

### Additional Reference Material

- Excellent introduction to building circuits with the [Manhattan Circuit building technique](http://www.qrpme.com/docs/K7QO%20Manhattan.pdf)
- [W2AEW Builds the mighty mite](https://youtu.be/2AdW9Zpl2Es)
- [Mighty simple shortwave transmitter](http://makerf.com/posts/mighty_simple_shortwave_transmitter)
- [Hack-a-day minimal mighty mite](http://hackaday.com/2015/09/29/minimal-mighty-mite/)
- [So you want to be a shortwave pirate broadcaster?](http://makerf.com/posts/so_you_want_to_be_a_shortwave_pirate) -- Describes how to modify mighty mite circuit to transmit AM voice
