# How the screen saver works

Windows 3.1's `SCRNSAVE.LIB`, linked into `SCRANTIC.SCR`, knows one switch:
`/s` runs, anything else configures. Windows 95 and later call a saver with
`/s`, `/p <hwnd>` and `/c[:<hwnd>]`. pcrecomp's host
(`runtime/win16/host/screensaver.c`) translates: `/s`
and `/p` hand the guest `/s`, `/c` hands it `/c`.

The guest still believes the screen is 640x480; its window is really the
monitor or the preview box, and every DC on it scales the guest's drawing to
fit. The guest's own code ends the saver on a key or mouse movement, as it
always did; in a preview those messages are held back, so hovering over the
settings does not end it, and Windows ends it by closing the box.
