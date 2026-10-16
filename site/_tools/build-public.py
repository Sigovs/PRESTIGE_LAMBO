"""Build the public preview (GitHub Pages) from site/: the v2 homepage and the service page only.
Run from the project root:  python3 site/_tools/build-public.py
Output: _public/ (gitignored here; it is its own repo, force-pushed to origin main by Alex's decision).

- index_v2.html and service.html are published exactly as they are (Alex, 16 Oct 2026: "as is");
  a root index.html only redirects to index_v2.html
- SIMULATE = True would swap the inventory figures for illustrative ones (kept for later use)
- only the assets the two pages reference are copied"""
SIMULATE = False
import os, re, shutil

SRC, OUT = 'site/', '_public/'

# real -> simulated (homepage inventory cards)
SIM = [
    ('Stock 10918', 'Stock L1042'), ('Stock 10914', 'Stock L1057'),
    ('Stock CJ2602', 'Stock P2611'), ('Stock 86180', 'Stock P2617'), ('Stock CJ2630', 'Stock P2623'),
    ('<dd>24 mi</dd>', '<dd>18 mi</dd>'), ('<dd>37 mi</dd>', '<dd>29 mi</dd>'),
    ('<dd>1,411 mi</dd>', '<dd>2,140 mi</dd>'), ('<dd>187 mi</dd>', '<dd>612 mi</dd>'), ('<dd>537 mi</dd>', '<dd>1,085 mi</dd>'),
    ('$741,697', '$719,900'), ('$651,697', '$664,900'), ('$286,697', '$274,900'),
]
NOTE_RE = re.compile(r'(<p class="t-legal inventory__note">).*?(</p>)', re.S)
NOTE = r'\1Sample listings for this preview: stock numbers, mileage and prices are illustrative and do not describe vehicles for sale. Price and availability subject to change.\2'
VDP_RE = re.compile(r'https://www\.lamborghinimiami\.com/vehicle-details/[^"]+')
SRP = 'https://www.lamborghinimiami.com/lamborghini-miami-fl'
REAL_LEFT = re.compile(r'Stock (10918|10914|CJ2602|86180|CJ2630)|\$(741|651|286),697|vehicle-details/')


def page(src, dst, sim):
    s = open(SRC + src, encoding='utf-8').read()
    if sim:
        for a, b in SIM:
            assert s.count(a) >= 1, a
            s = s.replace(a, b)
        s, n = NOTE_RE.subn(NOTE, s)
        assert n == 1
        s = VDP_RE.sub(SRP, s)
    if sim:
        assert not REAL_LEFT.search(s), REAL_LEFT.search(s).group(0)
    open(OUT + dst, 'w', encoding='utf-8').write(s)
    return s


if os.path.isdir(OUT):
    for name in os.listdir(OUT):                       # keep _public/.git
        if name != '.git':
            p = OUT + name
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
os.makedirs(OUT, exist_ok=True)

html = page('index_v2.html', 'index_v2.html', SIMULATE) + page('service.html', 'service.html', False)
open(OUT + 'index.html', 'w', encoding='utf-8').write(
    '<!doctype html><meta charset="utf-8"><title>Lamborghini Miami</title>'
    '<meta http-equiv="refresh" content="0; url=index_v2.html"><a href="index_v2.html">Lamborghini Miami</a>\n')

# assets referenced by the pages (src, srcset, href, imagesrcset), then by the CSS (url())
refs = set(re.findall(r'assets/[A-Za-z0-9_./-]+', html))
for css in [r for r in refs if r.endswith('.css')]:
    for u in re.findall(r'url\(["\']?\.\./([^"\')]+)', open(SRC + css, encoding='utf-8').read()):
        refs.add('assets/' + u)
missing = []
for r in sorted(refs):
    if not os.path.isfile(SRC + r):
        missing.append(r); continue
    os.makedirs(os.path.dirname(OUT + r), exist_ok=True)
    shutil.copy2(SRC + r, OUT + r)
open(OUT + '.nojekyll', 'w').close()
print(f'{len(refs) - len(missing)} assets copied; missing: {missing or "none"}')
