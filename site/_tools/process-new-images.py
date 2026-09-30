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

# ---- Hero rebuild (Alex, 30 Sep 2026: "take several good images from the folder") ----
# Slide 1 (dealer), landscape + portrait tablets: img8, yellow Revuelto between factory buildings, whole frame
im = Image.open(SRC + 'img8.webp').convert('RGB')
export(im, 'hero-dealer-revuelto', [2560, 1920, 1280], jpg_widths=(1920, 1280))
# Slide 2 (Temerario): gallery2 cropped so the Sant'Agata sign leaves the frame (sign ends at x 333)
im = Image.open(SRC + 'gallery2-desktop.webp').convert('RGB')
export(im.crop((400, 150, 2560, 1365)), 'slide-temerario-sagata', [1920, 1280], jpg_widths=(1920, 1280))
export(im.crop((1050, 300, 2000, 1420)), 'slide-temerario-sagata-p', [950, 800], jpg_widths=(800,))
# Slide 3 (Revuelto), landscape: img6 aerial, whole frame (portrait crop exported above)
im = Image.open(SRC + 'img6.webp').convert('RGB')
export(im, 'slide-revuelto-aerial', [2560, 1920, 1280], jpg_widths=(1920, 1280))
# Slide 4 (Urus SE), landscape: official lamborghini.com Urus SE gallery frame, orange Urus SE on red rocks at sunset
im = Image.open('research/press-images/urus-se_rocks-sunset-orange_2560x1440.jpg').convert('RGB')
export(im, 'slide-urus-se-rocks', [2560, 1920, 1280], jpg_widths=(1920, 1280))

# Slide 1 (dealer), landscape: Alex's own edit of img8 ("slide 1d.jpg", 1920x1080): car shifted right, left side darkened
im = Image.open(SRC + 'slide 1d.jpg').convert('RGB')
export(im, 'hero-dealer-alex', [1920, 1280], jpg_widths=(1920, 1280))

# Ad Personam (30 Sep 2026, Alex): personalization.webp (1744x1000), Revuelto interior.
# Landscape: the whole frame. Portrait: the steering wheel + centre console column (x 12-58%).
im = Image.open(SRC + 'personalization.webp').convert('RGB')
export(im, 'adp-cabin-rv-l', [1744, 1280], jpg_widths=(1744, 1280))
W, H = im.size
export(im.crop((round(W * 0.12), 0, round(W * 0.58), H)), 'adp-cabin-rv-p', [802, 600], jpg_widths=(802, 600))
