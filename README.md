# Rainbow Demons

Rainbow Demons is an independently designed Daisy Patch SM Eurorack
buffer-manipulation instrument.

## Releases

- The repository root preserves the original tested working build from
  2026-08-11, including its firmware, documentation and fabrication files.
- `Rainbow_Demons_v2/` contains the corrected 18HP hardware revision.
- `Rainbow_Demons_v2/release/` contains firmware and documentation v2.0.0.
- `Rainbow_Demons_v2/Rainbow_Demons_v2.0.0.zip` is the complete packaged v2
  release.

## Version 2.0.0

Version 2 adds:

- Clock-toggle recording in Slice and Scatter: start, stop/play, start fresh.
- A Mode 2 Feedback density control that creates increasingly frequent and
  shorter randomized recording windows clockwise.
- Physical Record and REC CV priority over Mode 2 automation.
- Automatic four-second Slice and eight-second Scatter capture limits.

The v2 firmware builds successfully and was flashed successfully to the target
module on 2026-08-13. Its new recording automation awaits the final hands-on
acceptance pass; the original root release remains the known working baseline.

## Independent-design disclaimer

Rainbow Demons is inspired by broad buffer-manipulation ideas associated with
MTL ASM's Count to 5. It is not a clone, reproduction, port, or claim of exact
pedal behavior. No original source code, firmware, schematics, PCB files, or
proprietary design material were used. This project is not affiliated with or
endorsed by MTL ASM.
