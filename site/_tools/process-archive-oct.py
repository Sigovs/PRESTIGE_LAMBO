#!/usr/bin/env python3
"""v3 archive strip (Oct 2026): the client's archive photos -> 3:2 cards like the 1980-86 ones
(assets/img/archive-<year>-640.jpg, 640 x 427, plus a 1280 for 2x screens where the source allows).

    python3 _tools/process-archive-oct.py

Each source is cut to 3:2 around a focus point (fractions of width / height) chosen per frame.
Sources: ___OCT changes/sources/archive/<year>_<name>.jpg (gitignored)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / 'archive'
OUT = ROOT / 'assets' / 'img'

# slug, source, focus x, focus y
CARDS = [
    ('1990', '1990_FullSizeRender-5.jpg', 0.45, 0.50),            # Ferruccio Lamborghini signing for Irv David
    ('2007', '2007_226098_211943248853445_999151_n.jpg', 0.50, 0.50),   # the Sharpie Gallardo (small source, 604 px)
    ('2014', '2014_DSC_9840.jpg', 0.50, 0.50),                    # Veneno on the turntable
    ('2020', '2020_DSC_4048.jpg', 0.50, 0.42),                    # grand opening: the gold bull handed over
    ('2021', '2021_DSC_9511.jpg', 0.50, 0.55),                    # Sián at the Lamborghini Miami sign
    ('2022', '2022_BMG03862.jpg', 0.45, 0.55),                    # Tecnomar for Lamborghini 63
    ('2024-trofeo', '2024a_20240621-h-7832.jpg', 0.50, 0.62),     # Super Trofeo start
    ('2024-movember', '2024b_DSC_2376.jpg', 0.50, 0.70),          # Countach with a moustache, Movember
    ('2025', '2025_DSC_1988-3.jpg', 0.50, 0.55),                  # Sián in white and purple
]
RATIO = 3 / 2


def cut(im, fx, fy):
    w, h = im.size
    if w / h > RATIO:
        cw, ch = round(h * RATIO), h
    else:
        cw, ch = w, round(w / RATIO)
    x0 = min(max(round(w * fx - cw / 2), 0), w - cw)
    y0 = min(max(round(h * fy - ch / 2), 0), h - ch)
    return im.crop((x0, y0, x0 + cw, y0 + ch))


for slug, name, fx, fy in CARDS:
    im = cut(Image.open(SRC / name).convert('RGB'), fx, fy)
    for tw in (640, 1280):
        if tw > im.width and tw != 640:
            continue                      # never upscale for 2x; the 640 is the floor every card has
        r = im.resize((tw, round(tw / RATIO)), Image.LANCZOS)
        r.save(OUT / f'archive-{slug}-{tw}.jpg', quality=80, optimize=True, progressive=True)
        r.save(OUT / f'archive-{slug}-{tw}.webp', quality=76, method=6)
    print(slug, im.size)
