from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, KeepTogether
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Rainbow_Demons_v2" / "release" / "Rainbow_Demons_Build_Documentation.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#17243A")
BLUE = colors.HexColor("#2E6F9E")
PALE = colors.HexColor("#EAF2F7")
INK = colors.HexColor("#20252B")
MUTED = colors.HexColor("#59636E")
RED = colors.HexColor("#A53D35")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=28,
                          leading=31, textColor=NAVY, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontSize=12, leading=16,
                          textColor=MUTED, alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17,
                          leading=20, textColor=NAVY, spaceBefore=2, spaceAfter=9))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
                          leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.7,
                          leading=11.4, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.6,
                          leading=9.5, textColor=INK))
styles.add(ParagraphStyle(name="Tinyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=6.8,
                          leading=8.2, textColor=INK))
styles.add(ParagraphStyle(name="TableHeader", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=6.8,
                          leading=8.2, textColor=colors.white))
styles.add(ParagraphStyle(name="Warn", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.5,
                          leading=11, textColor=RED, borderColor=colors.HexColor("#E7C6C2"),
                          borderWidth=0.6, borderPadding=7, backColor=colors.HexColor("#FFF5F3"), spaceAfter=8))


def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def bullets(items):
    return [p(f"<b>-</b> {item}") for item in items]


def table(rows, widths, header=True, tiny=False):
    cooked = []
    sty = "Tinyx" if tiny else "Smallx"
    for row_index, row in enumerate(rows):
        cell_style = "TableHeader" if header and row_index == 0 else sty
        cooked.append([cell if hasattr(cell, "wrap") else p(str(cell), cell_style) for cell in row])
    t = Table(cooked, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#BFC8D0")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, colors.HexColor("#F6F8FA")]),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(commands))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D6DCE1"))
    canvas.line(0.62 * inch, 0.48 * inch, 7.88 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.62 * inch, 0.31 * inch, "Rainbow Demons v2.0.0 - independent Patch SM instrument - 2026-08-13")
    canvas.drawString(6.95 * inch, 0.31 * inch, f"Page {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=letter, rightMargin=0.62*inch, leftMargin=0.62*inch,
                      topMargin=0.55*inch, bottomMargin=0.62*inch, title="Rainbow Demons Build Documentation")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates(PageTemplate(id="all", frames=frame, onPage=footer))

story = []

# Page 1
story += [Spacer(1, 0.38*inch), p("Rainbow Demons", "Cover"),
          p("An original, independently designed Eurorack instrument", "Subtitle")]
story.append(table([
    ["Release", "Platform", "Format", "Firmware status"],
    ["v2.0.0 / 2026-08-13", "Daisy Patch SM", "Tape-delay PCB / mono", "Built from verified baseline"],
], [1.2*inch, 1.55*inch, 1.2*inch, 2.4*inch]))
story += [Spacer(1, 12), p("What this package contains", "H1x")]
story += bullets([
    "Final source, Makefile, startup file and successfully compiled flashable binary.",
    "Tape-delay main PCB and faceplate Gerbers plus editable PCB source.",
    "Required PCB modifications, BOM, build sequence, acceptance test and quick-start control map.",
])
story += [p("Critical proven modifications", "H1x"), p(
    "Add <b>100k from the audio-input switched contact to GND</b>. Move the repurposed Reset-trigger tip "
    "from B6 to <b>B9/GATE_IN_2</b>. Record is <b>D1</b>, Reset is <b>D2</b>, Record LED is B8 and Status LED is B7. "
    "Feedback uses <b>CV_7/C8</b>. Do not restore obsolete ADC_12, D7/D10-button or B5/B6-LED assignments.", "Warn")]
story += [p("Release behavior", "H2x")]
story += bullets([
    "Mix is counter-clockwise dry and clockwise wet with exact digital endpoints.",
    "Tape provides lo-fi pitch/reverse delay and high-feedback pitch spirals.",
    "Slice captures up to 4 seconds; Scatter captures up to 8 seconds.",
    "Scatter heads span 1/8x to 8x (-3 to +3 octaves) and stop near noon.",
    "REC CV clock edges alternate start / stop-and-play / start-new capture.",
    "Slice Feedback controls auto-record density; clockwise makes windows more frequent and shorter.",
    "Changing Mode clears and invalidates the previous capture.",
])
story += [Spacer(1, 6), p("Independent-design disclaimer", "H2x"), p(
    "Rainbow Demons is inspired by broad buffer-manipulation ideas associated with MTL ASM's Count to 5. "
    "It is not a clone, reproduction, port, or claim of exact pedal behavior. No original source code, "
    "firmware, schematics, PCB files, or proprietary design material were used. This project is not "
    "affiliated with or endorsed by MTL ASM.", "Warn"), PageBreak()]

# Page 2
story += [p("1. Required tape-delay PCB changes", "H1x")]
mods = [
    ["Change", "Final connection", "Reason"],
    ["Input pulldown", "100k: input switched/normal contact to GND", "Stops floating open input"],
    ["Reset trigger", "Isolate original B6 trace; jack tip to B9", "B6 is an output; B9 is GATE_IN_2"],
    ["Record trigger", "Jack tip to B10", "Clock edges toggle start / stop capture"],
    ["Buttons", "Record D1; Reset D2; other side GND", "Matches final panel/firmware"],
    ["Mode toggle", "Outer lugs D7/D10; common GND", "Tape / Slice / Scatter"],
    ["Direction", "Outer lugs D3/D4; common GND", "Reverse / variable / forward"],
    ["Quantize", "Outer lugs D5/D6; common GND", "Semitone / free / octave"],
    ["LEDs", "B8 Record; B7 Status; each through 1k", "Plain GPIO indicators"],
]
story.append(table(mods, [1.15*inch, 3.0*inch, 2.9*inch], tiny=True))
story += [p("Final signal map", "H2x")]
signals = [
    ["Function", "Pin", "Function", "Pin"],
    ["Time pot", "A2 / ADC_9", "CV1 Time", "C5 / CV_1"],
    ["Feedback pot", "C8 / CV_7", "CV2 Filter", "C4 / CV_2"],
    ["Mix pot", "C9 / CV_8", "CV3 Flutter", "C3 / CV_3"],
    ["Filter pot", "A3 / ADC_10", "CV4 Feedback", "C2 / CV_4"],
    ["Flutter pot", "D9 / ADC_11", "CV5", "C6 / disabled"],
    ["Mono input", "B4", "Main output", "B2"],
    ["Optional output", "B1", "Ground", "Jack sleeves / commons"],
]
story.append(table(signals, [1.45*inch, 1.4*inch, 1.55*inch, 1.4*inch], tiny=True))
story += [p("Leave disconnected", "H2x")]
story += bullets([
    "B6 from the repurposed Reset trigger jack; B5 FREEZE LED; audio-input-right in the mono build.",
    "CV5-to-Mix modulation. The final firmware disables it to preserve exact Mix endpoints.",
])
story += [p("Unpowered checks", "H2x")]
story += bullets([
    "No shorts among +12V, -12V, 5V, 3V3 and GND; red stripe reaches marked -12V.",
    "Input normal contact measures about 100k to GND; Reset tip reaches B9 and not B6.",
    "Toggle commons and jack sleeves reach GND; LEDs have correct polarity and series resistors.",
])
story.append(PageBreak())

# Page 3
story += [p("2. Bill of materials", "H1x")]
bom = [
    ["Qty", "Part", "Specification / note"],
    ["1", "Daisy Patch SM", "DSP and conditioned Eurorack I/O"],
    ["1", "Tape-delay main PCB", "Main Gerbers included"],
    ["4", "Patch SM sockets", "1x10, 2.54 mm female headers"],
    ["1", "Power header + cable", "2x5 keyed; 10-to-16-pin ribbon; red stripe -12V"],
    ["5", "Potentiometers + knobs", "B10K linear; Time, Feedback, Mix, Filter, Flutter"],
    ["3", "Toggles", "SPDT ON-OFF-ON, panel mount"],
    ["2", "Buttons", "SPST-NO momentary, Record and Reset"],
    ["2", "LEDs + 1k resistors", "Diffused 3 or 5 mm; Record and Status"],
    ["1", "100k resistor", "0.25 W input switched-contact pulldown"],
    ["9", "Switched 3.5 mm jacks", "5 CV, 2 trigger, mono input, mono output"],
    ["1 opt.", "Second output jack", "Tip to B1 for mirrored output"],
    ["1", "Perfboard", "2.54 mm isolated pad-per-hole if controls are hand-wired"],
    ["1 lot", "Wire / heat-shrink", "26-28 AWG stranded; 22-24 AWG tinned bus wire"],
    ["1 set", "Insulated hardware", "M2.5/M3 standoffs, washers, rack screws"],
    ["1", "Front panel", "Matching faceplate Gerbers included"],
]
story.append(table(bom, [0.55*inch, 2.05*inch, 4.5*inch], tiny=True))
story += [p("Optional hand-wiring filter", "H2x"), p(
    "For long pot leads, add 1k in series with each of five wipers and optionally 10 nF from the Patch SM side "
    "of each resistor to GND. These parts reduce pickup; they are not required for basic operation.")]
story += [p("Mechanical rules", "H2x")]
story += bullets([
    "Dry-fit every control, carrier and perfboard before soldering; preserve rail and USB/BOOT clearance.",
    "Support carrier and perfboard with insulated hardware. Never let perfboard copper rest on the carrier.",
    "Verify exact pot shaft/bushing, toggle action and jack footprint against purchased parts.",
])
story.append(PageBreak())

# Page 4
story += [p("3. Assembly, flashing and checkout", "H1x")]
steps = [
    ("1", "Mechanical dry fit", "Fit panel controls, carrier and brackets. Confirm rail and USB/BOOT access."),
    ("2", "Power", "Install keyed header with red stripe at -12V. Do not feed external 5V/3V3 into Patch SM outputs."),
    ("3", "Analog wiring", "Wire pots/CVs per page 2. Ground sleeves. Add the 100k input pulldown."),
    ("4", "Audio/triggers", "Input B4; output B2; Record trigger B10; isolate B6 and bodge Reset trigger to B9."),
    ("5", "Digital wiring", "Record D1, Reset D2, toggles D3/D4/D5/D6/D7/D10, LEDs B8/B7."),
    ("6", "Inspect", "Meter rails, grounds, pulldown, B9 bodge, LED polarity and adjacent-header shorts."),
]
story.append(table([["Step", "Task", "Action"]] + [list(x) for x in steps], [0.48*inch, 1.35*inch, 5.25*inch], tiny=True))
story += [p("Flash", "H2x"), p("Enter DFU: hold BOOT, tap RESET, release BOOT. In Git Bash inside the firmware folder:")]
story.append(table([["Use", "Command"], ["Flash supplied build", "make program-dfu"],
                    ["Clean rebuild + flash", "make clean && make && make program-dfu"]],
                   [1.7*inch, 5.35*inch], tiny=True))
story += [p("Acceptance test", "H2x")]
story += bullets([
    "Power from a test/current-limited supply; stop if anything heats or current is abnormal.",
    "Mix fully counter-clockwise: clean dry audio. Fully clockwise: wet only, no direct leakage.",
    "Slice: hold Record, capture a phrase, release and hear playback.",
    "Scatter: capture, raise Flutter for three heads; Time/Feedback/Filter reverse left, stop near noon, forward right.",
    "REC CV: pulse 1 starts, pulse 2 stops/plays, pulse 3 starts a fresh capture.",
    "Slice Feedback: CCW disables auto-record; clockwise makes random windows more frequent and shorter. Record or REC CV takes priority.",
    "Change Mode and return. The old phrase must not resume.",
])
story += [p("Binary identity", "H2x"), p(
    "RainbowDemons.bin - final binary identity is listed in BUILD_MANIFEST.txt.<br/>"
    "Size: 88,252 bytes<br/><font size='7'>B5329B1F9805EFE256EF1C30324392757952D0C81F3856A0632B72B872BF06DA</font>")]
story.append(PageBreak())

# Page 5
story += [p("4. Quick start", "H1x")]
story.append(table([
    ["Global control", "Action"],
    ["Mode", "Up Tape / center Slice / down Scatter"],
    ["Direction", "Outer positions force direction; center lets DIR knobs cross reverse-stop-forward"],
    ["Quantize", "Outer positions select semitone/octave; center is free"],
    ["Mix", "Counter-clockwise dry / clockwise wet"],
    ["Record", "Hold to capture in Slice/Scatter; release to play"],
    ["REC CV", "Rising edges alternate start / stop-and-play / start fresh"],
    ["Reset", "Tap restarts heads; hold 1.2 seconds erases"],
], [1.55*inch, 5.5*inch], tiny=True))
story += [p("If an outer toggle label is reversed, exchange only that toggle's two outside wires.", "Warn")]
mode_rows = [
    ["Knob", "Tape", "Slice", "Scatter"],
    ["Time", "Read-head speed/direction", "Slice speed/direction", "Head 1 speed/direction"],
    ["Feedback", "Feedback amount", "Auto-record density", "Head 2 speed/direction"],
    ["Mix", "Dry/delay", "Dry/slices", "Dry/multi-head loop"],
    ["Filter", "Lo-fi tone/bandwidth", "Random start probability", "Head 3 speed/direction"],
    ["Flutter", "Stepped 31 ms-8 s length", "Grain/full-phrase length", "1, 2 or 3 heads"],
]
story += [p("Mode control map", "H2x"), table(mode_rows, [1.0*inch, 2.0*inch, 2.0*inch, 2.0*inch], tiny=True)]
story += [p("Mode notes", "H2x")]
story += bullets([
    "REC CV accepts a positive Eurorack clock (0V low, +5V high recommended); pulse width is ignored.",
    "If a capture reaches its 4/8-second limit, it stops automatically and the next pulse starts fresh.",
    "Tape: high Feedback plus Time away from unity creates cascading, unstable harmonized pitch spirals.",
    "Slice: capture is up to 4 seconds; Filter raises random slice jumps; Flutter changes slice length.",
    "Slice density windows: sparse 1.25-3.75 s, noon 0.3-0.9 s, dense 0.06-0.2 s. Record or REC CV disables automation until Reset/mode change.",
    "The REC input senses voltage, not cable insertion; a patched 0 V cable takes priority when its first rising edge arrives.",
    "Scatter: capture is up to 8 seconds; each head spans 1/8x-8x (-3 to +3 octaves), about 1x near 1:30.",
    "Changing Mode always clears captured audio.",
])
story += [p("Repeatable test setup", "H2x")]
story += bullets([
    "Direction/Quantize centered; Time and Filter noon; Flutter 2 o'clock. Use Feedback noon in Tape/Scatter, fully CCW for manual Slice tests.",
    "Leave CV inputs unpatched and change only Mix while verifying dry/wet behavior.",
])
story.append(PageBreak())

# Page 6
story += [p("5. Release files and fabrication notes", "H1x")]
files = [
    ["Folder", "Contents", "Use"],
    ["Top level", "Build guide, modifications, BOM, quick start, PDF", "Workshop reference"],
    ["firmware/", "Source, Makefile, startup, binary, manifest", "Rebuild or flash final firmware"],
    ["pcb/", "Main/faceplate Gerbers, source, base map", "Fabrication files; apply page 2 bodges"],
]
story.append(table(files, [1.8*inch, 3.05*inch, 2.2*inch], tiny=True))
story += [p("Gerber warning", "H2x"), p(
    "The included tape-delay PCB Gerbers reproduce the supplied V2 carrier layout. They do not include the "
    "100k input pulldown, B9 Reset-trigger bodge or final Rainbow Demons toggle wiring as copper revisions. "
    "Apply those changes manually, or update the KiCad source and rerun DRC before ordering a native revision.", "Warn")]
story += [p("Firmware build environment", "H2x")]
story += bullets([
    "Target Daisy Patch SM / STM32H750; internal flash address 0x08000000.",
    "The included Makefile checks libDaisy, CMSIS and DaisySP before compiling.",
    "On another computer, override LIBDAISY_DIR and DAISYSP_DIR rather than hard-editing source paths.",
])
story += [p("Final preservation checklist", "H2x")]
story += bullets([
    "Keep the release ZIP unchanged as the versioned 2026-08-13 baseline.",
    "Make experimental firmware in a new folder; do not overwrite this binary/source pair.",
    "Photograph the B9 bodge, 100k pulldown, red-stripe orientation and Patch SM orientation for the build record.",
    "If controls are replaced, confirm pot polarity and exchange toggle outer wires as needed.",
])
story += [Spacer(1, 18), p("Version 2.0.0 - release generated 2026-08-13", "Subtitle")]

doc.build(story)
print(OUT)
