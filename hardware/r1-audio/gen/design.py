"""R1 - Audio board at the rear wall (left part, Audio Out + Audio In blocks of the 3D model, R142): the audio jacks and the
analog front end. Every input leaves R1 as a differential pair scaled to the full scale of the A1 input buffer (8 Vrms differential,
referred to GND); the Cirrus buffers around ADC_VMID / DAC_VMID (AN0635, AN0679) sit next to the converters on A1.
Single source of truth for the schematic. Research: docs/ru/34_rear_boards_research.md (2, 3), doc 28; decisions R16, R23,
R64-R66, R72, R88, R116-R118, R135-R137.

Level plan (rev 0.2, checked by the cloud, task #24: CS53A04P DS1397 (CS5304P/8P family), CS4308P DS1317, AN0635, AN0679):
- ADC: 0 dBFS = 2.0 Vrms differential at the ADC pins. The recommended AN0635 buffer (inverting, 1.2k in / 300 R
  feedback, 68 uF per leg) has gain 1/4: 0 dBFS = 8 Vrms differential at its input. A1 uses it unchanged, so R1 delivers
  8.33 Vrms diff at FS (8 x (1200 + 49.9) / 1200, the 49.9 R build-out is in series). Rev 0.1 assumed 2 Vrms: gains x 4.17.
- Line 1-8 (TRS, balanced): OPA1637 gain 6.81k / (10k + 100 R) = 0.674: FS at +24.1 dBu (R135).
- Mic/Line 1-2 (combo): phantom 6.81k + 47 uF on XLR (R72), TRS joins after the blocking caps (no phantom on TRS); OPA1612
  two-op-amp front end gain 1 + 2 x 499 / 332 = 4.01 (+12 dB, lower Rg noise); loud path x 0.681 (FS at +11.9 dBu in;
  front end clips at about +13.6 dBu; a relay -12 dB attenuator ahead of it (rev 0.3) takes +24 dBu lines), quiet path 68.1k / 1k (+40 dB over loud, FS at -28.1 dBu in) - R117.
- Hi-Z 1-2: 1 MOhm, OPA1642 buffer x 1, then OPA1637 single-ended -> differential: loud x 1.37 (FS at +17.9 dBu),
  quiet x 137 (+40 dB, FS at -22.1 dBu).
- Phono L/R: relay per channel (R118, default = line): line -> OPA1637 x 4.12 (FS 2.02 Vrms = +8.3 dBu, CD level);
  phono -> computed RIAA (+35.0 dB at 1 kHz, error < 0.05 dB 20 Hz - 20 kHz; FS 36 mV at 1 kHz): active 3180/318 us
  (68.1k || 47n + 7.42k over 130 R + 470 uF), passive 75 us (787 R + 100n into the 16.7k FDA input) -> OPA1637 x 4.12.
- Outputs: DAC pairs from A1 (CS4308P 1.67 mA rms x 1.2k = 2.0 Vrms diff) -> OPA1612 difference amp x 3.09 ->
  6.19 Vrms = +18.0 dBu (R64), impedance-balanced TRS
  (hot through 47 R, cold 47 R to GND), RCA = copy of Main (R23); NO relays per pair open without power (R66, R137),
  closed only when MUTE and R2_OK are both high (R118).

Rev 0.1 (14.11.2026, PC) = schematic only; rev 0.2 (14.11.2026, cloud #24) = levels and values checked; rev 0.3 = -12 dB attenuator relay per combo (ATT1/ATT2 from R2); jacks vertical-mount (Neutrik NCJ6FI-V, NJ3FD-V), RCA part to choose.
Rev 0.9 (18.11.2026, schematic audit notes/reviews/schematics_2026-11-18.md, B2): phantom hot-plug: SMBJ18CA per Mic/Line leg at the far side of the 47 uF blocking
cap and the series 10 R -> 47 R (0805); MUTE / R2_OK series FETs 2N7002 -> AO3400A (coil voltage margin); everything else unchanged.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "r1-audio"
ID = "R1"
TITLE = "R1 - Audio jacks and analog front end: mic/Hi-Z two paths, line 1-8, phono, Main/Aux/RCA out on relays"
REV = "1.0"
M1_LIB = K.M1_LIB
BUS_NOTE = ("R1 -> A1: 18 differential ADC pairs (FS 8 Vrms diff into the AN0635 buffers), A1 -> R1: 4 DAC pairs; phantom per channel and phono/line "
            "from R2 (R118); output relays need MUTE and R2_OK (R137)")
PWR_FLAG_NETS = ("+12V", "-12V")   # ERC: rails from the PW connector feed power inputs (op-amps)
NO_PWR_FLAG = ("+3V3",)
W, H = 238.0, 105.0         # rear x 273-511, z 8-113 (rev 1.0: rear wall v6.1, rows z 95/69/43/17, top lowered 117 -> 113 so it clears the shelf at z 114, doc 41 sect. 24)
HOLES = [(4.0, 4.0), (234.0, 4.0), (4.0, 101.0), (234.0, 101.0),   # M3, board coordinates (KiCad, y down); 15.11.2026; rev 0.8: bottom +13 (H 109)
         (30.0, 70.0), (172.0, 6.0), (172.0, 31.0)]   # 16.11: beside the RCA pairs (RCJ-025 has no panel nut): the plug force goes into standoffs
A1_RISE = 5.1        # mm, see placement(). R179 (17.11.2026): A1 on the floor on ~10.7 mm standoffs (board plane z 13.7, sockets rows ~16.6 / 19.1) instead of the tray (R171: 19.0). Estimate +-1 mm: check against the socket drawing
LAYERS = 4

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603, R1206 = "Resistor_SMD:R_0603_1608Metric", "Resistor_SMD:R_1206_3216Metric"
C1206, C1210 = "Capacitor_SMD:C_1206_3216Metric", "Capacitor_SMD:C_1210_3225Metric"
CP8, CP63 = "Capacitor_SMD:CP_Elec_8x10.5", "Capacitor_SMD:CP_Elec_6.3x7.7"
SOIC8, VSSOP8 = "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "Package_SO:VSSOP-8_3x3mm_P0.65mm"
SOT23, SOD123 = "Package_TO_SOT_SMD:SOT-23", "Diode_SMD:D_SOD-123"
SMB, R0805 = "Diode_SMD:D_SMB", "Resistor_SMD:R_0805_2012Metric"
COMBO = "Connector_Audio:Jack_XLR-6.35mm_Neutrik_NCJ6FI-V_Vertical"
TRS = "Connector_Audio:Jack_6.35mm_Neutrik_NJ3FD-V_Vertical"
RCA = "ShtukaDruka:Jack_RCA_SameSky_RCJ-02_Vertical"   # Same Sky (CUI) RCJ-025, LCSC C4991609: vertical, no panel nut (none in stock at JLC)
RCA_LCSC = "C4991609"
RELAY = ("Relay:Omron_G6K-2", "Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y")
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Vertical"


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Q": 0, "K": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    def R(value, a, b, fp=R0402, **f):
        add(ref("R"), "Device:R", value, fp, {"1": a, "2": b}, **f)

    def C(value, a, b="GND", fp=C0402, **f):
        add(ref("C"), "Device:C", value, fp, {"1": a, "2": b}, **f)

    def CP(value, plus, minus="GND", fp=CP8, **f):
        add(ref("C"), "Device:C_Polarized", value, fp, {"1": plus, "2": minus}, **f)

    def clamp(node):                                     # diodes to the +-12 V rails (1N4148W: 1 = K, 2 = A)
        add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": "+12V", "2": node})
        add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": node, "2": "-12V"})

    def supply(u_pins, plus="3", minus="6"):            # decoupling for an op-amp
        C("100n 25V", "+12V", fp=C0603)
        C("100n 25V", "-12V", fp=C0603)

    def fda(name, inp, inn, outp, outn, rg, rf, cf, note):
        """OPA1637: inp -> Rg -> IN+, inn -> Rg -> IN-, OUT+ -> Rf -> IN-, OUT- -> Rf -> IN+; VOCM = GND (ADC buffers on A1)."""
        u = ref("U")
        add(u, "ShtukaDruka:OPA1637", "OPA1637", VSSOP8,
            {"1": f"{name}_IM", "2": "GND", "3": "+12V", "4": f"{name}_OP", "5": f"{name}_ON", "6": "-12V", "7": None,
             "8": f"{name}_IP"}, LCSC="C2860968", Note=f"{note}; gain {rf}/{rg}")
        R(rg, inp, f"{name}_IP", Note="Rg 0.1 %")
        R(rg, inn, f"{name}_IM", Note="Rg 0.1 %")
        R(rf, f"{name}_OP", f"{name}_IM", Note="Rf 0.1 %")
        R(rf, f"{name}_ON", f"{name}_IP", Note="Rf 0.1 %")
        C(cf, f"{name}_OP", f"{name}_IM", fp=C0603, Note="Cf C0G")
        C(cf, f"{name}_ON", f"{name}_IP", fp=C0603, Note="Cf C0G")
        R("49.9", f"{name}_OP", outp, Note="isolates the cable to A1")
        R("49.9", f"{name}_ON", outn)
        C("1n C0G", outp, outn, fp=C0603, Note="differential RF filter, 1.6 MHz with 2 x 49.9 R; the A1 buffer filters again")
        supply(u)

    # ---------------------------------------------------------------- power and control
    add(ref("J"), "Connector_Generic:Conn_02x05_Odd_Even", "Power from PW", MF.format("43045-1012_2x05"),
        {"1": "+12V", "2": "GND", "3": "-12V", "4": "GND", "5": "+5V", "6": "GND", "7": "+48V", "8": "GND", "9": "+5V", "10": "GND"},
        Note="same pinout as PW 'to A1/R1'; A1 gets +-12 V and +5 V through the board-to-board connector")
    for _ in range(2):
        CP("47u 25V", "+12V", fp=CP63)
        CP("47u 25V", "GND", "-12V", fp=CP63)
    add(ref("J"), "Connector_Generic:Conn_02x07_Odd_Even", "from R2", "Connector_PinHeader_2.54mm:PinHeader_2x07_P2.54mm_Vertical",
        {"1": "PH48_1", "2": "GND", "3": "PH48_2", "4": "GND", "5": "PHONO", "6": "GND", "7": "MUTE", "8": "GND", "9": "R2_OK",
         "10": "GND", "11": "ATT1", "12": "GND", "13": "ATT2", "14": "GND"},
        Note="same pinout as R2 'to A1/R1' (2x7 from rev 0.3: ATT1/ATT2 = Mic/Line attenuator relays); all lines pulled low on R2 while it boots")

    add(ref("J"), "Connector_Generic:Conn_01x03", "to F1 (mute)", "Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical",
        {"1": "MUTE", "2": "R2_OK", "3": "GND"}, Note="MUTE and R2_OK for the headphone relays on F1 (parallel to the output relay logic); "
        "the headphone board is at the front edge, R2's connector to R1 stays 2x7")

    # ---------------------------------------------------------------- board-to-board to A1
    adc = [f"ADC{k}" for k in range(1, 19)]
    a_pins = {}
    for k in range(10):                                  # ADC1-10: pair at pins 4k+1/4k+2, GND at 4k+3/4k+4
        a_pins[str(4 * k + 1)], a_pins[str(4 * k + 2)] = f"{adc[k]}_P", f"{adc[k]}_N"
        a_pins[str(4 * k + 3)], a_pins[str(4 * k + 4)] = "GND", "GND"
    add(ref("J"), "Connector_Generic:Conn_02x20_Odd_Even", "to A1 (ADC 1-10)", "Connector_PinHeader_2.54mm:PinHeader_2x20_P2.54mm_Vertical",
        a_pins, Note="differential pairs on adjacent pins, GND pair between pairs; mating part on A1")
    pairs_b = [f"{a}" for a in adc[10:]] + ["DAC_ML", "DAC_MR", "DAC_AL", "DAC_AR"]
    b_pins = {}
    for k, pr in enumerate(pairs_b):                     # 12 pairs: pins 4k+1/4k+2, GND 4k+3/4k+4 (k < 11)
        b_pins[str(4 * k + 1)], b_pins[str(4 * k + 2)] = f"{pr}_P", f"{pr}_N"
        if k < 11:
            b_pins[str(4 * k + 3)], b_pins[str(4 * k + 4)] = "GND", "GND"
    b_pins.update({"47": "+12V", "48": "-12V", "49": "+5V", "50": "+5V"})
    add(ref("J"), "Connector_Generic:Conn_02x25_Odd_Even", "to A1 (ADC 11-18, DAC 1-4, power)",
        "Connector_PinHeader_2.54mm:PinHeader_2x25_P2.54mm_Vertical", b_pins,
        Note="ADC 11-18 = line 1-8; DAC pairs Main L/R, Aux L/R from the CS4308P I-V stages on A1; +-12 V, +5 V to A1")

    # ---------------------------------------------------------------- phantom per channel (R118): PNP high-side, slow ramp
    for k in (1, 2):
        q = ref("Q")
        add(q, "Transistor_BJT:MMBTA92", "MMBTA92", SOT23, {"1": f"P48_{k}_B", "2": "+48V", "3": f"P48_{k}"},
            LCSC="C3009890", Note=f"phantom {k} switch (300 V PNP), Miller ramp")
        R("100k", "+48V", f"P48_{k}_B", Note="base pull-up: off by default")
        R("100k", f"P48_{k}_B", f"P48_{k}_BC", Note="base drive about 0.45 mA: 11 mA at hFE 25")
        C("2.2u 100V", f"P48_{k}_B", f"P48_{k}", fp=C1210,
          Note="Miller C-B: linear ramp of about 0.1-0.2 s (X7R at 48 V keeps about 1 uF)")
        add(ref("Q"), "Transistor_BJT:MMBTA42", "MMBTA42", SOT23, {"1": f"PH48_{k}_G", "2": "GND", "3": f"P48_{k}_BC"},
            Note="level shift from R2 (3.3 V); 300 V NPN: its collector sees 48 V when off (MMBT3904 is 40 V)")
        R("10k", f"PH48_{k}", f"PH48_{k}_G")
        R("100k", f"PH48_{k}_G", "GND")
        R("47k", f"P48_{k}", "GND", fp=R0603, Note="bleeds the rail when off")
        C("10u 63V", f"P48_{k}", fp=C1210, Note="AC ground for the 6.81k feed")

    # ---------------------------------------------------------------- Mic/Line 1-2: combo, phantom, OPA1612 front end, two paths
    for k in (1, 2):
        m = f"M{k}"
        add(ref("J"), "Connector_Audio:NCJ6FI-V", f"MIC/LINE {k}", COMBO,
            {"1": "GND", "2": f"{m}_X2", "3": f"{m}_X3", "G": "GND", "T": f"{m}_TT", "R": f"{m}_TR", "S": "GND"},
            LCSC="C368503", Note=f"Mic/Line {k}: XLR with phantom (R72), TRS line without; Neutrik NCJ6FI-V vertical")
        R("6.81k", f"P48_{k}", f"{m}_X2", fp=R1206, Note="phantom feed 0.1 %, matched pair")
        R("6.81k", f"P48_{k}", f"{m}_X3", fp=R1206, Note="phantom feed 0.1 %, matched pair")
        CP("47u 63V", f"{m}_X2", f"{m}_P", fp=CP8, Note="phantom blocking (doc 34, 2.3)")
        CP("47u 63V", f"{m}_X3", f"{m}_N", fp=CP8, Note="phantom blocking")
        R("0", f"{m}_TT", f"{m}_P", Note="TRS tip joins after the caps (no phantom on TRS); FS +11.9 dBu, clip +13.6 dBu")
        R("0", f"{m}_TR", f"{m}_N")
        for leg in ("P", "N"):
            R("10k", f"{m}_{leg}", "GND", Note="discharge / bias")
            # rev 0.9 (audit 18.11.2026, B2): hot-plugging an unbalanced XLR (pin 3 to shield) with phantom on moves the far side of the charged 47 uF
            # (46 V) to about -46 V. Before: 10 R into 1N4148W clamps = about 3.5 A for 0.5 ms and the -12 V rail pulled. Now a bidirectional TVS
            # (SMBJ18CA: 18 V standoff above the +24 dBu TS line peak 17.4 V; breakdown 20-22 V) takes the first peak at the cap, and 47 R (0805) limits the
            # tail into the clamps to 0.2 A for 1.5 ms (cap 47 uF x 47 R; 7.6 mJ in the resistor). Noise: 2 x 47 R adds about 1 dB to the 150 R mic.
            add(ref("D"), "Device:D_TVS", "SMBJ18CA", SMB, {"1": f"{m}_{leg}", "2": "GND"}, LCSC="C83327",
                Note="phantom hot-plug: clamps the far side of the blocking cap (rev 0.9, audit B2); Littelfuse C83327, 10042 pcs at JLC 18.11.2026")
            R("47", f"{m}_{leg}", f"{m}_{leg}X", fp=R0805, LCSC="C17714", Note="series 47 R (rev 0.9; was 10 R): limits the hot-plug tail into the clamps, 0.2 A / 1.5 ms")
            R("15k", f"{m}_{leg}X", f"{m}_{leg}A", fp=R0603, Note="attenuator -12 dB: series 15k, 0.1 %")
            R("4.99k", f"{m}_{leg}A", "GND", fp=R0603, Note="attenuator -12 dB: shunt 4.99k, 0.1 % (ratio 0.250)")
            clamp(f"{m}_{leg}S")
        add(ref("K"), RELAY[0], "G6K-2F-Y 5V", RELAY[1],
            {"A1": "+5V", "A2": f"ATT{k}_K", "11": f"{m}_PS", "12": f"{m}_PX", "14": f"{m}_PA",
             "21": f"{m}_NS", "22": f"{m}_NX", "24": f"{m}_NA"},
            LCSC="C2982926", Note=f"Mic/Line {k} attenuator -12 dB (line +24 dBu): de-energised = direct, energised = attenuated")
        add(ref("Q"), "Transistor_FET:2N7002", "2N7002", SOT23, {"1": f"ATT{k}_G", "2": "GND", "3": f"ATT{k}_K"}, Note="attenuator relay")
        R("1k", f"ATT{k}", f"ATT{k}_G")
        R("100k", f"ATT{k}_G", "GND")
        add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": "+5V", "2": f"ATT{k}_K"}, Note="flyback")
        C("470p C0G", f"{m}_PS", f"{m}_NS", fp=C0603, Note="RF")
        u = ref("U")
        add(u, "Amplifier_Operational:OPA1612AxD", "OPA1612", SOIC8,
            {"1": f"{m}_A", "2": f"{m}_FA", "3": f"{m}_PS", "4": "-12V", "5": f"{m}_NS", "6": f"{m}_FB", "7": f"{m}_B", "8": "+12V"},
            LCSC="C94590", Note="two-op-amp front end, gain 1 + 2 x 499 / 332 = 4.01 (+12 dB)")
        R("499", f"{m}_A", f"{m}_FA", Note="0.1 %")
        R("499", f"{m}_B", f"{m}_FB", Note="0.1 %")
        R("332", f"{m}_FA", f"{m}_FB", Note="Rg 0.1 %")
        supply(u)
        base = 2 * (k - 1)                              # mic 1 -> ADC1/2, mic 2 -> ADC3/4
        fda(f"{m}L", f"{m}_A", f"{m}_B", f"ADC{base + 1}_P", f"ADC{base + 1}_N", "10k", "6.81k", "150p",
            f"Mic {k} loud path -> ADC{base + 1} (FS at +11.9 dBu in)")
        fda(f"{m}Q", f"{m}_A", f"{m}_B", f"ADC{base + 2}_P", f"ADC{base + 2}_N", "1k", "68.1k", "18p",
            f"Mic {k} quiet path (+40 dB, FS at -28.1 dBu in) -> ADC{base + 2}")

    # ---------------------------------------------------------------- Hi-Z 1-2: OPA1642 buffer, two paths
    u = ref("U")
    hz = {}
    for k in (1, 2):
        h = f"H{k}"
        add(ref("J"), "Connector_Audio:AudioJack3", f"HI-Z {k}", TRS, {"T": f"{h}_T", "R": None, "S": "GND"},
            Note="Hi-Z 1 MOhm (also pedal return, R65); Neutrik NJ3FD-V vertical")
        R("1M", f"{h}_T", "GND", Note="input impedance")
        R("1k", f"{h}_T", f"{h}_S", fp=R0603, Note="series")
        clamp(f"{h}_S")
        C("100p C0G", f"{h}_S", fp=C0603)
        hz[k] = h
    add(u, "Amplifier_Operational:OPA1612AxD", "OPA1642", SOIC8,
        {"1": "H1_B", "2": "H1_B", "3": "H1_S", "4": "-12V", "5": "H2_S", "6": "H2_B", "7": "H2_B", "8": "+12V"},
        LCSC="C67640", Note="OPA1642 JFET dual (same pinout as the OPA1612 symbol): unity buffers")
    supply(u)
    for k in (1, 2):
        base = 4 + 2 * (k - 1)                          # Hi-Z 1 -> ADC5/6, Hi-Z 2 -> ADC7/8
        fda(f"H{k}L", f"H{k}_B", "GND", f"ADC{base + 1}_P", f"ADC{base + 1}_N", "10k", "13.7k", "68p",
            f"Hi-Z {k} loud path -> ADC{base + 1} (FS at +17.9 dBu)")
        fda(f"H{k}Q", f"H{k}_B", "GND", f"ADC{base + 2}_P", f"ADC{base + 2}_N", "1k", "137k", "18p",
            f"Hi-Z {k} quiet path (+40 dB, FS at -22.1 dBu) -> ADC{base + 2}")

    # ---------------------------------------------------------------- Phono L/R: relay phono/line, RIAA on OPA1612
    u_riaa = ref("U")
    riaa_pins = {"4": "-12V", "8": "+12V"}
    for k, side in ((1, "L"), (2, "R")):
        p = f"PH{side}"
        add(ref("J"), "Connector_Audio:AudioJack2", f"PHONO {side}", RCA, {"T": f"{p}_J", "S": "GND"}, LCSC=RCA_LCSC,
            Note="RCA jack RCJ-025, vertical, front face 22.1 mm above the board, no panel nut")
        add(ref("K"), RELAY[0], "G6K-2F-Y 5V", RELAY[1],
            {"A1": "+5V", "A2": "PHONO_K", "11": f"{p}_J", "12": f"{p}_LIN", "14": f"{p}_RIN",
             "21": f"{p}_DRV", "22": f"{p}_LIN", "24": f"{p}_R75"},
            LCSC="C2982926", Note="de-energised = line (R2 boots low); energised = phono (R118)")
        R("47k", f"{p}_RIN", "GND", Note="MM load 47k")
        C("100p C0G", f"{p}_RIN", fp=C0603, Note="MM load capacitance")
        R("100", f"{p}_RIN", f"{p}_RINS", fp=R0603)
        ip, im, o = ("3", "2", "1") if k == 1 else ("5", "6", "7")
        riaa_pins.update({ip: f"{p}_RINS", im: f"{p}_RFB", o: f"{p}_ROUT"})
        R("130", f"{p}_RFB", f"{p}_RG", Note="RIAA gain leg 0.1 %: +35.0 dB at 1 kHz")
        CP("470u 16V", f"{p}_RG", "GND", fp=CP8, Note="DC gain 1, corner 2.6 Hz")
        R("68.1k", f"{p}_ROUT", f"{p}_RN1", Note="RIAA 3180 us: 68.1k x 47n, 0.1 %")
        C("47n C0G", f"{p}_ROUT", f"{p}_RN1", fp=C1206, Note="1 %")
        R("7.42k", f"{p}_RN1", f"{p}_RFB", Note="RIAA 318 us: 9 x (Rg + R2), 0.1 %")
        R("787", f"{p}_ROUT", f"{p}_R75", fp=R0603, Note="passive 75 us: (787 || 16.7k FDA input) x 100n")
        C("100n C0G", f"{p}_R75", fp=C1206, Note="75 us, 1 %")
        R("100k", f"{p}_LIN", "GND", Note="line input bias")
        fda(f"PF{side}", f"{p}_DRV", "GND", f"ADC{8 + k}_P", f"ADC{8 + k}_N",
            "10k", "41.2k", "22p", f"Phono/line {side} -> ADC{8 + k} (x 4.12, FS 2.02 Vrms)")
    add(u_riaa, "Amplifier_Operational:OPA1612AxD", "OPA1612", SOIC8, riaa_pins, LCSC="C94590", Note="RIAA L/R")
    supply(u_riaa)
    add(ref("Q"), "Transistor_FET:2N7002", "2N7002", SOT23, {"1": "PHONO_G", "2": "GND", "3": "PHONO_K"}, Note="phono relays")
    R("1k", "PHONO", "PHONO_G")
    R("100k", "PHONO_G", "GND")
    add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": "+5V", "2": "PHONO_K"}, Note="flyback")

    # ---------------------------------------------------------------- Line 1-8: OPA1637 receivers, +24 dBu FS (R135)
    for k in range(1, 9):
        add(ref("J"), "Connector_Audio:AudioJack3", f"LINE {k}", TRS, {"T": f"L{k}_T", "R": f"L{k}_R", "S": "GND"},
            Note="balanced TRS, also mono TS (ring to sleeve); Neutrik NJ3FD-V vertical")
        R("100", f"L{k}_T", f"L{k}_TS", fp=R0603, Note="RF")
        R("100", f"L{k}_R", f"L{k}_RS", fp=R0603)
        C("1n C0G", f"L{k}_TS", fp=C0603)
        C("1n C0G", f"L{k}_RS", fp=C0603)
        fda(f"L{k}", f"L{k}_TS", f"L{k}_RS", f"ADC{10 + k}_P", f"ADC{10 + k}_N",
            "10k", "6.81k", "150p", f"Line {k} -> ADC{10 + k} (FS +24.1 dBu)")

    # ---------------------------------------------------------------- outputs: OPA1612 difference amps, impedance-balanced, relays
    outs = [("ML", "MAIN L"), ("MR", "MAIN R"), ("AL", "AUX L"), ("AR", "AUX R")]
    for i in range(2):
        u = ref("U")
        pins = {"4": "-12V", "8": "+12V"}
        for (ch, _), (ip, im, o) in zip(outs[2 * i:2 * i + 2], (("3", "2", "1"), ("5", "6", "7"))):
            pins.update({ip: f"{ch}_IP", im: f"{ch}_IM", o: f"{ch}_O"})
            R("10k", f"DAC_{ch}_P", f"{ch}_IP", Note="0.1 %")
            R("30.9k", f"{ch}_IP", "GND", Note="0.1 %: gain 3.09 -> 6.19 Vrms = +18.0 dBu at DAC FS (R64)")
            R("10k", f"DAC_{ch}_N", f"{ch}_IM", Note="0.1 %")
            R("30.9k", f"{ch}_O", f"{ch}_IM", Note="0.1 %")
            C("47p C0G", f"{ch}_O", f"{ch}_IM", fp=C0603)
            R("47", f"{ch}_O", f"{ch}_HOT", fp=R0603, Note="build-out, impedance balance")
        add(u, "Amplifier_Operational:OPA1612AxD", "OPA1612", SOIC8, pins, LCSC="C94590", Note="output stage")
        supply(u)
    for ch, label in outs:
        add(ref("J"), "Connector_Audio:AudioJack3", label, TRS, {"T": f"{ch}_TIP", "R": f"{ch}_RING", "S": "GND"},
            Note="impedance-balanced TRS (R64); Neutrik NJ3FD-V vertical")
        R("47", f"{ch}_RING", "GND", fp=R0603, Note="cold leg: same impedance as hot")
    for ch in ("ML", "MR"):
        R("100", f"{ch}_O", f"{ch}_RCAO", fp=R0603, Note="RCA = copy of Main (R23)")
    for side, ch in (("L", "ML"), ("R", "MR")):
        add(ref("J"), "Connector_Audio:AudioJack2", f"RCA {side}", RCA, {"T": f"RCA{side}_TIP", "S": "GND"}, LCSC=RCA_LCSC,
            Note="RCA jack RCJ-025, vertical, front face 22.1 mm above the board, no panel nut")
    for (a, b), name in ((("ML", "MR"), "MAIN"), (("AL", "AR"), "AUX"), (("RCA_L", "RCA_R"), "RCA")):
        if name == "RCA":
            c1, d1, c2, d2 = "ML_RCAO", "RCAL_TIP", "MR_RCAO", "RCAR_TIP"
        else:
            c1, d1, c2, d2 = f"{a}_HOT", f"{a}_TIP", f"{b}_HOT", f"{b}_TIP"
        add(ref("K"), RELAY[0], "G6K-2F-Y 5V", RELAY[1],
            {"A1": "+5V", "A2": "OUT_K", "11": c1, "12": None, "14": d1, "21": c2, "22": None, "24": d2},
            LCSC="C2982926", Note=f"{name} output relay: normally open, opens without power (R66, R137)")
    add(ref("Q"), "Transistor_FET:2N7002", "AO3400A", SOT23, {"1": "MUTE_G", "2": "OUT_KS", "3": "OUT_K"}, LCSC="C20917",
        Note="MUTE and R2_OK in series: relays close only when both are high. Rev 0.9 (audit): AO3400A (Rds 0.06 R at 2.5 V) instead of 2N7002: 3 coils of 21 mA "
        "(G6K-2F-Y 5 V, 237 R, must operate 4.0 V) through two 2N7002 at Vgs 3.3 V left 3.8-4.0 V at +5 V -5 %")
    add(ref("Q"), "Transistor_FET:2N7002", "AO3400A", SOT23, {"1": "R2OK_G", "2": "GND", "3": "OUT_KS"}, LCSC="C20917")
    R("1k", "MUTE", "MUTE_G")
    R("100k", "MUTE_G", "GND")
    R("1k", "R2_OK", "R2OK_G")
    R("100k", "R2OK_G", "GND")
    add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": "+5V", "2": "OUT_K"}, Note="flyback (3 coils)")
    K.mount_holes(add, ref, HOLES, "M3 standoff (Codex review 15.11.2026): corners first; the final positions come with the enclosure")
    return P


JACKS = {"MAIN L": (292, 95), "MAIN R": (314, 95), "AUX L": (292, 69), "AUX R": (314, 69), "RCA L": (292, 43), "RCA R": (314, 43),
         "MIC/LINE 1": (362, 95), "MIC/LINE 2": (394, 95), "HI-Z 1": (362, 69), "HI-Z 2": (394, 69),   # rev 1.0: rear wall v6.1, rows z 95 / 69 / 43 (docs/ru/img/41_rear_v6_1_jacks.csv)
         "PHONO L": (434, 95), "PHONO R": (456, 95), **{f"LINE {i + 1}": (434 + 22 * (i % 4), 69 if i < 4 else 43) for i in range(8)}}
X0, Z0 = 273.0, 113.0       # board origin in the rear-wall coordinates of tools/rear_panel.py (x from the left, z up)


def placement():
    """Rev 0.4: the jacks at the 3D model positions (top side, facing the wall; tools/rear_panel.py), cable headers in a row along
    the bottom edge, the rest by hardware/common/gen/autoplace.py (ICs on a grid, small parts around the IC they share signals with)."""
    import autoplace
    fixed = {}
    for p in parts():
        if p["ref"].startswith("J") and p["value"] in JACKS:
            xr, z = JACKS[p["value"]]
            fixed[p["ref"]] = (xr - X0, Z0 - z, 0, "top")
    for ref, x in (("J4", 40.0), ("J1", 82.0), ("J5", 122.0), ("J2", 165.0), ("J3", 200.0)):
        # R171 (17.11.2026): the two A1 headers (J4, J5) are raised by A1_RISE so they meet A1's sockets: A1 now stands on a tray
        # over the battery (R162), the socket rows are about 30.4 / 32.9 mm above the floor, the old row was at 11.5 / 14.0
        y = {"J1": 85.5, "J3": 90.5}.get(ref, 92.5) + (H - 96.0) - (A1_RISE if ref in ("J4", "J5") else 0.0)   # rev 0.8: bottom edge kept at z 8, so + (H - 96)
        fixed[ref] = (x, y, 90, "bottom")          # cable headers (2 x 25 and 2 x 20 to A1, small ones) along the bottom edge
    fixed.update(K.hole_fixed(parts(), HOLES))
    return autoplace.place(sys.modules[__name__], fixed=fixed, conn_side="bottom")


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; duplicate refs:", sorted({r for r in refs if refs.count(r) > 1}))
    single = {}
    for p in P:
        for pin, nn in p["pins"].items():
            if nn:
                single.setdefault(nn, []).append(f"{p['ref']}.{pin}")
    print("single-pin nets:", sorted(k for k, v in single.items() if len(v) == 1))
