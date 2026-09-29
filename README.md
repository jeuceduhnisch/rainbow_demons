# Rainbow Demons

Rainbow Demons is an independently designed Daisy Patch SM Eurorack
buffer-manipulation instrument.

## Releases

- The repository root preserves the original tested working build from
  2026-08-11, including its firmware, documentation and fabrication files.
- `Rainbow_Demons_v2/` contains the corrected 18HP hardware revision.
- `Rainbow_Demons_v2/release/` contains firmware and documentation v2.0.1.
- `Rainbow_Demons_v2/Rainbow_Demons_v2.0.1.zip` is the current complete release.
- `Rainbow_Demons_v2/Rainbow_Demons_v2.0.0.zip` remains the immutable rollback
  package.

## Version 2.0.1

Version 2 adds:

- Clock-toggle recording in Slice and Scatter: start, stop/play, start fresh.
- A Mode 2 Feedback density control that creates increasingly frequent and
  shorter randomized recording windows clockwise.
- Physical Record and REC CV priority over Mode 2 automation.
- Automatic four-second Slice and eight-second Scatter capture limits.
- A hardware-tested audio block-size correction that moves the callback cadence
  from an audible 3 kHz to 24 kHz and removes the high-pitched harmonic comb.

The v2.0.1 firmware was built, flashed, and tested on the target module on
2026-09-29. Tape, Slice, Scatter, recording, playback, three-head operation,
controls and mode switching passed without reported crackling or dropouts.

## Independent-design disclaimer

Rainbow Demons is inspired by broad buffer-manipulation ideas associated with
MTL ASM's Count to 5. It is not a clone, reproduction, port, or claim of exact
pedal behavior. No original source code, firmware, schematics, PCB files, or
proprietary design material were used. This project is not affiliated with or
endorsed by MTL ASM.

## License

This project is released under the Unlicense. See [LICENSE](LICENSE).

## Acknowledgments

Documentation, cleanup, and release organization were assisted by OpenAI Codex.
