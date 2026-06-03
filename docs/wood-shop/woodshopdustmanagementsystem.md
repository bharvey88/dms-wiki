# WoodshopDustManagementSystem

!!! note "Source"
    Mirrored from [WoodshopDustManagementSystem](https://dallasmakerspace.org/wiki/WoodshopDustManagementSystem) on the Dallas Makerspace wiki (CC BY-SA 3.0).

## Wood Shop Dust Management System

### Background

*Text by the late Walter Anderson*

Andrew Zalaket approached me and asked if I would create a system to monitor the Wood Shop dust bins and when they are full make a lot of noise, and send emails to the appropriate people. I agreed and he transferred the material; Raspberry Pi, Pi TFT Display, sensors, etc, that others who had previously worked on the project had pulled together.

In reviewing the material, it appears that they intended to use a Sparkfun/Adafuit time of flight sensor breakout board. I am not planning on using this sensor, since I believe it would be more work to make such a prototyping sensor work in a real world environment with a great deal of dust and grit. In fact the Wood Shop already owns and uses the sensor I am planning on adapting for this project. [Oneida Air Dust Sentry](https://www.oneida-air.com/inventoryD.asp?item_no=AXB999110B). This commercially packaged system already has a professionally packaged sensor and is very cost effective.

### Design

#### Reverse engineer Dust Sentry unit

The following are my notes from disassembling and reverse engineering the Dust Sentry sensor system

[![Notes on Dust Sensor](https://dallasmakerspace.org/w/images/c/c4/ReverseEngineerDustSensorNotes.png)](https://dallasmakerspace.org/wiki/File:ReverseEngineerDustSensorNotes.png)

Basically, the dust sensor system consists of two modules that operate at 24VDC. The first is the LED light, which flashes at a fixed rate when it is supplied 24 Volts. The other is an optical range detector which goes active high (24V) when an object is detected within its set range. There is a small knob on the sensor to control this range. To allow this sensor to be used with the Raspberry Pi (or any other embedded system) I added a optocoupler circuit (embedded in epoxy) that allows this signal from the sensor to trigger any chosen logic level such as 5V or 3.3V. This is accomplished by having the embedded system provide a Vcc, Gnd, and a connection to the signal line. I used a four pin connector, which I added to the sensor box.

Here is a photographic overview of the basic sensor modifications

[![Modified Sensor Overview](https://dallasmakerspace.org/w/images/thumb/1/11/ModifiedSensorOverview.jpg/1030px-ModifiedSensorOverview.jpg)](https://dallasmakerspace.org/wiki/File:ModifiedSensorOverview.jpg) [![OptoCoupler embedded in epoxy](https://dallasmakerspace.org/w/images/thumb/3/35/EpoxiedOptoCoupler.jpg/720px-EpoxiedOptoCoupler.jpg)](https://dallasmakerspace.org/wiki/File:EpoxiedOptoCoupler.jpg) [![Connector wiring](https://dallasmakerspace.org/w/images/thumb/7/71/LogicConnectorWiring.jpg/720px-LogicConnectorWiring.jpg)](https://dallasmakerspace.org/wiki/File:LogicConnectorWiring.jpg) [![Completed sensor modification](https://dallasmakerspace.org/w/images/thumb/b/b6/CompletedDustSensor.jpg/1024px-CompletedDustSensor.jpg)](https://dallasmakerspace.org/wiki/File:CompletedDustSensor.jpg)

#### Overall software requirements

Andrew and I agreed upon the following specifications

1\. Display general clean up after yourself message

2\. When sensor detects bin is full;

- Set off a VERY LOUD BUZZER (Sonalert)

- Send email to responsible group

3\. If triggered, then display message explaining that member must use RFID to turn off siren. They are then given some period of time (say 10-15 minutes) to empty bin and reset dust collection system. The persions RFID number is emailed to responsible group to monitor who turned off alarm.

4\. After time expired, check if still full, if so goto step 2, if not goto step 1
