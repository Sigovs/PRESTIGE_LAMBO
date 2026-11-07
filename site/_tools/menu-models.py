"""Menu: every model, by family, in the Models column (Alex, 6 Nov 2026, concept A with drop-downs: the column lists the
families; a click opens that family's models under it, one family at a time, the other columns never move. Client sheet rows 3-4 and Kirsten: the old multi-level drop-down was "too messy").

    python _tools/menu-models.py

Families and models follow the client's model tree (lamborghinimiami.aandemo.com, read 6 Nov 2026), with the
current range first. Models with a page of ours link to it; the others to the client's own page on
lamborghinimiami.com. Idempotent: the Models column is rebuilt on every run, the earlier models block under the
columns is removed, and the Vehicles column keeps only the inventory.
Styles: assets/css/menu_models.css. Behaviour: assets/js/menu_models.js (after the page's main_v2/3/4.js)."""
import re
from pathlib import Path
SITE = Path(__file__).resolve().parent.parent
LIVE = 'https://www.lamborghinimiami.com'
CSS_V, JS_V = 7, 1   # the models with a page of ours link to it (all but Concept since 6 Nov 2026)
FAMILIES = [
    ('revuelto', 'Revuelto', [('model-revuelto.html', 'Revuelto'), ('model-revuelto-sv.html', 'Revuelto SV')]),
    ('temerario', 'Temerario', [('model-temerario.html', 'Temerario')]),
    ('urus', 'Urus', [('model-urus-se.html', 'Urus SE'), ('model-urus-se-performante.html', 'Urus SE Performante'),
                      ('model-urus.html', 'Urus'), ('model-urus-s.html', 'Urus S'), ('model-urus-performante.html', 'Urus Performante')]),
    ('huracan', 'Huracán', [('model-huracan.html', 'Huracán'), ('model-huracan-sterrato.html', 'Huracán Sterrato'), ('model-huracan-tecnica.html', 'Huracán Tecnica'),
                            ('model-huracan-sto.html', 'Huracán STO'), ('model-huracan-evo-spyder.html', 'Huracán EVO Spyder')]),
    ('aventador', 'Aventador', [('model-aventador.html', 'Aventador')]),
    ('limited', 'Limited Series', [('model-limited-series.html', 'Limited Series'), ('model-countach-lpi-800-4.html', 'Countach LPI 800-4')]),
    ('concept', 'Concept', [('model-concept.html', 'Concept'), ('model-lanzador.html', 'Lanzador')]),
    ('marine', 'Marine', [('tecnomar63.html', 'Tecnomar for Lamborghini 63')]),
]
CHEV = '<svg class="icon menu__fam-chev" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'


def column(page):
    cur = lambda href: ' aria-current="page"' if href == page else ''
    fams = ''.join(f'''
                    <li class="menu__fam-item">
                        <button class="menu__link menu__fam" type="button" data-models-fam aria-expanded="false" aria-controls="menu-models-{k}"{' data-current' if any(h == page for h, _ in ms) else ''}>{n}{CHEV}</button>
                        <div class="menu__fam-drop" id="menu-models-{k}"><ul class="menu__fam-list">{''.join(f"""
                            <li><a class="menu__model" href="{h}"{cur(h)}>{t}</a></li>""" for h, t in ms)}
                        </ul></div>
                    </li>''' for k, n, ms in FAMILIES)
    return f'''
            <div class="menu__col menu__col--models" data-menu-models>
                <p class="menu__head">Models</p>
                <ul class="menu__list">{fams}
                </ul>
            </div>'''


PAGES = [p for p in SITE.glob('*.html') if p.name not in ('index.html', 'index_v2.html', 'index_v3.html')]
for path in sorted(PAGES):
    s = path.read_text(encoding='utf8')
    if 'menu__head">Vehicles' not in s:
        continue
    o = s
    # earlier versions: a Models column inside the main columns, and the models block under them
    s = re.sub(r'\s*<div class="menu__col menu__col--models"[^>]*>.*?</ul>\s*</div>(?=\s*<div class="menu__col">\s*<p class="menu__head">Vehicles)', '', s, flags=re.S)
    s = re.sub(r'\n\s*<nav class="menu__models" aria-label="Models">.*?</nav>', '', s, flags=re.S)
    # the Vehicles column keeps the inventory only
    m = re.search(r'(<div class="menu__col">\s*<p class="menu__head">Vehicles</p>\s*<ul class="menu__list">)(.*?)(\s*</ul>)', s, re.S)
    assert m, path.name
    items = re.findall(r'\s*<li>.*?</li>', m.group(2), re.S)
    keep = [li for li in items if not re.search(r'href="(index_v4\.html)?#range"|href="model-', li)]
    s = s[:m.start()] + m.group(1) + ''.join(keep) + m.group(3) + s[m.end():]
    # the Models column, first of the four
    s, k = re.subn(r'(<nav class="menu__cols" aria-label="Site">)', lambda mm: mm.group(1) + column(path.name), s, count=1)
    assert k == 1, path.name
    if 'menu_models.css' not in s:
        s, k = re.subn(r'(<link rel="stylesheet" href="assets/css/main_v\d\.css\?v=\d+">)', r'\1\n    <link rel="stylesheet" href="assets/css/menu_models.css?v=0">', s, count=1)
        assert k == 1, path.name
    s = re.sub(r'menu_models\.css\?v=\d+', f'menu_models.css?v={CSS_V}', s)
    if 'menu_models.js' not in s:
        s, k = re.subn(r'(<script src="assets/js/main_v\d\.js\?v=\d+" defer></script>)', r'\1\n<script src="assets/js/menu_models.js?v=0" defer></script>', s, count=1)
        assert k == 1, path.name
    s = re.sub(r'menu_models\.js\?v=\d+', f'menu_models.js?v={JS_V}', s)
    if s != o:
        path.write_text(s, encoding='utf8', newline='')
    print(path.name, len(keep), 'inventory items')
