0.01 -80 V+
%)
e
(
s N oi 0.001 -100
+
n
o
st
orti
0.0001 -120 Di
c o ni Pre-Output Driver OUT
ar m 0.00001 -140
al H IN- Tot
0.000001 -160 IN+
V-
Total
Harmonic
Distortion
+
Noise
(dB)
Product Sample & Technical Tools & Support &
Folder Buy Documents Software Community
OPA1611,OPA1612
SBOS450C–JULY2009–REVISEDAUGUST2014
OPA161x SoundPlus™ High-Performance, Bipolar-Input Audio Operational Amplifiers
1 Features 3 Description
• SuperiorSoundQuality The OPA1611 (single) and OPA1612 (dual) bipolar-
1 input operational amplifiers achieve very low
• UltralowNoise:1.1nV/?Hzat1kHz
1.1-nV/?Hz noise density with an ultralow distortion of
• UltralowDistortion: 0.000015% at 1 kHz. The OPA1611 and OPA1612
0.000015%at1kHz offer rail-to-rail output swing to within 600 mV with a
• HighSlewRate:27V/?s 2-k? load, which increases headroom and maximizes
dynamic range. These devices also have a high
• WideBandwidth:40MHz(G=+1)
outputdrivecapabilityof±30mA.
• HighOpen-LoopGain:130dB
These devices operate over a very wide supply range
• UnityGainStable
of ±2.25 V to ±18 V, on only 3.6 mA of supply current
• LowQuiescentCurrent: per channel. The OPA1611 and OPA1612 op amps
3.6mAperChannel are unity-gain stable and provide excellent dynamic
• Rail-to-RailOutput behavior overawiderangeofloadconditions.
• WideSupplyRange:±2.25Vto ±18V The dual version features completely independent
circuitry for lowest crosstalk and freedom from
• SingleandDualVersionsAvailable
interactions between channels, even when overdriven
oroverloaded.
2 Applications
Both the OPA1611 and OPA1612 are available in
• ProfessionalAudioEquipment
SOIC-8 packages and the OPA1612 is available in
• MicrophonePreamplifiers
SON-8. These devices are specified from –40°C to
• AnalogandDigitalMixingConsoles +85°C.
• BroadcastStudioEquipment
DeviceInformation(1)
• AudioTest AndMeasurement
PARTNUMBER PACKAGE BODYSIZE(NOM)
• High-EndA/VReceivers
OPA1611 SOIC(8) 4.90mm×3.91mm
SOIC(8) 4.90mm×3.91mm
OPA1612
SON(8) 3.00mm×3.00mm
(1) For all available packages, see the orderable addendum at
theendofthedatasheet.
space
space
THD+NRatiovsOutputAmplitude FunctionalBlockDiagram
1kHz Signal
BW = 80kHz
R = 0W SOURCE
G = +1, R = 600W L
G = +1, R = 2kW L G =-1, R = 600W
L G =-1, R = 2kW
L G = +10, R = 600W L G = +10, R = 2kW
L
0.01 0.1 1 10 20
Output Amplitude (V )
RMS
1
An IMPORTANT NOTICE at the end of this data sheet addresses availability, warranty, changes, use in safety-critical applications,
intellectualpropertymattersandotherimportantdisclaimers.PRODUCTIONDATA.

OPA1611,OPA1612
SBOS450C–JULY2009–REVISEDAUGUST2014 www.ti.com
Table of Contents
1 Features.................................................................. 1 8.1 ApplicationInformation............................................15
2 Applications........................................................... 1 8.2 NoisePerformance.................................................15
3 Description............................................................. 1 8.3 TotalHarmonicDistortionMeasurements...............17
8.4 CapacitiveLoads.....................................................17
4 RevisionHistory..................................................... 2
8.5 ApplicationCircuit...................................................18
5 PinConfigurationandFunctions......................... 3
9 Power-SupplyRecommendations...................... 19
6 Specifications......................................................... 4
10 Layout................................................................... 20
6.1 AbsoluteMaximumRatings......................................4
10.1 LayoutGuidelines.................................................20
6.2 HandlingRatings.......................................................4
10.2 LayoutExample....................................................20
6.3 RecommendedOperatingConditions.......................4
11 DeviceandDocumentationSupport................. 21
6.4 ElectricalCharacteristics:V =±2.25Vto±18V....5
S
6.5 TypicalCharacteristics..............................................7 11.1 DocumentationSupport........................................21
11.2 RelatedLinks........................................................21
7 DetailedDescription............................................ 12
11.3 Trademarks...........................................................21
7.1 Overview.................................................................12
11.4 ElectrostaticDischargeCaution............................21
7.2 FunctionalBlockDiagram.......................................12
11.5 Glossary................................................................21
7.3 FeatureDescription.................................................12
12 Mechanical,Packaging,andOrderable
8 ApplicationandImplementation........................ 15
Information........................................................... 21
4 Revision History
ChangesfromRevisionB(July2011)toRevisionC Page
• Changedformattomeetlatestdatasheetstandards;addednewsections,andmovedexistingsections........................... 1
• AddedSON-8(DRG)packagetodatasheet......................................................................................................................... 1
• ChangedSOtoSOICthroughoutdocumenttomatchindustrystandardterm...................................................................... 1
• Addedfront-pagecurve.......................................................................................................................................................... 1
• Addedtitletoblockdiagram................................................................................................................................................... 1
• DeletedPackageInformationtable;seepackageoptionaddendum..................................................................................... 3
ChangesfromRevisionA(August2009)toRevisionB Page
• RevisedFeatureslistitems.................................................................................................................................................... 1
• Updatedfront-pagefigure....................................................................................................................................................... 1
• Addedmaxspecificationforinputvoltagenoisedensityatf=1kHz .................................................................................... 5
• Correctedtypoinfootnote1forElectricalCharacteristics..................................................................................................... 5
• RevisedFigure4.................................................................................................................................................................... 7
• UpdatedFigure7.................................................................................................................................................................... 7
• ChangedFigure9 .................................................................................................................................................................. 7
• RevisedFigure11.................................................................................................................................................................. 7
• CorrectedtypoinFigure15.................................................................................................................................................... 8
• UpdatedFigure29................................................................................................................................................................ 12
• RevisedfourthparagraphofElectrincalOverstresssection................................................................................................ 13
• RevisedtableinFigure34.................................................................................................................................................... 17
2 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| www.ti.com          |     |               |     |     | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |
| ------------------- | --- | ------------- | --- | --- | ----------------------------------- | --- | --- |
| 5 Pin Configuration |     | and Functions |     |     |                                     |     |     |
DPackage
DPackage
OPA1611,SOIC-8
|     | (TopView) |     |     |     | OPA1612,SOIC-8 |     |     |
| --- | --------- | --- | --- | --- | -------------- | --- | --- |
(TopView)
|     | (1)   |       | (1) |     |         |     |         |
| --- | ----- | ----- | --- | --- | ------- | --- | ------- |
|     | NC 1  | 8 NC  |     |     |         |     |         |
|     |       |       |     |     | OUT A 1 |     | 8 V+    |
|     | -IN 2 | 7 V+  |     |     |         |     |         |
|     |       |       |     |     | -IN A 2 | A   | 7 OUT B |
|     | +IN 3 | 6 OUT |     |     |         |     |         |
|     |       |       |     |     | +IN A 3 | B   | 6 -IN B |
|     | V- 4  | 5 NC  | (1) |     |         |     |         |
|     |       |       |     |     | V- 4    |     | 5 +IN B |
DRGPackage
OPA1612,SON-8
(TopView)
V+
|     |     |     | OUT A 1 | 8       |     |     |     |
| --- | --- | --- | ------- | ------- | --- | --- | --- |
|     |     |     | -IN A 2 | 7 OUT B |     |     |     |
A
|     |     |     | +IN A 3 | 6 -IN B |     |     |     |
| --- | --- | --- | ------- | ------- | --- | --- | --- |
B
|     |     |     | V- 4 | 5 +IN B |     |     |     |
| --- | --- | --- | ---- | ------- | --- | --- | --- |
Pad(2)
(1) NCdenotesnointernalconnection.Pincanbeleftfloatingorconnectedtoanyvoltagebetween(V–)and(V+).
(2) Exposedthermaldiepadonunderside;connectthermaldiepadtoV–.Solderingthethermalpadimprovesheatdissipationandprovides
specifiedperformance.
PinFunctions
PIN
|     |     | NO. |     | I/O DESCRIPTION |     |     |     |
| --- | --- | --- | --- | --------------- | --- | --- | --- |
NAME
| D(OPA1611) | D(OPA1612) | DRG(OPA1612) |     |                                |     |     |     |
| ---------- | ---------- | ------------ | --- | ------------------------------ | --- | --- | --- |
| –IN        | 2          | —            | —   | I Invertinginput               |     |     |     |
| +IN        | 3          | —            | —   | I Noninvertinginput            |     |     |     |
| –INA       | —          | 2            | 2   | I Invertinginput,channelA      |     |     |     |
| +INA       | —          | 3            | 3   | I Noninvertinginput,channelA   |     |     |     |
| –INB       | —          | 6            | 6   | I Invertinginput,channelB      |     |     |     |
| +INB       | —          | 5            | 5   | I Noninvertinginput,channelB   |     |     |     |
| NC         | 1,5,8      | —            | —   | — Nointernalconnection         |     |     |     |
| OUT        | 6          | —            | —   | O Output                       |     |     |     |
| OUTA       | —          | 1            | 1   | O Output,channelA              |     |     |     |
| OUTB       | —          | 7            | 7   | O Output,channelB              |     |     |     |
| V–         | 4          | 4            | 4   | — Negative(lowest)powersupply  |     |     |     |
| V+         | 7          | 8            | 8   | — Positive(highest)powersupply |     |     |     |
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 3
|     |     |     | ProductFolderLinks:OPA1611 | OPA1612 |     |     |     |
| --- | --- | --- | -------------------------- | ------- | --- | --- | --- |

OPA1611,OPA1612
| SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |     |     |     |     |     |     | www.ti.com |
| ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- |
6 Specifications
| 6.1 Absolute | Maximum | Ratings |     |     |     |     |     |     |     |
| ------------ | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
overoperatingfree-airtemperaturerange(unlessotherwisenoted)(1)
|               |     |     |              |     | MIN |     | MAX |     | UNIT |
| ------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | ---- |
| Supplyvoltage |     |     | V =(V+)–(V–) |     |     |     | 40  |     | V    |
S
| Inputvoltage                                |     |     |     |      | (V–)–0.5 |     | (V+)+0.5   |     | V   |
| ------------------------------------------- | --- | --- | --- | ---- | -------- | --- | ---------- | --- | --- |
| Inputcurrent(allpinsexceptpower-supplypins) |     |     |     |      |          |     | ±10        |     | mA  |
| Outputshort-circuit(2)                      |     |     |     |      |          |     | Continuous |     |     |
| Operatingtemperature                        |     |     |     | (T ) | –55      |     | +125       |     | °C  |
A
| Junctiontemperature |     |     |     | (T) J |     |     | 200 |     | °C  |
| ------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
(1) StressesbeyondthoselistedunderAbsoluteMaximumRatingsmaycausepermanentdamagetothedevice.Thesearestressratings
only,whichdonotimplyfunctionaloperationofthedeviceattheseoranyotherconditionsbeyondthoseindicatedunderRecommended
OperatingConditions.Exposuretoabsolute-maximum-ratedconditionsforextendedperiodsmayaffectdevicereliability.
(2) Short-circuittoV /2(groundinsymmetricaldualsupplysetups),oneamplifierperpackage.
S
| 6.2 Handling              | Ratings |     |     |     |     |     |     |      |      |
| ------------------------- | ------- | --- | --- | --- | --- | --- | --- | ---- | ---- |
|                           |         |     |     |     |     |     | MIN | MAX  | UNIT |
| T Storagetemperaturerange |         |     |     |     |     |     | –65 | +150 | °C   |
stg
Humanbodymodel(HBM),perANSI/ESDA/JEDECJS-001,all
|     |     | pins(1) |     |     |     |     | –3000 | 3000 |     |
| --- | --- | ------- | --- | --- | --- | --- | ----- | ---- | --- |
V Electrostaticdischarge Chargeddevicemodel(CDM),perJEDECspecification V
| (ESD) |     |     |     |     |     |     | –1000 | 1000 |     |
| ----- | --- | --- | --- | --- | --- | --- | ----- | ---- | --- |
JESD22-C101,allpins(2)
|     |     | Machinemodel(MM) |     |     |     |     | –200 | 200 |     |
| --- | --- | ---------------- | --- | --- | --- | --- | ---- | --- | --- |
(1) JEDECdocumentJEP155statesthat500-VHBMallowssafemanufacturingwithastandardESDcontrolprocess.
(2) JEDECdocumentJEP157statesthat250-VCDMallowssafemanufacturingwithastandardESDcontrolprocess.
| 6.3 Recommended | Operating |     | Conditions |     |     |     |     |     |     |
| --------------- | --------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
overoperatingfree-airtemperaturerange(unlessotherwisenoted)
|                      |     |     |     |            | MIN | NOM |     | MAX     | UNIT |
| -------------------- | --- | --- | --- | ---------- | --- | --- | --- | ------- | ---- |
| Supplyvoltage(V+–V–) |     |     |     | 4.5(±2.25) |     |     |     | 36(±18) | V    |
| Specifiedtemperature |     |     |     |            | –40 |     |     | +85     | °C   |
4 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
|     |     |     | ProductFolderLinks:OPA1611 |     | OPA1612 |     |     |     |     |
| --- | --- | --- | -------------------------- | --- | ------- | --- | --- | --- | --- |

OPA1611,OPA1612
| www.ti.com |            |                  |           |            | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |     |
| ---------- | ---------- | ---------------- | --------- | ---------- | ----------------------------------- | --- | --- | --- |
| 6.4        | Electrical | Characteristics: | V = ±2.25 | V to ±18 V |                                     |     |     |     |
S
AtT =+25°CandR =2k?,unlessotherwisenoted.V =V =midsupply,unlessotherwisenoted.
| A   |     | L         |     | CM OUT         |     |     |     |      |
| --- | --- | --------- | --- | -------------- | --- | --- | --- | ---- |
|     |     | PARAMETER |     | TESTCONDITIONS | MIN | TYP | MAX | UNIT |
AUDIOPERFORMANCE
0.000015%
| THD+N | Totalharmonicdistortion+noise |     | G=+1,f=1kHz,VO=3VRMS                |     |     |           |     |     |
| ----- | ----------------------------- | --- | ----------------------------------- | --- | --- | --------- | --- | --- |
|       |                               |     |                                     |     |     | –136      |     | dB  |
|       |                               |     | SMPTE/DINtwo-tone,4:1(60Hzand7kHz), |     |     | 0.000015% |     |     |
|       |                               |     | G=+1,VO=3VRMS                       |     |     | –136      |     | dB  |
0.000012%
DIM30(3-kHzsquarewaveand15-kHzsine
| IMD | Intermodulationdistortion |     |                     |     |     |      |     |     |
| --- | ------------------------- | --- | ------------------- | --- | --- | ---- | --- | --- |
|     |                           |     | wave),G=+1,VO=3VRMS |     |     | –138 |     | dB  |
0.000008%
CCIFtwin-tone(19kHzand20kHz),G=+1,
VO=3VRMS
|     |     |     |     |     |     | –142 |     | dB  |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- |
FREQUENCYRESPONSE
|     |                         |     | G=100   |     |     | 80   |     | MHz  |
| --- | ----------------------- | --- | ------- | --- | --- | ---- | --- | ---- |
| GBW | Gain-bandwidthproduct   |     |         |     |     |      |     |      |
|     |                         |     | G=1     |     |     | 40   |     | MHz  |
| SR  | Slewrate                |     | G=–1    |     |     | 27   |     | V/?s |
|     | Full-powerbandwidth(1)  |     | VO=1VPP |     |     |      | 4   | MHz  |
|     | Overloadrecoverytime    |     | G=–10   |     |     | 500  |     | ns   |
|     | Channelseparation(dual) |     | f=1kHz  |     |     | –130 |     | dB   |
NOISE
|     | Inputvoltagenoise |     | f=20Hzto20kHz |     |     | 1.2 |     | ?VPP   |
| --- | ----------------- | --- | ------------- | --- | --- | --- | --- | ------ |
|     |                   |     | f=10Hz        |     |     |     | 2   | nV/?Hz |
Inputvoltagenoisedensity(2)
| en  |                          |     | f=100Hz |     |     | 1.5 |     | nV/?Hz |
| --- | ------------------------ | --- | ------- | --- | --- | --- | --- | ------ |
|     |                          |     | f=1kHz  |     |     | 1.1 | 1.5 | nV/?Hz |
|     |                          |     | f=10Hz  |     |     |     | 3   | pA/?Hz |
| In  | Inputcurrentnoisedensity |     |         |     |     |     |     |        |
|     |                          |     | f=1kHz  |     |     | 1.7 |     | pA/?Hz |
OFFSETVOLTAGE
| VOS     | Inputoffsetvoltage         |     | VS=±15V         |     |     | ±100 | ±500 | ?V      |
| ------- | -------------------------- | --- | --------------- | --- | --- | ---- | ---- | ------- |
| dVOS/dT | VOSovertemperature(2)      |     | TA=–40°Cto+85°C |     |     |      | 1    | 4 ?V/°C |
| PSRR    | Power-supplyrejectionratio |     | VS=±2.25Vto±18V |     |     | 0.1  |      | 1 ?V/V  |
INPUTBIASCURRENT
|     |                      |     | VCM=0V                |     |     | ±60 | ±250 | nA  |
| --- | -------------------- | --- | --------------------- | --- | --- | --- | ---- | --- |
| IB  | Inputbiascurrent     |     |                       |     |     |     |      |     |
|     |                      |     | VCM=0V,DRGpackageonly |     |     | ±60 | ±300 | nA  |
|     | IBovertemperature(2) |     | TA=–40°Cto+85°C       |     |     |     | 350  | nA  |
| IOS | Inputoffsetcurrent   |     | VCM=0V                |     |     | ±25 | ±175 | nA  |
INPUTVOLTAGERANGE
| VCM | Common-modevoltagerange |     |     |     | (V–)+2 |     | (V+)–2 | V   |
| --- | ----------------------- | --- | --- | --- | ------ | --- | ------ | --- |
CMRR Common-moderejectionratio (V–)+2V?VCM?(V+)–2V 110 120 dB
INPUTIMPEDANCE
|                                  | Differential |     |                     |     |     | 20k||8 |     | ?||pF |
| -------------------------------- | ------------ | --- | ------------------- | --- | --- | ------ | --- | ----- |
|                                  | Common-mode  |     |                     |     |     | 109||2 |     | ?||pF |
| (1) Full-powerbandwidth=SR/(2?×V |              |     | ),whereSR=slewrate. |     |     |        |     |       |
P
(2) Specifiedbydesignandcharacterization.
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 5
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| SBOS450C–JULY2009–REVISEDAUGUST2014 |                  |     |     |           |        |               |     |     |     |     | www.ti.com |
| ----------------------------------- | ---------------- | --- | --- | --------- | ------ | ------------- | --- | --- | --- | --- | ---------- |
| Electrical                          | Characteristics: |     | V   | = ±2.25 V | to ±18 | V (continued) |     |     |     |     |            |
S
AtT =+25°CandR =2k?,unlessotherwisenoted.V =V =midsupply,unlessotherwisenoted.
| A   |           | L   |     |     | CM             | OUT |     |     |     |     |      |
| --- | --------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | ---- |
|     | PARAMETER |     |     |     | TESTCONDITIONS |     |     | MIN | TYP | MAX | UNIT |
OPEN-LOOPGAIN
|     |                      |     |     | (V–)+0.2V?VO?(V+)–0.2V,RL=10k? |     |     |     | 114 | 130 |     | dB  |
| --- | -------------------- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- |
| AOL | Open-loopvoltagegain |     |     |                                |     |     |     |     |     |     |     |
|     |                      |     |     | (V–)+0.6V?VO?(V+)–0.6V,RL=2k?  |     |     |     | 110 | 114 |     | dB  |
OUTPUT
|       |                          |     |     | RL=10k?,AOL?114dB |     |     | (V–)+0.2                  |             |     | (V+)–0.2 | V   |
| ----- | ------------------------ | --- | --- | ----------------- | --- | --- | ------------------------- | ----------- | --- | -------- | --- |
| VOUT  | Voltageoutput            |     |     |                   |     |     |                           |             |     |          |     |
|       |                          |     |     | RL=2k?,AOL?110dB  |     |     | (V–)+0.6                  |             |     | (V+)–0.6 | V   |
| IOUT  | Outputcurrent            |     |     |                   |     |     |                           | SeeFigure27 |     |          | mA  |
| ZO    | Open-loopoutputimpedance |     |     |                   |     |     |                           | SeeFigure28 |     |          | ?   |
|       |                          |     |     |                   |     |     |                           |             | +55 |          | mA  |
| ISC   | Short-circuitcurrent     |     |     |                   |     |     |                           |             |     |          |     |
|       |                          |     |     |                   |     |     |                           |             | –62 |          | mA  |
| CLOAD | Capacitiveloaddrive      |     |     |                   |     |     | SeeTypicalCharacteristics |             |     |          | pF  |
POWERSUPPLY
| VS  | Specifiedvoltage             |     |     |                 |     |     | ±2.25 |     |     | ±18 | V   |
| --- | ---------------------------- | --- | --- | --------------- | --- | --- | ----- | --- | --- | --- | --- |
| IQ  | Quiescentcurrent(perchannel) |     |     | IOUT=0A         |     |     |       |     | 3.6 | 4.5 | mA  |
|     | IQoverTemperature(3)         |     |     | TA=–40°Cto+85°C |     |     |       |     |     | 5.5 | mA  |
TEMPERATURERANGE
|     | Specifiedrange           |     |     |     |     |     |     | –40 |     | +85  | °C   |
| --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- |
|     | Operatingrange           |     |     |     |     |     |     | –55 |     | +125 | °C   |
| ?   | Thermalresistance,SOIC-8 |     |     |     |     |     |     |     | 150 |      | °C/W |
JA
(3) Specifiedbydesignandcharacterization.
6 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| www.ti.com |          |                 |            |                            |     |     |     |     |     | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |
| ---------- | -------- | --------------- | ---------- | -------------------------- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- |
| 6.5        | Typical  | Characteristics |            |                            |     |     |     |     |     |                                     |     |     |
| AtT        | =+25°C,V |                 | =±15V,andR | =2k?,unlessotherwisenoted. |     |     |     |     |     |                                     |     |     |
|            | A        | S               |            | L                          |     |     |     |     |     |                                     |     |     |
100
z) z)
Ö H Ö H
V/ A/
n p
y ( y (
sit sit
v
|     | e n e n |     | Voltage Noise Density |     |     |     |     | di  |     |     |     |     |
| --- | ------- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | D D     | 10  |                       |     |     |     |     | V/  |     |     |     |     |
|     | e  e    |     |                       |     |     |     |     | n   |     |     |     |     |
|     | s s     |     |                       |     |     |     |     | 0   |     |     |     |     |
|     | oi oi   |     |                       |     |     |     |     | 2   |     |     |     |     |
N N
e  nt
|     | a g e |     |     |     | Current Noise Density |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
olt urr
V C
1
|     |     | 0.1 | 1 10 | 100 | 1k  | 10k | 100k |     |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
Time (1s/div)
Frequency (Hz)
Figure2.0.1-Hzto10-HzNoise
Figure1.InputVoltageNoiseDensityandInputCurrent
NoiseDensityvsFrequency
|     | z) 10k |     |     |     |     |     |     | 30  |       |     |                |     |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- | ----- | --- | -------------- | --- |
|     | H      |     |     |     |     |     |     |     | =±15V |     | Maximum output |     |
|     | ? V/   |     |     |     |     |     |     |     | V S   |     |                |     |
voltage range
|     | n   |     |     |     |                 |         |     | 25   |     |     | without slew-rate  |     |
| --- | --- | --- | --- | --- | --------------- | ------- | --- | ---- | --- | --- | ------------------ | --- |
|     | ( O |     | EO  |     |                 |         |     |      |     |     |                    |     |
|     | E   | 1k  |     |     | T o t a l O u   | t p u t |     | )    |     |     | induced distortion |     |
|     | y,  |     |     |     |                 |         |     | P P  |     |     |                    |     |
|     | sit | RS  |     |     | V o lt a g e  N | o i s e |     | V 20 |     |     |                    |     |
e (
|     | n   |     |     |     |     |          |     | g       |           |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | ------- | --------- | --- | --- | --- |
|     | D e |     |     |     |     |          |     | a       |           |     |     |     |
|     | al  |     |     |     |     |          |     | olt 1 5 |           |     |     |     |
|     | 100 |     |     |     |     |          |     | V       |           |     |     |     |
|     | ctr |     |     |     |     |          |     | ut      |           |     |     |     |
|     | e   |     |     |     |     |          |     |         | V =±5V    |     |     |     |
|     | p   |     |     |     |     |          |     | p 1 0   | S         |     |     |     |
|     | S   |     |     |     |     | Resistor |     | ut      |           |     |     |     |
|     | e   |     |     |     |     |          |     | O       |           |     |     |     |
|     | s   | 10  |     |     |     | Noise    |     |         |           |     |     |     |
|     | oi  |     |     |     |     |          |     | 5       | V =±2.25V |     |     |     |
|     | N   |     |     |     |     |          |     |         | S         |     |     |     |
e
|     | g     |     |     | E   | 2= e 2+ (i | R )2+ 4kTR |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | ---------- | ---------- | --- | --- | --- | --- | --- | --- |
|     | olt a |     |     |     | O n        | n S        | S   | 0   |     |     |     |     |
1
|     | V   |     |     |     |     |      |     | 10k |     | 100k | 1M  | 10M |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- |
|     |     | 100 | 1k  | 10k |     | 100k | 1M  |     |     |      |     |     |
Frequency (Hz)
|     |     |     | Source Resistance, R |     | (W) |     |     |     |     |     |     |     |
| --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
S
Figure4.MaximumOutputVoltagevsFrequency
Figure3.VoltageNoisevsSourceResistance
|     | 140 |     |     |     |     |     | 180 | 25  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
G = +10
|     | 120 |     |     |     |     |     | 160 | 20  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
15
|     | 100 |     | Gain           |      |     |     | 140             |       |     |                |       |        |
| --- | --- | --- | -------------- | ---- | --- | --- | --------------- | ----- | --- | -------------- | ----- | ------ |
|     |     |     |                |      |     |     | Phase (degrees) | 10    |     |                |       |        |
|     | 80  |     |                |      |     |     | 120             |       |     |                | G =-1 |        |
| B)  |     |     |                |      |     |     |                 | B) 5  |     |                |       |        |
|     | 60  |     |                |      |     |     | 100             |       |     |                |       | G = +1 |
| d   |     |     |                |      |     |     |                 | d     |     |                |       |        |
| n ( |     |     |                |      |     |     |                 | n ( 0 |     |                |       |        |
| ai  | 40  |     |                |      |     |     | 80              | ai    |     |                |       |        |
| G   |     |     |                |      |     |     |                 | G -5  |     |                |       |        |
|     | 20  |     | Phase          |      |     |     | 60              | -10   |     |                |       |        |
|     | 0   |     |                |      |     |     | 40              | -15   |     |                |       |        |
|     | -20 |     |                |      |     |     | 20              | -20   |     |                |       |        |
|     | -40 |     |                |      |     |     | 0               | -25   |     |                |       |        |
|     | 100 | 1k  | 10k            | 100k | 1M  | 10M | 100M            | 100k  |     | 1M             | 10M   | 100M   |
|     |     |     | Frequency (Hz) |      |     |     |                 |       |     | Frequency (Hz) |       |        |
Figure5.GainandPhasevsFrequency Figure6.Closed-LoopGainvsFrequency
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 7
|     |     |     |     |     | ProductFolderLinks:OPA1611 |     |     | OPA1612 |     |     |     |     |
| --- | --- | --- | --- | --- | -------------------------- | --- | --- | ------- | --- | --- | --- | --- |

0.01 -80
%)
e ( s N oi 0.001 -100
+
n
o
st
orti
0.0001 -120 Di
c ni
o ar m 0.00001 -140 H al Tot 0.000001 -160
Total
Harmonic
Distortion
+ Noise (dB)
0.01 -80
1kHz Signal
BW = 80kHz R = 0W %) SOURCE n ( 0.001 -100 o
orti
st
Di
G
G
=
=
+
+
1
1
,
,
R
R
L
L
=
=
6
2
0
kW
0W
ul
ati o n 0.0001 -120
G G = =- -1 1 , , R R L L = = 6 2 0 kW 0W er m o d 0.00001 -140 G = +10, R L = 600W I nt G = +10, R = 2kW L 0.000001 -160
0.01 0.1 1 10 20
Output Amplitude (V )
RMS
Intermodulation
Distortion
(dB)
0.01
%)
e ( s oi N
n + 0.001
o
orti
st Di
c o ni 0.0001 m ar
H
al Tot 0.00001
G = +1
SMPTE/DIN Two-Tone
4:1 (60Hz and 7kHz)
DIM30
(3kHz square wave and 15kHz sine wave)
CCIF Twin-Tone (19kHz and 20kHz)
0.1 1 10 20
Output Amplitude (V )
RMS
Total
Harmonic
Distortion
+ Noise
(dB)
0.001 -100 -80
%) +15V V OUT = 3V RMS
e ( BW > 500kHz oi s RSOURCEOPA1611 N
n + -15V RL R SOURCE = 600W -100
o
Di st
orti
0.0001 -120 R SOURCE = 300W
c o ni -120 m ar
H
Tot al 0.00001 -140 R SOURCE = 0W R SOURCE = 150W -140
10 100 1k 10k 100k
Frequency (Hz)
Total
Harmonic
Distortion
+ Noise
(dB)
0.0001 -120
%)
e ( s oi
N
+
n
o
orti
st Di
c ni o m ar
H
al Tot
0.00001 -140
G = +1, R = 600W G =-1, R = 2kW L L
G = +1, R = 2kW G = +11, R = 600W L L G =-1, R = 600W G = +11, R = 2kW L L
V = 3V OUT RMS BW > 500kHz
10 100 1k 10k 100k
Frequency (Hz)
Total
Harmonic
Distortion
+ Noise
(dB)
0.01 -80
G = +1, R = 600W G =-1, R = 2kW L L
G = +1, R = 2kW G = +10, R = 600W L L G =-1, R = 600W G = +10, R = 2kW
L L
0.001 -100
0.0001 -120
V = 3V OUT RMS
BW = 80kHz
0.00001 -140
10 100 1k 10k 20k
Frequency (Hz)
Total
Harmonic
Distortion
+ Noise
(dB)
OPA1611,OPA1612
SBOS450C–JULY2009–REVISEDAUGUST2014 www.ti.com
Typical Characteristics (continued)
AtT =+25°C,V =±15V,andR =2k?,unlessotherwisenoted.
A S L
%) +15V V OUT = 3V RMS
e ( BW = 80kHz oi s RSOURCEOPA1611
N
n
+ -15V RL
o
orti
Di st R SOURCE = 600W
ni c R SOURCE = 0W R = 300W m o R = 150W SOURCE ar SOURCE
H
al Tot
20 100 1k 10k 20k
Frequency (Hz)
Figure7.THD+NRatiovsFrequency Figure8.THD+NRatiovsFrequency
Figure9.THD+NRatiovsFrequency Figure10.THD+NRatiovsFrequency
Figure11.THD+NRatiovsOutputAmplitude Figure12.IntermodulationDistortionvsOutputAmplitude
8 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| www.ti.com |                 |     |            |             |                            |     |     |     | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |
| ---------- | --------------- | --- | ---------- | ----------- | -------------------------- | --- | --- | --- | ----------------------------------- | --- | --- |
| Typical    | Characteristics |     |            | (continued) |                            |     |     |     |                                     |     |     |
| AtT        | =+25°C,V        |     | =±15V,andR |             | =2k?,unlessotherwisenoted. |     |     |     |                                     |     |     |
|            | A               | S   |            | L           |                            |     |     |     |                                     |     |     |
-80
|     |     | =±15V |     |     |     |     |     | 160 |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
V S
|     | - 9 0       |                 |         |       |        |     | B) B)   |       |       |     |      |
| --- | ----------- | --------------- | ------- | ----- | ------ | --- | ------- | ----- | ----- | --- | ---- |
|     |             | V O U T =  3.5V | RM S    |       |        |     | d d     | 1 4 0 |       |     |      |
|     | -           |                 |         |       |        |     | o ( o ( |       | -PSRR |     |      |
|     | B) 1 0 0    | G  =   + 1      |         |       | = 600W |     | ati     |       |       |     |      |
|     | d           |                 |         |       | R L    |     | ati     | 1 2 0 |       |     |      |
|     | n ( - 1 1 0 |                 |         |       |        |     | R R     |       |       |     |      |
|     |             |                 |         |       |        |     | n  n    | +PSRR |       |     |      |
|     | ati o -     |                 |         |       |        |     | o o     | 1 0 0 |       |     |      |
|     | 1 2 0       |                 |         |       |        |     | cti cti |       |       |     | CMRR |
|     | ar          |                 |         |       |        |     | e e     |       |       |     |      |
|     | p - 1 3 0   |                 |         |       |        |     | ej ej   | 8 0   |       |     |      |
|     | e           |                 |         |       |        |     | R R     |       |       |     |      |
|     | S - 1 4 0   |                 |         |       |        |     | e  y    |       |       |     |      |
|     | el          |                 | R = 2kW |       |        |     | d pl    | 6 0   |       |     |      |
|     | n           |                 | L       |       |        |     | M o p   |       |       |     |      |
|     | n - 1 5 0   |                 |         |       |        |     | u       |       |       |     |      |
|     | h a         |                 |         |       |        |     | n- S    | 4 0   |       |     |      |
|     | C - 1 6 0   |                 |         |       |        |     | o er-   |       |       |     |      |
|     |             |                 | R       | = 5kW |        |     | m       |       |       |     |      |
|     |             |                 |         | L     |        |     | m o w   | 2 0   |       |     |      |
|     | - 1 7 0     |                 |         |       |        |     | o P     |       |       |     |      |
C
|     | -180 |     |     |     |     |      |     | 0    |     |             |             |
| --- | ---- | --- | --- | --- | --- | ---- | --- | ---- | --- | ----------- | ----------- |
|     |      | 10  | 100 | 1k  | 10k | 100k |     | 1 10 | 100 | 1k 10k 100k | 1M 10M 100M |
Frequency (Hz)
Frequency (Hz)
Figure13.ChannelSeparationvsFrequency Figure14.CMRRandPSRRvsFrequency
(ReferredtoInput)
|     |     |     |     |     | G = +1     |     |     |     |     |     | G =-1    |
| --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | -------- |
|     |     |     |     |     | C L = 50pF |     |     |     |     |     | C = 50pF |
L
CF =5.6pF
|     | v   |     |         |     |     |     | v   |     |         |         |     |
| --- | --- | --- | ------- | --- | --- | --- | --- | --- | ------- | ------- | --- |
|     | di  |     |         |     |     |     | di  |     |         |         |     |
|     | V/  |     | +15V    |     |     |     | V/  |     |         |         |     |
|     | m   |     |         |     |     |     | m   |     | RI =2kW | RF =2kW |     |
|     | 0   |     |         |     |     |     | 0   |     |         |         |     |
|     | 2   |     | OPA1611 |     |     |     | 2   |     |         |         |     |
+15V
|     |     |     | -15V |     | RL CL |     |     |     |     | OPA1611 |     |
| --- | --- | --- | ---- | --- | ----- | --- | --- | --- | --- | ------- | --- |
CL
-15V
|     |     |     | Time (0.1ms/div) |     |     |     |     |     | Time (0.1ms/div) |     |     |
| --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | ---------------- | --- | --- |
Figure15.Small-SignalStepResponse(100mV) Figure16.Small-SignalStepResponse(100mV)
|     |     | G = +1     |     |     |     |     |     | G =-1    |     |     |     |
| --- | --- | ---------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
|     |     | C L = 50pF |     |     |     |     |     | C = 50pF |     |     |     |
L
|     |     | R L = 2kW |     |       |     |     |     | R = 2kW |     |     |     |
| --- | --- | --------- | --- | ----- | --- | --- | --- | ------- | --- | --- | --- |
|     |     |           | R   | = 75W |     |     |     | L       |     |     |     |
F
R = 0W
F
|     | di v |     |     |     |     |     | di v |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     | V/   |     |     |     |     |     | V/   |     |     |     |     |
|     | 2    |     |     |     |     |     | 2    |     |     |     |     |
SeeApplications Information,
Input Protectionsection
|     |     |     | Time (0.5ms/div) |     |     |     |     |     | Time (0.5ms/div) |     |     |
| --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | ---------------- | --- | --- |
Figure17.Large-SignalStepResponse Figure18.Large-SignalStepResponse
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 9
|     |     |     |     |     | ProductFolderLinks:OPA1611 |     |     | OPA1612 |     |     |     |
| --- | --- | --- | --- | --- | -------------------------- | --- | --- | ------- | --- | --- | --- |

OPA1611,OPA1612
| SBOS450C–JULY2009–REVISEDAUGUST2014 |                 |            |     |             |                            |     |     |     |     |     |     |     |     | www.ti.com |
| ----------------------------------- | --------------- | ---------- | --- | ----------- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- |
| Typical                             | Characteristics |            |     | (continued) |                            |     |     |     |     |     |     |     |     |            |
| AtT                                 | =+25°C,V        | =±15V,andR |     |             | =2k?,unlessotherwisenoted. |     |     |     |     |     |     |     |     |            |
|                                     | A               | S          |     |             | L                          |     |     |     |     |     |     |     |     |            |
|                                     | 50              |            |     |             |                            |     |     |     | 25  |     |     |     |     |            |
C =  5 .6 p F
|     |     |     |     |      |         |     |     |     |     | R = 0W  |     |        | F          |     |
| --- | --- | --- | --- | ---- | ------- | --- | --- | --- | --- | ------- | --- | ------ | ---------- | --- |
|     |     |     | R   | = 0W | +15V    |     |     |     |     | S       |     |        |            |     |
|     |     |     | S   |      |         | RS  |     |     | 20  |         |     | RI=2kW | R =  2 k W |     |
|     | 40  |     |     |      |         |     |     |     |     |         |     |        | F          |     |
|     |     |     |     |      | OPA1611 |     |     |     |     | R = 25W |     |        | +15V       |     |
S
|     | %)       |        |         |       |      | RL  | CL  | %)   |       |         |     |     |             | RS  |
| --- | -------- | ------ | ------- | ----- | ---- | --- | --- | ---- | ----- | ------- | --- | --- | ----------- | --- |
|     |          |        | R = 25W |       | -15V |     |     |      | 1 5   |         |     |     | OP A 1 6 11 |     |
|     | ot ( 3 0 |        | S       |       |      |     |     | ot ( |       |         |     |     |             | CL  |
|     | o        |        |         |       |      |     |     | h o  |       |         |     |     | - 1 5 V     |     |
|     | s h      |        |         |       |      |     |     | s    |       |         |     |     |             |     |
|     | er       |        |         |       |      |     |     | er   | 1 0   |         |     |     |             |     |
|     | v 2 0    |        |         |       |      |     |     | v    |       |         |     |     |             |     |
|     | O        |        |         |       |      |     |     | O    |       |         |     |     |             |     |
|     |          |        | R       | = 50W |      |     |     |      |       | R = 50W |     |     |             |     |
|     | 10       |        |         | S     |      |     |     |      | 5     | S       |     |     |             |     |
|     |          | G = +1 |         |       |      |     |     |      | G =-1 |         |     |     |             |     |
|     | 0        |        |         |       |      |     |     |      | 0     |         |     |     |             |     |
0 100 200 300 400 500 600 0 100 200 300 400 500 600 700 800 900 1000
|     |     |     | Capacitive Load (pF) |     |     |     |     |     |     | Capacitive Load (pF) |     |     |     |     |
| --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- |
Figure19.Small-SignalOvershootvsCapacitiveLoad Figure20.Small-SignalOvershootvsCapacitiveLoad
|     |     |     | (100-mVOutputStep) |     |     |     |     |     |     | (100-mVOutputStep) |     |     |     |     |
| --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- |
|     | 1.0 |     |                    |     |     |     |     |     | 120 |                    |     |     |     |     |
0.8
100
|     | 0.6 |     |     |     |     |     |     |     |     |     | -I  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     | A)  |     |     | B   |     |     |     |
n
|     | 0 . 4     |     |     |      |     |     |     | nt (  | 80  |     |     |     |     |     |
| --- | --------- | --- | --- | ---- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
|     | V) 0 . 2  |     |     |      |     |     |     | e     |     |     |     |     |     |     |
|     | V/        |     |     | 10kW |     |     |     | urr   |     |     |     |     |     |     |
|     | m         |     |     |      |     |     |     |       | 60  |     |     |     |     |     |
|     | ( 0       |     |     |      |     |     |     | C     |     |     |     | +I  |     |     |
|     | OL        |     |     |      |     |     |     | S     |     |     |     | B   |     |     |
|     | A - 0 . 2 |     |     |      |     |     |     | d I O |     |     |     |     |     |     |
|     | - 0 . 4   |     |     |      |     |     |     | n     | 40  |     | I   |     |     |     |
|     |           |     |     |      |     |     |     | a     |     |     | OS  |     |     |     |
|     |           |     | 2kW |      |     |     |     | I B   |     |     |     |     |     |     |
-0.6
20
-0.8
|     | -1.0 |     |     |     |     |     |     |     | 0   |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |      |     |     |     |     |     |     |     | -40 | -15 | 10  | 35  | 50  | 85  |
|     | -40  | -15 |     | 10  | 35  | 60  | 85  |     |     |     |     |     |     |     |
Temperature (°C)
Temperature (°C)
Figure21.Open-LoopGainvsTemperature Figure22. I B andI OS vsTemperature
|     | 80  |     |     |     |     |     |     |     | 5.0 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
V =±18V
|     | 70  | S   |     | +I  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
B
4.5
60
50
|     | A)  |     |     |     |     |     |     |     | 4.0 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n 40
|     | (   |     |     |     |     |     |     | A)  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
S
|     | I O 3 0 |     |     |     |     |     |     | m   | 3.5 |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | d       |     |     |     | I   |     |     | (   |     |     |     |     |     |     |
|     | n 2 0   |     |     |     | OS  |     |     | I Q |     |     |     |     |     |     |
a
|     | B    |     |     |     |     |     |     |     | 3.0 |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | I 10 |     | -I  |     |     |     |     |     |     |     |     |     |     |     |
B
0
2.5
|     | -10 |     | Common-Mode Range       |     |     |      |     |     |     |     |                  |     |     |     |
| --- | --- | --- | ----------------------- | --- | --- | ---- | --- | --- | --- | --- | ---------------- | --- | --- | --- |
|     | -20 |     |                         |     |     |      |     |     | 2.0 |     |                  |     |     |     |
|     | -18 | -12 | -6                      |     | 0   | 6 12 | 18  |     | -40 | -15 | 10               | 35  | 60  | 85  |
|     |     |     | Common-Mode Voltage (V) |     |     |      |     |     |     |     | Temperature (°C) |     |     |     |
Figure23.I andI vsCommon-ModeVoltage Figure24.QuiescentCurrentvsTemperature
|     |     |     | B   | OS  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
10 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
|     |     |     |     |     |     | ProductFolderLinks:OPA1611 |     |     | OPA1612 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | ------- | --- | --- | --- | --- | --- |

OPA1611,OPA1612
| www.ti.com |                 |            |     |                            |     |     |     |     |     | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |     |
| ---------- | --------------- | ---------- | --- | -------------------------- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- |
| Typical    | Characteristics |            |     | (continued)                |     |     |     |     |     |                                     |     |     |     |
| AtT        | =+25°C,V        | =±15V,andR |     | =2k?,unlessotherwisenoted. |     |     |     |     |     |                                     |     |     |     |
|            | A               | S          |     | L                          |     |     |     |     |     |                                     |     |     |     |
|            | 4.0             |            |     |                            |     |     |     |     | 75  |                                     |     |     |     |
|            | 3.9             |            |     |                            |     |     |     |     | 70  |                                     |     |     |     |
-I
SC
|     | 3.8 |     |     |     |     |     |     |     | 65  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
3.7
60
3.6
|     | A)  |     |     |     |     |     |     | A)  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
m 55
|     | m 3.5   |     |     |     |     |     |     |     |      | +I  |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     | (       |     |     |     |     |     |     | (   | C 50 | SC  |     |     |     |
|     | I Q 3.4 |     |     |     |     |     |     |     | S    |     |     |     |     |
I
45
3.3
|     | 3,2 |     |                                |       |     |       |     |     | 40      |                  |     |        |     |
| --- | --- | --- | ------------------------------ | ----- | --- | ----- | --- | --- | ------- | ---------------- | --- | ------ | --- |
|     | 3.1 |     | Specified Supply-Voltage Range |       |     |       |     |     | 35      |                  |     |        |     |
|     | 3.0 |     |                                |       |     |       |     |     | 30      |                  |     |        |     |
|     | 0   | 4   | 8 12                           | 16 20 | 24  | 28 32 | 36  |     | -50 -25 | 0 25             | 50  | 75 100 | 125 |
|     |     |     | Supply Voltage (V)             |       |     |       |     |     |         | Temperature (°C) |     |        |     |
Figure25.QuiescentCurrentvsSupplyVoltage Figure26.Short-CircuitCurrentvsTemperature
|     | 15  |     |     |     |     |     |     |     | 10k |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
14
1k
V)
e (
|     | 13    | V = ± 1               | 5 V         |     |     |       |     |     |     |     |     |     |     |
| --- | ----- | --------------------- | ----------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     | g     | S                     |             |     |     | +25°C |     |     | 100 |     |     |     |     |
|     | a     | D ua l  v e           | rs ion with |     |     |       |     | W ) |     |     |     |     |     |
|     | olt   |                       |             |     |     | +85°C |     | (   |     |     |     |     |     |
|     | V     | both channels         |             |     |     |       |     | O   |     |     |     |     |     |
|     | ut    |                       |             |     |     | -40°C |     | Z   |     |     |     |     |     |
|     | p -13 | driven simultaneously |             |     |     |       |     |     | 10  |     |     |     |     |
ut
O
1
-14
|     | -15 |     |     |     |     |     |     |     | 0.1    |        |      |        |      |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------ | ---- | ------ | ---- |
|     | 0   | 10  | 20  |     | 30  | 40  | 50  |     | 10 100 | 1k 10k | 100k | 1M 10M | 100M |
Output Current (mA)
Frequency (Hz)
Figure27.OutputVoltagevsOutputCurrent Figure28.Open-LoopOutputImpedancevsFrequency
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 11
|     |     |     |     |     |     | ProductFolderLinks:OPA1611 |     |     | OPA1612 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | ------- | --- | --- | --- | --- |

OPA1611,OPA1612
SBOS450C–JULY2009–REVISEDAUGUST2014 www.ti.com
7 Detailed Description
7.1 Overview
The OPA161x family of bipolar-input operational amplifiers achieve very low 1.1-nV/?Hz noise density with
an ultralow distortion of 0.000015% at 1 kHz. The rail-to-rail output swing, within 600 mV with a 2-k? load,
increases headroom and maximizes dynamic range. These devices also have a high output drive capability
of ±40 mA. The wide supply range of ±2.25 V to ±18 V, on only 3.6 mA of supply current per channel, makes
them applicable to both 5V systems and 36V audio applications. The OPA1611 and OPA1612 op amps are
unity-gainstableandprovideexcellentdynamicbehavior overawiderangeofloadconditions.
7.2 Functional Block Diagram
V+
Pre-Output Driver OUT
IN-
IN+
V-
Figure29. OPA1611SimplifiedSchematic
7.3 Feature Description
7.3.1 PowerDissipation
The OPA1611 and OPA1612 series op amps are capable of driving 2-k? loads with a power-supply voltage up
to ±18 V. Internal power dissipation increases when operating at high supply voltages. Copper leadframe
construction used in the OPA1611 and OPA1612 series op amps improves heat dissipation compared to
conventionalmaterials.Circuitboardlayoutcanalsohelpminimizejunctiontemperaturerise.Widecoppertraces
help dissipate the heat by acting as an additional heat sink. Temperature rise can be further minimized by
solderingthedevicestothecircuitboardratherthanusingasocket.
7.3.2 ElectricalOverstress
Designers often ask questions about the capability of an operational amplifier to withstand electrical overstress.
These questions tend to focus on the device inputs, but may involve the supply voltage pins or even the output
pin. Each of these different pin functions have electrical stress limits determined by the voltage breakdown
characteristics of the particular semiconductor fabrication process and specific circuits connected to the pin.
Additionally, internal electrostatic discharge (ESD) protection is built into these circuits to protect them from
accidentalESDevents bothbeforeandduringproduct assembly.
12 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
www.ti.com SBOS450C–JULY2009–REVISEDAUGUST2014
Feature Description (continued)
Having a good understanding of this basic ESD circuitry and its relevance to an electrical overstress event is
helpful. Figure 30 shows the ESD circuits contained in the OPA161x series (indicated by the dashed line area).
The ESD protection circuitry involves several current-steering diodes connected from the input and output pins
and routed back to the internal power-supply lines, where they meet at an absorption device internal to the
operationalamplifier.Thisprotectioncircuitryisintendedtoremaininactiveduringnormalcircuit operation.
R
F
+V
S
+V
OPA1611
R
I -In ESD Current-
Steering Diodes
Op-Amp Out
+In Core
Edge-Triggered ESD
R
I Absorption Circuit L
D
V IN (1) -V
-V
S
(1) V =+V +500mV.
IN S
Figure30. EquivalentInternalESDCircuitryanditsRelationtoaTypical CircuitApplication
An ESD event produces a short duration, high-voltage pulse that is transformed into a short duration, high-
current pulse when discharged through a semiconductor device. The ESD protection circuits are designed to
provideacurrentpatharoundtheoperationalamplifiercoretopreventdamagetothecore.Theenergyabsorbed
bytheprotectioncircuitryisthendissipatedasheat.
When an ESD voltage develops across two or more of the amplifier device pins, current flows through one or
more of the steering diodes. Depending on the path that the current takes, the absorption device may activate.
The absorption device internal to the OPA1611 triggers when a fast ESD voltage pulse is impressed across the
supply pins. Once triggered, the absorption device quickly activates and clamps the ESD pulse to a safe voltage
level.
When the operational amplifier connects into a circuit such as the one Figure 30 shows, the ESD protection
components are intended to remain inactive and not become involved in the application circuit operation.
However, circumstances may arise where an applied voltage exceeds the operating voltage range of a given pin.
If this condition occurs, some of the internal ESD protection circuits may possibly be biased on, and conduct
current.Anysuchcurrentflowoccursthroughsteeringdiodepathsandrarelyinvolvestheabsorptiondevice.
Figure 30 shows a specific example where the input voltage, V , exceeds the positive supply voltage (+V ) by
IN S
500 mV or more. Much of what happens in the circuit depends on the supply characteristics. If +V can sink the
S
current, one of the upper input steering diodes conducts and directs current to +V . Excessively high current
S
levelscanflowwithincreasinglyhigherV .Asaresult,thedatasheetspecificationsrecommendthat applications
IN
limit theinputcurrentto10mA.
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 13
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
SBOS450C–JULY2009–REVISEDAUGUST2014 www.ti.com
Feature Description (continued)
Ifthesupplyisnotcapableofsinkingthecurrent,V maybeginsourcingcurrent totheoperationalamplifier,and
IN
then take over as the source of positive supply voltage. The danger in this case is that the voltage can rise to
levels that exceed the operational amplifier absolute maximum ratings. In extreme but rare cases, the absorption
device triggers on while +V and –V are applied. If this event happens, a direct current path is established
S S
between the +V and –V supplies. The power dissipation of the absorption device is quickly exceeded, and the
S S
extremeinternalheatingdestroystheoperationalamplifier.
Another common question involves what happens to the amplifier if an input signal is applied to the input while
the power supplies +V or –V are at 0 V. Again, the result depends on the supply characteristic while at 0 V, or
S S
at a level below the input signal amplitude. If the supplies appear as high impedance, then the operational
amplifier supply current may be supplied by the input source via the current steering diodes. This state is not a
normal bias condition; the amplifier most likely does not operate normally. If the supplies are low impedance,
then the current through the steering diodes can become quite high. The current level depends on the ability of
theinputsourcetodelivercurrent,andanyresistanceintheinput path.
If there is an uncertainty about the ability of the supply to absorb this current, external zener diodes may be
added to the supply pins; see Figure 30. The zener voltage must be selected such that the diode does not turn
on during normal operation. However, the zener diode voltage must be low enough so that the zener diode
conductsifthesupplypinbeginstoriseabovethesafeoperatingsupplyvoltagelevel.
7.3.3 OperatingVoltage
The OPA161x series op amps operate from ±2.25-V to ±18-V supplies while maintaining excellent performance.
The OPA161x series can operate with as little as +4.5 V between the supplies and with up to +36 V between the
supplies. However, some applications do not require equal positive and negative output voltage swing. With the
OPA161x series, power-supply voltages do not need to be equal. For example, the positive supply could be set
to+25Vwiththenegativesupplyat–5V.
In all cases, the common-mode voltage must be maintained within the specified range. In addition, key
parameters are assured over the specified temperature range of T = –40°C to +85°C. Parameters that vary with
A
operatingvoltageortemperatureareshownintheTypicalCharacteristics.
7.3.4 InputProtection
The input terminals of the OPA1611 and the OPA1612 are protected from excessive differential voltage with
back-to-back diodes, as Figure 31 shows. In most circuit applications, the input protection circuitry has no
consequence. However, in low-gain or G = +1 circuits, fast ramping input signals can forward bias these diodes
because the output of the amplifier cannot respond rapidly enough to the input ramp. This effect is illustrated in
Figure17oftheTypicalCharacteristics.Iftheinput signalisfast enoughtocreatethisforwardbiascondition,the
input signal current must be limited to 10 mA or less. If the input signal current is not inherently limited, an input
series resistor (R) or a feedback resistor (R ) can be used to limit the signal input current. This input series
I F
resistor degradesthelow-noiseperformanceof theOPA1611andisexaminedintheNoisePerformance section.
Figure31showsanexampleconfigurationwhenbothcurrent-limitinginput andfeedbackresistorsareused.
R
F
-
OPA1611 Output
R
I
+
Input
Figure31. PulsedOperation
14 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
www.ti.com SBOS450C–JULY2009–REVISEDAUGUST2014
8 Application and Implementation
8.1 Application Information
TheOPA1611andOPA1612areunity-gainstable,precisionopampswithverylownoise;thesedevicesare also
free from output phase reversal. Applications with noisy or high-impedance power supplies require decoupling
capacitorsclosetothedevicepower-supplypins.Inmost cases,0.1-?Fcapacitorsareadequate.
8.2 Noise Performance
Figure 32 shows the total circuit noise for varying source impedances with the op amp in a unity-gain
configuration(nofeedbackresistornetwork,andthereforenoadditionalnoisecontributions).
The OPA1611 (GBW = 40 MHz, G = +1) is shown with total circuit noise calculated. The op amp itself
contributes both a voltage noise component and a current noise component. The voltage noise is commonly
modeled as a time-varying component of the offset voltage. The current noise is modeled as the time-varying
component of the input bias current and reacts with the source resistance to create a voltage component of
noise. Therefore, the lowest noise op amp for a given application depends on the source impedance. For low
source impedance, current noise is negligible, and voltage noise generally dominates. The low voltage noise of
the OPA161x series op amps makes them a good choice for use in applications where the source impedance is
lessthan1k?.
8.2.1 DetailedDesignProcedure
TheequationinFigure32showsthecalculationofthetotalcircuit noise, withtheseparameters:
• e =voltagenoise
n
• I =currentnoise
n
• R =sourceimpedance
S
• k=Boltzmann’sconstant=1.38 ×10–23J/K
• T=temperatureindegreesKelvin(K)
8.2.2 ApplicationCurve
VOLTAGE NOISE SPECTRAL DENSITY
vs SOURCE RESISTANCE
H
z)
10k
?
V/
n
( O EO
E 1k Total Output
sit y, RS Voltage Noise
n
e
D
al 100
ctr
e
p
S Resistor
s e 10 Noise
oi
N
e
olt a g
1
E O 2= e n 2+ (i n R S )2+ 4kTR S
V
100 1k 10k 100k 1M
Source Resistance, R (W)
S
Figure32.NoisePerformanceoftheOPA1611InUnity-GainBufferConfiguration
8.2.3 BasicNoiseCalculations
Design of low-noise op amp circuits requires careful consideration of a variety of possible noise contributors:
noisefromthesignalsource,noisegeneratedintheopamp, andnoisefromthefeedbacknetworkresistors.The
totalnoiseofthecircuitistheroot-sum-squarecombinationofallnoisecomponents.
The resistive portion of the source impedance produces thermal noise proportional to the square root of the
resistance. Figure 32 plots this function. The source impedance is usually fixed; consequently, select the op amp
andthefeedbackresistorstominimizetherespectivecontributionstothetotalnoise.
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 15
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| SBOS450C–JULY2009–REVISEDAUGUST2014 |             |     |     |     |     |     |     |     | www.ti.com |
| ----------------------------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | ---------- |
| Noise Performance                   | (continued) |     |     |     |     |     |     |     |            |
Figure 33 shows both inverting and noninverting op amp circuit configurations with gain. In circuit configurations
withgain,thefeedbacknetworkresistorsalsocontributenoise.
The current noise of the op amp reacts with the feedback resistors to create additional noise components. The
feedbackresistorvaluescangenerallybechosentomakethesenoisesourcesnegligible.Theequationsfortotal
noiseareshownforbothconfigurations.
Noise in Noninverting Gain Configuration
Noise at the output:
R 2
|     |     |     |     |      | 2                      |     |       |        | 2      |
| --- | --- | --- | --- | ---- | ---------------------- | --- | ----- | ------ | ------ |
|     |     |     |     | 2= R | 2 e2+ e2+ e2+ (iR)2+ e |     |       | 2+ (iR | )2 R 2 |
|     | R   |     | E   | 1 +  |                        |     |       |        | 1 +    |
|     | 1   |     | O   | R    | n                      | 1   | 2 n 2 | S n    | S R    |
|     |     |     |     |      | 1                      |     |       |        | 1      |
E O
R
|     |     |     | Where e | =Ö4kTR | ´   | 1 + 2 | = thermal noise of R |     |     |
| --- | --- | --- | ------- | ------ | --- | ----- | -------------------- | --- | --- |
|     |     |     |         | S      | S   | R     |                      |     | S   |
1
R
S
R
|     |     |     |     | e =Ö4kTR | ´   | 2 = thermal noise of R |     |     |     |
| --- | --- | --- | --- | -------- | --- | ---------------------- | --- | --- | --- |
|     |     |     |     | 1        | 1   | R                      |     | 1   |     |
| V   |     |     |     |          |     | 1                      |     |     |     |
S
|     |     |     |     | e =Ö4kTR | = thermal noise of R |     |     |     |     |
| --- | --- | --- | --- | -------- | -------------------- | --- | --- | --- | --- |
|     |     |     |     | 2        | 2                    |     | 2   |     |     |
Noise in Inverting Gain Configuration
Noise at the output:
R 2
2
|     |     |     |     | 2=  | R 2     | e2+ e2+ e2+ (iR)2+ e |     | 2     |     |
| --- | --- | --- | --- | --- | ------- | -------------------- | --- | ----- | --- |
|     | R   |     | E O | 1 + |         | n 1                  | 2   | n 2 S |     |
|     | 1   |     |     | R   | 1 + R S |                      |     |       |     |
E O
|     | R S |     |         |        |     | R     |                      |     |     |
| --- | --- | --- | ------- | ------ | --- | ----- | -------------------- | --- | --- |
|     |     |     | Where e | =Ö4kTR | ´   | 2     | = thermal noise of R |     |     |
|     |     |     |         | S      | S   | R + R |                      |     | S   |
1 S
V S
R 2
|     |     |     |     | e 1 =Ö4kTR | 1 ´ |     | = thermal noise of R |     | 1   |
| --- | --- | --- | --- | ---------- | --- | --- | -------------------- | --- | --- |
R + R
1 S
|                                   |     |                |             | e =Ö4kTR | = thermal noise of R |     |     |     |     |
| --------------------------------- | --- | -------------- | ----------- | -------- | -------------------- | --- | --- | --- | --- |
|                                   |     |                |             | 2        | 2                    |     | 2   |     |     |
| FortheOPA161xseriesopampsat1kHz,e |     | =1.1nV/?Hzandi | =1.7pA/?Hz. |          |                      |     |     |     |     |
|                                   |     | n              | n           |          |                      |     |     |     |     |
Figure33. NoiseCalculationinGainConfigurations
16 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
|     |     | ProductFolderLinks:OPA1611 |     |     | OPA1612 |     |     |     |     |
| --- | --- | -------------------------- | --- | --- | ------- | --- | --- | --- | --- |

OPA1611,OPA1612
| www.ti.com |          |            |              |     | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |     |
| ---------- | -------- | ---------- | ------------ | --- | ----------------------------------- | --- | --- | --- |
| 8.3 Total  | Harmonic | Distortion | Measurements |     |                                     |     |     |     |
The OPA161x series op amps have excellent distortion characteristics. THD + noise is below 0.00008% (G = +1,
V O = 3 V RMS , BW = 80 kHz) throughout the audio frequency range, 20 Hz to 20 kHz, with a 2-k? load (see
Figure7 forcharacteristicperformance).
The distortion produced by OPA1611 series op amps is below the measurement limit of many commercially
available distortion analyzers. However, a special test circuit (such as Figure 34 shows) can be used to extend
themeasurementcapabilities.
Opampdistortioncanbeconsideredaninternalerror sourcethat canbereferredtotheinput.Figure34showsa
circuit that causes the op amp distortion to be 101 times (or approximately 40 dB) greater than that normally
produced by the op amp. The addition of R to the otherwise standard noninverting amplifier configuration alters
3
thefeedbackfactorornoisegainofthecircuit.Theclosed-loopgainisunchanged,butthefeedbackavailablefor
errorcorrectionisreducedbyafactorof101,thusextendingtheresolutionby101.Notethat theinput signaland
loadappliedtotheopamparethesameaswithconventionalfeedbackwithout R .KeepthevalueofR smallto
|     |     |     |     |     |     | 3   |     | 3   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
minimizeitseffectonthedistortionmeasurements.
Validity of this technique can be verified by duplicating measurements at high gain and/or high frequency where
the distortion is within the measurement capability of the test equipment. Measurements for this data sheet were
made with an audio precision system two distortion and noise analyzer, which greatly simplifies such repetitive
measurements. The measurement technique can, however, be performed with manual distortion measurement
instruments.
|     |     | R   |     | R   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 1   |     | 2   |     |     |     |     |
SIG. DIST.
|     |     |     |     |     |     | GAIN GAIN | R R   | R   |
| --- | --- | --- | --- | --- | --- | --------- | ----- | --- |
|     |     |     |     |     |     |           | 1 2   | 3   |
|     |     |     |     |     |     |           | ¥ 1kW | 10W |
1 101
|                  |     |     | R 3 OPA1611 |     | V = 3V |         |               |       |
| ---------------- | --- | --- | ----------- | --- | ------ | ------- | ------------- | ----- |
|                  | R   |     |             |     | O RMS  | -1 101  | 4.99kW 4.99kW | 49.9W |
| Signal Gain = 1+ | 2   |     |             |     |        |         |               |       |
|                  | R   |     |             |     |        |         | 549W 4.99kW   | 49.9W |
|                  | 1   |     |             |     |        | +10 110 |               |       |
R
| Distortion Gain = 1+ |     | 2   |     |     |     |     |     |     |
| -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
R II R
|     | 1   | 3   | Generator | Analyzer |     |     |     |     |
| --- | --- | --- | --------- | -------- | --- | --- | --- | --- |
|     |     |     | Output    | Input    |     |     |     |     |
Audio Precision
|     |     |     | System Two(1) |     | Load |     |     |     |
| --- | --- | --- | ------------- | --- | ---- | --- | --- | --- |
with PC Controller
(1) Formeasurementbandwidth,seeFigure7throughFigure12.
|                |       |     | Figure34. | DistortionTest | Circuit |     |     |     |
| -------------- | ----- | --- | --------- | -------------- | ------- | --- | --- | --- |
| 8.4 Capacitive | Loads |     |           |                |         |     |     |     |
The dynamic characteristics of the OPA1611 and OPA1612 have been optimized for commonly encountered
gains, loads, and operating conditions. The combination of low closed-loop gain and high capacitive loads
decreases the phase margin of the amplifier and can lead to gain peaking or oscillations. As a result, heavier
capacitive loads must be isolated from the output. The simplest way to achieve this isolation is to add a small
| resistor | (R equalto50?,forexample)inserieswiththeoutput. |     |     |     |     |     |     |     |
| -------- | ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
S
This small series resistor also prevents excess power dissipation if the output of the device becomes shorted.
Figure 19 and Figure 20 illustrate graphs of Small-Signal Overshoot vs Capacitive Load for several values of R S .
Also, refer to Applications Bulletin AB-028, Feedback Plots Define Op Amp AC Performance (SBOA015),
availablefordownloadfromtheTIwebsite,fordetailsofanalysistechniquesandapplicationcircuits.
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 17
|     |     |     | ProductFolderLinks:OPA1611 |     | OPA1612 |     |     |     |
| --- | --- | --- | -------------------------- | --- | ------- | --- | --- | --- |

OPA1611,OPA1612
SBOS450C–JULY2009–REVISEDAUGUST2014 www.ti.com
8.5 Application Circuit
Figure 35 shows how to use the OPA1611 as an amplifier for professional audio headphones. The circuit shows
theleft sidestereochannel.Anidenticalcircuit isusedtodrivetherightsidestereochannel.
820W
2200pF
+V 0.1mF
A
(+15V)
330W
I L+
OUT
OPA1611
2700pF
-V A 680W 620W
(-15V)
0.1mF +V A 0.1mF
(+15V)
Audio DAC
with Differential
Current 100W
Outputs 820W OPA1611 L Ch
Output
8200pF
2200pF
-V
A
(-15V)
+V 0.1mF 0.1mF
A
(+15V) 680W 620W
I L-
OUT
OPA1611 330W 2700pF
-V
A
(-15V)
0.1mF
Figure35. AudioDACPostFilter(I/VConverterandLow-PassFilter)
18 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
www.ti.com SBOS450C–JULY2009–REVISEDAUGUST2014
9 Power-Supply Recommendations
The OPA161x is specified for operation from 4.5 V to 36 V (±2.25 V to ±18 V); many specifications apply from
–40°C to +85°C. Parameters that can exhibit significant variance with regard to operating voltage or temperature
arepresentedintheTypicalCharacteristicssection.
CAUTION
Supply voltages larger than 40 V can permanently damage the device; see the
AbsoluteMaximumRatings.
Place 0.1-?F bypass capacitors close to the power-supply pins to reduce errors coupling in from noisy or high-
impedance power supplies. For more detailed information on bypass capacitor placement, refer to the Typical
Characteristicssection.
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 19
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| SBOS450C–JULY2009–REVISEDAUGUST2014 |     |     |     |     | www.ti.com |
| ----------------------------------- | --- | --- | --- | --- | ---------- |
10 Layout
| 10.1 Layout | Guidelines |     |     |     |     |
| ----------- | ---------- | --- | --- | --- | --- |
Forbestoperationalperformanceofthedevice, usegoodprintedcircuit board(PCB)layoutpractices,including:
• Noise can propagate into analog circuitry through the power pins of the circuit as a whole and the op amp
itself. Bypass capacitors are used to reduce the coupled noise by providing low-impedance power sources
localtotheanalogcircuitry.
– Connect low-ESR, 0.1-µF ceramic bypass capacitors between each supply pin and ground, placed as
close to the device as possible. A single bypass capacitor from V+ to ground is applicable for single-
supplyapplications.
• Separate grounding for analog and digital portions of the circuitry is one of the simplest and most-effective
methods of noise suppression. One or more layers on multilayer PCBs are usually devoted to ground planes.
A ground plane helps distribute heat and reduces EMI noise pickup. Make sure to physically separate digital
and analog grounds while paying attention to the flow of the ground current. For more detailed information,
| refertotheapplicationreportCircuitBoardLayoutTechniques |     | (SLOA089). |     |     |     |
| ------------------------------------------------------- | --- | ---------- | --- | --- | --- |
• In order to reduce parasitic coupling, run the input traces as far away from the supply or output traces as
possible. If these traces cannot be keep them separate, crossing the sensitive trace perpendicular as
opposedtoinparallelwiththenoisytraceisthepreferredmethod.
• Place the external components as close to the device as possible. As shown in Figure 36, keeping RF and
RGclosetotheinvertinginputminimizesparasiticcapacitance.
• Keep the length of input traces as short as possible. Always remember that the input traces are the most
sensitivepartofthecircuit.
• Consider a driven, low-impedance guard ring around the critical traces. A guard ring can significantly reduce
leakagecurrentsfromnearbytracesthatareatdifferent potentials.
| 10.2 Layout | Example |     |     |     |     |
| ----------- | ------- | --- | --- | --- | --- |
RIN
VIN +
RG VOUT
RF
(Schematic Representation)
Place components
close to device and to
Run the input traces
| as far away from | each other to reduce  |     |     |     |     |
| ---------------- | --------------------- | --- | --- | --- | --- |
| the supply lines | parasitic errors      |     |     | VS+ |     |
RF
as possible
|     |     | NC  | NC  |     |     |
| --- | --- | --- | --- | --- | --- |
RG
|     | GND | ±IN |     |     | GND |
| --- | --- | --- | --- | --- | --- |
V+
|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
|     |     | +IN | OUT |     |     |
VIN
RIN
|     |     | V±  | NC  | Use low-ESR, ceramic  |     |
| --- | --- | --- | --- | --------------------- | --- |
bypass capacitor
Only needed for
| dual-supply | GND | VS±  |     |     |     |
| ----------- | --- | ---- | --- | --- | --- |
VOUT
operation (or GND for single supply) Ground (GND) plane on another layer
Figure36. OperationalAmplifierBoardLayoutforaNoninvertingConfiguration
20 SubmitDocumentationFeedback Copyright©2009–2014,TexasInstrumentsIncorporated
ProductFolderLinks:OPA1611 OPA1612

OPA1611,OPA1612
| www.ti.com         |     |               |         |     | SBOS450C–JULY2009–REVISEDAUGUST2014 |     |
| ------------------ | --- | ------------- | ------- | --- | ----------------------------------- | --- |
| 11 Device          | and | Documentation | Support |     |                                     |     |
| 11.1 Documentation |     | Support       |         |     |                                     |     |
11.1.1 RelatedDocumentation
Forrelateddocumentationseethefollowing:
• FeedbackPlotsDefineOpAmpACPerformance,SBOA015
• CircuitBoardLayoutTechniques,SLOA089
| 11.2 Related | Links |     |     |     |     |     |
| ------------ | ----- | --- | --- | --- | --- | --- |
The table below lists quick access links. Categories include technical documents, support and community
resources,toolsandsoftware,andquickaccesstosampleorbuy.
Table1.RelatedLinks
|         |     |               |            | TECHNICAL | TOOLS&    | SUPPORT&  |
| ------- | --- | ------------- | ---------- | --------- | --------- | --------- |
| PARTS   |     | PRODUCTFOLDER | SAMPLE&BUY |           |           |           |
|         |     |               |            | DOCUMENTS | SOFTWARE  | COMMUNITY |
| OPA1611 |     | Clickhere     | Clickhere  | Clickhere | Clickhere | Clickhere |
| OPA1612 |     | Clickhere     | Clickhere  | Clickhere | Clickhere | Clickhere |
11.3 Trademarks
| SoundPlusisatrademarkofTexasInstruments, |     |           | Inc.                     |     |     |     |
| ---------------------------------------- | --- | --------- | ------------------------ | --- | --- | --- |
| Allothertrademarksaretheproperty         |     |           | oftheirrespectiveowners. |     |     |     |
| 11.4 Electrostatic                       |     | Discharge | Caution                  |     |     |     |
Thesedeviceshavelimitedbuilt-inESDprotection.Theleadsshouldbeshortedtogetherorthedeviceplacedinconductivefoam
duringstorageorhandlingtopreventelectrostaticdamagetotheMOSgates.
11.5 Glossary
| SLYZ022—TI                                  | Glossary. |            |               |                 |     |     |
| ------------------------------------------- | --------- | ---------- | ------------- | --------------- | --- | --- |
| Thisglossarylistsandexplainsterms,acronyms, |           |            |               | anddefinitions. |     |     |
| 12 Mechanical,                              |           | Packaging, | and Orderable | Information     |     |     |
The following pages include mechanical, packaging, and orderable information. This information is the most
current data available for the designated devices. This data is subject to change without notice and revision of
thisdocument.Forbrowser-basedversionsofthisdatasheet, refertotheleft-handnavigation.
Copyright©2009–2014,TexasInstrumentsIncorporated SubmitDocumentationFeedback 21
ProductFolderLinks:OPA1611 OPA1612

PACKAGE OPTION ADDENDUM
www.ti.com 10-Nov-2025
PACKAGING INFORMATION
Orderable part number Status Material type Package | Pins Package qty | Carrier RoHS Lead finish/ MSL rating/ Op temp (°C) Part marking
(1) (2) (3) Ball material Peak reflow (6)
(4) (5)
OPA1611AID Active Production SOIC (D) | 8 75 | TUBE Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1611A
OPA1611AID.B Active Production SOIC (D) | 8 75 | TUBE Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1611A
OPA1611AIDR Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1611A
OPA1611AIDR.B Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1611A
OPA1611AIDRG4 Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1611A
OPA1611AIDRG4.B Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1611A
OPA1612AID Active Production SOIC (D) | 8 75 | TUBE Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1612A
OPA1612AID.B Active Production SOIC (D) | 8 75 | TUBE Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1612A
OPA1612AIDR Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1612A
OPA1612AIDR.B Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1612A
OPA1612AIDRG4 Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1612A
OPA1612AIDRG4.B Active Production SOIC (D) | 8 2500 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OPA
1612A
OPA1612AIDRGR Active Production SON (DRG) | 8 3000 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OVII
OPA1612AIDRGR.B Active Production SON (DRG) | 8 3000 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OVII
OPA1612AIDRGRG4 Active Production SON (DRG) | 8 3000 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OVII
OPA1612AIDRGRG4.B Active Production SON (DRG) | 8 3000 | LARGE T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OVII
OPA1612AIDRGT Active Production SON (DRG) | 8 250 | SMALL T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OVII
OPA1612AIDRGT.B Active Production SON (DRG) | 8 250 | SMALL T&R Yes NIPDAU Level-2-260C-1 YEAR -40 to 85 OVII
(1) Status: For more details on status, see our product life cycle.
Addendum-Page 1

PACKAGE OPTION ADDENDUM
www.ti.com 10-Nov-2025
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
OTHER QUALIFIED VERSIONS OF OPA1612 :
•Automotive : OPA1612-Q1
NOTE: Qualified Version Definitions:
•Automotive - Q100 devices qualified for high-reliability automotive applications targeting zero defects
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
|             |      |     | (mm) W1 (mm)    |         |         |         |
| ----------- | ---- | --- | --------------- | ------- | ------- | ------- |
| OPA1611AIDR | SOIC | D 8 | 2500 330.0 12.4 | 6.4 5.2 | 2.1 8.0 | 12.0 Q1 |
OPA1611AIDRG4 SOIC D 8 2500 330.0 12.4 6.4 5.2 2.1 8.0 12.0 Q1
| OPA1612AIDR | SOIC | D 8 | 2500 330.0 12.4 | 6.4 5.2 | 2.1 8.0 | 12.0 Q1 |
| ----------- | ---- | --- | --------------- | ------- | ------- | ------- |
OPA1612AIDRG4 SOIC D 8 2500 330.0 12.4 6.4 5.2 2.1 8.0 12.0 Q1
OPA1612AIDRGR SON DRG 8 3000 330.0 12.4 3.3 3.3 1.1 8.0 12.0 Q2
OPA1612AIDRGRG4 SON DRG 8 3000 330.0 12.4 3.3 3.3 1.1 8.0 12.0 Q2
OPA1612AIDRGT SON DRG 8 250 180.0 12.4 3.3 3.3 1.1 8.0 12.0 Q2
Pack Materials-Page 1

PACKAGE MATERIALS INFORMATION

| www.ti.com |     |     |     |     |     | 10-Aug-2026 |
| ---------- | --- | --- | --- | --- | --- | ----------- |
TAPE AND REEL BOX DIMENSIONS
Width (mm)
H
W L

*All dimensions are nominal
Device Package Type Package Drawing Pins SPQ Length (mm) Width (mm) Height (mm)
| OPA1611AIDR     | SOIC | D   | 8 2500 | 353.0 | 353.0 | 32.0 |
| --------------- | ---- | --- | ------ | ----- | ----- | ---- |
| OPA1611AIDRG4   | SOIC | D   | 8 2500 | 353.0 | 353.0 | 32.0 |
| OPA1612AIDR     | SOIC | D   | 8 2500 | 353.0 | 353.0 | 32.0 |
| OPA1612AIDRG4   | SOIC | D   | 8 2500 | 353.0 | 353.0 | 32.0 |
| OPA1612AIDRGR   | SON  | DRG | 8 3000 | 353.0 | 353.0 | 32.0 |
| OPA1612AIDRGRG4 | SON  | DRG | 8 3000 | 353.0 | 353.0 | 32.0 |
| OPA1612AIDRGT   | SON  | DRG | 8 250  | 213.0 | 191.0 | 35.0 |
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
| OPA1611AID   | D   | SOIC | 8 75 | 506.6 | 8 3940 | 4.32 |
| ------------ | --- | ---- | ---- | ----- | ------ | ---- |
| OPA1611AID.B | D   | SOIC | 8 75 | 506.6 | 8 3940 | 4.32 |
| OPA1612AID   | D   | SOIC | 8 75 | 506.6 | 8 3940 | 4.32 |
| OPA1612AID.B | D   | SOIC | 8 75 | 506.6 | 8 3940 | 4.32 |
Pack Materials-Page 3

GENERIC PACKAGE VIEW
DRG 8 WSON - 0.8 mm max height
3 x 3, 0.5 mm pitch PLASTIC SMALL OUTLINE - NO LEAD
This image is a representation of the package family, actual package may vary.
Refer to the product data sheet for package details.
4225794/A
www.ti.com

PACKAGE OUTLINE
DRG0008A WSON - 0.8 mm max height
SCALE 5.000
PLASTIC SMALL OUTLINE - NO LEAD
3.1 B
A
2.9
3.1
PIN 1 INDEX AREA
2.9
0.8
0.7
C
SEATING PLANE
0.05
0.00 0.08 C
(0.2) TYP
EXPOSED 1.2 0.1
THERMAL PAD
4
5
2X
1.5 2 0.1
8
1
6X 0.5
0.3
8X
0.2
PIN 1 ID 0.6
8X 0.1 C A B
0.4
0.08 C
4218885/A 03/2020
NOTES:
1. All linear dimensions are in millimeters. Any dimensions in parenthesis are for reference only. Dimensioning and tolerancing
per ASME Y14.5M.
2. This drawing is subject to change without notice.
3. The package thermal pad must be soldered to the printed circuit board for thermal and mechanical performance.
www.ti.com

EXAMPLE BOARD LAYOUT
DRG0008A WSON - 0.8 mm max height
PLASTIC SMALL OUTLINE - NO LEAD
(1.2)
8X (0.7) SYMM
1 8
8X (0.25)
SYMM (2)
(0.75)
6X (0.5)
4 5
(R0.05) TYP
( 0.2) VIA
(0.35)
TYP
(2.7)
LAND PATTERN EXAMPLE
EXPOSED METAL SHOWN
SCALE:20X
0.07 MAX 0.07 MIN
ALL AROUND ALL AROUND
EXPOSED EXPOSED
METAL METAL
SOLDER MASK METAL METAL UNDER SOLDER MASK
OPENING SOLDER MASK OPENING
NON SOLDER MASK
SOLDER MASK
DEFINED
DEFINED
(PREFERRED)
SOLDER MASK DETAILS
4218885/A 03/2020
NOTES: (continued)
4. This package is designed to be soldered to a thermal pad on the board. For more information, see Texas Instruments literature
number SLUA271 (www.ti.com/lit/slua271).
5. Vias are optional depending on application, refer to device data sheet. If any vias are implemented, refer to their locations shown
on this view. It is recommended that vias under paste be filled, plugged or tented.
www.ti.com

EXAMPLE STENCIL DESIGN
DRG0008A WSON - 0.8 mm max height
PLASTIC SMALL OUTLINE - NO LEAD
SYMM
8X (0.7) METAL
TYP
8X (0.25) 1 8
SYMM
(1.79)
6X (0.5)
4
5
(R0.05) TYP
(1.13)
(2.7)
SOLDER PASTE EXAMPLE
BASED ON 0.125 mm THICK STENCIL
EXPOSED PAD
84% PRINTED SOLDER COVERAGE BY AREA
SCALE:25X
4218885/A 03/2020
NOTES: (continued)
6. Laser cutting apertures with trapezoidal walls and rounded corners may offer better paste release. IPC-7525 may have alternate
design recommendations.
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
