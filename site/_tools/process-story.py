"""Our Story: the client's 'Our history in pictures' prints (640 x 427, lamborghinimiami.aandemo.com/our-story/,
read 6 Nov 2026). Shown as prints, never enlarged (DESIGN_SYSTEM §6). 1980, 1983 and 1986 are already on disk
as archive-*; the two 2020 frames carry the dealer stamp at the bottom right and are cropped clear of it."""
from pathlib import Path
from PIL import Image
S = Path(__file__).resolve().parents[1]
SRC = S.parent / 'research/images-current-site/our-story'
OUT = S / 'assets/img'
JOBS = {
    '112-22': ('story-1980s', None),
    '114-24': ('story-1985', None),
    '116-26': ('story-1986-opening', None),
    '117-8': ('story-2002', None),
    '118-9': ('story-2020-showroom', (0, 0, 516, 344)),
    '119-10': ('story-2020-brett', (18, 70, 534, 414)),
}
# archive frames with a stamp at the bottom right (2014 signature, 2022 and 2025 shields): cropped clear of it
# (the Sián fills the right of its frame, so 2025 keeps its full width and loses the floor, where the stamp sits)
for base, box in (('archive-2014', (0, 0, 1112, 741)), ('archive-2022', (0, 0, 1112, 741)), ('archive-2025', (150, 0, 1200, 700))):
    im = Image.open(OUT / f'{base}-1280.jpg').convert('RGB')
    w, h = box[2] - box[0], box[3] - box[1]
    for size in (1112, 640):
        c = im.crop(box).resize((size, round(size * h / w)), Image.LANCZOS)
        name = base.replace('archive', 'story')
        c.save(OUT / f'{name}-{size}.jpg', quality=84, optimize=True, progressive=True)
        c.save(OUT / f'{name}-{size}.webp', quality=82, method=6)
    print(base, 'cropped')
for src, (name, box) in JOBS.items():
    im = Image.open(SRC / f'{src}.jpg').convert('RGB')
    if box:
        im = im.crop(box)
    w = im.width
    im.save(OUT / f'{name}-{w}.jpg', quality=84, optimize=True, progressive=True)
    im.save(OUT / f'{name}-{w}.webp', quality=82, method=6)
    print(name, im.size)
