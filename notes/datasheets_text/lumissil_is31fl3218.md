IS31FL3218

18 CHANNELS LED DRIVER

September 2024

GENERAL DESCRIPTION  FEATURES
IS31FL3218  is  comprised  of  18  constant  current    2.7V to 5.5V supply
| channels  | each  with  | independent  | PWM  | control,  |     |     |
| --------- | ----------- | ------------ | ---- | --------- | --- | --- |
  I2C interface, automatic address increment
designed for driving LEDs. The output current of each
function
channel can be set at up to 38mA (Max.) by an external
  Internal reset register
resistor. The average LED current of each channel can
  Modulate LED brightness with 256 steps PWM
be changed in 256 steps by changing the PWM duty
  Each channel can be controlled independently
cycle through an I2C interface.
  -40°C to +85°C temperature range
The chip can be turned off by pulling the SDB pin low or
  QFN-24 (4mm×4mm), SOP-24 packages
| by  using  | the  software  | shutdown  | feature  | to  reduce  |     |     |
| ---------- | -------------- | --------- | -------- | ----------- | --- | --- |
  RoHS & Halogen-Free Compliance
power consumption. The slave address is fixed “1010
1000”.    TSCA Compliance
IS31FL3218 is available in QFN-24 (4mm × 4mm) and  APPLICATIONS
SOP-24 packages. It operates from 2.7V to 5.5V over
  Mobile phones and other hand-held devices for
the temperature range of -40°C to +85°C.
LED display
    LED in home appliances

TYPICAL APPLICATION CIRCUIT

VBattery
|     | VBattery |     |     | 7   |     |     |
| --- | -------- | --- | --- | --- | --- | --- |
3
OUT1
|     |     | VCC |     | 8   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
OUT2
|     | 1   | F 0.1 F |     | 9   |     |     |
| --- | --- | ------- | --- | --- | --- | --- |
OUT3
10
OUT4
11
OUT5
|     | VDD |     |     | 12  |     |     |
| --- | --- | --- | --- | --- | --- | --- |
OUT6
13
OUT7
4.7k 4.7k
|     |     |     | IS31FL3218 | 14  |     |     |
| --- | --- | --- | ---------- | --- | --- | --- |
OUT8
|     |     | 5   |     | 15   |     |     |
| --- | --- | --- | --- | ---- | --- | --- |
|     |     | SDA |     | OUT9 |     |     |
6
|     | Micro      |     |     | 16    |     |     |
| --- | ---------- | --- | --- | ----- | --- | --- |
|     |            | SCL |     | OUT10 |     |     |
|     | Controller | 24  |     | 17    |     |     |
|     |            | SDB |     | OUT11 |     |     |
18
|     |     | 100k |     | OUT12 |     |     |
| --- | --- | ---- | --- | ----- | --- | --- |
19
OUT13
20
OUT14
21
|     |     | 2     |     | OUT15 |     |     |
| --- | --- | ----- | --- | ----- | --- | --- |
|     |     | R_EXT |     | 22    |     |     |
OUT16
|     |     | 3.3k |     | 23    |     |     |
| --- | --- | ---- | --- | ----- | --- | --- |
|     |     | 4    |     | OUT17 |     |     |
|     |     | GND  |     | 1     |     |     |
OUT18

Figure 1  Typical Application Circuit

Note 1: The maximum output current is set up to 23mA when R EXT = 3.3kΩ. The maximum output current can be set by external resistor, R EXT .
Please refer to the detail information in Page 9.
Note 2: The IC should be placed far away from the mobile antenna in order to prevent the EMI.
| Lumissil Microsystems – www.lumissil.com  |     |     |     |     |     | 1   |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- |
Rev. G, 09/05/2024

IS31FL3218

PIN CONFIGURATION
Package  Pin Configuration (Top View)
QFN-24

SOP-24

PIN DESCRIPTION
| No.  | Pin    | Description               |     |     |
| ---- | ------ | ------------------------- | --- | --- |
| 1    | OUT18  | Output channel for LEDs.  |     |     |
Input terminal used to connect an external resistor. This regulates
| 2   | R_EXT  |     |     |     |
| --- | ------ | --- | --- | --- |
the output current.
| 3                                         | VCC           | Power supply.                       |     |     |
| ----------------------------------------- | ------------- | ----------------------------------- | --- | --- |
| 4                                         | GND           | Ground.                             |     |     |
| 5                                         | SDA           | I2C serial data.                    |     |     |
| 6                                         | SCL           | I2C serial clock.                   |     |     |
| 7~23                                      | OUT1 ~ OUT17  | Output channel for LEDs.            |     |     |
| 24                                        | SDB           | Shutdown the chip when pulled low.  |     |     |
|                                           | Thermal Pad   | Connect to GND.                     |     |     |
| Lumissil Microsystems – www.lumissil.com  |               |                                     |     | 2   |
Rev. G, 09/05/2024

IS31FL3218

ORDERING INFORMATION
Industrial Range: -40°C to +85°C
| Order Part No.       | Package            | QTY        |     |
| -------------------- | ------------------ | ---------- | --- |
| IS31FL3218-QFLS2-TR  | QFN-24, Lead-free  | 2500/Reel  |     |
| IS31FL3218-GRLS2-TR  | SOP-24, Lead-free  | 1000/Reel  |     |
| IS31FL3218-GRLS2     | SOP-24, Lead-free  | 30/Tube    |     |

Copyright © 2024 Lumissil Microsystems. All rights reserved. Lumissil Microsystems reserves the right to make changes to this specification and its
products at any time without notice. Lumissil Microsystems assumes no liability arising out of the application or use of any information, products or
services described herein. Customers are advised to obtain the latest version of this device specification before relying on any published information and
before placing orders for products.
Lumissil Microsystems does not recommend the use of any of its products in life support applications where the failure or malfunction of the product can
reasonably be expected to cause failure of the life support system or to significantly affect its safety or effectiveness. Products are not authorized for use in
such applications unless Lumissil Microsystems receives written assurance to its satisfaction, that:
a.) the risk of injury or damage has been minimized;
b.) the user assume all such risks; and
c.) potential liability of Lumissil Microsystems is adequately protected under the circumstances
| Lumissil Microsystems – www.lumissil.com  |     |     | 3   |
| ----------------------------------------- | --- | --- | --- |
Rev. G, 09/05/2024

IS31FL3218

ABSOLUTE MAXIMUM RATINGS
| Supply voltage, V |     |     |     |     |     |     |     | -0.3V ~ +6.0V |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- |
CC
| Voltage at SCL, SDA, SDB, OUT1 ~ OUT18 |     |     |     |     |     |     |     | -0.3V ~ V | CC +0.3V |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | --- |
| Maximum junction temperature, T        |     |     |     |     |     |     |     | +150°C    |          |     |
JMAX
| Storage temperature range, T   |     |     | STG   |     |     |     |     | -65°C ~ +150°C |     |     |
| ------------------------------ | --- | --- | ----- | --- | --- | --- | --- | -------------- | --- | --- |
| Operating temperature range, T |     |     |       |     |     |     |     | -40°C ~ +85°C  |     |     |
A
Package thermal resistance, junction to ambient (4-layer standard test PCB based on  29°C /W (QFN)
| JESD 51-2A), θ |     |     |     |     |     |     |     | 40.8°C /W (SOP) |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- |
JA
| ESD (HBM)  |     |     |     |     |     |     |     | ±4kV  |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
| ESD (CDM)  |     |     |     |     |     |     |     | ±1kV  |     |     |
Note: Stresses beyond those listed under “Absolute Maximum Ratings” may cause permanent damage to the device. These are stress ratings
only and functional operation of the device at these or any other condition beyond those indicated in the operational sections of the specifications
is not implied. Exposure to absolute maximum rating conditions for extended periods may affect device reliability.

ELECTRICAL CHARACTERISTICS
T = 25°C, V = 2.7V ~ 5.5V, unless otherwise noted. Typical values are T = 25°C, V = 3.6V.
| A       | CC                |            |     |     |     | A          | CC    |       |            |     |
| ------- | ----------------- | ---------- | --- | --- | --- | ---------- | ----- | ----- | ---------- | --- |
| Symbol  |                   | Parameter  |     |     |     | Condition  | Min.  | Typ.  | Max. Unit  |     |
| V       |   Supply voltage  |            |     |     |     |            | 2.7   |       | 5.5        | V   |
CC
|       | Maximum output current of each    |     |     |     | V = 4.2V, V           | = 0.8V  |     |       |       |     |
| ----- | --------------------------------- | --- | --- | --- | --------------------- | ------- | --- | ----- | ----- | --- |
|       |                                   |     |     |     | CC                    | OUT     |     |       |       |     |
| I MAX |                                   |     |     |     |                       |         |     | 38    |   mA  |     |
|       | channel                           |     |     |     | R EXT = 2kΩ (Note 1)  |         |     |       |       |     |
| I     |   Quiescent power supply current  |     |     |     | R = 3.3kΩ             |         |     | 5.25  |   mA  |     |
| CC    |                                   |     |     |     | EXT                   |         |     |       |       |     |
I SD   Shutdown current  V SDB = 0V or software shutdown    3.1    μA
|     |                           |     |     |     | V = 0V or software shutdown,  |     |     |     |     |     |
| --- | ------------------------- | --- | --- | --- | ----------------------------- | --- | --- | --- | --- | --- |
| I   |   Output leakage current  |     |     |     | SDB                           |     |     |     | 1   | μA  |
| OZ  |                           |     |     |     | V = 5V                        |     |     |     |     |     |
OUT
| V EXT |   Output voltage of R-EXT pin  |     |     |     |     |     |     | 1.3  |     | V   |
| ----- | ------------------------------ | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
Logic Electrical Characteristics (SDA, SCL, SDB)
V IL   Logic “0” input voltage  V CC = 2.7V~5.5V      0.4  V
| V      |   Logic “1” input voltage  |     |     |     | V = 2.7V~5.5V  |     | 1.4  |     |     | V   |
| ------ | -------------------------- | --- | --- | --- | -------------- | --- | ---- | --- | --- | --- |
| IH     |                            |     |     |     | CC             |     |      |     |     |     |
| I IL   | Logic “0” input current    |     |     |     | (Note 2)       |     |      | 5   |     | nA  |
| I      |   Logic “1” input current  |     |     |     | (Note 2)       |     |      | 5   |     | nA  |
IH
| Lumissil Microsystems – www.lumissil.com  |     |     |     |     |     |     |     |     |     | 4   |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Rev. G, 09/05/2024

IS31FL3218

DIGITAL INPUT SWITCHING CHARACTERISTICS (NOTE 2)
| Symbol  |                              | Parameter  |     | Condition  | Min.  | Typ.  | Max.  | Unit  |
| ------- | ---------------------------- | ---------- | --- | ---------- | ----- | ----- | ----- | ----- |
|         | f   Serial-Clock frequency   |            |     |            |       |       | 400   | kHz   |
SCL
Bus free time between a STOP and a START
|     | t BUF   |     |     |     | 1.3  |     |     | μs  |
| --- | ------- | --- | --- | --- | ---- | --- | --- | --- |
condition
|     | t   Hold time (repeated) START condition   |     |     |     | 0.6  |     |     | μs  |
| --- | ------------------------------------------ | --- | --- | --- | ---- | --- | --- | --- |
HD, STA
t SU, STA   Repeated START condition setup time     0.6      μs
| t   |   STOP condition setup time   |     |     |     | 0.6  |     |     | μs  |
| --- | ----------------------------- | --- | --- | --- | ---- | --- | --- | --- |
SU, STO
|     | t   Data hold time   |     |     |     |     |     | 0.9  | μs  |
| --- | -------------------- | --- | --- | --- | --- | --- | ---- | --- |
HD, DAT
|     | t SU, DAT   Data setup time   |     |     |     | 100  |     |     | ns  |
| --- | ----------------------------- | --- | --- | --- | ---- | --- | --- | --- |
|     | t   SCL clock low period      |     |     |     | 1.3  |     |     | μs  |
LOW
|     | t HIGH   SCL clock high period   |     |     |     | 0.7  |     |     | μs  |
| --- | -------------------------------- | --- | --- | --- | ---- | --- | --- | --- |
Rise time of both SDA and SCL signals,
|     | t             |     |     | (Note 3)  |     | 20+0.1C |   300  | ns  |
| --- | ------------- | --- | --- | --------- | --- | ------- | ------ | --- |
|     | R receiving   |     |     |           |     |         | b      |     |
Fall time of both SDA and SCL signals,
|     | t F   |     |     | (Note 3)  |     | 20+0.1C | b   300  | ns  |
| --- | ----- | --- | --- | --------- | --- | ------- | -------- | --- |
receiving
| Note 1: The recommended minimum value of R |     |     | is 2kΩ, or it may cause a large current.  |     |     |     |     |     |
| ------------------------------------------ | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- |
EXT
Note 2: Guaranteed by design.
Note 3: C= total capacitance of one bus line in pF. I  ≤ 6mA. t  and t  measured between 0.3 × V  and 0.7 × V .
|     | b   |     | SINK R | F   | CC  |     | CC  |     |
| --- | --- | --- | ------ | --- | --- | --- | --- | --- |

| Lumissil Microsystems – www.lumissil.com  |     |     |     |     |     |     |     | 5   |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Rev. G, 09/05/2024

IS31FL3218
FUNCTIONAL BLOCK DIAGRAM
VCC
I = 7.8/R
S EXT
R_EXT
OUT1~OUT18
R_EXT
Block
SDA
PWM
SCL I2C Comparator
Register
SDB
POR
OSC Counter BG
GND
Lumissil Microsystems – www.lumissil.com 6
Rev. G, 09/05/2024

IS31FL3218
DETAILED DESCRIPTION
I2C INTERFACE Then the master sends an SCL pulse. If the
IS31FL3218 has received the address correctly, then it
The IS31FL3218 uses a serial bus, which conforms to
holds the SDA line low during the SCL pulse. If the SDA
the I2C protocol, to control the chip’s functions with two
line is not low, then the master should send a “STOP”
wires: SCL and SDA. The IS31FL3218’s slave address
signal (discussed later) and abort the transfer.
is “1010 1000”. It only supports write operations.
Following acknowledge of IS31FL3218, the register
The SCL line is uni-directional. The SDA line is
address byte is sent, most significant bit first.
bi-directional (open-collector) with a pull-up resistor
IS31FL3218 must generate another acknowledge
(typically 4.7kΩ). The maximum clock frequency
indicating that the register address has been received.
specified by the I2C standard is 400kHz. In this
discussion, the master is the microcontroller and the Then 8-bit of data byte are sent next, most significant
slave is the IS31FL3218. bit first. Each data bit should be valid while the SCL
level is stable high. After the data byte is sent, the
The timing diagram for the I2C is shown in Figure 2.
IS31FL3218 must generate another acknowledge to
The SDA is latched in on the stable high level of the
indicate that the data was received.
SCL. When there is no interface activity, the SDA line
should be held high. The “STOP” signal ends the transfer. To signal “STOP”,
the SDA signal goes high while the SCL signal is high.
The “START” signal is generated by lowering the SDA
signal while the SCL signal is high. The start signal will ADDRESS AUTO INCREMENT
alert all devices attached to the I2C bus to check the
To write multiple bytes of data into IS31FL3218, load
incoming address against their own chip address.
the address of the data register that the first data byte
The 8-bit chip address is sent next, most significant bit is intended for. During the IS31FL3218 acknowledge of
first. Each address bit must be stable while the SCL receiving the data byte, the internal address pointer will
level is high. increment by one. The next data byte sent to
IS31FL3218 will be placed in the new address, and so
After the last bit of the chip address is sent, the master
on. The auto increment of the address will continue as
checks for the IS31FL3218’s acknowledge. The master
long as data continues to be written to IS31FL3218
releases the SDA line high (through a pull-up resistor).
(Figure 5).
Figure 2 Interface timing
Figure 3 Bit transfer
Lumissil Microsystems – www.lumissil.com 7
Rev. G, 09/05/2024

IS31FL3218

Figure 4  Writing to IS31FL3218 (Typical)

Figure 5  Writing to IS31FL3218 (Automatic Address Increment)

REGISTERS DEFINITIONS
Table 1  Register Function
| Address  | Name               |                             | Function  | R/W  | Table  Default |     |
| -------- | ------------------ | --------------------------- | --------- | ---- | -------------- | --- |
| 00h      | Shutdown Register  | Set software shutdown mode  |           |      | 2              |     |
01h~12h  PWM Register  18 channels PWM duty cycle data register  3
0000
| 13h  | LED Control Register 1  | Channel 1 to 6 enable bit  |     |     | 4   |     |
| ---- | ----------------------- | -------------------------- | --- | --- | --- | --- |
0000
| 14h  | LED Control Register 2  | Channel 7 to 12 enable bit  |     |     | 5   |     |
| ---- | ----------------------- | --------------------------- | --- | --- | --- | --- |
W
| 15h  | LED Control Register 3  | Channel 13 to 18 enable bit  |     |     | 6   |     |
| ---- | ----------------------- | ---------------------------- | --- | --- | --- | --- |
Load PWM Register and LED Control
| 16h  | Update Register  |     |     |     | -  xxxx  |     |
| ---- | ---------------- | --- | --- | --- | -------- | --- |
Register’s data
xxxx
| 17h  | Reset Register  | Reset all registers into default  |     |     | -   |     |
| ---- | --------------- | --------------------------------- | --- | --- | --- | --- |

Table 2  00h  Shutdown Register  Table 3  01h~12h  PWM Register (OUT1~OUT18)
| Bit      | D7:D1     | D0   |          |            |     |     |
| -------- | --------- | ---- | -------- | ---------- | --- | --- |
|          |           |      | Bit      | D7:D0      |     |     |
| Name     | Reserved  | SSD  |          |            |     |     |
|          |           |      | Name     | PWM        |     |     |
| Default  | 000000    | 0    | Default  | 0000 0000  |     |     |
The Shutdown Register sets software shutdown mode
The PWM Registers adjusts LED luminous intensity in
| of IS31FL3218.   |     |     | 256 steps.   |     |     |     |
| ---------------- | --- | --- | ------------ | --- | --- | --- |

The value of a channel’s PWM Register decides the
SSD   Software Shutdown Enable  average output current for each output, OUT1~OUT18.
0    Software shutdown mode  The average output current may be computed using
the Formula (1):
1    Normal operation
|     |     |     | I   | 7   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
D[n]2n
|     |     |     | I  MAX |     |    (1)  |     |
| --- | --- | --- | ------- | --- | ------- | --- |
OUT
256
n0
Where “n” indicates the bit location in the respective
PWM register.
| Lumissil Microsystems – www.lumissil.com  |     |     |     |     |     | 8   |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- |
Rev. G, 09/05/2024

IS31FL3218

| For example: D7:D0 = 10110101,   |     |     | 16h  PWM Update Register  |     |     |     |     |
| -------------------------------- | --- | --- | ------------------------- | --- | --- | --- | --- |
I = I  (20+22+24+25+27)/256
|     | OUT  MAX |     | The data sent to the PWM Registers and the LED  |     |     |     |     |
| --- | -------- | --- | ----------------------------------------------- | --- | --- | --- | --- |
See Formula (2) in Page 10 to calculate the I   Control Registers will be stored in temporary registers.
MAX.
|     |     |     | A write operation of “0000 0000” value to the Update  |     |     |     |     |
| --- | --- | --- | ----------------------------------------------------- | --- | --- | --- | --- |
Table 4  13h  LED Control Register 1  Register is required to update the registers (01h~15h).
(OUT1~OUT6)

| Bit  | D7:D6  | D5:D0  |     |     |     |     |     |
| ---- | ------ | ------ | --- | --- | --- | --- | --- |
17h  Reset Register
| Name  | Reserved  | OUT6:OUT1  |             |                |              |                 |     |
| ----- | --------- | ---------- | ----------- | -------------- | ------------ | --------------- | --- |
|       |           |            | Once  user  | writes  “0000  | 0000”  data  | to  the  Reset  |     |
Default  00  000000  Register, IS31FL3218 will reset all registers to default
value. On initial power-up, the IS31FL3218 registers
Table 5  14h  LED Control Register 2
are reset to their default values for a blank display.
(OUT7~OUT12)

| Bit      | D7:D6     | D5:D0       |     |     |     |     |     |
| -------- | --------- | ----------- | --- | --- | --- | --- | --- |
| Name     | Reserved  | OUT12:OUT7  |     |     |     |     |     |
| Default  | 00        | 000000      |     |     |     |     |     |
Table 6  15h  LED Control Register 3
(OUT13~OUT18)
| Bit      | D7:D6     | D5:D0        |     |     |     |     |     |
| -------- | --------- | ------------ | --- | --- | --- | --- | --- |
| Name     | Reserved  | OUT18:OUT13  |     |     |     |     |     |
| Default  | 00        | 000000       |     |     |     |     |     |
The LED Control Registers store the on or off state of
each column LED.

| OUTx  LED State                           |     |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| 0    LED off                              |     |     |     |     |     |     |     |
| 1    LED on                               |     |     |     |     |     |     |     |
| Lumissil Microsystems – www.lumissil.com  |     |     |     |     |     |     | 9   |
Rev. G, 09/05/2024

IS31FL3218

| APPLICATION INFORMATION  |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

PWM CONTROL
256
| The  PWM  | Registers  | (01h~12h)  | can  | modulate  | LED  |     |     |     |     |     |     |     |
| --------- | ---------- | ---------- | ---- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- |
224
brightness of 18 channels with 256 steps. For example,
if the data in PWM Register is “0000 0100”, then the
192
PWM is the fourth step.
ataD MWP 160
| Writing   | new  data  continuously  |     | to  the    | registers    | can  |     |     |     |     |     |     |     |
| --------- | ------------------------ | --- | ---------- | ------------ | ---- | --- | --- | --- | --- | --- | --- | --- |
| modulate  | the  brightness of       |     | the  LEDs  | to  achieve  | a    |     | 128 |     |     |     |     |     |
breathing effect.
96
R
EXT
64
The maximum output current of OUT1~OUT18 can be
| adjusted by the external resistor, R |     |     |     | , as described in  |     |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
|                                      |     |     | EXT |                    |     |     | 32  |     |     |     |     |     |
Formula (2).
0
|     |     | V   |     |     |     |     | 0   | 4 8 | 12 16 | 20  | 24  | 28 32 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ----- |
EXT
|     | I  | x  |     | (2)  |     |     |     |     |                 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --------------- | --- | --- | --- |
|     | MAX | R   |     |      |     |     |     |     | Intensity Steps |     |     |     |

EXT
Figure 6  Gamma Correction (32 Steps)
| x = 58.5, V |  = 0.8V, V | = 1.3V.  |     |     |     |     |     |     |     |     |     |     |
| ----------- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|             | OUT        | EXT      |     |     |     |     |     |     |     |     |     |     |
Choosing more gamma steps provides for a more
| The recommended minimum value of R |     |     |     | is 2kΩ.  |     |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
EXT  continuous looking breathing effect. This is useful for
|     |     |     |     |     |     | very  | long  | breathing  | cycles.  | The  | recommended  |     |
| --- | --- | --- | --- | --- | --- | ----- | ----- | ---------- | -------- | ---- | ------------ | --- |
GAMMA CORRECTION
configuration is defined by the breath cycle T. When
In order to perform a better visual LED breathing effect
T=1s, choose 32 gamma steps, when T=2s, choose
we recommend using a gamma corrected PWM value  64  gamma  steps.  The  user  must  decide  the  final
to set the LED intensity. This results in a reduced
number of gamma steps not only by the LED itself, but
| number  | of  steps  for  | the  LED  | intensity  | setting,  | but  |     |     |     |     |     |     |     |
| ------- | --------------- | --------- | ---------- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- |
also based on the visual performance of the finished
| causes the change in intensity to appear more linear to  |     |     |     |     |     | product.  |     |     |     |     |     |     |
| -------------------------------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
the human eye.
Table 8  64 Gamma Steps With 256 PWM Steps
| Gamma  | correction,  | also  | known  | as  | gamma  |      |      |      |             |       |      |      |
| ------ | ------------ | ----- | ------ | --- | ------ | ---- | ---- | ---- | ----------- | ----- | ---- | ---- |
|        |              |       |        |     |        | C(0) | C(1) | C(2) | C(3)  C(4)  | C(5)  | C(6) | C(7) |
compression or encoding, is used to encode linear
luminance to match the non-linear characteristics of  0  1  2  3   4   5   6  7
| display.    | Since  the     | IS31FL3218  | can  | modulate   | the    |      |      |         |                         |     |      |         |
| ----------- | -------------- | ----------- | ---- | ---------- | ------ | ---- | ---- | ------- | ----------------------- | --- | ---- | ------- |
|             |                |             |      |            |        | C(8) | C(9) | C(10)   | C(11) C(12) C(13) C(14) |     |      | C(15)   |
| brightness  | of  the  LEDs  | with        | 256  | steps,  a  | gamma  |      |      |         |                         |     |      |         |
|             |                |             |      |            |        |      | 8    | 10  12  | 14   16                 |     | 18   | 20  22  |
correction function can be applied when computing
each subsequent LED intensity setting such that the  C(16) C(17) C(18) C(19) C(20) C(21) C(22) C(23)
changes  in  brightness  matches  the  human  eye's  24  26  29  32   35   38   41  44
brightness curve.
|     |     |     |     |     |     | C(24) | C(25) | C(26) | C(27) C(28) C(29) C(30) |     |     | C(31) |
| --- | --- | --- | --- | --- | --- | ----- | ----- | ----- | ----------------------- | --- | --- | ----- |
Table 7  32 Gamma Steps With 256 PWM Steps
|     |     |     |     |     |     |     | 47  | 50  53  | 57   61   |     | 65   | 69  73  |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | ---- | ------- |
C(0)  C(1)  C(2)  C(3)  C(4)  C(5)  C(6) C(7) C(32) C(33) C(34) C(35) C(36) C(37) C(38) C(39)
| 0   | 1   2   | 4   | 6   10   | 13  | 18  |     |     |         |           |     |           |      |
| --- | ------- | --- | -------- | --- | --- | --- | --- | ------- | --------- | --- | --------- | ---- |
|     |         |     |          |     |     |     | 77  | 81  85  | 89   94   |     | 99   104  | 109  |
C(8)  C(9)  C(10) C(11) C(12) C(13) C(14) C(15) C(40) C(41) C(42) C(43) C(44) C(45) C(46) C(47)
22   28   33   39   46   53   61  69  114  119  124  129   134   140   146  152
C(16) C(17) C(18) C(19) C(20) C(21) C(22) C(23) C(48) C(49) C(50) C(51) C(52) C(53) C(54) C(55)
78   86   96   106   116   126   138  149  158  164  170  176   182   188   195  202
| C(24) C(25) C(26) C(27) C(28) C(29) C(30) |     |     |     |     | C(31) |       |       |       |                         |     |     |       |
| ----------------------------------------- | --- | --- | --- | --- | ----- | ----- | ----- | ----- | ----------------------- | --- | --- | ----- |
|                                           |     |     |     |     |       | C(56) | C(57) | C(58) | C(59) C(60) C(61) C(62) |     |     | C(63) |
161   173   186   199   212   226   240  255  209  216  223  230   237   244   251  255
| Lumissil Microsystems – www.lumissil.com  |     |     |     |     |     |     |     |     |     |     |     | 10  |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Rev. G, 09/05/2024

IS31FL3218
256
224
192
160
128
96
64
32
0
0 8 16 24 32 40 48 56 64
Lumissil Microsystems – www.lumissil.com 11
Rev. G, 09/05/2024
ataD
MWP
SHUTDOWN MODE
Shutdown mode can either be used as a means of
reducing power consumption or generating a flashing
display (repeatedly entering and leaving shutdown
mode). During shutdown mode all registers retain their
data.
Software Shutdown
By setting SSD bit of the Configuration Register (00h)
to “0”, the IS31FL3218 will operate in software
shutdown mode, wherein they consume only 3.1μA
(Typ.) current. When the IS31FL3218 is in software
shutdown mode, all current sources are switched off.
Hardware Shutdown
Intensity Steps The chip enters hardware shutdown mode when the
SDB pin is pulled low.
Figure 7 Gamma Correction (64 Steps)
Note, the data of 32 gamma steps is the standard value and the data
of 64 gamma steps is the recommended value.

IS31FL3218
CLASSIFICATION REFLOW PROFILES
Profile Feature Pb-Free Assembly
Preheat & Soak
150°C
Temperature min (Tsmin)
200°C
Temperature max (Tsmax)
60-120 seconds
Time (Tsmin to Tsmax) (ts)
Average ramp-up rate (Tsmax to Tp) 3°C/second max.
Liquidous temperature (TL) 217°C
Time at liquidous (tL) 60-150 seconds
Peak package body temperature (Tp)* Max 260°C
Time (tp)** within 5°C of the specified
Max 30 seconds
classification temperature (Tc)
Average ramp-down rate (Tp to Tsmax) 6°C/second max.
Time 25°C to peak temperature 8 minutes max.
Figure 8 Classification profile
Lumissil Microsystems – www.lumissil.com 12
Rev. G, 09/05/2024

IS31FL3218
PACKAGE INFORMATION
QFN-24
Lumissil Microsystems – www.lumissil.com 13
Rev. G, 09/05/2024

IS31FL3218
SOP-24
Lumissil Microsystems – www.lumissil.com 14
Rev. G, 09/05/2024

IS31FL3218
RECOMMENDED LAND PATTERN
QFN-24
SOP-24
Note:
1. Land pattern complies to IPC-7351.
2. All dimensions in MM.
3. This document (including dimensions, notes & specs) is a recommendation based on typical circuit board manufacturing parameters. Since
land pattern design depends on many factors unknown (eg. user’s board manufacturing specs), user must determine suitability for use.
Lumissil Microsystems – www.lumissil.com 15
Rev. G, 09/05/2024

IS31FL3218

REVISION HISTORY
| Revision            |     | Detail Information  | Data        |     |
| ------------------- | --- | ------------------- | ----------- | --- |
| A  Initial release  |     |                     | 2012.01.09  |     |
1. Page 3 ORDERING INFORMATION, SOP-24 QTY changes to 30/Tube
| B   |     |     | 2012.04.08  |     |
| --- | --- | --- | ----------- | --- |
2. Remove TAPE AND REEL INFORMATION
C  Absolute Maximum Ratings: voltage at OUTX change from 5V to -0.3V~VCC+0.3V  2014.09.04
1. Update POD
2. Update ESD (HBM)
| D  3. Add land pattern  |     |     | 2016.09.02  |     |
| ----------------------- | --- | --- | ----------- | --- |
4. Add θ
JA
5. Add ESD(CDM)
| E  Update θ | JA for QFN package  |     | 2017.06.06  |     |
| ----------- | ------------------- | --- | ----------- | --- |
1. Add 1000/Reel packing for SOP-24
| F   |     |     | 2020.10.10  |     |
| --- | --- | --- | ----------- | --- |
2. Update RJA and land pattern
1.Update to new Lumissil logo
| G   |     |     | 2024.09.05  |     |
| --- | --- | --- | ----------- | --- |
2.Update POD, add RoHS

| Lumissil Microsystems – www.lumissil.com  |     |     |     | 16  |
| ----------------------------------------- | --- | --- | --- | --- |
Rev. G, 09/05/2024