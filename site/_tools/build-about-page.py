"""Builds about.html and our-story.html from ad-personam.html's shell (head, header, menu, footer, scripts),
so both follow any change to the department template. Main content: _tools/about-main.html, _tools/story-main.py."""
import re
import sys
from pathlib import Path
S = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(S / '_tools'))
shell = (S / 'ad-personam.html').read_text(encoding='utf8')

LD = '''<script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "AutoDealer",
        "name": "Lamborghini Miami",
        "brand": { "@type": "Brand", "name": "Lamborghini" },
        "parentOrganization": { "@type": "AutoDealer", "name": "Prestige Imports" },
        "telephone": "+1-833-290-5147",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "14780 Biscayne Boulevard",
            "addressLocality": "North Miami Beach",
            "addressRegion": "FL",
            "postalCode": "33181",
            "addressCountry": "US"
        },
        "geo": { "@type": "GeoCoordinates", "latitude": 25.913485, "longitude": -80.15750349 }
    }
    </script>'''

def sub(pat, rep, s, n=1):
    out, k = re.subn(pat, rep, s, count=n, flags=re.S)
    assert k == n, pat
    return out

def build(out, main, title, desc, preload, current, leaflet=True):
    page = sub(r'<main id="main">.*?</main>', lambda m: main.strip(), shell)
    page = sub(r'<title>.*?</title>', f'<title>{title}</title>', page)
    page = sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', page)
    page = sub(r'    <!-- Hero preload:.*?fetchpriority="high">\n    <link rel="preload"[^>]*>\n', lambda m: preload, page)
    page = sub(r'(<link rel="stylesheet" href="assets/css/service_v2.css\?v=\d+">)', r'\1\n    <link rel="stylesheet" href="assets/css/about_v2.css?v=12">', page)
    page = sub(r'(<script src="assets/js/service_v2.js\?v=\d+" defer></script>)', r'\1\n<script src="assets/js/about_v2.js?v=4" defer></script>', page)
    page = sub(r'<script type="application/ld\+json">.*?</script>', lambda m: LD, page)
    if not leaflet:
        page = sub(r'    <!-- Leaflet:.*?crossorigin="">\n', '', page)
        page = sub(r'<script src="https://unpkg.com/leaflet[^>]*>\s*</script>\n', '', page)
    # menu and footer: About us and Our story are pages now
    page = sub(r'<a class="menu__link" href="ad-personam.html" aria-current="page">', '<a class="menu__link" href="ad-personam.html">', page)
    # (the shell already carries them since the 6 Nov sweep; added here only if it ever loses them)
    if 'href="about.html"' not in page:
        page = sub(r'(<li><a class="menu__link" href="lifestyle.html">Lifestyle</a></li>)', r'<li><a class="menu__link" href="about.html">About us</a></li>\n                    \1', page)
        page = sub(r'(<li><a href="lifestyle.html">Lifestyle</a></li>)', r'<li><a href="about.html">About us</a></li>\n                        \1', page)
    page = page.replace('<a class="menu__link" href="index_v4.html#house">Our story</a>', '<a class="menu__link" href="our-story.html">Our story</a>')
    page = page.replace('<a href="index_v4.html#house">Our story</a>', '<a href="our-story.html">Our story</a>')
    page = page.replace(f'<a class="menu__link" href="{current}">', f'<a class="menu__link" href="{current}" aria-current="page">')
    page = page.replace('href="#request" data-menu-link>Schedule service', 'href="schedule-service.html">Schedule service')
    page = page.replace('<li><a href="#request">Schedule service</a></li>', '<li><a href="schedule-service.html">Schedule service</a></li>')
    if not leaflet:
        page = page.replace('<a class="site-header__link site-header__contact" href="#request">Contact</a>', '<a class="site-header__link site-header__contact" href="contact.html">Contact</a>')
    (S / out).write_text(page, encoding='utf8', newline='\n')
    print(out, len(page))

build('about.html', (S / '_tools/about-main.html').read_text(encoding='utf8'),
      'About Lamborghini Miami | Local dealership in North Miami Beach, FL',
      'Lamborghini Miami, part of Prestige Imports: a staple in Miami and South Florida for over 40 years. The Prestige Imports Difference, testimonials and how to reach us.',
      '    <!-- Hero preload: the night aerial -->\n    <link rel="preload" as="image" type="image/webp" href="assets/img/showroom-aerial-night-1760.webp" imagesrcset="assets/img/showroom-aerial-night-1760.webp 1760w, assets/img/showroom-aerial-night-1200.webp 1200w, assets/img/showroom-aerial-night-800.webp 800w" imagesizes="100vw" fetchpriority="high">\n',
      'about.html')

import importlib
story = importlib.import_module('story-main')
build('our-story.html', story.MAIN,
      'Lamborghini Miami History | North Miami Beach, FL',
      'The story of Prestige Imports and Lamborghini Miami, from Irv David in 1980 to Brett David today: our history in pictures.',
      '    <!-- Hero preload: the history film’s poster, landscape and phone -->\n    <link rel="preload" as="image" type="image/webp" media="(min-width: 1200px), (min-width: 768px) and (orientation: landscape)" href="assets/video/prestige-history-poster-d.webp" fetchpriority="high">\n    <link rel="preload" as="image" type="image/webp" media="(max-width: 1199.98px) and (orientation: portrait), (max-width: 767.98px)" href="assets/video/prestige-history-poster-m.webp" fetchpriority="high">\n',
      'our-story.html', leaflet=False)
