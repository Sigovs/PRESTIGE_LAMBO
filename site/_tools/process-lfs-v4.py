#!/usr/bin/env python3
"""Slide 06, Lamborghini Financial Services (v4, 22 Oct): Alex's 1920 x 1080 desktop frame,
`___OCT changes/sources/06-lfs/slide06d.jpg`.

    python3 _tools/process-lfs-v4.py

Writes assets/img/slide-lfs-{1920,1280}.{jpg,webp}. No phone frame was supplied: the slide
keeps the Revuelto profile phone crop (hero-dealer-alex-*) until one arrives.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / '06-lfs' / 'slide06d.jpg'
OUT = ROOT / 'assets' / 'img'

src = Image.open(SRC).convert('RGB')
for dw in (1920, 1280):
    img = src if dw == src.width else src.resize((dw, round(dw * 9 / 16)), Image.LANCZOS)
    img.save(OUT / f'slide-lfs-{dw}.jpg', quality=82, optimize=True, progressive=True)
    img.save(OUT / f'slide-lfs-{dw}.webp', quality=78, method=6)
for f in sorted(OUT.glob('slide-lfs-*')):
    print(f'{f.stat().st_size / 1024:7.0f} KB  {f.name}')
