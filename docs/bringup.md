# Bring-up notes

How `SCRANTIC.SCR` went from a floppy image to a working Windows screen saver,
in the order the problems showed up. Toolkit changes are on pcrecomp branch
`pcrecomp-johnny`; everything is IDA-free.

## The files

The archive.org floppy, "Screen Antics - Johnny Castaway (16 Color) (v1.01,
Int. 1.4.93) (Win3.1) (1.44M)", is a FAT12 image holding a Knowledge Dynamics
installer. The two big files end in `$`: a header (`65 5D 13 8C`, the stored
name at 0x1D) and a PKWARE DCL "implode" stream. `tools/kd_expand.py` reads
them: `SCRANTIC.SC$` is `SCRANTIC.EXE` (295,952 bytes, which the installer
renames `.SCR`), `RESOURCE.00$` is `RESOURCE.001` (1,175,645 bytes, every
script, bitmap and palette). `RESOURCE.MAP` is stored as is.

## The lift

`SCRANTIC.SCR` is a 13-code-segment Microsoft C NE. pcrecomp's own code map
finds 534 functions and 33,935 instruction heads; the lift has 4,158 basic-
block functions and no unresolved calls. Three imports had no PASCAL purge in
`win16.py` (SetPixel 10, CreateBitmapIndirect 4, CreateDIBPatternBrush 4).
The ordinal names come from Wine's `.spec` files
(`wine_spec_to_json.py`); `tools/relift.py` builds them on first run.

## Startup

1. **"Program Aborted" at once:** `LocalAlloc` was a stub returning 0. The host
   now keeps a first-fit local heap per DGROUP, in the heap+stack tail the NE
   header asks for. (The first version read `SEG_SEGMENT_BASE` one past its
   end for the last segment and handed out blocks over the stack.)
2. **A black window and 2 billion calls a second:** the scene scheduler polls
   `GetCurrentTime` for its next deadline. The host's clock was synthetic
   (16 ms per call), so the guest raced through time without drawing.
   `RecompGame.real_clock` gives it `GetTickCount`.
3. **Every sprite mask failed:** Johnny keeps a 1-bpp mask bitmap per sprite
   frame, hundreds of them; the host's 256 GDI handles ran out. Now 0x4000.
4. **Still nothing on screen:** all the drawing is `StretchBlt` with mask
   ROPs, between memory DCs and onto the window. The host sent every
   `StretchBlt` down WinG's path, which ignores plain DCs and the ROP. Now a
   real `StretchBlt` handles any non-WinG source.

After that: the island, the sea, the clouds and Johnny, in the 16 colours of
the game's own DIB colour tables.

## The screen saver protocol

`SCRNSAVE.LIB` (Windows 3.1) reads `lpCmdLine`: `-s`/`/s` runs, `-c`/`/c`
opens "ScreenSaverConfigure", anything else opens dialog 109 and then runs.
The host's `InitTask` used to hand every guest an empty command line; it now
passes one (ES:BX at PSP:0081) when there is one. `screensaver.c` maps the
Windows 95+ switches onto it:

| Windows calls | Guest gets | Host does |
|---|---|---|
| `/s` | `/s` | sizes the saver window to the monitor, topmost |
| `/p <hwnd>` | `/s` | makes the saver window a child filling `<hwnd>`; no input or activation messages reach the guest; no sound; quits when the parent goes |
| `/c`, `/c:<hwnd>` | `/c` | nothing more |

The guest asked `GetSystemMetrics` for the screen and believes 640x480. Every
DC on the saver window gets `MM_ANISOTROPIC` from 640x480 to the real client
size, so all of the guest's drawing scales with no change to it. Two things had
to stop resizing the window afterwards: the host's own "main frame is
640x480" rule (the saver hook now runs after it), and the guest's
`SetWindowPos` (ignored for the saver window).

The `/c` dialog failed to open: it is the program's first window, made before
any `RegisterClass`, and the host's fallback class name had never been
registered. Its checkboxes came up unticked (the host kept dialog state in a
table and never told the real controls), and its background was never erased.

## Installing

An installed `.scr` lives somewhere else entirely. The host now looks for
`mem_image.bin` and a `game\` folder beside the executable before the build
tree's compiled-in paths, and the `.scr` is linked `-static` with no console
(`-mwindows`). `Setup.cmd -Install` copies the three into
`%LOCALAPPDATA%\Programs\JohnnyCastaway` and sets
`HKCU\Control Panel\Desktop\SCRNSAVE.EXE`.

## Testing without a screen

`tools/hiddenrun.py` creates a private desktop, starts the program on it,
screenshots its windows from a thread that has joined that desktop (a GDI read
from another desktop comes back black), and with `--preview WxH` makes a
stand-in preview box and passes its handle as `{hwnd}`. `--end-at T` closes the
preview, or presses a key in the saver, which is how ending was checked: `/s`
exits on a key, `/p` when its box closes, `/c` when OK is clicked.
