#!/usr/bin/env python3
"""Stills from the client's service film for the schedule-service, order-parts and collision-center
pages (v4 samples, 23 Oct 2026): `___OCT changes/sources/04-service/Andres-Service-Landing-Video.mov`
(3840 x 2160). No stock imagery (Alex).

    python3 _tools/process-service-stills-v4.py

Writes assets/img/svcf-<name>-{1600,1200,800,560}.{jpg,webp}:
  sto     7.5 s  the grey Huracán STO in the workshop
  engine 10.5 s  a technician at an engine bay
  wheel  13.5 s  a technician fitting a wheel, the tyre
  body   16.5 s  a technician at a blue car's body
  wing   19.5 s  a carbon rear wing in the workshop
"""
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / '04-service' / 'Andres-Service-Landing-Video.mov'
OUT = ROOT / 'assets' / 'img'
TMP = ROOT / '_tools' / '_svcf-frames'
TMP.mkdir(exist_ok=True)
STILLS = {'sto': 7.5, 'engine': 10.5, 'wheel': 13.5, 'body': 16.5, 'wing': 19.5}
for name, t in STILLS.items():
    frame = TMP / f'{name}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(SRC), '-frames:v', '1', str(frame)], check=True)
    im = Image.open(frame).convert('RGB')
    for w in (1600, 1200, 800, 560):
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(OUT / f'svcf-{name}-{w}.webp', 'WEBP', quality=82, method=6)
        r.save(OUT / f'svcf-{name}-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    print(f'svcf-{name}: ok')
for f in TMP.iterdir(): f.unlink()
TMP.rmdir()
