"""Tecnomar for Lamborghini 63: the client's own photographs and wordmark from lamborghinimiami.aandemo.com/tecnomar63/
(read 6 Nov 2026), into assets/img/models/tecnomar-<role>-<width>. Never upscaled: each width is capped at the source's."""
from pathlib import Path
from PIL import Image
S = Path(__file__).resolve().parents[1]
SRC = S.parent / 'research/images-current-site/tecnomar'
OUT = S / 'assets/img/models'
JOBS = {
    # role: (source, widths, crop box or None)
    'hero': ('122-T365-LP-F4444.jpg', (1000, 1600, 1920), None),
    'hero-p': ('131-T365-LP-F0045_edit.jpg', (660,), (544, 0, 1204, 880)),   # authored phone frame: the stern at dusk, Miami behind
    'exterior': ('126-DSC_5863-Modifica-Edit-scaled-e1649084275496.jpg', (1000, 1320), None),
    'ext-bow': ('125-prove-1.jpg', (800, 1200), None),
    'ext-hardtop': ('128-T365-LP-F3768.jpg', (800, 1200), None),
    'ext-hull': ('127-DSC_5987_EDIT-e1649084286150.jpg', (800, 1200), None),
    'interior': ('132-T365-LP-F0066-1.jpg', (1000, 1600, 1920), None),
    'interior-p': ('132-T365-LP-F0066-1.jpg', (700,), (560, 0, 1260, 880)),
    'int-cabin': ('124-PROVA-02.jpg', (800, 1200), None),
    'int-start': ('123-PROVA-03.jpg', (800, 1200), None),
    'gallery-1': ('133-DE8A1924x_EDIT-scaled-e1649673517695.jpg', (900, 1600), None),
    'gallery-2': ('130-T365-LP-F0040-italy.jpg', (900, 1600), None),
    'gallery-3': ('131-T365-LP-F0045_edit.jpg', (900, 1244), None),
    'gallery-4': ('121-prova-3.jpg', (900, 1600), None),
    'gallery-5': ('129-DSC_6020-Modifica-scaled-e1648573636348.jpg', (900, 1600), None),
    'gallery-6': ('122-T365-LP-F4444.jpg', (900, 1600), None),
}
for role, (src, widths, box) in JOBS.items():
    im = Image.open(SRC / src).convert('RGB')
    if box:
        im = im.crop(box)
    for w in widths:
        w = min(w, im.width)
        r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f'tecnomar-{role}-{w}.jpg', quality=84, optimize=True, progressive=True)
        r.save(OUT / f'tecnomar-{role}-{w}.webp', quality=80, method=6)
    print(role, im.size, widths)
# the wordmark: white on transparent, kept as a PNG and a WebP
logo = Image.open(SRC / '120-tecnomar-w.png').convert('RGBA')
logo.save(S / 'assets/img/tecnomar-wordmark.png', optimize=True)
logo.save(S / 'assets/img/tecnomar-wordmark.webp', quality=90, method=6)
print('wordmark', logo.size)
