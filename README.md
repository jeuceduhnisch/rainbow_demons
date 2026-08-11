# Rainbow Demons - Final Working Release

Release date: 2026-08-11

This package preserves the tested DIY Eurorack instrument, final firmware and
the tape-delay PCB fabrication files actually used for the build.

## Independent-design disclaimer

Rainbow Demons is an independently designed instrument inspired by broad
buffer-manipulation ideas associated with MTL ASM's Count to 5. It is not a
clone, reproduction, port, or claim of exact pedal behavior. No original source
code, firmware, schematics, PCB files, or proprietary design material were
used. This project is not affiliated with or endorsed by MTL ASM.

## Start here

1. Read `PCB_MODIFICATIONS.md` before powering the tape-delay PCB.
2. Build from `BUILD_GUIDE.md` and `BOM.md`.
3. Flash `firmware/build/RainbowDemons.bin` or rebuild from source.
4. Use `QUICK_START.md` for the final control map.

The same material is combined into `Rainbow_Demons_Build_Documentation.pdf`.

## Package layout

- Top level - concise build guide, PCB changes, BOM, quick start and PDF.
- `firmware/` - final source, Makefile, startup file and verified binary.
- `pcb/` - tape-delay main PCB/faceplate Gerbers, source and base wiring map.

## Verified firmware

- Binary size: 87,208 bytes
- SHA-256: `661A7DB0510F7DD0625B3B4981CDC01A40592A78591653F14ADCE66548FBF970`
- Mode 3 head range: 1/8x to 8x, or -3 to +3 octaves
- Mix: counter-clockwise dry, clockwise wet, with hard digital endpoints
- Changing Mode clears captured audio and invalidates the previous phrase

## Gerber note

The included Gerbers are the tape-delay PCB files used for this build. They do
not contain the documented 100k pulldown, Reset-trigger bodge or new toggle
wiring as copper changes; apply those modifications manually.
