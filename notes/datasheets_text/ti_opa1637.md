OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUOGPUAST1 2603270
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
OPA1637 High-Fidelity, Low-Noise, Fully-Differential, Burr-Brown™ Audio
Operational Amplifier
| 1 Features |     |     | 3 Description |     |     |
| ---------- | --- | --- | ------------- | --- | --- |
• Low input voltage noise: 3.7 nV/?Hz at 1 kHz The OPA1637 is a low-noise, low total harmonic
distortion (THD), fully differential, Burr-Brown™ Audio
• Low THD + N: –120 dB at 1 kHz
operational amplifier that easily filters and drives fully
• Low supply current: 950 µA at ±18 V
differential, audio signal chains.
• Input offset voltage: ±200 µV (maximum)
• Input bias current: 2 nA (maximum) The OPA1637 also converts single-ended sources to
differential outputs required by high-fidelity analog-to-
• Low bias current noise: 400 fA/?Hz at 10 Hz
• Gain-bandwidth product: 9.2 MHz digital converters (ADCs). Designed for exceptional
low noise and THD, the bipolar super-beta inputs yield
• Differential output slew rate: 15 V/µs
a very low noise figure at very-low quiescent current
• Wide input and output common-mode range
and input bias current. This device is designed for
• Wide single-supply operating range: 3 V to 36 V
audio circuits where low power consumption is
• Low supply current power-down feature: < 20 µA
required along with excellent signal-to-noise ratio
• Overload power limit (SNR) and spurious-free dynamic range (SFDR).
• Current limit
The OPA1637 features high-voltage supply capability,
• Package: 8-pin VSSOP
allowing for supply voltages up to ±18 V. This
• Temperature range: –40°C to +125°C
capability allows high-voltage differential signal chains
2 Applications to benefit from the improved headroom and dynamic
range without adding separate amplifiers for each
• Professional audio mixer or control surface
polarity of the differential signal. Very-low voltage and
• Professional microphones and wireless systems current noise enables the OPA1637 for use in high-
• Professional speaker systems gain configurations with minimal impact to the audio
| • Professional audio amplifier |     |     | signal noise. |     |     |
| ------------------------------ | --- | --- | ------------- | --- | --- |
• Soundbar
The OPA1637 is characterized for operation over the
• Turntable wide temperature range of –40°C to +125°C, and is
• Professional video camera available in an 8-pin VSSOP package.
• Guitar and other instrument amplifier
Device Information (1)
• Data aquisition (DAQ)
|     |     |     | PART NUMBER | PACKAGE   | BODY SIZE (NOM)   |
| --- | --- | --- | ----------- | --------- | ----------------- |
|     |     |     | OPA1637     | VSSOP (8) | 3.00 mm × 3.00 mm |
(1) For all available packages, see the package option
addendum at the end of the datasheet.
|     | R  kF(cid:13)1  |     | 100 |     |     |
| --- | --------------- | --- | --- | --- | --- |
1
70
|     | C   |     | )zH—/Vn( ytisneD esioN egatloV 50 |     |     |
| --- | --- | --- | --------------------------------- | --- | --- |
3 . 3  Fn1F C
|     |     | R 75IS O(cid:13)1 1  µ2F | 30  |     |     |
| --- | --- | ------------------------ | --- | --- | --- |
R 49I1 (cid:13)
|                   | 5 V 5   V                          | INPUT_A                     | 20  |     |     |
| ----------------- | ---------------------------------- | --------------------------- | --- | --- | --- |
|                   | ±                                  | TPA3251                     |     |     |     |
| P C M 1 7 95 I    | O U T L / R + ± 3.5 V O PA163 + ±7 | C 10D  Fn C la s s   D erC  | 10  |     |     |
| A u d io  D A C I | O U T L / R ±   1 µ C F5           | F A m pA l ifD i            | 7   |     |     |
|                   | + PD                               | 1 C  µ 3F                   |     |     |     |
|                   | GND ±10 V ±10 V5 V                 |                             | 5   |     |     |
|                   | R 49I2 (cid:13)                    | INPUT_B                     |     |     |     |
|                   |                                    | R 75IS O(cid:13)2           | 3   |     |     |
C 3 Fn2F 2
1 R  kF(cid:13)2 3.
GND
1
Low-Noise, Low-Power, Fully-Differential Amplifier 100m 1 10 100 1k 10k 100k
Frequency (Hz)
|     | Gain Block and Interface |     |     |     | D022 |
| --- | ------------------------ | --- | --- | --- | ---- |
Low Input Voltage Noise
An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,
Copyrighint t©e l2le0c2t0u Tael xparso Ipnesrtrtuym meanttste Irnsc oarnpdor aottehder important disclaimers. PRODUCTION DATA. Submit Document Feedback 1
Product Folder Links: OPA1637

OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
Table of Contents
1 Features............................................................................1 8.4 Device Functional Modes..........................................17
2 Applications.....................................................................1 9 Application and Implementation..................................18
3 Description.......................................................................1 9.1 Application Information.............................................18
4 Revision History..............................................................2 9.2 Typical Applications..................................................22
5 Pin Configuration and Functions...................................3 10 Power Supply Recommendations..............................27
6 Specifications..................................................................4 11 Layout...........................................................................27
6.1 Absolute Maximum Ratings........................................4 11.1 Layout Guidelines...................................................27
6.2 ESD Ratings...............................................................4 11.2 Layout Example......................................................27
6.3 Recommended Operating Conditions.........................4 12 Device and Documentation Support..........................28
6.4 Thermal Information....................................................4 12.1 Device Support.......................................................28
6.5 Electrical Characteristics.............................................5 12.2 Documentation Support..........................................28
6.6 Typical Characteristics................................................8 12.3 Receiving Notification of Documentation Updates..28
7 Parameter Measurement Information..........................15 12.4 Support Resources.................................................28
7.1 Characterization Configuration.................................15 12.5 Trademarks.............................................................28
8 Detailed Description......................................................16 12.6 Electrostatic Discharge Caution..............................28
8.1 Overview...................................................................16 12.7 Glossary..................................................................28
8.2 Functional Block Diagram.........................................16 13 Mechanical, Packaging, and Orderable
8.3 Feature Description...................................................17 Information....................................................................28
4 Revision History
NOTE: Page numbers for previous revisions may differ from page numbers in the current version.
Changes from Revision A (May 2020) to Revision B (August 2020) Page
• Updated the numbering format for tables, figures, and cross-references throughout the document..................1
• Changed front page application diagram to show correct label and value for R ............................................1
F1
• Changed Figure 7-1 to show correct labels......................................................................................................15
• Changed Figure 9-5 to show correct label and value for R ..........................................................................22
F1
• Changed Figure 9-8 negative rail from 0 V to –5 V..........................................................................................24
Changes from Revision * (December 2019) to Revision A (May 2020) Page
• Changed device status from advanced information (preview) to production data (active) ................................1
2 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
5 Pin Configuration and Functions
IN- 1 8 IN+
VOCM 2 7 PD
VS+ 3 6 VS-
OUT+ 4 5 OUT-
Figure 5-1. DGK Package, 8-Pin VSSOP, Top View
Pin Functions
PIN
I/O DESCRIPTION
| NAME | NO. |                                            |
| ---- | --- | ------------------------------------------ |
| IN–  | 1   | I Inverting (negative) amplifier input     |
| IN+  | 8   | I Noninverting (positive) amplifier input  |
| OUT– | 5   | O Inverting (negative) amplifier output    |
| OUT+ | 4   | O Noninverting (positive) amplifier output |
Power down.
PD = logic low = power off mode.
| PD  | 7   | I PD = logic high = normal operation. |
| --- | --- | ------------------------------------- |
The logic threshold is referenced to VS+.
If power down is not needed, leave PD floating.
| VOCM | 2   | I Ouput common-mode voltage control input |
| ---- | --- | ----------------------------------------- |
| VS–  | 6   | I Negative power-supply input             |
| VS+  | 3   | I Positive power-supply input             |
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 3
Product Folder Links: OPA1637

OPA1637
| SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | ---------- |
6 Specifications
6.1 Absolute Maximum Ratings
over operating free-air temperature range (unless otherwise noted)(1)
|     |                                   |     |               |     | MIN | MAX UNIT |
| --- | --------------------------------- | --- | ------------- | --- | --- | -------- |
|     |                                   |     | Single supply |     |     | 40 V     |
| VS  | Supply voltage                    |     |               |     |     |          |
|     |                                   |     | Dual supply   |     |     | ±20 V    |
|     | IN+, IN–, Differential voltage(2) |     |               |     |     | ±0.5 V   |
IN+, IN–, VOCM, PD, OUT+, OUT? voltage(3) VVS– – 0.5 VVS+ + 0.5 V
|      | IN+, IN? current        |     |     |     | –10 | 10 mA      |
| ---- | ----------------------- | --- | --- | --- | --- | ---------- |
|      | OUT+, OUT? current      |     |     |     | –50 | 50 mA      |
|      | Output short-circuit(4) |     |     |     |     | Continuous |
| TA   | Operating Temperature   |     |     |     | –40 | 150 °C     |
| TJ   | Junction Temperature    |     |     |     | –40 | 175 °C     |
| Tstg | Storage Temperature     |     |     |     | –65 | 150 °C     |
(1) Stresses beyond those listed under Absolute Maximum Ratings may cause permanent damage to the device. These are stress ratings
only, which do not imply functional operation of the device at these or any other conditions beyond those indicated under
Recommended Operating Conditions. Exposure to absolute-maximum-rated conditions for extended periods may affect device
reliability.
(2) Input pins IN+ and IN– are connected with anti-parallel diodes in between the two terminals.  Differential input signals that are greater
than 0.5 V or less than –0.5 V must be current-limited to 10 mA or less.
(3) Input terminals are diode-clamped to the supply rails (VS+, VS–). Input signals that swing more than 0.5 V greater or less the supply
rails must be current-limited to 10 mA or less.
| (4) Short-circuit to V | S  / 2. |     |     |     |     |     |
| ---------------------- | ------- | --- | --- | --- | --- | --- |
6.2 ESD Ratings
VALUE UNIT
|     |                         | Human body model (HBM), per ANSI/ESDA/JEDEC JS-001(1) |     |     |     | ±1000 |
| --- | ----------------------- | ----------------------------------------------------- | --- | --- | --- | ----- |
| V   | Electrostatic discharge |                                                       |     |     |     | V     |
(ESD)
|     |     | Charged device model (CDM), per JEDEC specification JESD22-C101(2) |     |     |     | ±500 |
| --- | --- | ------------------------------------------------------------------ | --- | --- | --- | ---- |
(1) JEDEC document JEP155 states that 500-V HBM allows safe manufacturing with a standard ESD control process.
(2) JEDEC document JEP157 states that 250-V CDM allows safe manufacturing with a standard ESD control process.
6.3 Recommended Operating Conditions
over operating free-air temperature range (unless otherwise noted)
|     |                |     |               | MIN | NOM | MAX UNIT |
| --- | -------------- | --- | ------------- | --- | --- | -------- |
|     |                |     | Single-supply | 3   |     | 36       |
| V   | Supply voltage |     |               |     |     | V        |
S
|     |                       |     | Dual-supply | ±1.5 |     | ±18    |
| --- | --------------------- | --- | ----------- | ---- | --- | ------ |
| T   | Specified temperature |     |             | –40  |     | 125 °C |
A
6.4 Thermal Information
OPA1637
|     |     | THERMAL METRIC(1) |     |     | DGK (VSSOP) | UNIT |
| --- | --- | ----------------- | --- | --- | ----------- | ---- |
8 PINS
| R   | Junction-to-ambient thermal resistance |     |     |     | 181.1 | °C/W |
| --- | -------------------------------------- | --- | --- | --- | ----- | ---- |
?JA
R ?JC(top) Junction-to-case (top) thermal resistance 68.3 °C/W
| R   | Junction-to-board thermal resistance |     |     |     | 102.8 | °C/W |
| --- | ------------------------------------ | --- | --- | --- | ----- | ---- |
?JB
| ?   | Junction-to-top characterization parameter |     |     |     | 10.6 | °C/W |
| --- | ------------------------------------------ | --- | --- | --- | ---- | ---- |
JT
| ?   | Junction-to-board characterization parameter |     |     |     | 101.1 | °C/W |
| --- | -------------------------------------------- | --- | --- | --- | ----- | ---- |
JB
R ?JC(bot) Junction-to-case (bottom) thermal resistance N/A °C/W
(1) For information about traditional and new thermal metrics, see the Semiconductor and IC Package Thermal Metrics application report.
4 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
6.5 Electrical Characteristics
at T  = 25°C, V  (dual supply) = ±1.5 V to ±18 V, V  = 0 V, input common mode voltage (V ) = 0 V, R  = 2
| A   | S   |     | VOCM |     |     | ICM |     | F   |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- |
 = 10 k?(1) (unless otherwise noted)
| k?, V | = V , R    |     |                 |     |     |     |     |      |
| ----- | ---------- | --- | --------------- | --- | --- | --- | --- | ---- |
|       |  PD  VS+ L |     |                 |     |     |     |     |      |
|       | PARAMETER  |     | TEST CONDITIONS |     | MIN | TYP | MAX | UNIT |
FREQUENCY RESPONSE
SSBW Small-signal bandwidth V  (2) = 100 mV , G = –1 V/V 7 MHz
|     |                        | O                                  | PP              |              |     |     |     |      |
| --- | ---------------------- | ---------------------------------- | --------------- | ------------ | --- | --- | --- | ---- |
| GBP | Gain-bandwidth product | V  = 100 mV                        | , G = –10 V/V   |              |     | 9.2 |     | MHz  |
|     |                        | O                                  | PP              |              |     |     |     |      |
| FBP | Full-power bandwidth   | V O  = –1 V                        | PP , G = –1 V/V |              |     | 2.5 |     | MHz  |
| SR  | Slew rate              | G = –1, 10-V step                  |                 |              |     | 15  |     | V/µs |
|     |                        | 0.1% of final value, G = –1 V/V, V |                 |  = 10-V step |     | 1   |     |      |
O
|     | Settling time |                                     |     |             |     |     |     | µs  |
| --- | ------------- | ----------------------------------- | --- | ----------- | --- | --- | --- | --- |
|     |               | 0.01% of final value, G = –1 V/V, V |     | = 10-V step |     | 2   |     |     |
O
|     |     |                                  |     |         |     | –120 |     | dB  |
| --- | --- | -------------------------------- | --- | ------- | --- | ---- | --- | --- |
|     |     | Differential input, f = 1 kHz, V |     |  = 10 V |     |      |     |     |
O PP
|     |     |                                  |     |         |     | 0.0001  |     | %   |
| --- | --- | -------------------------------- | --- | ------- | --- | ------- | --- | --- |
|     |     |                                  |     |         |     | –115    |     | dB  |
|     |     | Single-ended input, f = 1 kHz, V |     |  = 10 V |     |         |     |     |
|     |     |                                  |     | O PP    |     | 0.00018 |     | %   |
Total harmonic distortion and
THD+N
|     | noise |                                   |     |         |     | –112 |     | dB  |
| --- | ----- | --------------------------------- | --- | ------- | --- | ---- | --- | --- |
|     |       | Differential input, f = 10 kHz, V |     |  = 10 V |     |      |     |     |
O PP
|     |     |                                   |     |         |     | 0.00025 |     | %   |
| --- | --- | --------------------------------- | --- | ------- | --- | ------- | --- | --- |
|     |     |                                   |     |         |     | –107    |     | dB  |
|     |     | Single-ended input, f = 10 kHz, V |     |  = 10 V |     |         |     |     |
|     |     |                                   |     | O PP    |     | 0.00045 |     | %   |
|     |     | Differential input, f = 1 kHz, V  |     |  = 10 V |     | –126    |     |     |
O PP
| HD2 | Second-order harmonic distortion |                                  |     |         |     |      |     | dB  |
| --- | -------------------------------- | -------------------------------- | --- | ------- | --- | ---- | --- | --- |
|     |                                  | Single-ended input, f = 1 kHz, V |     |  = 10 V |     | –120 |     |     |
O PP
|     |                                 | Differential input, f = 1 kHz, V |     | O  = 10 V PP |     | –131 |     |     |
| --- | ------------------------------- | -------------------------------- | --- | ------------ | --- | ---- | --- | --- |
| HD3 | Third-order harmonic distortion |                                  |     |              |     |      |     | dB  |
|     |                                 | Single-ended input, f = 1 kHz, V |     | O  = 10 V PP |     | –119 |     |     |
Overdrive recovery time G = 5 V/V, 2x output overdrive, dc-coupled 3.3 µs
NOISE
|     |     | f = 1 kHz |     |     |     | 3.7 |     |     |
| --- | --- | --------- | --- | --- | --- | --- | --- | --- |
nV/? Hz
| e n | Input differential voltage noise | f = 10 Hz           |     |     |     | 4   |     |       |
| --- | -------------------------------- | ------------------- | --- | --- | --- | --- | --- | ----- |
|     |                                  | f = 0.1 Hz to 10 Hz |     |     |     | 0.1 |     | µV PP |
|     |                                  | f = 1 kHz           |     |     |     | 300 |     |       |
fA/? Hz
| e   | Input current noise, each input | f = 10 Hz |     |     |     | 400 |     |     |
| --- | ------------------------------- | --------- | --- | --- | --- | --- | --- | --- |
i
|     |     | f = 0.1 Hz to 10 Hz |     |     |     | 13.4 |     | pA  |
| --- | --- | ------------------- | --- | --- | --- | ---- | --- | --- |
PP
OFFSET VOLTAGE
20 ±200
| V   | Input-referred offset voltage |                      |     |     |     |     |      | µV  |
| --- | ----------------------------- | -------------------- | --- | --- | --- | --- | ---- | --- |
| IO  |                               | T  = –40°C to +125°C |     |     |     |     | ±250 |     |
A
|     | Input offset voltage drift | T  = –40°C to +125°C |     |     |     | 0.1 |     | ±1 µV/°C |
| --- | -------------------------- | -------------------- | --- | --- | --- | --- | --- | -------- |
A
|      |                              |                        |     |     |     | 0.025 | ±0.5 |      |
| ---- | ---------------------------- | ---------------------- | --- | --- | --- | ----- | ---- | ---- |
| PSRR | Power-supply rejection ratio |                        |     |     |     |       |      | µV/V |
|      |                              | T A  = –40°C to +125°C |     |     |     |       |      | ±1   |
INPUT BIAS CURRENT
|     |                    |                      |     |     |     | 0.2 |     | ±2  |
| --- | ------------------ | -------------------- | --- | --- | --- | --- | --- | --- |
| I B | Input bias current |                      |     |     |     |     |     | nA  |
|     |                    | T  = –40°C to +125°C |     |     |     |     |     | ±4  |
A
|     | Input bias current drift | T A  = –40°C to +125°C |     |     |     | 2   | ±15 | pA/°C |
| --- | ------------------------ | ---------------------- | --- | --- | --- | --- | --- | ----- |
|     | Input offset current     |                        |     |     |     | 0.2 |     | ±1    |
| I   |                          |                        |     |     |     |     |     | nA    |
| OS  |                          | T  = –40°C to +125°C   |     |     |     |     |     | ±3    |
A
|     | Input offset current drift | T  = –40°C to +125°C |     |     |     | 1   | ±10 | pA/°C |
| --- | -------------------------- | -------------------- | --- | --- | --- | --- | --- | ----- |
A
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 5
Product Folder Links: OPA1637

OPA1637
| SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |     |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- |
6.5 Electrical Characteristics (continued)
at T A  = 25°C, V S  (dual supply) = ±1.5 V to ±18 V, V VOCM  = 0 V, input common mode voltage (V ICM ) = 0 V, R F  = 2
| k?, V | = V , R  = 10 k?(1) (unless otherwise noted) |     |                 |     |     |     |     |     |     |      |
| ----- | -------------------------------------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | ---- |
|       |  PD  VS+ L                                   |     |                 |     |     |     |     |     |     |      |
|       | PARAMETER                                    |     | TEST CONDITIONS |     |     |     | MIN | TYP | MAX | UNIT |
INPUT VOLTAGE
|      | Common-mode voltage         | T  = –40°C to +125°C |     |       |          |          | V + 1 |     | V   |  – 1 V |
| ---- | --------------------------- | -------------------- | --- | ----- | -------- | -------- | ----- | --- | --- | ------ |
|      |                             | A                    |     |       |          |          | VS–   |     | VS+ |        |
|      |                             | V + 1 V ? V          |     |  ?  V | – 1 V    |          |       | 140 |     |        |
|      |                             | VS–                  | ICM | VS+   |          |          |       |     |     |        |
|      |                             | V + 1 V ? V          |     |  ?  V | – 1 V, V |  = ±18 V | 126   | 140 |     |        |
| CMRR | Common-mode rejection ratio | VS–                  | ICM | VS+   |          | S        |       |     |     |        |
dB
|     |     | V VS–  + 1 V ? V | ICM |  ? V VS+ |  – 1 V, V | S  = ±18 V |     |     |     |     |
| --- | --- | ---------------- | --- | -------- | --------- | ---------- | --- | --- | --- | --- |
120
T A  = –40°C to   +125°C
INPUT IMPEDANCE
Input impedance differential
|     |      | V  = 0 V |     |     |     |     |     | 1 || 1 |     | G? || pF |
| --- | ---- | -------- | --- | --- | --- | --- | --- | ------ | --- | -------- |
|     | mode | ICM      |     |     |     |     |     |        |     |          |
OPEN-LOOP GAIN
|     |     | V S  = ±2.5 V, V     | VS– |  + 0.2 V < V | O  <  V | VS+  – 0.2 V  | 115 | 120 |     |     |
| --- | --- | -------------------- | --- | ------------ | ------- | ------------- | --- | --- | --- | --- |
|     |     | V S  = ±2.5 V, V     | VS– |  + 0.3 V < V | O  < V  | VS+  – 0.3 V, |     |     |     |     |
|     |     | T  = –40°C to +125°C |     |              |         |               | 110 | 120 |     |     |
A
| A OL | Open-loop voltage gain |               |      |              |      |           |     |     |     | dB  |
| ---- | ---------------------- | ------------- | ---- | ------------ | ---- | --------- | --- | --- | --- | --- |
|      |                        | V  = ±15 V, V |      |  + 0.6 V < V |  < V |  – 0.6 V  | 115 | 120 |     |     |
|      |                        | S             | VS–  |              | O    | VS+       |     |     |     |     |
|      |                        | V  = ±15 V, V |      | + 0.6 V < V  |  < V |  – 0.6 V, |     |     |     |     |
|      |                        | S             | VS–  |              | O    | VS+       | 110 | 120 |     |     |
T  = –40°C to +125°C
A
OUTPUT
|     |                                | V S  = ±2.5 V  |                    |     |     |     |     | ±100 |     |     |
| --- | ------------------------------ | -------------- | ------------------ | --- | --- | --- | --- | ---- | --- | --- |
|     |                                | V  = ±2.5 V, T |  = –40°C to +125°C |     |     |     |     | ±100 |     |     |
|     | Output voltage difference from | S              | A                  |     |     |     |     |      |     |     |
mV
|     | supply voltage | V  = ±18 V |     |     |     |     |     | ±230 |     |     |
| --- | -------------- | ---------- | --- | --- | --- | --- | --- | ---- | --- | --- |
S
|      |                       | V  = ±18 V, T |  = –40°C to +125°C |     |     |     |     | ±270 |     |     |
| ---- | --------------------- | ------------- | ------------------ | --- | --- | --- | --- | ---- | --- | --- |
|      |                       | S             | A                  |     |     |     |     |      |     |     |
| I SC | Short-circuit current |               |                    |     |     |     |     | ±31  |     | mA  |
Differential capacitive load, no output Isolation
| C    | Capacitive load drive      |                               |     |     |     |     |     |     | 50  | pF  |
| ---- | -------------------------- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOAD |                            | resistors, phase margin = 30° |     |     |     |     |     |     |     |     |
| Z    | Open-loop output impedance | f = 100 kHz (differential)    |     |     |     |     |     |     | 14  | ?   |
O
| OUTPUT COMMON-MODE VOLTAGE (V |     | ) CONTROL |     |     |     |     |     |     |     |     |
| ----------------------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
OCM
|     |     | V S  = ±2.5 V |     |     |     |     | V VS–  + 1 |     | V VS+ |  – 1 |
| --- | --- | ------------- | --- | --- | --- | --- | ---------- | --- | ----- | ---- |
Input Voltage Range
|     |     | V S  = ±18 V |     |     |     |     | V VS–  + 2 |     | V VS+ |  – 2 |
| --- | --- | ------------ | --- | --- | --- | --- | ---------- | --- | ----- | ---- |
Small-signal bandwidth from
|     |          | V = 100 mV |     |     |     |     |     |     | 2   |     |
| --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | VOCM pin | VOCM       | PP  |     |     |     |     |     |     |     |
MHz
Large-signal bandwidth from
|     |                             | V  = 0.6 V                    |     |     |          |     |     |          | 5.7 |          |
| --- | --------------------------- | ----------------------------- | --- | --- | -------- | --- | --- | -------- | --- | -------- |
|     | VOCM pin                    | VOCM                          | PP  |     |          |     |     |          |     |          |
|     |                             | V VOCM  = 0.5-V step, rising  |     |     |          |     |     |          | 3.5 |          |
|     | Slew rate from VOCM pin     |                               |     |     |          |     |     |          |     | V/µs     |
|     |                             | V VOCM  = 0.5-V step, falling |     |     |          |     |     |          | 5.5 |          |
|     | DC output balance           | V  fixed midsupply (V         |     |     |  = ±1 V) |     |     |          | 78  | dB       |
|     |                             | VOCM                          |     |     | O        |     |     |          |     |          |
|     | VOCM input impedance        |                               |     |     |          |     |     | 2.5 || 1 |     | M? || pF |
|     | VOCM offset from mid-supply | VOCMpin floating              |     |     |          |     |     |          | 2   | mV       |

|     | VOCM common-mode offset | V VOCM  = V | ICM , V O |  = 0 V |     |     |     |     | ±1  | ±6  |
| --- | ----------------------- | ----------- | --------- | ------ | --- | --- | --- | --- | --- | --- |
mV
voltage
|     |     | V VOCM  = V | ICM , V O |  = 0 V, T | A  = –40°C to +125°C |     |     |     |     | ±10 |
| --- | --- | ----------- | --------- | --------- | -------------------- | --- | --- | --- | --- | --- |
VOCM common-mode offset
|     |               | V  = V | , V   |  = 0 V, T |  = –40°C to +125°C |     |     | ±20 |     | ±60 µV/°C |
| --- | ------------- | ------ | ----- | --------- | ------------------ | --- | --- | --- | --- | --------- |
|     | voltage drift | VOCM   | ICM O |           | A                  |     |     |     |     |           |
POWER SUPPLY
|     |                             |     |     |     |     |     |     | 0.95 |     | 1.2 |
| --- | --------------------------- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
| I   | Quiescent operating current |     |     |     |     |     |     |      |     | mA  |
Q
|     |     | T A  = –40°C to +125°C |     |     |     |     |     |     |     | 1.6 |
| --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
6 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
6.5 Electrical Characteristics (continued)
at T A  = 25°C, V S  (dual supply) = ±1.5 V to ±18 V, V VOCM  = 0 V, input common mode voltage (V ICM ) = 0 V, R F  = 2
| k?, V | = V , R  = 10 k?(1) (unless otherwise noted) |     |                 |     |         |      |
| ----- | -------------------------------------------- | --- | --------------- | --- | ------- | ---- |
|  PD   | VS+ L                                        |     |                 |     |         |      |
|       | PARAMETER                                    |     | TEST CONDITIONS | MIN | TYP MAX | UNIT |
POWER DOWN
V  –
| V       | Power-down enable voltage | T  = –40°C to +125°C |     | VS+ |     | V   |
| ------- | ------------------------- | -------------------- | --- | --- | --- | --- |
|  PD(HI) |                           | A                    |     | 0.5 |     |     |
V  –
| V        | Power-down disable voltage  | T  = –40°C to +125°C |            |     | VS+   | V   |
| -------- | --------------------------- | -------------------- | ---------- | --- | ----- | --- |
|  PD(LOW) |                             | A                    |            |     | 2.0   |     |
|          | PD bias current             | V  PD   =  V         | VS+  – 2 V |     | 1 2   | µA  |
|          | Powerdown quiescent current |                      |            |     | 10 20 | µA  |
Turn-on time delay V  = 100 mV, time to V  = 90% of final value 10 µs
|     |     | IN  | O   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Turn-off time delay V  = 100 mV, time to V  = 10% of original value 15 µs
|     |     | IN  | O   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
(1) R  is connected differentially, from OUT+ to OUT–.
L
| (2) V  refers to the differential output voltage, V |     |  –  V | .    |     |     |     |
| --------------------------------------------------- | --- | ----- | ---- | --- | --- | --- |
| O                                                   |     | OUT+  | OUT– |     |     |     |
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 7
Product Folder Links: OPA1637

OPA1637
| SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |     |     |     |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- |
6.6 Typical Characteristics
at V  = ±18 V, T  = 25°C, V  = V  = 0 V, R  = 2 k?, R  = 10 k?, V  = 2 V , G = 1 V/V, and V PD = VS
|     | S   | A   | VOCM | VICM | F   | L   | OUT | PP  |     |     |
| --- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- |
+ (unless otherwise noted)
|                                       | 100 |     |     |     |                                       | 5000 |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | ------------------------------------- | ---- | --- | --- | --- | --- |
| )zH—/Vn( esioN egatloV derrefeR-tupnI | 70  |     |     |     | )zH—/Af( esioN tnerruC derrefeR-tupnI |      |     |     |     |     |
|                                       | 50  |     |     |     |                                       | 3000 |     |     |     |     |
2000
30
20
1000
|     | 10  |     |     |     |     | 700 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
7
500
5
300
3
200
2
100
1
100m 1 10 100 1k 10k 100k 0.1 0.5 23 5 1020 100 1000 10000 100000
Frequency (Hz)
|     |     |     | Frequency (Hz) |     |     |     |     |     |     | D014 |
| --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | ---- |
D013
Figure 6-1. Input-Referred Voltage Noise vs Figure 6-2. Current Noise vs Frequency
Frequency
|     | -90 |     |     |     |     | 0.1 |     |     |     | -60 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
)Bd( esioN (cid:14) noitrotsiD cinomraH latoT RL = 2 k: RL = 2 k: )Bd( esioN + noitrotsiD cinomraH latoT
R   =   1 0   k : )%( esioN (cid:14) noitrotsiD cinomraH latoT RL = 10 k:
|     | -95 | L :               |     |     |     |      |     |     |     |     |
| --- | --- | ----------------- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     |     | R L   =   6 0 0   |     |     |     |      |     |     |     |     |
|     |     |                   |     |     |     | 0.01 |     |     |     | -80 |
-100
-105
|     |     |     |     |     |     | 0.001 |     |     |     | -100 |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ---- |
-110
-115
|     |     |     |     |     |     | 0.0001 |     |     |     | -120 |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | ---- |
-120
|     |     |     |     |     |     | 1E-5 |     |     |     | -140 |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ---- |
-125
|     |     |     |                |         |     | 10m | 100m                    |     | 1   | 10   |
| --- | --- | --- | -------------- | ------- | --- | --- | ----------------------- | --- | --- | ---- |
|     | 10  | 100 | 1k             | 10k 20k |     |     | Output Amplitude (VRMS) |     |     |      |
|     |     |     | Frequency (Hz) |         |     |     |                         |     |     | D016 |
D015
|     |     |          |              |     |     |     | f = 1 kHz, V |  = ±15 V |     |     |
| --- | --- | -------- | ------------ | --- | --- | --- | ------------ | -------- | --- | --- |
|     |     | V  = 3 V | , V  = ±15 V |     |     |     |              | S        |     |     |
|     |     | OUT      | RMS S        |     |     |     |              |          |     |     |
Figure 6-4. Total Harmonic Noise + Distortion vs
Figure 6-3. Total Harmonic Distortion + Noise vs
Amplitude
Frequency
|     | 180 |     |     |     | 200 | 50  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Gain
|     | 160 |     |     | Phase | 160 |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
40
|           | 140 |     |     |     | 120       |              |     |     |     |     |
| --------- | --- | --- | --- | --- | --------- | ------------ | --- | --- | --- | --- |
|           | 120 |     |     |     | 80        | 30           |     |     |     |     |
|           | 100 |     |     |     | 40        |              |     |     |     |     |
| )Bd( niaG |     |     |     |     | Phase (q) | )Bd( niaG 20 |     |     |     |     |
|           | 80  |     |     |     | 0         |              |     |     |     |     |
|           | 60  |     |     |     | -40       | 10           |     |     |     |     |
|           | 40  |     |     |     | -80       | 0            |     |     |     |     |
|           | 20  |     |     |     | -120      |              |     |     |     |     |
G = 1
-10 G = 10
|     | 0   |     |     |     | -160 |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
G = 100
|     | -20 |               |                |     | -200 | -20 |               |                |          |      |
| --- | --- | ------------- | -------------- | --- | ---- | --- | ------------- | -------------- | -------- | ---- |
|     |     | 1 10 100      | 1k 10k 100k    | 1M  | 10M  | 1k  | 10k           | 100k           | 1M       | 10M  |
|     |     |               | Frequency (Hz) |     |      |     |               | Frequency (Hz) |          |      |
|     |     |               |                |     | D068 |     |               |                |          | D009 |
|     |     | V  = ±15 V, C |  = 50 pF       |     |      |     | V  = ±15 V, C |                |  = 50 pF |      |
|     |     | S             | L              |     |      |     | S             | L              |          |      |
Figure 6-5. Open Loop Gain vs Frequency Figure 6-6. Closed-Loop Gain vs Frequency
8 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
| www.ti.com |     |     |     | SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |     |
| ---------- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- |
| 180        |     |     |     | 0.09                                           |     |     |     |
)V/VP( oitaR noitcejeR edoM-nommoC
| )Bd( oitaR noitcejeR edoM-nommoC 160 |     |     |     | 0.08 |     |     |     |
| ------------------------------------ | --- | --- | --- | ---- | --- | --- | --- |
140
0.07
120
0.06
100
0.05
80
0.04
60
0.03
40
0.02
20
0.01
0
10m 100m 1 10 100 1k 10k 100k 1M 10M -40 -25 -10 5 20 35 50 65 80 95 110 125
Temperature (oC)
|     | Frequency (Hz) |     |     |     |     |     | D030 |
| --- | -------------- | --- | --- | --- | --- | --- | ---- |
D011
|     | V  = ±15 V |     |     |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- |
S
Figure 6-8. Common Mode Rejection Ratio vs
Figure 6-7. Common Mode Rejection Ratio vs
|     | Frequency |     |     |       | Temperature |     |     |
| --- | --------- | --- | --- | ----- | ----------- | --- | --- |
| 180 |           |     |     | -0.01 |             |     |     |
PSRR(cid:14)
|     |     |     | PSRR(cid:16) )V/VP( oitaR noitcejeR ylppuS rewoP |     |     |     |     |
| --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- |
)Bd( oitaR noitcejeR ylppuS rewoP 160
140
-0.02
120
100
-0.03
80
60
-0.04
40
20
| 0        |                |        |             | -0.05   |                  |          |            |
| -------- | -------------- | ------ | ----------- | ------- | ---------------- | -------- | ---------- |
|          |                |        |             | -40 -25 | -10 5 20 35      | 50 65 80 | 95 110 125 |
| 10m 100m | 1 10 100       | 1k 10k | 100k 1M 10M |         |                  |          |            |
|          | Frequency (Hz) |        |             |         | Temperature (oC) |          |            |
|          |                |        | D012        |         |                  |          | D031       |

V S  = ±15 V
Figure 6-9. Power Supply Rejection Ratio vs Figure 6-10. Power Supply Rejection Ratio vs
|                              | Frequency |     |                                              |       | Temperature |     |     |
| ---------------------------- | --------- | --- | -------------------------------------------- | ----- | ----------- | --- | --- |
| 40                           |           |     |                                              | 10000 |             |     |     |
| 35                           |           |     |                                              | 5000  |             |     |     |
| )PPV( egatloV tuptuO mumixaM |           |     | (cid:12):(cid:11) ecnadepmI tuptuO pooL-nepO |       |             |     |     |
3000
2000
30
1000
25
500
| 20  |     |     |     | 300 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
200
15
100
10
50
30
5
20
| 0    |        |          |        | 10   |        |          |        |
| ---- | ------ | -------- | ------ | ---- | ------ | -------- | ------ |
| 1 10 | 100 1k | 10k 100k | 1M 10M | 1 10 | 100 1k | 10k 100k | 1M 10M |
Frequency (Hz)
|     |     |     | D019 |     | Frequency (Hz) |     | D017 |
| --- | --- | --- | ---- | --- | -------------- | --- | ---- |
V  = ±15 V
|     | S   |     |     |     | V S  = ±15 V |     |     |
| --- | --- | --- | --- | --- | ------------ | --- | --- |
Figure 6-11. Maximum Output Voltage vs Figure 6-12. Output Impedance vs Frequency
Frequency
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 9
Product Folder Links: OPA1637

Input Offset Voltage (PV)
)%(
sreifilpmA
15
10
5
0
-200 -150 -100 -50 0 50 100 150 200
Input Offset Voltage (PV)
D001
V = ±1.5 V
S
Figure 6-13. Input Offset Voltage Histogram
)%(
sreifilpmA
15
10
5
0
-200 -150 -100 -50 0 50 100 150 200
D061
V = ±18 V
S
Figure 6-14. Input Offset Voltage Histogram
Offset Voltage Drift (PV/qC)
)%(
sreifilpmA
25
20
15
10
5
0
--11 --00..88 --00..66 --00..44 --00..22 00 00..22 00..44 00..66 00..88 11
Common-Mode Input Offset Voltage (mV)
D002
V = ±15 V
S
Figure 6-15. Input Offset Voltage Drift Histogram
)%(
sreifilpmA
20
15
10
5
0
-6 -4 -2 0 2 4 6
D006
V = ±18 V, VOCM = floating
S
Figure 6-16. Output Common Mode Voltage Offset
Common-Mode Input Offset Voltage (mV)
)%(
sreifilpmA
15
10
5
0
-6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6
Supply Voltage (V)
D007
V = ±18 V, VOCM = 0 V
S
Figure 6-17. Output Common Mode Voltage Offset
)Am(
tnerruC
tnecseiuQ
OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
2
1.8
1.6
1.4
1.2
1
0.8
0.6 -40oC
25oC
0.4
85oC
0.2 125oC
0
3 6 9 12 15 18 21 24 27 30 33 36
D045
Figure 6-18. Quiescent Current vs Supply Voltage
10 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
| www.ti.com |     |     |     | SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |
| ---------- | --- | --- | --- | ---------------------------------------------- | --- | --- |
| 1.5        |     |     |     | 1.6                                            |     |     |
Vs = r1.5 V
| 1.4 |     |     |     | 1.4 |     | Vs = r18 V |
| --- | --- | --- | --- | --- | --- | ---------- |
1.3
| )Am( tnerruC tnecseiuQ |     |     |     | )Am( tnerruC tnecseiuQ 1.2 |     |     |
| ---------------------- | --- | --- | --- | -------------------------- | --- | --- |
1.2
1
1.1
| 1   |     |     |     | 0.8 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
0.9
0.6
0.8
0.4
0.7
|     |     |     | VS =  r18 V | 0.2 |     |     |
| --- | --- | --- | ----------- | --- | --- | --- |
0.6
VS = r1.5 V
| 0.5 |     |     |     | 0   |     |     |
| --- | --- | --- | --- | --- | --- | --- |
-50 -25 0 25 50 75 100 125 150 0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5
|     | Temperature (oC) |     |     | VS+ Delta from Power Down (V) |     |     |
| --- | ---------------- | --- | --- | ----------------------------- | --- | --- |
D065 D053
|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Figure 6-19. Quiescent Current vs Temperature
Figure 6-20. Quiescent Current vs Power-Down
Delta from Supply Voltage
| 250 |     |     |     | 500 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
(cid:16)55oC
| 200                                             |     |     |     | 400 |     |     |
| ----------------------------------------------- | --- | --- | --- | --- | --- | --- |
| )VP( egatloV tesffO derrefeR-tupnI (cid:16)40oC |     |     |     |     |     |     |
25oC
| 150 |     |     |     | 300 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
85oC
| 125oC |     |     |     | )Ap( tnerruC saiB tupnI |     |     |
| ----- | --- | --- | --- | ----------------------- | --- | --- |
| 100   |     |     |     | 200                     |     |     |
150oC
| 50           |     |     |      | 100  |     |            |
| ------------ | --- | --- | ---- | ---- | --- | ---------- |
| 0            |     |     |      | 0    |     |            |
| -50          |     |     |      | -100 |     |            |
| -100         |     |     |      | -200 |     |            |
| (cid:16)17 V |     |     | 17 V |      |     |            |
| -150         |     |     |      | -300 |     | IB(cid:16) |
IB+
| -200 |     |     |     | -400 |     | IOS |
| ---- | --- | --- | --- | ---- | --- | --- |
| -250 |     |     |     | -500 |     |     |
-18 -14 -10 -6 -2 2 6 10 14 18 -18 -14 -10 -6 -2 2 6 10 14 18
| Input Common-Mode Voltage (V) |     |     |     | Input Common-Mode Voltage (V) |     |     |
| ----------------------------- | --- | --- | --- | ----------------------------- | --- | --- |
D023 D025
|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Figure 6-21. Input Offset Voltage vs Input Figure 6-22. Input Bias Current vs Input Common-
| Common-Mode Voltage |     |     |     |     | Mode Voltage |     |
| ------------------- | --- | --- | --- | --- | ------------ | --- |
| 500                 |     |     |     | 30  |              |     |
IB(cid:16)
450
IB+
400
|     |     |     | IOS | 28  |     |     |
| --- | --- | --- | --- | --- | --- | --- |
)Ap( tnerruC saiB tupnI 350
)V( egatloV tuptuO
300
26
250
200
150
24
100
(cid:16)40qC
| 50  |     |     |     | 125qC |     |     |
| --- | --- | --- | --- | ----- | --- | --- |
22
| 0     |                    |          |          | 25qC   |                     |          |
| ----- | ------------------ | -------- | -------- | ------ | ------------------- | -------- |
| -50   |                    |          |          | 85qC   |                     |          |
| -100  |                    |          |          | 20     |                     |          |
| 3 6 9 | 12 15 18           | 21 24 27 | 30 33 36 | 0 5 10 | 15 20 25            | 30 35 40 |
|       | Supply Voltage (V) |          |          |        | Output Current (mA) |          |
D027 D028
|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
Figure 6-23. Input Bias Current vs Supply Voltage Figure 6-24. Output Voltage vs Output Current
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 11
Product Folder Links: OPA1637

OPA1637
| SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | --- | --- | ---------- |
| -20                                            |     |     | 128 |     |            |
(cid:16)40qC
|     |     | 125qC | 126 |     |     |
| --- | --- | ----- | --- | --- | --- |
25qC
| -22 |     |     | 124 |     |     |
| --- | --- | --- | --- | --- | --- |
85qC
)Bd( niaG pooL-nepO
| )V( egatloV tuptuO |     |     | 122 |     |     |
| ------------------ | --- | --- | --- | --- | --- |
| -24                |     |     | 120 |     |     |
118
| -26 |     |     | 116 |     |       |
| --- | --- | --- | --- | --- | ----- |
|     |     |     | 114 |     | 25 qC |
| -28 |     |     | 112 |     | 85 qC |
125 qC
|     |     |     | 110 |     | (cid:16)40 qC |
| --- | --- | --- | --- | --- | ------------- |
| -30 |     |     | 108 |     |               |
-40 -35 -30 -25 -20 -15 -10 -5 0 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7
Output Voltage Delta from Supply Voltage, VS+/VS(cid:16) (V)
Output Current (mA)
D029 D049
|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
Figure 6-26. Open-Loop Gain vs Ouput Delta From
Figure 6-25. Output Voltage vs Output Current
Supply
| 20          |     |     | 20          |     |     |
| ----------- | --- | --- | ----------- | --- | --- |
| RISO = 0 :  |     |     | RISO = 0 :  |     |     |
| RISO = 25 : |     |     | RISO = 25 : |     |     |
17.5
| RISO = 50 :        |     |     | RISO = 50 :   |     |     |
| ------------------ | --- | --- | ------------- | --- | --- |
| 15                 |     |     | 15            |     |     |
| )%( toohsrevO 12.5 |     |     | )%( toohsrevO |     |     |
| 10                 |     |     | 10            |     |     |
7.5
5
5
2.5
| 0        |            |             | 0        |             |             |
| -------- | ---------- | ----------- | -------- | ----------- | ----------- |
| 20 40 60 | 80 100 120 | 140 160 180 |          |             |             |
|          |            |             | 0 50 100 | 150 200 250 | 300 350 400 |
Capacitive Load (pF)
D036 Capacitive Load (pF)
D037
A  = 1
|     | V   |     |     | A V  = 10 |     |
| --- | --- | --- | --- | --------- | --- |
Figure 6-27. Small-Signal Overshoot vs Capacitive Figure 6-28. Small-Signal Overshoot vs Capacitive
Load
Load
| 20  |     |     | 50  |     |     |
| --- | --- | --- | --- | --- | --- |
40
| 17  |     |     | )Am( tnerruC tiucriC-trohS 30 |     |     |
| --- | --- | --- | ----------------------------- | --- | --- |
20
)sP/V( etaR welS
| 14  |     |     | 10 IOUT(cid:14) (sinking) |     |     |
| --- | --- | --- | ------------------------- | --- | --- |
IOUT(cid:14) (sourcing)
0 IOUT(cid:16) (sourcing)
| 11  |     |     | -10 IOUT(cid:16) (sinking) |     |     |
| --- | --- | --- | -------------------------- | --- | --- |
-20
| 8   |     |              | -30 |     |     |
| --- | --- | ------------ | --- | --- | --- |
|     |     | Falling Edge | -40 |     |     |
Rising Edge
| 5   |     |     | -50 |     |     |
| --- | --- | --- | --- | --- | --- |
3 6 9 12 15 18 21 24 27 30 33 36 -25 -10 5 20 35 50 65 80 95 110 125
|     | Supply Voltage (V) |     |     | Temperature (oC) |     |
| --- | ------------------ | --- | --- | ---------------- | --- |
D041 D048
|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
Figure 6-29. Output Slew Rate vs Supply Voltage Figure 6-30. Short-Circuit Current vs Temperature
12 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

Time (1 Ps/div)
)V(
egatloV
3
2.5
2
1.5
1
0.5
0 VOUT(cid:14) VOUT(cid:16)
-0.5
-1
-1.5
-2
-2.5
-3
Time (5 Ps /div)
D044
Figure 6-31. Large-Signal Step Response
)V(
egatloV
1.1
1.08
1.06
1.04
1.02
1
0.98
0.96
0.94
0.92
VVOCM
(VOUT(cid:14) (cid:14) VOUT(cid:16))/2
0.9
D054
Figure 6-32. Output Common-Mode Step
Response, Rising
Time (5 Ps / div)
)V(
egatloV
0.1
0.08 V (V V O O U C T M (cid:14) (cid:14) VOUT(cid:16))/2
0.06
0.04
0.02
0
-0.02
-0.04
-0.06
-0.08
-0.1
Time (500 ns/div)
D055
Figure 6-33. Output Common-Mode Step
Response, Falling
)vid/Vm
05(
egatloV
VIN VOUT(cid:14)
VOUT(cid:16)
D043
Figure 6-34. Small-Signal Step Response, Falling
Time (500 ns/div)
)vid/Vm
05(
egatloV
VIN
VOUT(cid:14)
VOUT(cid:16)
Time (250 ns/div)
D042
Figure 6-35. Small-Signal Step Response, Rising
)vid/VP
052(
eulaV
laniF
ot
atleD
TUOV
OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
+0.01(cid:8)
Settling
Threshold
(cid:16)0.01%
Input Settling
Transition Threshold
D046
Figure 6-36. Output Settling Time to ±0.01%
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 13
Product Folder Links: OPA1637

OPA1637
| SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     | www.ti.com |
| ---------------------------------------------- | --- | --- | ---------- |
| 18                                             | 0.3 | 18  | 0.3        |
VPD
| 15  | 0.25 | 15  | VOUT 0.2 |
| --- | ---- | --- | -------- |
)V( DPV ,egatloV nwod-rewoP
)V( DPV ,egatloV nwod-rewoP
12 0.2 )V( TUOV ,egatloV tuptuO 12 0.1 )V( TUOV ,egatloV tuptuO
| 9   | 0.15 | 9   | 0    |
| --- | ---- | --- | ---- |
| 6   | 0.1  |     |      |
|     |      | 6   | -0.1 |
| 3   | 0.05 |     |      |
|     |      | 3   | -0.2 |
| 0   | 0    | 0   | -0.3 |
VPD
| -3  | -0.05 | -3  | -0.4 |
| --- | ----- | --- | ---- |
VOUT
| -6  | -0.1 | -6  | -0.5 |
| --- | ---- | --- | ---- |
Time (1 Ps/div)
Time (1 Ps/div)
D050
D051

Figure 6-37. Power-Down Time (PD Low to High)
Figure 6-38. Power-Down Time (PD High to Low)
|                   | VIN          |                   | VIN          |
| ----------------- | ------------ | ----------------- | ------------ |
|                   | VOUT(cid:14) |                   | VOUT(cid:14) |
|                   | VOUT(cid:16) |                   | VOUT(cid:16) |
| )vid/V 5( egatloV |              | )vid/V 5( egatloV |              |
Time (20 Ps/div) Time (20 Ps/div)
|     | D039 |     | D040 |
| --- | ---- | --- | ---- |

Figure 6-39. Output Negative Overload Recovery Figure 6-40. Output Positive Overload Recovery
14 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
7 Parameter Measurement Information
7.1 Characterization Configuration
The OPA1637 provides the advantages of a fully differential amplifier (FDA) configuration that offers very low
noise and harmonic distortion in a single, low-power amplifier. The FDA is a flexible device, where the main aim
is to provide a purely differential output signal centered on a user-configurable, common-mode voltage that is
usually matched to the input common-mode voltage required by an analog-to-digital converter (ADC) or class-D
amplifier. The circuit used for characterization of the differential-to-differential performance is seen in Figure 7-1.
|     | RI          | VIN±   RF   |       |     |     |
| --- | ----------- | ----------- | ----- | --- | --- |
|     | 2 k(cid:13) | 2 k(cid:13) | VOUT+ |     |     |
RISO
|     | ±   | VVS+ | 0 (cid:13) |     |     |
| --- | --- | ---- | ---------- | --- | --- |
VIDIFF/2
+
|     |     | ±   |     |     | +   |
| --- | --- | --- | --- | --- | --- |
VVOCM
|     |          | +         |               | R             |            |
| --- | -------- | --------- | ------------- | ------------- | ---------- |
|     |          | O PA163±7 |               | L             | C L VO U T |
| +   |          |           | R             | 10  k(cid:13) | DN P       |
| VCM | ±        |           | IS (cid:13) O |               |            |
| ±   | VIDIFF/2 | +         | 0             |               | ±          |
+
|     | R I | VVS±  VPD |     |     |     |
| --- | --- | --------- | --- | --- | --- |
2  k (cid:13)
|     |     | RF  | VOUT± |     |     |
| --- | --- | --- | ----- | --- | --- |
2 k(cid:13)
VIN+
All voltages except VIN and VOUT are
referenced to ground.
Figure 7-1. Differential Source to a Differential Gain of a 1-V/V Test Circuit
A similar circuit is used for single-ended to differential measurements, as shown in Figure 7-2.
VIN±
|     | RI          | RF  |       |     |     |
| --- | ----------- | --- | ----- | --- | --- |
|     | 2 k(cid:13) |     | VOUT+ |     |     |
2 k(cid:13)
RISO
VVS+
0 (cid:13)
±
+
VVOCM
|     |     | +        |            | R              | C      |
| --- | --- | -------- | ---------- | -------------- | ------ |
|     |     | OPA163±7 |            | L              | L VOUT |
|     |     |          | RISO       | 10  k (cid:13) | D NP   |
|     |     | +        | 0 (cid:13) |                |        |
±
R
|     | I   | VVS±  VPD |     |     |     |
| --- | --- | --------- | --- | --- | --- |
2  k (cid:13)
+
| VIN |     | R F           | VOUT± |     |     |
| --- | --- | ------------- | ----- | --- | --- |
|     | ±   | 2  k (cid:13) |       |     |     |
VIN+
All voltages except VOUT are
referenced to ground.
Figure 7-2. Single-Ended to Differential Gain of a 1-V/V Test Circuit
The FDA requires feedback resistor for both output pins to the input pins. These feedback resistors load the
output differentially only if the input common-mode voltage is equal to the output common-mode voltage set by
VOCM. When VOCM differs from the input common-mode range, the feedback resistors create single-ended
loading. The characterization plots fix the R F  (R F1  = R F2 ) value at 2 k?, unless otherwise noted. This value can
be adjusted to match the system design parameters with the following considerations in mind:
• The current needed to drive R F  from the peak output voltage to the input common-mode voltage adds to the
overall output load current. If the total load current (current through R  + current through R ) exceeds the
F L
current limit conditions, the device enters a current limit state, causing the output voltage to collapse.
• High feedback resistor values (R > 100 k?) interact with the amplifier input capacitance to create a zero in
F
the feedback network. Compensation must be added to account for this potential source of instability; see the
TI Precision Labs FDA Stability Training for guidance on designing an appropriate compensation network.
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 15
Product Folder Links: OPA1637

8 Detailed Description
8.1 Overview
The OPA1637 is a low-noise, low-distortion fully-differential amplifier (FDA) that features Texas Instrument's
super-beta bipolar input devices. Super-beta input devices feature very low input bias current as compared to
standard bipolar technology. The low input bias current and current noise makes the OPA1637 an excellent
choice for audio applications that require low-noise differential signal processing without significant current
consumption. This device is also designed for analog-to-digital audio input circuits that require low noise in a
single fully-differential amplifier. This device achieves lower current consumption at lower noise levels than what
is achievable with two low-noise amplifiers. The OPA1637 also features high-voltage capability, which allows the
device to be used in ±15-V supply circuits without any additional voltage clamping or regulators. This feature
enables a direct, single amplifier for a 24-dBm differential output drive (commonly found on mixers and digital
audio interfaces) without any additional amplification.
8.2 Functional Block Diagram
VS+
IN± ±
Low Noise
Differential I/O
Amplifier
IN+ +
5 M(cid:13)
OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
OUT+
+
±
OUT±
VS±
VS+
±
1 µA E V r C ro M r
Amplifier
+ VOCM
PD
5 M(cid:13)
VS±
16 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
8.3 Feature Description
8.3.1 Super-Beta Input Bipolar Transistors
The OPA1637 is designed on a modern bipolar process that features TI's super-beta input transistors. Traditional
bipolar transistors feature excellent voltage noise and offset drift, but suffer a tradeoff in high input bias current
(I ) and high input bias current noise. Super-beta transistors offer the benefits of low voltage noise and low offset
B
drift with an order of magnitude reduction in input bias current and reduction in input bias current noise. For
audio circuits, input bias current noise can dominate in circuits where higher resistance input resistors are used.
The OPA1637 enables a fully-differential, low-noise amplifier design without restrictions of low input resistance at
a power level unmatched by traditional single-ended amplifiers.
8.3.2 Power Down
The OPA1637 features a power-down circuit to disable the amplifier when a low-power mode is required by the
system. In the power-down state, the amplifier outputs are in a high-impedance state, and the amplifier total
quiescent current is reduced to less than 20 µA.
8.3.3 Flexible Gain Setting
The OPA1637 offers considerable flexibility in the configuration and selection of resistor values. Low input bias
current and bias current noise allows for larger gain resistor values with minimal impact to noise or offset. The
design starts with the selection of the feedback resistor value. The 2-k? feedback resistor value used for the
characterization curves is a good compromise among power, noise, and phase margin considerations. With the
feedback resistor values selected (and set equal on each side), the input resistors are set to obtain the desired
gain, with the input impedance also set with these input resistors. Differential I/O designs provide an input
impedance that is the sum of the two input resistors. Single-ended input to differential output designs present a
more complicated input impedance. Most characteristic curves implement the single-ended to differential design
as the more challenging requirement over differential-to-differential I/O.
8.3.4 Amplifier Overload Power Limit
In many bipolar-based amplifiers, the output stage of the amplifier can draw significant (several milliamperes) of
quiescent current if the output voltage becomes clipped (meaning the output voltage becomes limited by the
negative or positive supply voltage). This condition can cause the system to enter a high-power consumption
state, and potentially cause oscillations between the power supply and signal chain. The OPA1637 has an
advanced output stage design that eliminates this problem. When the output voltage reaches the V or V
VS+ VS–
voltage, there is virtually no additional current consumption from the nominal quiescent current. This feature
helps eliminate any potential system problems when the signal chain is disrupted by a large external transient
voltage.
8.4 Device Functional Modes
The OPA1637 has two functional modes: normal operation and power-down. The power-down state is enabled
when the voltage on the power-down pin is lowered to less than the power-down threshold. In the power-down
state, the quiescent current is significantly reduced, and the output voltage is high-impedance. This high
impedance can lead to the input voltages (+IN and –IN) separating, and forward-biasing the ESD protection
diodes. See Section 9 for guidance on power-down operation.
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 17
Product Folder Links: OPA1637

9 Application and Implementation
Note
Information in the following applications sections is not part of the TI component specification, and TI
does not warrant its accuracy or completeness. TI’s customers are responsible for determining
suitability of components for their purposes. Customers should validate and test their design
implementation to confirm system functionality.
9.1 Application Information
Most applications for the OPA1637 strive to deliver the best dynamic range in a design that delivers the desired
signal processing along with adequate phase margin for the amplifier. The following sections detail some of the
design issues with analysis and guidelines for improved performance.
9.1.1 Driving Capacitive Loads
The capacitive load of an ADC, or some other next-stage device, is commonly required to be driven. Directly
connecting a capacitive load to the output pins of a closed-loop amplifier such as the OPA1637 can lead to an
unstable response. One typical remedy to this instability is to add two small series resistors (R ) at the outputs
ISO
of the OPA1637 before the capacitive load. Good practice is to leave a place for the R elements in a board
ISO
layout (a 0-? value initially) for later adjustment, in case the response appears unacceptable.
For applications where the OPA1637 is used as an output device to drive an unknown capacitive load, such as a
cable, R is required. Figure 9-1 shows the required R value for a 40-degree phase-margin response. The
ISO ISO
peak required R value occurs when C is between 500 pF and 1 nF. As C increases beyond 1 nF, the
ISO L L
bandwidth response of the device reduces, resulting in a slower response but no major degradation in phase
margin. For a typical cable type, such as Belden 8451, capacitive loading can vary from 340 pF (10-foot cable) to
1.7 nF (50-foot cable). Selecting R to be 100 ? provides sufficient phase margin regardless of the cable
ISO
length. R can also be used within the loop feedback of the amplifier; however, simulation must be used to
ISO
verify the stability of the system.
Load Capacitance, CL (F)
):(
OSIR
,ecnatsiseR
noitalosI
OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
100
90
80
70
60
50
40
30
20
10
0
100 p 1 n 10 n 100 n
D069
Figure 9-1. Required Isolation Resistance vs Capacitive Load for a 40° Phase Margin
18 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
9.1.2 Operating the Power-Down Feature
The power-down feature on the OPA1637 allows the device to be put into a low power-consumption state, in
which quiescent current is minimized. To force the device into the low-power state, drive the PD pin lower than
the power-down threshold voltage (V – 2 V). Driving the PD pin lower than the power-down threshold voltage
VS+
forces the internal logic to disable both the differential and common-mode amplifiers. The PD pin has an internal
pullup current that allows the pin to be used in an open-drain MOSFET configuration without an additional pullup
resistor, as seen in Figure 9-2. In this configuration, the logic level can be referenced to the MOSFET, and the
voltage at the PD pin is level-shifted to account for use with high supply voltages. Be sure to select an N-type
MOSFET with a maximum B greater than the total supply voltage. For applications that do not use the
VDSS
power-down feature, tie the PD pin to the positive supply voltage.
VS+
1 µA
To
PD
Enabled amplifier
core
MOSFET
THRESHOLD Powerdown
OPA1637
GND
Figure 9-2. Power-Down ( PD) Pin Interface With Low-Voltage Logic Level Signals
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 19
Product Folder Links: OPA1637

OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
When PD is low (device is in power down) the output pins will be in a high-impedance state. When the device is
in the power-down state, the outputs are high impedance, and the output voltage is no longer controlled by the
amplifier, but dependant on the input and load configuration. In this case, the input voltage between IN– and IN+
can drift to a voltage that may forward-bias the input protection diodes. Take care to avoid high currents flowing
through the input diodes by using an input resistor to limit the current to less than 10 mA. In Figure 9-3, the
OPA1637 is configured in a differential gain of 5 with 100-? input resistors. When the device enters power down,
the voltage between IN– and IN+ increases until the internal protection diode is forward-biased. In this case,
exceeding a voltage on V with R = 0 ? of 2.5 V (diode forward voltage estimated at 0.5 V) results in a current
IN IN
greater than 10 mA. To avoid this high current, select R so that the maximum current flow is less than 10 mA
IN
when V is at maximum voltage.
IN
500 (cid:13)
100 (cid:13)
RIN +10 V
VIN
±
High± Z
+
VOCM
±
High± Z
+ PD
RIN
±10 V
100 (cid:13)
500 (cid:13)
Figure 9-3. Path of Input Current Flow When PD = Low
9.1.3 I/O Headroom Considerations
The starting point for most designs is to assign an output common-mode voltage for the OPA1637. For ac-
coupled signal paths, this voltage is often the default midsupply voltage to retain the most available output swing
around the voltage centered at the V voltage. For dc-coupled designs, set this voltage with consideration to
OCM
the required minimum headroom to the supplies, as described in the specifications for the V control. For
OCM
precision ADC drivers, this V output becomes the V input to the ADC. Often, V is set to V / 2 to
OCM CM CM REF
center the differential input on the available input when precision ADCs are being driven.
From target output V , the next step is to verify that the desired output differential peak-to-peak voltage,
OCM
V , stays within the supplies. For any desired differential V , make sure that the absolute maximum
OUTPP OUTPP
voltage at the output pins swings with Equation 1 and Equation 2, and confirm that these expressions are within
the supply rails minus the output headroom required for the RRO device.
V
V = V ± OUTPP
OUTMIN OCM 4 (1)
V
V = V + OUTPP
OUTMAX OCM 4 (2)
With the output headroom confirmed, the input junctions must also stay within the operating range. The input
range limitations require a maximum 1.0-V headroom from the supply voltages (VS+ and VS–) over the full
temperature range.
20 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
| www.ti.com |     |     |     | SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |
| ---------- | --- | --- | --- | ---------------------------------------------- | --- | --- |
9.1.4 Noise Performance
The first step in the output noise analysis is to reduce the application circuit to the simplest form with equal
feedback and gain setting elements to ground. Figure 9-4 shows the simplest analysis circuit with the FDA and
resistor noise terms to be considered.
|     |     |     | 2     | 2   |     |     |
| --- | --- | --- | ----- | --- | --- | --- |
|     |     |     | e     | e   |     |     |
|     |     |     | nRg   | nRf |     |     |
|     |     |     | RG RF |     |     |     |
|     |     |     | r     | r   |     |     |
I 2
n+
+
|     |     |     |     | e 2 |     |     |
| --- | --- | --- | --- | --- | --- | --- |
no
|     |     |     | 2 ± |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
I n±
e 2
ni
|     |     |     | 2     | 2     |     |     |
| --- | --- | --- | ----- | ----- | --- | --- |
|     |     |     | e nRg | e nRf |     |     |
|     |     |     | RG RF |       |     |     |
|     |     |     | r     | r     |     |     |
Figure 9-4. FDA Noise Analysis Circuit
The noise powers are shown in Figure 9-4 for each term. When the R  and R  (or R) terms are matched on
|     |     |     |     | F G | I   |     |
| --- | --- | --- | --- | --- | --- | --- |
each side, the total differential output noise is the root sum squared (RSS) of these separate terms. Using NG ?
1 + R F  / R G , the total output noise is given by Equation 3. Each resistor noise term is a 4kT × R power (4kT =
1.6E-20 J at 290 K).
| e (cid:11)e | NG(cid:12) 2 (cid:14)2(cid:11)i R | (cid:12) 2 (cid:14)2(cid:11)4kTR | NG(cid:12) |     |     |     |
| ----------- | --------------------------------- | -------------------------------- | ---------- | --- | --- | --- |
| o   ni      | N                                 | F                                | F          |     |     |     |
(3)
The first term is simply the differential input spot noise times the noise gain. The second term is the input current
noise terms times the feedback resistor (and because there are two uncorrelated current noise terms, the power
is two times one of them). The last term is the output noise resulting from both the R  and R  resistors, at again,
F G
twice the value for the output noise power of each side added together. Running a wide sweep of gains when
holding R  to 2 k? gives the standard values and resulting noise listed in Table 9-1. When the gain increases,
F
the input-referred noise approaches only the gain of the FDA input voltage noise term at 3.7 nV/? Hz.
Table 9-1. Swept Gain of the Output- and Input-Referred Spot Noise Calculations
GAIN (V/V) R F  (?) R G1  (?) A V E O  (nV/? Hz) E (nV/? Hz) I
| 0.1 | 2000 |     | 20000 | 0.1  | 9.4  | 93.9 |
| --- | ---- | --- | ----- | ---- | ---- | ---- |
| 1   | 2000 |     | 2000  | 1    | 13.6 | 13.6 |
| 2   | 2000 |     | 1000  | 2    | 17.8 | 8.9  |
| 5   | 2000 |     | 402   | 4.98 | 29.5 | 5.9  |
| 10  | 2000 |     | 200   | 10   | 48.6 | 4.9  |
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 21
Product Folder Links: OPA1637

OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
9.2 Typical Applications
9.2.1 Current-Output Audio DAC Buffer to Class-D Amplifier
RF1
1 k(cid:13)
CF1
3.3 nF RISO1
1
C
µ
2
F
75 (cid:13)
5 V R 49 I1 (cid:13) 5 V INPUT_A
±
TPA3251
A P u C d M io 1 D 7 A 95 C I I O O U U T T L L / / R R ± + C5 ± 3.5 V OPA163 + ±7 C 10 D F nF A C m la p A s l s if D i D er C
1 µF + PD C3
1 µF
GND ±10 V RI2 ±10 V 5 V INPUT_B
49 (cid:13) RISO2
75 (cid:13)
1 R k F (cid:13) 2 3. C 3 F n 2 F GND
Figure 9-5. Differential Current-to-Voltage Converter
9.2.1.1 Design Requirements
The requirements for this application are:
• Differential current-to-voltage conversion and filtering
• 1-kmho transimpedance gain
• 40-kHz Butterworth response filter
• 0-V dc common-mode voltage at DAC output
9.2.1.2 Detailed Design Procedure
This design provides current-to-voltage conversion from a current-output audio DAC into a voltage-input, class-D
amplifier. The order of design priorities are as follows:
• Select feedback-resistor values based on the gain required from the current-output stage to the voltage-input
stage. For this design, the full-scale, peak-to-peak output current of the PCM1795 ( I – I ) is ±4
OUTL/R+ OUTL/R–
mA. A gain of 1k gives a wide voltage swing of ±4 V, allowing for high SNR without exceeding the input
voltage limit of the TPA3251.
• After the gain is fixed, select the output common-mode voltage. The output common-mode voltage
determines the input common-mode voltage in this configuration. To set the nominal output voltage of the
PCM1795 to 0 V (which corresponds to the input common mode voltage of the OPA1637), shift the output
negatively from the desired common-mode input voltage by the gain multiplied by the dc center current value
of the PCM1795 (3.5 mA). In this case, –3.5 V satisfies the design goal.
• A bypass capacitor from the VOCM pin to ground must be selected to filter noise from the voltage divider.
The capacitor selection is determined by balancing the startup time of the system with the output common-
mode noise. A higher capacitance gives a lower frequency filter cutoff on the VOCM pin, thus giving lower
noise performance, but also slows down the initial startup time of the circuit as a result of the RC delay from
the resistor divider in combination with the filter capacitor.
• Select C so that the desired bandwidth of the active filter is achieved. The 3-dB frequency is determined by
F
the reciprocal of the product of R and C .
F F
• Use a passive filter on the output to increase noise filtering beyond the desired bandwidth. The passive filter
formed by R and C adds an additional real pole to the filter response. If the pole is designed at the
D1,2 DF
same frequency as the active filter pole, the overall 3-dB frequency shifts to a lower frequency value, and the
step response is overdamped. A trade-off must be made to give optimal transient response versus increased
filter attenuation at higher frequencies. For this design, the second pole is set to 106 kHz.
22 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
| www.ti.com |     |     | SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 |     |     |     |
| ---------- | --- | --- | ---------------------------------------------- | --- | --- | --- |
9.2.1.3 Application Curves
The simulated response of the current-to-voltage audio DAC buffer can be seen in Figure 9-6 and Figure 9-7.
| 90       |     | 0   | 1.2  |     |     |      |
| -------- | --- | --- | ---- | --- | --- | ---- |
| Gain     |     |     | 1.05 |     |     | VOUT |
| 75 Phase |     | -30 |      |     |     | VIN  |
0.9
| 60  |     | -60 | 0.75 |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
0.6
| 45  |     | -90 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
0.45
| 30        |     | -120      | 0.3         |     |     |     |
| --------- | --- | --------- | ----------- | --- | --- | --- |
| )Bd( niaG |     | )q( esahP | )V( egatloV |     |     |     |
0.15
| 15  |     | -150 |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- |
0
| 0   |     | -180 | -0.15 |     |     |     |
| --- | --- | ---- | ----- | --- | --- | --- |
-0.3
| -15 |     | -210 |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- |
-0.45
| -30 |     | -240 | -0.6 |     |     |     |
| --- | --- | ---- | ---- | --- | --- | --- |
-0.75
| -45 |                | -270 | -0.9  |          |             |             |
| --- | -------------- | ---- | ----- | -------- | ----------- | ----------- |
| -60 |                | -300 | -1.05 |          |             |             |
| 100 | 1k 10k 100k    | 1M   | -1.2  |          |             |             |
|     | Frequency (Hz) |      | 0 20  | 40 60 80 | 100 120 140 | 160 180 200 |
C105
Time (Ps)
| Figure 9-6. Gain and Phase Response for Current- |     |     |     |     |     | C105 |
| ------------------------------------------------ | --- | --- | --- | --- | --- | ---- |
Figure 9-7. Transient Response for Current-to-
to-Voltage Buffer
Voltage Buffer
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 23
Product Folder Links: OPA1637

OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
9.2.2 An MFB Filter Driving an ADC Application
A common application use case for fully-differential amplifiers is to easily convert a single-ended signal into a
differential signal to drive a differential input source, such as an ADC or class-D amplifier. Figure 9-8 shows an
example of the OPA1637 used to convert a single-ended, low-voltage signal audio source, such as a small
electret microphone, and deliver a low-noise differential signal that is common-mode shifted to the center of the
ADC input range. A multiple-feedback (MFB) configuration is used to provide a Butterworth filter response, giving
a 40-dB/decade rolloff with a –3-dB frequency of 30 kHz.
RF1
3.65 k(cid:13)
C F 1
| R            | R G 1           | 1  n F |                    |         |     |
| ------------ | --------------- | ------ | ------------------ | ------- | --- |
| I1  (cid:13) | 6 04   (cid:13) |        |                    | C       |     |
| 73 2         |                 |        | R O 1 R A 1        | A 1     |     |
|              |                 |        |  (cid:13) (cid:13) | 47   pF |     |
|              |                 |        | 2 0 10 0           |         |     |
+5 V
VIN
±
+ C
|        |     | VOCM FDA |     | A 2        |     |
| ------ | --- | -------- | --- | ---------- | --- |
| 6.2 nF |     | ±        |     | 1  n F ADC |     |
|        |     | + PD     |     |            |     |
±5 V VS+
|                |                 |                   | R O 2 R A 2                   | C       |     |
| -------------- | --------------- | ----------------- | ----------------------------- | ------- | --- |
|                |                 |                   | 2 0  (cid:13) 10 0   (cid:13) | A 3     |     |
| R              | R               |                   |                               | 47   pF |     |
| I2             | G 2             | R C F 2           |                               |         |     |
| 73 2  (cid:13) | 6 04   (cid:13) | F 2 1  n F        |                               |         |     |
|                |                 | 3.6 5   k(cid:13) |                               |         |     |
Figure 9-8. Example 30-kHz Butterworth Filter
9.2.2.1 Design Requirements
The requirements for this application are:
• Single-ended to differential conversion
• 5-V/V gain
• Active filter set to a Butterworth, 30-kHz response shape
• Output RC elements set by SAR input requirements (not part of the filter design)
• Filter element resistors and capacitors are set to limit added noise over the OPA1637 and noise peaking
9.2.2.2 Detailed Design Procedure
The design proceeds using the techniques and tools suggested in the Design Methodology for MFB Filters in
ADC Interface Applications application note. The process includes:
• Scale the resistor values to not meaningfully contribute to the output noise produced by the OPA1637.
• Select the RC ratios to hit the filter targets when reducing the noise gain peaking within the filter design.
• Set the output resistor to 100 ? into a 1-nF differential capacitor.
• Add 47-pF common-mode capacitors to the load capacitor to improve common noise filtering.
• Inside the loop, add 20-? output resistors after the filter feedback capacitor to increase the isolation to the
load capacitor.
24 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

9.2.2.3 Application Curves
The gain and phase plots are shown in Figure 9-9. The MFB filter features a Butterworth responses feature very
flat passband gain, with a 2-pole roll-off at 30 kHz to eliminate any higher-frequency noise from contaminating
the signal chain, and potentially alias back into the audio band.
Frequency (Hz)
)Bd(
niaG
)q(
esahP
OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
20 120
16 90
12 60
8 30
4 0
0 -30
-4 -60
-8 -90
-12 -120
-16 Gain -150
Phase
-20 -180
100 1k 10k 100k
C100
Figure 9-9. Gain and Phase Plot for a 30-kHz Butterworth Filter
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 25
Product Folder Links: OPA1637

OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
9.2.3 Differential Microphone Input to Line Level
Professional dynamic microphones typically feature low output impedance to minimize noise coupling on the
microphone cable. Interfacing the microphone with high-impedance circuitry typically requires the use of an
impedance conversion stage, often done with a transformer or discrete amplifiers. The flexibility of the OPA1637
allows the device to be configured with a low differential input impedance and 20 dB of gain, simplifying the
impedance conversion and gain stage into a single device. Figure 9-10 shows an example of a differential, low
input impedance, microphone level voltage (10 mV to 100 mV) amplifier to a line-level amplitude signal that also
has adjustable dc common-mode shift capability. This design example shows how the OPA1637 makes a great
choice for driving an ADC class-D amplifier.
RF1
Dynamic  750 (cid:13)
Microphone
|     |     |     | R   | C F 1    |     |
| --- | --- | --- | --- | -------- | --- |
|     |     |     | G 1 | 4. 7  nF |     |
7 5  (cid:13)
RISO1
100 (cid:13)
+15
XLR
Cable
±
To ADC/
| VIN | 1   | 1   |      | +   |                    |
| --- | --- | --- | ---- | --- | ------------------ |
|     | 3   | 3   | VOCM | FDA | Class D Amplifier/ |
|     | 2   | 2   |      | ±   | XLR output         |
|     |     |     | +    | PD  |                    |
+15
-15
RISO2
100 (cid:13)
|     |     |     | R             | C        |     |
| --- | --- | --- | ------------- | -------- | --- |
|     |     |     | G  (cid:13) 2 | F 2      |     |
|     |     | 7   | 5             | 4. 7  nF |     |
RF2
750 (cid:13)
Figure 9-10. Fully Differential, Low-Noise, 20-dB Microphone Gain Block With DC Shift
9.2.3.1 Application Curves
2.5
V O U T -
|     | 2   |     |     | V   |     |
| --- | --- | --- | --- | --- | --- |
O U T +
1.5
)V( egatloV tuptuO 1
0.5
0
-0.5
-1
-1.5
-2
-2.5
|     | 0   | 0.2 0.4 0.6 | 0.8 1 1.2 | 1.4 1.6 1.8 2 |     |
| --- | --- | ----------- | --------- | ------------- | --- |
Time (ms)
D075
|     |     | V   |  = 0 V |     |     |
| --- | --- | --- | ------ | --- | --- |
OCM
Figure 9-11. Output Waveform of the Microphone Amplifier
26 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

OPA1637
www.ti.com SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020
10 Power Supply Recommendations
The OPA1637 operates from supply voltages of 3.0 V to 36 V (±1.5 V to ±18 V, dual supply). Connect ceramic
bypass capacitors from both VS+ and VS– to GND.
11 Layout
11.1 Layout Guidelines
11.1.1 Board Layout Recommendations
• Keep differential signals routed together to minimize parasitic impedance mismatch.
• Connect a 0.1-µF capacitor to the supply nodes through a via.
• Connect a 0.1-µF capacitor to the VOCM pin if no external voltage is used.
• Keep any high-frequency nodes that can couple through parasitic paths away from the VOCM node.
• Clean the PCB board after assembly to minimize any leakage paths from excess flux into the VOCM node.
11.2 Layout Example
Connect IN+/IN± through
input resistors on the top
V
|     |     |     | IN layer.  Maintain symmetry  |     |
| --- | --- | --- | ----------------------------- | --- |
|     |     |     | R R between traces and        |     |
IN IN
routing to minimize
common mode coupling.
| Route the V |  pin  |     |     |     |
| ----------- | ----- | --- | --- | --- |
OCM
| connection through a via.  |     |     | IN±  IN+  |                        |
| -------------------------- | --- | --- | --------- | ---------------------- |
|                            |     | R   |           | Connect the powerdown  |
|                            |     | F   |           | R                      |
| Connect a 0.1 µF           |     |     |           | F                      |
pin through a via.  If
| capacitor to V | OCM  if no  |     | VOCM PD |     |
| -------------- | ----------- | --- | ------- | --- |
powerdown is not
| external voltage is used  |     | C   |         |                         |
| ------------------------- | --- | --- | ------- | ----------------------- |
|                           |     | CM  |         | needed, leave floating. |
| to set the output common  |     |     | VS+ VS± |                         |
mode voltage.
C
|     |     | BYPASS | OUT± | C      |
| --- | --- | ------ | ---- | ------ |
|     |     |        | OUT+ | BYPASS |
Connect bypass
capacitors through a via.
V
OUT
Figure 11-1. Example Layout
Copyright © 2020 Texas Instruments Incorporated Submit Document Feedback 27
Product Folder Links: OPA1637

OPA1637
SBOSA00B – DECEMBER 2019 – REVISED AUGUST 2020 www.ti.com
12 Device and Documentation Support
12.1 Device Support
12.1.1 Development Support
• OPA1637 TINA-TI™ model
• TINA-TI Gain of 0.2 100kHz Butterworth MFB Filter
• TINA-TI 100kHz MFB filter LG test
• TINA-TI Differential Transimpedance LG Sim
12.2 Documentation Support
12.2.1 Related Documentation
For related documentation see the following:
• Texas Instruments, OPAx192 36-V, Precision, Rail-to-Rail Input/Output, Low Offset Voltage, Low Input Bias
Current Op Amp with e-trim™ data sheet
• Texas Instruments, OPA161x SoundPlus™ High-Performance, Bipolar-Input Audio Operational Amplifiers
data sheet
• Texas Instruments, Design Methodology for MFB Filters in ADC Interface Applications application report
• Texas Instruments, Design for Wideband Differential Transimpedance DAC Output application report
• Texas Instruments, PCM1795 32-Bit, 192-kHz Sampling, Advanced Segment, Stereo Audio Digital-to-Analog
Converter data sheet
• Texas Instruments, TPA3251 175-W Stereo, 350-W Mono PurePath™ Ultra-HD Analog Input Class-D
Amplifier data sheet
12.3 Receiving Notification of Documentation Updates
To receive notification of documentation updates, navigate to the device product folder on ti.com. Click on
Subscribe to updates to register and receive a weekly digest of any product information that has changed. For
change details, review the revision history included in any revised document.
12.4 Support Resources
TI E2E™ support forums are an engineer's go-to source for fast, verified answers and design help — straight
from the experts. Search existing answers or ask your own question to get the quick design help you need.
Linked content is provided "AS IS" by the respective contributors. They do not constitute TI specifications and do
not necessarily reflect TI's views; see TI's Terms of Use.
12.5 Trademarks
Burr-Brown™ and TI E2E™ are trademarks of Texas Instruments.
All other trademarks are the property of their respective owners.
12.6 Electrostatic Discharge Caution
This integrated circuit can be damaged by ESD. Texas Instruments recommends that all integrated circuits be handled
with appropriate precautions. Failure to observe proper handling and installation procedures can cause damage.
ESD damage can range from subtle performance degradation to complete device failure. Precision integrated circuits may
be more susceptible to damage because very small parametric changes could cause the device not to meet its published
specifications.
12.7 Glossary
TI Glossary This glossary lists and explains terms, acronyms, and definitions.
13 Mechanical, Packaging, and Orderable Information
The following pages include mechanical, packaging, and orderable information. This information is the most
current data available for the designated devices. This data is subject to change without notice and revision of
this document. For browser-based versions of this data sheet, refer to the left-hand navigation.
28 Submit Document Feedback Copyright © 2020 Texas Instruments Incorporated
Product Folder Links: OPA1637

PACKAGE OPTION ADDENDUM
www.ti.com 15-Jul-2026
PACKAGING INFORMATION
Orderable part number Status Material type Package | Pins Package qty | Carrier RoHS Lead finish/ MSL rating/ Op temp (°C) Part marking
(1) (2) (3) Ball material Peak reflow (6)
(4) (5)
OPA1637DGKR Active Production VSSOP (DGK) | 8 2500 | LARGE T&R Yes NIPDAU | SN Level-2-260C-1 YEAR -40 to 125 1637
| NIPDAUAG
OPA1637DGKR.B Active Production VSSOP (DGK) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 1637
OPA1637DGKRG4 Active Production VSSOP (DGK) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 1637
OPA1637DGKRG4.B Active Production VSSOP (DGK) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 1637
OPA1637DGKT Active Production VSSOP (DGK) | 8 250 | SMALL T&R Yes NIPDAU | SN Level-2-260C-1 YEAR -40 to 125 1637
| NIPDAUAG
OPA1637DGKT.B Active Production VSSOP (DGK) | 8 250 | SMALL T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 125 1637
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
Important Information and Disclaimer:The information provided on this page represents TI's knowledge and belief as of the date that it is provided. TI bases its knowledge and belief on information provided by third parties, and
makes no representation or warranty as to the accuracy of such information. Efforts are underway to better integrate information from third parties. TI has taken and continues to take reasonable steps to provide representative
and accurate information but may not have conducted destructive testing or chemical analysis on incoming materials and chemicals. TI and TI suppliers consider certain information to be proprietary, and thus CAS numbers
and other limited information may not be available for release.
Addendum-Page 1

PACKAGE OPTION ADDENDUM
www.ti.com 15-Jul-2026
In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.
Addendum-Page 2

PACKAGE MATERIALS INFORMATION
|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
www.ti.com 24-Jul-2025
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
OPA1637DGKR VSSOP DGK 8 2500 330.0 12.4 5.3 3.4 1.4 8.0 12.0 Q1
OPA1637DGKRG4 VSSOP DGK 8 2500 330.0 12.4 5.3 3.4 1.4 8.0 12.0 Q1
OPA1637DGKT VSSOP DGK 8 250 330.0 12.4 5.3 3.4 1.4 8.0 12.0 Q1
OPA1637DGKT VSSOP DGK 8 250 330.0 12.4 5.25 3.35 1.25 8.0 12.0 Q1
OPA1637DGKT VSSOP DGK 8 250 330.0 12.4 5.3 3.4 1.4 8.0 12.0 Q1
Pack Materials-Page 1

PACKAGE MATERIALS INFORMATION
|            |     |     |     |     |     |             |
| ---------- | --- | --- | --- | --- | --- | ----------- |
| www.ti.com |     |     |     |     |     | 24-Jul-2025 |
TAPE AND REEL BOX DIMENSIONS
Width (mm)
H
W L

*All dimensions are nominal
Device Package Type Package Drawing Pins SPQ Length (mm) Width (mm) Height (mm)
| OPA1637DGKR   | VSSOP | DGK | 8 2500 | 353.0 | 353.0 | 32.0 |
| ------------- | ----- | --- | ------ | ----- | ----- | ---- |
| OPA1637DGKRG4 | VSSOP | DGK | 8 2500 | 353.0 | 353.0 | 32.0 |
| OPA1637DGKT   | VSSOP | DGK | 8 250  | 366.0 | 364.0 | 50.0 |
| OPA1637DGKT   | VSSOP | DGK | 8 250  | 366.0 | 364.0 | 50.0 |
| OPA1637DGKT   | VSSOP | DGK | 8 250  | 353.0 | 353.0 | 32.0 |
Pack Materials-Page 2

PACKAGE OUTLINE
DGK0008A VSSOP - 1.1 mm max height
SCALE 4.000
SMALL OUTLINE PACKAGE
C
5.05
TYP
A 4.75
0.1 C
PIN 1 INDEX AREA
SEATING
PLANE
6X 0.65
8
1
2X
3.1
1.95
2.9
NOTE 3
4
5
0.38
8X
0.25
B 3.1 0.13 C A B
2.9
NOTE 4
0.23
0.13
SEE DETAIL A
0.25
GAGE PLANE
1.1 MAX
0.15
0.7
0 -8 0.05
0.4
DETA 20AIL A
TYPICAL
4214862/A 04/2023
PowerPAD is a trademark of Texas Instruments.
NOTES:
1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
exceed 0.15 mm per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.25 mm per side.
5. Reference JEDEC registration MO-187.
www.ti.com

EXAMPLE BOARD LAYOUT
DGK0008A TM VSSOP - 1.1 mm max height
SMALL OUTLINE PACKAGE
SYMM
8X (1.4) (R0.05) TYP
8X (0.45) 1 8
SYMM
6X (0.65)
5
4
SEE DETAILS
(4.4)
LAND PATTERN EXAMPLE
EXPOSED METAL SHOWN
SCALE: 15X
SOLDER MASK METAL METAL UNDER SOLDER MASK
OPENING SOLDER MASK OPENING
EXPOSED METAL EXPOSED METAL
0.05 MAX 0.05 MIN
ALL AROUND ALL AROUND
NON-SOLDER MASK SOLDER MASK
DEFINED DEFINED
(PREFERRED)
SOLDE15.000R MASK DETAILS
4214862/A 04/2023
NOTES: (continued)
6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
8. Vias are optional depending on application, refer to device data sheet. If any vias are implemented, refer to their locations shown
on this view. It is recommended that vias under paste be filled, plugged or tented.
9. Size of metal pad may vary due to creepage requirement.
www.ti.com

EXAMPLE STENCIL DESIGN
DGK0008A TM VSSOP - 1.1 mm max height
SMALL OUTLINE PACKAGE
SYMM
8X (1.4) (R0.05) TYP
8X (0.45) 1 8
SYMM
6X (0.65)
5
4
(4.4)
SOLDER PASTE EXAMPLE
SCALE: 15X
4214862/A 04/2023
NOTES: (continued)
11. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
design recommendations.
12. Board assembly site may have different recommendations for stencil design.
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
