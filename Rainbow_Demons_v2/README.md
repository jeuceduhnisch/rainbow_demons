# Tape Delay 18HP All-In-One PCB and Faceplate - V2

This revision corrects the Alpha RD901F potentiometer and QingPu WQP-PJ398SM / Thonkiconn footprints, fixes the rear-mounted Daisy Patch SM pin mirroring, and removes the carrier PCB material behind the top and bottom Eurorack rails. The separate faceplate remains the full 128.5 mm Eurorack height.

Electrical notes:

- 10-pin Eurorack power is routed as pins 1-2 `-12V`, pins 3-8 `GND`, pins 9-10 `+12V`.
- The Patch SM `3V3` output on A10 feeds the five potentiometer high-side pins.
- The Patch SM `5V` output is not used by this tape-delay control board.
- Potentiometers are wired as `GND / wiper signal / 3V3`.
- Pot electrical pads are on 2.50 mm centers and mounting tabs are 9.60 mm apart, matching KiCad's official Alpha RD901F-40-00D footprint.
- RV2 is rotated 180 degrees behind the panel so its real Alpha-style pin row clears the Daisy Patch SM A5/A6 area.
- FREEZE and REVERSE are momentary switches to ground using the Wurth `430476085716` 12 x 12 mm THT footprint.
- Each LED has two LED holes plus two inline series-resistor holes; install a resistor between `R_SIG` and `R_LED_A`.
- The square/rectangular LED hole is cathode/ground.
- The square/rectangular jack hole is sleeve/ground.
- Jack pad centers are sleeve `-6.48 mm`, switch normal `-3.38 mm`, and tip `+4.92 mm` relative to the panel jack center.
- Each jack includes the manufacturer-recommended 3.0 mm NPTH beneath the barrel center.
- The populated carrier outline is 91.44 x 111.50 mm, spanning panel coordinates y=8.50 through y=120.00; there is no carrier material in either rail zone.
- The rear-mounted Patch SM footprint is mirrored before rotation so carrier A1 lands on module A1, A5 on A5, and all other named pins remain one-to-one.
- IN R is normalled from IN L through the jack switch contact.
- IN R is normalled from IN L. The OUT L and OUT R switch contacts are intentionally unconnected.

Fabrication status:

- The main PCB and faceplate were generated as KiCad 10 PCB files.
- KiCad CLI DRC on 2026-07-21 reported 0 violations and 0 unconnected items for both generated boards.
- Run KiCad DRC again before ordering after any manual edits.
- This layout uses generic 9 mm vertical pot, QingPu/Thonkiconn PJ398SM-style 3-pin jack, and 5 mm LED footprints. Verify against the exact parts you will buy before a full production order.

Files:

- `tape_delay_all_in_one_18hp_v2.kicad_pcb`: routed main PCB with corrected footprints, power mapping, and rail clearance.
- `tape_delay_faceplate_18hp_v2.kicad_pcb`: matching full-height FR4 faceplate.
- `faceplate_editable.svg`: editable faceplate art/text template.
- `tape_delay_all_in_one_wiring_map.csv`: Patch SM pin assignments.
- `main_gerbers.zip`: main PCB fabrication package, after export.
- `faceplate_gerbers.zip`: faceplate fabrication package, after export.
