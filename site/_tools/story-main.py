"""Our Story main content. Copy is the client's, word for word: lamborghinimiami.aandemo.com/our-story/ (read 6 Nov 2026)
for the text, the quote and the 1980-2020 captions; the client's October archive list (as on index_v4.html) for the
Lamborghini years. Headings are the page's own two: the H1 and "Our history in pictures"."""
from pathlib import Path
from html import escape
IMG = Path(__file__).resolve().parents[1] / 'assets/img'

# (year shown, [(file base, width, alt, caption)])
TIMELINE = [
    ('1980', [('archive-1980', 640, 'Irv David smiling in front of the original Prestige Motor Car Imports sign.', '1980, Irv David proudly standing in-front of the original Prestige Imports on West Dixie Highway.'),
              ('story-1980s', 640, 'The early Prestige Motor Car Imports showroom, cars parked along the street.', "Irv grew Prestige Imports to have Miami's finest exotic used-car inventory.")]),
    ('1983', [('archive-1983', 640, 'A sign on an empty lot reading Future New Home of Prestige Motorcar Imports.', '1983 when Irv purchased the land on Biscayne Boulevard, where a simple trailer served as a temporary sales office.')]),
    ('1985', [('story-1985', 640, 'The Prestige Imports showroom under construction: a steel frame on bare ground.', '1985, as the construction of the new Prestige Imports showroom was coming to life.')]),
    ('1986', [('archive-1986', 640, 'Night-time grand opening of the Prestige Imports showroom, with guests and cars outside.', '1986, outside the grand opening of the new Prestige Imports Showroom.'),
              ('story-1986-opening', 640, 'Guests inside the new showroom at the grand opening, a red Ferrari in front.', "1986, when Irv had the grand opening of the new Prestige Imports showroom and birthed Miami's supercar scene.")]),
    ('1988', [('archive-1988', 1280, 'Irv David seated in a white Lamborghini Countach, its doors raised.', 'Irv David secures the Lamborghini franchise for Miami.')]),
    ('1990', [('archive-1990', 1280, 'Ferruccio Lamborghini, in glasses and a dark suit, signing a book at a table.', 'Ferruccio Lamborghini signs a book for Irv David at the Diablo unveiling in Monte Carlo.')]),
    ('2002', [('story-2002', 640, 'The concrete frame and roof trusses of the Prestige Audi building under construction.', '2002, the construction of the Prestige Audi building at 14780 Biscayne Blvd.')]),
    ('2007', [('archive-2007', 640, 'A Lamborghini Gallardo covered in hand-drawn black-and-white Sharpie patterns.', 'The “Sharpie Lamborghini” by Jonah Cerwinske, commissioned by Brett David.')]),
    ('2013', [('archive-2013', 640, 'A green Lamborghini Aventador raised on a lift in the Lamborghini Miami workshop.', 'The Lamborghini Aventador Roadster is unveiled in Miami.')]),
    ('2014', [('story-2014', 1280, 'A silver Lamborghini Veneno with its doors raised, on a turntable in the showroom.', 'Delivery of the second of three Lamborghini Veneno Coupés.')]),
    ('2020', [('story-2020-showroom', 516, 'The glass front of the new Lamborghini Miami showroom, yellow cars inside.', '2020,  the completion of the all new Lamborghini Miami showroom.'),
              ('story-2020-brett', 516, 'Brett David by the Irv David Way street sign, a green Lamborghini beside him.', "2020, our CEO Brett David overseeing his family's dreams continue to grow.")]),
    ('2021', [('archive-2021', 1280, 'A grey Lamborghini Sián with its doors raised under the lit Lamborghini Miami sign at night.', 'Delivery of one of 63 Lamborghini Sián Coupés.')]),
    ('2022', [('story-2022', 1280, 'The Tecnomar for Lamborghini 63 yacht on the water in Miami.', 'Delivery of a Tecnomar for Lamborghini 63.')]),
    ('2024', [('archive-2024-trofeo', 640, 'Lamborghini Huracán Super Trofeo race cars at the start, an orange car leading.', 'The first Super Trofeo World Championship.'),
              ('archive-2024-movember', 1280, 'A red Lamborghini Countach with a painted moustache on a Miami street lined with palms.', 'Number one in Movember fundraising worldwide.')]),
    ('2025', [('story-2025', 1280, 'A white and purple Lamborghini Sián with its doors raised, in a studio.', 'Officially the number one US dealer for sales and service.')]),
]

def picture(base, w, alt, sizes):
    srcs = sorted({int(p.stem.rsplit('-', 1)[1]) for p in IMG.glob(f'{base}-*.jpg') if p.stem.rsplit('-', 1)[1].isdigit() and p.stem.rsplit('-', 1)[0] == base})
    assert srcs, base
    assert all((IMG / f'{base}-{s}.webp').exists() for s in srcs), base
    small = srcs[0]
    hi = srcs[-1]
    h = round(hi * (344 / 516 if base.startswith('story-2020') else 741 / 1112 if base in ('story-2014', 'story-2022', 'story-2025') else 427 / 640))
    webp = ', '.join(f'assets/img/{base}-{s}.webp {s}w' for s in reversed(srcs))
    jpg = ', '.join(f'assets/img/{base}-{s}.jpg {s}w' for s in reversed(srcs))
    return (f'<picture><source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="assets/img/{base}-{small}.jpg" srcset="{jpg}" sizes="{sizes}" width="{hi}" height="{h}" loading="lazy" decoding="async" alt="{escape(alt)}"></picture>')

def film():
    """One frame per photograph, in order; the year shows on the first frame of each year."""
    out = []
    n = sum(len(items) for _y, items in TIMELINE)
    k = 0
    for year, items in TIMELINE:
        for j, (base, w, alt, cap) in enumerate(items):
            k += 1
            hi = w >= 1280 or w >= 1112
            sizes = '(min-width: 1024px) 34rem, 100vw' if hi else '(min-width: 1024px) 24rem, 100vw'
            text = escape(cap, quote=False).replace('  ', '&nbsp; ').replace('Tecnomar for Lamborghini 63', '<a class="spec__link" href="tecnomar63.html">Tecnomar for Lamborghini 63</a>')
            out.append(f'''            <li class="film__frame{' film__frame--hi' if hi else ''}" data-year="{year}">
                <figure class="film__fig">{f"""
                    <p class="film__year">{year}</p>""" if j == 0 else ''}
                    <div class="film__print">{picture(base, w, alt, sizes)}</div>
                    <figcaption class="film__cap"><span class="film__y">{year}</span><span class="film__text">{text}</span></figcaption>
                </figure>
            </li>''')
    return '\n'.join(out)


DECADES = ['1990', '2000', '2010', '2020']   # 1980 is where the rule starts, beside the current year

MAIN = f'''<main id="main">

<!-- ============================ 1 · HERO ============================
     Our Story (6 Nov 2026, client sheet row 26 "Design"): the department template. The frame is the
     Prestige Imports archive portrait of Irv David in a Countach, already used on the homepage. -->
<section class="subhero story-hero" aria-labelledby="story-title">
    <div class="subhero__media">
        <picture>
            <source media="(min-width: 1200px), (min-width: 768px) and (orientation: landscape)" type="image/webp" srcset="assets/img/slide-prestige-3-1920.webp">
            <source media="(min-width: 1200px), (min-width: 768px) and (orientation: landscape)" srcset="assets/img/slide-prestige-3-1920.jpg">
            <source type="image/webp" srcset="assets/img/slide-prestige-3-p-800.webp">
            <img class="subhero__img" src="assets/img/slide-prestige-3-p-800.jpg" width="800" height="943" fetchpriority="high" decoding="async"
                 alt="Irv David seated in a white Lamborghini Countach with its doors raised, outside the early Prestige Imports.">
        </picture>
    </div>
    <div class="container subhero__inner">
        <div class="subhero__group">
            <h1 class="t-display-xl subhero__title" id="story-title">
                <span class="subhero__line">Lamborghini Miami</span>
                <span class="subhero__line">History</span>
                <span class="subhero__line">North Miami Beach FL</span>
            </h1>
            <div class="subhero__actions">
                <a class="btn btn--accent" href="#pictures">
                    <span>Our history in pictures</span>
                    <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
                </a>
                <a class="btn btn--secondary" href="about.html">
                    <span>About us</span>
                    <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
                </a>
            </div>
        </div>
    </div>
</section>

<!-- ============================ 2 · THE STORY ============================
     Redone 6 Nov 2026 (Alex: a wall of text). The client's four paragraphs, word for word, in their
     order, as three chapters: each beside a photograph that fills the height of its text, alternating
     sides; the first sentence of each chapter set large. Photographs: the Prestige Imports archive
     portraits of Irv David (as on the homepage) and the 2020 showroom opening. -->
<section class="chap band band--dark" aria-label="The story of Prestige Imports, part 1 of 3">
    <div class="container chap__grid">
        <figure class="chap__media" data-reveal>
            <picture>
                    <source media="(min-width: 768px)" type="image/webp" srcset="assets/img/slide-prestige-2-1920.webp">
                    <source media="(min-width: 768px)" srcset="assets/img/slide-prestige-2-1920.jpg">
                    <source type="image/webp" srcset="assets/img/slide-prestige-2-p-800.webp">
                    <img src="assets/img/slide-prestige-2-p-800.jpg" width="800" height="943" loading="lazy" decoding="async" alt="Irv David standing beside a white Lamborghini Countach outside the early Prestige Imports.">
                </picture>
        </figure>
        <div class="chap__body">
            <p class="chap__lead">Over 45 years ago, Prestige Imports established itself as a leader and innovator of the luxury automobile world.</p>
            <div class="chap__text"><p>Founded by Irv David, upon principles of excellent service and personal commitment to customer satisfaction, it has since expanded into one of the most successful auto groups in the country. Before Prestige Imports became what it is today, the business started from a gas station that Mr. David owned evolving into a dealership selling used European cars. Mr. David envisioned selling more than the typical vehicles and invested his time and energy in what he saw as an untapped market, but his drive and enthusiasm paid off. He made his dream a reality by becoming a pioneer in the exotic car market opening one of the first exotic car dealerships in Florida.</p></div>
        </div>
    </div>
</section>

<section class="chap band band--black chap--rev" aria-label="The story of Prestige Imports, part 2 of 3">
    <div class="container chap__grid">
        <figure class="chap__media" data-reveal>
            <picture>
                    <source type="image/webp" srcset="assets/img/archive-2020-1280.webp 1280w, assets/img/archive-2020-640.webp 640w" sizes="(min-width: 1024px) 50vw, 100vw">
                    <img src="assets/img/archive-2020-640.jpg" srcset="assets/img/archive-2020-1280.jpg 1280w, assets/img/archive-2020-640.jpg 640w" sizes="(min-width: 1024px) 50vw, 100vw" width="1280" height="853" loading="lazy" decoding="async" alt="Brett David and Stephan Winkelmann holding a gold Lamborghini bull at the grand opening of the new showroom.">
                </picture>
        </figure>
        <div class="chap__body">
            <p class="chap__lead">Upon Irv David’s tragic passing in 2007, his then 19&#8209;year&#8209;old son, Brett, was faced with a choice between remaining an heir to a budding empire or assuming his father’s position as CEO of Prestige Imports.</p>
            <div class="chap__text"><p>Brett David along with his team at Prestige Imports has now led the company to unparalleled growth and success while gaining new levels of achievement. Prestige Imports proudly counts itself among the most successful luxury automobile companies in the country. Currently, Prestige Imports is thriving under its corporate wings with premier franchises: Lamborghini Miami, which famously introduced the <strong>Sharpie Lamborghini</strong> and <strong>AU79 Aventador</strong>; Pagani of Miami, one of only three licensed dealers in the country, Lotus of Miami, offering the Evora, Exige, and Elise; and most recently KARMA Miami with the new Revero due for deliveries.</p></div>
        </div>
    </div>
</section>

<section class="chap band band--dark" aria-label="The story of Prestige Imports, part 3 of 3">
    <div class="container chap__grid">
        <figure class="chap__media" data-reveal>
            <picture>
                    <source media="(min-width: 768px)" type="image/webp" srcset="assets/img/slide-prestige-4-1920.webp">
                    <source media="(min-width: 768px)" srcset="assets/img/slide-prestige-4-1920.jpg">
                    <source type="image/webp" srcset="assets/img/slide-prestige-4-p-800.webp">
                    <img src="assets/img/slide-prestige-4-p-800.jpg" width="800" height="943" loading="lazy" decoding="async" alt="Irv David leaning on a white Lamborghini Diablo outside Prestige Imports, in black and white.">
                </picture>
        </figure>
        <div class="chap__body">
            <p class="chap__lead">Prestige Imports has expanded the vision set forth by the late Irv David.</p>
            <div class="chap__text"><p>The company is internationally renowned for its success with an array of various ventures and nontraditional projects. Prestige Imports is always thinking of the next cutting-edge idea, to go beyond expectations that will set off the industry. Prestige Imports recently introduced Exotics &amp; Espresso, a monthly meet &amp; greet event that brings together exotic car owners, enthusiasts, and other members of the South Florida community. The family-owned business also participates in countless fundraising events for local charities such as MyWish4U, Joe DiMaggio Children’s Hospital, and Chai Lifeline. In memory of his father, Brett teamed with the American Heart Association to develop the Prestigious Heart Fund, a non-profit dedicated to promoting heart health and awareness. In 2011, Brett, along with his sister Brooke, created the Ride2Revive Foundation which provides children who are undergoing medical treatment for life-threatening diseases, with memorable adrenaline-filled excursions, meant to distract them from their health-related struggles and revitalize their senses.</p><p>Located on Biscayne Boulevard in the heart of North Miami Beach, Prestige Imports has a collective inventory that intrinsically fits the South Florida lifestyle. Whether you are in the market to buy, lease or trade, Prestige Imports’ team of world-class agents will help you obtain the proper vehicle for your exact needs. In addition to Audi, Lamborghini, Pagani, and Lotus, you will find a revolving selection of Certified Pre-Owned vehicles featuring brands such as Aston Martin, Bentley, BMW, Ferrari, Jaguar, Land Rover, Maserati, Mercedes Benz, Porsche, and Rolls Royce.</p></div>
        </div>
    </div>
</section>

<!-- ============================ 3 · THE QUOTE ============================
     Brett David's words, as on the client's page: set alone, centred, regular weight. -->
<section class="quote band band--black" aria-label="Brett David">
    <div class="container">
        <figure class="quote__body">
            <blockquote class="quote__text"><p>“Being a second-generation dealership during this astonishing technological era allows us to redefine our focus and take advantage of the innovative and creative ideas that did not exist in the past. Along with our progressive thinking, we continue to instill our core belief which is to provide the highest level of service and product to our customers.”</p></blockquote>
            <figcaption class="quote__who">– Brett David</figcaption>
        </figure>
    </div>
</section>

<!-- ============================ 4 · OUR HISTORY IN PICTURES ============================
     Redone 6 Nov 2026 (Alex: the list read as a catalogue). From 1024 px the section is held on
     screen while its prints travel past, right to left, at two heights; the year of the print at
     the centre stands behind them, very large and pale (the showcase watermark, decorative), and
     the scale below carries it legibly with the decades. Phones, reduced motion and no-JS get the
     same frames as a vertical sequence. Captions are the client's, word for word. -->
<section class="film band band--light" id="pictures" aria-labelledby="pictures-title" data-film>
    <div class="container film__head">
        <h2 class="t-banner" id="pictures-title"><span class="svc-line">Our history</span> <span class="svc-line">in pictures</span></h2>
    </div>
    <div class="film__pin" data-film-pin>
        <div class="film__stage" data-film-stage>
            <p class="film__ghost" aria-hidden="true" data-film-ghost>1980</p>
            <ol class="film__track" data-film-track>
{film()}
            </ol>
            <div class="container film__scale" aria-hidden="true">
                <p class="film__now"><span data-film-now>1980</span></p>
                <div class="film__rule"><span class="film__fill" data-film-fill></span>{''.join(f'<span class="film__tick" data-film-tick="{d}">{d}</span>' for d in DECADES)}</div>
            </div>
        </div>
    </div>
    <div class="container film__end">
        <a class="btn btn--primary" href="srp.html">
            <span>View inventory</span>
            <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
        </a>
        <a class="btn btn--secondary" href="about.html">
            <span>About us</span>
            <svg class="icon btn__icon" aria-hidden="true"><use href="#i-arrow"/></svg>
        </a>
    </div>
</section>

</main>'''
