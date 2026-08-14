# Quick start

These controls describe Rainbow Demons. See the top-level README for the
independent-design disclaimer.

## Global controls

| Control | Function |
|---|---|
| Mode toggle | Up Tape / center Slice / down Scatter |
| Direction toggle | Outer positions force forward or reverse; center is knob-controlled |
| Quantize toggle | Outer positions select semitone or octave; center is free |
| Mix | Counter-clockwise dry / clockwise wet |
| Record | Hold to capture in Slice or Scatter; release to play |
| REC CV | Rising pulses alternate: start / stop-and-play / start fresh |
| Reset | Tap to restart heads; hold 1.2 seconds to erase |

Changing Mode clears all captured audio.

For clocked recording, patch a standard positive Eurorack clock to REC CV
(0V low, +5V high recommended). Pulse width is not used; each rising edge
changes the capture state. If capture reaches four seconds in Slice or eight
seconds in Scatter, it stops automatically and the next pulse starts fresh.
RESET CV only restarts the playback heads; it does not begin a recording.

The final firmware reads the two outside toggle contacts directly. If an outer
position does not match the engraved panel word, exchange that toggle's two
outside wires; its center behavior does not change.

## Tape - pitch-shifted/reverse delay

| Knob | Function |
|---|---|
| Time | Read-head direction, speed and pitch |
| Feedback | Processed signal returned to the buffer |
| Mix | Dry/delay balance |
| Filter | Lo-fi bandwidth and brightness |
| Flutter | Stepped buffer length, about 31 ms to 8 s |

For unstable harmonized pitch spirals, raise Feedback and move Time away from unity.

## Slice - asynchronous random sampler

Hold Record for a phrase up to four seconds, then release.

| Knob | Function |
|---|---|
| Time | Slice direction, speed and pitch |
| Feedback | Auto-record density: clockwise makes captures more frequent and shorter |
| Mix | Dry/sliced-sample balance |
| Filter | Random start probability/range |
| Flutter | Slice length, grains to full phrase |

With Feedback above its CCW off zone, Slice automatically records random
windows. Sparse settings produce roughly 1.25-3.75-second captures; noon gives
about 0.3-0.9 seconds; fully clockwise gives about 0.06-0.2 seconds. Clockwise
also shortens the random wait between windows. Pressing Record or sending the
first REC CV pulse takes manual/external priority; automatic recording remains
disabled until Reset is pressed or you leave and return to Slice. Because the
digital input senses voltage rather than cable insertion, an inserted cable at
0 V is recognized only when its first rising edge arrives.

## Scatter - one to three tape heads

Hold Record for a phrase up to eight seconds, then release.

| Knob | Function |
|---|---|
| Time | Head 1 direction/speed |
| Feedback | Head 2 direction/speed |
| Filter | Head 3 direction/speed |
| Flutter | One, two or three active heads |
| Mix | Dry/multi-head loop balance |

With Direction centered, each head runs reverse left of noon, stops near noon
and runs forward right of noon. Each spans 1/8x to 8x (-3 to +3 octaves), with
approximately 1x near 1:30.

## Reliable initial test settings

- Direction and Quantize centered.
- Time and Filter at noon.
- Feedback at noon for Tape/Scatter; fully CCW for predictable manual Slice
  testing. Mode 2 no longer has a neutral noon Feedback setting.
- Flutter at 2 o'clock.
- Leave CV inputs unpatched.
- Change only Mix while checking dry/wet behavior.
