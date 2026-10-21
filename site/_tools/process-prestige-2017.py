#!/usr/bin/env python3
"""v3 hero slide 05 (interim, Oct 2026): four of the client's 2017 archive photos for a slow
crossfade until Alex settles the AI animation the client asked for.

    python3 _tools/process-prestige-2017.py

Writes assets/img/slide-prestige-{1..4}-1920.{jpg,webp} (16:9 band) and -p-800 (phone, 800 x 943)."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / '05-prestige-2017'
OUT = ROOT / 'assets' / 'img'
PHONE = 943 / 800

# n, source, desktop band centre y, phone crop centre x (fractions)
PHOTOS = [
    (1, 'Photo-Jun-28-2017-1-25-13-PM.jpg', 0.52, 0.42),   # Irv David with the yellow Diablo SV, Prestige Imports sign
    (2, 'Photo-Aug-09-2017-2-23-55-PM.jpg', 0.50, 0.50),   # with the white Countach
    (3, 'Photo-Aug-09-2017-2-24-04-PM.jpg', 0.50, 0.47),   # in the Countach, doors up
    (4, 'Photo-Aug-09-2017-2-19-57-PM.jpg', 0.48, 0.44),   # black and white, the Diablo at the showroom
]


def save(img, stem):
    img.save(OUT / f'{stem}.jpg', quality=80, optimize=True, progressive=True)
    img.save(OUT / f'{stem}.webp', quality=76, method=6)


for n, name, cy, cx in PHOTOS:
    im = Image.open(SRC / name).convert('RGB')
    w, h = im.size
    bh = round(w * 9 / 16)
    y0 = min(max(round(h * cy - bh / 2), 0), h - bh)
    band = im.crop((0, y0, w, y0 + bh))
    save(band.resize((1920, 1080), Image.LANCZOS) if w >= 1920 else band, f'slide-prestige-{n}-1920')
    pw = round(h / PHONE)
    x0 = min(max(round(w * cx - pw / 2), 0), w - pw)
    save(im.crop((x0, 0, x0 + pw, h)).resize((800, 943), Image.LANCZOS), f'slide-prestige-{n}-p-800')
    print(n, name, (w, h))
