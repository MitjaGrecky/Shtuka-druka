OPA165x Ultra-Low-Noise, Low-Distortion, FET-Input,
Burr-Brown™ Audio Operational Amplifiers
1 Features 3 Description
• Ultra-low noise: The OPA1655 and OPA1656 (OPA165x) are Burr-
– Voltage noise: 2.9 nV/?Hz at 10 kHz Brown™ op amps designed specifically for audio
– Current noise: 6 fA/?Hz at 1 kHz and industrial applications, where maintaining signal
• Low distortion: fidelity is crucial. The FET-input architecture achieves
– 0.000029% (–131 dB) at 1 kHz a low 2.9?nV/?Hz voltage noise density and 6?fA/?Hz
– 0.000035% (–129 dB) at 20 kHz current noise density, allowing for very-low noise
• High open-loop gain: 150 dB performance in a wide variety of circuits. The high
• High output current: 100 mA bandwidth and high open-loop-gain design of the
• Low input bias current: 10 pA OPA165x delivers a low distortion of 0.000035%
• Slew rate: 24 V/?s (–129 dB) at 20 kHz, and improves audio signal
• Gain bandwidth product: 53 MHz fidelity across the full audio bandwidth. These devices
• Rail-to-rail output also feature excellent output current drive capability,
• Wide supply range: offering rail-to-rail output swing to within 250 mV of
±2.25 V to ±18 V or 4.5 V to 36 V the power supplies with a 2?k? load, and can deliver
• Quiescent current: 3.9 mA per channel 100 mA of output current.
2 Applications The OPA165x operate over a very wide supply range
of ±2.25 V to ±18 V or (4.5 V to 36 V) on 3.9 mA
• Professional microphones and wireless systems of supply current to accommodate the power-supply
• Professional audio mixer/control surface constraints of many types of audio products. The
• Guitar amplifier and other music instrument temperature range is specified from –40°C to +125°C.
amplifier
• A/V receiver Device Information
• Bookshelf stereo system PART NUMBER CHANNEL PACKAGE(1)
• Professional audio amplifier D (SOIC, 8)
OPA1655 Single
• DJ equipment
DBV (SOT-23, 5)
• Turntable
OPA1656 Dual D (SOIC, (8)
• Special function module
(1) For all available packages, see the package option
addendum at the end of the data sheet.
Pad
Bass
–
Input + – Output
OPA165x
+
OPA165x
Treble
Active Baxandall Tone Control
Frequency (Hz)
)zH—/Vn(
ytisneD
esioN
egatloV
OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
100
10
1
10 100 1k 10k 100k 1M 10M
C020
Ultra-Low Input Voltage Noise
An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,
intellectual property matters and other important disclaimers. PRODUCTION DATA.

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
Table of Contents
1 Features............................................................................1 7.4 Device Functional Modes..........................................18
2 Applications.....................................................................1 8 Application and Implementation..................................19
3 Description.......................................................................1 8.1 Application Information.............................................19
4 Revision History..............................................................2 8.2 Typical Applications..................................................20
5 Pin Configuration and Functions...................................3 8.3 Power Supply Recommendations.............................27
6 Specifications..................................................................4 8.4 Layout.......................................................................27
6.1 Absolute Maximum Ratings........................................4 9 Device and Documentation Support............................29
6.2 ESD Ratings...............................................................4 9.1 Device Support.........................................................29
6.3 Recommended Operating Conditions.........................4 9.2 Documentation Support............................................30
6.4 Thermal Information: OPA1655..................................5 9.3 Receiving Notification of Documentation Updates....30
6.5 Thermal Information: OPA1656..................................5 9.4 Support Resources...................................................30
6.6 Electrical Characteristics.............................................6 9.5 Trademarks...............................................................30
6.7 Typical Characteristics................................................8 9.6 Electrostatic Discharge Caution................................30
7 Detailed Description......................................................15 9.7 Glossary....................................................................30
7.1 Overview...................................................................15 10 Mechanical, Packaging, and Orderable
7.2 Functional Block Diagram.........................................15 Information....................................................................30
7.3 Feature Description...................................................15
4 Revision History
NOTE: Page numbers for previous revisions may differ from page numbers in the current version.
Changes from Revision B (December 2021) to Revision C (September 2022) Page
• Changed OPA1655 DBV (SOT-23, 5) package from preview to production data (active)..................................1
Changes from Revision A (July 2019) to Revision B (December 2021) Page
• Added OPA1655 production data (active) device and associated content.........................................................1
Changes from Revision * (March 2019) to Revision A (July 2019) Page
• Changed device status from advanced information (preview) to production data (active).................................1
2 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| www.ti.com |     |     |     |     | SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |
| ---------- | --- | --- | --- | --- | ---------------------------------------------- | --- |
5 Pin Configuration and Functions
|     |     |     |     |     | OUT | 1 5 V+ |
| --- | --- | --- | --- | --- | --- | ------ |
|     | NC  | 1   | 8   | NC  |     |        |
|     |     |     |     |     | V±  | 2      |
|     | –IN | 2 – | 7   | V+  |     |        |
+ ±
|     |     |     |     |     | +IN | 3 4 ±IN |
| --- | --- | --- | --- | --- | --- | ------- |
|     | +IN | 3 + | 6   | OUT |     |         |
|     | V–  | 4   | 5   | NC  |     |         |
Not to scale
Figure 5-2. OPA1655 DBV (5-Pin SOT-23) Package,
|     |     | Not to scale |     |     |     | Top View |
| --- | --- | ------------ | --- | --- | --- | -------- |
Figure 5-1. OPA1655 D (8-Pin SOIC) Package,
Top View
Pin Functions: OPA1655
PIN
|     |     | NO. |     | TYPE |     | DESCRIPTION |
| --- | --- | --- | --- | ---- | --- | ----------- |
NAME
|     |     | D (SOIC) DBV (SOT-23) |       |                                       |          |     |
| --- | --- | --------------------- | ----- | ------------------------------------- | -------- | --- |
| –IN |     | 2                     | 4     | Input Inverting input                 |          |     |
| +IN |     | 3                     | 3     | Input Noninverting input              |          |     |
| OUT |     | 6                     | 1     | Output Output                         |          |     |
| V–  |     | 4                     | 2     | Power Negative (lowest) power supply  |          |     |
| V+  |     | 7                     | 5     | Power Positive (highest) power supply |          |     |
|     |     |                       | OUT A | 1                                     | 8  V+    |     |
|     |     |                       | ±IN A | 2                                     | 7  OUT B |     |
|     |     |                       | +IN A | 3                                     | 6  ±IN B |     |
|     |     |                       | V±    | 4                                     | 5  +IN B |     |
Not to scale
Figure 5-3. OPA1656 D (8-Pin SOIC) Package, Top View
Pin Functions: OPA1656
PIN
|       |     | TYPE     |                                 |     | DESCRIPTION |     |
| ----- | --- | -------- | ------------------------------- | --- | ----------- | --- |
| NAME  |     | NO.      |                                 |     |             |     |
| –IN A |     | 2 Input  | Inverting input, channel A      |     |             |     |
| +IN A |     | 3 Input  | Noninverting input, channel A   |     |             |     |
| –IN B |     | 6 Input  | Inverting input, channel B      |     |             |     |
| +IN B |     | 5 Input  | Noninverting input, channel B   |     |             |     |
| OUT A |     | 1 Output | Output, channel A               |     |             |     |
| OUT B |     | 7 Output | Output, channel B               |     |             |     |
| V–    |     | 4 Power  | Negative (lowest) power supply  |     |             |     |
| V+    |     | 8 Power  | Positive (highest) power supply |     |             |     |
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 3
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | ---------- |
6 Specifications
6.1 Absolute Maximum Ratings
over operating free-air temperature range (unless otherwise noted)(1)
|         |                                           |                | MIN        | MAX        | UNIT |
| ------- | ----------------------------------------- | -------------- | ---------- | ---------- | ---- |
|         | Supply voltage, V                         |  = (V+) – (V–) |            | 40         | V    |
| Voltage |                                           | S              |            |            |      |
|         | Input                                     |                | (V–) – 0.5 | (V+) + 0.5 | V    |
|         | Input (all pins except power-supply pins) |                | –10        | 10         | mA   |
Current
|     | Output short-circuit(2) |     | Continuous |     |     |
| --- | ----------------------- | --- | ---------- | --- | --- |
|     | Operating, T            |     | –55        | 125 | °C  |
A
| Temperature | Junction, T |     |     | 150 | °C  |
| ----------- | ----------- | --- | --- | --- | --- |
J
|     | Storage, T stg |     | –65 | 150 | °C  |
| --- | -------------- | --- | --- | --- | --- |
(1) Operation outside the Absolute Maximum Ratings may cause permanent device damage. Absolute Maximum Ratings do not imply
functional operation of the device at these or any other conditions beyond those listed under Recommended Operating Conditions.
If used outside the Recommended Operating Conditions but within the Absolute Maximum Ratings, the device may not be fully
functional, and this may affect device reliability, functionality, performance, and shorten the device lifetime.
(2) Short-circuit to V  / 2 (groundinsymmetrical dual-supply setups), one amplifier per package.
S
6.2 ESD Ratings
|     |     |     |     | VALUE | UNIT |
| --- | --- | --- | --- | ----- | ---- |
Human-body model (HBM), per ANSI/ESDA/JEDEC JS-001(1)
±2000
| V   | Electrostatic discharge |     |     |     | V   |
| --- | ----------------------- | --- | --- | --- | --- |
(ESD) Charged-device model (CDM), per JEDEC specification JESD22-C101(2) ±1000
(1) JEDEC document JEP155 states that 500-V HBM allowssafemanufacturing with a standard ESD control process.
(2) JEDEC document JEP157 states that 250-V CDM allowssafemanufacturing with a standard ESD control process.
6.3 Recommended Operating Conditions
over operating free-air temperature range (unless otherwise noted)
|     |                       |               | MIN   | NOM | MAX UNIT |
| --- | --------------------- | ------------- | ----- | --- | -------- |
|     |                       | Single supply | 4.5   |     | 36       |
| V   | Supply voltage        |               |       |     | V        |
| S   |                       | Dual supply   | ±2.25 |     | ±18      |
| T   | Operating temperature |               | –40   |     | 125 °C   |
A
4 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| www.ti.com |     | SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |
| ---------- | --- | ---------------------------------------------- | --- | --- | --- |
6.4 Thermal Information: OPA1655
OPA1655
|     |     | THERMAL METRIC(1) | D (SOIC) | DBV (SOT23) | UNIT |
| --- | --- | ----------------- | -------- | ----------- | ---- |
|     |     |                   | 8 PINS   | 5 PINS      |      |
R ?JA Junction-to-ambient thermal resistance 120.9 143.4 °C/W
R ?JC(top) Junction-to-case (top) thermal resistance 58.9 68.4 °C/W
| R   | Junction-to-board thermal resistance |     | 65.1 | 39.2 | °C/W |
| --- | ------------------------------------ | --- | ---- | ---- | ---- |
?JB
| ?   | Junction-to-top characterization parameter |     | 13.5 | 20.4 | °C/W |
| --- | ------------------------------------------ | --- | ---- | ---- | ---- |
JT
? Junction-to-board characterization parameter 64.2 39.0 °C/W
JB
R ?JC(bot) Junction-to-case (bottom) thermal resistance N/A N/A °C/W
(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application
report.
6.5 Thermal Information: OPA1656
OPA1656
|     |     | THERMAL METRIC(1) | D (SOIC) |     | UNIT |
| --- | --- | ----------------- | -------- | --- | ---- |
8 PINS
| R   | Junction-to-ambient thermal resistance |     |     | 119.9 | °C/W |
| --- | -------------------------------------- | --- | --- | ----- | ---- |
?JA
| R   | Junction-to-case (top) thermal resistance |     |     | 51.8 | °C/W |
| --- | ----------------------------------------- | --- | --- | ---- | ---- |
?JC(top)
| R   | Junction-to-board thermal resistance |     |     | 65.4 | °C/W |
| --- | ------------------------------------ | --- | --- | ---- | ---- |
?JB
| ? JT | Junction-to-top characterization parameter   |     |     | 10.0 | °C/W |
| ---- | -------------------------------------------- | --- | --- | ---- | ---- |
| ? JB | Junction-to-board characterization parameter |     |     | 64.2 | °C/W |
| R    | Junction-to-case (bottom) thermal resistance |     |     | N/A  | °C/W |
?JC(bot)
(1) For more information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application
report.
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 5
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ---------- |
6.6 Electrical Characteristics
at T  = 25°C, V  = ±18 V, R  = 2 k?, and V  = V  = V /2 (unless otherwise noted)
| A   | S         | L   | CM  | OUT S           |     |     |     |      |
| --- | --------- | --- | --- | --------------- | --- | --- | --- | ---- |
|     | PARAMETER |     |     | TEST CONDITIONS | MIN | TYP | MAX | UNIT |
AUDIO PERFORMANCE
|       |                                   |     | G = 1, RL = 600 ?, VO = 3.5 VRMS, f = 1 kHz,  |                         |     | 0.000029% |     |     |
| ----- | --------------------------------- | --- | --------------------------------------------- | ----------------------- | --- | --------- | --- | --- |
|       |                                   |     | 80-kHz measurement bandwidth                  |                         |     | –131      |     | dB  |
|       |                                   |     | G = 1, RL = 600 ?, VO = 3.5 VRMS, f = 20 kHz, |                         |     | 0.0001%   |     |     |
|       |                                   |     | 80-kHz measurement bandwidth                  |                         |     | –120      |     | dB  |
| THD+N | Total harmonic distortion + noise |     |                                               |                         |     |           |     |     |
|       |                                   |     | G = 1, RL = 2 k?, VO = 3.5 VRMS, f = 1 kHz,   |                         |     | 0.000029% |     |     |
|       |                                   |     | 80-kHz measurement bandwidth                  |                         |     | –131      |     | dB  |
|       |                                   |     | G = 1, RL = 2 k?, VO = 3.5 VRMS, f = 20 kHz,  |                         |     | 0.000035% |     |     |
|       |                                   |     | 80-kHz measurement bandwidth                  |                         |     | –129      |     | dB  |
|       |                                   |     |                                               | SMPTE/DIN two-tone, 4:1 |     | 0.000018% |     |     |
|       |                                   |     |                                               | (60 Hz and 7 kHz)       |     | –135      |     | dB  |
G = 1
| IMD | Intermodulation distortion |     |               |                |     |           |     |     |
| --- | -------------------------- | --- | ------------- | -------------- | --- | --------- | --- | --- |
|     |                            |     | VO = 3.5 VRMS | CCIF twin-tone |     | 0.000020% |     |     |
(19 kHz and 20 kHz)
|     |     |     |     |     |     | –134 |     | dB  |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- |
FREQUENCY RESPONSE
|     | Gain-bandwidth product |     | G = 100 |     |     | 53  |     | MHz |
| --- | ---------------------- | --- | ------- | --- | --- | --- | --- | --- |
GBW
|     | Unity gain bandwidth    |     | G = 1                    |     |     | 20   |     | MHz  |
| --- | ----------------------- | --- | ------------------------ | --- | --- | ---- | --- | ---- |
| SR  | Slew rate               |     | G = –1, 10-V step        |     |     | 24   |     | V/µs |
|     | Full-power bandwidth(1) |     | VO = 1 VP                |     |     | 3.8  |     | MHz  |
|     | Overload recovery time  |     | G = –10                  |     |     | 100  |     | ns   |
|     | Channel separation      |     | f = 1 kHz                |     |     | –135 |     | dB   |
|     | Settling time           |     | 0.01%, G = –1, 10-V step |     |     | 800  |     | ns   |
NOISE
|     |     |     | f = 20 Hz to 20 kHz |     |     | 0.53 |     | µVRMS |
| --- | --- | --- | ------------------- | --- | --- | ---- | --- | ----- |
Input voltage noise
|     |                             |     | f = 0.1 Hz to 10 Hz |     |     | 1.9  |     | µVPP   |
| --- | --------------------------- | --- | ------------------- | --- | --- | ---- | --- | ------ |
|     |                             |     | f = 100 Hz          |     |     | 11.8 |     | nV/?Hz |
| en  | Input voltage noise density |     | f = 1 kHz           |     |     | 4.3  |     |        |
nV/?Hz
|     |                             |     | f = 10 kHz |     |     | 2.9 |     |        |
| --- | --------------------------- | --- | ---------- | --- | --- | --- | --- | ------ |
| in  | Input current noise density |     | f = 1 kHz  |     |     | 6   |     | fA/?Hz |
OFFSET VOLTAGE
| VOS     | Input offset voltage          |     | VS = ±2.25 V to ±18 V |                        |     | ±0.5 | ±1  | mV    |
| ------- | ----------------------------- | --- | --------------------- | ---------------------- | --- | ---- | --- | ----- |
|         |                               |     | V   =   ± 2 .2        | 5   V  t o   ± 1 8  V  |     |      |     |       |
| dVOS/dT | Input offset voltage drift(2) |     | S                     |                        |     | 0.3  | 2   | µV/°C |
|         |                               |     | T   =   – 4 0         | ° C   to   + 1 2 5 ° C |     |      |     |       |
A
PSRR Power-supply rejection ratio VS = ±2.25 V to ±18 V 0.3 5 µV/V
INPUT BIAS CURRENT
|     |                       |     |           | OPA1655 |     | ±10 |     |     |
| --- | --------------------- | --- | --------- | ------- | --- | --- | --- | --- |
| IB  | Input bias current(3) |     | VCM = 0 V |         |     |     |     | pA  |
|     |                       |     |           | OPA1656 |     | ±10 | ±20 |     |
|     |                       |     |           | OPA1655 |     | ±10 |     |     |
| IOS | Input offset current  |     | VCM = 0 V |         |     |     |     | pA  |
|     |                       |     |           | OPA1656 |     | ±10 | ±20 |     |
INPUT VOLTAGE RANGE
| VCM | Common-mode voltage range |     |     |     | (V–) |     | (V+) – 2.25 | V   |
| --- | ------------------------- | --- | --- | --- | ---- | --- | ----------- | --- |
CMRR Common-mode rejection ratio (V–) ? VCM ? (V+) – 2.25 106 120 dB
INPUT IMPEDANCE
|     | Differential |     |     |     |     | 100 || 9.1 |     | M? || pF    |
| --- | ------------ | --- | --- | --- | --- | ---------- | --- | ----------- |
|     | Common-mode  |     |     |     |     | 6 || 1.9   |     | 1012? || pF |
OPEN-LOOP GAIN
(V–) + 1.3 V ? VO ? (V+) – 1.3 V
|     |     |     |     |     | 134 | 150 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
RL = 600 ?
| AOL | Open-loop voltage gain |     |     |     |     |     |     | dB  |
| --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
(V–) + 0.5 V ? VO ? (V+) – 0.5 V
|     |     |     |     |     | 134 | 154 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
RL = 2 k?
6 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| www.ti.com |     |     |     |     | SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |
| ---------- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- |
6.6 Electrical Characteristics (continued)
at T  = 25°C, V  = ±18 V, R  = 2 k?, and V  = V  = V /2 (unless otherwise noted)
| A   | S         | L   | CM  | OUT S           |     |         |      |
| --- | --------- | --- | --- | --------------- | --- | ------- | ---- |
|     | PARAMETER |     |     | TEST CONDITIONS | MIN | TYP MAX | UNIT |
OUTPUT
| VO  | Voltage output             |     |           |     | (V–) + 0.25 | (V+) – 0.25 | V   |
| --- | -------------------------- | --- | --------- | --- | ----------- | ----------- | --- |
| ZO  | Open-loop output impedance |     | f = 1 MHz |     |             | 26          | ?   |
| ISC | Short-circuit current(4)   |     |           |     |             | ±100        | mA  |
| CL  | Capacitive load drive      |     |           |     |             | 100         | pF  |
POWER SUPPLY
|                                         |                                 |     | IO = 0 A, VS = ±2.25 V to ±18 V   |     |     | 3.9 4.6 |     |
| --------------------------------------- | ------------------------------- | --- | --------------------------------- | --- | --- | ------- | --- |
| IQ                                      | Quiescent current (per channel) |     |                                   |     |     |         | mA  |
|                                         |                                 |     | IO = 0 A, TA = –40°C to +125°C(2) |     |     | 5.0     |     |
| (1) Full-power bandwidth = SR / (2? × V |                                 |     | P ), where SR = slew rate.        |     |     |         |     |
(2) Specified by design and characterization.
(3) Input bias current test conditions can vary from nominal ambient conditions as a result of junction temperature differences.
(4) One channel at a time.
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 7
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- |
6.7 Typical Characteristics
| at T |  = 25°C, V |  = ±15 V, R |  = 2 k?, and V |     |  = V | /2 (unless otherwise noted) |     |     |     |     |
| ---- | ---------- | ----------- | -------------- | --- | ---- | --------------------------- | --- | --- | --- | --- |
| A    |            | S           | L              |     | CM S |                             |     |     |     |     |
100
)vid/Vn 005( esioN egatloV derrefeR tupnI
)zH—/Vn( ytisneD esioN egatloV
10
1
|     | 10  | 100 | 1k 10k | 100k | 1M  | 10M |     | Time (1 s/div) |     |     |
| --- | --- | --- | ------ | ---- | --- | --- | --- | -------------- | --- | --- |
Frequency (Hz)
|     |     |     |     |     |     | C020 |     |     |     | D029 |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ---- |

Figure 6-1. Input Voltage Noise Density vs Frequency
Figure 6-2. 0.1-Hz to 10-Hz Noise
|     | 1000 |                            |     |     |     |     | 50  |     |     |          |
| --- | ---- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | -------- |
|     |      | Voltage Noise Contribution |     |     |     |     |     |     |     | Vs=r18 V |
500
|     |     | Resistor Noise Contribution |     |     |     |     |     |     |     | Vs=r15 V   |
| --- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | ---------- |
|     | 200 | Current Noise Contribution  |     |     |     |     |     |     |     | Vs=r2.25 V |
40
|     | 100 | Total Noise Contribution |     |     |     |     |     |     |     |     |
| --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
)PV( egatloV tuptuO
50
)zH—/Vn( esioN
30
20
10
|     | 5   |     |     |     |     |     | 20  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
1
10
0.5
0.2
|     | 0.1 |     |                       |     |      |      | 0      |                |     |        |
| --- | --- | --- | --------------------- | --- | ---- | ---- | ------ | -------------- | --- | ------ |
|     |     |     |                       |     |      |      | 100 1k | 10k 100k       |     | 1M 10M |
|     | 10  | 100 | 1k                    | 10k | 100k | 1M   |        |                |     |        |
|     |     |     | Source Resistance (:) |     |      |      |        | Frequency (Hz) |     |        |
|     |     |     |                       |     |      | D120 |        |                |     | D113   |

Figure 6-4. Maximum Output Voltage vs Frequency
Figure 6-3. Voltage Noise vs Source Resistance
| 180 |     |     |     |     |     | 180 | 60  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
G = (cid:14)1
Gain
|     |     |     |     |     | Phase |     |     |     |     | G= (cid:16)1  |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | ------------- |
| 150 |     |     |     |     |       | 150 |     |     |     | G= (cid:14)10 |
G= +100
40
| 120       |     |     |     |     |     | 120          |           |     |     |     |
| --------- | --- | --- | --- | --- | --- | ------------ | --------- | --- | --- | --- |
| )Bd( niaG | 90  |     |     |     |     | 90 Phase (q) | )Bd( niaG |     |     |     |
20
|     | 60  |     |     |     |     | 60  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 30  |     |     |     |     | 30  |     |     |     |     |
0
|     | 0    |      |                |      |     | 0    |        |                |     |      |
| --- | ---- | ---- | -------------- | ---- | --- | ---- | ------ | -------------- | --- | ---- |
|     | -30  |      |                |      |     | -30  | -20    |                |     |      |
|     | 100m | 1 10 | 100 1k 10k     | 100k | 1M  | 10M  | 100 1k | 10k 100k       | 1M  | 10M  |
|     |      |      | Frequency (Hz) |      |     |      |        | Frequency (Hz) |     |      |
|     |      |      |                |      |     | D104 |        |                |     | D106 |
|     |      |      | C L  = 10 pF   |      |     |      |        |   C L  = 10 pF |     |      |
Figure 6-5. Open-Loop Gain and Phase vs Frequency Figure 6-6. Closed-Loop Gain vs Frequency
8 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| www.ti.com |     |     |     |     |     |     |     |     | SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- |
6.7 Typical Characteristics (continued)
| at T |  = 25°C, V |  = ±15 V, R |  = 2 k?, and V |     |                                  |  = V | /2 (unless otherwise noted)                   |     |     |     |     |                                  |     |
| ---- | ---------- | ----------- | -------------- | --- | -------------------------------- | ---- | --------------------------------------------- | --- | --- | --- | --- | -------------------------------- | --- |
|      | A          | S           | L              |     |                                  | CM   | S                                             |     |     |     |     |                                  |     |
|      | 0.01       |             |                |     |                                  |      | -80                                           |     | 1   |     |     |                                  | -40 |
|      |            |             |                |     | G = (cid:16)1, 600(cid:16): Load |      | )Bd( esioN (cid:14) noitrotsiD cinomraH latoT |     |     |     |     | G = (cid:16)1, 600(cid:16): Load |     |
)%( esioN (cid:14) noitrotsiD cinomraH latoT )%( esioN (cid:14) noitrotsiD cinomraH latoT )Bd( esioN + noitrotsiD cinomraH latoT
|     |       |     |     |     | G = (cid:16)1, 2k(cid:16): Load  |     |      |     |     |     |     | G = (cid:16)1, 2k(cid:16): Load  |     |
| --- | ----- | --- | --- | --- | -------------------------------- | --- | ---- | --- | --- | --- | --- | -------------------------------- | --- |
|     |       |     |     |     | G = (cid:16)1, 10k(cid:16): Load |     |      |     |     |     |     | G = (cid:16)1, 10k(cid:16): Load |     |
|     |       |     |     |     |                                  |     |      |     | 0.1 |     |     |                                  | -60 |
|     |       |     |     |     | G = (cid:14)1, 600(cid:16): Load |     |      |     |     |     |     | G = (cid:14)1, 600(cid:16): Load |     |
|     |       |     |     |     | G = (cid:14)1, 2k(cid:16): Load  |     |      |     |     |     |     | G = (cid:14)1, 2k(cid:16): Load  |     |
|     | 0.001 |     |     |     |                                  |     | -100 |     |     |     |     | G = (cid:14)1, 10k(cid:16): Load |     |
G = (cid:14)1, 10k(cid:16): Load
|     |         |        |                |     |                    |     |      |        | 0.01      |                         |     |                    | -80  |
| --- | ------- | ------ | -------------- | --- | ------------------ | --- | ---- | ------ | --------- | ----------------------- | --- | ------------------ | ---- |
|     |         |        |                |     |                    |     |      | 0.001  |           |                         |     |                    | -100 |
|     | 0.0001  |        |                |     |                    |     | -120 |        |           |                         |     |                    |      |
|     |         |        |                |     |                    |     |      | 0.0001 |           |                         |     |                    | -120 |
|     | 0.00001 |        |                |     |                    |     | -140 | 1E-5   |           |                         |     |                    | -140 |
|     |         | 20     | 100            | 1k  |                    | 10k | 20k  |        | 100m      |                         | 1   |                    | 10   |
|     |         |        | Frequency (Hz) |     |                    |     | D109 |        |           | Output Amplitude (VRMS) |     |                    | D110 |
|     | V       |  = 3 V |                |     | Bandwidth = 80 kHz |     |      |        | f = 1 kHz |                         |     | Bandwidth = 80 kHz |      |
|     |         | OUT    | RMS            |     |                    |     |      |        |           |                         |     |                    |      |
Figure 6-7. THD+N Ratio vs Frequency Figure 6-8. THD+N Ratio vs Output Amplitude
|     | 0.001 |     |     |     |     |     | -100 | 00..000055 |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | ---- | ---------- | --- | --- | --- | --- | --- |
G = (cid:16)1, VIN = 1 VPP (0.354 VRMS)
0.0005 G = (cid:16)1, HD2 )%( esioN (cid:14) noitrotsiD cinomraH latoT )Bd( esioN + noitrotsiD cinomraH latoT
G = (cid:16)1, HD3 0.003 G = (cid:16)1, VIN = 5 VPP (1.768 VRMS)
|                     | 0.0002 | G = (cid:16)1, HD4 |     |     |     |     |                | 0.002  |     |     |                                  |     |      |
| ------------------- | ------ | ------------------ | --- | --- | --- | --- | -------------- | ------ | --- | --- | -------------------------------- | --- | ---- |
|                     | 0.0001 |                    |     |     |     |     | -120           |        |     |     | G = +1, VIN = 1 VPP (0.354 VRMS) |     |      |
|                     |        | G = (cid:16)1, HD5 |     |     |     |     |                |        |     |     | G = +1, VIN = 5 VPP (1.768 VRMS) |     |      |
|                     | 5E-5   | G = (cid:14)1, HD2 |     |     |     |     |                |        |     |     |                                  |     |      |
|                     |        |                    |     |     |     |     | )Bd( edutilpmA | 0.001  |     |     |                                  |     | -100 |
| )(cid:8)( edutilpmA | 2E-5   | G = (cid:14)1, HD3 |     |     |     |     |                | 0.0007 |     |     |                                  |     |      |
|                     | 1E-5   | G = (cid:14)1, HD4 |     |     |     |     | -140           |        |     |     |                                  |     |      |
0.0005
|     | 5E-6 | G = (cid:14)1, HD5 |     |     |     |     |     |     |     |     |     |     |     |
| --- | ---- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.0003
2E-6
|     | 1E-6 |     |     |     |     |     | -160 | 0.0002 |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | ---- | ------ | --- | --- | --- | --- | --- |
5E-7
|     |      |     |     |     |     |     |      | 0.0001 |     |     |     |     | -120 |
| --- | ---- | --- | --- | --- | --- | --- | ---- | ------ | --- | --- | --- | --- | ---- |
|     | 2E-7 |     |     |     |     |     |      | 7E-5   |     |     |     |     |      |
|     | 1E-7 |     |     |     |     |     | -180 |        |     |     |     |     |      |
5E-5
5E-8
3E-5
2E-8
|     | 1E-8 |     |                |     |     |     | -200 | 22EE--55 |     |     |        |     |      |
| --- | ---- | --- | -------------- | --- | --- | --- | ---- | -------- | --- | --- | ------ | --- | ---- |
|     |      |     |                |     |     |     |      |          | r5  |     | r10    |     | r18  |
|     | 20   |     | 100            | 1k  |     | 10k | 20k  |          |     |     |        |     |      |
|     |      |     | Frequency (Hz) |     |     |     |      |          |     |     | VS (V) |     |      |
|     |      |     |                |     |     |     | D111 |          |     |     |        |     | D141 |
V OUT  = 3 V RMS Bandwidth = 80 kHz f = 1 kHz R L  = 2 k? Bandwidth = 80 kHz
Figure 6-9. Individual Harmonic Amplitude vs Frequency Figure 6-10. THD+N vs Supply Voltage
|     | 0.1 |     |     |     |     |     | -60 |     | 0   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
CCIF
-20
SMPTE
| )%( noitrotsiD noitaludomretnI |     |     |     |     |     |     | )Bd( noitrotsiD noitaludomretnI |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- |
-40
|     | 0.01 |     |     |     |     |     | -80 |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
-60
)cBd( edutilpmA
-80
|     | 0.001 |     |     |     |     |     | -100 |     | -100 |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | --- | --- | --- |
-120
-140
|     | 0.0001 |     |     |     |     |     | -120 |     |     |     |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
-160
-180
|     | 1E-5 |     |                         |     |                    |     | -140 |     | -200            |     |                |                    |         |
| --- | ---- | --- | ----------------------- | --- | ------------------ | --- | ---- | --- | --------------- | --- | -------------- | ------------------ | ------- |
|     | 10m  |     | 100m                    |     | 1                  |     | 10   |     | 20              | 100 | 1k             |                    | 10k 50k |
|     |      |     | Output Amplitude (VRMS) |     |                    |     | D140 |     |                 |     | Frequency (Hz) |                    | D142    |
|     |      |     |                         |     | Bandwidth = 80 kHz |     |      |     | G = 1, V  = 3 V |     | R  = 2 k?      | Bandwidth = 80 kHz |         |
|     |      |     |                         |     |                    |     |      |     | OUT             | RMS | L              |                    |         |
Figure 6-11. Intermodulation Distortion vs Amplitude Figure 6-12. FFT, 1-kHz Sine Wave
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 9
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | ---------- |
6.7 Typical Characteristics (continued)
| at T  = 25°C, V |  = ±15 V, R |  = 2 k?, and V |  = V | /2 (unless otherwise noted) |      |     |                |         |
| --------------- | ----------- | -------------- | ---- | --------------------------- | ---- | --- | -------------- | ------- |
| A               | S           | L              | CM S |                             |      |     |                |         |
| 0               |             |                |      |                             | 0    |     |                |         |
| -20             |             |                |      |                             | -20  |     |                |         |
| -40             |             |                |      |                             | -40  |     |                |         |
| -60             |             |                |      |                             | -60  |     |                |         |
| )cBd( edutilpmA |             |                |      | )cBd( edutilpmA             |      |     |                |         |
| -80             |             |                |      |                             | -80  |     |                |         |
| -100            |             |                |      |                             | -100 |     |                |         |
| -120            |             |                |      |                             | -120 |     |                |         |
| -140            |             |                |      |                             | -140 |     |                |         |
| -160            |             |                |      |                             | -160 |     |                |         |
| -180            |             |                |      |                             | -180 |     |                |         |
| -200            |             |                |      |                             | -200 |     |                |         |
|                 | 1k          | 10k            |      | 80k                         | 0    | 20k | 40k            | 60k 80k |
|                 |             | Frequency (Hz) |      |                             |      |     | Frequency (Hz) |         |
|                 |             |                |      | D143                        |      |     |                | D143    |
G = 1, V  = 3 V R  = 2 k? Bandwidth = 80 kHz V  = 3 V R  = 2 k? Bandwidth = 80 kHz
|     | OUT RMS | L   |     |     | OUT | RMS | L   |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Figure 6-13. FFT, 10-kHz Sine Wave Figure 6-14. FFT, CCIF Input (19 kHz + 20 kHz)
| -60 |     |     |     |     | 160 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
PSRR(cid:14)
|     |     |     |     |     | 140 |     |     | PSRR(cid:16) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ |
| -80 |     |     |     |     |     |     |     | CMRR         |
)Bd( noitarepeS lennahC
120
)Bd( oitaR noitcejeR
-100
100
| -120 |     |     |     |     | 80  |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- |
60
-140
40
-160
20
| -180 |         |                |     |      | 0    |     |                |        |
| ---- | ------- | -------------- | --- | ---- | ---- | --- | -------------- | ------ |
|      | 1k 10k  | 100k           | 1M  | 10M  | 1 10 | 100 | 1k 10k 100k    | 1M 10M |
|      |         | Frequency (Hz) |     |      |      |     | Frequency (Hz) |        |
|      |         |                |     | D114 |      |     |                | D107   |
| V    |  = 3 V  | G = 1          |     |      |      |     |                |        |
|      | OUT RMS |                |     |      |      |     |                |        |
Figure 6-15. Channel Separation vs Frequency
Figure 6-16. CMRR and PSRR vs Frequency (Referred to Input)
| 147                               |     |     |     |                                  | 126 |     |     |     |
| --------------------------------- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- |
| )Bd( oitaR noitcejeR ylppuS rewoP |     |     |     | )Bd( oitaR noitcejeR edoM-nommoC |     |     |     |     |
| 146                               |     |     |     |                                  | 125 |     |     |     |
| 145                               |     |     |     |                                  | 124 |     |     |     |
| 144                               |     |     |     |                                  | 123 |     |     |     |
| 143                               |     |     |     |                                  | 122 |     |     |     |
-40 -25 -10 5 20 35 50 65 80 95 110 125 -40 -25 -10 5 20 35 50 65 80 95 110 125
|     |     | Temperature (qC) |     |      |     | Temperature (qC) |     |      |
| --- | --- | ---------------- | --- | ---- | --- | ---------------- | --- | ---- |
|     |     |                  |     | D028 |     |                  |     | D027 |
|     |     |                  |     |      |     |                  |     |      |
Figure 6-17. Power Supply Rejection Ratio vs Temperature  Figure 6-18. Common Mode Rejection Ratio vs Temperature
|     | (Referred to Input) |     |     |     |     | (Referred to Input) |     |     |
| --- | ------------------- | --- | --- | --- | --- | ------------------- | --- | --- |
10 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| www.ti.com |     |     | SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |
| ---------- | --- | --- | ---------------------------------------------- | --- | --- |
6.7 Typical Characteristics (continued)
| at T  = 25°C, V |  = ±15 V, R  = 2 k?, and V |  = V /2 (unless otherwise noted) |     |     |     |
| --------------- | -------------------------- | -------------------------------- | --- | --- | --- |
| A               | S L                        | CM S                             |     |     |     |
| 15              |                            |                                  | 30  |     |     |
25
)%( sreifilpmA latoT
)%( sreifilpmA latoT
| 10  |     |     | 20  |     |     |
| --- | --- | --- | --- | --- | --- |
15
| 5   |     |     | 10  |     |     |
| --- | --- | --- | --- | --- | --- |
5
|       |                           |              | -2 -1.5 -1 | -0.5 0 0.5                   | 1 1.5 2 |
| ----- | ------------------------- | ------------ | ---------- | ---------------------------- | ------- |
| -1000 | -750 -500 -250 0 250      | 500 750 1000 |            |                              |         |
|       | Input Offset Voltage (PV) |              |            | Offset Voltage Drift (PV/qC) |         |
D001 D004
Count = 7955 Count = 32
Figure 6-19. Input Offset Voltage Distribution Figure 6-20. Input Offset Voltage Drift Distribution
| 1   |     |     | 100 |     |     |
| --- | --- | --- | --- | --- | --- |
-40qC
75
| 0.5                 |     |                     | 50  |     |     |
| ------------------- | --- | ------------------- | --- | --- | --- |
| )Vm( egatloV tesffO |     | )VP( egatloV tesffO |     |     |     |
25
| 0   |     |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- |
-25
| -0.5 |     |     | -50 |     |     |
| ---- | --- | --- | --- | --- | --- |
125qC
25qC
|     |     |     | -75  | 85qC |     |
| --- | --- | --- | ---- | ---- | --- |
| -1  |     |     | -100 |      |     |
-40 -25 -10 5 20 35 50 65 80 95 110 125 -18 -15 -12 -9 -6 -3 0 3 6 9 12 15 18
Temperature (qC) Input Common-Mode Voltage (V)
D017 D019

5 typical units shown
Figure 6-22. Input Offset vs Common Mode Voltage
Figure 6-21. Input Offset vs Temperature
|                    |                 | VIN  |                    |                 | VIN  |
| ------------------ | --------------- | ---- | ------------------ | --------------- | ---- |
|                    |                 | VOUT |                    |                 | VOUT |
| )vid/Vm 5( egatloV |                 |      | )vid/Vm 5( egatloV |                 |      |
|                    | Time (1 Ps/div) |      |                    | Time (1 Ps/div) |      |
D137 D135
|     | G = 1 C  = 20 pF |     | G = –1 | C  = 100 pF |     |
| --- | ---------------- | --- | ------ | ----------- | --- |
L L
Figure 6-23. Small-Signal Step Response (100 mV) Figure 6-24. Small-Signal Step Response (100 mV)
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 11
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- |
6.7 Typical Characteristics (continued)
| at T  = 25°C, V   |  = ±15 V, R |  = 2 k?, and V  |  = V /2 (unless otherwise noted) |      |                   |                 |      |
| ----------------- | ----------- | --------------- | -------------------------------- | ---- | ----------------- | --------------- | ---- |
| A                 | S           | L               | CM S                             |      |                   |                 |      |
|                   |             |                 | VIN                              |      |                   | VIN             |      |
|                   |             |                 | VOUT                             |      |                   | VOUT            |      |
| )vid/V 5( egatloV |             |                 |                                  |      | )vid/V 5( egatloV |                 |      |
|                   |             | Time (1 Ps/div) |                                  |      |                   | Time (1 Ps/div) |      |
|                   |             |                 |                                  | D136 |                   |                 | D139 |
|                   | G = 1       | R L  = 2 k?     | C L  = 100 pF                    |      | G = –1            | C L  = 100 pF   |      |
Figure 6-25. Large-Signal Step Response Figure 6-26. Large-Signal Step Response
| 158 |     |     |     |     | 100 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | 50  | IB+ |     |
| 156 |     |     |     |     | 20  | IB- |     |
IOS
10
| 154 |     |     |     | )An( tnerruC saiB tupnI | 5   |     |     |
| --- | --- | --- | --- | ----------------------- | --- | --- | --- |
2
1
)Bd( LOA 152
0.5
0.2
150
0.1
0.05
| 148 |     |     |     |     | 0.02 |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- |
0.01
0.005
146
0.002
| 144 |     |     |     |     | 0.001 |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- |
-40 -25 -10 5 20 35 50 65 80 95 110 125 -40 -25 -10 5 20 35 50 65 80 95 110 125
|     |     | Temperature(qC) |     |      |     | Temperature (qC) |      |
| --- | --- | --------------- | --- | ---- | --- | ---------------- | ---- |
|     |     |                 |     | D033 |     |                  | D024 |
|     |     |                 |     |      |     |                  |      |
Figure 6-27. Open-Loop Gain vs Temperature Figure 6-28. I  and I  vs Temperature
B OS
| 30                      |     |     |     |     | 4                          |            |     |
| ----------------------- | --- | --- | --- | --- | -------------------------- | ---------- | --- |
|                         | IB- |     |     |     |                            | VS = 4.5 V |     |
|                         | IB+ |     |     |     |                            | VS = 36 V  |     |
| 20                      | IOS |     |     |     |                            |            |     |
| )Ap( tnerruC saiB tupnI |     |     |     |     | )Am( tnerruC tnecseiuQ 3.9 |            |     |
10
|     | 0   |     |     |     | 3.8 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
-10
3.7
-20
| -30 |     |     |     |     | 3.6 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
-18 -15 -12 -9 -6 -3 0 3 6 9 12 15 18 -40 -25 -10 5 20 35 50 65 80 95 110 125
Temperature (qC)
|     | Input Common-Mode Voltage (V) |     |     | D023 |     |     | D031 |
| --- | ----------------------------- | --- | --- | ---- | --- | --- | ---- |
|     |                               |     |     |      |     |     |      |
Figure 6-29. I  and I  vs Common-Mode Voltage Figure 6-30. Supply Current vs Temperature
|     | B   | OS  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
12 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| www.ti.com |     |     |     |     |     | SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |
| ---------- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- |
6.7 Typical Characteristics (continued)
| at T |  = 25°C, V  = ±15 V, R |  = 2 k?, and V |     |  = V | /2 (unless otherwise noted) |     |     |     |     |
| ---- | ---------------------- | -------------- | --- | ---- | --------------------------- | --- | --- | --- | --- |
|      | A S                    | L              |     | CM S |                             |     |     |     |     |
|      | 4.5                    |                |     |      |                             | 18  |     |     |     |
|      | 4                      |                |     |      |                             | 17  |     |     |     |
25qC
)Am( tnerruC tnecseiuQ
|     |     |     |     |     |     | )V( egatloV tuptuO |     |     | -40qC |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ----- |
|     | 3.5 |     |     |     |     | 16                 |     |     |       |
|     | 3   |     |     |     |     | 15                 |     |     |       |
125qC
|     | 2.5 |     |     |     |     | 14  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 2   |     |     |     |     | 13  |     |     |     |
85qC
|     | 1.5 |     |     |     |     | 12  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0 4 8 12 16 20 24 28 32 36 0 10 20 30 40 50 60 70 80 90 100 110 120
|     |     | Supply Voltage (V) |     |     |      |     | Output Current (mA) |     |      |
| --- | --- | ------------------ | --- | --- | ---- | --- | ------------------- | --- | ---- |
|     |     |                    |     |     | D030 |     |                     |     | D025 |
|     |     |                    |     |     |      |     |                     |     |      |
Figure 6-31. Supply Current vs Supply Voltage Figure 6-32. Output Voltage vs Output Current (Sourcing)
|     | -12 |     |     |     |     | 140 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Sinking
|     |     | 85qC |     |     |     | 132 |     |     | Sourcing |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | -------- |
|     | -13 |      |     |     |     | 124 |     |     |          |
)Am( tnerruC tiucriC trohS
| )V( egatloV tuptuO |     |     |     |     |     | 116 |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
-14
|     |     | 125qC |     |     |     | 108 |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     | -15 |       |     |     |     | 100 |     |     |     |
92
-16
84
25qC
|     |     |     |     | -40qC |     | 76  |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
-17
68
|     | -18     |                     |          |        |         | 60          |                  |             |            |
| --- | ------- | ------------------- | -------- | ------ | ------- | ----------- | ---------------- | ----------- | ---------- |
|     |         |                     |          |        |         | -40 -25 -10 | 5 20             | 35 50 65 80 | 95 110 125 |
|     | 0 10 20 | 30 40 50            | 60 70 80 | 90 100 | 110 120 |             |                  |             |            |
|     |         | Output Current (mA) |          |        |         |             | Temperature (qC) |             |            |
|     |         |                     |          |        | D026    |             |                  |             | D041       |
|     |         |                     |          |        |         |             |                  |             |            |
Figure 6-33. Output Voltage vs Output Current (Sinking) Figure 6-34. Short-Circuit Current vs Temperature
|     | 75  |     |     |     |     | 100 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
RISO = 0 :
90 RISO = 25 :
RISO = 50 :
80
50
| )q( nigraM esahP |     |     |     |     |     | 70  |     |     |     |
| ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
)(cid:8)( toohsrevO
60
25
50
40
0
30
20
|     | -25 |                            |       |     |      | 10  |                           |       |      |
| --- | --- | -------------------------- | ----- | --- | ---- | --- | ------------------------- | ----- | ---- |
|     |     |                            |       |     |      | 10  |                           | 100   | 1000 |
|     | 10  |                            | 100   |     | 500  |     |                           |       |      |
|     |     | Load Capacitance,  CL (pF) |       |     |      |     | Load Capacitance, CL (pF) |       |      |
|     |     |                            |       |     | D105 |     |                           |       | D037 |
|     |     |                            | G = 1 |     |      |     |                           | G = 1 |      |
Figure 6-35. Phase Margin vs Capacitive Load Figure 6-36. Percent Overshoot vs Capacitive Load
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 13
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
| SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- |
6.7 Typical Characteristics (continued)
| at T  = 25°C, V |  = ±15 V, R |  = 2 k?, and V |  = V /2 (unless otherwise noted) |     |     |     |     |
| --------------- | ----------- | -------------- | -------------------------------- | --- | --- | --- | --- |
| A               | S           | L              | CM S                             |     |     |     |     |
60
RISO = 0 :
RISO = 25 :
| 50  | RISO = 50 : |     |                   |     |     |     |     |
| --- | ----------- | --- | ----------------- | --- | --- | --- | --- |
| 40  |             |     | )vid/V 5( egatloV |     |     |     |     |
)(cid:8)( toohsrevO
30
20
| 10  |     |     |     |     |     |     | VIN |
| --- | --- | --- | --- | --- | --- | --- | --- |
VOUT
0
Time (400 ns/div)
| 10  |     | 100 | 1000 |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- |
Load Capacitance, CL (pF)
D131 D134
|     |     | G = –1 |     |     | G = –10 |     |     |
| --- | --- | ------ | --- | --- | ------- | --- | --- |
Figure 6-37. Percent Overshoot vs Capacitive Load Figure 6-38. Negative Overload Recovery
1000
VIN
VOUT
100
)vid/V 5( egatloV
(cid:12):(cid:11)(cid:3)OZ
10
1
0.1
|     | Time (400 ns/div) |     |     | 1 10 | 100 1k | 10k 100k | 1M 10M |
| --- | ----------------- | --- | --- | ---- | ------ | -------- | ------ |
Frequency (Hz)
|     |     |         | D138 |     |     |     | D112 |
| --- | --- | ------- | ---- | --- | --- | --- | ---- |
|     |     | G = –10 |      |     |     |     |      |
Figure 6-39. Positive Overload Recovery Figure 6-40. Open-Loop Output Impedance vs Frequency
VIN
VOUT
)vid/V 5( egatloV
Time (400 ns/div)
D138
G = 1
Figure 6-41. No Phase Reversal
14 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

7 Detailed Description
7.1 Overview
The OPA1655 and OPA1656 (OPA165x) use a three-gain-stage architecture to achieve very low noise and
distortion. The Functional Block Diagram shows a simplified schematic of the OPA165x (one channel shown).
The devices consist of a low-noise input stage and feedforward pathway coupled to a high-current output stage.
This topology exhibits superior distortion performance under a wide range of loading conditions compared to
other operational amplifiers.
7.2 Functional Block Diagram
Feed-
forward
Path
CM1
CM2
+IN
Input Gain Output
OUT
Stage Stage Stage
-IN
7.3 Feature Description
7.3.1 Phase Reversal Protection
The OPA165x have internal phase-reversal protection. Many op amps exhibit phase reversal when the input is
driven beyond the linear common-mode range. This condition is most often encountered in noninverting circuits
when the input is driven beyond the specified common-mode voltage range, causing the output to reverse into
the opposite rail. The input of the OPA165x prevents phase reversal with excessive common-mode voltage.
Instead, the appropriate rail limits the output voltage. This performance is shown in Figure 7-1.
20
15
10
5
0
-5
-10
-15
-20
)V(
egatloV
OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
VIN
VOUT
Time (125 (cid:29)s/div)
C004
Figure 7-1. Output Waveform Devoid of Phase Reversal During an Input Overdrive Condition
7.3.2 Electrical Overstress
Designers often ask questions about the capability of an operational amplifier to withstand electrical overstress.
These questions tend to focus on the device inputs, but can involve the supply voltage pins or even the output
pin. Each of these different pin functions have electrical stress limits determined by the voltage breakdown
characteristics of the particular semiconductor fabrication process and specific circuits connected to the pin.
Additionally, internal electrostatic discharge (ESD) protection is built into these circuits to protect them from
accidental ESD events both before and during product assembly.
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 15
Product Folder Links: OPA1655 OPA1656

A good understanding of this basic ESD circuitry and the relevance to an electrical overstress event is helpful.
Figure 7-2 illustrates the ESD circuits contained in the OPA165x (indicated by the dashed line area). The ESD
protection circuitry involves several current-steering diodes connected from the input and output pins and routed
back to the internal power-supply lines, where the diodes meet at an absorption device internal to the operational
amplifier. This protection circuitry is intended to remain inactive during normal circuit operation.
TVS
RF
+VS
R1 IN± 20 Ÿ(cid:3)
RS IN+ 20 Ÿ(cid:3)
Power-Supply
ESD Cell RL
+
VIN ±
±VS
TVS
+ ±
+
± +
OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
Figure 7-2. Equivalent Internal ESD Circuitry Relative to a Typical Circuit Application
An ESD event produces a short-duration, high-voltage pulse that is transformed into a short-duration, high-
current pulse when discharging through a semiconductor device. The ESD protection circuits are designed to
provide a current path around the operational amplifier core to prevent damage. The energy absorbed by the
protection circuitry is then dissipated as heat.
When an ESD voltage develops across two or more amplifier device pins, current flows through one or
more steering diodes. Depending on the path that the current takes, the absorption device can activate. The
absorption device has a trigger, or threshold voltage, that is above the normal operating voltage of the OPA165x
but below the device breakdown voltage level. When this threshold is exceeded, the absorption device quickly
activates and clamps the voltage across the supply rails to a safe level.
When the operational amplifier connects into a circuit, as shown in Figure 7-2, the ESD protection components
are intended to remain inactive and do not become involved in the application circuit operation. However,
circumstances may arise where an applied voltage exceeds the operating voltage range of a given pin. If this
condition occurs, there is a risk that some internal ESD protection circuits can turn on and conduct current. Any
such current flow occurs through steering-diode paths and rarely involves the absorption device.
Figure 7-2 shows a specific example where the input voltage (V ) exceeds the positive supply voltage (V+)
IN
by 500 mV or more. Much of what happens in the circuit depends on the supply characteristics. If V+ can
sink the current, one of the upper input steering diodes conducts and directs current to V+. Excessively high
current levels can flow with increasingly higher V . As a result, the data sheet specifications recommend that
IN
applications limit the input current to 10 mA.
16 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

If the supply is not capable of sinking the current, V can begin sourcing current to the operational amplifier and
IN
then take over as the source of positive supply voltage. The danger in this case is that the voltage can rise to
levels that exceed the operational amplifier absolute maximum ratings.
Another common question involves what happens to the amplifier if an input signal is applied to the input when
the power supplies (V+ or V–) are at 0 V. Again, this question depends on the supply characteristic when at
0 V, or at a level below the input signal amplitude. If the supplies appear as high impedance, then the input
source supplies the operational amplifier current through the current-steering diodes. This state is not a normal
bias condition; most likely, the amplifier does not operate normally. If the supplies are low impedance, then the
current through the steering diodes can become quite high. The current level depends on the ability of the input
source to deliver current, and any resistance in the input path.
If there is any uncertainty about the ability of the supply to absorb this current, add external Zener diodes to the
supply pins; see Figure 7-2. Select the Zener voltage so that the diode does not turn on during normal operation.
However, the Zener voltage must be low enough so that the Zener diode conducts if the supply pin begins to rise
above the safe-operating, supply-voltage level.
7.3.3 EMI Rejection Ratio (EMIRR)
The electromagnetic interference (EMI) rejection ratio, or EMIRR, describes the EMI immunity of operational
amplifiers. An adverse effect that is common to many operational amplifiers is a change in the offset voltage
as a result of RF signal rectification. An operational amplifier that is more efficient at rejecting this change in
offset as a result of EMI has a higher EMIRR and is quantified by a decibel value. Measuring EMIRR can be
performed in many ways, but this document provides the EMIRR IN+, which specifically describes the EMIRR
performance when the RF signal is applied to the noninverting input pin of the operational amplifier. In general,
only the noninverting input is tested for EMIRR for the following three reasons:
• Operational amplifier input pins are known to be the most sensitive to EMI, and typically rectify RF signals
better than the supply or output pins.
• The noninverting and inverting operational amplifier inputs have symmetrical physical layouts and exhibit
nearly matching EMIRR performance.
• EMIRR is easier to measure on noninverting pins than on other pins because the noninverting input pin can
be isolated on a printed-circuit-board (PCB). This isolation allows the RF signal to be applied directly to the
noninverting input pin with no complex interactions from other components or connecting PCB traces.
A more formal discussion of the EMIRR IN+ definition and test method is provided in the EMI Rejection Ratio of
Operational Amplifiers application report, available for download at www.ti.com.
The EMIRR IN+ of the OPA165x is plotted versus frequency in Figure 7-3. If available, any dual and quad
operational amplifier device versions have nearly identical EMIRR IN+ performance. The OPA165x unity-gain
bandwidth is 20 MHz. EMIRR performance below this frequency denotes interfering signals that fall within the
operational amplifier bandwidth.
Frequency (Hz)
)Bd(
+NI
RRIME
OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
140
120
100
80
60
40
20
10M 100M 1G 10G
D115
Figure 7-3. OPA165x EMIRR vs Frequency
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 17
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
Table 7-1 lists the EMIRR IN+ values for the OPA165x at particular frequencies commonly encountered in real-
world applications. Applications listed in Table 7-1 can be centered on or operated near the particular frequency
shown. This information can be of special interest to designers working with these types of applications, or
working in other fields likely to encounter RF interference from broad sources, such as the industrial, scientific,
and medical (ISM) radio band.
Table 7-1. OPA165x EMIRR IN+ for Frequencies of Interest
FREQUENCY APPLICATION OR ALLOCATION EMIRR IN+
400 MHz Mobile radio, mobile satellite, space operation, weather, radar, UHF 36 dB
GSM, radio communication and navigation, GPS (to 1.6 GHz), ISM,
900 MHz 42 dB
aeronautical mobile, UHF
1.8 GHz GSM, mobile personal comm. broadband, satellite, L-band 52 dB
2.4 GHz 802.11b/g/n, Bluetooth® mobile personal comm., ISM, amateur radio and satellite, S-band 64 dB
3.6 GHz Radiolocation, aero comm./nav., satellite, mobile, S-band 67 dB
802.11a/n, aero communication and navigation, mobile communication,
5 GHz 77 dB
space and satellite operation, C-band
7.3.3.1 EMIRR IN+ Test Configuration
Figure 7-4 shows the circuit configuration for testing the EMIRR IN+. An RF source is connected to the
operational amplifier noninverting input pin using a transmission line. The operational amplifier is configured
in a unity-gain buffer topology with the output connected to a low-pass filter (LPF) and a digital multimeter
(DMM). A large impedance mismatch at the operational amplifier input causes a voltage reflection; however, this
effect is characterized and accounted for when determining the EMIRR IN+. The resulting dc offset voltage is
sampled and measured by the multimeter. The LPF isolates the multimeter from residual RF signals that can
interfere with multimeter accuracy. See the EMI Rejection Ratio of Operational Amplifiers application report for
more details.
Ambient temperature: 25Û&
+VS
±
50 (cid:13)(cid:3) Low-Pass Filter
+
RF source
DC Bias: 0 V
-VS
Sample /
Modulation: None (CW) Digital Multimeter
Frequency Sweep: 201 pt. Log Not shown: 0.1 µF and 10 µF Averaging
supply decoupling
Figure 7-4. EMIRR IN+ Test Configuration Schematic
7.4 Device Functional Modes
The OPA165x have a single functional mode and are operational when the power-supply voltage is greater than
4.5 V. The maximum specified power-supply voltage for the OPA165x is 36 V.
In all cases, the common-mode voltage must be maintained within the specified range. In addition, key
parameters are specified over the temperature range of T = –40°C to +125°C.
A
18 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
8 Application and Implementation
Note
Information  in  the  following  applications  sections  is  not  part  of  the  TI  component  specification,
and  TI  does  not  warrant  its  accuracy  or  completeness.  TI’s  customers  are  responsible  for
determining suitability of components for their purposes, as well as validating and testing their design
implementation to confirm system functionality.
8.1 Application Information
8.1.1 Basic Noise Calculations
Low-noise circuit design requires careful analysis of all noise sources. External noise sources can dominate in
many cases; consider the effect of source resistance on overall op amp noise performance. Total noise of the
circuit is the root-sum-square combination of all noise components.
Figure  8-1  shows  noninverting  (A)  and  inverting  (B)  op  amp  circuit  configurations  with  gain.  In  circuit
configurations with gain, the feedback network resistors contribute noise. In general, the current noise of the
op amp reacts with the feedback resistors to create additional noise components.
The selected feedback resistor values make these noise sources negligible. Low impedance feedback resistors
load the output of the amplifier. The equations for total noise are shown for both configurations.
(A) Noise in Noninverting Gain Configuration Noise at the output is given as EO, where
| R1  | R2  |       |        |          |               |     |            |        |         |        |
| --- | --- | ----- | ------ | -------- | ------------- | --- | ---------- | ------ | ------- | ------ |
|     |     |       | 4      |          |               | 2+  |            | 4      | „4 2    |        |
|     |     | 1 '1= | 1+ 2   | „ A5; 2+ | A0; 2+ A41æ42 |     | E0 „45; 2+ | E0 „ 1 | 2       |  84/5  |
|     |     | : ;   | l 4 1p | ¨:       | :             |     | :          | l 4 1  | + 4 2hp | > ?    |
|     | ±   |       |        |          | k             | o   |            | d      |         |        |
GND
|     | EO  |       |               |     | 8     |     |                     |     |     |     |
| --- | --- | ----- | ------------- | --- | ----- | --- | ------------------- | --- | --- | --- |
|     |     | 2 A5= | 4„G$ „6(-)„45 |     |       |     | Thermal noise of RS |     |     |     |
|     | +   | : ;   |               |     | ¾ *V  |     |                     |     |     |     |
|     |     |       | ¥             |     | d h   |     |                     |     |     |     |
RS
|     |     |          |        |        | 4 1 „4 2    | 8       |                           |     |     |     |
| --- | --- | -------- | ------ | ------ | ----------- | ------- | ------------------------- | --- | --- | --- |
|     |     | 3 A41æ42 | = 4„G$ | „6(-)„ |             |         | Thermal noise of R1 || R2 |     |     |     |
|     |     | : ;      | ¨      |        | d 4 1 +4 2h | d ¾*V h |                           |     |     |     |
+
|     | VS  |                 |     |     | ,     |     |                    |     |     |     |
| --- | --- | --------------- | --- | --- | ----- | --- | ------------------ | --- | --- | --- |
| ±   |     | 4 G$=1.38065„10 |     | 23  |       |     | Boltzmann Constant |     |     |     |
|     |     | : ;             |     | F   | -     |     |                    |     |     |     |
|     |     |                 |     |     | d h   |     |                    |     |     |     |
Source
|     |     | 5 6(-)=237.15+6(°%) |     |     |  -   |     | Temperature in kelvins |     |     |     |
| --- | --- | ------------------- | --- | --- | ---- | --- | ---------------------- | --- | --- | --- |
|     |     | : ;                 |     |     | > ?  |     |                        |     |     |     |
GND
(B) Noise in Inverting Gain Configuration Noise at the output is given as EO, where
| R1  | R2  |       |      |           |                  |     |       |               |        |     |
| --- | --- | ----- | ---- | --------- | ---------------- | --- | ----- | ------------- | ------ | --- |
|     |     |       |      |           |                  |     |       | „             | 2      |     |
|     |     |       |      | 4 2 „     |                  | 2   | „     | 4 5 + 4 1 4   | 2      |     |
|     |     | 6 '1= | 1+   |           | A0; 2+ A41+45æ42 | +   | E0 :  | ;             |  84/5  |     |
|     |     | : ;   | l 45 | + 4 1p ¨: | k                | o   | F H 4 | 5 + 4 1 + 4 2 | IG >   | ?   |
RS ±
EO
|     | +   |             |     |             | 4 5 +     | 4 1 „ 4 2 | 8     |                                  |     |     |
| --- | --- | ----------- | --- | ----------- | --------- | --------- | ----- | -------------------------------- | --- | --- |
|     |     | 7 A41+45æ42 | =   | 4„G$ „6(-)„ | :         | ;         |       |                                  |     |     |
|     |     | : ;         | ¨   |             | H 4 5 + 4 | 1 + 4 2 I | ¾ *V  | Thermal noise of (R1 + RS) || R2 |     |     |
| +   |     |             |     |             |           |           | d h   |                                  |     |     |
VS
| ±      |     |                     |     |     | ,     |     |     |                        |     |     |
| ------ | --- | ------------------- | --- | --- | ----- | --- | --- | ---------------------- | --- | --- |
|        | GND | 8 G$=1.38065„10     |     | 23  |       |     |     |                        |     |     |
| Source |     | : ;                 |     | F   | -     |     |     | Boltzmann Constant     |     |     |
|        |     |                     |     |     | d h   |     |     |                        |     |     |
| GND    |     | 9 6(-)=237.15+6(°%) |     |     |  -    |     |     | Temperature in kelvins |     |     |
|        |     | : ;                 |     |     | > ?   |     |     |                        |     |     |
Copyright © 2017, Texas Instruments Incorporated
where
• e N  is the voltage noise of the amplifier. For the OPA165x, e N  = 4.3 nV/?Hz at 1 kHz.
• i  is the current noise of the amplifier. For the OPA165x, i  = 6 fA/?Hz at 1 kHz.
N N
Note: For additional resources on noise calculations, see TI's Precision Labs Series.
Figure 8-1. Noise Calculation in Gain Configurations
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 19
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
8.2 Typical Applications
8.2.1 Preamplifier Circuit for Vinyl Record Playback With Moving-Magnet Phono Cartridges
The  noise  and  distortion  performance  of  the  OPA165x  is  exceptional  in  applications  with  high  source
impedances, which makes these devices an excellent choice in preamplifier circuits for moving magnet phono
cartridges. The high source impedance of the cartridge, and high gain required by the RIAA playback curve at
low frequency, requires an amplifier with both low input current noise and low input voltage noise.
15 V
MM Phono Input C5
R5
|     |     | OPA165x 100  F |     |
| --- | --- | -------------- | --- |
+ 100  (cid:8)
+IN (cid:7)
| R1  | C1  |     | Output |
| --- | --- | --- | ------ |
– VOUT
| 47 k | 150 pF | IN  |     |
| ---- | ------ | --- | --- |
(cid:5)
|     |     | (cid:1)            | R6      |
| --- | --- | ------------------ | ------- |
|     |     | 15 V               | 100 k   |
|     |     | R2 R3              | (cid:9) |
|     |     | 118 k (cid:0) 10 k |         |
(cid:2) (cid:3)
C2 C3
R4
|     |     | 27 nF 7.5 nF |     |
| --- | --- | ------------ | --- |
127
(cid:4)
C4
100  F
(cid:6)
Figure 8-2. Preamplifier Circuit for Vinyl Record Playback With Moving-Magnet Phono Cartridges
(Single Channel Shown)
8.2.1.1 Design Requirements
• Gain: 40 dB (1 kHz)
• RIAA accuracy: ±0.5 dB (100 Hz to 20 kHz)
• Power supplies: ±15 V
20 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

8.2.1.2 Detailed Design Procedure
Vinyl records are recorded using an equalization curve specified by the Recording Institute Association of
America (RIAA). The purpose of this equalization curve is to decrease the amount of space occupied by a
groove on the record and therefore maximize the amount of information able to be stored. Proper playback
of music stored on the record requires a preamplifier circuit that applies the inverse transfer function of the
recording equalization curve. The combination of the recording equalization and the playback equalization
results in a flat frequency response over the audio range, as Figure 8-3 shows.
20
15
10
5
0
-5
-10
-15
-20
10 100 1000 10000
)Bd(
niaG
OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
Playback Curve
Combined Response
Recording Curve
Frequency (Hz)
C009
Figure 8-3. RIAA Recording and Playback Curves Normalized at 1 kHz
The basic RIAA playback curve implements three time constants: 75 ?s, 380 ?s, and 3180 ?s. An IEC
amendment was later added to the playback curve and implements a pole in the curve at 20 Hz with the
intent of protecting loudspeakers from excessive low frequency content. Rather than strictly adhering to the
IEC amendment, this design moves this pole to a lower frequency to improve low frequency response and still
provide protection for loudspeakers.
Resistor R1 and capacitor C1 are selected to provide the proper input impedance for the moving magnet
cartridge. Cartridge loading is specified by the manufacturer in the cartridge datasheet and is absolutely crucial
for proper response at high frequency. 47 k? is a common value for the input resistor, and the capacitive
loading is usually specified from 200 pF to 300 pF per channel. This capacitive loading specification includes
the capacitance of the cable connecting the turntable to the preamplifier, as well as any additional parasitic
capacitances at the preamplifier input. Therefore, the value of C1 must be less than the loading specification to
account for these additional capacitances.
The output network consisting of R5, R6, and C5 serves to ac couple the preamplifier circuit to any subsequent
electronics in the signal path. 100-? resistor R5 limits in-rush current into coupling capacitor C5 and prevents
parasitic capacitance from cabling from causing instability. R6 prevents charge accumulation on C5. Capacitor
C5 is chosen to be the same value as C4; for simplicity however, the value of C5 must be large enough to avoid
attenuating low-frequency information.
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 21
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
The feedback resistor elements must be selected to provide the correct response within the audio bandwidth. In
order to achieve the correct frequency response, the passive components in Figure 8-2 must satisfy Equation 1,
Equation 2, and Equation 3:
(1)
R2×C2=3180 ?s (2)
R3×C3=75 ?s (3)
R2, R3, a R n2d R R 43 m × ust C 2al + so C 3be = s 3 e 1 le 8 c ? te s d to meet the design requirements for gain. The gain at 1 kHz is determined
by subtracting 20 dB from gain of the circuit at very low-frequency (near dc), as shown in Equation 4:
(4)
Therefor A e1,k Hthze = l A oLwF ? fre 2 q 0 u d e B ncy gain of the circuit must be 60 dB to meet the goal of 40 dB at 1 kHz and is
determined by resistors R2, R3, and R4 as shown in Equation 5:
(5)
R3+R2
Because
A L
th
F
e
=
re
1
a
+
re m
R4ultip =
le
1
c
0
o
00
m b
6
i
0
n a
d
t
B
ions of passive components that satisfy these equations, a spreadsheet or
other software calculation tool is the easiest method to examine resistor and capacitor combinations.
Capacitor C4 forces the gain of the circuit to unity at dc in order to limit the offset voltage at the output of the
preamplifier circuit. The high-pass corner frequency created by this capacitor is calculated by Equation 6:
(6)
1
The circ F u H it P d = e 2 s ? c R ri4b C e4d in Figure 8-2 is constructed with 1% tolerance resistors and 5% tolerance NP0, C0G
ceramic capacitors without any additional hand sorting. The large value of C4 typically requires an electrolytic
type to be used. However, electrolytic capacitors have the potential to introduce distortion into the signal path.
This circuit is constructed using a bipolar electrolytic capacitor specifically intended for audio applications.
22 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

8.2.1.3 Application Curves
The deviation from the ideal RIAA transfer function curve is shown in Figure 8-4 and normalized to an ideal gain
of 40 dB at 1 kHz. The measured gain at 1 kHz is 0.05 dB less than the design goal, and the maximum deviation
from 100 Hz to 20 kHz is 0.18 dB. The deviation from the ideal curve can be improved by hand-sorting resistor
and capacitor values to their ideal values. The value of C4 can also be increased to reduce the deviation at low
frequency.
A spectrum of the preamplifier output signal is shown in Figure 8-5 for a 10 mV , 1-kHz input signal (1-V
RMS RMS
output). All distortion harmonics are below the preamplifier noise floor.
Frequency (Hz)
)Bd(
edutingaM
1.5
1
0.5
0
-0.5
10 100 1k 10k
Frequency (Hz)
D202
Figure 8-4. Measured Deviation
From Ideal RIAA Response
)VBd(
edutilpmA
OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
0
-10
-20
-30
-40
-50
-60
-70
-80
-90
-100
-110
-120
-130
-140
-150
-160
100 1k 10k
D201
Figure 8-5. Output Spectrum for a 10-mV ,
RMS
1?kHz Input Signal
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 23
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
8.2.2 Composite Headphone Amplifier
Figure 8-6 shows the BUF634A buffer inside the feedback loop of the OPA165x to increase the available
output current for low-impedance headphones. If the BUF634A is used in wide-bandwidth mode, no additional
components beyond the feedback resistors are required to maintain loop stability.
12 V
100  F
(cid:2)
0.1  F
(cid:3)
0.1  F
(cid:4)
OPA165x
|     | Input + |     |     |     |     |
| --- | ------- | --- | --- | --- | --- |
Output
|     | –   |     | BUF634A |     |     |
| --- | --- | --- | ------- | --- | --- |
R1
|     | 100 k |     | 0.1  F |     |     |
| --- | ----- | --- | ------ | --- | --- |
(cid:5)
(cid:9)
0.1  F RBW
(cid:6)
100  F
(cid:7)
12 V
(cid:8)
|     | R2      | R3      |     |     |     |
| --- | ------- | ------- | --- | --- | --- |
|     | 500     | 500     |     |     |     |
|     | (cid:0) | (cid:1) |     |     |     |
Figure 8-6. Composite Headphone Amplifier (Single-Channel Shown)
8.2.2.1 Application Curves
| -85      |     |     | 0   |          |     |
| -------- | --- | --- | --- | -------- | --- |
| 249 : RL |     |     |     | 249 : RL |     |
32 : RL
| 16 : RL |     |     | -30 |     |     |
| ------- | --- | --- | --- | --- | --- |
-90
| )Bd( N + DHT |     | )cBd( edutilpmA | -60 |     |     |
| ------------ | --- | --------------- | --- | --- | --- |
-95
-90
-100
-120
-105
-150
| -110           |       |        | -180   |                |       |
| -------------- | ----- | ------ | ------ | -------------- | ----- |
| 20 Hz 100 Hz   | 1 kHz | 20 kHz |        |                |       |
|                |       |        | 0 5000 | 10000 15000    | 20000 |
| Frequency (Hz) |       |        |        | Frequency (Hz) |       |
|                |       | C051   |        |                | C052  |
Figure 8-7. THD+N vs Frequency for a  Figure 8-8. FFT for a 5-V  (1.77-V ),
|              |                |     |                    | PP RMS |     |
| ------------ | -------------- | --- | ------------------ | ------ | --- |
| 5?V  (1.77?V | ) Input Signal |     | 1?kHz Input Signal |        |     |
| PP           | RMS            |     |                    |        |     |
24 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
8.2.3 Baxandall Tone Control
Figure 8-9 gives an example of ultra-low noise and THD tone control. This circuit provides 20 dB of gain at the
first stage, followed by two separate tone controls for bass and treble. The passive circuit is designed to yield a
flat gain response with the potentiometers both set to 50%.
Bass
|     | 1.69 k    15.4 k |     | 11 k    | 100 k |    11 k |     |
| --- | ---------------- | --- | ------- | ----- | ------- | --- |
(cid:2)
|     | (cid:7) | (cid:6) | (cid:3) |     | (cid:0) |     |
| --- | ------- | ------- | ------- | --- | ------- | --- |
|     | 10 µF   |         | 10 nF   |     | 10 nF   |     |
–
|       |                |     |     | 11 k     |          | 15 V     |
| ----- | -------------- | --- | --- | -------- | -------- | -------- |
| Input | +              |     |     |          | (cid:10) |          |
|       |                | 1/2 |     |          |          | – Output |
|       | 10 µF  OPA1656 |     |     |          |          | 1/2      |
|       |                |     |     | 4.7 nF   |          | +        |
OPA1656
|     | 1.69 k |         |           |                |            |            |
| --- | ------ | ------- | --------- | -------------- | ---------- | ---------- |
|     |        | (cid:9) |           |                |            | 15 V       |
|     |        |         | 3.65 k    |                | 3.65 k     |    (cid:1) |
|     |        |         | (cid:4)   | 500 k          |    (cid:5) |            |
|     |        |         |           | Treble (cid:8) |            |            |
Figure 8-9. Dual Potentiometer Baxandall Tone Control
8.2.3.1 Application Curves
40
10% Bass / 90% Treble
|     | 36  |     |     |     | 50% Bass / 50% Treble |     |
| --- | --- | --- | --- | --- | --------------------- | --- |
90% Bass / 10% Treble
32
28
)Bd( edutilpmA
24
20
16
12
8
4
0
|     |     |     | 100 |     | 1k  | 10k |
| --- | --- | --- | --- | --- | --- | --- |
Frequency (Hz)
D203
Figure 8-10. Amplitude vs Frequency for Various Tone-Control Settings
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 25
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
8.2.4 Guitar Input to XLR Output
The OPA165x are an excellent choice for guitar input circuits as a result of the high input impedance and
ultra-low noise performance. Figure 8-11 gives an example of a basic guitar input circuit to differential XLR
schematic. The logarithmic taper potentiometer shown in this circuit provides 6 dB of gain at 0%, and 40 dB of
gain at 100%. The rail-to-rail output swing of the OPA165x allows for a high amplitude swing at the outputs of
the differentially configured amplifiers, while maintaining very low distortion performance. A 10-µF dc blocking
capacitor is used in the feedback of the noninverting stage to remove any dc offset as a result of the amplifier
offset voltage. However, this dc blocking capacitor can be eliminated for applications that are not sensitive to low
dc offsets.
100 k
| 10 µF   | (cid:3) |     |     |
| ------- | ------- | --- | --- |
| 1 k     | 1 k     |     |     |
(cid:0) (cid:4)
| ¼ Inch  | 10 pF   |     |     |
| ------- | ------- | --- | --- |
–
Jack
49
|     | + 1/2 | (cid:5) |     |
| --- | ----- | ------- | --- |
OPA1656
1 M
(cid:2)
XLR
Output
1 k
(cid:6) 1 k
(cid:7)
10 pF
5 V
|     | –   | 49     |     |
| --- | --- | ------ | --- |
(cid:8)
1/2
+
OPA1656
5 V
(cid:1)
Figure 8-11. Guitar Input to XLR Output Schematic
8.2.4.1 Application Curves
| 0.1  |     |               | 3.3 |
| ---- | --- | ------------- | --- |
| 0.08 |     | Input Voltage | 3   |
Output Voltage 1
| 0.06                |           |                  | 2.7                    |
| ------------------- | --------- | ---------------- | ---------------------- |
| 0.04                |           | Output Voltage 2 | 2.4                    |
| 0.02                |           |                  | 2.1                    |
| )V( egatloV tupnI 0 |           |                  | 1.8 )V( egatloV tuptuO |
| -0.02               |           |                  | 1.5                    |
| -0.04               |           |                  | 1.2                    |
| -0.06               |           |                  | 0.9                    |
| -0.08               |           |                  | 0.6                    |
| -0.1                |           |                  | 0.3                    |
| -0.12               |           |                  | 0                      |
| -0.14               |           |                  | -0.3                   |
| -0.16               |           |                  | -0.6                   |
| -0.18               |           |                  | -0.9                   |
| -0.2                |           |                  | -1.2                   |
| 0 0.4 0.8           | 1.2 1.6 2 | 2.4 2.8 3.2      | 3.6 4                  |
D200
Figure 8-12. 1-kHz Input Signal Transient Simulation
26 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
8.3 Power Supply Recommendations
The OPA165x are specified for operation from 4.5 V to 36 V (±2.25 V to ±18 V); many specifications apply from
–40°C to +125°C. Parameters that can exhibit significant variance with regard to operating voltage or
temperature are presented in the Typical Characteristics section.
The OPA165x operate with as little as 4.5 V between the supplies and with up to 36 V between the supplies.
However, some applications do not require equal positive and negative output voltage swing. With the OPA165x,
power-supply voltages are not required to be equal. For example, the positive supply can be set to 25 V with the
negative supply at –5 V.
8.4 Layout
8.4.1 Layout Guidelines
For best operational performance of the device, use good printed-circuit board (PCB) layout practices, including:
• Noise can propagate into analog circuitry through the power pins of the circuit as a whole and of op amp
itself. Bypass capacitors are used to reduce the coupled noise by providing low-impedance power sources
local to the analog circuitry.
– Connect low-ESR, 0.1-µF ceramic bypass capacitors between each supply pin and ground, placed as
close to the device as possible. A single bypass capacitor from V+ to ground is applicable for single-
supply applications.
• Separate grounding for analog and digital portions of circuitry is one of the simplest and most-effective
methods of noise suppression. One or more layers on multilayer PCBs are usually devoted to ground planes.
A ground plane helps distribute heat and reduces electromagnetic interference (EMI) noise pickup. Physically
separate digital and analog grounds, observing the flow of the ground current.
• To reduce parasitic coupling, run the input traces as far away from the supply or output traces as possible. If
these traces cannot be kept separate, crossing the sensitive trace perpendicular is much better as opposed
to in parallel with the noisy trace.
• Place the external components as close to the device as possible. As illustrated in Figure 8-13, keeping R
F
and R close to the inverting input minimizes parasitic capacitance.
G
• Keep the length of input traces as short as possible. Always remember that the input traces are the most
sensitive part of the circuit.
• Consider a driven, low-impedance guard ring around the critical traces. A guard ring can significantly reduce
leakage currents from nearby traces that are at different potentials.
• Cleaning the PCB following board assembly is recommended for best performance.
• Any precision integrated circuit can experience performance shifts resulting from moisture ingress into the
plastic package. Following any aqueous PCB cleaning process, baking the PCB assembly is recommended
to remove moisture introduced into the device packaging during the cleaning process. A low-temperature,
post-cleaning bake at 85°C for 30 minutes is sufficient for most circumstances.
8.4.1.1 Power Dissipation
The OPA165x op amps are capable of driving 600-? loads with a power-supply voltage up to ±18 V and
full operating temperature range. Internal power dissipation increases when operating at high supply voltages.
Copper leadframe construction used in the OPA165x improves heat dissipation compared to conventional
materials. Circuit board layout can also help minimize junction temperature rise. Wide copper traces help
dissipate the heat by acting as an additional heat sink. Temperature rise can be further minimized by soldering
the devices to the circuit board rather than using a socket.
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 27
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
8.4.2 Layout Example
|     | VIN A | +   | VIN B | +   |     |
| --- | ----- | --- | ----- | --- | --- |
VOUT A VOUT B
|     | RG  |     | RG  |     |     |
| --- | --- | --- | --- | --- | --- |
|     |     | RF  |     | RF  |     |
(Schematic Representation)
| Place components  | Output A |     |     |     |     |
| ----------------- | -------- | --- | --- | --- | --- |
c lo s e   t o   d e v i ce   a n d  t o   VS+ U s e  lo w -E S R ,
e a c h   o t h e r  t o  r e d u c e   c er a m ic  b yp a s s
| parasitic errors.  |     |     |     |     | capacitor. Place as  |
| ------------------ | --- | --- | --- | --- | -------------------- |
close to the device
as possible.
|       | OUTPUT A |     |     | V+       | GND      |
| ----- | -------- | --- | --- | -------- | -------- |
|       | RF       |     |     |          | Output B |
| GND   | -IN A    |     |     | OUTPUT B |          |
|       | RG       |     |     | RF       |          |
| VIN A | +IN A    |     |     | -IN B    | GND      |
RG
|     | V±  |     |     | +IN B | VIN B |
| --- | --- | --- | --- | ----- | ----- |
Keep input traces short
U s e   lo w -E S R ,   and   r u n   t h e   in p u t  tr aces
c e r a m i c   b y p a s s   GND
ca p a c i t o r .   P la c e   a s  VS± a s   fa r  a w a y   f r o m
|     |     | Ground (GND) plane on another layer  |     | t h e |   s u p p ly  l i n e s |
| --- | --- | ------------------------------------ | --- | ----- | ----------------------- |
close to the device  as possible.
as possible.
Figure 8-13. Operational Amplifier Board Layout for Noninverting Configuration
28 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
www.ti.com SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022
9 Device and Documentation Support
9.1 Device Support
9.1.1 Development Support
9.1.1.1 PSpice® for TI
PSpice® for TI is a design and simulation environment that helps evaluate performance of analog circuits. Create
subsystem designs and prototype solutions before committing to layout and fabrication, reducing development
cost and time to market.
9.1.1.2 TINA-TI™ Simulation Software (Free Download)
TINA-TI™ simulation software is a simple, powerful, and easy-to-use circuit simulation program based on a
SPICE engine. TINA-TI simulation software is a free, fully-functional version of the TINA™ software, preloaded
with a library of macromodels, in addition to a range of both passive and active models. TINA-TI simulation
software provides all the conventional dc, transient, and frequency domain analysis of SPICE, as well as
additional design capabilities.
Available as a free download from the Design tools and simulation web page, TINA-TI simulation software offers
extensive post-processing capability that allows users to format results in a variety of ways. Virtual instruments
offer the ability to select input waveforms and probe circuit nodes, voltages, and waveforms, creating a dynamic
quick-start tool.
Note
These files require that either the TINA software or TINA-TI software be installed. Download the free
TINA-TI simulation software from the TINA-TI™ software folder.
9.1.1.3 DIP-Adapter-EVM
Speed up your op amp prototyping and testing with the DIP-Adapter-EVM, which provides a fast, easy and
inexpensive way to interface with small, surface-mount devices. Connect any supported op amp using the
included Samtec terminal strips or wire them directly to existing circuits. The DIP-Adapter-EVM kit supports
the following industry-standard packages: D or U (SOIC-8), PW (TSSOP-8), DGK (VSSOP-8), DBV (SOT-23-6,
SOT-23-5 and SOT-23-3), DCK (SC70-6 and SC70-5), and DRL (SOT563-6).
9.1.1.4 DIYAMP-EVM
The DIYAMP-EVM is a unique evaluation module (EVM) that provides real-world amplifier circuits, enabling the
user to quickly evaluate design concepts and verify simulations. This EVM is available in three industry-standard
packages (SC70, SOT23, and SOIC) and 12 popular amplifier configurations, including amplifiers, filters, stability
compensation, and comparator configurations for both single and dual supplies.
9.1.1.5 TI Reference Designs
TI reference designs are analog solutions created by TI’s precision analog applications experts. TI reference
designs offer the theory of operation, component selection, simulation, complete PCB schematic and layout, bill
of materials, and measured performance of many useful circuits. TI reference designs are available online at
https://www.ti.com/reference-designs.
9.1.1.6 Filter Design Tool
The filter design tool is a simple, powerful, and easy-to-use active filter design program. The filter design tool
allows the user to create optimized filter designs using a selection of TI operational amplifiers and passive
components from TI's vendor partners.
Available as a web-based tool from the Design tools and simulation web page, the filter design tool allows the
user to design, optimize, and simulate complete multistage active filter solutions within minutes.
Copyright © 2022 Texas Instruments Incorporated Submit Document Feedback 29
Product Folder Links: OPA1655 OPA1656

OPA1655, OPA1656
SBOS901C – MARCH 2019 – REVISED SEPTEMBER 2022 www.ti.com
9.2 Documentation Support
9.2.1 Related Documentation
The following documents are recommended for reference when using the OPA165x, and are available for
download at www.ti.com.
• Texas Instruments, Source Resistance and Noise Considerations in Amplifiers technical brief
• Texas Instruments, Single-Supply Operation of Operational Amplifiers application bulletin
• Texas Instruments, Op Amp Performance Analysis application bulletin
• Texas Instruments, Compensate Transimpedance Amplifiers Intuitively application report
• Texas Instruments, Tuning in Amplifiers application bulletin
• Texas Instruments, Feedback Plots Define Op Amp AC Performance application bulletin
• Texas Instruments, Active Volume Control for Professional Audio design guide
9.3 Receiving Notification of Documentation Updates
To receive notification of documentation updates, navigate to the device product folder on ti.com. Click on
Subscribe to updates to register and receive a weekly digest of any product information that has changed. For
change details, review the revision history included in any revised document.
9.4 Support Resources
TI E2E™ support forums are an engineer's go-to source for fast, verified answers and design help — straight
from the experts. Search existing answers or ask your own question to get the quick design help you need.
Linked content is provided "AS IS" by the respective contributors. They do not constitute TI specifications and do
not necessarily reflect TI's views; see TI's Terms of Use.
9.5 Trademarks
Burr-Brown™, TINA-TI™, and TI E2E™ are trademarks of Texas Instruments.
TINA™ is a trademark of DesignSoft, Inc.
Bluetooth® is a registered trademark of Bluetooth SIG, Inc.
PSpice® is a registered trademark of Cadence Design Systems, Inc.
All trademarks are the property of their respective owners.
9.6 Electrostatic Discharge Caution
This integrated circuit can be damaged by ESD. Texas Instruments recommends that all integrated circuits be handled
with appropriate precautions. Failure to observe proper handling and installation procedures can cause damage.
ESD damage can range from subtle performance degradation to complete device failure. Precision integrated circuits may
be more susceptible to damage because very small parametric changes could cause the device not to meet its published
specifications.
9.7 Glossary
TI Glossary This glossary lists and explains terms, acronyms, and definitions.
10 Mechanical, Packaging, and Orderable Information
The following pages include mechanical, packaging, and orderable information. This information is the most
current data available for the designated devices. This data is subject to change without notice and revision of
this document. For browser-based versions of this data sheet, refer to the left-hand navigation.
30 Submit Document Feedback Copyright © 2022 Texas Instruments Incorporated
Product Folder Links: OPA1655 OPA1656

PACKAGE OPTION ADDENDUM
www.ti.com 9-Nov-2025
PACKAGING INFORMATION
Orderable part number Status Material type Package | Pins Package qty | Carrier RoHS Lead finish/ MSL rating/ Op temp (°C) Part marking
(1) (2) (3) Ball material Peak reflow (6)
(4) (5)
OPA1655DBVR Active Production SOT-23 (DBV) | 5 3000 | LARGE T&R Yes SN Level-2-260C-1 YEAR -40 to 125 2R8Q
OPA1655DBVR.B Active Production SOT-23 (DBV) | 5 3000 | LARGE T&R Yes SN Level-2-260C-1 YEAR -40 to 125 2R8Q
OPA1655DBVT Active Production SOT-23 (DBV) | 5 250 | SMALL T&R Yes SN Level-2-260C-1 YEAR -40 to 125 2R8Q
OPA1655DBVT.B Active Production SOT-23 (DBV) | 5 250 | SMALL T&R Yes SN Level-2-260C-1 YEAR -40 to 125 2R8Q
OPA1655DR Active Production SOIC (D) | 8 3000 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1655
OPA1655DR.B Active Production SOIC (D) | 8 3000 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1655
OPA1656ID Active Production SOIC (D) | 8 75 | TUBE Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1656
OPA1656ID.B Active Production SOIC (D) | 8 75 | TUBE Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1656
OPA1656IDR Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1656
OPA1656IDR.B Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1656
OPA1656IDRG4 Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1656
OPA1656IDRG4.B Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 OP1656
(1) Status: For more details on status, see our product life cycle.
(2) Material type: When designated, preproduction parts are prototypes/experimental devices, and are not yet approved or released for full production. Testing and final process, including without limitation quality assurance,
reliability performance testing, and/or process qualification, may not yet be complete, and this item is subject to further changes or possible discontinuation. If available for ordering, purchases will be subject to an additional
waiver at checkout, and are intended for early internal evaluation purposes only. These items are sold without warranties of any kind.
(3) RoHS values: Yes, No, RoHS Exempt. See the TI RoHS Statement for additional information and value definition.
(4) Lead finish/Ball material: Parts may have multiple material finish options. Finish options are separated by a vertical ruled line. Lead finish/Ball material values may wrap to two lines if the finish value exceeds the maximum
column width.
(5) MSL rating/Peak reflow: The moisture sensitivity level ratings and peak solder (reflow) temperatures. In the event that a part has multiple moisture sensitivity ratings, only the lowest level per JEDEC standards is shown.
Refer to the shipping label for the actual reflow temperature that will be used to mount the part to the printed circuit board.
(6) Part marking: There may be an additional marking, which relates to the logo, the lot trace code information, or the environmental category of the part.
Multiple part markings will be inside parentheses. Only one part marking contained in parentheses and separated by a "~" will appear on a part. If a line is indented then it is a continuation of the previous line and the two
combined represent the entire part marking for that device.
Addendum-Page 1

PACKAGE OPTION ADDENDUM
www.ti.com 9-Nov-2025
Important Information and Disclaimer:The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and
makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative
and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers
and other limited information may not be available for release.
In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.
Addendum-Page 2

PACKAGE MATERIALS INFORMATION
|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
www.ti.com 10-Aug-2026
TAPE AND REEL INFORMATION
| REEL DIMENSIONS |     |     | TAPE DIMENSIONS |     |     |     |
| --------------- | --- | --- | --------------- | --- | --- | --- |
K0  P1
W
B0
Reel
Diameter
|     |     |     | Cavity                                                    | A0  |     |     |
| --- | --- | --- | --------------------------------------------------------- | --- | --- | --- |
|     |     | A0  | Dimension designed to accommodate the component width     |     |     |     |
|     |     | B0  | Dimension designed to accommodate the component length    |     |     |     |
|     |     | K0  | Dimension designed to accommodate the component thickness |     |     |     |
|     |     | W   | Overall width of the carrier tape                         |     |     |     |
|     |     | P1  | Pitch between successive cavity centers                   |     |     |     |
Reel Width (W1)
QUADRANT ASSIGNMENTS FOR PIN 1 ORIENTATION IN TAPE
Sprocket Holes
|     |     | Q1 Q2 | Q1 Q2 |                        |     |     |
| --- | --- | ----- | ----- | ---------------------- | --- | --- |
|     |     | Q3 Q4 | Q3 Q4 | User Direction of Feed |     |     |
Pocket Quadrants

*All dimensions are nominal
| Device | Package Package | Pins | SPQ Reel Reel | A0 B0 | K0 P1 | W Pin1 |
| ------ | --------------- | ---- | ------------- | ----- | ----- | ------ |
Type Drawing Diameter Width (mm) (mm) (mm) (mm) (mm) Quadrant
|     |     |     | (mm) W1 (mm) |     |     |     |
| --- | --- | --- | ------------ | --- | --- | --- |
OPA1655DBVR SOT-23 DBV 5 3000 178.0 9.0 3.3 3.2 1.4 4.0 8.0 Q3
OPA1655DBVT SOT-23 DBV 5 250 178.0 9.0 3.3 3.2 1.4 4.0 8.0 Q3
| OPA1655DR  | SOIC | D 8 | 3000 330.0 12.4 | 6.4 5.2 | 2.1 8.0 | 12.0 Q1 |
| ---------- | ---- | --- | --------------- | ------- | ------- | ------- |
| OPA1656IDR | SOIC | D 8 | 2500 330.0 12.4 | 6.4 5.2 | 2.1 8.0 | 12.0 Q1 |
OPA1656IDRG4 SOIC D 8 2500 330.0 12.4 6.4 5.2 2.1 8.0 12.0 Q1
Pack Materials-Page 1

PACKAGE MATERIALS INFORMATION
|            |     |     |     |     |     |             |
| ---------- | --- | --- | --- | --- | --- | ----------- |
| www.ti.com |     |     |     |     |     | 10-Aug-2026 |
TAPE AND REEL BOX DIMENSIONS
Width (mm)
H
W L

*All dimensions are nominal
Device Package Type Package Drawing Pins SPQ Length (mm) Width (mm) Height (mm)
| OPA1655DBVR  | SOT-23 | DBV | 5 3000 | 190.0 | 190.0 | 30.0 |
| ------------ | ------ | --- | ------ | ----- | ----- | ---- |
| OPA1655DBVT  | SOT-23 | DBV | 5 250  | 190.0 | 190.0 | 30.0 |
| OPA1655DR    | SOIC   | D   | 8 3000 | 353.0 | 353.0 | 32.0 |
| OPA1656IDR   | SOIC   | D   | 8 2500 | 353.0 | 353.0 | 32.0 |
| OPA1656IDRG4 | SOIC   | D   | 8 2500 | 353.0 | 353.0 | 32.0 |
Pack Materials-Page 2

PACKAGE MATERIALS INFORMATION

| www.ti.com |     |     |     |     |     | 10-Aug-2026 |
| ---------- | --- | --- | --- | --- | --- | ----------- |
TUBE

T - Tube
| height |     |     | L - Tube length |     |     |     |
| ------ | --- | --- | --------------- | --- | --- | --- |
W - Tube
width
B - Alignment groove width

*All dimensions are nominal
Device Package Name Package Type Pins SPQ L (mm) W (mm) T (µm) B (mm)
| OPA1656ID   | D   | SOIC | 8 75 | 506.6 | 8 3940 | 4.32 |
| ----------- | --- | ---- | ---- | ----- | ------ | ---- |
| OPA1656ID.B | D   | SOIC | 8 75 | 506.6 | 8 3940 | 4.32 |
Pack Materials-Page 3

PACKAGE OUTLINE
DBV0005A SOT-23 - 1.45 mm max height
SCALE 4.000
SMALL OUTLINE TRANSISTOR
3.0 C
2.6
0.1 C
1.75
1.45 B A
PIN 1
INDEX AREA
1 5
2X 0.95 (0.1)
3.05
2.75
1.9 1.9
2
(0.15)
4
3
0.5
5X
0.3
0.15
0.2 C A B NOTE 5 4X 0 -15 (1.1) 0.00 TYP
1.45
0.90
4X 4 -15
0.25
GAGE PLANE 0.22
TYP
0.08
8
TYP 0.6
0 0.3 TYP SEATING PLANE
4214839/K 08/2024
NOTES:
1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. Refernce JEDEC MO-178.
4. Body dimensions do not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
exceed 0.25 mm per side.
5. Support pin may differ or may not be present.
www.ti.com

EXAMPLE BOARD LAYOUT
DBV0005A SOT-23 - 1.45 mm max height
SMALL OUTLINE TRANSISTOR
PKG
5X (1.1)
1
5
5X (0.6)
SYMM
(1.9)
2
2X (0.95)
3 4
(R0.05) TYP (2.6)
LAND PATTERN EXAMPLE
EXPOSED METAL SHOWN
SCALE:15X
SOLDER MASK
SOLDER MASK METAL UNDER
METAL OPENING
OPENING SOLDER MASK
EXPOSED METAL EXPOSED METAL
0.07 MAX 0.07 MIN
ARROUND ARROUND
NON SOLDER MASK SOLDER MASK
DEFINED DEFINED
(PREFERRED)
SOLDER MASK DETAILS
4214839/K 08/2024
NOTES: (continued)
6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
www.ti.com

EXAMPLE STENCIL DESIGN
DBV0005A SOT-23 - 1.45 mm max height
SMALL OUTLINE TRANSISTOR
PKG
5X (1.1)
1
5
5X (0.6)
SYMM
2 (1.9)
2X(0.95)
3 4
(R0.05) TYP
(2.6)
SOLDER PASTE EXAMPLE
BASED ON 0.125 mm THICK STENCIL
SCALE:15X
4214839/K 08/2024
NOTES: (continued)
8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
design recommendations.
9. Board assembly site may have different recommendations for stencil design.
www.ti.com

PACKAGE OUTLINE
D0008A SOIC - 1.75 mm max height
SCALE 2.800
SMALL OUTLINE INTEGRATED CIRCUIT
C
SEATING PLANE
.228-.244 TYP
[5.80-6.19]
.004 [0.1] C
A
PIN 1 ID AREA
6X .050
[1.27]
8
1
2X
.189-.197
[4.81-5.00] .150
NOTE 3 [3.81]
4X (0 -15 )
4
5
8X .012-.020
B .150-.157 [0.31-0.51]
.069 MAX
[3.81-3.98] .010 [0.25] C A B [1.75]
NOTE 4
.005-.010 TYP
[0.13-0.25]
4X (0 -15 )
SEE DETAIL A
.010 [0.25]
.004-.010
0 - 8
[0.11-0.25]
.016-.050
[0.41-1.27] DETAIL A
(.041) TYPICAL
[1.04]
4214825/C 02/2019
NOTES:
1. Linear dimensions are in inches [millimeters]. Dimensions in parenthesis are for reference only. Controlling dimensions are in inches.
Dimensioning and tolerancing per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
exceed .006 [0.15] per side.
4. This dimension does not include interlead flash.
5. Reference JEDEC registration MS-012, variation AA.
www.ti.com

EXAMPLE BOARD LAYOUT
D0008A SOIC - 1.75 mm max height
SMALL OUTLINE INTEGRATED CIRCUIT
8X (.061 )
[1.55]
SYMM SEE
DETAILS
1
8
8X (.024)
[0.6] SYMM
(R.002 ) TYP
[0.05]
5
4
6X (.050 )
[1.27]
(.213)
[5.4]
LAND PATTERN EXAMPLE
EXPOSED METAL SHOWN
SCALE:8X
SOLDER MASK SOLDER MASK
METAL OPENING OPENING METAL UNDER
SOLDER MASK
EXPOSED
METAL EXPOSED
METAL
.0028 MAX .0028 MIN
[0.07] [0.07]
ALL AROUND ALL AROUND
NON SOLDER MASK SOLDER MASK
DEFINED DEFINED
SOLDER MASK DETAILS
4214825/C 02/2019
NOTES: (continued)
6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
www.ti.com

EXAMPLE STENCIL DESIGN
D0008A SOIC - 1.75 mm max height
SMALL OUTLINE INTEGRATED CIRCUIT
8X (.061 )
[1.55] SYMM
1
8
8X (.024)
[0.6]
SYMM
(R.002 ) TYP
[0.05]
5
4
6X (.050 )
[1.27]
(.213)
[5.4]
SOLDER PASTE EXAMPLE
BASED ON .005 INCH [0.125 MM] THICK STENCIL
SCALE:8X
4214825/C 02/2019
NOTES: (continued)
8. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
design recommendations.
9. Board assembly site may have different recommendations for stencil design.
www.ti.com

IMPORTANT NOTICE AND DISCLAIMER
TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATASHEETS), DESIGN RESOURCES (INCLUDING REFERENCE
DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS”
AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD
PARTY INTELLECTUAL PROPERTY RIGHTS.
These resources are intended for skilled developers designing with TI products. You are solely responsible for (1) selecting the appropriate
TI products for your application, (2) designing, validating and testing your application, and (3) ensuring your application meets applicable
standards, and any other safety, security, regulatory or other requirements.
These resources are subject to change without notice. TI grants you permission to use these resources only for development of an
application that uses the TI products described in the resource. Other reproduction and display of these resources is prohibited. No license
is granted to any other TI intellectual property right or to any third party intellectual property right. TI disclaims responsibility for, and you fully
indemnify TI and its representatives against any claims, damages, costs, losses, and liabilities arising out of your use of these resources.
TI’s products are provided subject to TI’s Terms of Sale, TI’s General Quality Guidelines, or other applicable terms available either on
ti.com or provided in conjunction with such TI products. TI’s provision of these resources does not expand or otherwise alter TI’s applicable
warranties or warranty disclaimers for TI products. Unless TI explicitly designates a product as custom or customer-specified, TI products
are standard, catalog, general purpose devices.
TI objects to and rejects any additional or different terms you may propose.
IMPORTANT NOTICE
Copyright © 2026, Texas Instruments Incorporated
Last updated 10/2025
