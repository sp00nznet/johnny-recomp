# Testing Johnny Castaway

There is no conformance harness yet ([ROADMAP.md](../ROADMAP.md)); runs are
checked by screenshot.

## The switches

| Command | What it does |
|---|---|
| `johnny.scr /s` | full screen; any key or mouse movement ends it |
| `johnny.scr /p <hwnd>` | draws inside the window `<hwnd>` until that window closes |
| `johnny.scr /c` (or no arguments) | the settings dialog |

`build\johnny.exe` is the same program as a console build, for logs. Set
`PCRECOMP_MUTE=1` for silence.

## Runs that don't take a screen

`tools\hiddenrun.py` runs any of these on a private desktop and screenshots
it; every picture in the README was taken this way. Always mute it:

```
set PCRECOMP_MUTE=1
py -3 tools\hiddenrun.py --secs 30 --shot 20 --out out\run -- build\johnny.scr /s
py -3 tools\hiddenrun.py --preview 304x224 --secs 30 --shot 20 --out out\prev -- build\johnny.scr /p {hwnd}
```

`/s` on the real desktop would take the whole monitor, so don't run it there
from a script.
