#!/usr/bin/env python3
"""Ad Personam page (ad-personam.html, v4 sample, 23 Oct 2026): stills from the client's own
Ad Personam Revuelto reel, `___OCT changes/sources/ad-personam/Andres-Ad-Personam-Revuelto-Horizontal-Reel.mp4`
(3840 x 2160, 16.3 s; the same reel the homepage chapter loops). No stock imagery (Alex).

    python3 _tools/process-ad-personam-v4.py

Frames are taken mid-shot (scene cuts at 1.33, 2.67, 3.96, 5.34, 6.59, 7.97, 9.30, 10.34, 10.89, 11.97 s)
with ffmpeg at full 4K, then resized. Writes assets/img/adp-<name>-{1600,1200,800,560}.{jpg,webp}:
  wide   7.3 s  the red and black Revuelto, side on, by the hedge
  bull   4.6 s  the car from behind, past a palm trunk (the name is from the shot list; the bull-on-carbon shot is 5.34-6.59 s)
  wheel  9.8 s  the white and red steering wheel, the cabin
  door  11.4 s  the car with its door raised
"""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / 'ad-personam' / 'Andres-Ad-Personam-Revuelto-Horizontal-Reel.mp4'
OUT = ROOT / 'assets' / 'img'
TMP = ROOT / '_tools' / '_adp-frames'
TMP.mkdir(exist_ok=True)

STILLS = {'wide': 7.3, 'bull': 4.6, 'wheel': 9.8, 'door': 11.4}

for name, t in STILLS.items():
    frame = TMP / f'{name}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(SRC), '-frames:v', '1', str(frame)], check=True)
    im = Image.open(frame).convert('RGB')
    for w in (1600, 1200, 800, 560):
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(OUT / f'adp-{name}-{w}.webp', 'WEBP', quality=82, method=6)
        r.save(OUT / f'adp-{name}-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    print(f'adp-{name}: {im.width}x{im.height} -> 1600/1200/800/560')

for f in TMP.iterdir():
    f.unlink()
TMP.rmdir()
