"""Photos for the other model pages (_tools/models_more.py) -> assets/img/models/<slug>-<role>-<w>.{jpg,webp}.
Sources: research/images-current-site/models/<demo slug>/NN-*.jpg (the demo's and lamborghini.com's, gitignored).
Crops to the model template's own proportions (the hero stays whole, the CSS covers it; the band 2.4:1, the cockpit
1.89:1, the figures frame 1.744:1, the phone frames 0.655:1 and 1.36:1), at each photo's focal point. Never upscales.
Writes _tools/models_more_manifest.json: the widths actually written, which the page builder reads.

    python _tools/process-models-more.py [slug ...]"""
import json
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import models_more as M

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / 'assets' / 'img' / 'models'
MAN = Path(__file__).resolve().parent / 'models_more_manifest.json'
man = json.loads(MAN.read_text()) if MAN.exists() else {}


def src(page, n):
    f = sorted((M.RES / page['src']).glob(f'{n:02d}-*'))
    assert f, (page['slug'], n)
    return Image.open(f[0]).convert('RGB')


def crop(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    if w / h > ratio:                      # too wide: cut the sides around fx
        cw = round(h * ratio); x = min(max(round(w * fx - cw / 2), 0), w - cw)
        return im.crop((x, 0, x + cw, h))
    ch = round(w / ratio); y = min(max(round(h * fy - ch / 2), 0), h - ch)
    return im.crop((0, y, w, y + ch))


def save(slug, role, im, widths):
    done = []
    for w in widths:
        if w > im.width:
            continue
        done.append(w)
    if not done or max(done) < min(im.width, max(widths)):
        done.append(min(im.width, max(widths)))     # the source's own width when it falls between the steps
    done = sorted(set(done))
    for w in done:
        r = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f'{slug}-{role}-{w}.jpg', quality=82, optimize=True, progressive=True)
        r.save(OUT / f'{slug}-{role}-{w}.webp', quality=80, method=6)
    man[f'{slug}-{role}'] = done
    return done


def fit(page, role, im, ratio):
    """a source taller than its frame is cut here, at its focal point (models_more.FOCUS), not centred by the CSS"""
    if im.width / im.height >= ratio - 0.15:
        return im
    return crop(im, ratio, 0.5, M.FOCUS.get((page['slug'], role), 0.5))


def band(page, role, n, fy, fx=0.5):
    im = src(page, n)
    save(page['slug'], role, crop(im, 2.4, fx, fy), (1440, 2160))
    save(page['slug'], role + '-p', crop(im, 750 / 551, fx, fy), (750,))


def main_frame(page, role, n, fy=0.5, fx=0.5):
    im = src(page, n)
    save(page['slug'], role, crop(im, 2400 / 1267, fx, fy), (1000, 1600, 2400))
    save(page['slug'], role + '-p', crop(im, 786 / 1200, fx, fy), (786,))


def run(page):
    s = page['slug']
    n, fx = page['hero']
    im = src(page, n)
    save(s, 'hero', im, (1000, 1600, 2400))
    save(s, 'hero-p', crop(im, 786 / 1200, fx), (786,))
    save(s, 'tile', crop(im, 1.744, fx), (800, 1200))          # its tile on the family page
    if page.get('num'):
        n, fy = page['num']
        save(s, 'num', crop(src(page, n), 1.744, 0.5, fy), (800, 1200))
    for key in ('ext', 'design'):
        e = page.get(key)
        if e:
            band(page, 'ext', *e['img'])          # (file, fy[, fx for the phone frame])
            for i, c in enumerate(e.get('cards', []), 1):
                save(s, f'c{i}', fit(page, f'c{i}', src(page, c[0]), 1.744), (800, 1200))
    if page.get('int'):
        main_frame(page, 'int', *page['int']['img'])
        for i, c in enumerate(page['int']['cards'], 1):
            save(s, f'ic{i}', fit(page, f'ic{i}', src(page, c[0]), 1.744), (800, 1200))
    for sec in page.get('sections', []):
        if sec['kind'] != 'story':
            continue
        if sec.get('wide'):
            band(page, 'w-' + sec['key'], sec['wide'][0], sec['wide'][1])
        if sec.get('main'):
            main_frame(page, 'm-' + sec['key'], sec['main'][0], sec['main'][1])
        for i, c in enumerate(sec.get('cards', []), 1):
            save(s, f'{sec["key"]}-c{i}', fit(page, f'{sec["key"]}-c{i}', src(page, c[0]), 1.744), (800, 1200))
    for i, (n, _alt) in enumerate(page.get('gallery', []), 1):
        save(s, f'g{i}', fit(page, f'g{i}', src(page, n), 16 / 9), (900, 1600))
    print(s, 'done')


want = set(sys.argv[1:])
for p in M.PAGES + M.FAMILIES + M.SPECIAL:
    if not want or p['slug'] in want:
        run(p)
MAN.write_text(json.dumps(man, indent=1, sort_keys=True))
