# Rainbow Demons

Rainbow Demons is an independently designed Daisy Patch SM Eurorack
buffer-manipulation instrument. This repository intentionally contains only
the curated release; legacy experiments, recordings and generated diagnostics
are excluded by `.gitignore`.

## Current release

Version `2.0.0` adds:

- Clock-toggle recording in Slice and Scatter: start, stop/play, start fresh.
- A Mode 2 Feedback density control that creates increasingly frequent and
  shorter randomized recording windows clockwise.
- Physical Record and REC CV priority over Mode 2 automation.
- Automatic four-second Slice and eight-second Scatter capture limits.

Start with `outputs/RAINBOW_DEMONS_WORKING_RELEASE/README.md`. The packaged
release is `outputs/RAINBOW_DEMONS_v2.0.0.zip`.

## Status

The v2 firmware builds successfully and was flashed successfully to the target
module on 2026-08-13. The established audio, mix and multi-head behavior comes
from the working hardware baseline; the new v2 recording automation awaits
the final hands-on acceptance pass.
