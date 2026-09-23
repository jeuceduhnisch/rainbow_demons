from pathlib import Path
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from nano_r4_integrated_looper_model import (
    COLS, ROWS, MOUNT_PADS, xy, validate, J1_NETS, J1_TOP, J1_MAIN,
    NANO, SRAM, U1, JPWR, MAIN_PARTS, MAIN_WIRES,
    TOP_TERMINALS, TOP_HARDWARE, TOP_WIRES,
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
c.setTitle("Rainbow Demons Nano R4 Looper - Integrated Protoboard Build Reference")
c.setAuthor("Rainbow Demons DIY documentation")
c.setSubject("Direct-mounted controls, single J1 and exact isolated-pad coordinates")
TOTAL = 17
page_no = 0


def txt(x, y, s, size=9, bold=False, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    {"left": c.drawString, "right": c.drawRightString, "center": c.drawCentredString}[align](x, y, str(s))


def para(x, y, s, width, size=9, leading=None, color=INK):
    style = ParagraphStyle("p", fontName="Helvetica", fontSize=size,
                           leading=leading or size * 1.28, textColor=color)
    p = Paragraph(s, style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def header(title, subtitle=""):
    txt(36, 754, "RAINBOW DEMONS / DIRECT-MOUNT PROTOBOARD", 9, True, BLUE)
    txt(36, 720, title, 20, True)
    if subtitle:
        para(36, 695, subtitle, 540, 9)
    c.setStrokeColor(LIGHT); c.line(36, 682, 576, 682)


def footer():
    txt(36, 20, "Rev 2.0 | 23 Sep 2026 | two 24 x 44 isolated-pad boards | physical build untested", 7.2, color=GRAY)
    txt(576, 20, f"{page_no} / {TOTAL}", 7.2, color=GRAY, align="right")


def end():
    global page_no
    page_no += 1
    footer(); c.showPage()


def box(x, y, w, h, title=""):
    c.setFillColor(PALE); c.setStrokeColor(LIGHT)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    if title: txt(x + 12, y + h - 20, title, 11, True)


def table(x, y, width, headers, rows, widths, rowh=20, size=7.4, wrap=False):
    assert abs(sum(widths) - width) < .1
    c.setFillColor(INK); c.rect(x, y-rowh, width, rowh, fill=1, stroke=0)
    xx = x
    for head, cw in zip(headers, widths):
        txt(xx+5, y-rowh+6, head, size, True, white); xx += cw
    yy = y-rowh
    for ri, row in enumerate(rows):
        yy -= rowh
        c.setFillColor(PALE if ri % 2 == 0 else white); c.rect(x, yy, width, rowh, fill=1, stroke=0)
        c.setStrokeColor(LIGHT); c.line(x, yy, x+width, yy)
        xx = x
        for value, cw in zip(row, widths):
            if wrap:
                para(xx+5, yy+rowh-5, str(value), cw-10, size, size*1.12)
            else:
                txt(xx+5, yy+6, value, size)
            xx += cw
    return yy


class Board:
    def __init__(self, x, y, pitch=10.0, mirrored=False):
        self.x, self.y, self.p, self.m = x, y, pitch, mirrored

    def at(self, pad):
        col, row = xy(pad)
        dc = len(COLS)-1-col if self.m else col
        return self.x + dc*self.p, self.y - row*self.p

    def grid(self, labels=True):
        p = self.p
        c.setFillColor(white); c.setStrokeColor(GRAY); c.setLineWidth(.55)
        c.rect(self.x-p*.55, self.y-(ROWS-1)*p-p*.55,
               (len(COLS)-1)*p+p*1.1, (ROWS-1)*p+p*1.1, fill=1, stroke=1)
        for col in COLS:
            xx, _ = self.at(col+"1")
            if labels: txt(xx, self.y+p*.75, col, 5.2, True, align="center")
            for row in range(1, ROWS+1):
                xx, yy = self.at(f"{col}{row}")
                c.setStrokeColor(LIGHT); c.setFillColor(white)
                c.circle(xx, yy, 1.0, fill=1, stroke=1)
        if labels:
            for row in range(1, ROWS+1):
                _, yy = self.at("A"+str(row))
                txt(self.x-p*.7, yy-1.8, f"{row:02}", 4.5, align="right")
                txt(self.x+(len(COLS)-1)*p+p*.7, yy-1.8, f"{row:02}", 4.5)
        ax, ay = self.at("A1"); c.setFillColor(RED); c.circle(ax, ay+p*.42, 2.0, fill=1, stroke=0)

    def mounts(self):
        for pad in MOUNT_PADS:
            x, y = self.at(pad)
            c.setFillColor(white); c.setStrokeColor(AMBER); c.setLineWidth(1.2)
            c.circle(x, y, 3.0, fill=1, stroke=1)
            c.line(x-2.2,y,x+2.2,y); c.line(x,y-2.2,x,y+2.2)
            txt(x, y+4.5, "M3", 4.0, True, AMBER, "center")

    def connector(self, pins, ref, color=BLUE):
        pts=[]
        for pin,(pad,net,*_) in pins.items():
            x,y=self.at(pad); pts.append((x,y)); c.setFillColor(white); c.setStrokeColor(color)
            c.rect(x-2.4,y-2.4,4.8,4.8,fill=1,stroke=1)
            txt(x,y-1.5,pin,3.5,True,color,"center")
        txt(sum(x for x,_ in pts)/len(pts), max(y for _,y in pts)+9, ref, 6.4, True, color, "center")

    def dip(self, pins, ref, label):
        pts=[self.at(v[0]) for v in pins.values()]
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        left,right=min(xs)-5,max(xs)+5; bottom,top=min(ys)-5,max(ys)+5
        c.setFillColor(HexColor("#e9eef2")); c.setStrokeColor(INK)
        c.roundRect(left,bottom,right-left,top-bottom,4,fill=1,stroke=1)
        txt((left+right)/2,(top+bottom)/2+3,ref,7,True,align="center")
        txt((left+right)/2,(top+bottom)/2-7,label,5.2,align="center")
        for key,val in pins.items():
            x,y=self.at(val[0]); c.setFillColor(white); c.circle(x,y,2,fill=1,stroke=1)
            txt(x,y-1.5,key,3.7,True,align="center")

    def nano(self):
        pts=[self.at(v[0]) for v in NANO.values()]
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        left,right=min(xs)-5,max(xs)+5; bottom,top=min(ys)-5,max(ys)+5
        c.setFillColor(HexColor("#2e8b91")); c.setStrokeColor(INK)
        c.roundRect(left,bottom,right-left,top-bottom,5,fill=1,stroke=1)
        txt((left+right)/2,(top+bottom)/2+5,"NANO R4",8,True,white,"center")
        txt((left+right)/2,(top+bottom)/2-6,"USB-C UP",5.2,False,white,"center")
        for pad,_ in NANO.values():
            x,y=self.at(pad); c.setFillColor(white); c.circle(x,y,2,fill=1,stroke=1)

    def part(self, part):
        pts=[self.at(p) for p in part["pads"]]; ref=part["ref"]; kind=part["kind"]
        c.setStrokeColor(INK); c.setLineWidth(.8); c.setFillColor(white)
        if kind=="Q":
            x=sum(p[0] for p in pts)/3; y=sum(p[1] for p in pts)/3
            c.roundRect(x-12,y+4,24,12,4,fill=1,stroke=1); txt(x,y+8,ref,5.8,True,align="center")
            for px,py in pts: c.line(px,py,px,y+4)
        elif kind=="EL":
            x=sum(p[0] for p in pts)/2; y=sum(p[1] for p in pts)/2
            c.circle(x,y,6.5,fill=1,stroke=1); txt(x,y-2,ref,5.2,True,align="center")
            txt(pts[part.get("plus",0)][0],pts[part.get("plus",0)][1]+5,"+",6,True,RED,"center")
        elif kind=="JP":
            x1,y1=pts[0];x2,y2=pts[1];c.roundRect(min(x1,x2)-4,min(y1,y2)-4,abs(x2-x1)+8,abs(y2-y1)+8,3,fill=1,stroke=1)
            txt((x1+x2)/2,(y1+y2)/2-2,ref,5.2,True,align="center")
        else:
            x1,y1=pts[0];x2,y2=pts[-1];c.line(x1,y1,x2,y2)
            mx,my=(x1+x2)/2,(y1+y2)/2;c.rect(mx-7,my-3,14,6,fill=1,stroke=1);txt(mx,my-2,ref,4.8,True,align="center")
        for x,y in pts: c.setFillColor(white);c.setStrokeColor(INK);c.circle(x,y,1.6,fill=1,stroke=1)

    def wire(self, item, color):
        c.saveState(); c.setStrokeColor(color); c.setLineWidth(2.0 if item["note"].startswith("BARE") else 1.15)
        for route in item["routes"]:
            path=c.beginPath()
            for i,pad in enumerate(route):
                x,y=self.at(pad); path.moveTo(x,y) if i==0 else path.lineTo(x,y)
            c.drawPath(path)
        for pad in item["pads"]:
            x,y=self.at(pad);c.setFillColor(color);c.circle(x,y,1.45,fill=1,stroke=0)
        c.restoreState()

    def top_hardware(self):
        for h in TOP_HARDWARE:
            x,y=self.at(f"{h['center'][0]}{h['center'][1]}")
            c.setStrokeColor(AMBER);c.setFillColor(white);c.setLineWidth(1.0)
            if h["ref"].startswith("P"):
                c.circle(x,y,5.2,fill=1,stroke=1)
                for ox in (-2.5/2.54*self.p,0,2.5/2.54*self.p): c.circle(x+ox,y+7.5/2.54*self.p,1.6,fill=1,stroke=1)
            elif h["ref"].startswith("J"):
                c.circle(x,y,3.1,fill=1,stroke=1)
                for omm in (-6.48,-3.38,4.92): c.circle(x,y-omm/2.54*self.p,1.5,fill=1,stroke=1)
            elif h["ref"].startswith("S") and not h["ref"].startswith("SW"):
                c.rect(x-6.25/2.54*self.p,y-6.0/2.54*self.p,12.5/2.54*self.p,12.0/2.54*self.p,fill=0,stroke=1)
                for ox in (-6.25,6.25):
                    for oy in (-2.5,2.5): c.circle(x+ox/2.54*self.p,y-oy/2.54*self.p,1.4,fill=1,stroke=1)
            elif h["ref"].startswith("SW"):
                c.circle(x,y,3.0,fill=1,stroke=1)
                for oy in (-2.54,0,2.54): c.circle(x,y-oy/2.54*self.p,1.4,fill=1,stroke=1)
            else:
                c.circle(x,y,2.4,fill=1,stroke=1)
            txt(x,y-2,h["ref"],4.8,True,AMBER,"center")


def two_tables(x,y,width,items,size=5.6,rowh=15):
    half=(len(items)+1)//2; gap=8; each=(width-gap)/2
    def rows(seq):
        out=[]
        for w in seq:
            ep=f"{w['pads'][0]}..{w['pads'][-1]} ALL" if w["note"].startswith("BARE") else "-".join(w["pads"])
            out.append((w["ref"],ep,w["net"]))
        return out
    # Keep enough room for the net name; the previous 9 pt final column
    # clipped nearly every label in the compact side-by-side wiring tables.
    table(x,y,each,["ID","Endpoints","Net"],rows(items[:half]),[27,52,each-79],rowh,size)
    table(x+each+gap,y,each,["ID","Endpoints","Net"],rows(items[half:]),[27,52,each-79],rowh,size)


def draw_top_components(b):
    b.grid();b.mounts();b.connector(J1_TOP,"J1");b.top_hardware()


def draw_main_components(b):
    b.grid();b.mounts();b.connector(J1_MAIN,"J1");b.connector(JPWR,"J_PWR",RED)
    b.nano();b.dip(SRAM,"U2","23LC1024");b.dip(U1,"U1","TL074")
    for part in MAIN_PARTS:b.part(part)


# 1
header("A buildable two-board reference", "Every panel control is mechanically mounted to the top protoboard. No control or jack floats on a faceplate and there is only one board-to-board connector.")
box(36,526,540,126,"Locked architecture")
para(50,623,"Use <b>two matching 24-column x 44-row isolated-pad boards</b> at 2.54mm pitch. The Top Control Board holds all five pots, both toggles, both buttons, the bicolor LED and four jacks. The Main Board holds Nano R4, SRAM, TL074, power protection, audio and CV circuits.",512,9.5)
para(50,566,"J1 is a single 1x20 stack connector at C44-V44. Four M3 standoffs at D14, T14, D43 and T43 carry mechanical load. J2 and J3 do not exist in this revision.",512,9.5)
txt(36,498,"Historically matched hardware",13,True)
rows=[("Pots","Alpha RD901F-40-00D, 9mm vertical, B10K"),("Jacks","QingPu WQP-PJ398SM / Thonkiconn style"),("Buttons","Wurth 430476085716, 12x12mm THT"),("Quantize","Tayda A-5290, SPDT ON-OFF-ON"),("Loop/Shot","A-5291-style SPDT ON-ON, same 2.54mm pin pitch"),("LED","5mm, 3-lead common-cathode red/green")]
table(36,480,540,["Hardware","Required family"],rows,[120,420],rowh=27,size=8.4)
box(36,64,540,95,"Important protoboard rule")
para(50,130,"These controls use their real historical footprints. Some holes fall between the stock 2.54mm pads. Drill those lead and locating holes using page 4, then bridge each hardware lead to the named isolated pad on page 5 with the shortest possible tinned solid link. The hardware body remains directly attached to the Top Board.",512,9.2)
end()

# 2 BOM
header("BOM tied to the coordinate layouts", "Reference designators and values match the placement and connection pages.")
counts=Counter((p["value"],p["kind"]) for p in MAIN_PARTS)
rows=[(qty,value,{"R":"resistor / PTC","C":"ceramic or film","EL":"electrolytic","D":"diode","Q":"transistor","JP":"jumper"}.get(kind,kind)) for (value,kind),qty in sorted(counts.items())]
table(36,655,300,["Qty","Value","Type"],rows,[38,116,146],rowh=18,size=7.0)
hardware=[("5","Alpha RD901F B10K","P1-P5"),("4","WQP-PJ398SM","audio/CV jacks"),("2","Wurth 430476085716","Record / Play"),("1","Tayda A-5290","Quantize"),("1","A-5291 style ON-ON","Loop / Shot"),("1","5mm bicolor common-cathode LED","status"),("1","Arduino Nano R4","socketed"),("1","23LC1024-I/P + DIP-8 socket","U2"),("1","TL074CP + DIP-14 socket","U1"),("1","1x20 stack header pair","J1"),("1","2x5 Eurorack power header","J_PWR"),("2","24x44 isolated-pad boards","minimum hole span 58.42 x 109.22mm"),("4","M3 10-12mm standoffs","board stack")]
table(324,655,252,["Qty","Hardware","Use"],hardware,[34,126,92],rowh=27,size=6.8,wrap=True)
end()

# 3 J1
header("The only inter-board connector", "J1 is one straight 1x20 header. Pin 1 is C44 on both boards and pin 20 is V44.")
rows=[(pin,J1_TOP[pin][0],net) for pin,net in J1_NETS.items()]
table(36,655,300,["Pin","Hole","Net"],rows,[42,64,194],rowh=22,size=7.8)
box(360,458,216,197,"Stacking")
para(374,620,"Fit a 1x20 female socket to the Main Board and the matching long-pin male header to the Top Board. Mark pin 1 at C44 in red on both boards before soldering.",188,8.8)
para(374,548,"Fit M3 standoffs at D14, T14, D43 and T43. The header carries signals only; the standoffs resist control and patch-cable forces.",188,8.8)
box(360,250,216,170,"No panel harness")
para(374,385,"Pots, switches, buttons, LED and jacks terminate on the Top Board. Their shared +5V and ground buses also live there. Nothing connects through loose J2/J3 wiring.",188,8.8)
para(374,304,"J_PWR remains on the Main Board so rack power never travels through the control hardware board.",188,8.8)
end()

# 4 top placement
header("Top Control Board - real hardware footprints", "Component side. Gold outlines show the actual historical hardware bodies and lead patterns; blue squares are J1.")
b=Board(178,650,9.4,False);draw_top_components(b)
box(36,57,540,78,"Direct mounting")
para(50,112,"RD901F pots are rotated 90 degrees so their 2.50mm electrical-pin row sits above each shaft. WQP-PJ398SM jacks use sleeve / switch / tip offsets -6.48 / -3.38 / +4.92mm from the shaft. Leave jack switch-normal pins unconnected. Wurth buttons use all four mechanical leads, one electrical side per net.",512,8.4)
end()

# 5 top terminals
header("Top Control Board - lead-to-pad bridges", "After drilling the exact footprints, bridge each listed hardware lead to the named isolated pad with a short rigid tinned lead.")
rows=[]
for p in TOP_TERMINALS:
    mapping="; ".join(f"{pad}={net}" for pad,net in zip(p["pads"],p["nets"]))
    rows.append((p["ref"],p["value"],mapping))
table(36,655,540,["Ref","Historical part","Named grid-pad bridge"],rows,[44,176,320],rowh=31,size=7.2,wrap=True)
box(36,83,540,85,"Orientation rules")
para(50,137,"Pot pins are +5V / wiper / GND in the order printed above; reverse the two outer connections only if the physical rotation is opposite. SW1 centre is GND and its two throws are octave/semitone. SW2 common is GND and its selected throw is PLAY_MODE. LED centre lead is common cathode GND.",512,8.5)
end()

# 6 top buses
header("Top solder pass 1 - shared +5V and ground", "Solder side, mirrored. The A-column +5V and X-column ground spines eliminate repeated harness returns.")
items=[w for w in TOP_WIRES if w["stage"] in ("ground","power")]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,GRAY if w["stage"]=="ground" else RED)
two_tables(330,650,246,items,5.1,14)
box(330,87,246,78,"Meter before J1")
para(344,141,"All pot high sides reach +5N. All pot low sides, jack sleeves, button returns, toggle commons and LED cathode reach GND. +5N and GND must remain open to each other.",218,7.5)
end()

# 7 top signals
header("Top wiring - controls and jack tips", "Solder side, mirrored. Each green route terminates at exactly one J1 signal pin.")
items=[w for w in TOP_WIRES if w["stage"]=="signal"]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,GREEN)
two_tables(330,650,246,items,5.2,15)
box(330,210,246,84,"No floating controls")
para(344,267,"Every control body is soldered or mechanically fixed to this board. The only short links are the rigid lead-to-pad bridges documented on page 5; there is no faceplate harness.",218,7.6)
end()

# 8 main placement
header("Main Board - complete component placement", "Component side. All active electronics and Eurorack power remain on this lower board.")
b=Board(178,650,9.4,False);draw_main_components(b)
box(36,57,540,78,"Orientation")
para(50,112,"Nano USB-C faces row 23. U2 notch and U1 notch face row 1. J_PWR red stripe is pins 1/2 at W1/X1. J1 pin 1 is C44. Enlarge D14/T14/D43/T43 to 3.2mm only after continuity testing the surrounding pads.",512,8.5)
end()

# 9-10 main coordinates
parts1=MAIN_PARTS[:27];parts2=MAIN_PARTS[27:]
for number,subset,title in [(9,parts1,"Main Board - exact coordinates, part 1"),(10,parts2,"Main Board - exact coordinates, part 2")]:
    header(title,"These lead holes are authoritative when labels crowd the placement drawing.")
    rows=[(p["ref"],p["value"]," / ".join(p["pads"])," / ".join(p["nets"])) for p in subset]
    table(36,655,540,["Ref","Value","Lead holes","Nets"],rows,[42,84,105,309],rowh=21,size=6.3)
    end()

# 11 main ground
header("Main solder pass 1 - ground", "Solder side, mirrored. W6-W43 is the continuous bare ground spine; all other ground links are insulated.")
items=[w for w in MAIN_WIRES if w["stage"]=="ground"]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,GRAY)
two_tables(330,650,246,items,4.8,13)
end()

# 12 main power
header("Main wiring - power and reference", "Solder side, mirrored. Check protected rails before inserting Nano, SRAM or TL074.")
items=[w for w in MAIN_WIRES if w["stage"]=="power"]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,BLUE if "-12" in w["net"] else (PURPLE if "VREF" in w["net"] else RED))
two_tables(330,650,246,items,5.0,14)
box(330,118,246,98,"Expected rails")
para(344,185,"Before ICs: +12P after F1/D5, -12P after F2/D6, and no rail-to-ground short. After Nano provides +5N, VREF and VREF_DIV should sit near 2.5V.",218,7.7)
end()

digital_nets={"SCK","CIPO","COPI","SRAM_CS","SIO2","HOLD","HEAD1","HEAD1_F","HEAD2","HEAD2_F","HEAD3","HEAD3_F","AGE","AGE_F","MIX","MIX_F","REC_BTN","PLAY_BTN","Q_OCT","Q_SEMI","PLAY_MODE","LED_R_IN","LED_R_OUT","LED_G_IN","LED_G_OUT"}
audio_nets={"VREF","AIN_BIASED","AIN_SUM","AUDIO_ADC","AUDIO_FILT","AUDIO_IN_TIP","DAC_RAW","AOUT_AC","AOUT_FB","AOUT_OP","AUDIO_OUT_TIP","SPARE_LOOP"}
cv_nets={"REC_TIP","REC_BASE","REC_CV","PLAY_TIP","PLAY_BASE","PLAY_CV"}

# 13 digital/control
header("Main solder pass 3 - SRAM and controls", "Solder side, mirrored. These are the SPI, five pot, buttons, toggles and LED routes.")
items=[w for w in MAIN_WIRES if w["stage"]=="signal" and w["net"] in digital_nets]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,GREEN)
two_tables(330,650,246,items,4.9,13)
end()

# 14 audio
header("Main wiring - audio path", "Solder side, mirrored. Purple routes carry VREF; blue routes carry audio and DAC signals.")
items=[w for w in MAIN_WIRES if w["stage"]=="signal" and w["net"] in audio_nets]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,PURPLE if "VREF" in w["net"] else BLUE)
two_tables(330,650,246,items,5.0,14)
box(330,175,246,88,"DC check")
para(344,237,"No input: U1 pin 7 and Nano A1 should rest near 2.5V. Audio-output tip should rest near 0V DC after the output coupling stage.",218,7.7)
end()

# 15 CV
header("Main solder pass 5 - Record and Play CV", "Solder side, mirrored. Two identical NPN stages turn positive Eurorack pulses into protected active-low inputs.")
items=[w for w in MAIN_WIRES if w["stage"]=="signal" and w["net"] in cv_nets]
b=Board(54,650,9.4,True);b.grid()
for w in items:b.wire(w,AMBER)
two_tables(330,650,246,items,5.2,15)
box(330,210,246,104,"Transistor check")
para(344,282,"Verify the actual 2N3904 E-B-C lead order before insertion. D7/D8 anodes reach GND and bands face the base nodes. Collectors idle HIGH through R22/R25 and pulse LOW on a valid positive trigger.",218,7.6)
end()

# 16 build/test
header("Assembly and staged power-up", "Do not insert Nano, U1 or U2 until the passive continuity and rail tests pass.")
steps=[("1","Cut two 24x44 boards. Mark A1, J1 pin 1 and all four standoff holes."),("2","Drill Top Board hardware footprints from page 4; dry-fit every exact historical part."),("3","Fit top hardware and make the short lead-to-pad bridges from page 5."),("4","Complete Top Board bus and signal passes; meter J1 pins against page 3."),("5","Fit Main Board sockets, parts and J_PWR; leave Nano/U1/U2 out."),("6","Complete Main solder passes in order and meter every rail."),("7","Power Main Board current-limited. Confirm +12P, -12P, +5N and 2.5V VREF."),("8","Fit U1, then Nano, then U2. Test each stage before stacking."),("9","Install four standoffs, align J1 C44 on both boards, then stack."),("10","Run diagnostic firmware before audio firmware.")]
table(36,655,540,["Stage","Stop point"],steps,[52,488],rowh=32,size=8.2,wrap=True)
box(36,78,540,92,"USB rule")
para(50,140,"For USB-only flashing, remove the module from the rack, open JP1 and separate J1. Never let USB back-power the unpowered TL074/audio board through signal clamps. Reconnect J1 only after USB is removed or the rack is intentionally powered under the documented test condition.",512,8.8)
end()

# 17 scale
header("Actual-size board grids and build record", "Print at 100%. Both grids below are true 2.54mm pitch; all earlier placement drawings are enlarged.")
b1=Board(64,630,7.2,False);b1.grid(False);txt(147,300,"TOP CONTROL BOARD",8,True,align="center")
b2=Board(360,630,7.2,False);b2.grid(False);txt(443,300,"MAIN BOARD",8,True,align="center")
txt(36,265,"The line below must measure exactly 50mm.",9,True)
mm=72/25.4;c.setStrokeColor(INK);c.line(70,238,70+50*mm,238);c.line(70,232,70,244);c.line(70+50*mm,232,70+50*mm,244);txt(70+25*mm,250,"50mm",7,True,align="center")
box(36,55,540,145,"Build record")
para(50,174,"Builder: ________________________   Date: ____________   Board revision: __________",512,8.6)
para(50,143,"+12P: _____V   -12P: _____V   +5N: _____V   VREF: _____V",512,8.6)
para(50,112,"Firmware file / commit: ________________________________________________",512,8.6)
para(50,81,"SRAM: PASS / FAIL   Audio: PASS / FAIL   Controls/CV: PASS / FAIL",512,8.6)
end()

c.save()
print(PDF)
