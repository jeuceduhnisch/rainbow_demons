"""Canonical two-board layout for the Nano R4 three-head looper.

Both boards use 24 x 44 isolated pads at 2.54mm pitch. Coordinates are always
component-side coordinates: A-X left-to-right and 1-44 top-to-bottom.

The TOP board mechanically carries every user control and jack. The MAIN board
carries all active electronics. J1 is the only board-to-board connector.
"""

COLS = "ABCDEFGHIJKLMNOPQRSTUVWX"
ROWS = 44
MOUNT_PADS = ("D14", "T14", "D43", "T43")


def xy(pad):
    return COLS.index(pad[0]), int(pad[1:]) - 1


def column(col, first, last):
    return [f"{col}{row}" for row in range(first, last + 1)]


J1_NETS = {
    1: "+5N", 2: "GND", 3: "HEAD1", 4: "HEAD2", 5: "HEAD3",
    6: "AGE", 7: "MIX", 8: "REC_BTN", 9: "PLAY_BTN", 10: "Q_OCT",
    11: "Q_SEMI", 12: "PLAY_MODE", 13: "LED_R_OUT", 14: "LED_G_OUT",
    15: "AUDIO_IN_TIP", 16: "AUDIO_OUT_TIP", 17: "REC_TIP",
    18: "PLAY_TIP", 19: "GND", 20: "GND",
}


def single_row(row, first_col, nets):
    start = COLS.index(first_col)
    return {pin: (f"{COLS[start + pin - 1]}{row}", nets[pin]) for pin in nets}


J1_TOP = single_row(44, "C", J1_NETS)
J1_MAIN = single_row(44, "C", J1_NETS)


NANO = {
    "D13": ("H24", "SCK"), "3V3": ("H25", "NC_3V3"),
    "AREF": ("H26", "NC_AREF"), "A0": ("H27", "DAC_RAW"),
    "A1": ("H28", "AUDIO_FILT"), "A2": ("H29", "HEAD1_F"),
    "A3": ("H30", "HEAD2_F"), "A4": ("H31", "HEAD3_F"),
    "A5": ("H32", "AGE_F"), "A6": ("H33", "MIX_F"),
    "A7": ("H34", "NC_A7"), "5V": ("H35", "+5N"),
    "BOOT": ("H36", "NC_BOOT"), "GND_L": ("H37", "GND"),
    "VIN": ("H38", "VIN"),
    "D12": ("N24", "CIPO"), "D11": ("N25", "COPI"),
    "D10": ("N26", "SRAM_CS"), "D9": ("N27", "LED_R_IN"),
    "D8": ("N28", "PLAY_CV"), "D7": ("N29", "REC_CV"),
    "D6": ("N30", "PLAY_MODE"), "D5": ("N31", "Q_SEMI"),
    "D4": ("N32", "Q_OCT"), "D3": ("N33", "PLAY_BTN"),
    "D2": ("N34", "REC_BTN"), "GND_R": ("N35", "GND"),
    "RST": ("N36", "NC_RST"), "D0": ("N37", "LED_G_IN"),
    "D1": ("N38", "NC_D1"),
}

SRAM = {
    1: ("B4", "SRAM_CS", "CS"), 2: ("B5", "CIPO", "SO"),
    3: ("B6", "SIO2", "SIO2"), 4: ("B7", "GND", "VSS"),
    5: ("E7", "COPI", "SI"), 6: ("E6", "SCK", "SCK"),
    7: ("E5", "HOLD", "HOLD"), 8: ("E4", "+5N", "VCC"),
}

U1 = {
    1: ("B16", "VREF", "1OUT"), 2: ("B17", "VREF", "1-"),
    3: ("B18", "VREF_DIV", "1+"), 4: ("B19", "+12P", "V+"),
    5: ("B20", "VREF", "2+"), 6: ("B21", "AIN_SUM", "2-"),
    7: ("B22", "AUDIO_ADC", "2OUT"), 8: ("E22", "AOUT_OP", "3OUT"),
    9: ("E21", "AOUT_FB", "3-"), 10: ("E20", "AOUT_AC", "3+"),
    11: ("E19", "-12P", "V-"), 12: ("E18", "GND", "4+"),
    13: ("E17", "SPARE_LOOP", "4-"), 14: ("E16", "SPARE_LOOP", "4OUT"),
}

JPWR_NETS = {1: "-12_BUS", 2: "-12_BUS", 3: "GND", 4: "GND",
             5: "GND", 6: "GND", 7: "GND", 8: "GND",
             9: "+12_BUS", 10: "+12_BUS"}
JPWR = {}
for index in range(5):
    row = index + 1
    JPWR[index * 2 + 1] = (f"W{row}", JPWR_NETS[index * 2 + 1])
    JPWR[index * 2 + 2] = (f"X{row}", JPWR_NETS[index * 2 + 2])


MAIN_PARTS = [
    dict(ref="R1", value="10K", kind="R", pads=["B11", "E11"], nets=["SIO2", "+5N"]),
    dict(ref="R2", value="10K", kind="R", pads=["B13", "E13"], nets=["HOLD", "+5N"]),
    dict(ref="C1", value="100n", kind="C", pads=["G1", "I1"], nets=["+5N", "GND"]),
    dict(ref="JP1", value="VIN ENABLE", kind="JP", pads=["F42", "G42"], nets=["+12P", "VIN"]),
    dict(ref="R3", value="1K", kind="R", pads=["P24", "S24"], nets=["HEAD1", "HEAD1_F"]),
    dict(ref="C2", value="100n", kind="C", pads=["T24", "U24"], nets=["HEAD1_F", "GND"]),
    dict(ref="R4", value="1K", kind="R", pads=["P26", "S26"], nets=["HEAD2", "HEAD2_F"]),
    dict(ref="C3", value="100n", kind="C", pads=["T26", "U26"], nets=["HEAD2_F", "GND"]),
    dict(ref="R5", value="1K", kind="R", pads=["P28", "S28"], nets=["HEAD3", "HEAD3_F"]),
    dict(ref="C4", value="100n", kind="C", pads=["T28", "U28"], nets=["HEAD3_F", "GND"]),
    dict(ref="R6", value="1K", kind="R", pads=["P30", "S30"], nets=["AGE", "AGE_F"]),
    dict(ref="C5", value="100n", kind="C", pads=["T30", "U30"], nets=["AGE_F", "GND"]),
    dict(ref="R7", value="1K", kind="R", pads=["P32", "S32"], nets=["MIX", "MIX_F"]),
    dict(ref="C6", value="100n", kind="C", pads=["T32", "U32"], nets=["MIX_F", "GND"]),
    dict(ref="R8", value="1K", kind="R", pads=["P34", "S34"], nets=["AUDIO_ADC", "AUDIO_FILT"]),
    dict(ref="C7", value="22n", kind="C", pads=["S35", "U35"], nets=["AUDIO_FILT", "GND"]),
    dict(ref="D1", value="BAT85", kind="D", pads=["T34", "V34"], nets=["AUDIO_FILT", "+5N"], band=1),
    dict(ref="D2", value="BAT85", kind="D", pads=["U36", "S36"], nets=["GND", "AUDIO_FILT"], band=1),
    dict(ref="C8", value="100n", kind="C", pads=["U37", "V37"], nets=["GND", "+5N"]),
    dict(ref="C9", value="10u", kind="EL", pads=["V39", "U39"], nets=["+5N", "GND"], plus=0),
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
    dict(ref="R18", value="1K", kind="R", pads=["K18", "M18"], nets=["LED_R_IN", "LED_R_OUT"]),
    dict(ref="R19", value="1K", kind="R", pads=["K20", "M20"], nets=["LED_G_IN", "LED_G_OUT"]),
    dict(ref="R20", value="100K", kind="R", pads=["A26", "D26"], nets=["REC_TIP", "REC_BASE"]),
    dict(ref="R21", value="1M", kind="R", pads=["F27", "F29"], nets=["REC_BASE", "GND"]),
    dict(ref="D7", value="1N4148", kind="D", pads=["B28", "D28"], nets=["GND", "REC_BASE"], band=1),
    dict(ref="Q1", value="2N3904", kind="Q", pads=["E26", "F26", "G26"], nets=["GND", "REC_BASE", "REC_CV"]),
    dict(ref="R22", value="10K", kind="R", pads=["F24", "G24"], nets=["REC_CV", "+5N"]),
    dict(ref="R23", value="100K", kind="R", pads=["A36", "D36"], nets=["PLAY_TIP", "PLAY_BASE"]),
    dict(ref="R24", value="1M", kind="R", pads=["F37", "F39"], nets=["PLAY_BASE", "GND"]),
    dict(ref="D8", value="1N4148", kind="D", pads=["B38", "D38"], nets=["GND", "PLAY_BASE"], band=1),
    dict(ref="Q2", value="2N3904", kind="Q", pads=["E36", "F36", "G36"], nets=["GND", "PLAY_BASE", "PLAY_CV"]),
    dict(ref="R25", value="10K", kind="R", pads=["F34", "G34"], nets=["PLAY_CV", "+5N"]),
]


TOP_TERMINALS = [
    # RD901F pots are rotated 90 degrees: electrical pins sit 7.5mm above
    # each shaft and land beside the named grid pads at 2.50mm pitch.
    dict(ref="P1", value="HEAD 1 / RD901F", kind="HW", pads=["B3", "C3", "D3"], nets=["+5N", "HEAD1", "GND"]),
    dict(ref="P2", value="HEAD 2 / RD901F", kind="HW", pads=["F3", "G3", "H3"], nets=["+5N", "HEAD2", "GND"]),
    dict(ref="P3", value="HEAD 3 / RD901F", kind="HW", pads=["K3", "L3", "M3"], nets=["+5N", "HEAD3", "GND"]),
    dict(ref="P4", value="AGE / RD901F", kind="HW", pads=["P3", "Q3", "R3"], nets=["+5N", "AGE", "GND"]),
    dict(ref="P5", value="MIX / RD901F", kind="HW", pads=["U3", "V3", "W3"], nets=["+5N", "MIX", "GND"]),
    dict(ref="SW1", value="A-5290 QUANTIZE", kind="HW", pads=["G15", "G16", "G17"], nets=["Q_OCT", "GND", "Q_SEMI"]),
    dict(ref="SW2", value="A-5291 LOOP/SHOT", kind="HW", pads=["Q15", "Q16"], nets=["PLAY_MODE", "GND"]),
    # One pin from each internally common side of the 12x12 Wurth switch.
    dict(ref="S1", value="WURTH RECORD", kind="HW", pads=["E22", "J24"], nets=["REC_BTN", "GND"]),
    dict(ref="S2", value="WURTH PLAY", kind="HW", pads=["O22", "T24"], nets=["PLAY_BTN", "GND"]),
    dict(ref="LED1", value="5MM RED/GREEN", kind="HW", pads=["K23", "L23", "M23"], nets=["LED_R_OUT", "GND", "LED_G_OUT"]),
    # PJ398SM sleeve/tip pads are 6.48mm above and 4.92mm below the shaft.
    dict(ref="JIN", value="PJ398SM AUDIO IN", kind="HW", pads=["D31", "D36"], nets=["GND", "AUDIO_IN_TIP"]),
    dict(ref="JOUT", value="PJ398SM AUDIO OUT", kind="HW", pads=["J31", "J36"], nets=["GND", "AUDIO_OUT_TIP"]),
    dict(ref="JREC", value="PJ398SM RECORD CV", kind="HW", pads=["P31", "P36"], nets=["GND", "REC_TIP"]),
    dict(ref="JPLAY", value="PJ398SM PLAY CV", kind="HW", pads=["V31", "V36"], nets=["GND", "PLAY_TIP"]),
]

TOP_HARDWARE = [
    dict(ref="P1", label="HEAD 1", part="Alpha RD901F-40-00D", center=("C", 6), drill=7.0, rotation=90),
    dict(ref="P2", label="HEAD 2", part="Alpha RD901F-40-00D", center=("G", 6), drill=7.0, rotation=90),
    dict(ref="P3", label="HEAD 3", part="Alpha RD901F-40-00D", center=("L", 6), drill=7.0, rotation=90),
    dict(ref="P4", label="AGE", part="Alpha RD901F-40-00D", center=("Q", 6), drill=7.0, rotation=90),
    dict(ref="P5", label="MIX", part="Alpha RD901F-40-00D", center=("V", 6), drill=7.0, rotation=90),
    dict(ref="SW1", label="QUANTIZE", part="Tayda A-5290 ON-OFF-ON", center=("G", 16), drill=5.0),
    dict(ref="SW2", label="LOOP/SHOT", part="A-5291-style ON-ON", center=("Q", 16), drill=5.0),
    dict(ref="S1", label="RECORD", part="Wurth 430476085716", center=("G", 23), drill=0.0),
    dict(ref="LED1", label="LED", part="5mm common-cathode red/green", center=("L", 23), drill=5.0),
    dict(ref="S2", label="PLAY", part="Wurth 430476085716", center=("Q", 23), drill=0.0),
    dict(ref="JIN", label="AUDIO IN", part="QingPu WQP-PJ398SM", center=("D", 34), drill=3.0),
    dict(ref="JOUT", label="AUDIO OUT", part="QingPu WQP-PJ398SM", center=("J", 34), drill=3.0),
    dict(ref="JREC", label="RECORD CV", part="QingPu WQP-PJ398SM", center=("P", 34), drill=3.0),
    dict(ref="JPLAY", label="PLAY CV", part="QingPu WQP-PJ398SM", center=("V", 34), drill=3.0),
]


def _pin_items(groups):
    out = []
    for group_name, group in groups:
        for key, value in group.items():
            if value[1].startswith("NC_"):
                continue
            out.append((f"{group_name}.{key}", value[0], value[1]))
    return out


def _part_items(parts):
    out = []
    for part in parts:
        for index, (pad, net) in enumerate(zip(part["pads"], part["nets"]), 1):
            out.append((f"{part['ref']}.{index}", pad, net))
    return out


def _routes(pads):
    source = pads[0]
    sx, sy = xy(source)
    routes = []
    for destination in pads[1:]:
        dx, dy = xy(destination)
        if sx == dx or sy == dy:
            routes.append([source, destination])
        else:
            routes.append([source, f"{COLS[dx]}{sy + 1}", destination])
    return routes


def build_wires(parts, groups, ground_col, power_col, prefix):
    endpoints = {}
    for owner, pad, net in _part_items(parts) + _pin_items(groups):
        endpoints.setdefault(net, []).append((owner, pad))
    wires = []
    serial = 1
    for net in sorted(endpoints):
        if net.startswith("NC_"):
            continue
        pads = []
        for _, pad in endpoints[net]:
            if pad not in pads:
                pads.append(pad)
        stage = "ground" if net == "GND" else ("power" if net in {"+5N", "+12_BUS", "-12_BUS", "+12_FUSED", "-12_FUSED", "+12P", "-12P", "VIN", "VREF_DIV", "VREF"} else "signal")
        if net in {"GND", "+5N"}:
            col = ground_col if net == "GND" else power_col
            bus = column(col, 6, 43)
            wires.append(dict(ref=f"{prefix}{serial:03}", stage=stage, net=net,
                              pads=bus, routes=[bus], note=f"BARE {net} spine; solder every {col}6-{col}43 pad"))
            serial += 1
            for pad in pads:
                if pad in bus:
                    continue
                row = max(6, min(int(pad[1:]), 43))
                destination = f"{col}{row}"
                link = [pad, destination]
                wires.append(dict(ref=f"{prefix}{serial:03}", stage=stage, net=net,
                                  pads=link, routes=_routes(link), note=""))
                serial += 1
        elif len(pads) > 1:
            wire = dict(ref=f"{prefix}{serial:03}", stage=stage, net=net,
                        pads=pads, routes=_routes(pads), note="")
            wires.append(wire)
            serial += 1
    return wires


TOP_WIRES = build_wires(TOP_TERMINALS, [("J1", J1_TOP)], "X", "A", "T")
MAIN_WIRES = build_wires(
    MAIN_PARTS,
    [("NANO", NANO), ("SRAM", SRAM), ("U1", U1), ("J_PWR", JPWR), ("J1", J1_MAIN)],
    "W", "V", "M",
)


def _validate_board(parts, groups, wires, reserved=()):
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
        for index, (pad, net) in enumerate(zip(part["pads"], part["nets"]), 1):
            assign(pad, net, f"{part['ref']}.{index}")
    for group_name, group in groups:
        for key, value in group.items():
            if value[1].startswith("NC_"):
                continue
            assign(value[0], value[1], f"{group_name}.{key}")

    parent = {}
    def find(pad):
        parent.setdefault(pad, pad)
        if parent[pad] != pad:
            parent[pad] = find(parent[pad])
        return parent[pad]

    for wire in wires:
        for pad in wire["pads"]:
            assign(pad, wire["net"])
        for a, b in zip(wire["pads"], wire["pads"][1:]):
            parent[find(b)] = find(a)

    groups_by_net = {}
    for pad, net in expected.items():
        if net.startswith("NC_"):
            continue
        groups_by_net.setdefault(net, set()).add(find(pad))
    disconnected = {net: roots for net, roots in groups_by_net.items() if len(roots) != 1}
    assert not disconnected, disconnected
    for pad in reserved:
        assert pad not in occupied and pad not in expected, ("reserved hole used", pad)
    return expected, occupied


def validate():
    top = _validate_board(TOP_TERMINALS, [("J1", J1_TOP)], TOP_WIRES, MOUNT_PADS)
    main = _validate_board(
        MAIN_PARTS,
        [("NANO", NANO), ("SRAM", SRAM), ("U1", U1), ("J_PWR", JPWR), ("J1", J1_MAIN)],
        MAIN_WIRES,
        MOUNT_PADS,
    )
    for pin in J1_NETS:
        assert J1_TOP[pin][1] == J1_MAIN[pin][1]
    return top, main


if __name__ == "__main__":
    (tn, to), (mn, mo) = validate()
    print(f"PASS: top {len(to)} occupied pads/{len(TOP_WIRES)} links; "
          f"main {len(mo)} occupied pads/{len(MAIN_WIRES)} links; "
          "J1 agreement, connectivity and reserved standoff holes checked.")
