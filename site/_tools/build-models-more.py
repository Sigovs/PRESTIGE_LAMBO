"""Builds the other model pages on the model template (Alex, 6 Nov 2026; client sheet rows 34-44): model-<slug>.html for
the Huracán, Urus, Aventador, Limited Series and Lanzador pages the demo carried in its own layout. Shell: model-revuelto.html
(head, header, menu, footer, scripts; model_v3.css / model_v3.js) plus model_more_v3.css. Data: _tools/models_more.py.
Photos: _tools/process-models-more.py (run it first; its manifest gives the widths). Run _tools/menu-models.py after,
so the menu links these pages.

    python _tools/build-models-more.py"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import models_more as M

SITE = Path(__file__).resolve().parents[1]
SHELL = (SITE / 'model-revuelto.html').read_text(encoding='utf8')
MAN = json.loads((Path(__file__).resolve().parent / 'models_more_manifest.json').read_text())
DEMO = json.loads((M.RES / 'demo.json').read_text(encoding='utf8'))
SRP = (SITE / 'srp.html').read_text(encoding='utf8')
CONFIG = 'https://configurator.lamborghini.com/'
ZOOM = '<span class="mzoom" aria-hidden="true"><svg class="icon"><use href="#i-expand"/></svg></span>'
ARROW = '<svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>'
EXT = '<svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg>'
ALL = {p['slug']: p for p in M.PAGES + M.FAMILIES + M.SPECIAL}
NAMES = {'urus-se': 'Urus SE', 'urus-se-performante': 'Urus SE Performante', **{s: p['name'] for s, p in ALL.items()}}


def configurator(page):
    for s in DEMO.get(page['src'], {}).get('sections', []):
        for l in s['links']:
            if l.startswith('Configure yours -> '):
                return html.escape(l.split(' -> ', 1)[1])
    return CONFIG


def pic(slug, role, sizes, alt, cls='', eager=False, portrait=False, widths=None):
    w = widths or MAN[f'{slug}-{role}']
    webp = ', '.join(f'assets/img/models/{slug}-{role}-{x}.webp {x}w' for x in w)
    jpg = ', '.join(f'assets/img/models/{slug}-{role}-{x}.jpg {x}w' for x in w)
    p = ''
    if portrait:
        pw = MAN[f'{slug}-{role}-p'][-1]
        p = f'\n                    <source media="(max-width: 767.98px) and (orientation: portrait)" type="image/webp" srcset="assets/img/models/{slug}-{role}-p-{pw}.webp">'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<picture>{p}
                    <source type="image/webp" srcset="{webp}" sizes="{sizes}">
                    <img{f' class="{cls}"' if cls else ''} src="assets/img/models/{slug}-{role}-{w[-1]}.jpg" srcset="{jpg}" sizes="{sizes}" {load} decoding="async" alt="{alt}">
                </picture>'''


def is_sentence(t):
    return t.rstrip().endswith(('.', '!', '?', '”', '"'))


def cards(slug, prefix, lst):
    out = []
    for i, (_n, text, alt) in enumerate(lst, 1):
        role = f'{prefix}{i}'
        label = text if text and not is_sentence(text) else alt.rstrip('.')
        cap = ''
        if text:
            cap = (f'<figcaption class="mcard__cap"><span class="mcard__text">{text}</span></figcaption>' if is_sentence(text)
                   else f'<figcaption class="mcard__cap"><span class="mcard__title">{text}</span></figcaption>')
        out.append(f'''
            <figure class="mcard">
                <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/{slug}-{role}-{MAN[f'{slug}-{role}'][-1]}.webp" aria-label="Open photo: {html.escape(label)}">
                    {pic(slug, role, '(min-width: 1024px) 30vw, (min-width: 768px) 45vw, 100vw', alt)}
                    {ZOOM}
                </button>
                {cap}
            </figure>''')
    n = len(lst)
    return f'''
    <div class="container mstory__cards mstory__cards--{3 if n >= 3 else 2}{' mstory__cards--one' if n == 1 else ''}">{''.join(out)}
    </div>''' if lst else ''


def hero(page):
    s, name = page['slug'], page['name']
    claim = f'\n        <p class="mbig__claim">{page["claim"]}</p>' if page.get('claim') else ''
    lead = f'\n        <p class="mbig__lead">{page["lead"]}</p>' if page.get('lead') else ''
    inv = f'\n            <a class="btn btn--tertiary" href="srp.html?model={page["inv"][0]}"><span>View inventory</span></a>' if page.get('inv') else ''
    return f'''
<!-- ============================ 1 · THE MODEL ============================ -->
<section class="mbig" aria-labelledby="model-title">
    <div class="mbig__media">
                {pic(s, 'hero', '100vw', f'The Lamborghini {name}.', 'mbig__img', True).replace('<picture>', f'<picture>{chr(10)}                    <source media="(max-width: 767.98px) and (orientation: portrait)" type="image/webp" srcset="assets/img/models/{s}-hero-p-{MAN[s + "-hero-p"][-1]}.webp">', 1)}
    </div>
    <div class="container mbig__inner">
        <p class="t-eyelet mbig__eyelet">Lamborghini Miami</p>
        <h1 class="mbig__name" id="model-title">{name}</h1>{claim}{lead}
        <div class="mbig__actions">
            <a class="btn btn--accent" href="#inquire"><span>Inquire</span>{ARROW}</a>
            <a class="btn btn--secondary" href="{configurator(page)}" rel="noopener"><span>Configure yours</span>{EXT}</a>{inv}
        </div>
    </div>
</section>
'''


def intro(text, legal='', eyelet='Overview', heading=None, band='black'):
    head = f'\n            <h2 class="t-banner mintro__title" id="intro-title">{heading}</h2>' if heading else ''
    lab = 'aria-labelledby="intro-title"' if heading else f'aria-label="{eyelet}"'
    leg = f'\n            <p class="t-legal mintro__legal">{legal}</p>' if legal else ''
    return f'''
<!-- ============================ OVERVIEW ============================
     The client's overview, full width (sheet: "a lot of empty space next to text ... made full width"). -->
<section class="mintro band band--{band}" {lab}>
    <div class="container mintro__inner">
        <p class="t-eyelet section-head__eyelet">{eyelet}</p>{head}
        <p class="mintro__text">{text}</p>{leg}
    </div>
</section>
'''


def figures(page):
    s, name = page['slug'], page['name']
    nums = ''.join(f'''
                <div class="mnum__item"><dt class="mnum__label">{lab}</dt><dd class="mnum__value">{v}<span class="mnum__unit">{u}</span></dd></div>''' for v, u, lab in page['nums'])
    inv = f'\n            <a class="btn btn--tertiary" href="srp.html?model={page["inv"][0]}"><span>View {page["inv"][0]} inventory</span></a>' if page.get('inv') else ''
    return f'''
<!-- ============================ 2 · FIGURES ============================ -->
<section class="mnum band band--dark" aria-labelledby="facts-title">
    <div class="container mnum__grid">
        <header class="mnum__head">
            <p class="t-eyelet section-head__eyelet">{name}</p>
            <h2 class="t-banner" id="facts-title">In figures</h2>
        </header>
        <dl class="mnum__list">{nums}
        </dl>
        <figure class="mnum__media">
            {pic(s, 'num', '(min-width: 1024px) 45vw, 100vw', f'The Lamborghini {name}.')}
        </figure>
        <p class="t-legal mnum__src">As published by Automobili Lamborghini; power and speed in US units.</p>
        <div class="mcta__row mnum__cta">
            <a class="btn btn--secondary" href="{configurator(page)}" rel="noopener"><span>Configure yours</span>{EXT}</a>{inv}
        </div>
    </div>
</section>
'''


def story(page, key, eyelet, heading, text, band, wide=None, main=None, card_list=(), card_prefix='c', legal='', ctas='', long=False, sid=None):
    s = page['slug']
    sid = sid or key
    head_cls = 'mstory__head mstory__head--long' if long else 'mstory__head'
    media = ''
    if wide:
        role, alt = wide
        media = f'''
    <figure class="mstory__wide">
        <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/{s}-{role}-{MAN[f'{s}-{role}'][-1]}.webp" aria-label="Open photo: {html.escape(alt.rstrip('.'))}">
            {pic(s, role, '100vw', alt, '', False, True)}
            {ZOOM}
        </button>
    </figure>'''
    if main:
        role, alt = main
        media = f'''
    <div class="container">
        <figure class="mstory__main">
            <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/{s}-{role}-{MAN[f'{s}-{role}'][-1]}.webp" aria-label="Open photo: {html.escape(alt.rstrip('.'))}">
                {pic(s, role, '(min-width: 1440px) 1320px, 100vw', alt)}
                {ZOOM}
            </button>
        </figure>
    </div>'''
    leg = f'\n    <div class="container"><p class="t-legal mstory__legal">{legal}</p></div>' if legal else ''
    row = f'\n    <div class="container mcta__row">{ctas}\n    </div>' if ctas else ''
    return f'''
<!-- ============================ {heading.upper()} ============================ -->
<section class="mstory band band--{band}{' mstory--flush' if wide and not (card_list or legal or ctas) else ''}" id="{sid}" aria-labelledby="{sid}-title" data-gallery>
    <div class="container {head_cls}">
        <div>
            <p class="t-eyelet section-head__eyelet">{eyelet}</p>
            <h2 class="t-banner" id="{sid}-title">{heading}</h2>
        </div>
        <p class="t-lead mstory__text">{text}</p>
    </div>{media}{cards(s, card_prefix, card_list)}{leg}{row}
</section>
'''


def tiles(page, models=None, eyelet=None, heading='Models'):
    items = []
    for slug in models or page['models']:
        name = NAMES[slug]
        if slug in ALL:
            img = pic(slug, 'tile', '(min-width: 1280px) 25vw, (min-width: 768px) 50vw, 100vw', f'The Lamborghini {name}.')
        else:   # a page of the current range: its own hero frame
            img = pic(slug, 'hero', '(min-width: 1280px) 25vw, (min-width: 768px) 50vw, 100vw', f'The Lamborghini {name}.', widths=[1000, 1600])
        items.append(f'''
            <li>
                <a class="mtile" href="model-{slug}.html">
                    <span class="mtile__media">{img}</span>
                    <span class="mtile__name">{name}</span>
                    <span class="mtile__more">Explore the model<svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></span>
                </a>
            </li>''')
    lead = f'\n            <p class="t-lead mtiles__lead">{page["models_lead"]}</p>' if page.get('models_lead') else ''
    return f'''
<!-- ============================ MODELS ============================
     The family's models, as the site's dark photo tiles (the demo's white cut-out cards with the name baked in are gone). -->
<section class="mtiles band band--black" id="models" aria-labelledby="models-title">
    <div class="container">
        <header class="section-head mtiles__head"><div>
            <p class="t-eyelet section-head__eyelet">{eyelet or page['name']}</p>
            <h2 class="t-banner" id="models-title">{heading}</h2>{lead}
        </div></header>
        <ul class="mtiles__grid mtiles__grid--{len(items)}">{''.join(items)}
        </ul>
    </div>
</section>
'''


def gallery(page):
    s, g = page['slug'], page.get('gallery') or []
    if not g:
        return ''
    n = len(g)
    items = ''.join(f'''
            <li class="mgal__item mgal__item--{i}">
                <button class="mgal__open" type="button" data-gal-open="{i - 1}" data-full="assets/img/models/{s}-g{i}-{MAN[f'{s}-g{i}'][-1]}.webp" aria-label="Open photo {i} of {n}: {alt}">
                    {pic(s, f'g{i}', '(min-width: 1024px) 50vw, 100vw', alt)}
                    {ZOOM}
                </button>
            </li>''' for i, (_f, alt) in enumerate(g, 1))
    return f'''
<!-- ============================ GALLERY ============================ -->
<section class="mgal band band--dark" aria-labelledby="gal-title">
    <div class="container">
        <header class="section-head"><div>
            <p class="t-eyelet section-head__eyelet">{page['name']}</p>
            <h2 class="t-banner" id="gal-title">Gallery</h2>
        </div></header>
        <ol class="mgal__grid mgal__grid--{n}" data-gallery>{items}
        </ol>
    </div>
</section>
<!-- gallery lightbox: one photo at a time, ← → / swipe / Esc; model_v3.js -->
<dialog class="glb" aria-label="{page['name']} gallery" data-gallery-box data-lenis-prevent>
    <figure class="glb__stage">
        <img class="glb__img" alt="" data-glb-img>
        <figcaption class="glb__cap"><span class="glb__n" data-glb-n>1 / {n}</span> <span data-glb-cap></span></figcaption>
    </figure>
    <button class="glb__btn glb__btn--prev" type="button" data-glb-prev aria-label="Previous photo"><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    <button class="glb__btn glb__btn--next" type="button" data-glb-next aria-label="Next photo"><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    <button class="glb__close" type="button" data-glb-close aria-label="Close gallery"><svg class="icon" aria-hidden="true"><use href="#i-close"/></svg></button>
</dialog>
'''


# films the demo embeds that YouTube refuses (403: private or not embeddable, checked 6 Nov 2026): left out
DEAD_FILMS = {'7ztOTUO_Mcs', 'aGE3MzZrHw0', 'C74Hq3HVD0Y'}
POSTER = {'MTQB1nQ4mEw': 'sddefault', 'DUvkXmg28F4': 'sddefault'}   # no maxres frame for these two
# the picture inside each poster, without its letterbox bars: the frame takes it until Play
POSTER_RATIO = {'YibwDv52Jjc': '2.4', '_TDrGgwM58A': '2.35', 'R98KsxKs6Q4': '2.35', 'MTQB1nQ4mEw': '2.4', 'DUvkXmg28F4': '2.37'}


def film(page):
    vid = M.YT.get(page['src'])
    if not vid or vid in DEAD_FILMS:
        return ''
    return f'''
<!-- ============================ FILM ============================
     The film the client's page embeds (YouTube); it loads only on Play. -->
<section class="mmedia band band--black" id="film" aria-label="{page['name']}, film">
    <div class="container">
            <div class="mfilm" data-yt="{vid}" data-yt-title="Lamborghini {page['name']}"{f' style="--poster-ratio: {POSTER_RATIO[vid]}"' if vid in POSTER_RATIO else ''}>
                <img class="mfilm__poster" src="https://i.ytimg.com/vi/{vid}/{POSTER.get(vid, 'maxresdefault')}.jpg" width="1280" height="720" loading="lazy" decoding="async" alt="">
                <button class="mfilm__play" type="button" data-yt-play aria-label="Play the Lamborghini {page['name']} film (YouTube)">
                    <svg class="icon" aria-hidden="true"><use href="#i-play"/></svg><span>Watch the film</span>
                </button>
            </div>
    </div>
</section>
'''


def compare(sec):
    head = ''.join(f'<th scope="col">{c}</th>' for c in sec['head'])
    rows = ''.join('<tr>' + ''.join(f'<td data-col="{html.escape(sec["head"][i])}">{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in sec['rows'])
    return f"""
<!-- ============================ AT A GLANCE ============================
     The client's comparison, as a table; on phones each row reads as a short list. -->
<section class="mcompare band band--black" aria-labelledby="compare-title">
    <div class="container">
        <header class="section-head"><div>
            <p class="t-eyelet section-head__eyelet">{sec['eyelet']}</p>
            <h2 class="t-banner" id="compare-title">{sec['heading']}</h2>
        </div></header>
        <table class="mcompare__table">
            <thead><tr>{head}</tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
</section>
"""


def quote(text):
    return f'''
<!-- ============================ QUOTE ============================ -->
<section class="mquote band band--black" aria-label="Quote">
    <div class="container">
        <blockquote class="mquote__text"><p>{text}</p></blockquote>
    </div>
</section>
'''


def cta(page):
    if page.get('cta') is False:
        return ''
    c = page.get('cta')
    name = page['name']
    if c:
        eyelet, title, conf = c['eyelet'], c['heading'], c['configure']
    else:
        eyelet, title, conf = 'Lamborghini Miami', f'<span class="svc-line">Your {name}</span> <span class="svc-line">starts here</span>', 'Configure yours'
    return f'''
<!-- ============================ CTA BAND ============================ -->
<section class="mcta band band--black" aria-labelledby="cta-title">
    <div class="container mcta__grid">
        <div>
            <p class="t-eyelet section-head__eyelet">{eyelet}</p>
            <h2 class="t-banner mcta__title" id="cta-title">{title}</h2>
            <p class="t-lead mcta__lead">Talk to our sales team on Biscayne Boulevard.</p>
        </div>
        <div class="mcta__actions">
            <a class="btn btn--accent" href="#inquire"><span>Inquire</span>{ARROW}</a>
            <a class="btn btn--secondary" href="tel:+18332905147"><span>Call (833) 290-5147</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-phone"/></svg></a>
            <a class="btn btn--tertiary" href="{configurator(page)}" rel="noopener"><span>{conf}</span></a>
        </div>
    </div>
</section>
'''


def inventory(page):
    if not page.get('inv'):
        return ''
    fam, rx = page['inv']
    cards_ = []
    for li in re.findall(r'<li data-year[^>]*data-model="' + fam + r'"[^>]*>.*?</article>', SRP, flags=re.S):
        g = lambda pat: (re.search(pat, li, re.S) or [None, ''])[1]
        title = g(r'<h3 class="vehicle-card__name">([^<]*)</h3>')
        if not re.search(rx, title):
            continue
        img = g(r'srcset="(assets/img/inv/[^ "]+-640\.webp)')
        miles = g(r'ph-gauge[^<]*</i><span>([^<]*)</span>')
        ext = g(r'Exterior</span><span class="vehicle-card__detail-value">([^<]*)<')
        price = g(r'class="vehicle-card__price">([^<]*)<')
        stock = g(r'Stock</span><span class="vehicle-card__detail-value">([^<]*)<')
        cond = g(r'data-cond="([^"]*)"')
        cards_.append(f'''            <li class="minv__card">
                <a class="minv__link" href="vdp.html">
                    <img src="{img}" width="640" height="480" loading="lazy" decoding="async" alt="{title}, {ext}">
                    <span class="minv__cond">{cond}</span>
                    <span class="minv__name">{title}</span>
                    <span class="minv__meta">{ext} · {miles} · Stock {stock}</span>
                    <span class="minv__price">{price}</span>
                </a>
            </li>''')
    if not cards_:
        return ''
    return f'''
<!-- ============================ IN STOCK ============================
     Read from srp.html at build time; each opens its vehicle page. -->
<section class="minv band band--dark" id="in-stock" aria-labelledby="inv-title">
    <div class="container">
        <header class="minv__head">
            <div>
                <p class="t-eyelet section-head__eyelet">Lamborghini Miami</p>
                <h2 class="t-banner" id="inv-title">In our inventory</h2>
            </div>
            <a class="btn btn--secondary" href="srp.html?model={fam}"><span>View all {fam} inventory</span>{ARROW}</a>
        </header>
        <ol class="minv__grid">
{chr(10).join(cards_[:6])}
        </ol>
    </div>
</section>
'''


def body(page):
    s = page['slug']
    out = hero(page)
    if page in M.PAGES:
        out += intro(page['intro'], page.get('intro_legal', ''))
        out += figures(page)
        e, i = page['ext'], page['int']
        out += story(page, 'exterior', 'Exterior', 'Design', e['text'], 'black', wide=('ext', e['alt']), card_list=e['cards'], card_prefix='c',
                     legal=e.get('legal', ''), ctas=f'\n        <a class="btn btn--secondary" href="{configurator(page)}" rel="noopener"><span>Choose your colour</span>{EXT}</a>\n        <a class="btn btn--tertiary" href="ad-personam.html"><span>Ad Personam personalization</span></a>')
        out += story(page, 'interior', 'Interior', 'The cockpit', i['text'], 'dark', main=('int', i['alt']), card_list=i['cards'], card_prefix='ic',
                     ctas=f'\n        <a class="btn btn--accent" href="#inquire"><span>Book a viewing</span>{ARROW}</a>\n        <a class="btn btn--tertiary" href="{configurator(page)}" rel="noopener"><span>Design your interior</span></a>')
    elif page in M.FAMILIES:
        out += intro(page['intro'])
        d = page['design']
        out += story(page, 'exterior', page['name'], 'Design', d['text'], 'dark', wide=('ext', d['alt']), card_list=d.get('cards', []), card_prefix='c')
        out += tiles(page)
    else:
        for sec in page['sections']:
            if sec['kind'] == 'intro':
                out += intro(sec['text'], eyelet=sec['eyelet'], heading=sec.get('heading'))
            elif sec['kind'] == 'quote':
                out += quote(sec['text'])
            elif sec['kind'] == 'compare':
                out += compare(sec)
            elif sec['kind'] == 'tiles':
                out += tiles(page, sec['models'], sec['eyelet'], sec['heading'])
            else:
                k = sec['key']
                link = sec.get('link')
                ctas = f'\n        <a class="btn btn--secondary" href="{link[1]}"><span>{link[0]}</span>{ARROW}</a>' if link else ''
                out += story(page, k, sec['eyelet'], sec['heading'], sec['text'], sec['band'],
                             wide=('w-' + k, sec['wide'][2]) if sec.get('wide') else None,
                             main=('m-' + k, sec['main'][2]) if sec.get('main') else None,
                             card_list=sec.get('cards', []), card_prefix=f'{k}-c', long=sec.get('long', False), ctas=ctas)
    out += gallery(page) + film(page) + cta(page) + inventory(page)
    return out


OPTIONS = ['Revuelto', 'Revuelto SV', 'Temerario', 'Urus SE', 'Urus SE Performante', 'Huracán', 'Huracán Sterrato', 'Huracán Tecnica', 'Huracán STO',
           'Huracán EVO Spyder', 'Urus', 'Urus S', 'Urus Performante', 'Aventador', 'Limited Series', 'Countach LPI 800-4', 'Concept', 'Lanzador', 'Other']


def page_html(page):
    s, name = page['slug'], page['name']
    form = re.search(r'<!-- =+ \d+ · INQUIRE =+.*?</section>\n', SHELL, re.S).group(0)
    form = form.replace('<span class="svc-line">the Revuelto</span>', f'<span class="svc-line">{page.get("form_title") or "the " + name}</span>')
    pick = page.get('option') or name
    opts = '\n'.join(f'                                    <option{" selected" if o == pick else ""}>{o}</option>' for o in OPTIONS)
    form = re.sub(r'(<select class="field__input field__select" id="enq-model" name="model">).*?(\s*</select>)', lambda m: m.group(1) + '\n' + opts + m.group(2), form, flags=re.S)
    form = form.replace('about the Revuelto.', f'about {page.get("form_title") or "the " + name}.').replace('Configure your Revuelto', 'Configure your Lamborghini' if page.get('form_title') else f'Configure your {name}')
    form = form.replace('href="https://configurator.lamborghini.com/" rel="noopener">\n                    <span>Configure your', f'href="{configurator(page)}" rel="noopener">\n                    <span>Configure your')
    assert 'Revuelto</option>' in form and 'the Revuelto' not in form, s
    main = f'<main id="main">\n{body(page)}\n{form}\n</main>'
    out = re.sub(r'<main id="main">.*?</main>', lambda m: main, SHELL, count=1, flags=re.S)
    desc = html.escape(page.get('desc') or DEMO.get(page['src'], {}).get('desc') or f'The Lamborghini {name} at Lamborghini Miami, North Miami Beach, FL.')
    out = re.sub(r'<title>.*?</title>', f'<title>Lamborghini {name} | Lamborghini Miami, North Miami Beach, FL</title>', out, count=1)
    out = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', out, count=1)
    out = out.replace('<!-- GENERATED by _tools/build-model-pages.py: edit the template there, not this file. -->',
                      '<!-- GENERATED by _tools/build-models-more.py (data: _tools/models_more.py): edit it there, not this file. -->')
    hw = MAN[f'{s}-hero']
    pre = (f'\n    <link rel="stylesheet" href="assets/css/model_more_v3.css?v=4">'
           f'\n    <link rel="preload" as="image" type="image/webp" media="(min-width: 768px), (orientation: landscape)" imagesrcset="'
           + ', '.join(f'assets/img/models/{s}-hero-{w}.webp {w}w' for w in hw) + '" imagesizes="100vw" fetchpriority="high">')
    out = re.sub(r'(<link rel="stylesheet" href="assets/css/model_v3\.css\?v=\d+">)', lambda m: m.group(1) + pre, out, count=1)
    out = out.replace(' aria-current="page"', '')
    for needle in ('model_more_v3.css', f'<h1 class="mbig__name" id="model-title">{name}</h1>', 'id="inquire"'):
        assert needle in out, (s, needle)
    return out


for p in M.PAGES + M.FAMILIES + M.SPECIAL:
    f = SITE / f"model-{p['slug']}.html"
    f.write_text(page_html(p), encoding='utf8', newline='\n')
    print(f.name, len(f.read_text(encoding='utf8')))
