"""Build the inventory MOCKUPS for developer handoff: srp.html (12 real cars) and vdp.html
(one representative VDP: 2024 Revuelto, stock CJ2602). Layout after the latest Prestige demo
(prestigeimports.aandemo.com/current-inventory, 16 Oct 2026); look from the Lamborghini v2 system.
Run from the project root:  python3 site/_tools/build-inventory-mockups.py

Data: research/inventory-capture-live (captured 30 Sep 2026). Card photos are cropped locally
(16:9, clear of the bottom-right shield); the VDP gallery hotlinks the dealer CDN (cdn-ds.com).
Header, menu and footer are taken from service.html so the pages stay in step with it."""
import html, json, re, os
from PIL import Image

ROOT = 'site/'
CAP = 'research/inventory-capture-live/'
IMG = ROOT + 'assets/img/inv/'
os.makedirs(IMG, exist_ok=True)
E = html.escape

cars = {v['stock']: v for v in json.load(open(CAP + 'vehicles.json'))}
SRP_STOCKS = ['CJ2630', 'CJ2626', 'CJ2622', '10918', '10914', '10881A',
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
             ('href="index_v2.html#new"', 'href="srp.html#new"'),
             ('href="index_v2.html#pre-owned"', 'href="srp.html#used"'),
             ('href="#request" data-menu-link', 'href="service.html#request"'),
             ('href="#request"', 'href="service.html#request"'),
             ('href="https://www.lamborghinimiami.com/lamborghini-miami-fl"', 'href="srp.html"'),
             ('>Contact</a>', '>Contact</a>')]:
    CHROME_TOP = CHROME_TOP.replace(a, b)
    CHROME_FOOT = CHROME_FOOT.replace(a, b)
CHROME_TOP = CHROME_TOP.replace('<a class="site-header__link site-header__contact" href="service.html#request">',
                                '<a class="site-header__link site-header__contact" href="index_v2.html#visit">')


def page(title, desc, body, extra_js=''):
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
        /* ?figma = static capture mode: no reveals, no Lenis, every image eager (as index_v2.html). */
        if (/[?&]figma\\b/.test(location.search)) {{
            document.documentElement.classList.add('figma');
            document.addEventListener('DOMContentLoaded', () => {{
                document.querySelectorAll('img[loading="lazy"]').forEach((img) => {{ img.loading = 'eager'; }});
            }});
        }} else {{
            document.documentElement.classList.add('js');
        }}
    </script>
    <!-- MOCKUP for developer handoff (Lamborghini Miami inventory). Generated by
         site/_tools/build-inventory-mockups.py; edit the generator, not this file. -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wdth,wght@8..144,25..151,100..1000&display=swap">
    <link rel="stylesheet" href="https://unpkg.com/lenis@1.3.26/dist/lenis.css">
    <link rel="stylesheet" href="assets/css/tokens_v2.css?v=103">
    <link rel="stylesheet" href="assets/css/main_v2.css?v=104">
    <link rel="stylesheet" href="assets/css/forms_v2.css?v=1">
    <link rel="stylesheet" href="assets/css/inventory_v2.css?v=5">
</head>
<body class="page-inventory">

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
<script src="assets/js/inventory_v2.js?v=2" defer></script>
</body>
</html>
'''


# ---------- the two CTAs (client, 16 Oct 2026; as on the Prestige demo) ----------
def ctas(v, cls=''):
    name = E(model_name(v))
    data = f'data-vehicle="{name}" data-stock="{E(v["stock"])}" data-vin="{E(v["vin"])}"'
    return f'''<div class="lead-ctas{cls}">
                            <button class="btn btn--accent btn--md" type="button" data-lead-open="availability" {data}><span>Check availability</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
                            <button class="btn btn--secondary btn--md" type="button" data-lead-open="consultation" {data}><span>Schedule consultation</span></button>
                        </div>'''


def price_block(v, size=''):
    p = price(v)
    if p:
        return f'''<div class="price{size}">
                            <span class="price__label">Sale price</span>
                            <span class="price__value">{p}</span>
                        </div>'''
    # client, 16 Oct 2026: "Call for price" is click-to-call (sales)
    return f'''<div class="price{size}">
                            <span class="price__label">Price</span>
                            <a class="price__call" href="tel:+18332905147" aria-label="Call for price, sales (833) 290-5147"><span>Call for price</span><svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg></a>
                        </div>'''


def card(v):
    i = info(v['stock'])
    name = model_name(v)
    img = card_image(v['stock'])
    href = 'vdp.html' if v['stock'] == VDP_STOCK else 'vdp.html'   # mockup: every card opens the one VDP
    cond = 'New' if v['condition_site'] == 'New' else 'Pre-owned'
    if img:
        media = f'''<a class="icard__media" href="{href}" tabindex="-1" aria-hidden="true">
                        <picture>
                            <source type="image/webp" srcset="{img}-640.webp 640w, {img}-1024.webp 1024w" sizes="(min-width: 1200px) 410px, (min-width: 768px) 45vw, 100vw">
                            <img src="{img}-640.jpg" srcset="{img}-640.jpg 640w, {img}-1024.jpg 1024w" sizes="(min-width: 1200px) 410px, (min-width: 768px) 45vw, 100vw" width="1024" height="576" loading="lazy" decoding="async" alt="{E(name)} in {E(v['exteriorColor'] or '')}, on the Lamborghini Miami turntable.">
                        </picture>
                        <span class="icard__tag">{cond}</span>
                    </a>'''
    else:
        media = f'''<a class="icard__media icard__media--plate" href="{href}" tabindex="-1" aria-hidden="true">
                        <span class="icard__plate">{E(v['model'])}</span>
                        <span class="icard__plate-note">Photography in preparation</span>
                        <span class="icard__tag">{cond}</span>
                    </a>'''
    rows = [('Exterior', v['exteriorColor'] or '—'), ('Interior', v['interiorColor'] or '—'),
            ('Engine', engine(i)), ('Stock', v['stock'])]
    rows_html = '\n'.join(f'                        <div><dt>{k}</dt><dd>{E(val)}</dd></div>' for k, val in rows)
    pn = pnum(v)
    attrs = {
        'condition': cond, 'year': v['year'], 'model': {'Huracan': 'Huracán'}.get(v['model'], v['model']),
        'trim': '' if v['trim'] in ('.', '') else v['trim'],
        'price': 'call' if pn is None else 'u250' if pn < 250000 else '250-400' if pn <= 400000 else '400',
        'body': 'SUV' if v['model'] == 'Urus' else 'Spyder' if 'Spyder' in (v['trim'] or '') else 'Coupe',
        'colour': COLOUR.get((v['exteriorColor'] or 'x').split()[0], 'Other'),
        'mileage': '1k' if v['mileage'] < 1000 else '10k' if v['mileage'] <= 10000 else 'more', 'drive': 'AWD',
        'sort-price': pn or 0, 'sort-year': v['year'], 'sort-miles': v['mileage'], 'sort-date': v['dateInStock'],
        'text': ' '.join(str(x) for x in [name, v['stock'], v['exteriorColor'], v['interiorColor']] if x).lower()}
    da = ' '.join(f'data-{k}="{E(str(val))}"' for k, val in attrs.items())
    return f'''                <li {da}>
                <article class="icard">
                    {media}
                    <div class="icard__body">
                        <h3 class="icard__title"><a href="{href}">{E(name)}</a></h3>
                        <p class="icard__meta">{miles(v)}<span aria-hidden="true"> · </span>{(v['transmission'] or '').capitalize()}</p>
                        <dl class="icard__rows">
{rows_html}
                        </dl>
                        {price_block(v)}
                        {ctas(v)}
                    </div>
                </article>
                </li>'''


# ---------- lead dialog (one dialog, two kinds; the vehicle is filled in by inventory_v2.js) ----------
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
        <button class="btn btn--primary btn--md" type="button" data-lead-close><span>Close</span></button>
    </div>
</dialog>'''


# ---------- SRP ----------
def options(title, items, name):
    lis = '\n'.join(f'''                            <li><label class="filter__option"><input type="checkbox" name="{name}" value="{E(val)}"><span>{E(lab)}</span><span class="filter__count">{n}</span></label></li>'''
                    for val, lab, n in items)
    return lis

def count_by(key):
    c = {}
    for v in cars.values():
        k = key(v)
        if k: c[k] = c.get(k, 0) + 1
    return c

models = count_by(lambda v: {'Huracan': 'Huracán'}.get(v['model'], v['model']))
years = count_by(lambda v: str(v['year']))
cond = count_by(lambda v: 'New' if v['condition_site'] == 'New' else 'Pre-owned')
trims = count_by(lambda v: None if v['trim'] in ('.', '') else v['trim'])
def pnum(v):
    p = price(v); return int(p[1:].replace(',', '')) if p else None
price_c = count_by(lambda v: 'call' if pnum(v) is None else 'u250' if pnum(v) < 250000 else '250-400' if pnum(v) <= 400000 else '400')
body_c = count_by(lambda v: 'SUV' if v['model'] == 'Urus' else 'Spyder' if 'Spyder' in (v['trim'] or '') else 'Coupe')
COLOUR = {'Nero': 'Black', 'Grigio': 'Grey', 'Giallo': 'Yellow', 'Rosso': 'Red'}
colour_c = count_by(lambda v: COLOUR.get((v['exteriorColor'] or 'x').split()[0], 'Other') if v['exteriorColor'] else 'Other')
miles_c = count_by(lambda v: '1k' if v['mileage'] < 1000 else '10k' if v['mileage'] <= 10000 else 'more')

def dropdown(label, title, items, name, wide=False):
    return f'''            <details class="filter">
                <summary class="filter__trigger"><span>{label}</span><svg class="icon filter__caret" aria-hidden="true"><use href="#i-chevron-down"/></svg></summary>
                <div class="filter__panel{' filter__panel--wide' if wide else ''}">
                    <p class="filter__group-title">{title}</p>
                    <ul class="filter__list">
{options(title, items, name)}
                    </ul>
                    <div class="filter__panel-foot"><button class="filter__clear" type="button">Clear</button></div>
                </div>
            </details>'''

srp_cards = '\n'.join(card(cars[s]) for s in SRP_STOCKS)
srp_body = f'''<!-- ============================ INTRO ============================ -->
<section class="srp-intro band band--dark" aria-labelledby="srp-title">
    <div class="container srp-intro__grid">
        <div>
            <p class="t-eyelet section-head__eyelet">Inventory</p>
            <h1 class="t-banner" id="srp-title">The current selection</h1>
        </div>
        <p class="srp-intro__count"><b data-result-count>{TOTAL}</b> vehicles</p>
    </div>
</section>

<!-- ============================ SEARCH + FILTERS ============================
     As the Prestige demo: keyword search, five dropdowns, All filters, sort. The dropdown
     panels float (they never push the results); All filters opens in flow below the row. -->
<div class="filter-bar" role="search" aria-label="Refine results">
    <div class="container">
        <form class="srp-search" action="#" role="presentation">
            <label class="visually-hidden" for="srp-q">Search by keyword</label>
            <input class="field__input srp-search__input" id="srp-q" type="search" placeholder="Search by keyword" autocomplete="off">
            <button class="btn btn--secondary btn--md srp-search__btn" type="submit"><span>Search</span></button>
        </form>
        <div class="filter-bar__row">
{dropdown('Condition', 'Condition', [(k, k, n) for k, n in cond.items()], 'condition')}
{dropdown('Year', 'Year', [(k, k, n) for k, n in sorted(years.items(), reverse=True)], 'year')}
{dropdown('Model', 'Lamborghini models', [(k, k, n) for k, n in sorted(models.items())], 'model')}
{dropdown('Trim', 'Trim', [(k, k, n) for k, n in sorted(trims.items())], 'trim')}
{dropdown('Price', 'Price', [(k, l, price_c.get(k, 0)) for k, l in [('u250', 'Under $250,000'), ('250-400', '$250,000 – $400,000'), ('400', 'Over $400,000'), ('call', 'Call for price')]], 'price')}
            <button class="filter__trigger filter__trigger--all" type="button" aria-expanded="false" aria-controls="filter-all" data-all-toggle>
                <svg class="icon" aria-hidden="true"><use href="#i-sliders"/></svg><span>All filters</span>
            </button>
            <span class="filter-bar__spacer"></span>
            <details class="sort">
                <summary class="sort__trigger"><span class="sort__label">Sort:</span> <span class="sort__value">Recently listed</span><svg class="icon filter__caret" aria-hidden="true"><use href="#i-chevron-down"/></svg></summary>
                <div class="sort__panel">
                    <button class="sort__option is-active" type="button">Recently listed</button>
                    <button class="sort__option" type="button">Price · low to high</button>
                    <button class="sort__option" type="button">Price · high to low</button>
                    <button class="sort__option" type="button">Year · newest first</button>
                    <button class="sort__option" type="button">Mileage · lowest first</button>
                </div>
            </details>
        </div>
        <div class="filter-all" id="filter-all" hidden>
            <div class="filter-all__grid">
                <div><p class="filter__group-title">Body style</p><ul class="filter__list">
{options('', [(k, k, n) for k, n in sorted(body_c.items())], 'body')}
                </ul></div>
                <div><p class="filter__group-title">Exterior colour</p><ul class="filter__list">
{options('', [(k, l, colour_c.get(k, 0)) for k, l in [('Black', 'Black'), ('Grey', 'Grey'), ('Yellow', 'Yellow'), ('Red', 'Red'), ('Other', 'Other or not listed')]], 'colour')}
                </ul></div>
                <div><p class="filter__group-title">Mileage</p><ul class="filter__list">
{options('', [(k, l, miles_c.get(k, 0)) for k, l in [('1k', 'Under 1,000 mi'), ('10k', '1,000 – 10,000 mi'), ('more', 'Over 10,000 mi')]], 'mileage')}
                </ul></div>
                <div><p class="filter__group-title">Drivetrain</p><ul class="filter__list">
{options('', [('AWD', 'All-wheel drive', TOTAL)], 'drive')}
                </ul></div>
            </div>
            <div class="filter-all__foot">
                <button class="filter__clear" type="button" data-reset-all>Reset all</button>
                <button class="btn btn--primary btn--md" type="button" data-all-close><span>Show {TOTAL} results</span></button>
            </div>
        </div>
        <div class="filter-chips" aria-label="Active filters" data-chips>
            <button class="chip-clear" type="button" hidden data-chips-clear>Clear all</button>
        </div>
    </div>
</div>

<!-- ============================ RESULTS ============================
     Card after the Prestige demo card (photo, name, mileage · gearbox, Exterior / Interior /
     Engine / Stock, price, two CTAs), in the homepage vcard language: black on #181818,
     square, accent price. "Call for price" is a tel: link (client). -->
<section class="srp-results band band--dark" aria-label="Inventory results">
    <div class="container">
        <ul class="srp-grid" role="list">
{srp_cards}
        </ul>
        <p class="srp-empty" hidden data-empty>No vehicles match these filters. <button class="spec__link" type="button" data-chips-clear>Clear all filters</button></p>
        <nav class="pagination" aria-label="Results pages">
            <a class="pagination__link pagination__link--nav is-disabled" aria-disabled="true"><svg class="icon" aria-hidden="true"><use href="#i-chevron-left"/></svg><span class="visually-hidden">Previous page</span></a>
            <a class="pagination__link is-active" href="#" aria-current="page">1</a>
            <a class="pagination__link" href="#">2</a>
            <a class="pagination__link" href="#">3</a>
            <a class="pagination__link pagination__link--nav" href="#"><svg class="icon" aria-hidden="true"><use href="#i-chevron-right"/></svg><span class="visually-hidden">Next page</span></a>
        </nav>
        <p class="t-legal srp-note">Listings as published on lamborghinimiami.com on 30 Sep 2026. Price includes dealer fee of $1,447.50 and $299 electronic filing fee; tax, tag, title and registration fees are not included and are calculated at time of purchase. Price and availability subject to change.</p>
    </div>
</section>'''


# ---------- VDP ----------
v = cars[VDP_STOCK]
vi = info(VDP_STOCK)
name = model_name(v)
photos = v['photos']
# the stage opens on the clean front three-quarter (photo 0 carries the dealer lockup band)
START = next((k for k, u in enumerate(photos) if u.split('/')[-1] == v['downloaded'][0]['url'].split('/')[-1]), 0)

def md_inline(t):   # client: "**text**" renders bold (the platform prints the asterisks today)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', E(t))

raw = block(vdp_html(VDP_STOCK), 'mod-vehicle-comments', 'mod-vehicle-equipment')
raw = re.sub(r'<br\s*/?>', '\n', raw)
lines = [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '', raw)).split('\n') if l.strip()]
lines = [l for l in lines if l.upper() != 'ABOUT THIS VEHICLE' and not l.startswith('<')]
prose = []
for l in lines:
    m = re.fullmatch(r'\*\*(.+)\*\*', l)
    if m and len(prose) == 0: prose.append(f'<p class="vdp-prose__lead"><strong>{E(m.group(1))}</strong></p>')
    elif m: prose.append(f'<h3 class="vdp-prose__sub">{E(m.group(1))}</h3>')
    else: prose.append(f'<p>{md_inline(l)}</p>')
prose_html = '\n                    '.join(prose)

eq = block(vdp_html(VDP_STOCK), 'mod-vehicle-equipment')[:80000]
equipment = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip().strip('"') for x in re.findall(r'<li[^>]*>([\s\S]*?)</li>', eq)]
equipment = [x for x in equipment if x][:132]
eq_html = '\n'.join(f'                        <li>{E(x)}</li>' for x in equipment)

GALLERY_SHOWN = 12
thumbs = '\n'.join(
    f'''                <li{' hidden data-more' if k >= GALLERY_SHOWN else ''}><button class="vdp-thumb" type="button" data-photo="{k}" aria-label="Photo {k + 1} of {len(photos)}"><img src="{u}" width="1024" height="768" loading="lazy" decoding="async" alt=""></button></li>'''
    for k, u in enumerate(photos))

specs = [('Exterior', v['exteriorColor']), ('Interior', v['interiorColor']), ('Engine', '6.5L V12 plug-in hybrid'),
         ('Transmission', '8-speed dual-clutch'), ('Drivetrain', vi.get('Drivetrain', '—')), ('Mileage', miles(v)),
         ('Stock', v['stock']), ('VIN', v['vin'])]
spec_rows = '\n'.join(f'                        <div class="spec__row"><dt class="spec__label">{k}</dt><dd class="spec__value">{E(val)}</dd></div>' for k, val in specs)

related = [cars[s] for s in ['86180', 'CJ2626', '10914']]   # the other Revueltos, then the Temerario
related_html = '\n'.join(card(r) for r in related)
photos_json = json.dumps(photos)
STRIP = [START] + [k for k in range(len(photos)) if k != START and k != 0][:4]   # the opening view, then four more (not the lockup frame)
strip = '\n'.join(f'''                <li><button class="vdp-thumb" type="button" data-photo="{k}" aria-label="Photo {k + 1} of {len(photos)}"><img src="{photos[k]}" width="1024" height="768" loading="lazy" decoding="async" alt=""></button></li>''' for k in STRIP)

vdp_body = f'''<div class="vdp band band--dark">
    <div class="container">

        <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="index_v2.html">Home</a><span aria-hidden="true">/</span>
            <a href="srp.html">Inventory</a><span aria-hidden="true">/</span>
            <span aria-current="page">{E(name)}</span>
        </nav>

        <!-- ============================ SUMMARY: gallery · panel · action bar (as the Prestige VDP) ============================ -->
        <section class="vdp-summary" aria-label="Vehicle overview">
            <div class="vdp-media">
            <div class="vdp-stage" data-stage>
                <img class="vdp-stage__img" src="{photos[START]}" width="1024" height="768" fetchpriority="high" decoding="async"
                     alt="{E(name)} in {E(v['exteriorColor'])}, photograph {START + 1} of {len(photos)}" data-stage-img data-start="{START}">
                <button class="vdp-stage__nav vdp-stage__nav--prev" type="button" aria-label="Previous photo" data-stage-prev><svg class="icon" aria-hidden="true"><use href="#i-chevron-left"/></svg></button>
                <button class="vdp-stage__nav vdp-stage__nav--next" type="button" aria-label="Next photo" data-stage-next><svg class="icon" aria-hidden="true"><use href="#i-chevron-right"/></svg></button>
                <a class="vdp-stage__count" href="#photos"><span data-stage-n>{START + 1}</span>&nbsp;/&nbsp;{len(photos)} photos</a>
                <script type="application/json" data-photos>{photos_json}</script>
            </div>
            <ul class="vdp-strip" role="list" aria-label="More photos">
{strip}
            </ul>
            </div>

            <aside class="vdp-panel" aria-label="Price and details">
                <p class="t-eyelet vdp-panel__cond">Pre-owned</p>
                <h1 class="vdp-panel__title">{E(name)}</h1>
                {price_block(v, ' price--lg')}
                <dl class="spec vdp-panel__spec">
{spec_rows}
                </dl>
                {ctas(v, ' lead-ctas--panel')}
            </aside>

            <div class="vdp-bar">
                <div class="vdp-bar__actions">
                    <button class="vdp-action" type="button" data-share><svg class="icon" aria-hidden="true"><use href="#i-external"/></svg><span>Share</span></button>
                    <a class="vdp-action" href="sms:+18332905147?&amp;body={E('About the ' + name + ', stock ' + v['stock'])}"><svg class="icon" aria-hidden="true"><use href="#i-phone"/></svg><span>Text us</span></a>
                    <span class="vdp-bar__status" role="status" data-share-status></span>
                </div>
                <div class="vdp-bar__buy">
                    <a class="btn btn--secondary btn--md" href="tel:+18332905147"><span>(833) 290-5147</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-phone"/></svg></a>
                    <a class="btn btn--secondary btn--md" href="https://shop.lamborghinimiami.com/" rel="noopener"><span>Start buying</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg></a>
                </div>
            </div>
        </section>

        <!-- ============================ SECTIONS: About · Options · Finance (accordions, as Prestige) ============================ -->
        <div class="vdp-sections">
            <details class="vdp-acc" open>
                <summary class="vdp-acc__head"><h2 class="vdp-acc__title">About this vehicle</h2><svg class="icon vdp-acc__chev" aria-hidden="true"><use href="#i-chevron-down"/></svg></summary>
                <div class="vdp-acc__body vdp-prose">
                    {prose_html}
                </div>
            </details>
            <details class="vdp-acc">
                <summary class="vdp-acc__head"><h2 class="vdp-acc__title">Options &amp; equipment</h2><span class="vdp-acc__count">{len(equipment)} items</span><svg class="icon vdp-acc__chev" aria-hidden="true"><use href="#i-chevron-down"/></svg></summary>
                <div class="vdp-acc__body">
                    <ul class="vdp-options">
{eq_html}
                    </ul>
                    <p class="t-legal">Equipment data © 2026 Autodata, Inc. dba ChromeData, as published on the listing.</p>
                </div>
            </details>
            <details class="vdp-acc">
                <summary class="vdp-acc__head"><h2 class="vdp-acc__title">Finance calculator</h2><svg class="icon vdp-acc__chev" aria-hidden="true"><use href="#i-chevron-down"/></svg></summary>
                <div class="vdp-acc__body">
                    <form class="calc" autocomplete="off" data-calc>
                        <div class="calc__grid">
                            <div class="field"><label class="field__label" for="calc-price">Vehicle price ($)</label><input class="field__input" id="calc-price" type="text" inputmode="decimal" value="{price(v)[1:]}" data-calc-price></div>
                            <div class="field"><label class="field__label" for="calc-down">Down payment ($)</label><input class="field__input" id="calc-down" type="text" inputmode="decimal" placeholder="e.g. 150,000" data-calc-down></div>
                            <div class="field"><label class="field__label" for="calc-apr">APR (%)</label><input class="field__input" id="calc-apr" type="text" inputmode="decimal" placeholder="Your rate" data-calc-apr></div>
                            <div class="field"><label class="field__label" for="calc-term">Term (months)</label>
                                <select class="field__input field__select" id="calc-term" data-calc-term><option>36</option><option>48</option><option selected>60</option><option>72</option><option>84</option></select></div>
                        </div>
                        <dl class="calc__out">
                            <div><dt>Loan amount</dt><dd data-calc-loan>—</dd></div>
                            <div class="calc__monthly"><dt>Monthly payment</dt><dd data-calc-monthly>—</dd></div>
                        </dl>
                        <p class="t-legal">An estimate from the figures you enter; it is not an offer of credit. Tax, tag, title and registration are not included.</p>
                    </form>
                </div>
            </details>
        </div>

        <!-- ============================ GALLERY ============================ -->
        <section class="vdp-gallery" id="photos" aria-labelledby="photos-title">
            <header class="vdp-gallery__head"><h2 class="t-title" id="photos-title">Gallery</h2><p class="vdp-gallery__n">{len(photos)} photos</p></header>
            <ul class="vdp-gallery__grid" role="list">
{thumbs}
            </ul>
            <button class="btn btn--secondary btn--md vdp-gallery__more" type="button" data-gallery-more><span>Show all {len(photos)} photos</span></button>
        </section>

        <p class="t-legal vdp-note">Price includes dealer fee of $1,447.50 and $299 electronic filing fee; tax, tag, title and registration fees are not included and are calculated at time of purchase. Listing as published on lamborghinimiami.com on 30 Sep 2026; price and availability subject to change.</p>
    </div>
</div>

<!-- ============================ RELATED ============================ -->
<section class="related band band--black" aria-labelledby="related-title">
    <div class="container">
        <header class="related__head">
            <h2 class="t-title" id="related-title">Related vehicles</h2>
            <a class="btn btn--tertiary" href="srp.html"><span>View all inventory</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </header>
        <ul class="srp-grid srp-grid--related" role="list">
{related_html}
        </ul>
    </div>
</section>'''

open(ROOT + 'srp.html', 'w', encoding='utf-8').write(page(
    'Lamborghini Inventory | Lamborghini Miami, North Miami Beach, FL',
    'New and pre-owned Lamborghini for sale at Lamborghini Miami, Biscayne Boulevard, North Miami Beach.', srp_body))
open(ROOT + 'vdp.html', 'w', encoding='utf-8').write(page(
    f'Used {name} for sale | Lamborghini Miami, stock {v["stock"]}',
    f'{name} in {v["exteriorColor"]}, {miles(v)}, at Lamborghini Miami, North Miami Beach.', vdp_body))
print('srp.html, vdp.html written;', len(SRP_STOCKS), 'cards,', len(photos), 'photos,', len(equipment), 'equipment items')
