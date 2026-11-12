"""
kd_expand.py - Unpack the compressed files on the Screen Antics floppy.

Sierra shipped Johnny Castaway on one 1.44 MB disk with a Knowledge Dynamics
installer. Each big file on it ends in '$' (SCRANTIC.SC$, RESOURCE.00$): a
header (magic 65 5D 13 8C, then at 0x1C a length byte and the stored file
name) followed by a PKWARE Data Compression Library "implode" stream. The
installer's only other job is to rename SCRANTIC.EXE to SCRANTIC.SCR.

    python tools/kd_expand.py <the floppy folder> <out folder>
    python tools/kd_expand.py --selftest

The decoder is written from the DCL format (literal/length/distance codes
built from the fixed bit-length tables every DCL stream uses); its structure
follows Mark Adler's blast.c (zlib licence; see NOTICE).
"""
import os
import sys

# Code lengths, run-length packed: each byte is (count-1) << 4 | length.
LITLEN = [11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8, 9, 7, 6, 7, 8, 7, 6,
          55, 8, 23, 24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5, 7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9,
          8, 25, 11, 8, 11, 9, 12, 8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27,
          44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45, 12, 61, 12, 45, 44, 173]
LENLEN = [2, 35, 36, 53, 38, 23]
DISTLEN = [2, 20, 53, 230, 247, 151, 248]
BASE = [3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264]
EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]
MAGIC = b'e]\x13\x8c'


def _table(rep, n):
    lens = []
    for b in rep:
        lens += [b & 15] * ((b >> 4) + 1)
    lens = lens[:n]
    count = [0] * 14
    for ln in lens:
        count[ln] += 1
    offs = [0] * 14
    for i in range(1, 13):
        offs[i + 1] = offs[i] + count[i]
    sym = [0] * n
    for s, ln in enumerate(lens):
        if ln:
            sym[offs[ln]] = s
            offs[ln] += 1
    return count, sym


LIT, LEN, DIST = _table(LITLEN, 256), _table(LENLEN, 16), _table(DISTLEN, 64)


class _Bits:
    def __init__(self, data, pos):
        self.d, self.p, self.buf, self.cnt = data, pos, 0, 0

    def get(self, n):
        v = self.buf
        while self.cnt < n:
            v |= self.d[self.p] << self.cnt
            self.p += 1
            self.cnt += 8
        self.buf, self.cnt = v >> n, self.cnt - n
        return v & ((1 << n) - 1)

    def decode(self, h):                     # codes are stored bit-inverted, MSB first
        count, sym = h
        code = first = index = 0
        for ln in range(1, 14):
            code |= self.get(1) ^ 1
            c = count[ln]
            if code < first + c:
                return sym[index + code - first]
            index += c
            first = (first + c) << 1
            code <<= 1
        raise ValueError('bad DCL code')


def explode(data, pos=0):
    """Decompress one PKWARE DCL stream starting at data[pos]."""
    s = _Bits(data, pos)
    coded, dict_bits = s.get(8), s.get(8)
    if coded > 1 or not 4 <= dict_bits <= 6:
        raise ValueError('not a DCL stream')
    out = bytearray()
    while True:
        if s.get(1):
            sym = s.decode(LEN)
            length = BASE[sym] + s.get(EXTRA[sym])
            if length == 519:
                return bytes(out)
            low = 2 if length == 2 else dict_bits
            dist = (s.decode(DIST) << low) + s.get(low) + 1
            if dist > len(out):
                raise ValueError('distance too far back')
            for _ in range(length):
                out.append(out[-dist])
        else:
            out.append(s.decode(LIT) if coded else s.get(8))


def expand(path):
    """-> (stored name, contents) of one Knowledge Dynamics '$' file."""
    d = open(path, 'rb').read()
    if d[:4] != MAGIC:
        raise ValueError(f'{path}: not a Knowledge Dynamics compressed file')
    n = d[0x1C]
    name = d[0x1D:0x1D + n].split(b'\0')[0].decode('ascii')
    return name, explode(d, 0x1D + n + 1)


def main(argv):
    if argv[1:] == ['--selftest']:
        # A stored-literal stream: header 00 06, nine literal bits per byte,
        # then the end code (length 519).
        bits, nbits = 0, 0
        def put(v, n):
            nonlocal bits, nbits
            bits |= v << nbits; nbits += n
        for ch in b'Johnny':
            put(0, 1); put(ch, 8)
        put(1, 1); put(0b0000000, 7); put(0xFF, 8)   # length code 15 (inverted 0000000) + 8 extra = 519
        raw = bytes([0, 6]) + bits.to_bytes((nbits + 7) // 8, 'little')
        assert explode(raw) == b'Johnny', explode(raw)
        print('kd_expand selftest: ok')
        return 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    src, out = argv[1], argv[2]
    os.makedirs(out, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if f.upper() not in ('SCRANTIC.SC$', 'RESOURCE.00$'):   # INSTALL.EX$ is not needed
            continue
        name, data = expand(os.path.join(src, f))
        if name.upper() == 'SCRANTIC.EXE':
            name = 'SCRANTIC.SCR'                # what the installer names it
        open(os.path.join(out, name), 'wb').write(data)
        print(f'{f} -> {name} ({len(data)} bytes)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
