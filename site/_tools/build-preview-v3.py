#!/usr/bin/env python3
"""v3 client preview package (Oct 2026): every v3 page in one folder, the v3 home served as
index.html, so the client opens one link and never meets v1 / v2 or the old site.

    python3 site/_tools/build-preview-v3.py        (from the project root)

Writes lambo-miami-sl11-v3/ and lamborghini-miami-sl11-v3.zip (same convention as the v1 / v2
packages: Alex uploads it to allautonetwork.com/previews/lambo-miami-sl11-v3/ and overwrites the
same path each time). Only the assets the pages, their CSS and their JS reference are copied.
Big films are not in it: they stream from the client's Dropbox. The notes for Alex
(.dev-note / .dev-notes) are taken out: the client sees the site, not our working notes."""
import os, re, shutil, sys, zipfile

SRC = 'site/'
NAME = 'lambo-miami-sl11-v3'
ZIP = 'lamborghini-miami-sl11-v3.zip'
HOME = 'index.html'
PAGES = {'index_v3.html': 'index.html', 'service.html': 'service.html', 'srp.html': 'srp.html', 'vdp.html': 'vdp.html',
         'contact.html': 'contact.html', 'lifestyle.html': 'lifestyle.html',
         'model-revuelto.html': 'model-revuelto.html', 'model-revuelto-sv.html': 'model-revuelto-sv.html',
         'model-urus-se-performante.html': 'model-urus-se-performante.html',
         'model-temerario.html': 'model-temerario.html', 'model-urus-se.html': 'model-urus-se.html'}
# --page model-revuelto.html: a separate preview that opens on one page (it becomes index.html,
# the home moves to home.html), in its own folder and zip
if '--page' in sys.argv:
    entry = sys.argv[sys.argv.index('--page') + 1]
    slug = entry.replace('.html', '').replace('model-', '')
    NAME, ZIP, HOME = f'lambo-miami-{slug}-preview', f'lamborghini-miami-{slug}-preview.zip', 'home.html'
    PAGES['index_v3.html'] = 'home.html'
    PAGES[entry] = 'index.html'
OUT = NAME + '/'

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

text = ''
for src, dst in PAGES.items():
    s = open(SRC + src, encoding='utf-8').read().replace('index_v3.html', HOME)
    if HOME != 'index.html':
        for a, b in PAGES.items():
            if b == 'index.html':
                s = s.replace(f'href="{a}', 'href="index.html')
    s = re.sub(r'\n?[ \t]*<p class="dev-note"[^>]*>.*?</p>', '', s, flags=re.S)
    s = re.sub(r'\n?<div class="container dev-notes"[^>]*>.*?</div>\n', '\n', s, flags=re.S)
    assert 'Note for Alex' not in s, src
    open(OUT + dst, 'w', encoding='utf-8').write(s)
    text += s

ASSET = re.compile(r'assets/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+')
refs = set(ASSET.findall(text))
seen = set()
while True:   # CSS url(../x) and any assets/ path named inside CSS / JS
    new = set()
    for r in refs - seen:
        seen.add(r)
        if r.endswith(('.css', '.js')) and os.path.isfile(SRC + r):
            body = open(SRC + r, encoding='utf-8').read()
            new |= set(ASSET.findall(body))
            new |= {'assets/' + u for u in re.findall(r'url\(["\']?\.\./([^"\')?#]+)', body)}
    if not new - refs:
        break
    refs |= new
missing = []
for r in sorted(refs):
    if not os.path.isfile(SRC + r):
        missing.append(r)
        continue
    os.makedirs(os.path.dirname(OUT + r), exist_ok=True)
    shutil.copy2(SRC + r, OUT + r)

if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(OUT):
        for f in files:
            if f == '.DS_Store':
                continue
            p = os.path.join(root, f)
            z.write(p, p)
size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f'{len(PAGES)} pages, {len(refs) - len(missing)} assets, {size / 1048576:.1f} MB -> {ZIP}; missing: {missing or "none"}')
