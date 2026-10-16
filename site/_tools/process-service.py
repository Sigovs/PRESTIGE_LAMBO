"""Derive the service page images (service.html) from research originals (originals untouched).
Run from the project root:  python3 site/_tools/process-service.py
Each job: source, crop box (left, top, right, bottom) or None, output stem, widths.
Outputs webp + jpg at every width, never upscaled."""
import os
from PIL import Image
R = 'research/images-current-site/service/'
OUT = 'site/assets/img/'
JOBS = [
  # hero, landscape: official AL Huracán STO in a workshop, low-key (no watermark). Full frame;
  # the dark left half (windows, column) is the text field under a constructed scrim.
  (R+'service_huracan-sto-in-workshop-official_1920x1080.jpg', None, 'svc-hero-l', [1920, 1440, 960]),
  # hero, portrait phones: the car alone, 4:3, shown above the copy (no text over it)
  (R+'service_huracan-sto-in-workshop-official_1920x1080.jpg', (450, 142, 1700, 1080), 'svc-hero-p', [1200, 800]),
  # the workshop: dealer-shot Aventador SVJ under a raised Aventador; the crop stops at y 1900,
  # above the stamped 'Lamborghini Miami' shield (starts at about y 1990)
  (R+'service_workshop-lifts-aventador-svj_1824x2280.jpg', (0, 0, 1824, 1900), 'svc-workshop', [1200, 800, 560]),
  # pickup & delivery: dealer-shot Prestige enclosed transporter and flatbed (no watermark)
  (R+'service_prestige-enclosed-transporter-and-flatbed_1920x1280.jpg', None, 'svc-transport', [1440, 960, 640]),
]
os.makedirs(OUT, exist_ok=True)
for src, box, stem, widths in JOBS:
    im = Image.open(src).convert('RGB')
    if box: im = im.crop(box)
    for w in widths:
        if w > im.width: continue
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(f'{OUT}{stem}-{w}.webp', 'WEBP', quality=82, method=6)
        r.save(f'{OUT}{stem}-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
        print(f'{stem}-{w}: {w}x{h}')
