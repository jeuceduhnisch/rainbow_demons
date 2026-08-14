# Concise build guide

This guide builds Rainbow Demons using the tape-delay PCB and final firmware in
this package. See the top-level README for the independent-design disclaimer.

## 1. Mechanical dry fit

Dry-fit the panel, pots, toggles, buttons, LEDs, jacks, Patch SM carrier and any
perfboard before soldering. Confirm rail clearance, USB/BOOT access and that no
metal hardware can contact perfboard copper.

## 2. Power and carrier

Install the keyed 10-pin Eurorack header with the marked -12V edge at the red
stripe. Socket the Patch SM if possible. Do not feed external 5V or 3V3 into the
Patch SM output rails.

## 3. Pots and CV

Wire the five pots and CV jacks exactly as listed in `PCB_MODIFICATIONS.md`.
Pot end terminals go to the appropriate supply and GND; the wiper goes to the
listed ADC/CV pin. Ground every jack sleeve. CV inputs are already conditioned
by the Patch SM, so external attenuators are optional.

## 4. Audio and triggers

- Mono input tip -> B4; sleeve -> GND.
- Add 100k from the input jack switched/normal contact to GND.
- Main output tip -> B2; optional mirrored output -> B1.
- Record trigger tip -> B10.
- Isolate the reused Reset jack from B6 and wire its tip -> B9.

## 5. Digital controls

- Record button -> D1 to GND.
- Reset button -> D2 to GND.
- Mode toggle outer lugs -> D7/D10; common -> GND.
- Direction toggle outer lugs -> D3/D4; common -> GND.
- Quantize toggle outer lugs -> D5/D6; common -> GND.
- Record LED -> B8 through 1k; Status LED -> B7 through 1k; cathodes -> GND.

If a toggle reads upside-down, exchange only its two outside wires.

## 6. Unpowered inspection

Check the rail isolation, red-stripe orientation, B9 Reset bodge, 100k input
pulldown, LED polarity/resistors, jack grounds and adjacent-header shorts.

## 7. Flash firmware

Put the Patch SM in DFU mode: hold BOOT, tap RESET, then release BOOT. From Git
Bash in the included `firmware` directory run:

```sh
make program-dfu
```

To rebuild first:

```sh
make clean && make && make program-dfu
```

The supplied Makefile uses the complete SDK at
`C:/Users/Jeuce/Documents/Codex/2026-07-07/i-h/work` when the nearby
DaisyExamples SDK is incomplete. Override `LIBDAISY_DIR` and `DAISYSP_DIR` on
the make command line on another computer.

## 8. First power and acceptance test

1. Power from a current-limited/test Eurorack supply if available.
2. Confirm no component heats and the Patch SM starts normally.
3. With Mix fully counter-clockwise, confirm clean dry audio.
4. With Mix fully clockwise, confirm no direct-signal leakage.
5. Record and play a phrase in Slice.
6. Record in Scatter; verify three heads with Flutter high.
7. In Scatter, verify Time, Feedback and Filter run reverse-left, stop near
   noon and run forward-right with Direction centered.
8. Change modes and return; the old capture must not resume.

Do not install the module in the main case until these checks pass.
