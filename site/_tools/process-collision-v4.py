#!/usr/bin/env python3
"""Collision center page hero (v4 sample, 23 Oct 2026): a still, the client's DSC_3226
(`___OCT changes/sources/04-service/DSC_3226-Edit.jpg`, 5504 x 6880): the blue car on the four-post
lift, its underside and the tool chests. Landscape: a 16:9 band from BAND_TOP (the lift, the underside,
the chests: dark on the left under the copy). Portrait phones: a 4:3 crop from the top of the band.

    python3 _tools/process-collision-v4.py

Writes assets/img/cc-hero-l-{1920,1440,960}.{jpg,webp} and cc-hero-p-{1200,800}.{jpg,webp}.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / '04-service' / 'DSC_3226-Edit.jpg'
OUT = ROOT / 'assets' / 'img'
BAND_TOP = 2064

im = Image.open(SRC).convert('RGB'); w, h = im.size
band = im.crop((0, BAND_TOP, w, BAND_TOP + round(w * 9 / 16)))
for dw in (1920, 1440, 960):
    r = band.resize((dw, round(dw * 9 / 16)), Image.LANCZOS)
    r.save(OUT / f'cc-hero-l-{dw}.webp', 'WEBP', quality=82, method=6)
    r.save(OUT / f'cc-hero-l-{dw}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
ph = round(w * 3 / 4)
port = im.crop((0, 1400, w, 1400 + ph))   # the car on the lift and the chests, 4:3
for dw in (1200, 800):
    r = port.resize((dw, round(dw * 3 / 4)), Image.LANCZOS)
    r.save(OUT / f'cc-hero-p-{dw}.webp', 'WEBP', quality=82, method=6)
    r.save(OUT / f'cc-hero-p-{dw}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
print('cc-hero: ok')
