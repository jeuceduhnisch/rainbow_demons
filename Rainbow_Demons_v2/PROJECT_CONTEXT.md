# Rainbow Demons project context

Current release: v2.0.1, 2026-09-29.

The module is built from the Tape Delay V2 carrier PCB with the documented
100k input pulldown, B9 Reset-trigger bodge and Rainbow Demons control wiring.
The current firmware uses a 2-sample audio block at 48 kHz. This replaces the
v2.0.0 16-sample setting whose 3 kHz callback cadence produced an audible
harmonic comb on the built module.

The v2.0.1 binary was compiled, flashed and hardware-tested. Tape, Slice,
Scatter, recording/playback, all three Scatter heads, controls and mode
switching passed without reported crackling or dropouts.

Do not overwrite `Rainbow_Demons_v2.0.0.zip`; it is the rollback package.
Future experiments belong in new versioned folders or branches.
