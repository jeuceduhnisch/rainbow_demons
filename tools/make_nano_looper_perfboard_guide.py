from pathlib import Path
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase.pdfmetrics import stringWidth

from nano_r4_looper_perfboard_model import (
    COLS, ROWS, MOUNT_PADS, xy, validate,
    CORE_PARTS, CORE_WIRES, CORE_J1, NANO, SRAM,
    INTERFACE_PARTS, INTERFACE_WIRES, INTERFACE_J1, U1, J2, J3, JPWR,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "Rainbow_Demons_Nano_R4_Three_Head_Looper_Build_Guide.pdf"

validate()

W, H = letter
INK = HexColor("#18232d")
GRAY = HexColor("#68747c")
LIGHT = HexColor("#dce3e8")
PALE = HexColor("#f3f6f8")
BLUE = HexColor("#225c97")
RED = HexColor("#b12c2c")
GREEN = HexColor("#236c51")
AMBER = HexColor("#a96512")
PURPLE = HexColor("#6c3d86")

c = canvas.Canvas(str(PDF), pagesize=letter)
c.setTitle("Rainbow Demons Nano R4 Looper - Exact Perfboard Build Guide")
c.setAuthor("Rainbow Demons DIY documentation")
c.setSubject("Exact 24 x 36 isolated-pad placements and connections")
TOTAL = 19
page_no = 0


def txt(x, y, s, size=9, bold=False, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    {"left": c.drawString, "right": c.drawRightString, "center": c.drawCentredString}[align](x, y, str(s))


def para(x, y, s, width, size=9, leading=None, color=INK):
    st = ParagraphStyle("p", fontName="Helvetica", fontSize=size,
                        leading=leading or size * 1.3, textColor=color)
    p = Paragraph(s, st)
    _, hh = p.wrap(width, 900)
    assert y - hh >= 30, (page_no, y, hh, s[:60])
    p.drawOn(c, x, y - hh)
    return y - hh


def box(x, y, w, h, title=None, fill=PALE):
    c.setFillColor(fill); c.setStrokeColor(LIGHT); c.setLineWidth(.7)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
    if title:
        txt(x + 12, y + h - 19, title, 11, True)


def header(title, sub):
    global page_no
    page_no += 1
    txt(36, 760, "RAINBOW DEMONS / EXACT PERFBOARD REFERENCE", 8.6, True, BLUE)
    txt(36, 731, title, 20.5, True)
    para(36, 711, sub, 540, 9.2, 12)
    c.setStrokeColor(LIGHT); c.line(36, 685, 576, 685)
    txt(36, 20, "Rev 1.1 | 23 Sep 2026 | perimeter headers | Physical build untested", 7.5, color=GRAY)
    txt(576, 20, f"{page_no} / {TOTAL}", 7.5, color=GRAY, align="right")


def end(): c.showPage()


def table(x, y, width, headers, rows, colwidths, rowh=20, size=8, wrap=False):
    assert abs(sum(colwidths) - width) < .1
    c.setFillColor(INK); c.rect(x, y-rowh, width, rowh, fill=1, stroke=0)
    xx = x
    for h, cw in zip(headers, colwidths):
        txt(xx+5, y-rowh+6, h, size, True, white); xx += cw
    y -= rowh
    for i, row in enumerate(rows):
        rh = rowh
        if wrap:
            counts = [max(1, int((stringWidth(str(v), "Helvetica", size)+cw-12)//(cw-10)))
                      for v, cw in zip(row, colwidths)]
            rh = max(rowh, max(counts) * size * 1.2 + 6)
        c.setFillColor(PALE if i % 2 == 0 else white); c.rect(x, y-rh, width, rh, fill=1, stroke=0)
        xx = x
        for val, cw in zip(row, colwidths):
            val = str(val)
            if wrap and stringWidth(val, "Helvetica", size) > cw-10:
                st = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size*1.15, textColor=INK)
                p = Paragraph(val, st); _, ph = p.wrap(cw-10, rh-3); p.drawOn(c, xx+5, y-3-ph)
            else:
                assert stringWidth(val, "Helvetica", size) <= cw-8, (page_no, val, cw)
                txt(xx+5, y-rh+(rh-size)/2+1, val, size)
            xx += cw
        c.setStrokeColor(LIGHT); c.line(x, y-rh, x+width, y-rh)
        y -= rh
    assert y >= 30, ("table low", page_no, y)
    return y


def check(x, y, s, width=530, size=8.7):
    c.setStrokeColor(INK); c.rect(x, y-1, 6, 6, fill=0, stroke=1)
    return para(x+15, y+7, s, width-15, size) - 5


class Board:
    def __init__(self, x, y, pitch=13, mirrored=False):
        self.x, self.y, self.p, self.m = x, y, pitch, mirrored

    def at(self, pad):
        col, row = xy(pad)
        dc = len(COLS)-1-col if self.m else col
        return self.x + dc*self.p, self.y - row*self.p

    def grid(self, labels=True):
        p = self.p
        c.setFillColor(white); c.setStrokeColor(GRAY); c.setLineWidth(.55)
        c.rect(self.x-p*.55, self.y-(ROWS-1)*p-p*.55, (len(COLS)-1)*p+p*1.1, (ROWS-1)*p+p*1.1, fill=1, stroke=1)
        for col in COLS:
            xx, _ = self.at(col+"1")
            if labels: txt(xx, self.y+p*.75, col, 5.4 if p < 12 else 6.5, True, align="center")
            for row in range(1, ROWS+1):
                x, y = self.at(f"{col}{row}")
                c.setStrokeColor(LIGHT); c.setFillColor(white)
                c.circle(x, y, max(1.0, p*.09), fill=1, stroke=1)
        if labels:
            for row in range(1, ROWS+1):
                _, yy = self.at("A"+str(row))
                txt(self.x-p*.72, yy-2, f"{row:02}", 4.8 if p < 12 else 5.8, align="right")
                txt(self.x+(len(COLS)-1)*p+p*.72, yy-2, f"{row:02}", 4.8 if p < 12 else 5.8)
        ax, ay = self.at("A1")
        c.setFillColor(RED); c.circle(ax, ay+p*.42, max(2, p*.15), fill=1, stroke=0)

    def part(self, part):
        pts = [self.at(p) for p in part["pads"]]
        ref, kind = part["ref"], part["kind"]
        c.setStrokeColor(INK); c.setLineWidth(.8); c.setFillColor(white)
        if kind == "Q":
            x = sum(p[0] for p in pts)/3; y = sum(p[1] for p in pts)/3
            c.roundRect(x-13, y+5, 26, 13, 5, fill=1, stroke=1)
            for px, py in pts: c.line(px, py, px, y+5)
            txt(x, y+9, ref, 6.2, True, align="center")
        elif kind == "EL":
            x = sum(p[0] for p in pts)/2; y = sum(p[1] for p in pts)/2
            c.circle(x, y, min(10, self.p*.7), fill=1, stroke=1)
            txt(x, y-2, ref, 5.8, True, align="center")
            plus = part.get("plus", 0); txt(pts[plus][0], pts[plus][1]+5, "+", 6.5, True, RED, "center")
        elif kind == "JP":
            x1,y1=pts[0]; x2,y2=pts[1]
            c.roundRect(min(x1,x2)-5, min(y1,y2)-5, abs(x2-x1)+10, abs(y2-y1)+10, 3, fill=1, stroke=1)
            txt((x1+x2)/2, (y1+y2)/2-2, ref, 5.7, True, align="center")
        else:
            x1,y1=pts[0]; x2,y2=pts[1]
            c.line(x1,y1,x2,y2)
            mx,my=(x1+x2)/2,(y1+y2)/2
            if kind in ("R","D"):
                c.saveState(); c.translate(mx,my)
                ang = 90 if abs(y2-y1)>abs(x2-x1) else 0
                if ang: c.rotate(90)
                length=max(13, min(31, ((y2-y1)**2+(x2-x1)**2)**.5*.55))
                c.rect(-length/2,-4,length,8,fill=1,stroke=1)
                if kind=="D":
                    side = 1 if part.get("band",1)==1 else -1
                    c.setLineWidth(1.8); c.line(side*(length/2-3),-4,side*(length/2-3),4)
                txt(0,-2,ref,5.4,True,align="center"); c.restoreState()
            else:
                c.rect(mx-7,my-3,14,6,fill=1,stroke=1); txt(mx,my-2,ref,5.1,True,align="center")
        for x,y in pts:
            c.setFillColor(white); c.setStrokeColor(INK); c.circle(x,y,max(1.7,self.p*.13),fill=1,stroke=1)

    def dip(self, pins, ref, label):
        pts = [self.at(v[0]) for v in pins.values()]
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        left,right=min(xs)-5,max(xs)+5; bottom,top=min(ys)-5,max(ys)+5
        c.setFillColor(HexColor("#e9eef2")); c.setStrokeColor(INK)
        c.roundRect(left,bottom,right-left,top-bottom,4,fill=1,stroke=1)
        txt((left+right)/2,(top+bottom)/2+3,ref,7,True,align="center")
        txt((left+right)/2,(top+bottom)/2-7,label,5.4,align="center")
        for key,val in pins.items():
            x,y=self.at(val[0]); c.setFillColor(white); c.circle(x,y,2,fill=1,stroke=1)
            txt(x,y-1.8,str(key),4.2,True,align="center")

    def nano(self):
        pts=[self.at(v[0]) for v in NANO.values()]
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        left,right=min(xs)-5,max(xs)+5; bottom,top=min(ys)-5,max(ys)+5
        c.setFillColor(HexColor("#2e8b91")); c.setStrokeColor(INK)
        c.roundRect(left,bottom,right-left,top-bottom,5,fill=1,stroke=1)
        txt((left+right)/2,(top+bottom)/2+5,"NANO R4",8,True,white,"center")
        txt((left+right)/2,(top+bottom)/2-6,"USB-C UP",5.5,False,white,"center")
        for name,(pad,_) in NANO.items():
            x,y=self.at(pad); c.setFillColor(white); c.circle(x,y,2.1,fill=1,stroke=1)

    def connector(self, pins, ref, color=BLUE):
        pts=[]
        for pin,(pad,net,*_) in pins.items():
            if net=="KEY": continue
            x,y=self.at(pad); pts.append((x,y)); c.setFillColor(white); c.setStrokeColor(color)
            c.rect(x-2.5,y-2.5,5,5,fill=1,stroke=1)
            txt(x,y-1.7,pin,3.7,True,color,align="center")
        if pts:
            txt(sum(x for x,_ in pts)/len(pts), max(y for _,y in pts)+10, ref, 6.5, True, color, "center")

    def mounts(self):
        for pad in MOUNT_PADS:
            x, y = self.at(pad)
            c.setFillColor(white); c.setStrokeColor(AMBER); c.setLineWidth(1.2)
            c.circle(x, y, max(3.0, self.p*.25), fill=1, stroke=1)
            c.line(x-2.4, y, x+2.4, y); c.line(x, y-2.4, x, y+2.4)
            txt(x, y+4.5, "M3", 4.2, True, AMBER, "center")

    def wire(self, item, color):
        c.saveState(); c.setStrokeColor(color); c.setLineWidth(1.25)
        if item["note"].startswith("BARE"): c.setLineWidth(2.0)
        for route in item.get("routes", [item["pads"]]):
            path=c.beginPath()
            for i,pad in enumerate(route):
                x,y=self.at(pad)
                if i==0: path.moveTo(x,y)
                else: path.lineTo(x,y)
            c.drawPath(path)
        for pad in item["pads"]:
            x,y=self.at(pad); c.setFillColor(color); c.circle(x,y,max(1.6,self.p*.11),fill=1,stroke=0)
        c.restoreState()


def draw_core_components(b):
    b.grid(); b.mounts(); b.nano(); b.dip(SRAM,"U2","23LC1024"); b.connector(CORE_J1,"J1")
    for p in CORE_PARTS: b.part(p)


def draw_interface_components(b):
    b.grid(); b.mounts(); b.dip(U1,"U1","TL074"); b.connector(INTERFACE_J1,"J1")
    b.connector(J2,"J2"); b.connector(J3,"J3"); b.connector(JPWR,"J_PWR",RED)
    for p in INTERFACE_PARTS: b.part(p)


def op_rows(items):
    return [(w["ref"], " > ".join(w["pads"]), w["note"] or w["net"]) for w in items]


def two_op_tables(x,y,width,items,size=6.5):
    half=(len(items)+1)//2; left=items[:half]; right=items[half:]
    gap=8; each=(width-gap)/2
    def endpoints(w):
        pads=w["pads"]
        if len(pads)>5 and w["note"].startswith("BARE"):
            return f"{pads[0]}..{pads[-1]} ALL"
        return "-".join(pads)
    rows1=[(w["ref"],endpoints(w)) for w in left]
    rows2=[(w["ref"],endpoints(w)) for w in right]
    table(x,y,each,["ID","Endpoints"],rows1,[34,each-34],rowh=16,size=size)
    table(x+each+gap,y,each,["ID","Endpoints"],rows2,[34,each-34],rowh=16,size=size)


# 1
header("Build from coordinates, not interpretation",
       "This replacement adds actual component holes, mirrored solder views and a numbered endpoint list for every electrical connection.")
box(36,535,540,126,"Fixed construction assumptions")
para(50,627,"Use <b>two 24-column x 36-row boards of INDIVIDUAL, ISOLATED pads at 2.54mm pitch</b>. Coordinates are A-X left-to-right and 1-36 top-to-bottom on the component side. Do not use stripboard or grouped-pad protoboard.",512,10)
para(50,571,"Core Board carries Nano R4, 23LC1024 and ADC filtering. Interface Board carries TL074, power protection, audio and CV circuits. J1 is a direct 2x15 stack connector on the right edge at W20/X20 through W34/X34 on both boards.",512,9.5)
txt(36,505,"How to read every board page",13,True)
rows=[("COMPONENT side","Letters A-X read left to right; red dot marks A1."),
      ("SOLDER side","Board is flipped left/right; letters read X-A. Row numbers never change."),
      ("Filled dots","Solder endpoints. A crossing line is insulated and does not join other pads."),
      ("BARE spine","Solder every named pad on the continuous bus."),
      ("J1 key","Remove pin 30 and permanently block socket position X34."),]
table(36,487,540,["Mark","Meaning"],rows,[115,425],rowh=24,size=8.6,wrap=True)
txt(36,318,"Build order",13,True)
rows=[("1","Mark and cut both boards; dry-fit J1 and four standoffs."),
      ("2","Place parts and sockets; do not insert ICs or Nano."),
      ("3","Complete each solder pass and tick every link ID."),
      ("4","Test boards separately, then stack with pin 1 aligned."),
      ("5","Run diagnostic firmware before the audio firmware."),]
table(36,302,540,["Stage","Stop point"],rows,[55,485],rowh=22,size=8.8)
box(36,65,540,82,"Status and hard stop")
para(50,119,"The coordinate model passes occupied-hole, per-net continuity, J1 agreement and key-position checks. The physical assembly and real-time firmware remain <b>unbench-tested</b>. Never use rack power and USB together during first bring-up; open JP1 and separate the boards for USB-only diagnostics.",512,9.2)
end()

# 2 BOM
header("Complete BOM for the coordinate layouts",
       "Values and reference numbers on this page match the placement drawings. Buy a few spare resistors, capacitors and headers.")
counts=Counter((p["value"],p["kind"]) for p in CORE_PARTS+INTERFACE_PARTS)
rows=[]
for (value,kind),qty in sorted(counts.items(),key=lambda z:(z[0][1],z[0][0])):
    rows.append((qty,value,{"R":"resistor / PTC","C":"ceramic or film","EL":"electrolytic","D":"diode","Q":"transistor","JP":"jumper"}.get(kind,kind)))
y=table(36,665,300,["Qty","Value","Type"],rows,[38,116,146],rowh=19,size=7.5)
rows2=[("1","Arduino Nano R4","Socketed on two 1x15 female headers"),
       ("1","23LC1024-I/P","PDIP-8 + socket"),("1","TL074CP","PDIP-14 + socket"),
       ("1 pair","2x15 stack headers","2.54mm; remove/key pin 30"),
       ("1","2x10 header + housing","J2 controls"),("1","2x4 header + housing","J3 jacks"),
       ("1","2x5 shrouded header","J_PWR Eurorack"),("2","24x36 isolated-pad boards","Minimum hole-center area 58.42 x 88.90mm"),
       ("4","M3 standoffs","10-12mm, plus screws/washers"),]
table(324,665,252,["Qty","Hardware","Requirement"],rows2,[40,92,120],rowh=27,size=7.1,wrap=True)
box(324,103,252,251,"Panel hardware")
para(338,323,"5 x B10K linear pots; Head 1-3 preferably center-detent.<br/><br/>1 x SPDT ON-OFF-ON quantize toggle.<br/><br/>1 x SPDT ON-ON Loop/One-shot toggle.<br/><br/>2 x normally-open momentary buttons.<br/><br/>1 x 3-lead common-cathode red/green LED.<br/><br/>4 x mono 3.5mm jacks.<br/><br/>10-to-16 Eurorack ribbon cable; red stripe at -12V.<br/><br/>24-28AWG solid insulated hookup wire; crimp contacts for J2/J3.",224,8.4)
para(36,83,"<b>Part-specific warning:</b> verify the actual 2N3904 E/B/C lead order and electrolytic polarity before insertion. Diode bands and capacitor + marks are printed on placement pages.",540,8.4)
end()

# 3 connectors/panel
header("Service boundaries and panel harness",
       "J1 replaces inter-board flying wires. J2 and J3 make the panel harness detachable and give every panel lug a named destination.")
rows=[(p,CORE_J1[p][1],"Core <-> Interface") for p in range(1,31)]
table(36,665,250,["J1","Net","Role"],rows,[30,82,138],rowh=17,size=6.8)
rows2=[(p,J2[p][1]) for p in range(1,21)]
y=table(306,665,270,["J2","Panel net"],rows2,[38,232],rowh=18,size=7.3)
rows3=[(p,J3[p][1]) for p in range(1,9)]
table(306,y-18,270,["J3","Jack net"],rows3,[38,232],rowh=16,size=7.1)
box(306,45,270,62,"Orientation")
para(320,86,"On both boards, J1 pin 1 is W20 and pin 2 is X20. Pin 29 is W34. X34 is the blocked key. Mark W20 red before soldering. J2/J3 pin 1 is the upper-left pad in the component view.",242,7.8)
end()

# 4 core placement
header("Core Board - component placement",
       "Place every part in the listed holes. Nano USB-C faces toward row 18. Socket U2 and the Nano; leave JP1 open until power checks pass.")
b=Board(142,651,14,False); draw_core_components(b)
box(36,65,540,70,"Polarity and orientation")
para(50,111,"U2 notch faces row 1. D1 band is at V30; D2 band is at S32. C9 positive lead is V35. Nano USB-C faces toward row 18. J1 pin 1 is W20; X34 stays empty. Enlarge D2/T2/D35/T35 to 3.2mm for four M3 standoffs.",512,8.6)
end()

# 5 core coordinate tables
header("Core Board - exact lead and socket coordinates",
       "These tables are authoritative when a label is crowded in the drawing. No two component leads share a hole.")
part_rows=[(p["ref"],p["value"]," / ".join(p["pads"])) for p in CORE_PARTS]
y=table(36,665,288,["Ref","Value","Lead holes"],part_rows,[36,76,176],rowh=19,size=7.4)
nano_rows=[(k,v[0],v[1]) for k,v in NANO.items()]
table(324,665,252,["Nano","Hole","Net"],nano_rows,[52,44,156],rowh=17,size=6.8)
sram_rows=[(pin,val[0],val[2],val[1]) for pin,val in SRAM.items()]
table(36,y-18,288,["U2 pin","Hole","Name","Net"],sram_rows,[40,43,55,150],rowh=17,size=6.8)
para(36,94,"J1 coordinates are printed on page 3. The five 1K/100n control filters are R3/C2 through R7/C6. R8/C7 is the audio input filter. BAT85 clamps D1/D2 protect A1.",540,8.5)
end()

# 6 core ground/power
header("Core solder pass 1 - ground and power",
       "SOLDER side: columns are mirrored. Build the U-column ground spine and V-column +5N spine before any signal links.")
b=Board(54,645,11,True); b.grid()
for w in CORE_WIRES:
    if w["stage"] in ("ground","power"): b.wire(w, GRAY if w["stage"]=="ground" else RED)
items=[w for w in CORE_WIRES if w["stage"] in ("ground","power")]
two_op_tables(330,645,246,items,6.1)
box(330,125,246,88,"Checks")
para(344,184,"CG01 and CP01 are bare spines soldered at every pad. CG02 is bare only from X20-X28. All other links are insulated. Verify U-to-V is open before fitting Nano/U2.",218,8)
end()

# 7 core signal A
header("Core solder pass 2 - SRAM and digital control",
       "SOLDER side. These links join SPI, buttons, toggles, CV logic and LED control. Crossings are insulated.")
core_a=[w for w in CORE_WIRES if w["stage"]=="signal" and (int(w["ref"][2:])<=7 or int(w["ref"][2:])>=22)]
b=Board(54,645,11,True); b.grid()
for w in core_a: b.wire(w, GREEN)
two_op_tables(330,645,246,core_a,6.0)
box(330,210,246,76,"Before continuing")
para(344,259,"Check D10/D11/D12/D13 only reach U2 pins 1/5/2/6 respectively. U2 pins 3 and 7 reach +5N through R1/R2. No SPI link may touch the ground or +5 spines at a crossing.",218,7.8)
end()

# 8 core signal B
header("Core solder pass 3 - DAC, audio and control ADCs",
       "SOLDER side. Complete CS08-CS21, then meter each J1 analog pin to its Nano destination through the specified resistor.")
core_b=[w for w in CORE_WIRES if w["stage"]=="signal" and 8<=int(w["ref"][2:])<=21]
b=Board(54,645,11,True); b.grid()
for w in core_b: b.wire(w, BLUE)
two_op_tables(330,645,246,core_b,6.0)
box(330,245,246,99,"Expected resistance")
para(344,315,"J1 pins 9/11/13/15/17 to Nano A2-A6: about 1K.<br/>J1 pin 5 to A1: about 1K.<br/>J1 pin 7 to A0: direct continuity.<br/>D1 cathode: +5N. D2 anode: GND.",218,8)
end()

# 9 interface placement
header("Interface Board - component placement",
       "Place U1, protection, audio, CV and header parts exactly as shown. J1 occupies the same coordinates as on the Core Board.")
b=Board(142,651,14,False); draw_interface_components(b)
box(36,58,540,78,"Polarity and orientation")
para(50,112,"U1 notch faces row 1. D5 band L7; D6 band N3. C10 + at J7; C11 + at J5; C14 + at K3; C17 + at L12. D7 band F28; D8 band F33. Verify Q1/Q2 E-B-C. Enlarge D2/T2/D35/T35 to 3.2mm for the matching standoffs.",512,8.3)
end()

# 10 interface parts top
header("Interface Board - exact lead coordinates, part 1",
       "Power, reference and audio parts. Coordinates refer to the component side even when you are working from a mirrored solder drawing.")
rows=[(p["ref"],p["value"]," / ".join(p["pads"])) for p in INTERFACE_PARTS[:17]]
table(36,665,540,["Ref","Value","Lead holes"],rows,[45,120,375],rowh=25,size=8)
box(36,112,540,94,"U1 TL074 socket")
para(50,176,"Pin 1 B3; 2 B4; 3 B5; 4 B6; 5 B7; 6 B8; 7 B9. Opposite row: pin 14 E3; 13 E4; 12 E5; 11 E6; 10 E7; 9 E8; 8 E9. Notch faces row 1.",512,9)
end()

# 11 interface parts bottom
header("Interface Board - exact lead coordinates, part 2",
       "Output, LED and CV-trigger parts. Transistor holes are emitter, base, collector only if your actual 2N3904 matches that lead order.")
rows=[(p["ref"],p["value"]," / ".join(p["pads"])) for p in INTERFACE_PARTS[17:]]
y=table(36,665,540,["Ref","Value","Lead holes"],rows,[45,120,375],rowh=25,size=8)
box(36,y-112,540,94,"Headers on the component side")
para(50,y-45,"J1: W20/X20 through W34/X34; X34 empty.<br/>J2: A23/B23 through A32/B32.<br/>J3: A33/B33 through A36/B36.<br/>J_PWR: A12/B12 through A16/B16; keyed notch must force red stripe to pins 1/2 at row 12.",512,9)
end()

# 12 interface ground
header("Interface solder pass 1 - ground",
       "SOLDER side. C1-C36 is the main bare ground spine; J1 and J2 each have a shorter local bare ground spine.")
ground=[w for w in INTERFACE_WIRES if w["stage"]=="ground"]
b=Board(54,645,11,True); b.grid()
for w in ground: b.wire(w, GRAY)
two_op_tables(330,645,246,ground,5.7)
box(330,79,246,68,"Continuity")
para(344,124,"Every J_PWR ground pin, every jack sleeve, U1 pin 12, J1 grounds and J2 grounds must reach C1-C36. No rail or signal may reach the C-column ground spine.",218,7.7)
end()

# 13 interface power
header("Interface solder pass 2 - rails and VREF",
       "SOLDER side. Red is +5N/+12; blue is -12; amber is the 2.5V reference divider node.")
power=[w for w in INTERFACE_WIRES if w["stage"]=="power"]
b=Board(54,645,11,True); b.grid()
for w in power:
    color=BLUE if "-12" in w["net"] else (AMBER if w["net"]=="VREF_DIV" else RED)
    b.wire(w,color)
two_op_tables(330,645,246,power,5.8)
box(330,150,246,93,"Power before ICs")
para(344,216,"With J1 disconnected: verify protected +12 at L7/J7/B6, protected -12 at L3/J3/E6, and no short to C/GND. After Nano supplies +5N through J1, VREF_DIV must be near 2.5V.",218,7.8)
end()

# 14 interface audio
header("Interface solder pass 3 - reference and audio",
       "SOLDER side. These are the U1 reference, input attenuation, DAC coupling and output-gain links.")
audio=[w for w in INTERFACE_WIRES if w["stage"]=="signal" and int(w["ref"][2:].rstrip("b"))<=17]
b=Board(54,645,11,True); b.grid()
for w in audio: b.wire(w, PURPLE if "VREF" in w["net"] else BLUE)
two_op_tables(330,645,246,audio,5.8)
box(330,190,246,92,"Signal check")
para(344,255,"No input: U1 pin 7 and J1 pin 5 should rest near 2.5V. J3 audio-output tip should rest near 0V DC after C17. U1 pin 14 is tied to pin 13; pin 12 is grounded.",218,7.8)
end()

# 15 interface controls
header("Interface solder pass 4 - controls and status LED",
       "SOLDER side. J2 signals route to J1; R18/R19 limit the red and green LED currents.")
controls=[w for w in INTERFACE_WIRES if w["stage"]=="signal" and 19<=int(w["ref"][2:].rstrip("b"))<=32]
b=Board(54,645,11,True); b.grid()
for w in controls: b.wire(w, GREEN)
two_op_tables(330,645,246,controls,5.8)
box(330,235,246,77,"Logic levels")
para(344,287,"Record, Play, quantize and mode inputs are active-low 5V logic. They must only connect to GND through their panel switches. LED outputs reach J2 only through 1K resistors.",218,7.8)
end()

# 16 interface CV
header("Interface solder pass 5 - Record and Play CV",
       "SOLDER side. Two identical NPN stages convert positive Eurorack pulses to clean active-low Nano inputs and clamp negative CV.")
cv=[w for w in INTERFACE_WIRES if w["stage"]=="signal" and int(w["ref"][2:].rstrip("b"))>=33]
b=Board(54,645,11,True); b.grid()
for w in cv: b.wire(w, AMBER)
two_op_tables(330,645,246,cv,5.8)
box(330,302,246,107,"Transistor and diode check")
para(344,378,"Q1/Q2 holes left-to-right are Q-R-S = emitter-base-collector in the component drawing. Confirm your actual 2N3904 before insertion. D7/D8 anodes reach GND; bands face the base nodes. Collector outputs idle HIGH through R22/R25.",218,7.8)
end()

# 17 panel harness and panel locations
header("Panel hardware - exact lug connections",
       "The panel harness is detachable at J2/J3. Lug names are functional; verify physical pot and jack lugs with a meter before crimping.")
rows=[("HEAD 1","CW J2.1; wiper J2.3; CCW J2.4"),("HEAD 2","CW J2.1; wiper J2.5; CCW J2.6"),
      ("HEAD 3","CW J2.1; wiper J2.7; CCW J2.8"),("AGE","CW J2.1; wiper J2.9; CCW J2.10"),
      ("MIX","CW J2.1; wiper J2.11; CCW J2.12"),("RECORD","NO contact J2.13; other contact J2.20 GND"),
      ("PLAY","NO contact J2.14; other contact J2.20 GND"),("QUANTIZE","common J2.20 GND; throws J2.15 OCT / J2.16 SEMI"),
      ("LOOP/SHOT","common J2.20 GND; one throw J2.17; other throw unused"),
      ("LED","red anode J2.18; green anode J2.19; common cathode J2.20"),]
table(36,665,330,["Part","Exact connection"],rows,[88,242],rowh=31,size=7.7,wrap=True)
rows2=[("AUDIO IN","tip J3.1; sleeve J3.2"),("AUDIO OUT","tip J3.3; sleeve J3.4"),
       ("RECORD CV","tip J3.5; sleeve J3.6"),("PLAY CV","tip J3.7; sleeve J3.8")]
table(384,665,192,["Jack","Connection"],rows2,[76,116],rowh=31,size=7.2,wrap=True)
box(384,359,192,146,"Suggested 14HP centers")
para(397,476,"Millimetres from panel upper-left:<br/><br/>H1 14,20; H2 35.4,20; H3 56.8,20.<br/>Age 22,45; Mix 49,45.<br/>Quant 18,67; Mode 45,67.<br/>Record 18,84; LED 35.4,84; Play 53,84.<br/>Jacks x 9/26/44/61 at y108.",166,7.8)
box(384,225,192,105,"Fit rule")
para(397,300,"These centers are a layout aid, not a blind drill template. Confirm bushing diameters, body clearance, rail clearance and the actual 14HP panel width before drilling.",166,7.8)
end()

# 18 tests
header("Staged power-up and functional checks",
       "Do not insert the Nano, U1 or U2 until the unpowered checks pass. Power down immediately if any voltage or temperature is wrong.")
y=653
txt(36,y,"A. Boards separated, unpowered",12,True); y-=29
for s in ["Both X34 key positions are empty/blocked; W20 is marked pin 1 on both boards.",
          "No short from +12P, -12P or +5N to GND; +12P and -12P are not shorted together.",
          "Core J1 pins 9/11/13/15/17 reach Nano A2-A6 through about 1K.",
          "Interface J_PWR pins 1/2 reach only the -12 path; pins 9/10 reach only the +12 path."]:
    y=check(36,y,s)
txt(36,y-5,"B. Interface Board alone",12,True); y-=34
for s in ["Apply current-limited rack power: +12P and -12P have correct polarity after D5/D6.",
          "Insert U1 only after rails pass. Confirm VREF output U1 pin 1 is near 2.5V when +5N is present.",
          "AUDIO_ADC rests near 2.5V; AUDIO OUT tip rests near 0V DC."]:
    y=check(36,y,s)
txt(36,y-5,"C. Stacked diagnostic",12,True); y-=34
for s in ["Fit JP1, stack J1 squarely, power from rack, and verify Nano VIN and +5N before fitting U2.",
          "Diagnostic firmware reports all pots, buttons and toggles correctly; CV inputs idle HIGH and pulse LOW.",
          "Fit U2 and pass a walking-byte test across addresses 0x00000-0x1FFFF."]:
    y=check(36,y,s)
txt(36,y-5,"D. Audio firmware",12,True); y-=34
for s in ["Mix fully CCW is dry-only; fully CW is wet-only.","All three head pots at detent give stable +1x playback.",
          "Record/overdub, Loop/One-shot, manual retrigger and both CV inputs match the firmware contract."]:
    y=check(36,y,s)
box(36,64,540,67,"USB rule")
para(50,108,"For USB-only flashing: remove the module from the rack, open JP1 and unplug J1. Do not let USB back-power the unpowered TL074 board through signal clamps.",512,9)
end()

# 19 actual scale/build record
header("Print scale, board marks and build record",
       "Only the two grids below are actual 2.54mm pitch at 100% printing. All earlier board drawings are enlarged.")
b1=Board(62,629,7.2,False); b1.grid(False)
b2=Board(344,629,7.2,True); b2.grid(False)
txt(145,353,"COMPONENT",8,True,align="center"); txt(427,353,"SOLDER",8,True,align="center")
txt(36,326,"Print at 100% / Actual size. The line below must measure exactly 50mm.",10,True)
c.setStrokeColor(INK); c.line(70,292,70+141.732,292); c.line(70,286,70,298); c.line(211.732,286,211.732,298)
txt(140.8,305,"50mm",8,True,align="center")
box(36,113,540,140,"Build record")
txt(50,224,"Builder: ________________________   Date: ____________   Board rev: __________",8.8)
txt(50,201,"+12P: _____V   -12P: _____V   +5N: _____V   VREF: _____V",8.8)
txt(50,178,"Firmware file / commit: _________________________________________________",8.8)
txt(50,155,"SRAM: PASS / FAIL   Audio: PASS / FAIL   Controls/CV: PASS / FAIL",8.8)
txt(50,130,"Notes: _______________________________________________________________",8.8)
txt(36,91,"Primary references",10,True)
para(36,79,"Arduino Nano R4: https://docs.arduino.cc/hardware/nano-r4<br/>Microchip 23LC1024 DS20005142: https://ww1.microchip.com/downloads/en/DeviceDoc/20005142C.pdf<br/>Doepfer A-100 power pinout: https://doepfer.de/a100_man/a100t_e.htm",540,7.2,9,GRAY)
end()

assert page_no == TOTAL, (page_no,TOTAL)
c.save()
print(PDF)
