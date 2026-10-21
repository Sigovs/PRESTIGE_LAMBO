#!/usr/bin/env python3
"""v3 model pages (Oct 2026): official lamborghini.com model imagery -> web sizes.
Sources (downloaded from www.lamborghini.com/en-en/models/<model>, gitignored):
    ___OCT changes/sources/models/<slug>/
    python3 _tools/process-model-photos.py revuelto

Writes assets/img/models/<slug>-<role>-<w>.{jpg,webp}. Never upscales."""
from pathlib import Path
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'img' / 'models'
OUT.mkdir(parents=True, exist_ok=True)

SETS = {
    'revuelto': [
        # role, source file, widths
        ('hero', 'Revuelto_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-A-last-optim.jpg', (2400, 1600, 1000)),
        ('hero-p', 'Revuelto_02-Exterior-V_Chapter-Main_Still-B_Config-Alt-A-optim.jpg', (786,)),
        ('exterior', 'banner-desktop.jpg', (2160, 1440)),
        ('exterior-p', 'banner-mobile.jpg', (750,)),
        ('ext-headlight', 'Revuelto_02-Exterior-H_Card-Headlight-last-optim.jpg', (1200, 800)),
        ('ext-rear', 'Revuelto_02-Exterior-H_Card-Rear-last-optim.jpg', (1200, 800)),
        ('ext-engine', 'Revuelto_02-Exterior-H_Card-EngineBay-last-optim.jpg', (1200, 800)),
        ('interior', 'Revuelto_03-Interior-H_Chapter-Main_Still-B-optim.jpg', (2400, 1600, 1000)),
        ('interior-p', 'Revuelto_03-Interior-V_Chapter-Main_Still-B-optim.jpg', (786,)),
        ('int-wheel', 'Revuelto_03-Interior-H_Card-DrivingModes_Still-optim.jpg', (1200, 800)),
        ('int-passenger', 'Revuelto_03-Interior-H_Card-PassengerDisplay_Still-optim.jpg', (1200, 800)),
        ('int-engine', 'Revuelto_00-Mecha-H_Card-Engine-last-optim.jpg', (1200, 800)),
        ('gallery-1', 'gallery1-desktop.jpg', (1600, 900)),
        ('gallery-2', 'gallery2-desktop.jpg', (1600, 900)),
        ('gallery-3', 'gallery3-desktop.jpg', (1600, 900)),
        ('gallery-4', 'gallery4-desktop.jpg', (1600, 900)),
        ('gallery-5', 'gallery5-desktop.jpg', (1600, 900)),
    ],
}

slug = sys.argv[1] if len(sys.argv) > 1 else 'revuelto'
SRC = ROOT.parent / '___OCT changes' / 'sources' / 'models' / slug
for role, name, widths in SETS[slug]:
    im = Image.open(SRC / name).convert('RGB')
    for w in widths:
        if w > im.width:
            w = im.width
        r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f'{slug}-{role}-{w}.jpg', quality=80, optimize=True, progressive=True)
        r.save(OUT / f'{slug}-{role}-{w}.webp', quality=78, method=6)
    print(role, im.size, widths)
