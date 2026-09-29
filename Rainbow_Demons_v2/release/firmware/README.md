# Final firmware

This source/binary pair is v2.0.1, the 2026-09-29 hardware-tested release. It
preserves the v2.0.0 behavior and changes the audio block size from 16 to 2 to
move the callback cadence from an audible 3 kHz to 24 kHz.

This is independent clean-room firmware for Rainbow Demons. See the top-level
README for the independent-design disclaimer.

## Flash the supplied binary

Enter DFU mode by holding BOOT, tapping RESET and releasing BOOT, then run from
Git Bash:

```sh
make program-dfu
```

## Rebuild and flash

```sh
make clean && make && make program-dfu
```

The Makefile falls back to the known-good SDK at
`C:/Users/Jeuce/Documents/Codex/2026-07-07/i-h/work`. On another system,
override `LIBDAISY_DIR` and `DAISYSP_DIR` on the command line.

See `BUILD_MANIFEST.txt` for the accepted binary hash and behavior summary.

## Callback-noise correction

The v2.0.0 build used a 16-sample block at 48 kHz. A phone recording showed a
stable comb at approximately 3, 6, 9 and 12 kHz, matching the 3 kHz callback
rate and its harmonics. The 2-sample diagnostic removed the audible squeal and
passed Tape, Slice and Scatter stress testing on the built module. No DSP,
control-map or hardware-pin behavior changed in v2.0.1.

## REC trigger behavior

In Slice and Scatter, successive rising edges on `GATE_IN_1/B10` alternate:

1. Start a fresh capture.
2. Stop capture and begin playback.
3. Start another fresh capture.

Slice still stops automatically at four seconds and Scatter at eight seconds.
The physical Record button retains hold-to-record behavior.

## Slice automatic recording

In Slice, Feedback is an internal random-record density control. Full
counter-clockwise disables it. Turning clockwise makes capture events more
frequent and their windows shorter: roughly 1.25-3.75 seconds near the sparse
end, 0.3-0.9 seconds near noon and 0.06-0.2 seconds fully clockwise.

A physical Record press or the first REC trigger edge latches manual/external
priority and disables the generator until Reset is pressed or the mode is
changed. The gate input cannot detect a cable held at 0 V, so external priority
begins on the first received rising edge, not at physical cable insertion.
