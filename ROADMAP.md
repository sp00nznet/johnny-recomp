# Roadmap

- **Long-run content.** The story advances with real days (`NumDays`,
  `CurrentYear/Month/Day` in `SCRANTIC.INI`): Mary, the visitors, the
  holidays, night. Run for days, or move the dates, and check each.
- **Password on wake.** Settings' Password opens the original's Change
  Password dialog; check that `/s` asks for it before ending, and decide
  whether to defer to Windows' own lock instead.
- **One missing sound.** `FindResource` misses `WAVE`/`WAVESFX11` once per
  run; find whether the floppy version lacks it or the lookup is wrong.
- **The settings dialog's picture.** The empty square left of the checkboxes
  is meant to hold an icon or bitmap the host does not load yet.
- **A conformance harness.** Compare `/s` frames against the original under
  Windows 3.1 (a VM with the real `.SCR`), frame by frame from a fixed seed.
- **The 256-colour version.** Lift it too when a copy turns up.
- **Multiple monitors.** `/s` covers the primary monitor only.
