"""Build the inventory MOCKUPS for developer handoff: srp.html and vdp.html (2024 Revuelto, CJ2602).

Round 4 (Alex, 16 Oct 2026): the pages are the latest Prestige SRP/VDP — their own markup and
layout CSS — with the Lamborghini header, footer, fonts and colours, and only the client's
changes (click-to-call on "Call for price", the two CTAs, bold in the VDP description).
  * markup: <main> of prestige-final/srp_v2.html and vdp_v2.html, data substituted (below)
  * layout CSS: prestige-extract-srp.css / -vdp.css — the rules of Prestige's own stylesheets that
    those pages use, pulled in the browser by extract-prestige-css.js, scoped to .pi; this script
    renames their custom properties to --pi-* and writes assets/css/prestige_srp.css / _vdp.css
  * Lamborghini layer: assets/css/inventory_pi.css (scoped to .pi; theme, type, components)
  * behaviour: Prestige's own JS (prestige_srp.js = search5.js, two marked patches;
    prestige_vdp.js = vdp.js) plus inventory_pi.js (lead dialog, photo stage)
Run from the project root:  python3 site/_tools/build-inventory-mockups.py
Data: research/inventory-capture-live (captured 30 Sep 2026)."""
import html, json, re, os
from PIL import Image

ROOT = 'site/'
CAP = 'research/inventory-capture-live/'
IMG = ROOT + 'assets/img/inv/'
os.makedirs(IMG, exist_ok=True)
E = html.escape

cars = {v['stock']: v for v in json.load(open(CAP + 'vehicles.json'))}
# only cars with photographs (Alex, 19 Oct 2026): CJ2626, CJ2627, CJ2632 and 86230X have none yet
cars = {k: v for k, v in cars.items() if os.path.exists(f'{CAP}photos/{k}-1.jpg')}
SRP_STOCKS = None  # set below: all cars with photographs, recently listed first
_OLD_SRP = ['CJ2630', 'CJ2626', 'CJ2622', '10918', '10914', '10881A',
              '85991Z', '86198X', 'CJ2602', '86180', '86104X', '86065X']   # recently listed first
VDP_STOCK = 'CJ2602'
TOTAL = len(cars)


# ---------- data ----------
def vdp_html(stock):
    return open(f'{CAP}raw/vdp/{stock}.html', encoding='utf-8', errors='ignore').read()

def block(s, cls, stop=None):
    m = re.search(r'<div[^>]*class="[^"]*\b' + cls + r'\b', s)
    seg = s[m.start():]
    if stop: seg = seg[:seg.find(stop)]
    return re.sub(r'<(script|style)[\s\S]*?</\1>', '', seg)

def info(stock):
    t = re.sub(r'<[^>]+>', '\n', block(vdp_html(stock), 'mod-vehicle-info')[:60000])
    lines = [html.unescape(x).strip() for x in t.split('\n') if x.strip()]
    keys = ['Drivetrain', 'Cylinders', 'Displacement', 'Doors']
    return {l: lines[i + 1] for i, l in enumerate(lines) if l in keys and i + 1 < len(lines)}

def model_name(v):
    model = {'Huracan': 'Huracán'}.get(v['model'], v['model'])
    trim = '' if v['trim'] in ('.', '', None) else ' ' + v['trim']
    return f"{v['year']} Lamborghini {model}{trim}"

def engine(i):
    return f"{float(i['Displacement']):.1f}L V{i['Cylinders']}" if i.get('Cylinders') else '—'

def price(v):
    m = re.search(r'\$[\d,]+', v['price_displayed'] or '')
    return m.group(0) if m else None

def miles(v): return f"{v['mileage']:,} mi"


# ---------- images: 16:9 card crops, above the shield bug (y >= 683 on the 1024x768 frames) ----------
def card_image(stock):
    src = f'{CAP}photos/{stock}-1.jpg'
    if not os.path.exists(src): return None
    im = Image.open(src).convert('RGB').crop((0, 80, 1024, 656))
    for w in (1024, 640):
        r = im.resize((w, round(576 * w / 1024)), Image.LANCZOS)
        r.save(f'{IMG}{stock.lower()}-{w}.webp', 'WEBP', quality=82, method=6)
        r.save(f'{IMG}{stock.lower()}-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    return f'assets/img/inv/{stock.lower()}'


# ---------- shared chrome from service.html ----------
svc = open(ROOT + 'service.html', encoding='utf-8').read()
home = open(ROOT + 'index_v2.html', encoding='utf-8').read()
SPRITE = re.search(r'<svg class="sprite"[\s\S]*?</svg>', home).group(0).replace('</svg>', '''    <symbol id="i-chevron-down" viewBox="0 0 24 24"><path d="m5 9 7 7 7-7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square"/></symbol>
    <symbol id="i-sliders" viewBox="0 0 24 24"><path d="M3 7h11M18 7h3M3 17h3M10 17h11M16 4v6M8 14v6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square"/></symbol>
</svg>''')
CHROME_TOP = svc[svc.index('<a class="skip-link"'):svc.index('<main id="main">')]
CHROME_FOOT = svc[svc.index('<!-- ============================ FOOTER'):svc.index('</footer>') + len('</footer>')]
for a, b in [(' aria-current="page"', ''),
             ('href="index_v2.html#new"', 'href="srp.html?condition=new"'),
             ('href="index_v2.html#pre-owned"', 'href="srp.html?condition=used"'),
             ('href="srp.html#new"', 'href="srp.html?condition=new"'),
             ('href="srp.html#used"', 'href="srp.html?condition=used"'),
             ('href="#request" data-menu-link', 'href="service.html#request"'),
             ('href="#request"', 'href="service.html#request"'),
             ('href="https://www.lamborghinimiami.com/lamborghini-miami-fl"', 'href="srp.html"'),
             ('>Contact</a>', '>Contact</a>')]:
    CHROME_TOP = CHROME_TOP.replace(a, b)
    CHROME_FOOT = CHROME_FOOT.replace(a, b)
CHROME_TOP = CHROME_TOP.replace('<a class="site-header__link site-header__contact" href="service.html#request">',
                                '<a class="site-header__link site-header__contact" href="index_v2.html#visit">')


# ---------- Prestige layout CSS: custom properties renamed to --pi-*, emptied declarations dropped ----------
PI_VARS = ['bg', 'bg-soft', 'bg-deep', 'cream', 'ink', 'ink-soft', 'ink-muted', 'header-bg', 'rule', 'rule-strong',
           'font-display', 'font-sans', 'sp-1', 'sp-2', 'sp-3', 'sp-4', 'sp-5', 'sp-6', 'sp-7', 'sp-8', 'section-py',
           'header-h', 'srp-header-h', 'ease', 'pop', 'container-max', 'container-wide', 'surface-card', 'card-ease',
           'card-dur', 'card-lift', 'w-standard', 'srp-pop']
for kind in ('srp', 'vdp'):
    css = open(f'{ROOT}_tools/prestige-extract-{kind}.css', encoding='utf-8').read()
    css = re.sub(r'var\(--(' + '|'.join(sorted(PI_VARS, key=len, reverse=True)) + r')\b', r'var(--pi-\1', css)
    css = re.sub(r'\s*transition-(?:property|duration|timing-function|delay):\s*;', '', css)
    open(f'{ROOT}assets/css/prestige_{kind}.css', 'w', encoding='utf-8').write(
        f"/* GENERATED from site/_tools/prestige-extract-{kind}.css by build-inventory-mockups.py.\n"
        f"   Prestige's own layout rules for the {kind.upper()}, scoped to .pi; custom properties as --pi-*\n"
        f"   (their Lamborghini values are set in inventory_pi.css). Do not edit by hand. */\n" + css)


def page(title, desc, body, kind):
    return f'''<!doctype html>
<html lang="en-US">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{E(title)}</title>
    <meta name="description" content="{E(desc)}">
    <meta name="theme-color" content="#000000">
    <link rel="icon" href="assets/img/bull.svg" type="image/svg+xml">
    <script>
        /* ?figma = static capture mode: no Lenis, every image eager (as index_v2.html). */
        if (/[?&]figma\\b/.test(location.search)) {{
            document.documentElement.classList.add('figma');
            document.addEventListener('DOMContentLoaded', () => {{
                document.querySelectorAll('img[loading="lazy"]').forEach((img) => {{ img.loading = 'eager'; }});
            }});
        }} else {{
            document.documentElement.classList.add('js');
        }}
    </script>
    <!-- DEVELOPER MOCKUP (Lamborghini Miami inventory). Generated by site/_tools/build-inventory-mockups.py;
         edit the generator, not this file. Form submission is SIMULATED (no endpoint). -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wdth,wght@8..144,25..151,100..1000&display=swap">
    <!-- Prestige's icon set (Phosphor), as on the Prestige pages -->
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/thin/style.css">
    <link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css">
    <link rel="stylesheet" href="https://unpkg.com/lenis@1.3.26/dist/lenis.css">
    <link rel="stylesheet" href="assets/css/tokens_v2.css?v=103">
    <link rel="stylesheet" href="assets/css/main_v2.css?v=104">
    <link rel="stylesheet" href="assets/css/forms_v2.css?v=1">
    <link rel="stylesheet" href="assets/css/prestige_{kind}.css?v=1">
    <link rel="stylesheet" href="assets/css/inventory_pi.css?v=17">
</head>
<body class="page-inventory page-{kind}">

{SPRITE}

{CHROME_TOP}
<main id="main">
{body}
</main>

{CHROME_FOOT}

{LEAD_DIALOG}

<script src="https://unpkg.com/lenis@1.3.26/dist/lenis.min.js" defer></script>
<script src="assets/js/main_v2.js?v=105" defer></script>
<script src="assets/js/forms_v2.js?v=1" defer></script>
<script src="assets/js/prestige_{kind}.js?v=2" defer></script>
<script src="assets/js/inventory_pi.js?v=4" defer></script>
</body>
</html>
'''


def field(id_, label, typ='text', req=True, auto='', extra=''):
    r = ' <span class="field__req">(required)</span>' if req else ''
    a = f' autocomplete="{auto}"' if auto else ''
    rq = ' required' if req else ''
    return f'''<div class="field">
                            <label class="field__label" for="{id_}">{label}{r}</label>
                            <input class="field__input" id="{id_}" name="{id_.split('-')[1]}" type="{typ}"{a}{rq}{extra} aria-describedby="{id_}-err">
                            <p class="field__error" data-no-rise id="{id_}-err" hidden></p>
                        </div>'''

LEAD_DIALOG = f'''<!-- ============================ LEAD DIALOG ============================
     Opened by "Check availability" and "Schedule consultation" (cards and VDP). One form, two
     kinds; the kind and the vehicle travel as hidden fields. Fields and consent wording follow
     the Prestige forms. No endpoint yet (data-endpoint=""): the request is confirmed locally. -->
<dialog class="lead" id="lead" aria-labelledby="lead-title" data-lenis-prevent>
    <div class="lead__head">
        <div>
            <p class="t-eyelet lead__kind" data-lead-kind>Check availability</p>
            <h2 class="lead__title" id="lead-title" data-lead-vehicle>2024 Lamborghini Revuelto</h2>
            <p class="lead__stock" data-lead-stock>Stock CJ2602</p>
        </div>
        <button class="lead__close" type="button" data-lead-close aria-label="Close">
            <svg class="icon" aria-hidden="true"><use href="#i-close"/></svg>
        </button>
    </div>
    <form class="form lead__form" id="lead-form" action="#" method="post" novalidate data-lead-form data-endpoint="" data-done="#lead-done"
          data-fail="Your request could not be sent. Please try again, or call sales on (833) 290-5147.">
        <input type="hidden" name="request" value="availability" data-lead-field="request">
        <input type="hidden" name="vehicle" value="" data-lead-field="vehicle">
        <input type="hidden" name="stock" value="" data-lead-field="stock">
        <input type="hidden" name="vin" value="" data-lead-field="vin">
        <div class="form__summary" data-no-rise role="alert" tabindex="-1" hidden data-form-summary></div>
        <div class="form__row">
            {field('lead-first', 'First name', auto='given-name')}
            {field('lead-last', 'Last name', auto='family-name')}
        </div>
        <div class="form__row">
            {field('lead-email', 'Email', 'email', auto='email')}
            {field('lead-phone', 'Phone', 'tel', auto='tel', extra=' inputmode="tel"')}
        </div>
        <fieldset class="field segmented">
            <legend class="field__label">Preferred contact <span class="field__req">(required)</span></legend>
            <div class="segmented__opts">
                <label class="segmented__opt"><input type="radio" name="prefer" value="call" checked><span>Call</span></label>
                <label class="segmented__opt"><input type="radio" name="prefer" value="text"><span>Text</span></label>
                <label class="segmented__opt"><input type="radio" name="prefer" value="email"><span>Email</span></label>
            </div>
        </fieldset>
        <div class="form__row" data-lead-only="consultation" hidden>
            <div class="field">
                <label class="field__label" for="lead-date">Preferred date</label>
                <input class="field__input" id="lead-date" name="date" type="date" disabled>
            </div>
            <div class="field">
                <label class="field__label" for="lead-time">Preferred time</label>
                <select class="field__input field__select" id="lead-time" name="time" disabled>
                    <option value="">Any time</option>
                    <option>Morning</option>
                    <option>Afternoon</option>
                    <option>Evening</option>
                </select>
            </div>
        </div>
        <div class="field">
            <label class="field__label" for="lead-message">Message</label>
            <textarea class="field__input field__textarea" id="lead-message" name="message" rows="4" data-lead-field="message"></textarea>
        </div>
        <div class="field field--consent">
            <label class="check check--consent">
                <input class="check__input" type="checkbox" name="consent" value="yes" id="lead-consent" required aria-describedby="lead-consent-err">
                <span class="check__box" aria-hidden="true"></span>
                <span class="check__label">Please note that by completing this form, you agree to being contacted via text, phone and email. <span class="field__req">(required)</span></span>
            </label>
            <p class="field__error" data-no-rise id="lead-consent-err" hidden></p>
        </div>
        <div class="form__foot">
            <button class="btn btn--accent form__submit" type="submit" data-form-submit>
                <span data-submit-label>Send request</span>
                <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
            </button>
            <p class="form__status" data-no-rise role="status" aria-live="polite" data-form-status></p>
        </div>
    </form>
    <div class="form-done lead__done" id="lead-done" tabindex="-1" hidden data-form-done data-no-rise>
        <p class="t-title form-done__title">Thank you<span data-done-name></span>.</p>
        <p class="t-lead form-done__text">Our sales team will contact you about this car, Monday to Friday 9:00 am – 7:00 pm and Saturday 10:00 am – 6:00 pm. To speak to someone now, call <a class="spec__link" href="tel:+18332905147">(833) 290-5147</a>.</p>
        <p class="t-legal lead__mock">Developer mockup: submission is simulated. Nothing was sent; the form has no endpoint yet.</p>
        <button class="btn btn--primary btn--md" type="button" data-lead-close><span>Close</span></button>
    </div>
</dialog>'''

# =====================================================================================
# PRESTIGE MARKUP, LAMBO DATA
# The <main> of each page is Prestige's own (prestige-final/srp_v2.html, vdp_v2.html, the build
# the AAN demo runs), wrapped in <main class="pi"> so the copied Prestige CSS is scoped to it.
# Only data, links and the three client changes are substituted; the deltas the AAN demo has
# over the prototype are applied too (keyword search; two card CTAs; no Certified block on a
# car that is not certified).
# =====================================================================================

def prestige_main(name):
    s = open(os.path.join(os.path.abspath('.'), '..', '_______PRESTIGE TO PREVIEW', 'prestige-final', name), encoding='utf-8').read()
    i = s.index('<main'); j = s.index('</main>')
    inner = s[s.index('>', i) + 1:j]
    cls = re.search(r'<main class="([^"]+)"', s[i:i + 60]).group(1)
    return cls, inner

def sub1(s, pattern, repl, flags=re.S):
    out, n = re.subn(pattern, repl, s, count=1, flags=flags)
    assert n == 1, pattern[:80]
    return out

def card_photo(stock):
    """4:3 card photo — the studio frame as shot (Prestige's card media is 463:347, i.e. 4:3)."""
    src = f'{CAP}photos/{stock}-1.jpg'
    if not os.path.exists(src): return None
    im = Image.open(src).convert('RGB')
    for w in (1024, 640):
        r = im.resize((w, round(768 * w / 1024)), Image.LANCZOS)
        r.save(f'{IMG}{stock.lower()}-43-{w}.webp', 'WEBP', quality=82, method=6)
        r.save(f'{IMG}{stock.lower()}-43-{w}.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    return f'assets/img/inv/{stock.lower()}-43'

def media_img(v, sizes):
    p = card_photo(v['stock'])
    name = model_name(v)
    if not p:   # no photographs yet (the demo shows its "Coming soon" frame here; Lambo shows its plate)
        return f'''<span class="vehicle-card__plate"><span class="vehicle-card__plate-name">{E(v['model'])}</span><span class="vehicle-card__plate-note">Photography in preparation</span></span>'''
    return f'''<picture><source type="image/webp" srcset="{p}-640.webp 640w, {p}-1024.webp 1024w" sizes="{sizes}"><img src="{p}-640.jpg" srcset="{p}-640.jpg 640w, {p}-1024.jpg 1024w" sizes="{sizes}" width="1024" height="768" alt="{E(name)}" loading="lazy"></picture>'''

def lead_data(v):
    return f'data-vehicle="{E(model_name(v))}" data-stock="{E(v["stock"])}" data-vin="{E(v["vin"])}"'

def price_block_pi(v, label_cls='vehicle-card__price-label', value_cls='vehicle-card__price'):
    p = price(v)
    if p:
        return f'''<span class="{label_cls}">Sale Price</span>
                                <span class="{value_cls}">{p}</span>'''
    # client, 16 Oct 2026: "Call for price" is click-to-call (sales line)
    return f'''<span class="{label_cls}">Price</span>
                                <a class="{value_cls} price-call" href="tel:+18332905147" aria-label="Call for price, sales (833) 290-5147">Call for Price</a>'''

COLOUR = {'Nero': 'Black', 'Grigio': 'Grey', 'Giallo': 'Yellow', 'Rosso': 'Red', 'Blu': 'Blue', 'Verde': 'Green', 'Oro': 'Gold'}
FACETS = {
    'year':   lambda v: str(v['year']),
    'make':   lambda v: 'Lamborghini',
    'model':  lambda v: {'Huracan': 'Huracán'}.get(v['model'], v['model']),
    'trim':   lambda v: None if v['trim'] in ('.', '') else v['trim'],
    'engine': lambda v: engine(info(v['stock'])),
    'body':   lambda v: 'SUV' if v['model'] == 'Urus' else 'Spyder' if 'Spyder' in (v['trim'] or '') else 'Coupe',
    'colour': lambda v: COLOUR.get((v['exteriorColor'] or 'x').split()[0], 'Not listed'),
    'trans':  lambda v: 'Automatic',
    'drive':  lambda v: 'All-wheel drive',
    'cond':   lambda v: 'New' if v['condition_site'] == 'New' else 'Pre-owned',
}
def card_data(v):
    p = price(v)
    d = {k: (f(v) or '') for k, f in FACETS.items()}
    d.update({'price': p[1:].replace(',', '') if p else '', 'miles': v['mileage'], 'date': v['dateInStock'],
              'text': ' '.join(str(x) for x in [model_name(v), v['stock'], v['vin'], v['exteriorColor'], v['interiorColor']] if x).lower()})
    return ' '.join(f'data-{k}="{E(str(val))}"' for k, val in d.items())

def srp_card(v):
    i = info(v['stock'])
    name = model_name(v)
    trans = (v['transmission'] or '').capitalize()
    return f'''                <li {card_data(v)}>
                    <article class="vehicle-card vehicle-card--extended">
                        <div class="vehicle-card__media">
                            <a class="vehicle-card__media-link" href="vdp.html" tabindex="-1" aria-hidden="true">{media_img(v, '(min-width: 1100px) 30vw, (min-width: 760px) 46vw, 100vw')}</a>
                            <div class="vehicle-card__actions" aria-label="Quick actions">
                                <button class="vehicle-card__action" type="button">
                                    <i class="ph ph-heart" aria-hidden="true"></i><span>Save</span>
                                </button>
                                <button class="vehicle-card__action" type="button">
                                    <i class="ph ph-share-network" aria-hidden="true"></i><span>Share</span>
                                </button>
                                <button class="vehicle-card__action" type="button">
                                    <i class="ph ph-chat-circle" aria-hidden="true"></i><span>Text</span>
                                </button>
                            </div>
                        </div>
                        <div class="vehicle-card__body">
                            <a href="vdp.html" class="vehicle-card__heading-link">
                                <h3 class="vehicle-card__name">{E(name)}</h3>
                            </a>
                            <ul class="vehicle-card__specs">
                                <li class="spec"><i class="ph ph-gauge" aria-hidden="true"></i><span>{miles(v)}</span></li>
                                <li class="spec"><i class="ph ph-gear-six" aria-hidden="true"></i><span>{E(trans)}</span></li>
                            </ul>
                            <ul class="vehicle-card__details">
                                <li><span class="vehicle-card__detail-label">Exterior</span><span class="vehicle-card__detail-value">{E(v['exteriorColor'] or '—')}</span></li>
                                <li><span class="vehicle-card__detail-label">Interior</span><span class="vehicle-card__detail-value">{E(v['interiorColor'] or '—')}</span></li>
                                <li><span class="vehicle-card__detail-label">Engine</span><span class="vehicle-card__detail-value">{E(engine(i))}</span></li>
                                <li><span class="vehicle-card__detail-label">Stock</span><span class="vehicle-card__detail-value">{E(v['stock'])}</span></li>
                            </ul>
                            <div class="vehicle-card__price-block">
                                {price_block_pi(v)}
                            </div>
                            <div class="vehicle-card__ctas">
                                <button class="btn btn--solid is-accent" type="button" data-lead-open="availability" {lead_data(v)}><span>Check Availability</span></button>
                                <button class="btn" type="button" data-lead-open="consultation" {lead_data(v)}><span>Schedule Consultation</span></button>
                            </div>
                        </div>
                    </article>
                </li>'''

def opt_list(items, name):
    return '\n'.join(f'                            <li><label class="filter__option"><input type="checkbox" name="{name}" value="{E(l)}"> {E(l)} <span class="filter__option-count">{n}</span></label></li>' for l, n in items)

def facet_items(key, order=None):
    c = count_by(FACETS[key])
    return sorted(c.items(), reverse=(key == 'year'))

def count_by(key):
    c = {}
    for v in cars.values():
        k = key(v)
        if k: c[k] = c.get(k, 0) + 1
    return c

def replace_filter_list(main, label, key, title=None):
    """the <ul class="filter__list"> inside the <details class="filter"> whose trigger reads `label`"""
    pat = r'(<span>' + re.escape(label) + r'</span>[\s\S]*?<p class="filter__group-title">)[^<]*(</p>\s*<ul class="filter__list">)[\s\S]*?(</ul>)'
    return sub1(main, pat, lambda m: m.group(1) + (title or label) + m.group(2) + '\n' + opt_list(facet_items(key), key) + '\n                        ' + m.group(3))

def replace_all_col(main, title, key):
    pat = r'(<p class="filter__group-title">' + re.escape(title) + r'</p>\s*<ul class="filter__list">)[\s\S]*?(</ul>)'
    return sub1(main, pat, lambda m: m.group(1) + '\n' + opt_list(facet_items(key), key) + '\n                            ' + m.group(2))

SRP_STOCKS = [v['stock'] for v in sorted(cars.values(), key=lambda v: v['dateInStock'], reverse=True)]

srp_cls, srp = prestige_main('srp_v2.html')
srp = srp.replace('<b>149</b>', f'<b>{TOTAL}</b>')
# AAN demo delta: keyword search above the dropdown row (its markup, as the demo renders it)
srp = sub1(srp, r'(<div class="filter-bar" role="search" aria-label="Refine results">)',
           r'''\1
            <div class="stock_search-outer">
                <div class="stock_search">
                    <input type="text" class="key-search" id="stock" name="stock" placeholder="Search By Keyword" aria-label="Search by keyword">
                    <a href="#" class="stock-btn btn">Search</a>
                </div>
            </div>''')
srp = replace_filter_list(srp, 'Year', 'year')
srp = replace_filter_list(srp, 'Make', 'make')
srp = replace_filter_list(srp, 'Model', 'model', 'Lamborghini models')
srp = replace_filter_list(srp, 'Trim', 'trim')
srp = replace_filter_list(srp, 'Engine', 'engine')
# the New / Pre-owned state the navigation links select (?condition=new|used): a filter in Prestige's own
# markup, kept out of the visible row (the demo has no Condition dropdown); it shows as a chip like any other
srp = sub1(srp, r'(\s*<!-- ALL FILTERS)', lambda m: '''
                <details class="filter" hidden data-condition-filter>
                    <summary class="filter__trigger"><span>Condition</span></summary>
                    <div class="filter__panel">
                        <p class="filter__group-title">Condition</p>
                        <ul class="filter__list">
''' + opt_list(facet_items('cond'), 'cond') + '''
                        </ul>
                    </div>
                </details>''' + m.group(1))
srp = sub1(srp, r'<span class="t-caption">12 of 23</span>', '')
srp = replace_all_col(srp, 'Body style', 'body')
srp = replace_all_col(srp, 'Exterior color', 'colour')
srp = replace_all_col(srp, 'Transmission', 'trans')
srp = replace_all_col(srp, 'Drivetrain', 'drive')
srp = srp.replace('Show 149 results', 'Apply')   # the demo's label
srp = srp.replace('<p class="filter__group-title">Body style</p>', '<p class="filter__group-title">Body</p>').replace('<p class="filter__group-title">Transmission</p>', '<p class="filter__group-title">Trans</p>')   # the demo's group titles
srp = sub1(srp, r'<span class="sort__value">Recently listed</span>', '<span class="sort__value">All</span>')   # as the demo
srp = sub1(srp, r'(<ul class="srp-grid">)[\s\S]*?(</ul>\s*<!-- Pagination -->)',
           lambda m: m.group(1) + '\n' + '\n'.join(srp_card(cars[s]) for s in SRP_STOCKS) + '\n            ' + m.group(2))
srp = sub1(srp, r'(\s*<!-- Pagination -->)', lambda m: '''
            <p class="srp-empty" hidden data-srp-empty>No vehicles match these filters. <button class="chip-clear" type="button" data-srp-clear>Clear all</button></p>''' + m.group(1))
srp = sub1(srp, r'\s*<!-- Pagination -->\s*<nav class="pagination"[\s\S]*?</nav>', '')   # the demo has no pagination: every car on one page
srp = srp.replace('srp_v2.html', 'srp.html').replace('vdp_v2.html', 'vdp.html').replace('index_v2.html', 'index_v2.html')
assert 'assets/images/' not in srp, re.findall(r'assets/images/[^"]+', srp)[:3]


# ---------- VDP ----------
v = cars[VDP_STOCK]
vi = info(VDP_STOCK)
name = model_name(v)
photos = v['photos']
START = 1   # Alex, round 3: the first full-car exterior frame (photo 1 carries the dealer lockup band)

def md_inline(t):   # client: "**text**" renders bold (the platform prints the asterisks today)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', E(t))

raw = block(vdp_html(VDP_STOCK), 'mod-vehicle-comments', 'mod-vehicle-equipment')
raw = re.sub(r'<br\s*/?>', '\n', raw)
lines = [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '', raw)).split('\n') if l.strip()]
lines = [l for l in lines if l.upper() != 'ABOUT THIS VEHICLE' and not l.startswith('<')]
prose = []
for l in lines:   # every line a Prestige t-body paragraph; the only change is "**…**" rendered bold (client)
    prose.append(f'<p class="t-body">{md_inline(l)}</p>')
# MOCKUP INSERTION (client: bold key stats in the description). One staff-style line with a VERIFIED
# figure in the platform's own "**…**" markup, rendered by md_inline like the rest: Revuelto maximum
# combined power 1,015 CV (747 kW), lamborghini.com model page, captured 30 Sep 2026 (DATA_SOURCES,
# "Model range"). No verified torque figure exists in the ledger, so none is shown.
DEMO_LINE = 'Maximum combined power: **1,015 CV (747 kW)**, the manufacturer figure for the Revuelto.'
k = next(i for i, x in enumerate(prose) if 'Groundbreaking Performance' in x) + 2   # after that section's paragraph
prose.insert(k, f'<p class="t-body" data-mockup-insert>{md_inline(DEMO_LINE)}</p>')
prose_html = '\n                        '.join(prose)

eq = block(vdp_html(VDP_STOCK), 'mod-vehicle-equipment')[:80000]
equipment = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip().strip('"') for x in re.findall(r'<li[^>]*>([\s\S]*?)</li>', eq)]
equipment = sorted([x for x in equipment if x], key=lambda x: x.lower().lstrip('"'))   # alphabetical, as the demo lists them
eq_html = '\n'.join(f'                    <li>{E(x)}</li>' for x in equipment)

specs = [('Exterior', v['exteriorColor']), ('Interior', v['interiorColor']), ('Engine', '6.5L V12 plug-in hybrid'),
         ('Transmission', '8-speed dual-clutch'), ('Drivetrain', vi.get('Drivetrain', '—')), ('Mileage', f"{v['mileage']:,} mi"),
         ('Stock', v['stock']), ('VIN', v['vin'])]
spec_html = '\n'.join(f'                    <li><span class="vdp-specs__label">{k}</span><span class="vdp-specs__value">{E(val)}</span></li>' for k, val in specs)

vdp_cls, vdp = prestige_main('vdp_v2.html')
vdp = sub1(vdp, r'<span class="breadcrumb__current" aria-current="page">[^<]*</span>', f'<span class="breadcrumb__current" aria-current="page">{E(name)}</span>')
vdp = sub1(vdp, r'<img src="assets/images/vdp1\.jpg" alt="[^"]*">',
           f'<img src="{photos[START]}" alt="{E(name)} in {E(v["exteriorColor"])}, photograph {START + 1} of {len(photos)}" data-stage-img data-start="{START}" width="1024" height="768">')
vdp = sub1(vdp, r'href="#photos" aria-label="See all 7 photos"', f'href="#photos" aria-label="See all {len(photos)} photos"')
vdp = sub1(vdp, r'(<i class="ph ph-images" aria-hidden="true"></i>) 7 Photos', rf'\1 <span><span data-stage-n>{START + 1}</span> / {len(photos)} Photos</span>')
vdp = sub1(vdp, r'(<h1 class="t-h2 vdp-panel__title">)[^<]*(</h1>)', lambda m: m.group(1) + E(name) + m.group(2))
vdp = sub1(vdp, r'(<div class="vdp-panel__price">)[\s\S]*?(</div>)', lambda m: m.group(1) + f'''
                    <span class="t-eyebrow">Price</span>
                    <span class="t-h3 vdp-panel__price-value">{price(v)}</span>
                ''' + m.group(2))
vdp = sub1(vdp, r'(<ul class="vdp-specs">)[\s\S]*?(</ul>)', lambda m: m.group(1) + '\n' + spec_html + '\n                ' + m.group(2))
# the VDP keeps Prestige's single INQUIRE (the two CTAs are the SRP request); it opens the lead dialog
vdp = sub1(vdp, r'<a href="#" class="btn btn--solid"><span>Inquire</span></a>',
           f'''<button class="btn btn--solid is-accent" type="button" data-lead-open="inquire" {lead_data(v)}><span>Inquire</span></button>''')
# the reports this car's listing offers (CARFAX, AutoCheck, iPacket — all three, as Prestige's bar), in dark-ground variants
# CARFAX: the official value badge the dealer serves for this car (1-Owner); AutoCheck and iPacket: Prestige's
# marks unchanged. All three on white badge tiles of one height (a badge is never recoloured)
vdp = vdp.replace('assets/images/carfax.svg', 'assets/img/pi/carfax-1own.svg').replace('assets/images/autocheck.svg', 'assets/img/pi/autocheck.svg').replace('assets/images/ipacket.svg', 'assets/img/pi/ipacket.svg')
vdp = vdp.replace('alt="CARFAX 1-Owner"', 'alt="Show me the CARFAX — 1 Owner"')
vdp = sub1(vdp, r'<a class="btn btn--solid" href="tel:\+18332906287"><span>\(833\)&nbsp;290-6287</span></a>',
           '<a class="btn btn--solid" href="tel:+18332905147"><span>(833)&nbsp;290-5147</span></a>')
vdp = sub1(vdp, r'<a class="btn" href="#"><span>Start Buying</span></a>', '<a class="btn" href="https://shop.lamborghinimiami.com/" rel="noopener"><span>Start Buying</span></a>')
# AAN demo delta: the Certified block renders only for certified cars; CJ2602 is not certified
vdp = sub1(vdp, r'\s*<!-- ═+ PRESTIGE CERTIFIED[\s\S]*?</section>', '')
vdp = sub1(vdp, r'(<div class="vdp-prose">)[\s\S]*?(</div>\s*</div>\s*</details>)', lambda m: m.group(1) + '\n                        ' + prose_html + '''
                    ''' + m.group(2))   # no disclaimer paragraph: the demo shows only the dealer's text
vdp = sub1(vdp, r'(<ul class="vdp-options">)[\s\S]*?(</ul>)', lambda m: m.group(1) + '\n' + eq_html + '\n                    ' + m.group(2))
vdp = sub1(vdp, r'placeholder="e\.g\. 431,950"', f'placeholder="e.g. {price(v)[1:]}" value="{price(v)[1:]}.00"')   # as the demo: the listing price
vdp = sub1(vdp, r'(<output class="vdp-calc__output" id="calc-loan">)0\.00(</output>)', lambda m: m.group(1) + price(v)[1:] + '.00' + m.group(2))
vdp = sub1(vdp, r'Contact Prestige Imports for current rates and terms\.', 'Contact Lamborghini Miami for current rates and terms.')
vdp = sub1(vdp, r'<span class="vdp-gallery-sec__count">7 photos</span>', f'<span class="vdp-gallery-sec__count">{len(photos)} photos</span>')
vdp = sub1(vdp, r'(<ul class="vdp-photos">)[\s\S]*?(</ul>)', lambda m: m.group(1) + '\n' + '\n'.join(
    f'                <li class="vdp-photos__item"><img src="{u}" alt="{E(name)}, photograph {k + 1} of {len(photos)}" loading="lazy"></li>' for k, u in enumerate(photos)) + '\n            ' + m.group(2))

def related_card(r):
    return f'''                <li>
                    <a href="vdp.html" class="vehicle-card">
                        <div class="vehicle-card__media">
                            {media_img(r, '(min-width: 960px) 30vw, 100vw')}
                        </div>
                        <div class="vehicle-card__body">
                            <h3 class="vehicle-card__name">{'New' if r['condition_site'] == 'New' else 'Used'} {E(model_name(r))}</h3>
                            <ul class="vehicle-card__specs">
                                <li class="spec"><i class="ph ph-gauge" aria-hidden="true"></i><span>{miles(r)}</span></li>
                                <li class="spec"><i class="ph ph-gear-six" aria-hidden="true"></i><span>{(r['transmission'] or '').capitalize()}</span></li>
                            </ul>
                        </div>
                    </a>
                </li>'''
RELATED = ['86180', '10914', 'CJ2630', 'CJ2622', '86198X', '10881A']   # vehicles with photographs
vdp = sub1(vdp, r'(<ul class="vdp-related__track" data-related-track aria-label="Related vehicles">)[\s\S]*?(</ul>\s*<div class="vdp-related__foot">)',
           lambda m: m.group(1) + '\n' + '\n'.join(related_card(cars[s]) for s in RELATED) + '\n            ' + m.group(2))
vdp = vdp.replace('srp_v2.html', 'srp.html').replace('vdp_v2.html', 'vdp.html')
assert 'assets/images/' not in vdp, re.findall(r'assets/images/[^"]+', vdp)[:3]

def wrap(cls, inner):
    return f'''<!-- Prestige markup (prestige-final, the build the AAN demo runs), Lamborghini data and styling.
     .pi scopes the copied Prestige layout CSS (prestige_srp.css / prestige_vdp.css) to this block. -->
<div class="pi" data-no-rise>
<div class="{cls}">
{inner}
</div>
</div>'''

open(ROOT + 'srp.html', 'w', encoding='utf-8').write(page(
    'Lamborghini Inventory | Lamborghini Miami, North Miami Beach, FL',
    'New and pre-owned Lamborghini for sale at Lamborghini Miami, Biscayne Boulevard, North Miami Beach.',
    wrap(srp_cls, srp), 'srp'))
open(ROOT + 'vdp.html', 'w', encoding='utf-8').write(page(
    f'Used {name} for sale | Lamborghini Miami, stock {v["stock"]}',
    f'{name} in {v["exteriorColor"]}, {v["mileage"]:,} mi, at Lamborghini Miami, North Miami Beach.',
    wrap(vdp_cls, vdp), 'vdp'))
print('srp.html, vdp.html written;', len(SRP_STOCKS), 'cards,', len(photos), 'photos,', len(equipment), 'equipment items')
