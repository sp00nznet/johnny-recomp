# Notice

The MIT license in [LICENSE](LICENSE) covers what is ours in this repository:
the game-specific runtime (`runtime/`), the setup scripts, the tools and the
documentation. It does not cover the screen saver.

*Screen Antics: Johnny Castaway* is © 1992 Sierra On-Line / Dynamix, and is
not ours to license. Its executable, resources and floppy image are not in
this repository and are excluded by `.gitignore`. This project is not
affiliated with or endorsed by them.

- You need your own copy to use any of this. Setup unpacks it into `game/`;
  the pipeline reads it from there.
- Lifted code is a derivative work of the binary it came from. Anything the
  pipeline writes into `work/` or `src/recomp/gen*/` carries whatever license
  the original carries, not this one. The MIT grant stops at our own work.
- The Win16 ordinal map (`work/win16_imports.json`, API names by ordinal) is
  built on your machine by pcrecomp's `tools/ne/wine_spec_to_json.py` from
  Wine's 16-bit `.spec` files, which are LGPL-2.1. It is generated, gitignored
  and not distributed; no Wine code or data is in this repository.

| Path | Upstream | License |
|---|---|---|
| `tools/kd_expand.py` | written for this project in Python; its decoder's structure follows Mark Adler's `blast.c` (zlib `contrib/blast`, 2003-2013) | [zlib](LICENSES/zlib.txt), for the part that follows `blast.c` |

The Win16 front end, host runtime and screen saver host are
[pcrecomp](https://github.com/sp00nznet/pcrecomp)'s, MIT, fetched by setup and
not vendored here.
