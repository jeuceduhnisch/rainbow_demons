"""Canonical isolated-pad layouts for the Nano R4 three-head looper.

Coordinates always refer to the COMPONENT side: columns A-X left-to-right,
rows 1-36 top-to-bottom. Solder-side diagrams mirror columns only.
Every point-to-point link is insulated unless its note explicitly says BARE.
"""

COLS = "ABCDEFGHIJKLMNOPQRSTUVWX"
ROWS = 36


def xy(p):
    return COLS.index(p[0]), int(p[1:]) - 1


def column(col, first, last):
    return [f"{col}{r}" for r in range(first, last + 1)]


def connector_2x(start_row, rows, left, right, nets):
    out = {}
    for index in range(rows):
        pin_a = index * 2 + 1
        pin_b = pin_a + 1
        row = start_row + index
        out[pin_a] = (f"{left}{row}", nets[pin_a])
        out[pin_b] = (f"{right}{row}", nets[pin_b])
    return out


J1_NETS = {
    1: "+12P", 2: "GND", 3: "+5N", 4: "GND",
    5: "AUDIO_ADC", 6: "GND", 7: "DAC_RAW", 8: "GND",
    9: "HEAD1", 10: "GND", 11: "HEAD2", 12: "GND",
    13: "HEAD3", 14: "GND", 15: "AGE", 16: "GND",
    17: "MIX", 18: "GND", 19: "REC_BTN", 20: "PLAY_BTN",
    21: "Q_OCT", 22: "Q_SEMI", 23: "PLAY_MODE", 24: "REC_CV",
    25: "PLAY_CV", 26: "LED_R_IN", 27: "LED_G_IN", 28: "+5N",
    29: "GND", 30: "KEY",
}


CORE_J1 = connector_2x(20, 15, "H", "I", J1_NETS)
INTERFACE_J1 = connector_2x(20, 15, "H", "I", J1_NETS)


NANO = {
    "D13": ("H3", "SCK"), "3V3": ("H4", "NC_3V3"),
    "AREF": ("H5", "NC_AREF"), "A0": ("H6", "DAC_RAW"),
    "A1": ("H7", "AUDIO_FILT"), "A2": ("H8", "HEAD1_F"),
    "A3": ("H9", "HEAD2_F"), "A4": ("H10", "HEAD3_F"),
    "A5": ("H11", "AGE_F"), "A6": ("H12", "MIX_F"),
    "A7": ("H13", "NC_A7"), "5V": ("H14", "+5N"),
    "BOOT": ("H15", "NC_BOOT"), "GND_L": ("H16", "GND"),
    "VIN": ("H17", "VIN"),
    "D12": ("N3", "CIPO"), "D11": ("N4", "COPI"),
    "D10": ("N5", "SRAM_CS"), "D9": ("N6", "LED_R_IN"),
    "D8": ("N7", "PLAY_CV"), "D7": ("N8", "REC_CV"),
    "D6": ("N9", "PLAY_MODE"), "D5": ("N10", "Q_SEMI"),
    "D4": ("N11", "Q_OCT"), "D3": ("N12", "PLAY_BTN"),
    "D2": ("N13", "REC_BTN"), "GND_R": ("N14", "GND"),
    "RST": ("N15", "NC_RST"), "D0": ("N16", "LED_G_IN"),
    "D1": ("N17", "NC_D1"),
}


SRAM = {
    1: ("B4", "SRAM_CS", "CS"), 2: ("B5", "CIPO", "SO"),
    3: ("B6", "SIO2", "SIO2"), 4: ("B7", "GND", "VSS"),
    5: ("E7", "COPI", "SI"), 6: ("E6", "SCK", "SCK"),
    7: ("E5", "HOLD", "HOLD"), 8: ("E4", "+5N", "VCC"),
}


CORE_PARTS = [
    dict(ref="R1", value="10K", kind="R", pads=["B11", "E11"], nets=["SIO2", "+5N"]),
    dict(ref="R2", value="10K", kind="R", pads=["B13", "E13"], nets=["HOLD", "+5N"]),
    dict(ref="C1", value="100n", kind="C", pads=["G1", "I1"], nets=["+5N", "GND"]),
    dict(ref="JP1", value="VIN ENABLE", kind="JP", pads=["F18", "G18"], nets=["+12P", "VIN"]),
    dict(ref="R3", value="1K", kind="R", pads=["P20", "S20"], nets=["HEAD1", "HEAD1_F"]),
    dict(ref="C2", value="100n", kind="C", pads=["T20", "U20"], nets=["HEAD1_F", "GND"]),
    dict(ref="R4", value="1K", kind="R", pads=["P22", "S22"], nets=["HEAD2", "HEAD2_F"]),
    dict(ref="C3", value="100n", kind="C", pads=["T22", "U22"], nets=["HEAD2_F", "GND"]),
    dict(ref="R5", value="1K", kind="R", pads=["P24", "S24"], nets=["HEAD3", "HEAD3_F"]),
    dict(ref="C4", value="100n", kind="C", pads=["T24", "U24"], nets=["HEAD3_F", "GND"]),
    dict(ref="R6", value="1K", kind="R", pads=["P26", "S26"], nets=["AGE", "AGE_F"]),
    dict(ref="C5", value="100n", kind="C", pads=["T26", "U26"], nets=["AGE_F", "GND"]),
    dict(ref="R7", value="1K", kind="R", pads=["P28", "S28"], nets=["MIX", "MIX_F"]),
    dict(ref="C6", value="100n", kind="C", pads=["T28", "U28"], nets=["MIX_F", "GND"]),
    dict(ref="R8", value="1K", kind="R", pads=["P30", "S30"], nets=["AUDIO_ADC", "AUDIO_FILT"]),
    dict(ref="C7", value="22n", kind="C", pads=["S31", "U31"], nets=["AUDIO_FILT", "GND"]),
    dict(ref="D1", value="BAT85", kind="D", pads=["T30", "X30"], nets=["AUDIO_FILT", "+5N"], band=1),
    dict(ref="D2", value="BAT85", kind="D", pads=["U32", "S32"], nets=["GND", "AUDIO_FILT"], band=1),
    dict(ref="C8", value="100n", kind="C", pads=["U33", "X33"], nets=["GND", "+5N"]),
    dict(ref="C9", value="10u", kind="EL", pads=["X35", "U35"], nets=["+5N", "GND"], plus=0),
]


CORE_WIRES = []


def cw(ref, stage, net, pads, note=""):
    CORE_WIRES.append(dict(ref=ref, stage=stage, net=net, pads=pads, note=note))


cw("CG01", "ground", "GND", column("U", 1, 36), "BARE spine; solder every U pad")
cw("CG02", "ground", "GND", column("I", 20, 28), "BARE J1 ground spine; solder every pad")
for ref, pads in [
    ("CG03", ["I20", "U20"]), ("CG04", ["H34", "U34"]),
    ("CG05", ["H16", "U16"]), ("CG06", ["N14", "U14"]),
    ("CG07", ["B7", "U7"]), ("CG08", ["I1", "U1"]),
]: cw(ref, "ground", "GND", pads)

cw("CP01", "power", "+5N", column("X", 1, 36), "BARE +5N spine; solder every X pad")
for ref, pads in [
    ("CP02", ["H14", "X14"]), ("CP03", ["E4", "X4"]),
    ("CP04", ["E11", "X11"]), ("CP05", ["E13", "X13"]),
    ("CP06", ["H21", "X21"]), ("CP07", ["I33", "X33"]),
    ("CP07b", ["G1", "X1"]),
]: cw(ref, "power", "+5N", pads)
cw("CP08", "power", "+12P", ["H20", "F18"])
cw("CP09", "power", "VIN", ["G18", "H17"])

for ref, net, pads in [
    ("CS01", "SRAM_CS", ["B4", "N5"]), ("CS02", "CIPO", ["B5", "N3"]),
    ("CS03", "COPI", ["E7", "N4"]), ("CS04", "SCK", ["E6", "H3"]),
    ("CS05", "SIO2", ["B6", "B11"]), ("CS06", "HOLD", ["E5", "B13"]),
    ("CS07", "DAC_RAW", ["H23", "H6"]),
    ("CS08", "HEAD1", ["H24", "P20"]), ("CS09", "HEAD1_F", ["S20", "T20", "H8"]),
    ("CS10", "HEAD2", ["H25", "P22"]), ("CS11", "HEAD2_F", ["S22", "T22", "H9"]),
    ("CS12", "HEAD3", ["H26", "P24"]), ("CS13", "HEAD3_F", ["S24", "T24", "H10"]),
    ("CS14", "AGE", ["H27", "P26"]), ("CS15", "AGE_F", ["S26", "T26", "H11"]),
    ("CS16", "MIX", ["H28", "P28"]), ("CS17", "MIX_F", ["S28", "T28", "H12"]),
    ("CS18", "AUDIO_ADC", ["H22", "P30"]),
    ("CS19", "AUDIO_FILT", ["S30", "T30", "H7"]),
    ("CS20", "AUDIO_FILT", ["S30", "S31"]), ("CS21", "AUDIO_FILT", ["S30", "S32"]),
    ("CS22", "REC_BTN", ["H29", "N13"]), ("CS23", "PLAY_BTN", ["I29", "N12"]),
    ("CS24", "Q_OCT", ["H30", "N11"]), ("CS25", "Q_SEMI", ["I30", "N10"]),
    ("CS26", "PLAY_MODE", ["H31", "N9"]), ("CS27", "REC_CV", ["I31", "N8"]),
    ("CS28", "PLAY_CV", ["H32", "N7"]), ("CS29", "LED_R_IN", ["I32", "N6"]),
    ("CS30", "LED_G_IN", ["H33", "N16"]),
]: cw(ref, "signal", net, pads)


U1 = {
    1: ("B3", "VREF", "1OUT"), 2: ("B4", "VREF", "1-"),
    3: ("B5", "VREF_DIV", "1+"), 4: ("B6", "+12P", "V+"),
    5: ("B7", "VREF", "2+"), 6: ("B8", "AIN_SUM", "2-"),
    7: ("B9", "AUDIO_ADC", "2OUT"), 8: ("E9", "AOUT_OP", "3OUT"),
    9: ("E8", "AOUT_FB", "3-"), 10: ("E7", "AOUT_AC", "3+"),
    11: ("E6", "-12P", "V-"), 12: ("E5", "GND", "4+"),
    13: ("E4", "SPARE_LOOP", "4-"), 14: ("E3", "SPARE_LOOP", "4OUT"),
}


J2_NETS = {
    1: "+5N", 2: "GND", 3: "HEAD1", 4: "GND", 5: "HEAD2", 6: "GND",
    7: "HEAD3", 8: "GND", 9: "AGE", 10: "GND", 11: "MIX", 12: "GND",
    13: "REC_BTN", 14: "PLAY_BTN", 15: "Q_OCT", 16: "Q_SEMI",
    17: "PLAY_MODE", 18: "LED_R_OUT", 19: "LED_G_OUT", 20: "GND",
}
J2 = connector_2x(20, 10, "N", "O", J2_NETS)
J3_NETS = {1: "AUDIO_IN_TIP", 2: "GND", 3: "AUDIO_OUT_TIP", 4: "GND",
           5: "REC_TIP", 6: "GND", 7: "PLAY_TIP", 8: "GND"}
J3 = connector_2x(20, 4, "V", "W", J3_NETS)
JPWR_NETS = {1: "-12_BUS", 2: "-12_BUS", 3: "GND", 4: "GND", 5: "GND",
             6: "GND", 7: "GND", 8: "GND", 9: "+12_BUS", 10: "+12_BUS"}
JPWR = connector_2x(3, 5, "T", "U", JPWR_NETS)


INTERFACE_PARTS = [
    dict(ref="F1", value="250mA PTC", kind="R", pads=["R7", "P7"], nets=["+12_BUS", "+12_FUSED"]),
    dict(ref="D5", value="1N5817", kind="D", pads=["N7", "L7"], nets=["+12_FUSED", "+12P"], band=1),
    dict(ref="F2", value="100mA PTC", kind="R", pads=["R3", "P3"], nets=["-12_BUS", "-12_FUSED"]),
    dict(ref="D6", value="1N5817", kind="D", pads=["N3", "L3"], nets=["-12_FUSED", "-12P"], band=0),
    dict(ref="C10", value="10u", kind="EL", pads=["J7", "J9"], nets=["+12P", "GND"], plus=0),
    dict(ref="C11", value="10u", kind="EL", pads=["J3", "J5"], nets=["-12P", "GND"], plus=1),
    dict(ref="C12", value="100n", kind="C", pads=["F6", "H6"], nets=["+12P", "GND"]),
    dict(ref="C13", value="100n", kind="C", pads=["F7", "H7"], nets=["-12P", "GND"]),
    dict(ref="R9", value="10K", kind="R", pads=["G3", "I3"], nets=["+5N", "VREF_DIV"]),
    dict(ref="R10", value="10K", kind="R", pads=["I4", "I7"], nets=["VREF_DIV", "GND"]),
    dict(ref="C14", value="10u", kind="EL", pads=["K3", "K6"], nets=["VREF_DIV", "GND"], plus=0),
    dict(ref="C15", value="100n", kind="C", pads=["M3", "M5"], nets=["VREF_DIV", "GND"]),
    dict(ref="C16", value="1u film", kind="C", pads=["P10", "R10"], nets=["AUDIO_IN_TIP", "AIN_BIASED"]),
    dict(ref="R11", value="1M", kind="R", pads=["T10", "T13"], nets=["AIN_BIASED", "VREF"]),
    dict(ref="R12", value="100K", kind="R", pads=["Q10", "N10"], nets=["AIN_BIASED", "AIN_SUM"]),
    dict(ref="R13", value="39K", kind="R", pads=["L8", "N8"], nets=["AIN_SUM", "AUDIO_ADC"]),
    dict(ref="C17", value="4.7u", kind="EL", pads=["L12", "N12"], nets=["DAC_RAW", "AOUT_AC"], plus=0),
    dict(ref="R14", value="100K", kind="R", pads=["P12", "P15"], nets=["AOUT_AC", "GND"]),
    dict(ref="R15", value="10K", kind="R", pads=["J14", "L14"], nets=["AOUT_FB", "GND"]),
    dict(ref="R16", value="10K", kind="R", pads=["N14", "P14"], nets=["AOUT_FB", "AOUT_OP"]),
    dict(ref="R17", value="1K", kind="R", pads=["R16", "T16"], nets=["AOUT_OP", "AUDIO_OUT_TIP"]),
    dict(ref="R18", value="1K", kind="R", pads=["K16", "M16"], nets=["LED_R_IN", "LED_R_OUT"]),
    dict(ref="R19", value="1K", kind="R", pads=["K18", "M18"], nets=["LED_G_IN", "LED_G_OUT"]),
    dict(ref="R20", value="100K", kind="R", pads=["V26", "T26"], nets=["REC_TIP", "REC_BASE"]),
    dict(ref="R21", value="1M", kind="R", pads=["R27", "R29"], nets=["REC_BASE", "GND"]),
    dict(ref="D7", value="1N4148", kind="D", pads=["C28", "F28"], nets=["GND", "REC_BASE"], band=1),
    dict(ref="Q1", value="2N3904", kind="Q", pads=["Q26", "R26", "S26"], nets=["GND", "REC_BASE", "REC_CV"]),
    dict(ref="R22", value="10K", kind="R", pads=["U26", "X26"], nets=["REC_CV", "+5N"]),
    dict(ref="R23", value="100K", kind="R", pads=["V31", "T31"], nets=["PLAY_TIP", "PLAY_BASE"]),
    dict(ref="R24", value="1M", kind="R", pads=["R32", "R34"], nets=["PLAY_BASE", "GND"]),
    dict(ref="D8", value="1N4148", kind="D", pads=["C33", "F33"], nets=["GND", "PLAY_BASE"], band=1),
    dict(ref="Q2", value="2N3904", kind="Q", pads=["Q31", "R31", "S31"], nets=["GND", "PLAY_BASE", "PLAY_CV"]),
    dict(ref="R25", value="10K", kind="R", pads=["U31", "X31"], nets=["PLAY_CV", "+5N"]),
]


INTERFACE_WIRES = []


def iw(ref, stage, net, pads, note=""):
    INTERFACE_WIRES.append(dict(ref=ref, stage=stage, net=net, pads=pads, note=note))


iw("IG01", "ground", "GND", column("A", 1, 36), "BARE spine; solder every A pad")
iw("IG02", "ground", "GND", column("I", 20, 28), "BARE J1 ground spine")
iw("IG03", "ground", "GND", column("O", 20, 25), "BARE J2 ground spine")
for ref, pads in [
    ("IG04", ["I20", "A20"]), ("IG05", ["H34", "A34"]), ("IG06", ["O20", "A20"]),
    ("IG07", ["O29", "A29"]), ("IG08", ["W20", "A20"]), ("IG09", ["W21", "A21"]),
    ("IG10", ["W22", "A22"]), ("IG11", ["W23", "A23"]),
    ("IG12", ["T4", "A4"]), ("IG13", ["U4", "A4"]), ("IG14", ["T5", "A5"]),
    ("IG15", ["U5", "A5"]), ("IG16", ["T6", "A6"]), ("IG17", ["U6", "A6"]),
    ("IG18", ["J9", "A9"]), ("IG19", ["J5", "A5"]), ("IG20", ["I7", "A7"]),
    ("IG21", ["K6", "A6"]), ("IG22", ["M5", "A5"]), ("IG23", ["E5", "A5"]),
    ("IG24", ["N15", "A15"]), ("IG25", ["L14", "A14"]),
    ("IG26", ["Q26", "A26"]), ("IG27", ["R29", "A29"]), ("IG28", ["C28", "A28"]),
    ("IG29", ["Q31", "A31"]), ("IG30", ["R34", "A34"]), ("IG31", ["C33", "A33"]),
    ("IG32", ["H6", "A6"]), ("IG33", ["H7", "A7"]), ("IG34", ["P15", "A15"]),
]: iw(ref, "ground", "GND", pads)

iw("IP01", "power", "+5N", column("G", 1, 18), "BARE local +5N spine")
iw("IP02", "power", "+5N", column("X", 20, 36), "BARE CV +5N spine")
for ref, pads in [
    ("IP03", ["H21", "G18"]), ("IP04", ["I33", "G18"]), ("IP05", ["N20", "G18"]),
    ("IP06", ["G18", "X20"]), ("IP07", ["U7", "R7"]), ("IP08", ["P7", "N7"]),
    ("IP09", ["L7", "B6", "J7"]), ("IP10", ["L7", "H20"]),
    ("IP11", ["U3", "R3"]), ("IP12", ["P3", "N3"]), ("IP13", ["L3", "E6", "J3"]),
    ("IP14", ["I3", "I4"]), ("IP15", ["I3", "K3"]), ("IP16", ["I3", "M3"]),
]: iw(ref, "power", INTERFACE_PARTS[0]["nets"][0] if False else ("+5N" if ref in {"IP03","IP04","IP05","IP06","IP14","IP15","IP16"} else "+12_BUS"), pads)

# Correct power-net labels for the non-5V operations above.
for w, net in zip(INTERFACE_WIRES[-10:], ["+12_BUS", "+12_FUSED", "+12P", "+12P", "-12_BUS", "-12_FUSED", "-12P", "VREF_DIV", "VREF_DIV", "VREF_DIV"]):
    w["net"] = net
iw("IP17", "power", "+12_BUS", ["T7", "U7"])
iw("IP18", "power", "-12_BUS", ["T3", "U3"])
iw("IP19", "power", "+12P", ["B6", "F6"])
iw("IP20", "power", "-12P", ["E6", "F7"])

for ref, net, pads in [
    ("IS01", "VREF_DIV", ["I3", "B5"]), ("IS02", "VREF", ["B3", "B4"]),
    ("IS03", "VREF", ["B3", "B7"]), ("IS04", "VREF", ["B3", "T13"]),
    ("IS05", "AUDIO_IN_TIP", ["V20", "P10"]), ("IS05b", "AIN_BIASED", ["R10", "T10", "Q10"]),
    ("IS06", "AIN_SUM", ["N10", "B8"]),
    ("IS07", "AIN_SUM", ["B8", "L8"]), ("IS08", "AUDIO_ADC", ["N8", "B9"]),
    ("IS09", "AUDIO_ADC", ["B9", "H22"]), ("IS10", "DAC_RAW", ["H23", "L12"]),
    ("IS11", "AOUT_AC", ["N12", "P12", "E7"]), ("IS12", "AOUT_FB", ["J14", "N14"]),
    ("IS13", "AOUT_FB", ["N14", "E8"]), ("IS14", "AOUT_OP", ["P14", "E9"]),
    ("IS15", "AOUT_OP", ["E9", "R16"]), ("IS16", "AUDIO_OUT_TIP", ["T16", "V21"]),
    ("IS17", "SPARE_LOOP", ["E4", "E3"]),
    ("IS19", "HEAD1", ["N21", "H24"]), ("IS20", "HEAD2", ["N22", "H25"]),
    ("IS21", "HEAD3", ["N23", "H26"]), ("IS22", "AGE", ["N24", "H27"]),
    ("IS23", "MIX", ["N25", "H28"]), ("IS24", "REC_BTN", ["N26", "H29"]),
    ("IS25", "PLAY_BTN", ["O26", "I29"]), ("IS26", "Q_OCT", ["N27", "H30"]),
    ("IS27", "Q_SEMI", ["O27", "I30"]), ("IS28", "PLAY_MODE", ["N28", "H31"]),
    ("IS29", "LED_R_IN", ["I32", "K16"]), ("IS30", "LED_R_OUT", ["M16", "O28"]),
    ("IS31", "LED_G_IN", ["H33", "K18"]), ("IS32", "LED_G_OUT", ["M18", "N29"]),
    ("IS33", "REC_TIP", ["V22", "V26"]), ("IS34", "REC_BASE", ["T26", "R26", "R27"]),
    ("IS35", "REC_BASE", ["F28", "R26"]), ("IS36", "REC_CV", ["S26", "U26", "I31"]),
    ("IS37", "PLAY_TIP", ["V23", "V31"]), ("IS38", "PLAY_BASE", ["T31", "R31", "R32"]),
    ("IS39", "PLAY_BASE", ["F33", "R31"]), ("IS40", "PLAY_CV", ["S31", "U31", "H32"]),
]: iw(ref, "signal", net, pads)


def _validate_board(parts, pin_groups, wires, empty=()):
    expected = {}
    occupied = {}

    def assign(pad, net, owner=None):
        x, y = xy(pad)
        assert 0 <= x < len(COLS) and 0 <= y < ROWS, pad
        if owner:
            assert pad not in occupied, (pad, owner, occupied.get(pad))
            occupied[pad] = owner
        assert pad not in expected or expected[pad] == net, (pad, net, expected.get(pad))
        expected[pad] = net

    for part in parts:
        for pad, net in zip(part["pads"], part["nets"]):
            assign(pad, net, part["ref"])
    for group_name, group in pin_groups:
        for key, value in group.items():
            pad, net = value[0], value[1]
            if net == "KEY":
                continue
            assign(pad, net, f"{group_name}.{key}")
    parent = {}

    def find(p):
        parent.setdefault(p, p)
        if parent[p] != p:
            parent[p] = find(parent[p])
        return parent[p]

    for wire in wires:
        for pad in wire["pads"]:
            assign(pad, wire["net"])
        for a, b in zip(wire["pads"], wire["pads"][1:]):
            parent[find(b)] = find(a)

    groups = {}
    for pad, net in expected.items():
        if net.startswith("NC_"):
            continue
        groups.setdefault(net, set()).add(find(pad))
    disconnected = {net: roots for net, roots in groups.items() if len(roots) != 1}
    assert not disconnected, disconnected
    for pad in empty:
        assert pad not in occupied and pad not in expected, ("must stay empty", pad)
    return expected, occupied


def validate():
    core = _validate_board(
        CORE_PARTS,
        [("NANO", NANO), ("U2", SRAM), ("J1", CORE_J1)],
        CORE_WIRES,
        empty=("I34",),
    )
    interface = _validate_board(
        INTERFACE_PARTS,
        [("U1", U1), ("J1", INTERFACE_J1), ("J2", J2), ("J3", J3), ("J_PWR", JPWR)],
        INTERFACE_WIRES,
        empty=("I34",),
    )
    # Cross-board interface agreement is the central invariant.
    for pin in range(1, 31):
        assert CORE_J1[pin][1] == INTERFACE_J1[pin][1]
    return core, interface


if __name__ == "__main__":
    (cn, co), (an, ao) = validate()
    print(
        f"PASS: Core {len(co)} occupied pads/{len(CORE_WIRES)} links; "
        f"Interface {len(ao)} occupied pads/{len(INTERFACE_WIRES)} links; "
        "J1 pin map, empty key and per-net connectivity checked."
    )
