# Final BOM

Quantities describe the tested mono Rainbow Demons build. The optional second output may
be added if the panel has room.

| Category | Qty | Part / value | Notes |
|---|---:|---|---|
| DSP | 1 | Electrosmith Daisy Patch SM | Main processor and Eurorack I/O conditioning |
| Main PCB | 1 | Tape-delay all-in-one Patch SM PCB | Main Gerbers included |
| Patch SM sockets | 4 | 1x10, 2.54 mm female headers | Keep the Patch SM removable |
| Power header | 1 | 2x5 keyed Eurorack header | Red stripe = -12V |
| Power cable | 1 | 10-to-16-pin Eurorack ribbon | Verify orientation at both ends |
| Pots | 5 | B10K linear | Time, Feedback, Mix, Filter, Flutter |
| Knobs | 5 | To fit pot shafts | About 10-12 mm diameter |
| Toggles | 3 | SPDT ON-OFF-ON | Mode, Direction, Quantize; common to GND |
| Buttons | 2 | SPST-NO momentary | Record and Reset |
| LEDs | 2 | 3 mm or 5 mm diffused | Record and Status |
| LED resistors | 2 | 1k, 0.25 W | One may already exist at TEMPO/B8 |
| Input pulldown | 1 | 100k, 0.25 W | Input switched contact to GND |
| Jacks | 9 | PJ398SM/PJ301M-12-style switched 3.5 mm | 5 CV, 2 trigger, mono in, mono out |
| Optional output jack | 1 | Same as above | Connect to B1 for mirrored output |
| Perfboard | 1 | 2.54 mm isolated pad-per-hole | Only if controls are not PCB-mounted |
| Hookup wire | 1 lot | 26-28 AWG stranded | Color-code power, ground, analog and digital |
| Bus wire | 1 lot | 22-24 AWG tinned solid | Ground/power buses if using perfboard |
| Heat-shrink | 1 kit | 1.5-4 mm | Insulate panel terminals and bodges |
| Standoffs/hardware | 1 set | M2.5/M3 nylon or insulated | Support carrier and perfboard independently |
| Front panel | 1 | Matching tape-delay PCB panel | Faceplate Gerbers included |

## Optional noise filtering

For long hand-wired pot leads, add one 1k resistor in series with each of the
five pot wipers and optionally 10 nF from the Patch SM side of each resistor to
GND. These are noise-control parts, not required for basic operation.
