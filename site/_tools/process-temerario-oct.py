#!/usr/bin/env python3
"""Temerario hero slide 03 (v3), from Alex's edit of the client photo DSC_8916:
`___OCT changes/sources/02-temerario/slide 03d.jpg` (1920 x 1080).

    python3 _tools/process-temerario-oct.py

Writes assets/img/slide-temerario-03d-{1920,1280}.{jpg,webp} (desktop, Alex's frame) and
slide-temerario-03d-p-{800,950}.{jpg,webp} (phone, 800 x 943). The car in the 16:9 frame is
wider than the phone frame, so the phone crop comes from the client's 4:5 original,
mirrored to face the same way as Alex's edit, bottom-anchored.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT.parent / '___OCT changes' / 'sources' / '02-temerario'
SRC = DIR / 'slide 03d.jpg'
SRC_PHONE = DIR / 'DSC_8916-Edit.jpg'
OUT = ROOT / 'assets' / 'img'
PHONE_RATIO = 943 / 800


def save(img, stem):
    img.save(OUT / f'{stem}.jpg', quality=82, optimize=True, progressive=True)
    img.save(OUT / f'{stem}.webp', quality=78, method=6)


src = Image.open(SRC).convert('RGB')
w, h = src.size
for dw in (1920, 1280):
    save(src.resize((dw, round(dw * h / w)), Image.LANCZOS), f'slide-temerario-03d-{dw}')

phone_src = ImageOps.mirror(Image.open(SRC_PHONE).convert('RGB'))
pw, ph = phone_src.size
ch = round(pw * PHONE_RATIO)
phone = phone_src.crop((0, ph - ch, pw, ph))
for dw in (800, 950):
    save(phone.resize((dw, round(dw * PHONE_RATIO)), Image.LANCZOS), f'slide-temerario-03d-p-{dw}')
