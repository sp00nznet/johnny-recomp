# Building Johnny Castaway by hand

`Setup.cmd` runs exactly these steps (`tools/setup.ps1`).

## Prerequisites

Windows 10/11, **Python 3.10+** (`py -3 --version`) with `capstone`, **CMake**
3.16+, **Ninja**, **MSYS2** with `mingw-w64-x86_64-gcc`
(`C:\msys64\mingw64\bin\gcc.exe`, on `PATH` so gcc finds `cc1`), **git**, and
pcrecomp cloned beside this repository as `pcrecomp`, on
`main`, or
`PCRECOMP_DIR` pointing at it.

Your copy: the files from the floppy (`SCRANTIC.SC$`, `RESOURCE.00$`,
`RESOURCE.MAP`), or an installed copy (`SCRANTIC.SCR`, `RESOURCE.001`,
`RESOURCE.MAP`).

## Steps

```
git clone https://github.com/sp00nznet/pcrecomp ..\pcrecomp
python tools\kd_expand.py <floppy folder> game        & rem or copy an installed copy's files
copy <floppy folder>\RESOURCE.MAP game\
python tools\relift.py
cmake -S . -B build -G Ninja -DCMAKE_C_COMPILER=C:/msys64/mingw64/bin/gcc.exe
cmake --build build
build\johnny.scr /s
```

`build\johnny.exe` is the same program as a console build, for logs.

## Notes

- The floppy's big files are compressed with the PKWARE Data Compression
  Library ("implode"); `tools\kd_expand.py` unpacks them and renames
  `SCRANTIC.EXE` to `SCRANTIC.SCR`, as the installer did.
  `py -3 tools\kd_expand.py --selftest` checks the decoder.
- `tools\relift.py` first builds `work\win16_imports.json`, the Win16 API
  names by ordinal, with pcrecomp's `tools/ne/wine_spec_to_json.py`. It
  downloads Wine's 16-bit `.spec` files from the Wine mirror on GitHub (a few
  hundred KB, once). Those are LGPL, so the map is generated on your machine
  and never committed.
- `Setup.cmd -Install` copies `johnny.scr`, `mem_image.bin` and `game\` to
  `%LOCALAPPDATA%\Programs\JohnnyCastaway` and points
  `HKCU\Control Panel\Desktop\SCRNSAVE.EXE` at it.
