# Changelog

## v0.1.0 (2026-11-12)

First build. `SCRANTIC.SCR` (the 16-colour v1.01 floppy) lifted with
pcrecomp's own NE code map, no IDA: 4,158 functions, 0 unresolved.

- `johnny.scr` is an installable 64-bit Windows screen saver: `/s` runs Johnny
  full screen (scaled from 640x480), `/p <hwnd>` draws in the settings'
  preview box, `/c` opens the original settings dialog.
- Johnny's scenes play one after another: sleeping, walking, fishing, building
  a fire. Sound plays.
- `Setup.cmd` unpacks the floppy's compressed files (`tools/kd_expand.py`),
  lifts, builds, and with `-Install` sets it as your screen saver.
- `tools/hiddenrun.py` runs it on a private desktop and screenshots it.
- Toolkit: pcrecomp branch `pcrecomp-johnny` (the screen saver protocol, a
  Win16 local heap, real StretchBlt, and the GDI calls Johnny needs).
