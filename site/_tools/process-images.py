"""Derive web images for site/assets/img from research originals (originals untouched).
Run from the project root:  python3 site/_tools/process-images.py
Each job: source, crop box (left, top, right, bottom) or None, output stem, widths.
Crops remove the stamped 'Lamborghini Miami' shield watermark or inventory footer band where noted."""
import os
from PIL import Image
R = 'research/images-current-site/'
S = 'research/inventory-capture-2026-09-30/photos/'
OUT = 'site/assets/img/'
JOBS = [
  # hero: Temerario front 3/4, dark studio (no watermark)
  (R+'hero/hero_temerario-blue-front-3q-dark_1920x707.jpg', None, 'hero-temerario', [1920, 1440, 960]),
  (R+'hero/hero_temerario-blue-front-3q-dark_1920x707.jpg', (760, 40, 1920, 707), 'hero-temerario-m', [1160, 780]),
  # Ad Personam: Urus SE cabin; crop drops the bottom-right shield watermark
  (R+'models/urus-se/urus-se_interior-dashboard-orange_5000x3333.jpg', (0, 280, 4400, 2755), 'adp-urus-se-cabin', [2400, 1600, 1000]),
  (R+'models/urus-se/urus-se_interior-dashboard-orange_5000x3333.jpg', (700, 0, 3300, 3250), 'adp-urus-se-cabin-m', [1000, 720]),
  # Service: dealer workshop; crop drops watermark
  (R+'service/service_workshop-white-bays-technician_1697x2121.jpg', (170, 0, 1626, 1820), 'service-workshop', [1200, 800, 560]),
  # Showroom aerial at night; crop drops watermark
  (R+'showroom-facility/facility_lamborghini-miami-showroom-aerial-night_1980x1114.png', (0, 0, 1760, 990), 'showroom-aerial-night', [1760, 1200, 800]),
  # Archive prints (640px masters, shown small)
  (R+'showroom-facility/history-under-1600/history_1980_irv-david-original-prestige-west-dixie_640x427.jpg', None, 'archive-1980', [640]),
  (R+'showroom-facility/history-under-1600/history_1983_biscayne-land-future-home-sign_640x427.jpg', None, 'archive-1983', [640]),
  (R+'showroom-facility/history-under-1600/history_1986_grand-opening-night_640x427.jpg', None, 'archive-1986', [640]),
  # Inventory primary photos (1024x768 max); crop drops the Prestige/Lamborghini Miami footer band
  (S+'urus-se-2026.jpg', (0, 24, 1024, 600), 'inv-2026-urus-se', [1024, 640]),
  (S+'revuelto-2024-giallo.jpg', (0, 24, 1024, 600), 'inv-2024-revuelto-giallo', [1024, 640]),
  (S+'revuelto-2024-acheso.jpg', (0, 24, 1024, 600), 'inv-2024-revuelto-acheso', [1024, 640]),
  (S+'huracan-perf-spyder-2018.jpg', (0, 24, 1024, 600), 'inv-2018-huracan-performante-spyder', [1024, 640]),
  (S+'urus-2022.jpg', (0, 24, 1024, 600), 'inv-2022-urus', [1024, 640]),
]
os.makedirs(OUT, exist_ok=True)
for src, box, stem, widths in JOBS:
    im = Image.open(src).convert('RGB')
    if box: im = im.crop(box)
    for w in widths:
        w2 = min(w, im.width)
        h2 = round(im.height * w2 / im.width)
        r = im.resize((w2, h2), Image.LANCZOS)
        r.save(f'{OUT}{stem}-{w2}.webp', 'WEBP', quality=78, method=6)
        r.save(f'{OUT}{stem}-{w2}.jpg', 'JPEG', quality=80, optimize=True, progressive=True)
        print(stem, w2, h2)
