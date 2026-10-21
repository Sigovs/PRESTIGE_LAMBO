#!/usr/bin/env python3
"""v3 model pages (client, Oct 2026): our own page per model, so "Learn more" and "Inquire"
keep the visitor with Lamborghini Miami instead of lamborghini.com and its all-dealer form.
The configurator stays a link out (client: "totally understand the configurator link out").

    python3 _tools/build-model-pages.py

Builds model-<slug>.html from one template. The header, menu and footer are lifted from
service.html, so the shared chrome stays in one place. Figures are only those already shown
in the range (US units); none are invented for a model Lamborghini has not published.
The enquiry form is a mock-up: it validates and confirms locally, it is NOT connected
(the client's DriveCentric campaign comes later)."""
from pathlib import Path
import re

SITE = Path(__file__).resolve().parent.parent
SVC = (SITE / 'service.html').read_text()
CONFIGURATOR = 'https://configurator.lamborghini.com/'

MODELS = [
    dict(slug='revuelto', name='Revuelto', mark='Revuelto', mk='1',
         claim='The quantum of driving',
         facts=[('Max power', '1,001 hp'), ('Top speed', '>217 mph'), ('0–62 mph', '2.5 s')],
         art_alt='Lamborghini Revuelto in orange, front three-quarter view, its Y-shaped headlights lit.',
         media=None,
         inventory='Revuelto',
         # v3 (Alex, 21 Oct): the full model page — large hero, figures, exterior, interior, gallery, in stock.
         # Photos and the exterior line are lamborghini.com's own (en-en/models/revuelto); figures in US units.
         story=dict(
             lead='The first HPEV hybrid super sports car: a new V12, three electric motors and a dual-clutch e-gearbox.',
             hero_alt='A Lamborghini Revuelto in violet, front three-quarter view, in a dark studio.',
             numbers=[('1,001', 'hp', 'Max power, V12 and three electric motors combined'), ('&gt;217', 'mph', 'Top speed'),
                      ('2.5', 's', '0–62 mph'), ('6.5', 'L', 'V12 displacement')],
             numbers_img=('int-engine', 'The Revuelto’s V12 engine and e-gearbox, on a dark ground.'),
             exterior=dict(text='Revuelto blends Lamborghini heritage with a bold new design language. Sculpted lines, sharp surfaces and the iconic center line define a futuristic silhouette, while the exposed V12 proudly celebrates its racing DNA.',
                           wide_alt='A Lamborghini Revuelto in orange, in side profile against an orange ground.',
                           cards=[('ext-headlight', 'Headlights', 'Y-shaped lights frame the front.', 'The front of an orange Revuelto, its Y-shaped headlights lit.'),
                                  ('ext-rear', 'The rear', 'Hexagonal exhausts sit high, between the taillights.', 'The rear of an orange Revuelto, its taillights lit.'),
                                  ('ext-engine', 'The exposed V12', 'The engine stays on show under the rear cover.', 'The engine bay of an orange Revuelto, seen from above.')]),
             interior=dict(text='Inside, a cockpit built around the driver: the instruments behind the wheel, the driving modes at the driver’s hands, and a display of its own for the passenger.',
                           main_alt='The Revuelto cockpit in black and orange, seen from the passenger side.',
                           cards=[('int-wheel', 'At the wheel', 'Digital instruments, and the driving modes at the driver’s hands.', 'The Revuelto steering wheel and digital instruments.'),
                                  ('int-passenger', 'For the passenger', 'A display of its own, set into the dashboard.', 'The passenger display in the Revuelto dashboard, in orange leather.')]),
             gallery=[('gallery-5', 'A grey Revuelto on track at dusk, from behind.'), ('gallery-1', 'A green Revuelto on snow below mountains.'),
                      ('gallery-2', 'An orange Revuelto from behind, on a lit circuit at night.'), ('gallery-3', 'The Revuelto centre console in orange and black.'),
                      ('gallery-4', 'A yellow Revuelto on track, seen from above.'),
                      ('gallery-6', 'A dark blue Revuelto in a studio, front three-quarter view.'), ('gallery-7', 'A lime-green Revuelto in a studio, front three-quarter view.'),
                      ('gallery-8', 'The front of an orange Revuelto, close up, its headlights lit.'), ('gallery-9', 'The rear of an orange Revuelto with its spoiler raised, airflow drawn over it.')],
         ),
         note=''),
    dict(slug='revuelto-sv', name='Revuelto SV', mark='Revuelto SV', mk='0.62',
         claim='Hockenheim record holder',
         facts=[('Hockenheimring lap', '1:41.6')],
         art_alt='Lamborghini Revuelto SV in grey and black carbon fibre with red accents, front three-quarter view.',
         media=dict(kind='youtube', id='1UE_RnIbt4c', title='Revuelto SV film'),
         inventory='Revuelto SV', note='',
         story=dict(
             lead='Super Veloce, to a new dimension: a naturally aspirated V12, hybrid performance and motorsport-derived technologies, for a limited number of drivers.',
             hero_alt='A Lamborghini Revuelto SV in red and black, front three-quarter view, in a concrete studio.',
             numbers=[('1,050', 'hp', 'Max power, V12 and electric motors combined'), ('216', 'mph', 'Top speed'),
                      ('2.4', 's', '0–62 mph'), ('1:41.6', '', 'Hockenheimring lap, a production car record')],
             numbers_img=('int-engine', 'The Revuelto SV’s V12 engine, on a dark ground.'),
             exterior=dict(text='The Super Veloce treatment shows from every side: aerodynamics of its own front and rear, and carbon fibre throughout.',
                           wide_alt='A Lamborghini Revuelto SV in profile against a red ground.',
                           cards=[('ext-front', 'The front', 'Y-shaped lights and a front built for downforce.', 'The front of a red and black Revuelto SV, head-on.'),
                                  ('ext-rear', 'The rear', 'A fixed wing over the exhausts and the diffuser.', 'The rear of a red and black Revuelto SV.'),
                                  ('ext-aero', 'Aerodynamics', 'Airflow worked for balance and grip at speed.', 'The Revuelto SV with its airflow drawn over the body.')]),
             interior=dict(text='Inside, a cockpit for the track: carbon-shell seats and a wheel built around the driver.',
                           main_alt='The Revuelto SV cockpit in black and red.',
                           cards=[('int-driver', 'For the driver', 'The wheel, the instruments and the driving modes at hand.', 'The Revuelto SV steering wheel and instruments.'),
                                  ('int-seats', 'The seats', 'Carbon-shell seats, trimmed in black and red.', 'The Revuelto SV seats in black with red details.')]),
             gallery=[('gallery-1', 'A Revuelto SV from above, its carbon engine cover open to view.'), ('gallery-2', 'A red and black Revuelto SV in a concrete studio.'),
                      ('gallery-3', 'A grey Revuelto SV in a tunnel, a bull mural behind it.'), ('gallery-4', 'A grey Revuelto SV from above, at speed in the wet.'),
                      ('gallery-5', 'The Revuelto SV’s Y-shaped taillight, close up.'), ('gallery-6', 'A Revuelto SV with its carbon fibre parts highlighted.'),
                      ('gallery-7', 'A Revuelto SV wheel and tyre, close up.'), ('gallery-8', 'The Revuelto SV’s brake cooling, airflow drawn over the wheel.'),
                      ('gallery-9', 'The Revuelto SV brakes, discs and calipers.')],
         )),
    dict(slug='temerario', name='Temerario', mark='Temerario', mk='0.86',
         claim='You can’t hide who you are',
         facts=[('Max power', '907 hp'), ('Top speed', '213 mph'), ('0–62 mph', '2.7 s')],
         art_alt='Lamborghini Temerario in dark blue, front three-quarter view, its hexagonal daytime lights lit.',
         media=None, inventory='Temerario', note='',
         story=dict(
             lead='Lamborghini’s first super sports car with a twin-turbo V8 and three electric motors, and the second of its HPEV range.',
             hero_alt='A Lamborghini Temerario in orange, front three-quarter view, in a dark studio.',
             numbers=[('907', 'hp', 'Max power, V8 and three electric motors combined'), ('213', 'mph', 'Top speed'),
                      ('2.7', 's', '0–62 mph'), ('4.0', 'L', 'Twin-turbo V8')],
             numbers_img=('int-engine', 'The Temerario powertrain, on a dark ground.'),
             exterior=dict(text='Temerario marks a new Lamborghini design milestone, with bold lines, futuristic hexagonal DRLs, an exposed engine and a functional spoiler enhancing aerodynamic efficiency.',
                           wide_alt='A Lamborghini Temerario in blue, in side profile.',
                           cards=[('ext-headlight', 'Hexagonal lights', 'The daytime running lights draw a hexagon at each corner.', 'The front of a dark Temerario, its hexagonal lights lit.'),
                                  ('ext-rear', 'The rear', 'Hexagonal taillights and a functional spoiler.', 'The rear of a dark Temerario, its taillights lit.'),
                                  ('ext-engine', 'The exposed engine', 'The V8 stays on show under the rear deck.', 'The engine bay of a Temerario, close up.')]),
             interior=dict(text='Inside, a cockpit built around the driver: the instruments behind the wheel, the driving modes at the driver’s hands, and a display for the passenger.',
                           main_alt='The Temerario cockpit in black and tan.',
                           cards=[('int-wheel', 'At the wheel', 'Digital instruments, and the driving modes at hand.', 'The Temerario steering wheel and digital instruments.'),
                                  ('int-passenger', 'For the passenger', 'A display of its own, set into the dashboard.', 'The passenger display in the Temerario dashboard.')]),
             gallery=[('gallery-1', 'A yellow Temerario on a circuit.'), ('gallery-2', 'A green Temerario at sunset beside the Sant’Agata Bolognese sign.'),
                      ('gallery-3', 'A blue Temerario by an old tower.'), ('gallery-4', 'The hexagonal light of a yellow Temerario, close up.'),
                      ('gallery-5', 'A white Temerario from behind, in a doorway with curtains.'), ('gallery-6', 'A yellow Temerario in a dark studio.'),
                      ('gallery-7', 'A green Temerario in a dark studio.'), ('gallery-8', 'The Temerario’s spoiler, airflow drawn over it.'),
                      ('gallery-9', 'The front of a Temerario, airflow drawn over it.')],
         )),
    dict(slug='urus-se', name='Urus SE', mark='Urus SE', mk='1',
         claim='Dare to live more',
         facts=[('Max power', '789 hp'), ('Top speed', '194 mph'), ('0–62 mph', '3.4 s')],
         art_alt='Lamborghini Urus SE in orange, front three-quarter view.',
         media=None, inventory='Urus', note='',
         story=dict(
             lead='Lamborghini’s first plug-in hybrid Super SUV, and its next step toward full hybridization.',
             hero_alt='A Lamborghini Urus SE in teal, front three-quarter view, in a dark studio.',
             numbers=[('789', 'hp', 'Max power, V8 and electric motor combined'), ('194', 'mph', 'Top speed'),
                      ('3.4', 's', '0–62 mph'), ('4.0', 'L', 'Twin-turbo V8')],
             numbers_img=('int-engine', 'The Urus SE’s twin-turbo V8, on a dark ground.'),
             exterior=dict(text='Urus SE features sportier proportions and refined lines that improve aerodynamics, cooling and rear downforce. Extensive customization options enhance its bold, muscular character.',
                           wide_alt='A Lamborghini Urus SE in orange, in side profile.',
                           cards=[('ext-headlight', 'Headlights', 'A new light signature across the front.', 'The front of an orange Urus SE, its headlights lit.'),
                                  ('ext-rear', 'The rear', 'Slim taillights across a wider rear.', 'The rear of an orange Urus SE.'),
                                  ('ext-wheel', 'The wheels', 'Large wheels fill the arches.', 'A wheel of an orange Urus SE, close up.')]),
             interior=dict(text='Inside, a wide central screen, and the drive modes chosen at the centre console.',
                           main_alt='The Urus SE cockpit in black and orange.',
                           cards=[('int-selector', 'Drive modes', 'Selected at the centre console.', 'The Urus SE drive mode selector on the centre console.'),
                                  ('int-screen', 'The screen', 'A central display for the car’s functions.', 'The Urus SE central touchscreen.')]),
             gallery=[('gallery-1', 'An orange Urus SE raising dust on a dirt road.'), ('gallery-2', 'Three Urus SE in a field: orange, blue and yellow.'),
                      ('gallery-3', 'A dark Urus SE through spray, close up.'), ('gallery-4', 'An orange Urus SE on rocks at sunset.'),
                      ('gallery-5', 'A yellow Urus SE in a green landscape.'), ('gallery-6', 'The front corner of an orange Urus SE, close up.'),
                      ('gallery-7', 'A dark Urus SE in a studio.'), ('gallery-8', 'The Urus SE rear spoiler, airflow drawn over it.'),
                      ('gallery-9', 'An orange Urus SE seen from above.')],
         )),
    dict(slug='urus-se-performante', name='Urus SE Performante', mark='Performante', mk='0.68',
         claim='Urus at its peak',
         facts=[('Max power', '801 hp'), ('Top speed', '194 mph'), ('0–62 mph', '3.3 s')],
         art_alt='Lamborghini Urus SE Performante in yellow-green with a carbon bonnet, front three-quarter view.',
         media=dict(kind='youtube', id='5ZtLH3s8Wvg', title='Urus SE Performante film'),
         inventory='Urus', note='',
         story=dict(
             lead='The plug-in hybrid Super SUV at its most precise: aerodynamics, driving dynamics and an innovative suspension system.',
             hero_alt='A Lamborghini Urus SE Performante in violet, front three-quarter view, in a dark studio.',
             numbers=[('801', 'hp', 'Max power, V8 and electric motor combined'), ('194', 'mph', 'Top speed'),
                      ('3.3', 's', '0–62 mph'), ('4.0', 'L', 'Twin-turbo V8')],
             numbers_img=('int-engine', 'The Urus SE Performante’s twin-turbo V8, on a dark ground.'),
             exterior=dict(text='Extensive use of carbon fiber lightens Urus SE Performante, optimizing the power-to-weight ratio to achieve unrivaled performance.',
                           wide_alt='A Lamborghini Urus SE Performante in lime, in side profile against a red ground.',
                           cards=[('ext-front', 'The front', 'A front shaped for air and cooling.', 'The front of a lime Urus SE Performante, close up.'),
                                  ('ext-bonnet', 'The bonnet', 'A vented bonnet over the V8.', 'The vented bonnet of a lime Urus SE Performante.'),
                                  ('ext-spoiler', 'The spoiler', 'A rear spoiler for downforce.', 'The rear spoiler of a lime Urus SE Performante.')]),
             interior=dict(text='Inside, a sports wheel, and seats trimmed for the Performante.',
                           main_alt='The Urus SE Performante cockpit in black with red details.',
                           cards=[('int-wheel', 'At the wheel', 'The steering wheel and instruments, close to hand.', 'The Urus SE Performante steering wheel and instruments.'),
                                  ('int-seats', 'The seats', 'Trimmed in black with red stitching.', 'The Urus SE Performante seats in black with red stitching.')]),
             gallery=[('gallery-0', 'A lime Urus SE Performante from above, at night in the city.'), ('gallery-1', 'A lime Urus SE Performante from behind, at night.'), ('gallery-2', 'A lime Urus SE Performante at speed, at night.'),
                      ('gallery-3', 'The exhausts of a Urus SE Performante, close up.'), ('gallery-4', 'A Urus SE Performante interior detail with the Lamborghini script.'),
                      ('gallery-5', 'A lime Urus SE Performante head-on.'), ('gallery-6', 'A green Urus SE Performante in a dark studio.'),
                      ('gallery-7', 'A white Urus SE Performante in a dark studio.'), ('gallery-8', 'Airflow along the side of a Urus SE Performante.'),
                      ('gallery-9', 'The Urus SE Performante brakes.')][:9],
         )),
]
ORDER = ['revuelto', 'revuelto-sv', 'temerario', 'urus-se', 'urus-se-performante']


def chunk(start, end):
    a = SVC.index(start)
    return SVC[a:SVC.index(end, a)]


SPRITE = chunk('<svg class="sprite"', '<a class="skip-link"')
SPRITE = SPRITE.replace('</svg>', '    <symbol id="i-expand" viewBox="0 0 24 24"><path d="M14 4h6v6M10 20H4v-6M20 4l-7 7M4 20l7-7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square"/></symbol>\n</svg>', 1)
SPRITE = SPRITE.replace('</svg>', '    <symbol id="i-play" viewBox="0 0 24 24"><path d="M7 4.5v15L19.5 12Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="miter"/></symbol>\n</svg>', 1)
HEADER = chunk('<!-- ============================ HEADER', '<main id="main">')
FOOTER = chunk('<!-- ============================ FOOTER', '<script src="https://unpkg.com/lenis')
# chrome as it stands on a model page: no current Service page, Contact goes to the enquiry
HEADER = HEADER.replace(' aria-current="page"', '').replace('href="#request">Contact', 'href="#enquire">Contact')
HEADER = HEADER.replace('<li><a class="menu__link" href="#request" data-menu-link>Schedule service</a></li>',
                        '<li><a class="menu__link" href="service.html#request">Schedule service</a></li>')
FOOTER = FOOTER.replace(' aria-current="page"', '').replace('<li><a href="#request">Schedule service</a></li>',
                                                           '<li><a href="service.html#request">Schedule service</a></li>')
# the models, as pages, in the menu and footer
models_li = ''.join(f'\n                    <li><a class="menu__link" href="model-{s}.html">{next(m for m in MODELS if m["slug"] == s)["name"]}</a></li>' for s in ORDER)
HEADER = HEADER.replace('<li><a class="menu__link" href="index_v3.html#range">Models</a></li>',
                        '<li><a class="menu__link" href="index_v3.html#range">Models</a></li>' + models_li, 1)


def facts(m):
    rows = ''.join(f'''
                <div class="spec__row"><dt class="spec__label">{k}</dt><dd class="spec__value">{v}</dd></div>''' for k, v in m['facts'])
    return f'''<dl class="spec mfacts__list">{rows}
            </dl>'''


def media(m):
    md = m['media']
    if not md:
        return ''
    if md['kind'] == 'youtube':
        vid = md['id']
        inner = f'''<div class="mfilm" data-yt="{vid}" data-yt-title="{md['title']}">
                <img class="mfilm__poster" src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" width="1280" height="720" loading="lazy" decoding="async" alt="">
                <button class="mfilm__play" type="button" data-yt-play aria-label="Play the {md['title']} (YouTube)">
                    <svg class="icon" aria-hidden="true"><use href="#i-play"/></svg><span>Watch the film</span>
                </button>
            </div>'''
    else:
        s, w, h = md['src'], md['w'], md['h']
        inner = f'''<figure class="mphoto">
                <picture>
                    <source type="image/webp" srcset="assets/img/{s}-1280.webp 1280w, assets/img/{s}-1920.webp 1920w" sizes="100vw">
                    <img src="assets/img/{s}-1920.jpg" srcset="assets/img/{s}-1280.jpg 1280w, assets/img/{s}-1920.jpg 1920w" sizes="100vw" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{md['alt']}">
                </picture>
            </figure>'''
    return f'''
<!-- ============================ 3 · FILM / PHOTOGRAPH ============================ -->
<section class="mmedia band band--black" aria-label="{m['name']}, film and photography">
    <div class="container">
            {inner}
    </div>
</section>
'''


import html as _html
SRP = (SITE / 'srp.html').read_text()


def pic(slug, role, widths, sizes, alt, cls='', eager=False, portrait=None):
    w = widths
    webp = ', '.join(f'assets/img/models/{slug}-{role}-{x}.webp {x}w' for x in w)
    jpg = ', '.join(f'assets/img/models/{slug}-{role}-{x}.jpg {x}w' for x in w)
    p_src = ''
    if portrait:
        pr, pw = portrait
        p_src = f'\n                    <source media="(max-width: 767.98px) and (orientation: portrait)" type="image/webp" srcset="assets/img/models/{slug}-{pr}-{pw}.webp">'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<picture>{p_src}
                    <source type="image/webp" srcset="{webp}" sizes="{sizes}">
                    <img{f' class="{cls}"' if cls else ''} src="assets/img/models/{slug}-{role}-{w[-1]}.jpg" srcset="{jpg}" sizes="{sizes}" {load} decoding="async" alt="{alt}">
                </picture>'''


def inventory(m):
    name = m.get('inventory')
    if not name:
        return ''
    cards = []
    for li in __import__('re').findall(r'<li data-year[^>]*data-model="' + name + r'"[^>]*>.*?</article>', SRP, flags=__import__('re').S):
        g = lambda pat: (__import__('re').search(pat, li, __import__('re').S) or [None, ''])[1]
        title = g(r'<h3 class="vehicle-card__name">([^<]*)</h3>')
        img = g(r'srcset="(assets/img/inv/[^ "]+-640\.webp)')
        miles = g(r'ph-gauge[^<]*</i><span>([^<]*)</span>')
        ext = g(r'Exterior</span><span class="vehicle-card__detail-value">([^<]*)<')
        price = g(r'class="vehicle-card__price">([^<]*)<')
        stock = g(r'Stock</span><span class="vehicle-card__detail-value">([^<]*)<')
        cond = g(r'data-cond="([^"]*)"')
        cards.append(f'''            <li class="minv__card">
                <a class="minv__link" href="vdp.html">
                    <img src="{img}" width="640" height="480" loading="lazy" decoding="async" alt="{title}, {ext}">
                    <span class="minv__cond">{cond}</span>
                    <span class="minv__name">{title}</span>
                    <span class="minv__meta">{ext} · {miles} · Stock {stock}</span>
                    <span class="minv__price">{price}</span>
                </a>
            </li>''')
    cards = cards[:6]
    return f'''
<!-- ============================ 6 · IN STOCK ============================
     The {name}s in our inventory, read from srp.html at build time; each opens its vehicle page,
     and View all opens the inventory filtered to the model (srp.html?model={name}). -->
<section class="minv band band--dark" id="in-stock" aria-labelledby="inv-title">
    <div class="container">
        <header class="minv__head">
            <div>
                <p class="t-eyelet section-head__eyelet">Lamborghini Miami</p>
                <h2 class="t-banner" id="inv-title">In our inventory</h2>
            </div>
            <a class="btn btn--secondary" href="srp.html?model={name}"><span>View all {name} inventory</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </header>
        <ol class="minv__grid">
{chr(10).join(cards) if cards else '            <li class="minv__none">No ' + name + ' in stock today. Ask our sales team about allocation.</li>'}
        </ol>
    </div>
</section>
'''


def story(m):
    st, slug, name = m['story'], m['slug'], m['name']
    ZOOM = '<span class="mzoom" aria-hidden="true"><svg class="icon"><use href="#i-expand"/></svg></span>'
    nums = ''.join(f'''
                <div class="mnum__item"><dt class="mnum__label">{lab}</dt><dd class="mnum__value">{v}<span class="mnum__unit">{u}</span></dd></div>''' for v, u, lab in st['numbers'])
    ZOOM = '<span class="mzoom" aria-hidden="true"><svg class="icon"><use href="#i-expand"/></svg></span>'
    def cards(lst):
        return ''.join(f'''
            <figure class="mcard">
                <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/{slug}-{r}-1200.webp" aria-label="Open photo: {title}">
                    {pic(slug, r, (800, 1200), '(min-width: 1024px) 30vw, (min-width: 768px) 45vw, 100vw', alt)}
                    {ZOOM}
                </button>
                <figcaption class="mcard__cap"><span class="mcard__title">{title}</span><span class="mcard__text">{text}</span></figcaption>
            </figure>''' for r, title, text, alt in lst)
    ex, it = st['exterior'], st['interior']
    n_gal = len(st['gallery'])
    gal = ''.join(f'''
            <li class="mgal__item mgal__item--{i}">
                <button class="mgal__open" type="button" data-gal-open="{i - 1}" data-full="assets/img/models/{slug}-{r}-1600.webp" aria-label="Open photo {i} of {n_gal}: {alt}">
                    {pic(slug, r, (900, 1600), '(min-width: 1024px) 50vw, 100vw', alt)}
                    {ZOOM}
                </button>
            </li>''' for i, (r, alt) in enumerate(st['gallery'], 1))
    hero = f'''
<!-- ============================ 1 · THE MODEL ============================
     Large hero: lamborghini.com's own studio frame, full screen; the copy low left on a floor-up scrim.
     Enquire stays on this page; Configure links out; View inventory opens the inventory for this model. -->
<section class="mbig" aria-labelledby="model-title">
    <div class="mbig__media">
                {pic(slug, 'hero', (1000, 1600, 2400), '100vw', st['hero_alt'], 'mbig__img', True, ('hero-p', 786))}
    </div>
    <div class="container mbig__inner">
        <p class="t-eyelet mbig__eyelet">Lamborghini Miami · New</p>
        <h1 class="mbig__name" id="model-title">{name}</h1>
        <p class="mbig__claim">{m['claim']}</p>
        <p class="mbig__lead">{st['lead']}</p>
        <div class="mbig__actions">
            <a class="btn btn--accent" href="#enquire"><span>Enquire</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
            <a class="btn btn--secondary" href="{CONFIGURATOR}" rel="noopener"><span>Configure yours</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg></a>
            <a class="btn btn--tertiary" href="srp.html?model={m.get('inventory', name)}"><span>View inventory</span></a>
        </div>
    </div>
</section>

<!-- ============================ 2 · FIGURES ============================ -->
<section class="mnum band band--black" aria-labelledby="facts-title">
    <div class="container mnum__grid">
        <header class="mnum__head">
            <p class="t-eyelet section-head__eyelet">{name}</p>
            <h2 class="t-banner" id="facts-title">In figures</h2>
        </header>
        <dl class="mnum__list">{nums}
        </dl>
        <figure class="mnum__media">
            {pic(slug, st['numbers_img'][0], (800, 1200), '(min-width: 1024px) 45vw, 100vw', st['numbers_img'][1])}
        </figure>
        <p class="t-legal mnum__src">As published by Automobili Lamborghini; power and speed in US units.</p>
        <div class="mcta__row mnum__cta">
            <a class="btn btn--secondary" href="{CONFIGURATOR}" rel="noopener"><span>Configure yours</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg></a>
            <a class="btn btn--tertiary" href="srp.html?model={m.get('inventory', name)}"><span>See the {name}s in stock</span></a>
        </div>
    </div>
</section>

<!-- ============================ 3 · EXTERIOR ============================ -->
<section class="mstory band band--dark" id="exterior" aria-labelledby="ext-title" data-gallery>
    <div class="container mstory__head">
        <div>
            <p class="t-eyelet section-head__eyelet">Exterior</p>
            <h2 class="t-banner" id="ext-title">Design</h2>
        </div>
        <p class="t-lead mstory__text">{ex['text']}</p>
    </div>
    <figure class="mstory__wide">
        <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/{slug}-exterior-2160.webp" aria-label="Open photo: the {name} in profile">
            {pic(slug, 'exterior', (1440, 2160), '100vw', ex['wide_alt'], '', False, ('exterior-p', 750))}
            {ZOOM}
        </button>
    </figure>
    <div class="container mstory__cards mstory__cards--3">{cards(ex['cards'])}
    </div>
    <div class="container mcta__row">
        <a class="btn btn--secondary" href="{CONFIGURATOR}" rel="noopener"><span>Choose your colour</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg></a>
        <a class="btn btn--tertiary" href="index_v3.html#ad-personam"><span>Ad Personam personalization</span></a>
    </div>
</section>

<!-- ============================ 4 · INTERIOR ============================ -->
<section class="mstory band band--black" id="interior" aria-labelledby="int-title" data-gallery>
    <div class="container mstory__head">
        <div>
            <p class="t-eyelet section-head__eyelet">Interior</p>
            <h2 class="t-banner" id="int-title">The cockpit</h2>
        </div>
        <p class="t-lead mstory__text">{it['text']}</p>
    </div>
    <div class="container">
        <figure class="mstory__main">
            <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/{slug}-interior-1600.webp" aria-label="Open photo: the cockpit">
                {pic(slug, 'interior', (1000, 1600, 2400), '(min-width: 1440px) 1320px, 100vw', it['main_alt'], '', False, ('interior-p', 786))}
                {ZOOM}
            </button>
        </figure>
    </div>
    <div class="container mstory__cards mstory__cards--2">{cards(it['cards'])}
    </div>
    <div class="container mcta__row">
        <a class="btn btn--accent" href="#enquire"><span>Book a viewing</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        <a class="btn btn--tertiary" href="{CONFIGURATOR}" rel="noopener"><span>Design your interior</span></a>
    </div>
</section>

<!-- ============================ 5 · GALLERY ============================ -->
<section class="mgal band band--dark" aria-labelledby="gal-title">
    <div class="container">
        <header class="section-head"><div>
            <p class="t-eyelet section-head__eyelet">{name}</p>
            <h2 class="t-banner" id="gal-title">Gallery</h2>
        </div></header>
        <ol class="mgal__grid" data-gallery>{gal}
        </ol>
    </div>
</section>
<!-- gallery lightbox: one photo at a time, ← → / swipe / Esc; model_v3.js -->
<dialog class="glb" aria-label="{name} gallery" data-gallery-box data-lenis-prevent>
    <figure class="glb__stage">
        <img class="glb__img" alt="" data-glb-img>
        <figcaption class="glb__cap"><span class="glb__n" data-glb-n>1 / {n_gal}</span> <span data-glb-cap></span></figcaption>
    </figure>
    <button class="glb__btn glb__btn--prev" type="button" data-glb-prev aria-label="Previous photo"><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    <button class="glb__btn glb__btn--next" type="button" data-glb-next aria-label="Next photo"><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    <button class="glb__close" type="button" data-glb-close aria-label="Close gallery"><svg class="icon" aria-hidden="true"><use href="#i-close"/></svg></button>
</dialog>

{media(m)}
<!-- ============================ CTA BAND ============================ -->
<section class="mcta band band--black" aria-labelledby="cta-title">
    <div class="container mcta__grid">
        <div>
            <p class="t-eyelet section-head__eyelet">Lamborghini Miami</p>
            <h2 class="t-banner mcta__title" id="cta-title"><span class="svc-line">Your {name}</span> <span class="svc-line">starts here</span></h2>
            <p class="t-lead mcta__lead">Talk to our sales team on Biscayne Boulevard about allocation, specification and delivery.</p>
        </div>
        <div class="mcta__actions">
            <a class="btn btn--accent" href="#enquire"><span>Enquire</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
            <a class="btn btn--secondary" href="tel:+18332905147"><span>Call (833) 290-5147</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-phone"/></svg></a>
            <a class="btn btn--tertiary" href="{CONFIGURATOR}" rel="noopener"><span>Configure yours</span></a>
        </div>
    </div>
</section>
{inventory(m)}'''
    return hero


def model_options(m):
    opts = [n['name'] for n in MODELS] + ['Temerario', 'Urus SE', 'Other']
    seen, out = set(), []
    for o in opts:
        if o in seen:
            continue
        seen.add(o)
        sel = ' selected' if o == m['name'] else ''
        out.append(f'<option{sel}>{o}</option>')
    return '\n                                '.join(out)


def STUDIO(m):
    slug, name = m['slug'], m['name']
    return f'''<!-- ============================ 1 · THE MODEL ============================
     Studio, as the range on the home page: the name as a watermark, the car cut out,
     the copy and actions upper left. Enquire stays on this page; Configure links out. -->
<section class="mhero" aria-labelledby="model-title">
    <div class="container mhero__inner">
        <p class="mhero__mark" aria-hidden="true" style="--mk:{m['mk']}">{m['mark']}</p>
        <div class="mhero__text">
            <p class="t-eyelet mhero__eyelet">Lamborghini Miami · New</p>
            <h1 class="mhero__name" id="model-title">{name}</h1>
            <p class="mhero__claim">{m['claim']}</p>
            <div class="mhero__actions">
                <a class="btn btn--accent" href="#enquire"><span>Enquire</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
                <a class="btn btn--secondary" href="{CONFIGURATOR}" rel="noopener"><span>Configure yours</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg></a>
                <a class="btn btn--tertiary" href="srp.html?model={m.get('inventory', name)}"><span>View inventory</span></a>
            </div>
        </div>
        <figure class="mhero__media">
            <picture>
                <source type="image/webp" srcset="assets/img/showcase-{slug}-800.webp 800w, assets/img/showcase-{slug}-1200.webp 1200w, assets/img/showcase-{slug}-1830.webp 1830w" sizes="(min-width: 1024px) 62vw, 100vw">
                <img class="mhero__car" src="assets/img/showcase-{slug}-800.png" width="1830" height="863" fetchpriority="high" decoding="async" alt="{m['art_alt']}">
            </picture>
        </figure>
    </div>
</section>

<!-- ============================ 2 · FIGURES ============================ -->
<section class="mfacts band band--dark" aria-labelledby="facts-title">
    <div class="container mfacts__grid">
        <div>
            <p class="t-eyelet section-head__eyelet">{name}</p>
            <h2 class="t-banner" id="facts-title">The figures</h2>
        </div>
        <div>
            {facts(m)}
            <p class="t-legal mfacts__src">As published by Automobili Lamborghini; power and speed in US units.</p>
        </div>
    </div>
</section>
{media(m)}'''


def page(m):
    slug, name = m['slug'], m['name']
    return f'''<!doctype html>
<html lang="en-US">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Lamborghini {name} | Lamborghini Miami, North Miami Beach, FL</title>
    <meta name="description" content="The Lamborghini {name} at Lamborghini Miami, 14780 Biscayne Boulevard, North Miami Beach: enquire with our sales team or configure yours.">
    <meta name="robots" content="noindex">
    <meta name="theme-color" content="#000000">
    <link rel="icon" href="assets/img/bull.svg" type="image/svg+xml">
    <script>
        /* ?figma = static capture mode: no reveals, no Lenis, every image eager (as index_v3.html). */
        if (/[?&]figma\\b/.test(location.search)) {{
            document.documentElement.classList.add('figma');
            document.addEventListener('DOMContentLoaded', () => {{
                document.querySelectorAll('img[loading="lazy"]').forEach((img) => {{ img.loading = 'eager'; }});
            }});
        }} else {{
            document.documentElement.classList.add('js');
        }}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wdth,wght@8..144,25..151,100..1000&display=swap">
    {'' if m.get('story') else f'<link rel="preload" as="image" type="image/webp" imagesrcset="assets/img/showcase-{slug}-800.webp 800w, assets/img/showcase-{slug}-1200.webp 1200w, assets/img/showcase-{slug}-1830.webp 1830w" imagesizes="(min-width: 1024px) 62vw, 100vw" fetchpriority="high">'}
    <link rel="stylesheet" href="https://unpkg.com/lenis@1.3.26/dist/lenis.css">
    <link rel="stylesheet" href="assets/css/tokens_v3.css?v=302">
    <link rel="stylesheet" href="assets/css/main_v3.css?v=320">
    <link rel="stylesheet" href="assets/css/service_v2.css?v=9">
    <link rel="stylesheet" href="assets/css/model_v3.css?v=17">
</head>
<body class="page-model{' page-model--story' if m.get('story') else ''}">

<!-- GENERATED by _tools/build-model-pages.py: edit the template there, not this file. -->
{SPRITE}
<a class="skip-link" href="#main">Skip to content</a>

{HEADER}<main id="main">

{story(m) if m.get('story') else STUDIO(m)}
<!-- ============================ 4 · ENQUIRE ============================
     Sales enquiry for this model, kept with Lamborghini Miami (not lamborghini.com's
     all-dealer form). Every state as on the service page; NOT connected yet. -->
<section class="request band band--dark" id="enquire" aria-labelledby="enquire-title">
    <div class="container">
        <header class="section-head">
            <div>
                <p class="t-eyelet section-head__eyelet">Sales</p>
                <h2 class="t-banner" id="enquire-title"><span class="svc-line">Enquire about</span> <span class="svc-line">the {name}</span></h2>
                <p class="t-lead section-head__lead">Our sales team in Miami will contact you. Or call <a class="spec__link" href="tel:+18332905147">(833) 290-5147</a>.</p>
            </div>
        </header>

        <div class="request__grid">
            <div class="request__form-wrap">
                <form class="form" id="enquire-form" action="#" method="post" novalidate data-enquire-form data-endpoint="">
                    <div class="form__summary" data-no-rise role="alert" tabindex="-1" hidden data-form-summary></div>
                    <div class="form__row">
                        <div class="field">
                            <label class="field__label" for="enq-first">First name <span class="field__req">(required)</span></label>
                            <input class="field__input" id="enq-first" name="first" type="text" autocomplete="given-name" required aria-describedby="enq-first-err">
                            <p class="field__error" data-no-rise id="enq-first-err" hidden></p>
                        </div>
                        <div class="field">
                            <label class="field__label" for="enq-last">Last name <span class="field__req">(required)</span></label>
                            <input class="field__input" id="enq-last" name="last" type="text" autocomplete="family-name" required aria-describedby="enq-last-err">
                            <p class="field__error" data-no-rise id="enq-last-err" hidden></p>
                        </div>
                    </div>
                    <div class="form__row">
                        <div class="field">
                            <label class="field__label" for="enq-email">Email <span class="field__req">(required)</span></label>
                            <input class="field__input" id="enq-email" name="email" type="email" autocomplete="email" required aria-describedby="enq-email-err">
                            <p class="field__error" data-no-rise id="enq-email-err" hidden></p>
                        </div>
                        <div class="field">
                            <label class="field__label" for="enq-phone">Phone <span class="field__req">(required)</span></label>
                            <input class="field__input" id="enq-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="enq-phone-err">
                            <p class="field__error" data-no-rise id="enq-phone-err" hidden></p>
                        </div>
                    </div>
                    <fieldset class="field segmented">
                        <legend class="field__label">Preferred contact <span class="field__req">(required)</span></legend>
                        <div class="segmented__opts">
                            <label class="segmented__opt"><input type="radio" name="prefer" value="call" checked><span>Call</span></label>
                            <label class="segmented__opt"><input type="radio" name="prefer" value="text"><span>Text</span></label>
                            <label class="segmented__opt"><input type="radio" name="prefer" value="email"><span>Email</span></label>
                        </div>
                    </fieldset>
                    <div class="field">
                        <label class="field__label" for="enq-model">Model</label>
                        <select class="field__input field__select" id="enq-model" name="model">
                                {model_options(m)}
                        </select>
                    </div>
                    <div class="field">
                        <label class="field__label" for="enq-message">Message</label>
                        <textarea class="field__input field__textarea" id="enq-message" name="message" rows="4"></textarea>
                    </div>
                    <div class="field field--consent">
                        <label class="check check--consent">
                            <input class="check__input" type="checkbox" name="consent" value="yes" id="enq-consent" required aria-describedby="enq-consent-err">
                            <span class="check__box" aria-hidden="true"></span>
                            <span class="check__label">Please note that by completing this form, you agree to being contacted via text, phone and email. <span class="field__req">(required)</span></span>
                        </label>
                        <p class="field__error" data-no-rise id="enq-consent-err" hidden></p>
                    </div>
                    <div class="form__foot">
                        <button class="btn btn--accent form__submit" type="submit" data-form-submit>
                            <span data-submit-label>Send enquiry</span>
                            <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
                        </button>
                        <p class="form__status" data-no-rise role="status" aria-live="polite" data-form-status></p>
                    </div>
                </form>
                <div class="form-done" tabindex="-1" hidden data-form-done data-no-rise>
                    <p class="t-eyelet section-head__eyelet">Enquiry sent</p>
                    <p class="t-title form-done__title">Thank you<span data-done-name></span>.</p>
                    <p class="t-lead form-done__text">Our sales team will contact you about the {name}. For anything urgent, call <a class="spec__link" href="tel:+18332905147">(833) 290-5147</a>.</p>
                    <button class="btn btn--tertiary form-done__again" type="button" data-form-again><span>Send another enquiry</span></button>
                </div>
            </div>
            <aside class="request__aside" aria-label="Lamborghini Miami sales">
                <address class="request__address">
                    14780 Biscayne Boulevard<br>
                    North Miami Beach, FL 33181
                </address>
                <dl class="spec spec--hours">
                    <div class="spec__row"><dt class="spec__label">Sales</dt><dd class="spec__value"><a href="tel:+18332905147">(833) 290-5147</a></dd></div>
                </dl>
                <a class="btn btn--tertiary request__directions" href="{CONFIGURATOR}" rel="noopener">
                    <span>Configure your {name}</span>
                    <svg class="icon btn__icon" aria-hidden="true"><use href="#i-external"/></svg>
                </a>
            </aside>
        </div>
    </div>
</section>

</main>

{FOOTER}<script src="https://unpkg.com/lenis@1.3.26/dist/lenis.min.js" defer></script>
<script src="assets/js/main_v3.js?v=309" defer></script>
<script src="assets/js/model_v3.js?v=6" defer></script>
</body>
</html>
'''


for m in MODELS:
    out = SITE / f"model-{m['slug']}.html"
    out.write_text(page(m))
    print('wrote', out.name)
