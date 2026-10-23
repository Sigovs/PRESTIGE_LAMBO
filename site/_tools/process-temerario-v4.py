#!/usr/bin/env python3
"""Temerario hero slide 03 (v4, 22 Oct client change): the client's DSC_1766 (white car, rear
three-quarter, palm and sea), `___OCT changes/sources/03-temerario/DSC_1766-Edit-copy.jpg`
(4409 x 5512, 4:5).

    python3 _tools/process-temerario-v4.py

Desktop: Alex's own 1920 x 1080 frame of that photo (`slide 03d.jpg`: the car smaller, right of
centre, sky and water around it). Writes assets/img/slide-temerario-1766-{1920,1280}.{jpg,webp}.
Phone: Alex's own portrait frame `slide 03m.png` (440 x 956, a whole phone screen), used whole,
not cropped (Alex, 22 Oct). The slide shows it full-height on portrait phones
(`hero__slide--full-m`). Writes slide-temerario-1766-m-440.{jpg,webp}.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT.parent / '___OCT changes' / 'sources' / '03-temerario'
SRC = DIR / 'DSC_1766-Edit-copy.jpg'
SRC_DESK = DIR / 'slide 03d.jpg'
SRC_PHONE = DIR / 'slide 03m.png'
SRC_PHONE = DIR / 'slide 03m.png'
OUT = ROOT / 'assets' / 'img'
STEM = 'slide-temerario-1766'


def save(img, stem):
    img.save(OUT / f'{stem}.jpg', quality=82, optimize=True, progressive=True)
    img.save(OUT / f'{stem}.webp', quality=78, method=6)


desk = Image.open(SRC_DESK).convert('RGB')
for dw in (1920, 1280):
    save(desk.resize((dw, round(dw * 9 / 16)), Image.LANCZOS) if dw != desk.width else desk, f'{STEM}-{dw}')

phone = Image.open(SRC_PHONE).convert('RGB')
save(phone, f'{STEM}-m-{phone.width}')

for f in sorted(OUT.glob(f'{STEM}*')):
    print(f'{f.stat().st_size / 1024:7.0f} KB  {f.name}')
