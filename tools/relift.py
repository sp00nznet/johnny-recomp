"""
relift.py - Regenerate Johnny Castaway's lifted tree from your own copy.

Everything below work/ is derived from SCRANTIC.SCR (a Win16 NE executable)
and is never committed. No IDA: pcrecomp builds the code map itself
(tools/ne/ne_codemap.py, the default inside ne_link).

    python tools/relift.py

PCRECOMP_DIR defaults to ../pcrecomp (branch main).
"""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PC = os.path.abspath(os.environ.get('PCRECOMP_DIR', os.path.join(ROOT, '..', 'pcrecomp')))
MODULES = ['game/SCRANTIC.SCR']


def main():
    # Win16 API names by ordinal, from Wine's 16-bit .spec files (downloaded
    # once, a few hundred KB; pcrecomp's wine_spec_to_json.py).
    imports = os.path.join(ROOT, 'work', 'win16_imports.json')
    if not os.path.exists(imports):
        os.makedirs(os.path.dirname(imports), exist_ok=True)
        subprocess.run([sys.executable, os.path.join(PC, 'tools', 'ne', 'wine_spec_to_json.py'),
                        '-o', imports], cwd=ROOT, check=True)
    cmd = [sys.executable, os.path.join(PC, 'tools', 'ne', 'ne_link.py'),
           '--work', 'work', '--prefix', 'recomp',
           '--shims', os.path.join(PC, 'runtime', 'win16', 'host'), '--shims', 'runtime',
           *MODULES]
    print('>', ' '.join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
