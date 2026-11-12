# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `NOTICE.md` (replacing `NOTICE`, with a row and `LICENSES/zlib.txt` for
  `tools/kd_expand.py`'s debt to `blast.c`), `CONTRIBUTING.md`,
  `CONTRIBUTORS.md`, `docs/building.md`, `docs/testing.md`,
  `docs/screensaver.md`, a manual-only `installer` workflow, and a `setup.sh`
  that says plainly there is no Linux or macOS build yet.

### Changed
- README in the ra2 house style; the step-by-step build, the switches and the
  screen saver notes moved to `docs/`.

## [0.1.0] - 2026-11-12

### Added
- First build. `SCRANTIC.SCR` (the 16-color v1.01 floppy) lifted with
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
