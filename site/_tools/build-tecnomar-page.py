"""Builds tecnomar63.html on the model-page template (model-revuelto.html's shell: head, header, menu, footer,
scripts; model_v3.css / model_v3.js). Copy is the client's, word for word, from lamborghinimiami.aandemo.com/tecnomar63/
(read 6 Nov 2026), typos included ("avant-guarde", "Centro Stiel"); headings are the page's own. Photographs and the
wordmark are the client's (_tools/process-tecnomar.py); the film is Lamborghini's own on YouTube (eY4BGylYrAY)."""
import re
from pathlib import Path
S = Path(__file__).resolve().parents[1]
shell = (S / 'model-revuelto.html').read_text(encoding='utf8')
ZOOM = '<span class="mzoom" aria-hidden="true"><svg class="icon"><use href="#i-expand"/></svg></span>'
NAME = 'Tecnomar for Lamborghini 63'


def pic(role, widths, sizes, alt, cls='', eager=False, portrait=None):
    webp = ', '.join(f'assets/img/models/tecnomar-{role}-{w}.webp {w}w' for w in widths)
    jpg = ', '.join(f'assets/img/models/tecnomar-{role}-{w}.jpg {w}w' for w in widths)
    p = f'\n                    <source media="(max-width: 767.98px) and (orientation: portrait)" type="image/webp" srcset="assets/img/models/tecnomar-{portrait[0]}-{portrait[1]}.webp">' if portrait else ''
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<picture>{p}
                    <source type="image/webp" srcset="{webp}" sizes="{sizes}">
                    <img{f' class="{cls}"' if cls else ''} src="assets/img/models/tecnomar-{role}-{widths[-1]}.jpg" srcset="{jpg}" sizes="{sizes}" {load} decoding="async" alt="{alt}">
                </picture>'''


def cards(lst):
    return ''.join(f'''
            <figure class="mcard">
                <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/tecnomar-{r}-1200.webp" aria-label="Open photo: {title}">
                    {pic(r, (800, 1200), '(min-width: 1024px) 30vw, (min-width: 768px) 45vw, 100vw', alt)}
                    {ZOOM}
                </button>
                <figcaption class="mcard__cap"><span class="mcard__title">{title}</span><span class="mcard__text">{text}</span></figcaption>
            </figure>''' for r, title, text, alt in lst)


EXT_CARDS = [
    ('ext-bow', 'The bow lights', 'The bow lights are a tribute to the concept.', 'The bow of the yacht at speed, its red light line glowing along the hull.'),
    ('ext-hardtop', 'The Hard Top', 'The Hard Top is inspired by Lamborghini’s roadster models; it provides not only protection from the sun and wind but also amazing aerodynamic performance.', 'A black Tecnomar for Lamborghini 63 at speed, its hard top closed, the Miami skyline behind.'),
    ('ext-hull', 'The hull', 'The super-performing hull comes from the design of the team of naval engineers specialized in the study of computational fluid dynamics.', 'A gold Tecnomar for Lamborghini 63 from the stern quarter, on still water below a hillside.'),
]
INT_CARDS = [
    ('int-cabin', 'The Pilot Cabin', 'The Pilot Cabin interprets the automotive cockpit in a nautical key, in which all navigation and monitoring systems are fully integrated. As in the supersport Lamborghini are also the details in carbon fiber, the use of the Carbon Skin, the supersport seats, and the rudder/ steering wheel.', 'The two supersport seats, the steering wheel and the screens of the Pilot Cabin, the sea behind.'),
    ('int-start', '“start&amp;stop”', 'Finally, the unmistakable “start&amp;stop” button (present on the yacht in two units, one per engine) is the same that starts the engine of the Lamborghini Car.', 'The helm of the yacht: the digital instruments, the central screen and the controls.'),
]
GALLERY = [
    ('gallery-1', 'Two Tecnomar for Lamborghini 63 yachts at speed, throwing up spray.'),
    ('gallery-2', 'A green Tecnomar for Lamborghini 63 from above, its cockpit open.'),
    ('gallery-3', 'The stern of the yacht lit at dusk, the Miami skyline behind.'),
    ('gallery-4', 'A seat headrest with the Lamborghini shield, the sea at sunset behind.'),
    ('gallery-5', 'The open deck and its lounge at dusk, under the hard top.'),
    ('gallery-6', 'A green Tecnomar for Lamborghini 63 at speed on open water.'),
]
SPECS = [('Engine Bore (mm)', '128'), ('Engine Displacement (L)', '24'), ('Max Output (hp)', '2000'), ('Rated Speed (rpm)', '2300'),
         ('Width (ft)', '18'), ('Length (ft)', '63'), ('Cruising Speed (KN)', '41'), ('Max Speed (KN)', '60')]
NUMBERS = [('2000', 'hp', 'Max Output (hp)'), ('60', 'kn', 'Max Speed (KN)'), ('41', 'kn', 'Cruising Speed (KN)'), ('63', 'ft', 'Length (ft)')]
VERSIONS = [
    ('Lounge version', 'Open space is the concept, functional and essential, with a fully equipped galley, day head for guests, and storage; a big open space with lounge sofas and wardrobe. Last but not least the owner private bathroom in order to have always your privacy.'),
    ('One cabin version', 'Maintaining the design and style of the lounge version, the galley is divided by the bow area, thus obtaining a king-size bed from the bow sofa. The forward cabin is therefore equipped with large spaces and a dedicated owner bathroom.'),
    ('Two cabin version', 'Two independent cabins is the new solution to optimize spaces and have the best comfort. Master cabin at bow with its king-size maintains comfort levels worthy of a super luxury hotel. The guest cabin was created to accommodate a couple of friends or two children, thanks to the possibility of having two separate singles bed that can be joined together in a large one.'),
]

nums = ''.join(f'''
                <div class="mnum__item"><dt class="mnum__label">{lab}</dt><dd class="mnum__value">{v}<span class="mnum__unit">{u}</span></dd></div>''' for v, u, lab in NUMBERS)
# the four set large are not repeated in the table: it carries the other rows
specs = ''.join(f'''
                <div class="spec__row"><dt class="spec__label">{k}</dt><dd class="spec__value">{v}</dd></div>''' for k, v in SPECS if k not in {lab for _v, _u, lab in NUMBERS})
versions = ''.join(f'''
            <li class="points__item">
                <h3 class="points__title">{t}</h3>
                <p class="points__text">{x}</p>
            </li>''' for t, x in VERSIONS)
gal = ''.join(f'''
            <li class="mgal__item mgal__item--{i}">
                <button class="mgal__open" type="button" data-gal-open="{i - 1}" data-full="assets/img/models/tecnomar-{r}-1600.webp" aria-label="Open photo {i} of {len(GALLERY)}: {alt}">
                    {pic(r, (900, 1600) if r != 'gallery-3' else (900, 1244), '(min-width: 1024px) 50vw, 100vw', alt)}
                    {ZOOM}
                </button>
            </li>''' for i, (r, alt) in enumerate(GALLERY, 1))

MAIN = f'''<main id="main">

<!-- ============================ 1 · TECNOMAR FOR LAMBORGHINI 63 ============================
     Tecnomar (6 Nov 2026, client sheet row 33 "This page needs a design"): the model page, for the yacht.
     Hero: the client's green Tecnomar at speed; on phones, the client's stern at dusk with Miami behind. -->
<section class="mbig tec-hero" aria-labelledby="model-title">
    <div class="mbig__media">
                {pic('hero', (1000, 1600, 1920), '100vw', 'A green Tecnomar for Lamborghini 63 at speed on open water.', 'mbig__img', True, ('hero-p', 660))}
    </div>
    <div class="container mbig__inner">
        <p class="t-eyelet mbig__eyelet">Lamborghini Miami presents</p>
        <h1 class="mbig__name tec-hero__name" id="model-title">
            <img class="tec-hero__mark" src="assets/img/tecnomar-wordmark.webp" width="1621" height="380" alt="Tecnomar for Lamborghini 63">
        </h1>
        <p class="mbig__claim">The future is today</p>
        <p class="mbig__lead">Discover the ultimate automotive yacht</p>
        <div class="mbig__actions">
            <a class="btn btn--accent" href="#inquire"><span>Inquire</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
            <a class="btn btn--secondary" href="#film"><span>Watch the film</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </div>
    </div>
</section>

<!-- ============================ 2 · THE YACHT, IN FIGURES ============================
     The client's opening paragraph and the Technical Features table, every row as published. -->
<section class="mnum band band--black tec-num" aria-labelledby="facts-title">
    <div class="container mnum__grid">
        <header class="mnum__head tec-num__head">
            <h2 class="t-banner" id="facts-title">Technical Features</h2>
            <div class="tec-num__text">
                <p>The Yacht “Tecnomar for Lamborghini 63“ is not simply an exercise in style and design but she also represents the avant-guarde of luxury speed boats. Inspired by the performance of Lamborghini supersport cars, there are two innovative elements at the basis of her design concept: speed and dynamic weight. The two engines MAN V 12 – 2000HP allow the yacht to reach the impressive speed of 60 knots, while the use of carbon fiber (a typical element of the cars of Sant’Agata Bolognese) guarantees the classification in the range of ultralight boats with a maximum weight of 24 tons for 63 feet in length.</p>
                <p>Terzo Millennio, Sián FKP 37: these are the main inspirations.</p>
            </div>
        </header>
        <dl class="mnum__list">{nums}
        </dl>
        <dl class="spec tec-num__specs">{specs}
        </dl>
    </div>
</section>

<!-- ============================ 3 · EXTERIORS ============================ -->
<section class="mstory band band--dark" id="exterior" aria-labelledby="ext-title" data-gallery>
    <div class="container mstory__head">
        <div>
            <h2 class="t-banner" id="ext-title">Exteriors</h2>
        </div>
        <p class="t-lead mstory__text">The design of the EXTERIORS is the result of the close collaboration between the two Centro Stiel and has led to the creation of a cutting-edge silhouette, completely out of any typical nautical scheme. The super-performing hull comes from the design of the team of naval engineers specialized in the study of computational fluid dynamics while the hull and superstructure were relaunched in a contemporary form while keeping the lines created by designer Marcello Gandini for the iconic Lamborghini cars Miura and Countach from the ’60s and ’70s.</p>
    </div>
    <figure class="mstory__wide">
        <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/tecnomar-exterior-1320.webp" aria-label="Open photo: the yacht at speed">
            {pic('exterior', (1000, 1320), '100vw', 'A gold Tecnomar for Lamborghini 63 at speed below a hillside, spray at its stern.')}
            {ZOOM}
        </button>
    </figure>
    <div class="container mstory__cards mstory__cards--3">{cards(EXT_CARDS)}
    </div>
</section>

<!-- ============================ 4 · INTERIORS ============================ -->
<section class="mstory band band--black" id="interior" aria-labelledby="int-title" data-gallery>
    <div class="container mstory__head">
        <div>
            <h2 class="t-banner" id="int-title">Interiors</h2>
        </div>
        <p class="t-lead mstory__text">The INTERIORS are the result of a high-tech design based on the use of high-tech materials in terms of weight and functionality, perfectly combined with the best craftsmanship tradition of Made-In-Italy. The unmistakably automotive inspiration proposes iconic elements of the Lamborghini design, such as hexagons, clean lines, and the Y. Colors and materials are, 100% customizable through the program Ad Personam.</p>
    </div>
    <div class="container">
        <figure class="mstory__main">
            <button class="mcard__open" type="button" data-gal-open data-full="assets/img/models/tecnomar-interior-1600.webp" aria-label="Open photo: the Pilot Cabin">
                {pic('interior', (1000, 1600, 1920), '(min-width: 1440px) 1320px, 100vw', 'The Pilot Cabin at night: two supersport seats and the helm, the Miami skyline behind.', '', False, ('interior-p', 700))}
                {ZOOM}
            </button>
        </figure>
    </div>
    <div class="container mstory__cards mstory__cards--2">{cards(INT_CARDS)}
    </div>
    <div class="container mcta__row">
        <a class="btn btn--accent" href="#inquire"><span>Inquire</span><svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg></a>
        <a class="btn btn--tertiary" href="ad-personam.html"><span>Ad Personam</span></a>
    </div>
</section>

<!-- ============================ 5 · THREE VARIANTS ============================
     The client's three versions, on the light band, as the service page's rule-topped columns. -->
<section class="difference band band--light tec-versions" aria-labelledby="versions-title">
    <div class="container">
        <header class="section-head">
            <div>
                <p class="t-lead tec-versions__intro" id="versions-title">The yacht “Tecnomar for Lamborghini 63” is available in three main variants:</p>
            </div>
        </header>
        <ul class="points tec-versions__list">{versions}
        </ul>
    </div>
</section>

<!-- ============================ 6 · GALLERY ============================ -->
<section class="mgal band band--dark" aria-label="{NAME}, photographs">
    <div class="container">
        <ol class="mgal__grid" data-gallery>{gal}
        </ol>
    </div>
</section>
<!-- gallery lightbox: one photo at a time, ← → / swipe / Esc; model_v3.js -->
<dialog class="glb" aria-label="{NAME} gallery" data-gallery-box data-lenis-prevent>
    <figure class="glb__stage">
        <img class="glb__img" alt="" data-glb-img>
        <figcaption class="glb__cap"><span class="glb__n" data-glb-n>1 / {len(GALLERY)}</span> <span data-glb-cap></span></figcaption>
    </figure>
    <button class="glb__btn glb__btn--prev" type="button" data-glb-prev aria-label="Previous photo"><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    <button class="glb__btn glb__btn--next" type="button" data-glb-next aria-label="Next photo"><svg class="icon" aria-hidden="true"><use href="#i-arrow"/></svg></button>
    <button class="glb__close" type="button" data-glb-close aria-label="Close gallery"><svg class="icon" aria-hidden="true"><use href="#i-close"/></svg></button>
</dialog>

<!-- ============================ 7 · FILM ============================
     Lamborghini's film on YouTube, as embedded on the client's page; it loads only on Play. -->
<section class="mmedia band band--black" id="film" aria-label="{NAME}, film">
    <div class="container">
            <div class="mfilm" data-yt="eY4BGylYrAY" data-yt-title="Introducing the phenomenal Tecnomar for Lamborghini 63">
                <img class="mfilm__poster" src="https://i.ytimg.com/vi/eY4BGylYrAY/maxresdefault.jpg" width="1280" height="720" loading="lazy" decoding="async" alt="">
                <button class="mfilm__play" type="button" data-yt-play aria-label="Play the film Introducing the phenomenal Tecnomar for Lamborghini 63 (YouTube)">
                    <svg class="icon" aria-hidden="true"><use href="#i-play"/></svg><span>Watch the film</span>
                </button>
            </div>
    </div>
</section>
'''

# the enquiry: the model page's own form, for the yacht
form = re.search(r'<!-- =+ \d+ · INQUIRE =+.*?</section>\n', shell, re.S) or re.search(r'<section class="request band band--dark" id="inquire".*?</section>\n', shell, re.S)
form = form.group(0)
form = form.replace('<span class="svc-line">Inquire about</span> <span class="svc-line">the Revuelto</span>', '<span class="svc-line">Tecnomar for</span> <span class="svc-line">Lamborghini 63</span>')
form = form.replace('<p class="t-eyelet section-head__eyelet">Sales</p>', '<p class="t-eyelet section-head__eyelet">Inquire</p>')
form = re.sub(r'<select class="field__input field__select" id="enq-model" name="model">.*?</select>',
              '<select class="field__input field__select" id="enq-model" name="model">\n                                    <option selected>Tecnomar for Lamborghini 63</option>\n                                    <option>Revuelto</option>\n                                    <option>Revuelto SV</option>\n                                    <option>Temerario</option>\n                                    <option>Urus SE</option>\n                                    <option>Urus SE Performante</option>\n                                    <option>Other</option>\n                            </select>', form, flags=re.S)
form = form.replace('about the Revuelto.', 'about the Tecnomar for Lamborghini 63.')
form = re.sub(r'\s*<a class="btn btn--tertiary request__directions" href="https://configurator.lamborghini.com/".*?</a>', '', form, flags=re.S)
assert 'Revuelto</option>' in form and 'Revuelto.' not in form

page = re.sub(r'<main id="main">.*?</main>', lambda m: MAIN + '\n' + form + '\n</main>', shell, count=1, flags=re.S)
page = page.replace('<title>Lamborghini Revuelto | Lamborghini Miami, North Miami Beach, FL</title>', f'<title>{NAME} | Lamborghini Miami, North Miami Beach, FL</title>')
page = page.replace('<meta name="description" content="The Lamborghini Revuelto at Lamborghini Miami, 14780 Biscayne Boulevard, North Miami Beach: inquire with our sales team or configure yours.">',
                    f'<meta name="description" content="Lamborghini Miami presents the {NAME} in North Miami Beach, FL: the future is today. Discover the ultimate automotive yacht.">')
page = page.replace('<!-- GENERATED by _tools/build-model-pages.py: edit the template there, not this file. -->', '<!-- GENERATED by _tools/build-tecnomar-page.py: edit it there, not this file. -->')
page = page.replace('<link rel="stylesheet" href="assets/css/model_v3.css?v=23">', '<link rel="stylesheet" href="assets/css/model_v3.css?v=23">\n    <link rel="stylesheet" href="assets/css/tecnomar_v3.css?v=2">\n    <link rel="preload" as="image" type="image/webp" media="(min-width: 768px), (orientation: landscape)" imagesrcset="assets/img/models/tecnomar-hero-1000.webp 1000w, assets/img/models/tecnomar-hero-1600.webp 1600w, assets/img/models/tecnomar-hero-1920.webp 1920w" imagesizes="100vw" fetchpriority="high">')
page = page.replace('<body class="page-model page-model--story">', '<body class="page-model page-model--story page-tecnomar">')
# chrome: About us and Our story are pages now (the shell carries them since the 6 Nov sweep; added only if missing)
if 'href="about.html"' not in page:
    page = page.replace('<li><a class="menu__link" href="lifestyle.html">Lifestyle</a></li>', '<li><a class="menu__link" href="about.html">About us</a></li>\n                    <li><a class="menu__link" href="lifestyle.html">Lifestyle</a></li>', 1)
    page = page.replace('<li><a href="lifestyle.html">Lifestyle</a></li>', '<li><a href="about.html">About us</a></li>\n                        <li><a href="lifestyle.html">Lifestyle</a></li>', 1)
page = page.replace('<a class="menu__link" href="index_v4.html#house">Our story</a>', '<a class="menu__link" href="our-story.html">Our story</a>')
page = page.replace('<a href="index_v4.html#house">Our story</a>', '<a href="our-story.html">Our story</a>')
for needle in ('our-story.html">Our story', 'about.html">About us', 'tecnomar-wordmark', 'enq-model'):
    assert needle in page, needle
(S / 'tecnomar63.html').write_text(page, encoding='utf8', newline='\n')
print('tecnomar63.html', len(page))
