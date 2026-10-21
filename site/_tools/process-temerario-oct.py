#!/usr/bin/env python3
"""Temerario hero slide, October client photos (DSC_8916 / 8930 / 8942).

The three sources are 4:5 portraits; the desktop slide is 16:9, so each gets a
full-width horizontal band (top edge set per photo, as a fraction of the height)
and a phone crop at the existing portrait ratio (800 x 943).

    python3 _tools/process-temerario-oct.py

Writes assets/img/slide-temerario-oct-{a,b,c}-{1920,1280}.{jpg,webp}
and slide-temerario-oct-{a,b,c}-p-{800,950}.{jpg,webp}.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / '02-temerario'
OUT = ROOT / 'assets' / 'img'

# key, file, desktop band top (fraction of height), phone crop centre x (fraction of width)
PHOTOS = [
    ('a', 'DSC_8916-Edit.jpg', 0.350, 0.48),   # profile on the causeway, palm + Brickell
    ('b', 'DSC_8930-Edit.jpg', 0.315, 0.40),   # three-quarter front, curve + skyline
    ('c', 'DSC_8942-Edit.jpg', 0.365, 0.50),   # rear, palm + bridge
]
DESK = [1920, 1280]
PHONE = [800, 950]
PHONE_RATIO = 943 / 800


def save(img, stem):
    img.save(OUT / f'{stem}.jpg', quality=82, optimize=True, progressive=True)
    img.save(OUT / f'{stem}.webp', quality=78, method=6)


for key, name, top, cx in PHOTOS:
    src = Image.open(SRC / name).convert('RGB')
    w, h = src.size

    band_h = round(w * 9 / 16)
    y0 = min(round(h * top), h - band_h)
    band = src.crop((0, y0, w, y0 + band_h))
    for dw in DESK:
        save(band.resize((dw, round(dw * 9 / 16)), Image.LANCZOS), f'slide-temerario-oct-{key}-{dw}')

    # phone: full height, width trimmed to the portrait ratio around cx
    pw = round(h / PHONE_RATIO)
    x0 = min(max(round(w * cx - pw / 2), 0), w - pw) if pw < w else 0
    ph_src = src.crop((x0, 0, x0 + min(pw, w), h)) if pw < w else src.crop((0, round((h - w * PHONE_RATIO) / 2), w, round((h + w * PHONE_RATIO) / 2)))
    for dw in PHONE:
        save(ph_src.resize((dw, round(dw * PHONE_RATIO)), Image.LANCZOS), f'slide-temerario-oct-{key}-p-{dw}')
    print(key, name, 'band y', y0, '..', y0 + band_h, 'of', h)
