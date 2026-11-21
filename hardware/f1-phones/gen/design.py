"""F1 - Headphone board (front lip, horizontal, P94, R159, R165): two 6.35 mm stereo jacks (Cliff S1 CL1115, 12.7 mm high) and one TI OPA1622
per jack. Each channel is a difference amplifier that takes the CS4308P I-V stage pair from A1 (2 Vrms differential full scale, DAC
outputs 5-8 = Phones 1 / Phones 2, R87: the volume is the DAC's digital attenuator) and gives 4 Vrms single-ended: gain 20k / 10k = 2 =
R67 (>= 4 V on 600 Ohm, >= 30 mA on 32 Ohm; the OPA1622 gives +145 / -130 mA).
Single source of truth for the schematic. Research: docs/ru/21_audio_board.md, docs/ru/34_rear_boards_research.md (3); decisions R8, R66,
R67, R87, R137, P94.

Mute (R66, R137): a G6K-2 DPDT per jack, normally open, closes only when MUTE and R2_OK are both high (same logic as the output relays
on R1); the OPA1622 enable pin follows MUTE (held low while R2 boots, thresholds 0.78 / 0.82 V against the device ground, datasheet 7.3.3 and
7.4.2). The enable pin is not a high-impedance output: the relay is the real mute.

Connectors (contract with the other boards): from A1 2x6 audio header (pairs with a ground between them), from PW JST PH 4 (+12 V, GND, -12 V,
+5 V for the relays), from R1 JST PH 3 (MUTE, R2_OK, GND).
Rev 0.1 (14.11.2026, PC) = schematic only.
Rev 0.4 (18.11.2026, PC, R174/R176): no front lip. The board (100 x 38 mm) lies on the floor under the front edge of P1, the jacks stand on the
front wall (nose to the wall), all parts on the top side, height <= 12 mm (jacks 12.7 mm, relays 5.4 mm), cable headers lie flat in the rear strip.
Rev 0.3 (16.11.2026, PC, R165, doc 39): low case. The board lies on 1 mm standoffs in the 28 mm lip in front of P1, so EVERYTHING is on the top
side (no room underneath): jacks Cliff S1/BBB CL1115 (Digikey 4654-CL1115-ND, hand-soldered, not at JLCPCB; 12.7 mm high instead of 15.67), the
cable headers lie flat (2x6 right angle, JST PH side entry), board 135 x 27 mm.
Rev 0.5 (18.11.2026, schematic audit notes/reviews/schematics_2026-11-18.md): mute-chain FETs 2N7002 -> AO3400A (C20917), nothing else changed.
Rev 0.6 (20.11.2026): placement only: the small parts are packed with a 1.4 mm courtyard gap (was 0.25) so that the router can fan out the 0.5 mm pitch pins of the OPA1622.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "f1-phones"
ID = "F1"
TITLE = "F1 - Headphones: 2 x Cliff S1 6.35 mm, 2 x OPA1622 difference amplifiers x2, mute relays"
REV = "0.8"
M1_LIB = K.M1_LIB
BUS_NOTE = ("From A1: Phones 1 and 2 as differential pairs (2 Vrms FS) -> OPA1622 difference amp x2 -> 10 R -> relay -> NMJ6HCD2; "
            "volume is the DAC's digital attenuator (R87); mute relays need MUTE and R2_OK (R66, R137)")
PWR_FLAG_NETS = ("+12V", "-12V")      # ERC: rails from the connector (+5V already gets the standard flag)
NO_PWR_FLAG = ("+3V3",)
W, H = 100.0, 38.0          # rev 0.4 (R174/R176, no front lip): board on the floor under the front edge of P1; y 0 = 1.5 mm behind the front wall inside, nose of the jacks towards the top edge
HOLES = [(4.0, 4.0), (96.0, 4.0), (4.0, 34.0), (96.0, 34.0), (30.0, 31.0)]   # M3, board coordinates (KiCad, y down); 18.11.2026
LAYERS = 2

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603 = "Resistor_SMD:R_0603_1608Metric"
C1210 = "Capacitor_SMD:C_1210_3225Metric"
SOT23, SOD123 = "Package_TO_SOT_SMD:SOT-23", "Diode_SMD:D_SOD-123"
JACK = "ShtukaDruka:Jack_6.35mm_Cliff_S1_Horizontal"   # pads S R T (make, pins 4 5 6) and SN RN TN (break, 1 2 3) of the Cliff drawing CL1115
VSON10 = "Package_SON:Texas_S-PVSON-N10"
RELAY = ("Relay:Omron_G6K-2", "Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y")
PH = "Connector_JST:JST_PH_S{n}B-PH-K_1x0{n}_P2.00mm_Horizontal"   # side entry, 4.8 mm high (R168 style)


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

    # ---------------------------------------------------------------- connectors
    pairs = ["HP1L_P", "HP1L_N", "GND", "HP1R_P", "HP1R_N", "GND", "HP2L_P", "HP2L_N", "GND", "HP2R_P", "HP2R_N", "GND"]
    add(ref("J"), "Connector_Generic:Conn_02x06_Odd_Even", "from A1", "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Horizontal",
        {str(i + 1): net for i, net in enumerate(pairs)},
        Note="Phones 1/2 from the CS4308P I-V stages on A1 (outputs 5-8): L+ L- GND R+ R- GND per jack, pins 1-12; twisted pairs, "
        "2 Vrms differential full scale")
    add(ref("J"), "Connector_Generic:Conn_01x04", "from PW", PH.format(n=4), {"1": "+12V", "2": "GND", "3": "-12V", "4": "+5V"},
        Note="+-12 V for the amplifiers, +5 V for the relay coils (PW 'to F1', 4 pins from PW rev 0.5)")
    add(ref("J"), "Connector_Generic:Conn_01x05", "from R1 (mute, detect)", PH.format(n=5), {"1": "MUTE", "2": "R2_OK", "3": "GND", "4": "DET_HP1", "5": "DET_HP2"},
        Note="MUTE and R2_OK from R2 via R1 ('to F1' header on R1 rev 0.4); low while R2 boots (R66, R137). Rev 0.8 (P124): pins 4, 5 = cable detect HP1, HP2 to R2 (high = plugged)")
    for _ in range(2):
        C("10u 25V", "+12V", fp=C1210)
        C("10u 25V", "GND", "-12V", fp=C1210)

    # ---------------------------------------------------------------- mute logic: coils close only with MUTE and R2_OK
    R("1k", "MUTE", "MUTE_G")
    R("100k", "MUTE_G", "GND")
    R("1k", "R2_OK", "R2OK_G")
    R("100k", "R2OK_G", "GND")
    add(ref("Q"), "Transistor_FET:2N7002", "AO3400A", SOT23, {"1": "MUTE_G", "2": "COIL_KS", "3": "COIL_K"}, LCSC="C20917",
        Note="MUTE and R2_OK in series: the relays close only when both are high. Rev 0.5 (audit 18.11.2026): AO3400A instead of 2N7002 (two coils of 21 mA "
        "through two 2N7002 at Vgs 3.3 V: coil voltage close to the 4.0 V must-operate of the G6K-2F-Y 5 V)")
    add(ref("Q"), "Transistor_FET:2N7002", "AO3400A", SOT23, {"1": "R2OK_G", "2": "GND", "3": "COIL_KS"}, LCSC="C20917")
    add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": "+5V", "2": "COIL_K"}, Note="flyback")

    # ---------------------------------------------------------------- per jack: OPA1622 difference amps, relay, jack
    for k in (1, 2):
        h = f"HP{k}"
        u = ref("U")
        add(u, "Amplifier_Audio:OPA1622", "OPA1622", VSON10,
            {"1": f"{h}L_IP", "2": "+12V", "3": "GND", "4": "-12V", "5": f"{h}R_IP", "6": f"{h}R_IM", "7": f"{h}R_O", "8": f"{h}_EN",
             "9": f"{h}L_O", "10": f"{h}L_IM", "11": "-12V"},
            LCSC="C2876559", Note=f"Phones {k}: two difference amplifiers, gain 2; thermal pad to V-; EN follows MUTE (0.82 V / 0.78 V vs GND pin)")
        R("1k", "MUTE", f"{h}_EN", Note="enable: low while MUTE is low (supply ramp, boot); never left floating")
        R("100k", f"{h}_EN", "GND")
        C("100n 25V", "+12V", fp=C0603)
        C("100n 25V", "-12V", fp=C0603)
        for ch in ("L", "R"):
            c = f"{h}{ch}"
            R("10k", f"{c}_P", f"{c}_IP", fp=R0603, Note="0.1 %: Rin")
            R("10k", f"{c}_N", f"{c}_IM", fp=R0603, Note="0.1 %: Rin")
            R("20k", f"{c}_O", f"{c}_IM", fp=R0603, Note="0.1 %: Rf, gain 2")
            R("20k", f"{c}_IP", "GND", fp=R0603, Note="0.1 %: Rg")
            C("22p C0G", f"{c}_O", f"{c}_IM", fp=C0603, Note="Cf, stability with the cable - check")
            R("10", f"{c}_O", f"{c}_OR", fp=R0603, Note="output build-out; feedback is taken before it")
        # relay: first contact set tip (left), second ring (right); common 11 / 21, normally open 14 / 24
        add(ref("K"), RELAY[0], "G6K-2F-Y 5V", RELAY[1],
            {"A1": "+5V", "A2": "COIL_K", "11": f"{h}L_OR", "12": None, "14": f"{h}_TIP", "21": f"{h}R_OR", "22": None, "24": f"{h}_RING"},
            LCSC="C2982926", Note=f"Phones {k} mute relay: normally open, opens without power (R66, R137)")
        add(ref("J"), "Connector_Audio:AudioJack3_Switch", f"PHONES {k}", JACK,
            {"T": f"{h}_TIP", "TN": None, "R": f"{h}_RING", "RN": None, "S": "GND", "SN": f"{h}_SN"},
            Note=f"Phones {k}: Cliff S1/BBB CL1115 (Digikey 4654-CL1115-ND), 6.35 mm stereo, switched (rev 0.8: the sleeve break contact SN is the cable detect), 12.7 mm high, "
            "hand-soldered (not at JLCPCB). Wall 3 mm + fibre washer 1.6 + nut 5.0 is 9.6 mm, the thread 9.35 mm: leave the washer out")
        # rev 0.8 (P124, R202): cable detect and discharge. SN = sleeve (GND) while the jack is empty, opens when a plug goes in: 100k pull-up to +5V,
        # 10k + 100 nF = 1 ms to the detect line (high = plugged); 100k from tip and ring to GND at the jack side discharge the cable while the relay is open.
        R("100k", "+5V", f"{h}_SN", Note="cable detect pull-up (SN is on GND while the jack is empty)")
        R("10k", f"{h}_SN", f"DET_{h}", Note="detect line, RC 1 ms with 100 nF")
        C("100n", f"DET_{h}", Note="detect debounce, RC 1 ms")
        R("100k", f"{h}_TIP", "GND", Note="discharge of the cable while the relay is open")
        R("100k", f"{h}_RING", "GND", Note="discharge of the cable while the relay is open")
    K.mount_holes(add, ref, HOLES, "M3 standoff (Codex review 15.11.2026): corners first; the final positions come with the enclosure")
    return P


def placement():
    """Rev 0.4 (R174/R176): the board lies on the floor under the front edge of P1, 100 x 38 mm, EVERYTHING on the top side. The wall is at board
    y -1.5 (inside face); the Cliff jacks sit on it nose to the top edge, centres 48 mm apart (x 27 / 75 = model x 32 / 80 with the board at model
    x 5); the body of a jack is 24.25 mm deep (to y 22.75), so the rest of the parts go between the jacks and in the rear strip y 23.5-37.4. The cable
    headers lie flat in the rear strip and open towards the rear edge (towards P1's rear / A1). Parts are packed by hardware/common/gen/packer.py. No routing."""
    import packer
    P = parts()
    t = "top"
    fixed = {}
    jacks = [p["ref"] for p in P if p["value"].startswith("PHONES")]
    for r, x in zip(jacks, (27.0, 75.0)):
        fixed[r] = (x, 9.1, 0, t)                  # centre of the pad field: rows 4/1 at y 2.75, 2/5 at 9.1, 3/6 at 15.45; body to y 22.75
    heads = [p["ref"] for p in P if p["lib"].startswith("Connector_Generic") and p["ref"] not in jacks]
    for r, (x, y, rot) in zip(heads, ((51.0, 25.5, 270), (70.0, 30.6, 0), (84.0, 30.6, 0))):
        fixed[r] = (x, y, rot, t)
    fixed.update(K.hole_fixed(P, HOLES))
    grp = {1: [], 2: [], 0: []}
    for p in P:
        if p["ref"] in fixed:
            continue
        side = 0
        for pin_net in p["pins"].values():
            if pin_net and pin_net.startswith("HP1"):
                side = 1
            elif pin_net and pin_net.startswith("HP2"):
                side = 2
        if p["value"].startswith("G6K"):
            side = 1 if "HP1" in str(p["pins"]) else 2
        grp[side].append(p["ref"])
    G = [(24.0, 29.0, t, grp[1], 0), (58.0, 10.0, t, grp[2], 0), (*[float(v) for v in os.environ.get("F1_G0", "88,10").split(",")], t, grp[0], 0)]
    # rev 0.8 (P124): the HP2 group anchor 52,10 -> 58,10 (the relay K2 no longer fitted next to the jack after +10 small parts and the 5-pin header); header 3 at x 84 (5 pins, 12.4 mm)
    # rev 0.7: the mute-logic cluster (anchor 88,10; before 90,14): 2 unrouted after the GND pour instead of 4 (probes 88,10 -> 2, 95,24 -> 5, 62,18 -> 6, 40,12 -> 4; exp_gap, Freerouting 1.9.0)
    # rev 0.6 (20.11.2026, router finding f1-four-gaps.md): the pins +12V / GND / -12V of the OPA1622 are on a 0.5 mm pitch and the GND pad could not leave the chip:
    # courtyard gap 0.25 -> 1.4 mm so that the neighbouring resistors, capacitors and the relay leave a free corridor for the fan-out of pins 2-4 (and the EN, HP1R_IM, HP1L_O nets)
    return packer.pack(sys.modules[__name__], P, fixed, G, [(0, 0, W, H)], gap=float(os.environ.get("PLACE_GAP", "1.4")),
                       ic_gap=(float(os.environ["PLACE_ICGAP"]) if os.environ.get("PLACE_ICGAP") else None))


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
