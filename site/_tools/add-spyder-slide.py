#!/usr/bin/env python3
"""Home hero carousel (index_v4.html): the new Temerario Spyder slide (Kirsten, 20 Nov 2026).

    python -X utf8 _tools/add-spyder-slide.py

1. Frame: Alex's own 1920x1080 ("NEW SLIDER/Temerario Spyder hero d.jpg", copied to
   ___OCT changes/sources/models/temerario-spyder/alex_slide_d.jpg): desktop at 1920 and 1280.
   No phone frame: on phones the slide shows the whole 16:9 frame above the copy (as the LFS slide),
   so the car is never cut.
2. The slide sits second, after the opening film. Idempotent: the slide is replaced, never added twice.
3. Every slide is renumbered (ids, "n of N") and the dots are rebuilt from the slides' own labels.
Styles: .hero__slide--spyder in assets/css/main_v4.css."""
import re
from pathlib import Path
from PIL import Image

SITE = Path(__file__).resolve().parent.parent
SRC = SITE.parent / '___OCT changes' / 'sources' / 'models' / 'temerario-spyder' / 'alex_slide_d.jpg'
IMG = SITE / 'assets' / 'img'

im = Image.open(SRC).convert('RGB')          # 1920 x 1080
for w in (1920, 1280):
    r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    r.save(IMG / f'slide-temerario-spyder-{w}.jpg', quality=84, optimize=True, progressive=True)
    r.save(IMG / f'slide-temerario-spyder-{w}.webp', quality=82, method=6)
for old in IMG.glob('slide-temerario-spyder-m-*'):   # the earlier phone crop, no longer used
    old.unlink()
print('frames', im.size)

SLIDE = '''        <article class="hero__slide hero__slide--model hero__slide--spyder hero__slide--bleed" data-slide aria-roledescription="slide" aria-label="2 of 10: Temerario Spyder" id="hero-slide-2">
            <div class="hero__inner container">
                <div class="hero__group">
                    <div class="hero__copy">
                        <p class="hero__eyelet t-eyelet" data-hero-line style="--i:0">Temerario Spyder</p>
                        <h2 class="hero__title hero__title--claim t-display-xl"><span class="hero__line" data-hero-line style="--i:1">Unfiltered</span> <span class="hero__line" data-hero-line style="--i:2">Performance</span></h2>
                        <p class="hero__place hero__figures" data-hero-line style="--i:3">907 hp · 213 mph · 0–62 mph 2.8 s</p>
                    </div>
                    <div class="hero__actions" data-hero-line style="--i:4">
                        <a class="btn btn--primary" href="model-temerario-spyder.html"><span>Explore the model</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
                        <a class="btn btn--secondary" href="model-temerario-spyder.html#inquire"><span>Inquire</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
                    </div>
                </div>
                <!-- 20 Nov 2026 (Kirsten): the new Temerario Spyder, Alex's frame (_tools/add-spyder-slide.py).
                     Phones show the whole 16:9 frame above the copy. Claim and figures as on the model page. -->
                <picture class="hero__media">
                    <source type="image/webp" data-srcset="assets/img/slide-temerario-spyder-1920.webp 1920w, assets/img/slide-temerario-spyder-1280.webp 1280w" sizes="100vw">
                    <img class="hero__img" data-src="assets/img/slide-temerario-spyder-1920.jpg" data-srcset="assets/img/slide-temerario-spyder-1920.jpg 1920w, assets/img/slide-temerario-spyder-1280.jpg 1280w" sizes="100vw" width="1920" height="1080" decoding="async" alt="A blue Lamborghini Temerario Spyder, roof open, in side profile in a blue studio.">
                </picture>
                <div class="hero__scrim" aria-hidden="true"></div>
            </div>
        </article>
'''

page = SITE / 'index_v4.html'
s = page.read_text(encoding='utf-8')
old = re.search(r'\n(\s*<article class="hero__slide[^"]*hero__slide--spyder.*?</article>\n)', s, re.S)
if old:
    s = s[:old.start() + 1] + SLIDE + s[old.end():]
else:
    first = re.search(r'\n(\s*<article class="hero__slide[^"]*hero__slide--opening.*?</article>\n)', s, re.S)
    assert first, 'opening slide not found'
    s = s[:first.end()] + SLIDE + s[first.end():]

# renumber every slide, then rebuild the dots from the slides' labels
arts = list(re.finditer(r'<article class="hero__slide[^>]*>', s))
n = len(arts)
names = []
out, last = [], 0
for i, a in enumerate(arts, 1):
    tag = a.group(0)
    names.append(re.search(r'aria-label="\d+ of \d+: ([^"]*)"', tag).group(1))
    tag = re.sub(r'aria-label="\d+ of \d+: ', f'aria-label="{i} of {n}: ', tag)
    tag = re.sub(r'id="hero-slide-\d+"', f'id="hero-slide-{i}"', tag)
    out.append(s[last:a.start()] + tag)
    last = a.end()
s = ''.join(out) + s[last:]
dots = ''.join(
    f'\n                <li><button class="hero__dot" type="button" data-go="{i}" aria-label="Slide {i + 1} of {n}: {nm}"'
    f'{" aria-current=\"true\"" if i == 0 else ""}><span class="hero__dot-num">{i + 1:02d}</span><span class="hero__dot-bar" aria-hidden="true"><span class="hero__dot-fill"></span></span></button></li>'
    for i, nm in enumerate(names))
s, k = re.subn(r'(<ol class="hero__dots" role="list">).*?(\n\s*</ol>)', lambda mm: mm.group(1) + dots + mm.group(2), s, count=1, flags=re.S)
assert k == 1
# main_v4.css carries .hero__slide--spyder: a new version, so a cached copy is not used
s = re.sub(r'main_v4\.css\?v=413"', 'main_v4.css?v=414"', s)
page.write_text(s, encoding='utf-8', newline='\n')
print(n, 'slides:', ' | '.join(names))
