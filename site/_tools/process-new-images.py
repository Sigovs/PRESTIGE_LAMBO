"""Alex's supplied frames (NEW IMAGES/*.webp, 30 Sep 2026) -> hero slide sizes.
Resize and export only; the portrait frame is a centred crop of the aerial.
Never upscaled. Run from the project root."""
from PIL import Image
SRC = 'NEW IMAGES/'
OUT = 'site/assets/img/'

def export(im, stem, widths, jpg_widths=()):
    for w in widths:
        if w > im.width:
            continue
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(f'{OUT}{stem}-{w}.webp', 'WEBP', quality=80, method=6)
        if w in jpg_widths:
            r.save(f'{OUT}{stem}-{w}.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
        print(stem, w, r.size)

# Slide 3, landscape: Revuelto (yellow) side profile between buildings
im = Image.open(SRC + 'img8.webp').convert('RGB')
export(im, 'slide-revuelto-yellow', [2560, 1920, 1280], jpg_widths=(1920, 1280))

# Slide 3, portrait: the aerial, cropped to the car's column (x 25-75%, full height)
im = Image.open(SRC + 'img6.webp').convert('RGB')
W, H = im.size
crop = im.crop((round(W * 0.25), 0, round(W * 0.75), H))
export(crop, 'slide-revuelto-aerial-p', [1200, 800], jpg_widths=(800,))

# Ad Personam: Revuelto rear detail at sunset (img2)
im = Image.open(SRC + 'img2.webp').convert('RGB')
export(im, 'adp-rear-l', [2560, 1920, 1280], jpg_widths=(1920, 1280))
W, H = im.size
# portrait: the taillight and haunch column, x 40-80% (1024 px), full height
crop = im.crop((round(W * 0.40), 0, round(W * 0.80), H))
export(crop, 'adp-rear-p', [1024, 600], jpg_widths=(1024, 600))
