#!/usr/bin/env python3
"""Service page, v4 (22 Oct client round 2): the workshop photograph. The client's DSC_3226
(`___OCT changes/sources/04-service/DSC_3226-Edit.jpg`, 5504 x 6880, 4:5: a blue Lamborghini on
a four-post lift) replaces the dealer-shot SVJ (svc-workshop-*). Full frame, 4:5.

    python3 _tools/process-service-v4.py

Writes assets/img/svc-workshop-3226-{1200,800,560}.{jpg,webp}. The hero film is encoded by
hand (see service.html, section 1): ffmpeg, 6.214-18.31 s of Andres-Service-Landing-Video.mov,
1920x1080 and a 4:3 centre crop at 960x720 for portrait phones, first-frame posters.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent / '___OCT changes' / 'sources' / '04-service' / 'DSC_3226-Edit.jpg'
OUT = ROOT / 'assets' / 'img'

im = Image.open(SRC).convert('RGB')
for w in (1200, 800, 560):
    h = round(im.height * w / im.width)
    r = im.resize((w, h), Image.LANCZOS)
    r.save(OUT / f'svc-workshop-3226-{w}.webp', 'WEBP', quality=82, method=6)
    r.save(OUT / f'svc-workshop-3226-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    print(f'svc-workshop-3226-{w}: {w}x{h}')
