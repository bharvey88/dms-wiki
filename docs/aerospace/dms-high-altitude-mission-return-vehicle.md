# DMS High Altitude Mission Return Vehicle

!!! note "Source"
    Mirrored from [DMS High Altitude Mission Return Vehicle](https://dallasmakerspace.org/wiki/DMS_High_Altitude_Mission_Return_Vehicle) on the Dallas Makerspace wiki (CC BY-SA 3.0).

[![](https://dallasmakerspace.org/w/images/thumb/5/57/2016-02-09_23.44.05.jpg/300px-2016-02-09_23.44.05.jpg)](https://dallasmakerspace.org/wiki/File:2016-02-09_23.44.05.jpg) [](https://dallasmakerspace.org/wiki/File:2016-02-09_23.44.05.jpg)Mission Return Vehicle

## Overview

The return vehicle is the drone which will be dropped from a high altitude balloon during the [DMS High Altitude Balloon](dms-high-altitude-balloon.md) mission. It will be capable of detaching itself from the balloon at a predetermined altitude and autonomously gliding to a target location (which will most likely be the launch point).

## Background

Perusing similar HAB projects, it seems the glider designs vary. There is no consensus on any particular aerodynamic aspect, like aspect ratio. It may not be difficult at all to get something that will at least work.

## Design

### Mission Profile

Extremely high altitude gliding will likely call for a dive to denser, warmer air. Once an altitude and / or speed is reached where control is established, the aircraft may need to maneuver through a jet stream or air corridor. If no maneuvering is required it can glide directly to the target return point and kill altitude.

Whether maneuvering will be required is not presently known. If it's needed, the UAV will need to be able to determine its flight path autonomously. The potential for insufficient height / glide range needs to be evaluated. If there's a substantial chance of not having sufficient range, alternate landing sites should be available, and the computer should be able to redirect itself to the best one.

### Aircraft

A flying wing design is the current vehicle selection. This is in the Aero/RC corner at the makerspace. It's a derivative of the [FT Versa Wing](https://dallasmakerspace.org/w/index.php?title=FT_Versa_Wing&action=edit&redlink=1), with an enlarged center section. It has been glide tested, and performance seems adequate.

### Electronics

The aircraft will employ a PixHawk or APM. It will also have a GoPro, OSD, and FPV system, a telemetry transmitter, and an APRS radio. More detail is available on the talk thread.

### Specifications

|               |                                               |
|---------------|-----------------------------------------------|
| Wingspan      | 46" (1168mm)                                  |
| Wing Area     | 465 sq. in. (3.23 sq/ft) (29.99 dm^2)         |
| Wing Loading  | TBD                                           |
| Flying Weight | TBD                                           |
| Servos        | \(2\) 9g micro metal gear with grease removed |

## References

- [US Standard Atmosphere](http://www.engineeringtoolbox.com/standard-atmosphere-d_604.html)
