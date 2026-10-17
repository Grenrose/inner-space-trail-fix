#!/usr/bin/env python3
"""Build SMALL7.FON: a 'Small Fonts' bitmap face with a 7-pixel cell, the size
Operation: Inner Space asks for when it labels icons
(CreateFont(7,...,PROOF_QUALITY, VARIABLE_PITCH|FF_SWISS, "Small Fonts")).

Wine's own smalle.fon only has an 11-pixel face, so labels drawn at y=32 run
to row 42 and spill into sprite-sheet margins the game never clears, which is
what made moving icons trail. Here all ink sits in rows 0..5; row 6 is empty.

Hand-drawn glyphs ('#' = ink), 6 rows each (row 6 is added blank).
Capitals use rows 0-4; lowercase x-height rows 1-4; descenders use row 5.

usage: small7font.py OUT.FON [preview.png]
"""
import struct, sys

G = {
' ': ["..", "..", "..", "..", "..", ".."],
'!': ["#", "#", "#", ".", "#", "."],
'"': ["#.#", "#.#", "...", "...", "...", "..."],
'#': ["#.#", "###", "#.#", "###", "#.#", "..."],
'$': [".##", "##.", ".#.", ".##", "##.", "..."],
'%': ["#.#", "..#", ".#.", "#..", "#.#", "..."],
'&': [".#.", "#.#", ".#.", "#.#", ".##", "..."],
"'": ["#", "#", ".", ".", ".", "."],
'(': [".#", "#.", "#.", "#.", ".#", ".."],
')': ["#.", ".#", ".#", ".#", "#.", ".."],
'*': ["#.#", ".#.", "#.#", "...", "...", "..."],
'+': ["...", ".#.", "###", ".#.", "...", "..."],
',': [".", ".", ".", ".", "#", "#"],
'-': ["...", "...", "###", "...", "...", "..."],
'.': [".", ".", ".", ".", "#", "."],
'/': ["..#", "..#", ".#.", "#..", "#..", "..."],
'0': ["###", "#.#", "#.#", "#.#", "###", "..."],
'1': [".#.", "##.", ".#.", ".#.", "###", "..."],
'2': ["##.", "..#", ".#.", "#..", "###", "..."],
'3': ["##.", "..#", ".#.", "..#", "##.", "..."],
'4': ["#.#", "#.#", "###", "..#", "..#", "..."],
'5': ["###", "#..", "##.", "..#", "##.", "..."],
'6': [".##", "#..", "###", "#.#", "###", "..."],
'7': ["###", "..#", ".#.", ".#.", ".#.", "..."],
'8': ["###", "#.#", "###", "#.#", "###", "..."],
'9': ["###", "#.#", "###", "..#", "##.", "..."],
':': [".", "#", ".", "#", ".", "."],
';': [".", "#", ".", ".", "#", "#"],
'<': ["..#", ".#.", "#..", ".#.", "..#", "..."],
'=': ["...", "###", "...", "###", "...", "..."],
'>': ["#..", ".#.", "..#", ".#.", "#..", "..."],
'?': ["##.", "..#", ".#.", "...", ".#.", "..."],
'@': [".#.", "#.#", "###", "#..", ".##", "..."],
'A': [".#.", "#.#", "###", "#.#", "#.#", "..."],
'B': ["##.", "#.#", "##.", "#.#", "##.", "..."],
'C': [".##", "#..", "#..", "#..", ".##", "..."],
'D': ["##.", "#.#", "#.#", "#.#", "##.", "..."],
'E': ["###", "#..", "##.", "#..", "###", "..."],
'F': ["###", "#..", "##.", "#..", "#..", "..."],
'G': [".##", "#..", "#.#", "#.#", ".##", "..."],
'H': ["#.#", "#.#", "###", "#.#", "#.#", "..."],
'I': ["###", ".#.", ".#.", ".#.", "###", "..."],
'J': ["..#", "..#", "..#", "#.#", ".#.", "..."],
'K': ["#.#", "#.#", "##.", "#.#", "#.#", "..."],
'L': ["#..", "#..", "#..", "#..", "###", "..."],
'M': ["#...#", "##.##", "#.#.#", "#...#", "#...#", "....."],
'N': ["#..#", "##.#", "#.##", "#..#", "#..#", "...."],
'O': [".#.", "#.#", "#.#", "#.#", ".#.", "..."],
'P': ["##.", "#.#", "##.", "#..", "#..", "..."],
'Q': [".#.", "#.#", "#.#", "##.", ".##", "..."],
'R': ["##.", "#.#", "##.", "#.#", "#.#", "..."],
'S': [".##", "#..", ".#.", "..#", "##.", "..."],
'T': ["###", ".#.", ".#.", ".#.", ".#.", "..."],
'U': ["#.#", "#.#", "#.#", "#.#", "###", "..."],
'V': ["#.#", "#.#", "#.#", "#.#", ".#.", "..."],
'W': ["#...#", "#...#", "#.#.#", "##.##", "#...#", "....."],
'X': ["#.#", "#.#", ".#.", "#.#", "#.#", "..."],
'Y': ["#.#", "#.#", ".#.", ".#.", ".#.", "..."],
'Z': ["###", "..#", ".#.", "#..", "###", "..."],
'[': ["##", "#.", "#.", "#.", "##", ".."],
'\\': ["#..", "#..", ".#.", "..#", "..#", "..."],
']': ["##", ".#", ".#", ".#", "##", ".."],
'^': [".#.", "#.#", "...", "...", "...", "..."],
'_': ["...", "...", "...", "...", "...", "###"],
'`': ["#.", ".#", "..", "..", "..", ".."],
'a': ["...", ".##", "#.#", "#.#", ".##", "..."],
'b': ["#..", "##.", "#.#", "#.#", "##.", "..."],
'c': ["...", ".##", "#..", "#..", ".##", "..."],
'd': ["..#", ".##", "#.#", "#.#", ".##", "..."],
'e': ["...", ".#.", "###", "#..", ".##", "..."],
'f': [".##", "#..", "###", "#..", "#..", "..."],
'g': ["...", ".##", "#.#", ".##", "..#", "##."],
'h': ["#..", "##.", "#.#", "#.#", "#.#", "..."],
'i': ["#", ".", "#", "#", "#", "."],
'j': [".#", "..", ".#", ".#", ".#", "#."],
'k': ["#..", "#.#", "##.", "##.", "#.#", "..."],
'l': ["#", "#", "#", "#", "#", "."],
'm': [".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "....."],
'n': ["...", "##.", "#.#", "#.#", "#.#", "..."],
'o': ["...", ".#.", "#.#", "#.#", ".#.", "..."],
'p': ["...", "##.", "#.#", "##.", "#..", "#.."],
'q': ["...", ".##", "#.#", ".##", "..#", "..#"],
'r': ["...", "#.#", "##.", "#..", "#..", "..."],
's': ["...", ".##", "##.", "..#", "##.", "..."],
't': [".#.", "###", ".#.", ".#.", ".##", "..."],
'u': ["...", "#.#", "#.#", "#.#", ".##", "..."],
'v': ["...", "#.#", "#.#", "#.#", ".#.", "..."],
'w': [".....", "#...#", "#.#.#", "#.#.#", ".#.#.", "....."],
'x': ["...", "#.#", ".#.", ".#.", "#.#", "..."],
'y': ["...", "#.#", "#.#", ".##", "..#", "##."],
'z': ["...", "###", "..#", "#..", "###", "..."],
'{': [".##", ".#.", "##.", ".#.", ".##", "..."],
'|': ["#", "#", "#", "#", "#", "."],
'}': ["##.", ".#.", ".##", ".#.", "##.", "..."],
'~': ["....", ".#.#", "#.#.", "....", "....", "...."],
}
BOX = ["###", "#.#", "#.#", "#.#", "###", "..."]       # default glyph (codes without a design)

CELL_H, ASCENT, FIRST, LAST = 7, 5, 0x20, 0xFF
FACE = b"Small Fonts\0"


def glyph(code):
    rows = G.get(chr(code), BOX) if code < 0x7F else BOX
    w = len(rows[0]) + 1                                  # +1 px spacing column
    assert all(len(r) == len(rows[0]) for r in rows) and len(rows) == 6, chr(code)
    return w, [r + "." for r in rows] + ["." * w]         # row 6 always blank


def build_fnt():
    chars = [glyph(c) for c in range(FIRST, LAST + 1)]
    n = len(chars)
    hdr_len = 118
    table_len = (n + 1) * 4                               # v2 table: WORD width, WORD offset (+ sentinel)
    bits_off = hdr_len + table_len
    bitmaps, offsets, off = [], [], bits_off
    for w, rows in chars:
        offsets.append(off)
        ncols = (w + 7) // 8
        data = bytearray()
        for cb in range(ncols):                           # column-major 8-pixel strips
            for r in rows:
                byte = 0
                for bit in range(8):
                    x = cb * 8 + bit
                    if x < w and r[x] == "#":
                        byte |= 0x80 >> bit
                data.append(byte)
        bitmaps.append(bytes(data))
        off += len(data)
    face_off = off
    total = face_off + len(FACE)
    widths = [w for w, _ in chars]
    avg = round(sum(widths[ord('a') - FIRST:ord('z') - FIRST + 1]) / 26)
    hdr = struct.pack("<HI60sHHHHHHHBBBHBHHBHHBBBBHIIIIB",
        0x0200, total, b"Small Fonts 7px for Operation: Inner Space under Wine",
        0,                      # raster
        5,                      # nominal point size (7 px @ 96 dpi)
        96, 96,                 # vertical/horizontal resolution
        ASCENT, 0, 0,           # ascent, internal leading, external leading
        0, 0, 0,                # italic, underline, strikeout
        400,                    # weight
        0,                      # ANSI charset
        0, CELL_H,              # pixel width (0 = variable), pixel height
        0x21,                   # variable pitch | FF_SWISS
        avg, max(widths),
        FIRST, LAST, ord('?') - FIRST, ord(' ') - FIRST,
        (sum(widths) + 15) // 16 * 2,
        0, face_off, 0, bits_off, 0)
    assert len(hdr) == hdr_len, len(hdr)
    table = b"".join(struct.pack("<HH", w, o) for w, o in zip(widths, offsets))
    table += struct.pack("<HH", 0, off)                   # sentinel
    fnt = hdr + table + b"".join(bitmaps) + FACE
    assert len(fnt) == total
    return fnt, hdr


def build_fon(fnt, hdr):
    """Wrap one FNT in a minimal NE font library (.FON) with FONTDIR + FONT."""
    SHIFT = 4
    def pad(b):
        return b + b"\0" * ((-len(b)) % (1 << SHIFT))
    modname = b"SMALL7"
    desc = b"FONTRES 100,96,96 : Small Fonts 7"
    fontdir = struct.pack("<HH", 1, 1) + hdr[:113] + b"\0" + FACE   # count, ordinal, entry, no device, face
    mz = bytearray(64)
    mz[0:2] = b"MZ"
    struct.pack_into("<H", mz, 0x18, 0x40)
    struct.pack_into("<I", mz, 0x3C, 64)
    ne_off = 64
    # tables following the 64-byte NE header
    restab_hdr_len = 2 + 8 + 12 + 8 + 12 + 2                   # shift, 2 types x (typeinfo + 1 nameinfo), end
    resname = bytes([len(modname)]) + modname + b"\0\0" + b"\0"   # resident names
    modref, impnames, enttab = b"", b"\0", b"\0\0"
    nonres = bytes([len(desc)]) + desc + b"\0\0" + b"\0"
    seg_tab = 0x40
    rsrc_tab = seg_tab
    resn_tab = rsrc_tab + restab_hdr_len
    modr_tab = resn_tab + len(resname)
    impn_tab = modr_tab + len(modref)
    ent_tab = impn_tab + len(impnames)
    tables_end = ne_off + ent_tab + len(enttab)
    nonres_off = tables_end
    data_start = nonres_off + len(nonres)
    data_start += (-data_start) % (1 << SHIFT)
    fd_off = data_start
    fd = pad(fontdir)
    fn_off = fd_off + len(fd)
    fn = pad(fnt)
    def nameinfo(off, ln, rid):
        return struct.pack("<HHHHHH", off >> SHIFT, ln >> SHIFT, 0x0c50, rid, 0, 0)
    rsrc = struct.pack("<H", SHIFT)
    rsrc += struct.pack("<HHI", 0x8007, 1, 0) + nameinfo(fd_off, len(fd), 0x8001)   # RT_FONTDIR
    rsrc += struct.pack("<HHI", 0x8008, 1, 0) + nameinfo(fn_off, len(fn), 0x8001)   # RT_FONT
    rsrc += b"\0\0"
    ne = bytearray(64)
    ne[0:2] = b"NE"
    ne[2], ne[3] = 5, 10
    struct.pack_into("<HH", ne, 0x04, ent_tab, len(enttab))
    struct.pack_into("<H", ne, 0x0C, 0x8300)                    # library, no data segs
    struct.pack_into("<H", ne, 0x20, len(nonres))
    struct.pack_into("<HHHHH", ne, 0x22, seg_tab, rsrc_tab, resn_tab, modr_tab, impn_tab)
    struct.pack_into("<I", ne, 0x2C, nonres_off)
    struct.pack_into("<H", ne, 0x32, SHIFT)
    struct.pack_into("<H", ne, 0x34, 2)                         # resource segments
    ne[0x36] = 2                                                # Windows
    struct.pack_into("<H", ne, 0x3E, 0x030A)                    # expected Windows 3.10
    body = bytes(mz) + bytes(ne) + rsrc + resname + modref + impnames + enttab + nonres
    body += b"\0" * (fd_off - len(body))
    return body + fd + fn


if __name__ == "__main__":
    fnt, hdr = build_fnt()
    fon = build_fon(fnt, hdr)
    open(sys.argv[1], "wb").write(fon)
    print("wrote %s: %d bytes (one face: 7 px cell, ascent %d, ink rows 0..5)" % (sys.argv[1], len(fon), ASCENT))
    if len(sys.argv) > 2:
        from PIL import Image
        samples = ["CALENDAR CARDFILE CLOCK CONTROL", "notepad winhelp regedit hh.exe",
                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789", "abcdefghijklmnopqrstuvwxyz gjpqy"]
        lines = []
        for s in samples:
            gl = [glyph(ord(c)) for c in s]
            lines.append(["".join(rows[r] for w, rows in gl) for r in range(CELL_H)])
        W = max(len(l[0]) for l in lines)
        img = Image.new("L", (W + 4, len(lines) * (CELL_H + 3)), 0)
        for i, l in enumerate(lines):
            for r, row in enumerate(l):
                for x, ch in enumerate(row):
                    if ch == "#":
                        img.putpixel((x + 2, i * (CELL_H + 3) + 1 + r), 255)
        img.resize((img.width * 8, img.height * 8), Image.NEAREST).save(sys.argv[2])
        w = sum(glyph(ord(c))[0] for c in "CALENDAR")
        print("'CALENDAR' is %d px wide -> centred on x=22 it spans %d..%d (cell 6..37)" % (w, 22 - w // 2, 22 - w // 2 + w - 1))
