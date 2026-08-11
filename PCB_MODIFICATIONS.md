# Required modifications to the reused tape-delay PCB

These modifications convert the included tape-delay PCB wiring for Rainbow
Demons. See the top-level README for the independent-design disclaimer.

These changes match the final working firmware. Perform continuity checks with
the module unpowered.

## Required

1. **Audio-input pulldown:** add a 100k resistor from the audio input jack's
   switched/normal contact to GND. This prevents an open input from floating.
2. **Reset trigger:** the original CLOCK OUT tip runs to `B6/GATE_OUT_2`, which
   is an output. Isolate or ignore that trace and wire the jack tip to
   `B9/GATE_IN_2`. Keep the sleeve at GND.
3. **Record trigger:** retain the CLOCK IN connection to `B10/GATE_IN_1`.
4. **Buttons:** Record goes to `D1`; Reset goes to `D2`. Each button shorts its
   pin to GND when pressed.
5. **Mode toggle:** SPDT ON-OFF-ON, common to GND, outer lugs to `D7` and `D10`.
6. **Direction toggle:** common to GND, outer lugs to `D3` and `D4`.
7. **Quantize toggle:** common to GND, outer lugs to `D5` and `D6`.
8. **LEDs:** Record LED is driven from `B8`; Status LED from `B7`. Each LED
   requires a series resistor. The existing TEMPO/B8 position normally already
   has one; add 1k at B7 if the reused footprint has none.

## Final analog connections

| Panel control | Patch SM pin |
|---|---|
| Time pot | `A2 / ADC_9` |
| Feedback pot | `C8 / CV_7` |
| Mix pot | `C9 / CV_8` |
| Filter pot | `A3 / ADC_10` |
| Flutter pot | `D9 / ADC_11` |
| CV1 Time | `C5 / CV_1` |
| CV2 Filter | `C4 / CV_2` |
| CV3 Flutter | `C3 / CV_3` |
| CV4 Feedback | `C2 / CV_4` |
| CV5 | `C6 / CV_5`; unused by final firmware |
| Mono input | `B4 / AUDIO_IN_LEFT` |
| Main output | `B2 / AUDIO_OUT_LEFT` |
| Optional second output | `B1 / AUDIO_OUT_RIGHT` |

The final firmware reduced the recording-path overload that caused the
high-frequency tone. No additional input attenuator is required on the tested
module. Keep the 100k switched-contact pulldown.

## Leave disconnected

- Original `B6/GATE_OUT_2` connection to the repurposed Reset trigger jack.
- `B5/FREEZE LED`, unless deliberately repurposed in a future firmware build.
- Audio-input-right if building the tested mono version.
- CV5-to-Mix modulation; it is disabled so Mix can reach exact dry/wet endpoints.

## Unpowered checks

- No short between +12V, -12V, 5V, 3V3 and GND.
- Audio input normal contact measures about 100k to GND with no cable inserted.
- Trigger sleeves and toggle commons have continuity to GND.
- Reset trigger tip reaches B9 and does not reach B6.
- Eurorack red stripe reaches the PCB's marked -12V end.
