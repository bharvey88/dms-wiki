# Self Driving RC Car

!!! note "Source"
    Mirrored from [Self Driving RC Car](https://dallasmakerspace.org/wiki/Self_Driving_RC_Car) on the Dallas Makerspace wiki (CC BY-SA 3.0).

## Overview

Self driving autonomous RC Car. The RC car is controlled by a modified RC controller with inputs from an Arduino connected to a PC. The PC determines the direction of the RC car by interpreting a visual display in front of the RC car. The visual display is sent from the front of the RC car via an android phone to the PC via WIFI wireless connection. The visual display is interpreted by the PC using a Neurel Net algorithm. The Neurel Net algorithm looks for dissimilar visual displays (in greyscale) of a defined track. Based on the algorithm results the PC feeds instructions to the Arduino controller so the RC follows the track.

## Members

- [Larry D'Agostino](https://dallasmakerspace.org/wiki/User:Larrydag)

## Parts List

- RC Car: Hotwheels ([Walmart](http://www.walmart.com/ip/Hot-Wheels-ZL1-Remote-Controlled-Vehicle/21984629))
- Android phone
- Arduino Uno
- Laptop
- Opto-isolator: 4N35 or 4N38 (qty 4)
- 1K Resitor (qty 4)
- breadboard and wires

## Assembly

## Status

- All parts assembled
- All software installed
- PC control to Arduino works
- Android to PC video feed works

### Next Steps

- Video capture is not working properly. Fix Java program.
- Perform autonomous test
- Port PC Java apps to Python
- Port Neural Net algorithm to R

## Resources

- Diagrams

- [![](https://dallasmakerspace.org/w/images/thumb/5/52/Opto_schem.png/112px-Opto_schem.png)](https://dallasmakerspace.org/wiki/File:Opto_schem.png)

  Opto-isolator circuit diagram

- [![](https://dallasmakerspace.org/w/images/thumb/3/31/Rccar_bb.png/120px-Rccar_bb.png)](https://dallasmakerspace.org/wiki/File:Rccar_bb.png)

  Arduino controller connections

- Software for android, arduino, and PC: [NNRCcar](https://github.com/dps/nnrccar/blob/master/arduino/serialrccar/serialrccar.pde)

## Credits

Originally designed and developed by [David Singleton](http://blog.davidsingleton.org/nnrccar/)
