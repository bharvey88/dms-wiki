# EMCO PC Mill 50

!!! note "Source"
    Mirrored from [EMCO PC Mill 50](https://dallasmakerspace.org/wiki/EMCO_PC_Mill_50) on the Dallas Makerspace wiki (CC BY-SA 3.0).

[![](https://dallasmakerspace.org/w/images/thumb/1/18/Emco.jpg/300px-Emco.jpg)](https://dallasmakerspace.org/wiki/File:Emco.jpg) [](https://dallasmakerspace.org/wiki/File:Emco.jpg)The EMCO Mill

Regrettably, the EMCO PC 50 has been permanently removed from service.

[Here is the page](../machine-shop/emco-mill-retrofit.md) that describes the retrofit that was performed on it to make it functional.

This CNC Mill currently uses the [Portable CNC Cart](../inactive-projects/portable-cnc-cart.md).

This page will provide information on its design and function.

## EMC2 Software Settings

- Use the Parallel port at 0xE800

## Motor

Picture of the motor faceplate: [Media:2013-02-13_18-16-10_182.jpg](https://dallasmakerspace.org/w/images/0/04/2013-02-13_18-16-10_182.jpg)

## Steve Alaniz's Operation Guide

- There is an on/off switch for the unit.
- A knob to turn on the spindle motor and two big emergency stop buttons on the front and side in case something goes horribly wrong.

- I (Steve!) added an Arduino to monitor the spindle EStop buttons and to control the air. Turning the spindle on will enable the air flow and EStop will kill both the spindle and air. You will also be prompted to turn the spindle all the way off if you happen to leave it on. The display will give an estimated spindle speed. It is derived from the speed control potentiometer and should actually be quite accurate.

- The best materials to cut are wood, plastic and Aluminum However it *CAN* cut steel with the correct settings and you may want to use a liquid coolant for steel instead of air just to be sure. This is a small mill with a low spindle speed of about 2000 RPM max. I've actually limited the top speed having read that there is a point where speed trades off for the motor power so you'd have a spindle moving very fast but easy to jam. Most small mills have a top speed of about 2200 RPM. I know there are people familiar with mills and I would like to hear from them what cut speed and cut depth would be appropriate for a 2200 RPM spindle speed.

## Operation

The steps for operation are:

- Power up the computer.
- Launch the Linux CNC program
- Load your G-Code file
- Power on the Emco
- Toggle Machine Power \[F2\] or the orange icon circle with a vertical bar.
- Home all (Home finds the home switch and does a fine adjustment. The switches may be noisy and I think Debounce may need to be tweaked. If home fails just retry for now)
- Set the X Y and Z axis and set the 0 points if you need to by selecting an axis and using Touch Off to zero that axis.
- Hit run and keep your fingers crossed.

- [![](https://dallasmakerspace.org/w/images/thumb/0/0b/EmcoBOB.jpeg/120px-EmcoBOB.jpeg)](https://dallasmakerspace.org/wiki/File:EmcoBOB.jpeg)

  Break Out Board connections

- [![](https://dallasmakerspace.org/w/images/thumb/7/71/EmcoVFD.jpg/120px-EmcoVFD.jpg)](https://dallasmakerspace.org/wiki/File:EmcoVFD.jpg)

  VFD connections and control

[File:EMCOarduinoCODE.rtf](https://dallasmakerspace.org/wiki/File:EMCOarduinoCODE.rtf)
