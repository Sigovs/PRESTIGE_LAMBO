#!/usr/bin/env python3
"""v3 Lifestyle page (client, Oct 2026): "Lifestyle by Lamborghini" — promote the events the
dealership does for Lamborghini with a series of event films, and get people onto the
newsletter (first name, last name, email, phone).

    python3 _tools/build-lifestyle-page.py

Builds lifestyle.html. Header, menu and footer are lifted from service.html, as the model
pages are. Films: the Revuelto launch is the client's own file and streams from their
Dropbox (Alex: big films stay on Dropbox, not on our server); the other four are the
YouTube links the client sent, titled as YouTube titles them. The form is a mock-up (NOT
connected)."""
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SVC = (SITE / 'service.html').read_text()
LAUNCH = 'https://www.dropbox.com/scl/fi/5fgo02y7z3g1ryk9h0ga7/REVUELTO-LAUNCH.mp4?rlkey=aotj3dorcynsq6u4oj4t3j9a3&amp;raw=1'

FILMS = [
    dict(kind='file', src=LAUNCH, poster='assets/video/revuelto-launch-poster-d.webp', place='Lamborghini Miami',
         title='The Revuelto unveiling', text='Our launch night for the Revuelto, in the showroom on Biscayne Boulevard.'),
    dict(kind='yt', id='gurkbOVaYIc', place='Lamborghini', title='#SHEdrivesalambo',
         text='A celebration dedicated to women who drive Lamborghini.'),
    dict(kind='yt', id='jpmvl3w4ZKU', place='Napa Valley', title='Esperienza Terra',
         text='Lamborghini Esperienza Terra, in the Napa Valley.'),
    dict(kind='yt', id='egjLBe6lMXU', place='Vallelunga', title='Lamborghini Accademia',
         text='The Lamborghini Accademia racing experience, at Vallelunga.'),
    dict(kind='yt', id='2g9XCfy_LMo', place='New England', title='Esperienza Giro',
         text='Lamborghini Esperienza Giro USA, through New England.'),
]


def chunk(start, end):
    a = SVC.index(start)
    return SVC[a:SVC.index(end, a)]


SPRITE = chunk('<svg class="sprite"', '<a class="skip-link"')
SPRITE = SPRITE.replace('</svg>', '    <symbol id="i-play" viewBox="0 0 24 24"><path d="M7 4.5v15L19.5 12Z" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="miter"/></symbol>\n</svg>', 1)
HEADER = chunk('<!-- ============================ HEADER', '<main id="main">')
FOOTER = chunk('<!-- ============================ FOOTER', '<script src="https://unpkg.com/lenis')
HEADER = HEADER.replace(' aria-current="page"', '').replace('href="#request">Contact', 'href="#newsletter">Contact')
HEADER = HEADER.replace('<li><a class="menu__link" href="#request" data-menu-link>Schedule service</a></li>',
                        '<li><a class="menu__link" href="service.html#request">Schedule service</a></li>')
HEADER = HEADER.replace('<li><a class="menu__link" href="lifestyle.html">Lifestyle</a></li>',
                        '<li><a class="menu__link" href="lifestyle.html" aria-current="page">Lifestyle</a></li>')
FOOTER = FOOTER.replace(' aria-current="page"', '').replace('<li><a href="#request">Schedule service</a></li>',
                                                           '<li><a href="service.html#request">Schedule service</a></li>')


def card(f, i):
    poster = f'https://i.ytimg.com/vi/{f["id"]}/maxresdefault.jpg'
    return f'''            <li class="event">
                <button class="event__media" type="button" data-film-open data-yt="{f['id']}" data-film-title="{f['title']}" aria-label="Play {f['title']} (YouTube)">
                    <img src="{poster}" width="1280" height="720" loading="lazy" decoding="async" alt="">
                    <span class="event__play" aria-hidden="true"><svg class="icon"><use href="#i-play"/></svg></span>
                </button>
                <p class="event__place">{f['place']}</p>
                <h4 class="event__title">{f['title']}</h4>
                <p class="event__text">{f['text']}</p>
            </li>'''


def feature(f):
    return f'''        <article class="efeature">
            <button class="efeature__media" type="button" data-film-open data-src="{f['src']}" data-poster="{f['poster']}" data-film-title="{f['title']}" aria-label="Play {f['title']} (film)">
                <img src="{f['poster']}" width="1920" height="1080" loading="lazy" decoding="async" alt="">
                <span class="efeature__play" aria-hidden="true"><svg class="icon"><use href="#i-play"/></svg><span>Watch the film</span></span>
            </button>
            <div class="efeature__text">
                <p class="event__place">{f['place']} · Our event</p>
                <h3 class="efeature__title">{f['title']}</h3>
                <p class="event__text">{f['text']}</p>
            </div>
        </article>'''


def page():
    cards = '\n'.join(card(f, i) for i, f in enumerate(FILMS[1:]))
    return f'''<!doctype html>
<html lang="en-US">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Lifestyle by Lamborghini | Lamborghini Miami, North Miami Beach, FL</title>
    <meta name="description" content="Lifestyle by Lamborghini at Lamborghini Miami: the events we do for Lamborghini, from our Revuelto unveiling to Esperienza and Accademia. Join the list to hear about the next one.">
    <meta name="robots" content="noindex">
    <meta name="theme-color" content="#000000">
    <link rel="icon" href="assets/img/bull.svg" type="image/svg+xml">
    <script>
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
    <link rel="stylesheet" href="https://unpkg.com/lenis@1.3.26/dist/lenis.css">
    <link rel="stylesheet" href="assets/css/tokens_v3.css?v=302">
    <link rel="stylesheet" href="assets/css/main_v3.css?v=320">
    <link rel="stylesheet" href="assets/css/service_v2.css?v=9">
    <link rel="stylesheet" href="assets/css/model_v3.css?v=6">
</head>
<body class="page-model page-lifestyle">

<!-- GENERATED by _tools/build-lifestyle-page.py: edit the template there, not this file. -->
{SPRITE}
<a class="skip-link" href="#main">Skip to content</a>

{HEADER}<main id="main">

<!-- ============================ 1 · LIFESTYLE ============================
     The subject is the car at our own event: the Revuelto unveiling (the client's film, 0:23.5-0:32.4:
     the cover comes off, doors up) fills the screen; the copy sits low left on a floor-up scrim, so
     the film reads above it. Reduced motion keeps the poster (the car with its doors up). -->
<section class="lhero" aria-labelledby="life-title">
    <div class="lhero__media" aria-hidden="true">
        <video class="lhero__video" muted playsinline loop preload="none" poster="assets/video/revuelto-launch-poster-d.webp" data-loop
               data-src-d="assets/video/revuelto-launch-loop-d.mp4" data-src-m="assets/video/revuelto-launch-loop-m.mp4" data-poster-m="assets/video/revuelto-launch-poster-m.webp"></video>
    </div>
    <div class="container lhero__inner">
        <p class="t-eyelet lhero__eyelet">Lamborghini Miami</p>
        <h1 class="t-display-xl lhero__title" id="life-title"><span class="subhero__line">Lifestyle</span> <span class="subhero__line">by Lamborghini</span></h1>
        <div class="lhero__foot">
            <p class="t-lead lhero__lead">The events we do for Lamborghini, in Miami and beyond.</p>
            <div class="lhero__actions">
                <a class="btn btn--accent" href="#newsletter"><span>Join the list</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
                <a class="btn btn--secondary" href="#events"><span>Our events</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
            </div>
        </div>
    </div>
</section>

<!-- ============================ 2 · EVENTS ============================
     One feature and one row: our own event, the Revuelto unveiling, as a full-width cinema frame;
     then the four Lamborghini events, as four equal films. -->
<section class="events band band--dark" id="events" aria-labelledby="events-title">
    <div class="container">
        <header class="events__head">
            <div>
                <p class="t-eyelet section-head__eyelet">Lifestyle by Lamborghini</p>
                <h2 class="t-banner" id="events-title">Our events</h2>
            </div>
            <p class="t-lead events__intro">Unveilings in our showroom, drives and track days with Lamborghini. Each one on film.</p>
        </header>

{feature(FILMS[0])}

        <h3 class="events__sub">With Lamborghini</h3>
        <ol class="events__row">
{cards}
        </ol>
    </div>
</section>

<!-- ============================ 3 · NEWSLETTER ============================
     The client's ask: get people onto the newsletter. First name, last name, email, phone.
     Every state as the enquiry forms; NOT connected yet. -->
<section class="request band band--black newsletter" id="newsletter" aria-labelledby="news-title">
    <div class="container newsletter__grid">
        <header class="newsletter__head">
            <div>
                <p class="t-eyelet section-head__eyelet">Newsletter</p>
                <h2 class="t-banner" id="news-title"><span class="svc-line">Hear about</span> <span class="svc-line">the next one</span></h2>
                <p class="t-lead newsletter__lead">Join the Lamborghini Miami list for invitations to what comes next.</p>
                <ul class="newsletter__list">
                    <li>Unveilings in our showroom</li>
                    <li>Drives and track days with Lamborghini</li>
                </ul>
            </div>
        </header>
        <div class="newsletter__form">
            <div class="request__form-wrap">
                <form class="form" id="news-form" action="#" method="post" novalidate data-enquire-form data-endpoint="" data-fail="You could not be added just now. Please try again, or call (833) 290-5147.">
                    <div class="form__summary" data-no-rise role="alert" tabindex="-1" hidden data-form-summary></div>
                    <div class="form__row">
                        <div class="field">
                            <label class="field__label" for="nl-first">First name <span class="field__req">(required)</span></label>
                            <input class="field__input" id="nl-first" name="first" type="text" autocomplete="given-name" required aria-describedby="nl-first-err">
                            <p class="field__error" data-no-rise id="nl-first-err" hidden></p>
                        </div>
                        <div class="field">
                            <label class="field__label" for="nl-last">Last name <span class="field__req">(required)</span></label>
                            <input class="field__input" id="nl-last" name="last" type="text" autocomplete="family-name" required aria-describedby="nl-last-err">
                            <p class="field__error" data-no-rise id="nl-last-err" hidden></p>
                        </div>
                    </div>
                    <div class="form__row">
                        <div class="field">
                            <label class="field__label" for="nl-email">Email <span class="field__req">(required)</span></label>
                            <input class="field__input" id="nl-email" name="email" type="email" autocomplete="email" required aria-describedby="nl-email-err">
                            <p class="field__error" data-no-rise id="nl-email-err" hidden></p>
                        </div>
                        <div class="field">
                            <label class="field__label" for="nl-phone">Phone <span class="field__req">(required)</span></label>
                            <input class="field__input" id="nl-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="nl-phone-err">
                            <p class="field__error" data-no-rise id="nl-phone-err" hidden></p>
                        </div>
                    </div>
                    <div class="field field--consent">
                        <label class="check check--consent">
                            <input class="check__input" type="checkbox" name="consent" value="yes" id="nl-consent" required aria-describedby="nl-consent-err">
                            <span class="check__box" aria-hidden="true"></span>
                            <span class="check__label">Please note that by completing this form, you agree to being contacted via text, phone and email. <span class="field__req">(required)</span></span>
                        </label>
                        <p class="field__error" data-no-rise id="nl-consent-err" hidden></p>
                    </div>
                    <div class="form__foot">
                        <button class="btn btn--accent form__submit" type="submit" data-form-submit>
                            <span data-submit-label>Join the list</span>
                            <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
                        </button>
                        <p class="form__status" data-no-rise role="status" aria-live="polite" data-form-status></p>
                    </div>
                </form>
                <div class="form-done" tabindex="-1" hidden data-form-done data-no-rise>
                    <p class="t-eyelet section-head__eyelet">You are on the list</p>
                    <p class="t-title form-done__title">Thank you<span data-done-name></span>.</p>
                    <p class="t-lead form-done__text">We will be in touch about the next Lamborghini Miami event.</p>
                    <button class="btn btn--tertiary form-done__again" type="button" data-form-again><span>Add someone else</span></button>
                </div>
            </div>
        </div>
    </div>
</section>

</main>

<!-- The film lightbox: one for every film on the page (a file, or a YouTube embed). -->
<dialog class="film" aria-label="Film" data-film data-lenis-prevent>
    <button class="film__close" type="button" data-film-close><svg class="icon" aria-hidden="true"><use href="#i-close"/></svg><span class="visually-hidden">Close video</span></button>
    <div class="film__stage" data-film-stage></div>
</dialog>

{FOOTER}<script src="https://unpkg.com/lenis@1.3.26/dist/lenis.min.js" defer></script>
<script src="assets/js/main_v3.js?v=307" defer></script>
<script src="assets/js/model_v3.js?v=4" defer></script>
<script src="assets/js/lifestyle_v3.js?v=1" defer></script>
</body>
</html>
'''


(SITE / 'lifestyle.html').write_text(page())
print('wrote lifestyle.html')
