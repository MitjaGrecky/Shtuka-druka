|     |     | Product | Order | Technical |     | Tools &  |     | Support & |     |     |     |     |
| --- | --- | ------- | ----- | --------- | --- | -------- | --- | --------- | --- | --- | --- | --- |
|     |     | Folder  | Now   | Documents |     | Software |     | Community |     |     |     |     |
TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019
2
TCA9546A Low Voltage 4-Channel I C and SMBus Switch with Reset Function
| 1 Features                               |     |     |     |     | 2 Applications |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
| • 1-of-4Bidirectionaltranslatingswitches |     |     |     |     | • Servers      |     |     |     |     |     |     |     |
1
• I2CBusandSMBuscompatible • Routers(telecomswitchingequipment)
| • Active-lowresetinput |     |     |     |     | • Factoryautomation |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
ProductswithI2Cslaveaddressconflicts(multiple,
| • Threeaddresspins,allowinguptoeight |     |     |     |     | •                     |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
| TCA9546AdevicesontheI2Cbus           |     |     |     |     | identicaltempsensors) |     |     |     |     |     |     |     |
• ChannelselectionviaI2CBus,inanycombination
3 Description
• Power-upwithallswitchchannelsdeselected
|        |             |     |     |     | The    | TCA9546A   | is  | a quad  | bidirectional |          | translating |     |
| ------ | ----------- | --- | --- | --- | ------ | ---------- | --- | ------- | ------------- | -------- | ----------- | --- |
| • LowR | ON switches |     |     |     |        |            |     |         | I2C           |          |             |     |
|        |             |     |     |     | switch | controlled |     | via the |               | bus. The | SCL/SDA     |     |
• Allowsvoltage-leveltranslationbetween
|     |     |     |     |     | upstream |     | pair fans | out | to four downstream |     | pairs, | or  |
| --- | --- | --- | --- | --- | -------- | --- | --------- | --- | ------------------ | --- | ------ | --- |
1.8-V, 2.5-V,3.3-V,and5-Vbuses channels. Any individual SCn/SDn channel or
|     |     |     |     |     | combination |     | of channels |     | can be | selected, | determined |     |
| --- | --- | --- | --- | --- | ----------- | --- | ----------- | --- | ------ | --------- | ---------- | --- |
• Noglitchonpower-up
bythecontentsoftheprogrammablecontrolregister.
• Supportshotinsertion
• Lowstandbycurrent An active-low reset (RESET) input allows the
|     |     |     |     |     | TCA9546A |     | to recover | from | a situation | in  | which | one of |
| --- | --- | --- | --- | --- | -------- | --- | ---------- | ---- | ----------- | --- | ----- | ------ |
• Operatingpower-supplyvoltagerangeof1.65Vto
|      |     |     |     |     | the     | downstream | I2C | buses  | is stuck | in    | a low   | state. |
| ---- | --- | --- | --- | --- | ------- | ---------- | --- | ------ | -------- | ----- | ------- | ------ |
| 5.5V |     |     |     |     | Pulling | RESET      | low | resets | the I2C  | state | machine | and    |
• 5.5VTolerantinputs
|                            |     |     |     |     | causesallthechannels           |     |     |     | to be deselected, |     | as does | the |
| -------------------------- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | ----------------- | --- | ------- | --- |
| • 0to400-kHzClockfrequency |     |     |     |     | internalpower-onresetfunction. |     |     |     |                   |     |         |     |
• Latch-upperformanceexceeds100mAPerJESD The pass gates of the switches are constructed such
|     |     |     |     |     | that | the VCC | pin | can be | used to | limit | the maximum |     |
| --- | --- | --- | --- | --- | ---- | ------- | --- | ------ | ------- | ----- | ----------- | --- |
78
• ESDProtectionexceedsJESD22 high voltage, which will be passed by the TCA9546A.
|     |     |     |     |     | This | allows | the use | of different | bus | voltages |     | on each |
| --- | --- | --- | --- | --- | ---- | ------ | ------- | ------------ | --- | -------- | --- | ------- |
– 4000-VHuman-bodymodel(A114-A)
|     |     |     |     |     | pair, | so  | that 1.8-V, |     | 2.5-V, or | 3.3-V | parts | can |
| --- | --- | --- | --- | --- | ----- | --- | ----------- | --- | --------- | ----- | ----- | --- |
– 1500-VCharged-devicemodel(C101) communicate with 5-V parts without any additional
|     |     |     |     |     | protection. |         | External | pull-up | resistors | pull     | the | bus up  |
| --- | --- | --- | --- | --- | ----------- | ------- | -------- | ------- | --------- | -------- | --- | ------- |
|     |     |     |     |     | to the      | desired | voltage  | level   | for each  | channel. |     | All I/O |
pinsare5.5-Vtolerant.
DeviceInformation(1)
|     |     |     |     |     | DEVICENAME |     |     | PACKAGE   |     | BODYSIZE(NOM) |     |     |
| --- | --- | --- | --- | --- | ---------- | --- | --- | --------- | --- | ------------- | --- | --- |
|     |     |     |     |     |            |     |     | TSSOP(16) |     | 5.00mmx4.40mm |     |     |
TCA9546A
|     |     |     |     |     |     |     |     | SOIC(16) |     | 9.90mmx3.91mm |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------------- | --- | --- |
(1) Forallavailablepackages,seetheorderableaddendumat
theendofthedatasheet.
SimplifiedApplicationDiagram
|     |     |     |     | V   |        | Channel 0 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | SDA | CC SD0 |           |     |     |     |     |     |     |
SlavesA0,A1...AN
|     |     | I2C or SMBus |     | SCL | SC0 |     |     |     |     |     |     |     |
| --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Master
Channel 1
|     |     | (e.g. Processor) |     | RESET | SD1 |     | Slaves B0, B1...BN |     |     |     |     |     |
| --- | --- | ---------------- | --- | ----- | --- | --- | ------------------ | --- | --- | --- | --- | --- |
SC1
TCA9546A
Channel 2
|     |     |     |     |     | SD2 |     | Slaves C0, C1...CN |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- |
|     |     |     |     | A0  | SC2 |     |                    |     |     |     |     |     |
A1
|     |     |     |     | A2  |     | Channel 3 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
GND
|     |     |     |     |     | SD3 |     | Slaves D0, D1...DN |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- |
SC3
1
An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,
intellectualpropertymattersandotherimportantdisclaimers.PRODUCTIONDATA.

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
Table of Contents
1 Features.................................................................. 1 8.3 FeatureDescription.................................................11
2 Applications........................................................... 1 8.4 DeviceFunctionalModes........................................11
3 Description............................................................. 1 8.5 Programming...........................................................11
8.6 ControlRegister......................................................14
4 RevisionHistory..................................................... 2
9 ApplicationandImplementation........................ 16
5 PinConfigurationandFunctions......................... 3
9.1 ApplicationInformation............................................16
6 Specifications......................................................... 4
9.2 TypicalApplication..................................................16
6.1 AbsoluteMaximumRatings ....................................4
10 PowerSupplyRecommendations..................... 19
6.2 ESDRatings..............................................................4
10.1 Power-OnResetRequirements ...........................19
6.3 RecommendedOperatingConditions.....................4
11 Layout................................................................... 21
6.4 ThermalInformation..................................................4
6.5 ElectricalCharacteristics..........................................5 11.1 LayoutGuidelines.................................................21
6.6 I2CInterfaceTimingRequirements..........................6 11.2 LayoutExample....................................................21
6.7 SwitchingCharacteristics.........................................6 12 DeviceandDocumentationSupport................. 22
6.8 InterruptandResetTimingRequirements...............7 12.1 ReceivingNotificationofDocumentationUpdates22
6.9 TypicalCharacteristics..............................................7 12.2 SupportResources...............................................22
7 ParameterMeasurementInformation..................8 12.3 Trademarks...........................................................22
12.4 ElectrostaticDischargeCaution............................22
8 DetailedDescription............................................ 10
12.5 Glossary................................................................22
8.1 Overview.................................................................10
13 Mechanical,Packaging,andOrderable
8.2 FunctionalBlockDiagram.......................................10
Information........................................................... 22
4 Revision History
ChangesfromRevisionA(February2015)toRevisionB Page
• ChangedthePinConfigurationimageappearance............................................................................................................... 3
• ChangedV =3.3VtoV =2.5VinFigure15................................................................................................................ 16
CC CC
ChangesfromOriginal(April2014)toRevisionA Page
• AddedDpackagetothedatasheet. ...................................................................................................................................... 1
• ChangedHandlingRatingstabletoESDRatings. ................................................................................................................ 4
• AddedDpackagetotheThermalInformationtable.............................................................................................................. 4
2 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
| www.ti.com          |               |     |     | SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |     |
| ------------------- | ------------- | --- | --- | -------------------------------------- | --- |
| 5 Pin Configuration | and Functions |     |     |                                        |     |
DorPWPackage
TSSOPandSOIC16Pins
TopView
|     | A0    | 1   |     | 16  VCC |     |
| --- | ----- | --- | --- | ------- | --- |
|     | A1    | 2   |     | 15  SDA |     |
|     | RESET | 3   |     | 14  SCL |     |
|     | SD0   | 4   |     | 13  A2  |     |
|     | SC0   | 5   |     | 12  SC3 |     |
|     | SD1   | 6   |     | 11  SD3 |     |
|     | SC1   | 7   |     | 10  SC2 |     |
|     | GND   | 8   |     | 9  SD2  |     |
Not to scale
PinFunctions
PIN
DESCRIPTION
| NAME | NO. |                                  |     |           |     |
| ---- | --- | -------------------------------- | --- | --------- | --- |
| A0   | 1   | Addressinput0.ConnectdirectlytoV |     | orground. |     |
CC
| A1  | 2   | Addressinput1.ConnectdirectlytoV |     | CC orground. |     |
| --- | --- | -------------------------------- | --- | ------------ | --- |
RESET 3 Activelowresetinput.ConnecttoV orV (1)throughapull-upresistor,ifnotused.
CC DPUM
| SD0 | 4   | Serialdata0.ConnecttoV |     | (1)throughapull-upresistor. |     |
| --- | --- | ---------------------- | --- | --------------------------- | --- |
DPU0
(1)throughapull-upresistor.
| SC0 | 5   | Serialclock0.ConnecttoV | DPU0 |                             |     |
| --- | --- | ----------------------- | ---- | --------------------------- | --- |
| SD1 | 6   | Serialdata1.ConnecttoV  |      | (1)throughapull-upresistor. |     |
DPU1
| SC1 | 7   | Serialclock1.ConnecttoV |     | (1)throughapull-upresistor. |     |
| --- | --- | ----------------------- | --- | --------------------------- | --- |
DPU1
| GND | 8   | Ground                 |     |                             |     |
| --- | --- | ---------------------- | --- | --------------------------- | --- |
| SD2 | 9   | Serialdata2.ConnecttoV |     | (1)throughapull-upresistor. |     |
DPU2
(1)throughapull-upresistor.
| SC2 | 10  | Serialclock2.ConnecttoV | DPU2 |                             |     |
| --- | --- | ----------------------- | ---- | --------------------------- | --- |
| SD3 | 11  | Serialdata3.ConnecttoV  |      | (1)throughapull-upresistor. |     |
DPU3
| SC3 | 12  | Serialclock3.ConnecttoV |     | (1)throughapull-upresistor. |     |
| --- | --- | ----------------------- | --- | --------------------------- | --- |
DPU3
| A2  | 13  | Addressinput2.ConnectdirectlytoV |     | CC orground. |     |
| --- | --- | -------------------------------- | --- | ------------ | --- |
SCL 14 Serialclockline.ConnecttoV (1)throughapull-upresistor.
DPUM
| SDA | 15  | Serialdataline.ConnecttoV |     | (1)throughapull-upresistor. |     |
| --- | --- | ------------------------- | --- | --------------------------- | --- |
DPUM
| VCC | 16  | Supplypower |     |     |     |
| --- | --- | ----------- | --- | --- | --- |
(1) V isthepull-upreferencevoltagefortheassociateddataline.V isthemasterI2CmasterreferencevoltageandV -V
| DPUX |     |     | DPUM |     | DPU0 DPU3 |
| ---- | --- | --- | ---- | --- | --------- |
aretheslavechannelreferencevoltages.
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 3
ProductFolderLinks:TCA9546A

TCA9546A
| SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |     |     |     |     | www.ti.com |     |
| -------------------------------------- | --- | --- | --- | --- | ---------- | --- |
6 Specifications
Ratings(1)
| 6.1 Absolute Maximum |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | --- | --- | --- |
overoperatingfree-airtemperaturerange(unlessotherwisenoted)
|                      |     |     |     | MIN  | MAX | UNIT |
| -------------------- | --- | --- | --- | ---- | --- | ---- |
| V Supplyvoltagerange |     |     |     | –0.5 | 7   | V    |
CC
| V Inputvoltagerange(2) |     |     |     | –0.5 | 7   | V   |
| ---------------------- | --- | --- | --- | ---- | --- | --- |
I
| I I Inputcurrent |     |     |     |     | ±20 | mA  |
| ---------------- | --- | --- | --- | --- | --- | --- |
| I Outputcurrent  |     |     |     |     | ±25 | mA  |
O
| ContinuouscurrentthroughV |     |     |     |     | ±100 | mA  |
| ------------------------- | --- | --- | --- | --- | ---- | --- |
CC
| ContinuouscurrentthroughGND |     |     |     |     | ±100 | mA  |
| --------------------------- | --- | --- | --- | --- | ---- | --- |
| P Totalpowerdissipation     |     |     |     |     | 400  | mW  |
tot
| T A Operatingfree-airtemperaturerange |     |     |     | –40 | 85  | °C  |
| ------------------------------------- | --- | --- | --- | --- | --- | --- |
| T Storagetemperaturerange             |     |     |     | -65 | 150 | °C  |
stg
(1) Stressesbeyondthoselistedunder"absolutemaximumratings"maycausepermanentdamagetothedevice.Thesearestressratings
only,andfunctionaloperationofthedeviceattheseoranyotherconditionsbeyondthoseindicatedunder"recommendedoperating
conditions"isnotimplied.Exposuretoabsolute-maximum-ratedconditionsforextendedperiodsmayaffectdevicereliability.
(2) Theinputnegative-voltageandoutputvoltageratingsmaybeexceedediftheinputandoutputcurrentratingsareobserved.
6.2 ESD Ratings
|                          |                                                       |     |     | VALUE |     | UNIT |
| ------------------------ | ----------------------------------------------------- | --- | --- | ----- | --- | ---- |
|                          | Human-bodymodel(HBM),perANSI/ESDA/JEDECJS-001(1)      |     |     | ±4000 |     |      |
| V Electrostaticdischarge |                                                       |     |     |       |     | V    |
| (ESD)                    | Charged-devicemodel(CDM),perJEDECspecificationJESD22- |     |     |       |     |      |
|                          | C101(2)                                               |     |     | ±1500 |     |      |
(1) JEDECdocumentJEP155statesthat500-VHBMallowssafemanufacturingwithastandardESDcontrolprocess.Manufacturingwith
lessthan500-VHBMispossiblewiththenecessaryprecautions.
(2) JEDECdocumentJEP157statesthat250-VCDMallowssafemanufacturingwithastandardESDcontrolprocess.Manufacturingwith
lessthan250-VCDMispossiblewiththenecessaryprecautions.
| 6.3 Recommended | Operating | Conditions(1) |     |      |     |      |
| --------------- | --------- | ------------- | --- | ---- | --- | ---- |
|                 |           |               |     | MIN  | MAX | UNIT |
| V Supplyvoltage |           |               |     | 1.65 | 5.5 | V    |
CC
|                          |     | SCL,SDA     |     | 0.7×V CC | 6      |     |
| ------------------------ | --- | ----------- | --- | -------- | ------ | --- |
| V High-levelinputvoltage |     |             |     |          |        | V   |
| IH                       |     | A2–A0,RESET |     | 0.7×V    | V +0.5 |     |
CC CC
|                         |     | SCL,SDA |     | –0.5 | 0.3×V |     |
| ----------------------- | --- | ------- | --- | ---- | ----- | --- |
| V Low-levelinputvoltage |     |         |     |      | CC    | V   |
IL
|                                |     | A2–A0,RESET |     | –0.5 | 0.3×V CC |     |
| ------------------------------ | --- | ----------- | --- | ---- | -------- | --- |
| T Operatingfree-airtemperature |     |             |     | –40  | 85       | °C  |
A
(1) AllunusedinputsofthedevicemustbeheldatV CC orGNDtoensureproperdeviceoperation.RefertotheTIapplicationreport,
ImplicationsofSloworFloatingCMOSInputs,literaturenumberSCBA004.
| 6.4 Thermal Information |     |     |     |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | --- |
TCA9546A
|                                        | THERMALMETRIC(1) |     | D      | PW     |     | UNIT |
| -------------------------------------- | ---------------- | --- | ------ | ------ | --- | ---- |
|                                        |                  |     | 16PINS | 16PINS |     |      |
| R Junction-to-ambientthermalresistance |                  |     | 92.3   | 122.3  |     |      |
?JA
| R Junction-to-case(top)thermalresistance |     |     | 52.3 | 56.6 |     |     |
| ---------------------------------------- | --- | --- | ---- | ---- | --- | --- |
?JCtop
| R ?JB Junction-to-boardthermalresistance   |     |     | 50.1 | 57.4 |     | °C/W |
| ------------------------------------------ | --- | --- | ---- | ---- | --- | ---- |
| ? Junction-to-topcharacterizationparameter |     |     | 17.7 | 10.9 |     |      |
JT
| ? Junction-to-boardcharacterizationparameter |     |     | 49.8 | 66.8 |     |     |
| -------------------------------------------- | --- | --- | ---- | ---- | --- | --- |
JB
(1) Formoreinformationabouttraditionalandnewthermalmetrics,seetheSemiconductorandICPackageThermalMetricsapplication
report.
4 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
| www.ti.com |                               |     |     |     |     | SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |     |     |     |
| ---------- | ----------------------------- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- |
| 6.5        | Electrical Characteristics(1) |     |     |     |     |                                        |     |     |     |
overrecommendedoperatingfree-airtemperaturerange(unlessotherwisenoted)
|     | PARAMETER |     |     | TESTCONDITIONS |     | V   | MIN | TYP(2) MAX | UNIT |
| --- | --------- | --- | --- | -------------- | --- | --- | --- | ---------- | ---- |
CC
| V      | Power-onresetvoltage,V | CC  | Noload,    |      | V I =V C C or   |              |     | 1.2 1.5 | V   |
| ------ | ---------------------- | --- | ---------- | ---- | --------------- | ------------ | --- | ------- | --- |
| PORR   | rising                 |     |            |      | G ND(3 )        |              |     |         |     |
|        | Power-onresetvoltage,V |     |            |      | V =V or         |              |     |         |     |
| V      | falling(4)             | CC  | Noload,    |      | I ND(3 C ) C    |              | 0.8 | 1       |     |
| PORF   |                        |     |            |      | G               |              |     |         |     |
|        |                        |     |            |      |                 | 5V           |     | 3.6     |     |
|        |                        |     |            |      |                 | 4.5Vto5.5V   | 2.6 | 4.5     |     |
|        |                        |     |            |      |                 | 3.3V         |     | 1.9     |     |
|        |                        |     |            |      |                 | 3Vto3.6V     | 1.6 | 2.8     |     |
| V pass | Switchoutputvoltage    |     | V SWin =V  | CC , | I SWout =–100?A |              |     |         | V   |
|        |                        |     |            |      |                 | 2.5V         |     | 1.4     |     |
|        |                        |     |            |      |                 | 2.3Vto2.7V   | 1.0 | 1.8     |     |
|        |                        |     |            |      |                 | 1.8V         |     | 0.8     |     |
|        |                        |     |            |      |                 | 1.65Vto1.95V | 0.5 | 1.1     |     |
|        |                        |     | V OL =0.4V |      |                 |              | 3   | 7       |     |
| I OL   | SDA                    |     |            |      |                 | 1.65Vto5.5V  |     |         | mA  |
|        |                        |     | V =0.6V    |      |                 |              | 6   | 10      |     |
OL
|     | SCL,SDA         |     |     |     |     |     |     | ±1  |     |
| --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | SC3–SC0,SD3–SD0 |     |     |     |     |     |     | ±1  |     |
orGND(3)
| I I |       |     | V I =V CC |     |     | 1.65Vto5.5V |     |     | ?A  |
| --- | ----- | --- | --------- | --- | --- | ----------- | --- | --- | --- |
|     | A2–A0 |     |           |     |     |             |     | ±1  |     |
|     | RESET |     |           |     |     |             |     | ±1  |     |
|     |       |     |           |     |     | 5.5V        |     | 50  |     |
orGND(3)
|     |     |           | V I =V CC |     |     | 3.6V |     | 20  |     |
| --- | --- | --------- | --------- | --- | --- | ---- | --- | --- | --- |
|     |     | f =400kHz | I =0      |     |     |      |     |     |     |
|     |     | SCL       | O         |     |     |      |     |     |     |
|     |     |           | t =300ns  |     |     | 2.7V |     | 11  |     |
r,max
|     |     |     |     |     |     | 1.65V |     | 6   |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
Operatingmode
|     |     |     |     |     |     | 5.5V |     | 35  |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
V =V orGND(3)
|     |     |           | I CC |     |     | 3.6V |     | 14  |     |
| --- | --- | --------- | ---- | --- | --- | ---- | --- | --- | --- |
|     |     | f =100kHz | I =0 |     |     |      |     |     |     |
|     |     | SCL       | O    |     |     | 2.7V |     | 5   |     |
t r,max =1µs
|     |     |           |         |     |     | 1.65V |     | 2       |     |
| --- | --- | --------- | ------- | --- | --- | ----- | --- | ------- | --- |
| I   |     |           |         |     |     |       |     |         | ?A  |
| CC  |     |           |         |     |     | 5.5V  |     | 1.6     | 2   |
|     |     |           | =GND(3) |     |     | 3.6V  |     | 1.0 1.3 |     |
|     |     | Lowinputs | V I     |     |     |       |     |         |     |
I =0
|     |     |     | O   |     |     | 2.7V  |     | 0.7 1.1  |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | -------- | --- |
|     |     |     |     |     |     | 1.65V |     | 0.4 0.55 |     |
Standbymode
|     |     |            |      |     |     | 5.5V |     | 1.6     | 2   |
| --- | --- | ---------- | ---- | --- | --- | ---- | --- | ------- | --- |
|     |     |            | V =V |     |     | 3.6V |     | 1.0 1.3 |     |
|     |     | Highinputs | I CC |     |     |      |     |         |     |
|     |     |            | I =0 |     |     | 2.7V |     | 0.7 1.1 |     |
O
|     |     |     |     |     |     | 1.65V |     | 0.4 0.55 |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | -------- | --- |
SCLorSDAinputat0.6V,
|       |                |         | OtherinputsatV   |     | orGND(3)   | 1.65Vto5.5V |     | 2 15 |     |
| ----- | -------------- | ------- | ---------------- | --- | ---------- | ----------- | --- | ---- | --- |
|       | Supply-current |         |                  | CC  |            |             |     |      |     |
| ?I CC |                | SCL,SDA |                  |     |            |             |     |      | ?A  |
|       | change         |         | SCLorSDAinputatV |     | –0.6V,     |             |     |      |     |
|       |                |         |                  |     | C C        | 1.65Vto5.5V |     | 2 15 |     |
|       |                |         | OtherinputsatV   | CC  | or G ND(3) |             |     |      |     |
|       | A2–A0          |         |                  |     |            |             |     | 4.5  | 6   |
orGND(3)
| C i      |                 |     | V I =V CC |          |           | 1.65Vto5.5V |     |         | pF  |
| -------- | --------------- | --- | --------- | -------- | --------- | ----------- | --- | ------- | --- |
|          | RESET           |     |           |          |           |             |     | 4.5 5.5 |     |
| C        | SCL,SDA         |     |           |          |           |             |     | 15 19   |     |
| i o(OFF) |                 |     | V =V      | orGND(3) | SwitchOFF | 1.65Vto5.5V |     |         | pF  |
| (5 )     | SC3–SC0,SD3–SD0 |     | I CC      |          |           |             |     | 6       | 8   |
(1) Foroperationbetweenspecifiedvoltageranges,refertotheworst-caseparameterinbothapplicableranges.
(2) Alltypicalvaluesareatnominalsupplyvoltage(1.8-V,2.5-V,3.3-V,or5-VV CC ),T A =25°C.
| (3) RESET=V                                          | CC (heldhigh)whenallotherinputvoltages,V |     |     | I =GND. |     |     |     |     |     |
| ---------------------------------------------------- | ---------------------------------------- | --- | --- | ------- | --- | --- | --- | --- | --- |
| (4) Thepower-onresetcircuitresetstheI2CbuslogicwithV |                                          |     |     | <V      | .   |     |     |     |     |
CC PORF
(5) C dependsoninternalcapacitanceandexternalcapacitanceaddedtotheSCnlineswhenchannels(s)areON.
io(ON)
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 5
ProductFolderLinks:TCA9546A

TCA9546A
| SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |                    |     |             |     |     |     |     |     |     |     | www.ti.com |     |
| -------------------------------------- | ------------------ | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- |
| Electrical                             | Characteristics(1) |     | (continued) |     |     |     |     |     |     |     |            |     |
overrecommendedoperatingfree-airtemperaturerange(unlessotherwisenoted)
TYP(2)
|     | PARAMETER                |     |     |     | TESTCONDITIONS |           |            | V CC | MIN |      | MAX | UNIT |
| --- | ------------------------ | --- | --- | --- | -------------- | --------- | ---------- | ---- | --- | ---- | --- | ---- |
|     |                          |     |     |     |                |           | 4.5Vto5.5V |      |     | 4 10 | 16  |      |
|     |                          |     |     | V O | =0.4V          | I O =15mA |            |      |     |      |     |      |
|     |                          |     |     |     |                |           | 3Vto3.6V   |      |     | 5 13 | 20  |      |
| R   | Switchon-stateresistance |     |     |     |                |           |            |      |     |      |     | ?    |
ON
|         |           |        |              |     |       |         | 2.3Vto2.7V   |     |     | 7 16 | 45  |     |
| ------- | --------- | ------ | ------------ | --- | ----- | ------- | ------------ | --- | --- | ---- | --- | --- |
|         |           |        |              | V   | =0.4V | I =10mA |              |     |     |      |     |     |
|         |           |        |              | O   |       | O       | 1.65Vto1.95V |     | 10  | 25   | 70  |     |
| 6.6 I2C | Interface | Timing | Requirements |     |       |         |              |     |     |      |     |     |
overrecommendedoperatingfree-airtemperaturerange(unlessotherwisenoted)(seeFigure5)
|     |                   |     |     |     |     |     | STANDARDMODE |       | FASTMODE |        |     |      |
| --- | ----------------- | --- | --- | --- | --- | --- | ------------ | ----- | -------- | ------ | --- | ---- |
|     |                   |     |     |     |     |     | I2CBUS       |       |          | I2CBUS |     | UNIT |
|     |                   |     |     |     |     |     | MIN          | MAX   |          | MIN    | MAX |      |
| f   | I2Cclockfrequency |     |     |     |     |     |              | 0 100 |          | 0      | 400 | kHz  |
scl
| t   | I2Cclockhightime |     |     |     |     |     |     | 4   |     | 0.6 |     | ?s  |
| --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sch
I2Cclocklowtime
| t scl |              |     |     |     |     |     | 4.7 |     |     | 1.3 |     | ?s  |
| ----- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t     | I2Cspiketime |     |     |     |     |     |     | 50  |     |     | 50  | ns  |
sp
| t sds | I2Cserial-datasetuptime |     |     |     |     |     | 250  |     |     | 100  |     | ns  |
| ----- | ----------------------- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- |
| t     | I2Cserial-dataholdtime  |     |     |     |     |     | 0(1) |     |     | 0(1) |     | ?s  |
sdh
| t     | I2Cinputrisetime                  |     |     |                  |     |     |     | 1000 | 20+0.1C | (2) | 300 | ns  |
| ----- | --------------------------------- | --- | --- | ---------------- | --- | --- | --- | ---- | ------- | --- | --- | --- |
| icr   |                                   |     |     |                  |     |     |     |      |         | b   |     |     |
|       | I2Cinputfalltime                  |     |     |                  |     |     |     |      |         | (2) |     |     |
| t icf |                                   |     |     |                  |     |     |     | 300  | 20+0.1C | b   | 300 | ns  |
| t     | I2Coutputfalltime                 |     |     | 10-pFto400-pFbus |     |     |     | 300  | 20+0.1C | (2) | 300 | ns  |
| ocf   |                                   |     |     |                  |     |     |     |      |         | b   |     |     |
| t     | I2Cbusfreetimebetweenstopandstart |     |     |                  |     |     | 4.7 |      |         | 1.3 |     | ?s  |
buf
I2Cstartorrepeatedstartconditionsetup
| t sts |                                      |     |     |     |     |     | 4.7 |     |     | 0.6 |     | ?s  |
| ----- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t     | I2Cstartorrepeatedstartconditionhold |     |     |     |     |     |     | 4   |     | 0.6 |     | ?s  |
sth
| t   | I2Cstopconditionsetup |     |     |     |     |     |     | 4   |     | 0.6 |     | ?s  |
| --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sps
Valid-datatime(hightolow)(3)
| t vdL(Data) |     |     |     | SCLlowtoSDAoutputlowvalid |     |     |     | 1   |     |     |     | 1 ?s |
| ----------- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | ---- |
t Valid-datatime(lowtohigh)(3) SCLlowtoSDAoutputhighvalid 0.6 0.6 ?s
vdH(Data)
ACKsignalfromSCLlow
| t vd(ack) | Valid-datatimeofACKcondition |     |     |     |     |     |     | 1   |     |     |     | 1 ?s |
| --------- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
toSDAoutputlow
| C   | I2Cbuscapacitiveload |     |     |     |     |     |     | 400 |     |     | 400 | pF  |
| --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
b
(1) Adeviceinternallymustprovideaholdtimeofatleast300nsfortheSDAsignal(referredtotheV IH minoftheSCLsignal),inorderto
bridgetheundefinedregionofthefallingedgeofSCL.
(2) C =totalbuscapacitanceofonebuslineinpF
b
(3) Datatakenusinga1-k?pullupresistorand50-pFload(seeFigure5)
| 6.7 Switching |     | Characteristics |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
overrecommendedoperatingfree-airtemperaturerange,C ?100pF(unlessotherwisenoted)(seeFigure5)
L
|       |                      |           |      |        |         | FROM     |     | TO       |     |     |     |      |
| ----- | -------------------- | --------- | ---- | ------ | ------- | -------- | --- | -------- | --- | --- | --- | ---- |
|       |                      | PARAMETER |      |        |         |          |     |          |     | MIN | MAX | UNIT |
|       |                      |           |      |        |         | (INPUT)  |     | (OUTPUT) |     |     |     |      |
|       |                      |           | R ON | =20?,C | L =15pF |          |     |          |     |     | 0.3 |      |
| t (1) | Propagationdelaytime |           |      |        |         | SDAorSCL |     | SDnorSCn |     |     |     | ns   |
| pd    |                      |           | R    | =20?,C | =50pF   |          |     |          |     |     |     | 1    |
|       |                      |           | ON   |        | L       |          |     |          |     |     |     |      |
(1) ThepropagationdelayisthecalculatedRCtimeconstantofthetypicalON-stateresistanceoftheswitchandthespecifiedload
capacitance,whendrivenbyanidealvoltagesource(zerooutputimpedance).
6 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
| www.ti.com |           |     |       |        |              |     |     |     | SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |     |     |     |
| ---------- | --------- | --- | ----- | ------ | ------------ | --- | --- | --- | -------------------------------------- | --- | --- | --- |
| 6.8        | Interrupt | and | Reset | Timing | Requirements |     |     |     |                                        |     |     |     |
overrecommendedoperatingfree-airtemperaturerange(unlessotherwisenoted)
|      |                         |     |     |     | PARAMETER |     |     |     |     |     | MIN | MAX UNIT |
| ---- | ----------------------- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | -------- |
| t WL | Pulseduration,RESETlow  |     |     |     |           |     |     |     |     |     | 6   | ns       |
| t    | (1) RESETtime(SDAclear) |     |     |     |           |     |     |     |     |     |     | 500 ns   |
rst
| t REC(STA) | RecoverytimefromRESETtostart |     |     |     |     |     |     |     |     |     | 0   | ns  |
| ---------- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(1) t isthepropagationdelaymeasuredfromthetimetheRESETpinisfirstassertedlowtothetimetheSDApinisassertedhigh,
rst
|     | signalingastopcondition.Itmustbeaminimumoft |     |     |     |     | .   |     |     |     |     |     |     |
| --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
WL
| 6.9 | Typical | Characteristics |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 800     |                 |     |     |     |     | 1.8 |     |     |     |     |     |
VCC = 5.5V
|     | 700 VCC = 3.3V |     |     |     |     |     | 1.6 |     |     |     |     |     |
| --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
VCC = 1.65V
|     | 600 |     |     |     |     |     | )Aµ( edoM ybdnatS ,CCI 1.4 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- |
|     | 500 |     |     |     |     |     | 1.2                        |     |     |     |     |     |
)Vm( LOV
|     | 400 |     |     |     |     |     | 1   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 300 |     |     |     |     |     | 0.8 |     |     |     |     |     |
|     | 200 |     |     |     |     |     | 0.6 |     |     |     |     |     |
25ºC (Room Temperature)
|     | 100 |     |     |     |     |     | 0.4 |     |     | 85ºC |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
-40ºC
|     | 0   |     |          |     |     |       | 0.2 |     |       |         |       |       |
| --- | --- | --- | -------- | --- | --- | ----- | --- | --- | ----- | ------- | ----- | ----- |
|     | 0   | 2   | 4        | 6   | 8   | 10 12 | 1.5 | 2   | 2.5 3 | 3.5     | 4 4.5 | 5 5.5 |
|     |     |     | IOL (mA) |     |     |       |     |     |       | VCC (V) |       |       |
|     |     |     |          |     |     | D003  |     |     |       |         |       | D004  |
Figure1.SDAOutputLowVoltage(V OL )vsLoadCurrent Figure2.StandbyCurrent(I CC )vsSupplyVoltage(V CC )at
|     |     | (I OL | )atThreeV | CC  | Levels |     |     |     | ThreeTemperaturePoints |     |     |     |
| --- | --- | ----- | --------- | --- | ------ | --- | --- | --- | ---------------------- | --- | --- | --- |
|     | 6   |       |           |     |        |     | 30  |     |                        |     |     |     |
25ºC (Room Temperature)
|     | 5.8 |     |     | 85ºC |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 5.6 |     |     | -40º |     |     | 25  |     |     |     |     |     |
5.4
20
| )Fp( )FFO(OIC |     |     |     |     |     |     | )mhO( NOR |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- |
5.2
|     | 5   |     |     |     |     |     | 15  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4.8
10
4.6
|     | 4.4 |     |     |     |     |     |     |     |     | 25ºC (Room Temperature) |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- |
5
|     | 4.2 |     |     |     |     |     |     |     |     | 85ºC |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
-40ºC
|     | 4   |     |     |     |     |     | 0   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5
|     |     |     | VCC (V) |     |     |      |     |     |     | VCC (V) |     |      |
| --- | --- | --- | ------- | --- | --- | ---- | --- | --- | --- | ------- | --- | ---- |
|     |     |     |         |     |     | D006 |     |     |     |         |     | D001 |
Figure3.Slavechannel(SCn/SDn)capacitance(C )vs. Figure4.ON-Resistance(R )vsSupplyVoltage(V )at
|     |                 |     |                           |     |     | io(OFF) |     |     |                   | ON  |     | CC  |
| --- | --------------- | --- | ------------------------- | --- | --- | ------- | --- | --- | ----------------- | --- | --- | --- |
|     | SupplyVoltage(V |     | )atThreeTemperaturePoints |     |     |         |     |     | ThreeTemperatures |     |     |     |
CC
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 7
ProductFolderLinks:TCA9546A

TCA9546A
| SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |             |             |     |     |     |     |     |     | www.ti.com |
| -------------------------------------- | ----------- | ----------- | --- | --- | --- | --- | --- | --- | ---------- |
| 7 Parameter                            | Measurement | Information |     |     |     |     |     |     |            |
V
CC
RL= 1 k?
SDn, SCn
DUT
CL= 50 pF
(See Note 1)
Copyright © 2016,Texas Instruments Incorporated
I2C PORT LOAD CONFIGURATION
Two Bytes for Complete
Device Programming
| Stop                | Start Address |         |         | R/W   |     | Data  | Data  |     | Stop      |
| ------------------- | ------------- | ------- | ------- | ----- | --- | ----- | ----- | --- | --------- |
|                     |               | Address | Address |       | ACK |       |       | ACK |           |
| Condition Condition | Bit 7         |         |         | Bit 0 |     | Bit 7 | Bit 0 |     | Condition |
|                     |               | Bit 6   | Bit 1   |       | (A) |       |       | (A) |           |
| (P)                 | (S) (MSB)     |         |         | (LSB) |     | (MSB) | (LSB) |     | (P)       |
BYTE DESCRIPTION
1 I2C address + R/W
2 Control register data
|     | tscl |     | tsch |     |     |     |     |     |     |
| --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- |
0.7× VCC
| SCL  |     |      |     |     |     |             |      |     | 0.3× VCC |
| ---- | --- | ---- | --- | --- | --- | ----------- | ---- | --- | -------- |
|      |     |      |     |     |     | t v d ( A C | K )  |     |          |
|      |     | ticr |     |     |     |             | tsts |     |          |
|      |     |      |     |     |     | o r   t v d | L    |     |          |
| tbuf |     | ticf |     |     |     |             |      |     |          |
|      |     |      |     |     | tsp | t v         | d H  |     |          |
0.7× VCC
SDA
0.3× VCC
|     | ticf | ticr |     |     |      |     |      |     |     |
| --- | ---- | ---- | --- | --- | ---- | --- | ---- | --- | --- |
|     |      |      |     |     | tsdh |     | tsps |     |     |
tsth
|     |     | tsds |     |     |     | Repeat |     |      |     |
| --- | --- | ---- | --- | --- | --- | ------ | --- | ---- | --- |
|     |     |      |     |     |     | Start  |     | Stop |     |
Start or Repeat
|     |     |     |     |     |     | Condition | Condition |     |     |
| --- | --- | --- | --- | --- | --- | --------- | --------- | --- | --- |
Start Condition
VOLTAGE WAVEFORMS
| A. C L includesprobeandjigcapacitance. |     |     |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
B. All input pulses are supplied by generators having the following characteristics: PRR ? 10 MHz, Z = 50 ?,
O
t/t ?30ns.
r f
| C. Theoutputsaremeasuredoneatatime,withonetransitionpermeasurement. |     |     |     |     |     |     |     |     |     |
| ------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure5. I2CInterfaceLoad Circuit, ByteDescriptions,andVoltageWaveforms
8 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
www.ti.com SCPS205B–APRIL2014–REVISEDNOVEMBER2019
| Parameter | Measurement | Information | (continued)       |
| --------- | ----------- | ----------- | ----------------- |
| Start     |             |             | ACK or Read Cycle |
SCL
SDA
30%
trst
50%
RESET
tREC
tWL
|     | Figure6. | Reset Timing |     |
| --- | -------- | ------------ | --- |
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 9
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
8 Detailed Description
8.1 Overview
The TCA9546A is a 4-channel, bidirectional translating I2C switch. The master SCL/SDA signal pair is directed to
four channels of slave devices, SC0/SD0-SC3/SD3. Any individual downstream channel can be selected as well
asanycombinationofthefourchannels.
The device offers an active-low RESET input which resets the state machine and allows the TCA9546A to
recover should one of the downstream I2C buses get stuck in a low state. The state machine of the device can
alsoberesetbycyclingthepowersupply,V ,alsoknownasapower-on reset (POR). Both the RESET function
CC
andaPORwillcauseallchannelstobedeselected.
The connections of the I2C data path are controlled by the same I2C master device that is switched to
communicate with multiple I2C slaves. After the successful acknowledgment of the slave address (hardware
selectable by A0 and A1 pins), a single 8-bit control register is written to or read from to determine the selected
channels.
The TCA9546A may also be used for voltage translation, allowing the use of different bus voltages on each
SCn/SDn pair such that 1.8-V, 2.5-V, or 3.3-V parts can communicate with 5-V parts. This is achieved by using
externalpull-upresistors topullthebusuptothedesiredvoltagefor themaster andeachslavechannel.
8.2 Functional Block Diagram
TCA9546A
5
SC0
7
SC1
SC2 10
12
SC3
SD0 4
SD1 6
SD2 9
SD3 11
Switch Control Logic
GND 8
VCC 16
RESET 3 Power-On Reset
SCL 14 1 A0
2
15 Input Filter I2C Bus Control A1
SDA 13
A2
10 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
www.ti.com SCPS205B–APRIL2014–REVISEDNOVEMBER2019
8.3 Feature Description
The TCA9546A is a 4-channel, bidirectional translating switch for I2C buses that supports Standard-Mode (100
kHz)andFast-Mode(400 kHz) operation. The TCA9546A features I2C control using a single 8-bit control register
in which the four least significant bits control the enabling and disabling of the 4 switch channels of I2C data flow.
Depending on the application, voltage translation of the I2C bus can also be achieved using the TCA9546A to
allow1.8-V, 2.5-V,or3.3-Vpartstocommunicatewith5-Vparts.Additionally, in the event that communication on
the I2C bus enters a fault state, the TCA9546A can be reset to resume normal operation using the RESET pin
featureorbyapower-onresetwhichresultsfromcyclingpower tothedevice.
8.4 Device Functional Modes
8.4.1 RESETInput
TheRESETinputisanactive-lowsignalthat may be used to recover from a bus-fault condition. When this signal
is asserted low for a minimum of t , the TCA9546A resets its registers and I2C state machine and deselects all
WL
channels.TheRESET inputmustbeconnectedtoV throughapull-upresistor.
CC
8.4.2 Power-OnReset
When power is applied to V , an internal power-on reset holds the TCA9546A in a reset condition until V has
CC CC
reached V . At this point, the reset condition is released, and the TCA9546A registers and I2C state machine
POR
are initialized to their default states, all zeroes, causing all the channels to be deselected. Thereafter, V must
CC
beloweredbelowV toresetthedevice.
POR
8.5 Programming
8.5.1 I2CInterface
The I2C bus is for two-way two-line communication between different ICs or modules. The two lines are a serial
data line (SDA) and a serial clock line (SCL). Both lines must be connected to a positive supply via a pullup
resistor when connected to the output stages of a device. Data transfer can be initiated only when the bus is not
busy.
One data bit is transferred during each clock pulse. The data on the SDA line must remain stable during the high
periodoftheclockpulse,aschangesinthedatalineatthistimeareinterpretedascontrolsignals(seeFigure 7).
SDA
SCL
Data Line Change
Stable; of Data
Data Valid Allowed
Figure7. BitTransfer
Both data and clock lines remain high when the bus is not busy. A high-to-low transition of the data line while the
clock is high is defined as the start condition (S). A low-to-high transition of the data line while the clock is high is
definedasthestopcondition(P)(seeFigure8).
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 11
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
Programming (continued)
SDA
SCL
|     | S                                           |     |     | P              |     |
| --- | ------------------------------------------- | --- | --- | -------------- | --- |
|     | Start Condition                             |     |     | Stop Condition |     |
|     | Figure8. DefinitionofStartandStopConditions |     |     |                |     |
A device generating a message is a transmitter; a device receiving is the receiver. The device that controls the
messageisthemaster,andthedevicesthatarecontrolledbythemaster aretheslaves(seeFigure9).
SDA
SCL
I2C
| Master       |          | Slave        |             | Master       |             |
| ------------ | -------- | ------------ | ----------- | ------------ | ----------- |
|              | Slave    |              | Master      | Transmitter/ | Multiplexer |
| Transmitter/ |          | Transmitter/ |             |              |             |
| Receiver     | Receiver | Receiver     | Transmitter | Receiver     |             |
Slave
Figure9. SystemConfiguration
Thenumberofdatabytestransferredbetweenthestartand the stop conditions from transmitter to receiver is not
limited. Each byte of eight bits is followed by one acknowledge (ACK) bit. The transmitter must release the SDA
linebeforethereceivercansendanACKbit.
When a slave receiver is addressed, it must generate an ACK after the reception of each byte. Also, a master
must generate an ACK after the reception of each byte that has been clocked out of the slave transmitter. The
device that acknowledges must pull down the SDA line during the ACK clock pulse so that the SDA line is stable
low during the high pulse of the ACK-related clock period (see Figure 10). Setup and hold times must be taken
intoaccount.
12 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
www.ti.com SCPS205B–APRIL2014–REVISEDNOVEMBER2019
Programming (continued)
Data Output
by Transmitter
NACK
Data Output
by Receiver
ACK
SCL From
|     |     | 1   | 2   |     | 8   | 9   |
| --- | --- | --- | --- | --- | --- | --- |
Master
S
|     | Start |     |     |     | Clock Pulse for ACK |     |
| --- | ----- | --- | --- | --- | ------------------- | --- |
Condition
Figure10. AcknowledgmentontheI2CBus
DataistransmittedtotheTCA9546AcontrolregisterusingthewritemodeshowninFigure11.
Slave Address
Control Register
| S   | 1 1 1 0 A2 | A1 A0 0 | A X X | X X B3 B2 | B1 B0 A P |     |
| --- | ---------- | ------- | ----- | --------- | --------- | --- |
SDA
Start Condition R/W ACK From Slave ACK From Slave Stop Condition
|     |     | Figure11. WriteControlRegister |     |     |     |     |
| --- | --- | ------------------------------ | --- | --- | --- | --- |
DataisreadfromtheTCA9546AcontrolregisterusingthereadmodeshowninFigure12.
|       | Slave Address |       |     | Control Register |          |     |
| ----- | ------------- | ----- | --- | ---------------- | -------- | --- |
| SDA S | 1 1 1         | 1     | A   |                  | NA P     |     |
|       | 0 A2          | A1 A0 | 0 0 | 0 0 B3           | B2 B1 B0 |     |
Start Condition R/W ACK From Slave NACK From Master Stop Condition
|     |     | Figure12. ReadControlRegister |     |     |     |     |
| --- | --- | ----------------------------- | --- | --- | --- | --- |
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 13
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
8.6 Control Register
8.6.1 DeviceAddress
Following a start condition, the bus master must output the address of the slave it is accessing. The address of
the TCA9546A is shown in Figure 13. To conserve power, no internal pullup resistors are incorporated on the
hardware-selectableaddresspins,andtheymust bepulledhighorlow.
Slave Address
1 1 1 0 A2 A1 A0 R/W
Fixed Hardware
Selectable
Figure13. TCA9546AAddress
The last bit of the slave address defines the operation to be performed. When set to a logic 1, a read is selected,
whilealogic0selectsawriteoperation.
8.6.2 Control Register Description
Following the successful acknowledgment of the slave address, the bus master sends a byte to the TCA9546A,
whichisstoredinthecontrolregister(seeFigure14). If multiple bytes are received by the TCA9546A, it will save
thelastbytereceived.ThisregistercanbewrittenandreadviatheI2Cbus.
Channel Selection Bits
(Read/Write)
7 6 5 4 3 2 1 0
X X X X B3 B2 B1 B0
Channel 0
Channel 1
Channel 2
Channel 3
Figure14. ControlRegister
8.6.3 Control Register Definition
One or several SCn/SDn downstream pairs, or channels, are selected by the contents of the control register (see
Table 1). This register is written after the TCA9546A has been addressed. The four LSBs of the control byte are
used to determine which channel or channels are to be selected. When a channel is selected, the channel
becomesactiveafterastopcondition has been placed on the I2C bus. This ensures that all SCn/SDn lines are in
a high state when the channel is made active, so that no false conditions are generated at the time of
connection.Astopconditionalwaysmustoccur rightaftertheacknowledgecycle.
14 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
| www.ti.com                   |     |     | SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |     |
| ---------------------------- | --- | --- | -------------------------------------- | --- |
| Control Register (continued) |     |     |                                        |     |
Write(ChannelSelection),ControlRegisterRead(ChannelStatus)(1)
Table1.ControlRegister
| B7 B6 | B5 B4 | B3 B2 | B1 B0 | COMMAND |
| ----- | ----- | ----- | ----- | ------- |
0 Channel0disabled
| X X | X X | X X | X   |     |
| --- | --- | --- | --- | --- |
1 Channel0enabled
0 Channel1disabled
| X X | X X | X X | X   |     |
| --- | --- | --- | --- | --- |
1 Channel1enabled
0 Channel2disabled
| X X | X X | X   | X X |     |
| --- | --- | --- | --- | --- |
1 Channel2enabled
0 Channel3disabled
| X X | X X | X   | X X |     |
| --- | --- | --- | --- | --- |
1 Channel3enabled
Nochannelselected,
| 0 0 | 0 0 | 0 0 | 0 0 |     |
| --- | --- | --- | --- | --- |
power-up/resetdefaultstate
(1) Severalchannelscanbeenabledatthesametime.Forexample,B3=0,B2=1,B1=1,B0=0meansthatchannels0and3are
disabled,andchannels1and2areenabled.Careshouldbetakennottoexceedthemaximumbuscapacity.
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 15
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
9 Application and Implementation
9.1 Application Information
Applications of the TCA9546A contains an I2C (or SMBus) master device and up to four I2C slave devices. The
downstream channels are ideally used to resolve I2C slave address conflicts. For example, if four identical digital
temperaturesensorsareneededintheapplication,onesensorcanbeconnectedateachchannel: 0,1, 2, and3.
When the temperature at a specific location needs to be read, the appropriate channel can be enabled and all
other channels switched off, the data can be retrieved, and the I2C master can move on and read the next
channel.
In an application where the I2C bus contain many additional slave devices that do not result in I2C slave address
conflicts, these slave devices can be connected to any desired channel to distribute the total bus capacitance
across multiple channels. If multiple switches will be enabled simultaneously, additional design requirements
mustbeconsidered(SeeDesignRequirementsandDetailedDesignProcedure).
9.2 Typical Application
A typical application of the TCA9546A contains anywhere from 1 to 5 separate data pull-up voltages, V , one
DPUX
for the master device (V ) and one for each of the selectable slave channels (V – V ). In the event
DPUM DPU0 DPU3
wherethemasterdeviceandallslavedevicesoperate at the same voltage, then the pass voltage, V = V .
pass DPUX
Once the maximum V is known, V can be selected easily using Figure 16. In an application where voltage
pass cc
translationisnecessary,additionaldesignrequirementsmust beconsidered(SeeDesignRequirements).
Figure15showsanapplicationinwhichtheTCA9546Acanbeused.
V = 1.65 V to 5.5 V
DPUM
V = 2.5 V
CC
V = 1.65 V to 5.5 V
DPU0
16
VCC
15 4
SDA SDA SD0
I2C/SMBus 14 5 Channel 0
SCL SCL SC0
Master
3 V = 1.65 V to 5.5 V
RESET DPU1
SD1 6
7 Channel 1
SC1
V = 1.65 V to 5.5 V
TCA9546A DPU2
9
SD2
Channel 2
10
SC2
V = 1.65 V to 5.5 V
DPU3
13
A2
2
A1 11
1 A0 SD3
8 GND SC3 12 Channel 3
Figure15. TCA9546ATypical ApplicationSchematic
16 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
www.ti.com SCPS205B–APRIL2014–REVISEDNOVEMBER2019
Typical Application (continued)
9.2.1 Design Requirements
TheA0,A1,andA2pinsarehardware selectable to control the slave address of the TCA9546A. These pins may
betieddirectlytoGNDorV intheapplication.
CC
If multiple slave channels will be activated simultaneously in the application, then the total I from SCL/SDA to
OL
GND onthemastersidewillbethesumofthecurrentsthroughallpull-upresistors, R .
p
The pass-gate transistors of the TCA9546A are constructed such that the V voltage can be used to limit the
CC
maximumvoltagethatispassedfromoneI2Cbustoanother.
Figure16showsthevoltagecharacteristicsofthepass-gatetransistors(notethat thegraphwas generated using
data specified in the Electrical Characteristics section of this data sheet). In order for the TCA9546A to act as a
voltage translator, the V voltage must be equal to or lower than the lowest bus voltage. For example, if the
pass
mainbusisrunningat5Vandthedownstreambusesare3.3Vand2.7V,V must be equal to or below 2.7 V
pass
toeffectivelyclamp the downstream bus voltages. As shown in Figure 16, V is 2.7 V when the TCA9546A
pass(max)
supply voltage is 4 V or lower, so the TCA9546A supply voltage could be set to 3.3 V. Pull-up resistors then can
beusedtobringthebusvoltagestotheirappropriatelevels(seeFigure15).
9.2.2 DetailedDesignProcedure
Once all the slaves are assigned to the appropriate slave channels and bus voltages are identified, the pull-up
resistors, R , for each of the buses need to be selected appropriately. The minimum pull-up resistance is a
p
functionofV ,V ,andI :
DPUX OL,(max) OL
V -V
R = DPUX OL(max)
p(min) I
OL (1)
Themaximumpull-upresistanceisafunctionofthe maximum rise time, t (300 ns for fast-mode operation, f =
r SCL
400kHz)andbuscapacitance,C :
b
t
R = r
p(max) 0.8473´C
b (2)
The maximum bus capacitance for an I2C bus must not exceed 400 pF for fast-mode operation. The bus
capacitance can be approximated by adding the capacitance of the TCA9546A, C , the capacitance of
io(OFF)
wires/connections/traces, and the capacitance of each individual slave on a given channel. If multiple channels
willbeactivatedsimultaneously,eachoftheslavesonallchannelswillcontributetototalbuscapacitance.
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 17
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
| Typical Application | (continued) |     |     |     |     |     |     |     |     |
| ------------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
9.2.3 TCA9546AApplicationCurves
| 5                       |     |     |     |     | 25  |     |     |     |               |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- |
| 25ºC (Room Temperature) |     |     |     |     |     |     |     |     | Standard-mode |
| 85ºC                    |     |     |     |     |     |     |     |     | Fast-mode     |
| 4 -40ºC                 |     |     |     |     | 20  |     |     |     |               |
)mhOk( )xam(pR
| 3   |     |     |     |     | 15  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
)V( ssapV
| 2   |     |     |     |     | 10  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1   |     |     |     |     | 5   |     |     |     |     |
| 0   |     |     |     |     | 0   |     |     |     |     |
0 0.5 1 1.5 2 2.5 3 3.5 4 4.5 5 5.5 0 50 100 150 200 250 300 350 400 450
|     |     | VCC (V) |     |     |     |     |     | Cb (pF) |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | ------- | --- |
D007 D008
| Standard-mode |     | SPACE |        |     | Standard-mode |           |       | Fast-mode |                  |
| ------------- | --- | ----- | ------ | --- | ------------- | --------- | ----- | --------- | ---------------- |
| (f kHz,t      |     | (f    | kHz,t) |     | (f            | =100kHz,t | =1µs) | (f        | =400kHz,t=300ns) |
| SCL r         |     | SCL   | r      |     | SCL           |           | r     | SCL       | r                |
Figure16.Pass-GateVoltage(V )vsSupplyVoltage Figure17.MaximumPull-Upresistance(R )vsBus
|     |                              |     | pass |     |     |     |               |     | p(max) |
| --- | ---------------------------- | --- | ---- | --- | --- | --- | ------------- | --- | ------ |
|     | (V )atThreeTemperaturePoints |     |      |     |     |     | Capacitance(C |     | )      |
|     | CC                           |     |      |     |     |     |               |     | b      |
1.8
1.6
1.4
1.2
)mhOk( )nim(pR
1
0.8
0.6
0.4
|     |     | 0.2 |     |     |     |     | VDPUX > 2V |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- |
VDPUX <= 2
0
|     |     |     | 0 0.5 | 1 1.5 2 | 2.5 3 | 3.5 4 | 4.5 5 5.5 |     |     |
| --- | --- | --- | ----- | ------- | ----- | ----- | --------- | --- | --- |
VDPUX (V)
D009
|     |                                     |     | V =0.2*V  | ,I        | =2mAwhenV |                              | ?2V |     |        |
| --- | ----------------------------------- | --- | --------- | --------- | --------- | ---------------------------- | --- | --- | ------ |
|     |                                     |     | OL        | DPUX OL   |           | DPUX                         |     |     |        |
|     |                                     |     | V =0.4V,I | =3mAwhenV |           | >2V                          |     |     |        |
|     |                                     |     | OL        | OL        |           | DPUX                         |     |     |        |
|     | Figure18.MinimumPull-UpResistance(R |     |           |           | p(min)    | )vsPull-UpReferenceVoltage(V |     |     | DPUX ) |
18 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
| www.ti.com |                        |     |     | SCPS205B–APRIL2014–REVISEDNOVEMBER2019 |     |     |
| ---------- | ---------------------- | --- | --- | -------------------------------------- | --- | --- |
| 10 Power   | Supply Recommendations |     |     |                                        |     |     |
The operating power-supply voltage range of the TCA9546A is 1.65 V to 5.5 V applied at the VCC pin. When the
TCA9546A is powered on for the first time or anytime the device needs to be reset by cycling the power supply,
thepower-onresetrequirementsmustbefollowedtoensuretheI2Cbuslogicisinitializedproperly.
| 10.1 Power-On | Reset Requirements |     |     |     |     |     |
| ------------- | ------------------ | --- | --- | --- | --- | --- |
In the event of a glitch or data corruption, TCA9546A can be reset to its default conditions by using the power-on
reset feature. Power-on reset requires that the device go through a power cycle to be completely reset. This
resetalsohappenswhenthedeviceispoweredonfor thefirsttimeinanapplication.
Apower-onresetisshowninFigure19.
V
CC
|     | Ramp-Down |     |     | Ramp-Up |     |     |
| --- | --------- | --- | --- | ------- | --- | --- |
V
CC_TRR
| V drops below V | –50 mV |     |     |     |     |     |
| --------------- | ------ | --- | --- | --- | --- | --- |
| CC              | PORF   |     |     |     |     |     |
Time
Time to Re-Ramp
|     |     | V     |     | V     |     |     |
| --- | --- | ----- | --- | ----- | --- | --- |
|     |     | CC_FT |     | CC_RT |     |     |
Figure19. V isLowered Below thePORThreshold,ThenRampedBackUptoV
CC CC
Table2specifiestheperformanceofthepower-onresetfeaturefor TCA9546Afor bothtypesofpower-onreset.
Table2.RecommendedSupplySequencingAndRampRates(1)
|     |          | PARAMETER |     |             | MIN TYP | MAX UNIT |
| --- | -------- | --------- | --- | ----------- | ------- | -------- |
| V   | Falltime |           |     | SeeFigure19 | 1       | 100 ms   |
CC_FT
| V   | Risetime |     |     | SeeFigure19 | 0.1 | 100 ms |
| --- | -------- | --- | --- | ----------- | --- | ------ |
CC_RT
|          | Timetore-ramp(whenV | CC dropsbelowV | PORF(min) –50mVor |             |     |     |
| -------- | ------------------- | -------------- | ----------------- | ----------- | --- | --- |
| V CC_TRR |                     |                |                   | SeeFigure19 | 40  | ?s  |
whenV CC dropstoGND)
|       | LevelthatV canglitchdownto,butnotcauseafunctional |      |     |             |     |       |
| ----- | ------------------------------------------------- | ---- | --- | ----------- | --- | ----- |
| V     | CC                                                |      |     | SeeFigure20 |     | 1.2 V |
| CC_GH | disruptionwhenV                                   | =1?s |     |             |     |       |
CC_GW
V Glitchwidththatwillnotcauseafunctionaldisruptionwhen SeeFigure20 10 ?s
| CC_GW | V =0.5×V                        |     |     |             |     |        |
| ----- | ------------------------------- | --- | --- | ----------- | --- | ------ |
|       | CC_GH CC                        |     |     |             |     |        |
| V     | VoltagetrippointofPORonfallingV |     |     | SeeFigure21 | 0.8 | 1.25 V |
| PORF  |                                 |     | CC  |             |     |        |
V PORR VoltagetrippointofPORonrisingV CC SeeFigure21 1.05 1.5 V
| (1) AllsupplysequencingandrampratevaluesaremeasuredatT |     |     | =25°C |     |     |     |
| ------------------------------------------------------ | --- | --- | ----- | --- | --- | --- |
A
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 19
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
Glitches in the power supply can also affect the power-on reset performance of this device. The glitch width
(V ) and height (V ) are dependent on each other. The bypass capacitance, source impedance, and
CC_GW CC_GH
device impedance are factors that affect power-on reset performance. Figure 20 and Table 2 provide more
informationonhowtomeasurethesespecifications.
V
CC
V
CC_GH
Time
V
CC_GW
Figure20. GlitchWidthandGlitchHeight
V is critical to the power-on reset. V is the voltage level at which the reset condition is released and all the
POR POR
registers and the I2C/SMBus state machine are initialized to their default states. The value of V differs based
POR
ontheV beingloweredtoorfrom0.Figure21andTable2providemoredetailsonthisspecification.
CC
V
CC
V
PORR
V
PORF
Time
POR
Time
Figure21. V
POR
20 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

TCA9546A
www.ti.com SCPS205B–APRIL2014–REVISEDNOVEMBER2019
11 Layout
11.1 Layout Guidelines
For PCB layout of the TCA9546A, common PCB layout practices should be followed but additional concerns
related to high-speed data transfer such as matched impedances and differential pairs are not a concern for I2C
signal speeds. It is common to have a dedicated ground plane on an inner layer of the board and pins that are
connected to ground should have a low-impedance path to the ground plane in the form of wide polygon pours
and multiple vias. By-pass and de-coupling capacitors are commonly used to control the voltage on the VCC pin,
using a larger capacitor to provide additional power in the event of a short power supply glitch and a smaller
capacitor tofilterouthigh-frequencyripple.
In an application where voltage translation is not required, all V voltages and V could be at the same
|     |     |     | DPUX | CC  |
| --- | --- | --- | ---- | --- |
potential and a single copper plane could connect all of pull-up resistors to the appropriate reference voltage. In
an application where voltage translation is required, V , V , V , V , and V may all be on the
|     |     | DPUM DPU0 | DPU1 DPU2 | DPU3 |
| --- | --- | --------- | --------- | ---- |
samelayeroftheboardwithsplitplanestoisolatedifferent voltagepotentials.
ToreducethetotalI2CbuscapacitanceaddedbyPCBparasitics, datalines(SCnandSDn)should be a short as
possibleandthewidthsofthetracesshouldalsobeminimized(e.g. 5-10milsdependingoncopperweight).
11.2 Layout Example
LEGEND
| Partial Power Plane | Polygonal |     |     |     |
| ------------------- | --------- | --- | --- | --- |
To I2C Master
Copper Pour
VIAto Power Plane
VIAto GND Plane (Inner Layer)
V
DPUM
By-pass/De-coupling
capacitors
| V    | GND |     | V   |     |
| ---- | --- | --- | --- | --- |
| DPU0 |     |     | CC  |     |
0 lennahC evalS oT
|     | A0  |     | VCC |     |
| --- | --- | --- | --- | --- |
V
DPU3
|     | A1  |     | SDA |     |
| --- | --- | --- | --- | --- |
To Slave Channel 3
|     | RESET |          | SCL |     |
| --- | ----- | -------- | --- | --- |
|     | SD0   | A6459ACT | A2  |     |
|     | SC0   |          | SC3 |     |
|     | SD1   |          | SD3 |     |
1 lennahC evalS oT
|     | SC1 |     | SC2 |     |
| --- | --- | --- | --- | --- |
|     | GND |     | SD2 | V   |
DPU2 To Slave Channel 2
GND
V
DPU1
Copyright©2014–2019,TexasInstrumentsIncorporated SubmitDocumentationFeedback 21
ProductFolderLinks:TCA9546A

TCA9546A
SCPS205B–APRIL2014–REVISEDNOVEMBER2019 www.ti.com
| 12 Device      | and Documentation | Support          |         |
| -------------- | ----------------- | ---------------- | ------- |
| 12.1 Receiving | Notification      | of Documentation | Updates |
To receive notification of documentation updates, navigate to the device product folder on ti.com. In the upper
right corner, click on Alert me to register and receive a weekly digest of any product information that has
changed.Forchangedetails,reviewtherevisionhistoryincludedinanyreviseddocument.
| 12.2 Support | Resources |     |     |
| ------------ | --------- | --- | --- |
TI E2E™ support forums are an engineer's go-to source for fast, verified answers and design help — straight
fromtheexperts.Searchexistinganswersoraskyourownquestiontogetthequickdesignhelpyouneed.
Linked content is provided "AS IS" by the respective contributors. They do not constitute TI specifications and do
notnecessarilyreflectTI'sviews;seeTI'sTermsofUse.
12.3 Trademarks
E2EisatrademarkofTexasInstruments.
| Allothertrademarksaretheproperty |           | oftheirrespectiveowners. |     |
| -------------------------------- | --------- | ------------------------ | --- |
| 12.4 Electrostatic               | Discharge | Caution                  |     |
This integrated circuit can be damaged by ESD. Texas Instruments recommends that all integrated circuits be handled with
appropriateprecautions.Failuretoobserveproperhandlingandinstallationprocedurescancausedamage.
ESDdamagecanrangefromsubtleperformancedegradationtocompletedevicefailure.Precisionintegratedcircuitsmaybemore
susceptibletodamagebecauseverysmallparametricchangescouldcausethedevicenottomeetitspublishedspecifications.
12.5 Glossary
| SLYZ022—TI                                  | Glossary.  |               |                 |
| ------------------------------------------- | ---------- | ------------- | --------------- |
| Thisglossarylistsandexplainsterms,acronyms, |            |               | anddefinitions. |
| 13 Mechanical,                              | Packaging, | and Orderable | Information     |
Thefollowingpagesincludemechanical,packaging, andorderableinformation.Thisinformationisthemost
currentdataavailableforthedesignateddevices.Thisdataissubject tochangewithoutnoticeandrevision of
thisdocument.Forbrowser-basedversionsofthisdatasheet, refertotheleft-handnavigation
22 SubmitDocumentationFeedback Copyright©2014–2019,TexasInstrumentsIncorporated
ProductFolderLinks:TCA9546A

PACKAGE OPTION ADDENDUM
www.ti.com 10-Apr-2026
PACKAGING INFORMATION
Orderable part number Status Material type Package | Pins Package qty | Carrier RoHS Lead finish/ MSL rating/ Op temp (°C) Part marking
(1) (2) (3) Ball material Peak reflow (6)
(4) (5)
TCA9546ADR Active Production SOIC (D) | 16 2500 | LARGE T&R Yes NIPDAU Level-1-260C-UNLIM -40 to 85 TCA9546A
TCA9546ADR.B Active Production SOIC (D) | 16 2500 | LARGE T&R Yes NIPDAU Level-1-260C-UNLIM -40 to 85 TCA9546A
TCA9546APWR Active Production TSSOP (PW) | 16 2000 | LARGE T&R Yes NIPDAU | SN Level-1-260C-UNLIM -40 to 85 PW546A
TCA9546APWR.B Active Production TSSOP (PW) | 16 2000 | LARGE T&R Yes NIPDAU Level-1-260C-UNLIM -40 to 85 PW546A
TCA9546APWRG4 Active Production TSSOP (PW) | 16 2000 | LARGE T&R Yes NIPDAU Level-1-260C-UNLIM -40 to 85 PW546A
TCA9546APWRG4.B Active Production TSSOP (PW) | 16 2000 | LARGE T&R Yes NIPDAU Level-1-260C-UNLIM -40 to 85 PW546A
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
In no event shall TI's liability arising out of such information exceed the total purchase price of the TI part(s) at issue in this document sold by TI to Customer on an annual basis.
Addendum-Page 1

PACKAGE OPTION ADDENDUM
www.ti.com 10-Apr-2026
Addendum-Page 2

PACKAGE MATERIALS INFORMATION
|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
www.ti.com 18-Oct-2026
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
TCA9546ADR SOIC D 16 2500 330.0 16.4 6.5 10.3 2.1 8.0 16.0 Q1
TCA9546APWR TSSOP PW 16 2000 330.0 12.4 6.9 5.6 1.6 8.0 12.0 Q1
TCA9546APWR TSSOP PW 16 2000 330.0 12.4 6.9 5.3 1.6 8.0 12.0 Q1
TCA9546APWR TSSOP PW 16 2000 330.0 12.4 6.9 5.6 1.6 8.0 12.0 Q1
TCA9546APWRG4 TSSOP PW 16 2000 330.0 12.4 6.9 5.6 1.6 8.0 12.0 Q1
Pack Materials-Page 1

PACKAGE MATERIALS INFORMATION
|            |     |     |     |     |     |             |
| ---------- | --- | --- | --- | --- | --- | ----------- |
| www.ti.com |     |     |     |     |     | 18-Oct-2026 |
TAPE AND REEL BOX DIMENSIONS
Width (mm)
H
W L

*All dimensions are nominal
Device Package Type Package Drawing Pins SPQ Length (mm) Width (mm) Height (mm)
| TCA9546ADR    | SOIC  | D   | 16 2500 | 353.0 | 353.0 | 32.0 |
| ------------- | ----- | --- | ------- | ----- | ----- | ---- |
| TCA9546APWR   | TSSOP | PW  | 16 2000 | 353.0 | 353.0 | 32.0 |
| TCA9546APWR   | TSSOP | PW  | 16 2000 | 367.0 | 367.0 | 35.0 |
| TCA9546APWR   | TSSOP | PW  | 16 2000 | 356.0 | 356.0 | 35.0 |
| TCA9546APWRG4 | TSSOP | PW  | 16 2000 | 353.0 | 353.0 | 32.0 |
Pack Materials-Page 2

PACKAGE OUTLINE
PW0016A TSSOP - 1.2 mm max height
SCALE 2.500
SMALL OUTLINE PACKAGE
SEATING
PLANE
C
6.6
TYP
6.2
A
0.1 C
PIN 1 INDEX AREA
14X 0.65
16
1
2X
5.1 4.55
4.9
NOTE 3
4X (0 -12 )
8
9
0.30
B 4.5 16X 0.17 1.2 MAX
4.3
0.1 C A B
NOTE 4
(0.15) TYP
SEE DETAIL A
0.25
GAGE PLANE
0.15
0.05
0.75
0.50
0 -8
DETA 20AIL A
TYPICAL
4220204/B 12/2023
NOTES:
1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. This dimension does not include mold flash, protrusions, or gate burrs. Mold flash, protrusions, or gate burrs shall not
exceed 0.15 mm per side.
4. This dimension does not include interlead flash. Interlead flash shall not exceed 0.25 mm per side.
5. Reference JEDEC registration MO-153.
www.ti.com

EXAMPLE BOARD LAYOUT
PW0016A TSSOP - 1.2 mm max height
SMALL OUTLINE PACKAGE
16X (1.5) SYMM
(R0.05) TYP
1
16X (0.45) 16
SYMM
14X (0.65)
8 9
(5.8)
LAND PATTERN EXAMPLE
EXPOSED METAL SHOWN
SCALE: 10X
SOLDER MASK METAL UNDER SOLDER MASK
OPENING METAL SOLDER MASK OPENING
EXPOSED METAL EXPOSED METAL
0.05 MAX 0.05 MIN
ALL AROUND ALL AROUND
NON-SOLDER MASK SOLDER MASK
DEFINED DEFINED
(PREFERRED) SOLDE15.000R MASK DETAILS
4220204/B 12/2023
NOTES: (continued)
6. Publication IPC-7351 may have alternate designs.
7. Solder mask tolerances between and around signal pads can vary based on board fabrication site.
www.ti.com

EXAMPLE STENCIL DESIGN
PW0016A TSSOP - 1.2 mm max height
SMALL OUTLINE PACKAGE
16X (1.5) SYMM
(R0.05) TYP
1
16X (0.45) 16
SYMM
14X (0.65)
8 9
(5.8)
SOLDER PASTE EXAMPLE
BASED ON 0.125 mm THICK STENCIL
SCALE: 10X
4220204/B 12/2023
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
