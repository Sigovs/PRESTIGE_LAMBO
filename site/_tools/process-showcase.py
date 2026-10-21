#!/usr/bin/env python3
"""v2 range showcase: Alex's front three-quarter art (MODELS/NEW MODELS, 2430x923 RGBA).
One shared crop for all four, so the scale and baseline Alex set are kept:
x 600..2430, y 60..923 (1830x863). The bodies sit at ~14-89% of the width; the
shadow tails that run further left are faded out over the first 240 px of the
crop (alpha ramp), so the cut never shows as an edge. Resize only, never upscaled.
image 6.png (Revuelto SV) added in v3 (Oct 2026, client request; it had been held back pending US approval)."""
from PIL import Image
import os
SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'MODELS', 'NEW MODELS')
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img')
MAP = {'revuelto': 'image 9.png', 'temerario': 'image 8.png', 'urus-se': 'image 10.png', 'urus-se-performante': 'image 7.png', 'revuelto-sv': 'image 6.png'}
BOX = (600, 60, 2430, 923)
RAMP = 240
for slug, f in MAP.items():
    im = Image.open(os.path.join(SRC, f)).convert('RGBA').crop(BOX)
    w, h = im.size
    a = im.getchannel('A')
    ramp = Image.linear_gradient('L').rotate(90, expand=True).resize((RAMP, h))   # left 0 -> right 255
    mask = Image.new('L', (w, h), 255); mask.paste(ramp, (0, 0))
    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(a, mask))
    for tw in (1830, 1200, 800):
        r = im if tw == w else im.resize((tw, round(h * tw / w)), Image.LANCZOS)
        p = os.path.join(OUT, f'showcase-{slug}-{tw}.webp')
        r.save(p, 'WEBP', quality=84, method=6)
        if tw == 800:
            r.save(os.path.join(OUT, f'showcase-{slug}-800.png'), optimize=True)
    print(slug, im.size)
