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
    dict(slug='urus-se-performante', name='Urus SE Performante', mark='Performante', mk='0.68',
         claim='Urus at its peak',
         facts=[('Max power', '801 hp'), ('Top speed', '194 mph'), ('0–62 mph', '3.3 s')],
         art_alt='Lamborghini Urus SE Performante in yellow-green with a carbon bonnet, front three-quarter view.',
         media=dict(kind='youtube', id='5ZtLH3s8Wvg', title='Urus SE Performante film'),
         note='Film: the YouTube link the client sent (it loads only on click). The enquiry form is a mock-up and is not connected: the client wants it to feed a DriveCentric campaign.'),
    dict(slug='revuelto', name='Revuelto', mark='Revuelto', mk='1',
         claim='The quantum of driving',
         facts=[('Max power', '1,001 hp'), ('Top speed', '>217 mph'), ('0–62 mph', '2.5 s')],
         art_alt='Lamborghini Revuelto in orange, front three-quarter view, its Y-shaped headlights lit.',
         media=dict(kind='photo', src='hero-dealer-alex', w=1920, h=1080,
                    alt='A yellow Lamborghini Revuelto in side profile between factory buildings.'),
         note='The enquiry form is a mock-up and is not connected (DriveCentric later).'),
    dict(slug='revuelto-sv', name='Revuelto SV', mark='Revuelto SV', mk='0.62',
         claim='Hockenheim record holder',
         facts=[('Hockenheimring lap', '1:41.6')],
         art_alt='Lamborghini Revuelto SV in grey and black carbon fibre with red accents, front three-quarter view.',
         media=None,
         note='No hp / mph / 0–62 published for the SV yet (lamborghini.com has only the Hockenheim lap, 6 Aug 2026), and no SV photography or film: the page has no media band until the client sends some. The enquiry form is a mock-up and is not connected (DriveCentric later).'),
]
ORDER = ['revuelto', 'revuelto-sv', 'urus-se-performante']


def chunk(start, end):
    a = SVC.index(start)
    return SVC[a:SVC.index(end, a)]


SPRITE = chunk('<svg class="sprite"', '<a class="skip-link"')
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
    <link rel="preload" as="image" type="image/webp" imagesrcset="assets/img/showcase-{slug}-800.webp 800w, assets/img/showcase-{slug}-1200.webp 1200w, assets/img/showcase-{slug}-1830.webp 1830w" imagesizes="(min-width: 1024px) 62vw, 100vw" fetchpriority="high">
    <link rel="stylesheet" href="https://unpkg.com/lenis@1.3.26/dist/lenis.css">
    <link rel="stylesheet" href="assets/css/tokens_v3.css?v=302">
    <link rel="stylesheet" href="assets/css/main_v3.css?v=315">
    <link rel="stylesheet" href="assets/css/service_v2.css?v=9">
    <link rel="stylesheet" href="assets/css/model_v3.css?v=6">
</head>
<body class="page-model">

<!-- GENERATED by _tools/build-model-pages.py: edit the template there, not this file. -->
{SPRITE}
<a class="skip-link" href="#main">Skip to content</a>

{HEADER}<main id="main">

<!-- ============================ 1 · THE MODEL ============================
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
                <a class="btn btn--tertiary" href="srp.html?condition=new"><span>View inventory</span></a>
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
{media(m)}
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
                <p class="dev-note" data-dev-note><b>Note for Alex</b> {m['note']}</p>
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
<script src="assets/js/main_v3.js?v=307" defer></script>
<script src="assets/js/model_v3.js?v=4" defer></script>
</body>
</html>
'''


for m in MODELS:
    out = SITE / f"model-{m['slug']}.html"
    out.write_text(page(m))
    print('wrote', out.name)
