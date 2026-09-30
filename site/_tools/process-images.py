"""Derive web images for site/assets/img from research originals (originals untouched).
Run from the project root:  python3 site/_tools/process-images.py
Each job: source, crop box (left, top, right, bottom) or None, output stem, widths.
Crops remove the stamped 'Lamborghini Miami' shield watermark or inventory footer band where noted."""
import os
from PIL import Image
R = 'research/images-current-site/'
S = 'research/inventory-capture-2026-09-30/photos/'
P = 'research/press-images/'
OUT = 'site/assets/img/'
JOBS = [
  # hero: Temerario front 3/4, dark studio (no watermark)
  (R+'hero/hero_temerario-blue-front-3q-dark_1920x707.jpg', None, 'hero-temerario', [1920, 1440, 960]),
  (R+'hero/hero_temerario-blue-front-3q-dark_1920x707.jpg', (760, 40, 1920, 707), 'hero-temerario-m', [1160, 780]),
  # Ad Personam, full-bleed peak. Two authored crops, both clear of the bottom-right shield watermark:
  # landscape keeps the whole windscreen band as the text field; portrait centres the wheel with dark bands above and below.
  (R+'models/urus-se/urus-se_interior-dashboard-orange_5000x3333.jpg', (0, 0, 5000, 2800), 'adp-cabin-l', [2560, 1920, 1440, 1024]),
  (R+'models/urus-se/urus-se_interior-dashboard-orange_5000x3333.jpg', (800, 600, 2800, 3333), 'adp-cabin-p', [1200, 900, 600]),
  # Models band: official lamborghini.com side profiles (all face left, full length) — one image system
  (P+'revuelto_side-profile-orange_2160x533.jpg', None, 'model-revuelto', [1296, 960, 648]),
  (P+'temerario_side-profile-blue_2160x533.jpg', None, 'model-temerario', [1296, 960, 648]),
  (P+'urus-se_side-profile-orange_2160x533.jpg', None, 'model-urus-se', [1296, 960, 648]),
  (P+'urus-se-performante_side-profile-lime_1440x355.jpg', None, 'model-urus-se-performante', [1296, 960, 648]),
  # Mobile hero: yellow Temerario, night track — portrait phones only; crop centred on the car (x 950-2450)
  (P+'temerario_front-3q-yellow-night-track_2560x1463.jpg', (950, 0, 2450, 1463), 'hero-temerario-night-p', [1400, 1000, 750]),
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
  (S+'huracan-2015.jpg', (0, 24, 1024, 600), 'inv-2015-huracan-lp610-4', [1024, 640]),
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
