# Final firmware

This is the exact source/binary pair accepted on the working module on
2026-08-11. Preserve it as the stable baseline.

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
