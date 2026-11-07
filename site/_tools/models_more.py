"""The other model pages (Alex, 6 Nov 2026; client sheet rows 34-44: "This page should follow the model page or if
that's too much time, just adjust the content so it looks cleaner. There's a lot of empty space next to text that
might just need to be made full width"). Data for _tools/process-models-more.py and _tools/build-models-more.py.

Copy: the client's own text on lamborghinimiami.aandemo.com (read 6 Nov 2026), word for word, picked by sentence
from research/images-current-site/models/sentences.json (S(page, section, i...)). Headings are our model template's.
Photos: the demo's and lamborghini.com's (history/<model>), the better frame of the two, by file number in
research/images-current-site/models/<demo slug>/ (gitignored).

Roles: hero, num (figures), ext (the band), int (the cockpit), c<n> (cards), g<n> (gallery), w-<key> (a story band).
A card is (file, sentence indices or a title of the client's own words)."""
import json
from pathlib import Path

RES = Path(__file__).resolve().parents[2] / 'research' / 'images-current-site' / 'models'
SENT = json.loads((RES / 'sentences.json').read_text(encoding='utf8'))


def S(src, sec, *idx):
    s = SENT[src][sec]['s']
    return ' '.join(s[i] for i in idx)


def NUMS(src):
    import re
    out = []
    for n in SENT[src]['figures']['nums']:
        m = re.match(r'^([>\d.,]+)(hp|mph|s|L)(.*)$', n)
        v, u, lab = m.groups()
        out.append((v.replace('>', '&gt;'), u, lab))
    return out


def CLAIM(src):
    """The client's tagline, set in sentence case (the case is CSS's job everywhere else on the site)."""
    t = SENT[src]['hero']['s'][0].lower()
    return t[0].upper() + t[1:]


H = 'huracan-sterrato-mlp'
PAGES = [
    # ---------------- Huracán ----------------
    dict(slug='huracan-sterrato', src='huracan-sterrato-mlp', name='Huracán Sterrato', inv=('Huracán', r'Hurac'),
         hero=(25, 0.62), claim=CLAIM(H), lead=S(H, 'overview', 0),
         intro=S(H, 'overview', 1, 2), intro_legal=S(H, 'overview', 3, 4),
         num=(19, 0.5), nums=NUMS(H),
         ext=dict(img=(23, 0.55), text=S(H, 'exterior', 0), legal=S(H, 'exterior', 4, 5),
                  cards=[(24, S(H, 'exterior', 1), 'The Sterrato’s raised body over its wheel, close up.'),
                         (7, S(H, 'exterior', 2), 'The air intake on the Sterrato’s rear hood, close up.'),
                         (9, S(H, 'exterior', 3), 'The front of the Sterrato, head-on, its additional lights lit.')],
                  alt='A Huracán Sterrato drifting on snow, throwing up a cloud.'),
         int=dict(img=(4, 0.5), text=S(H, 'interior', 0), alt='The Huracán Sterrato cockpit: the steering wheel and the digital instruments.',
                  cards=[(10, S(H, 'interior', 1), 'A Sterrato sports seat with the Sterrato script.'),
                         (16, S(H, 'interior', 2), 'The Sterrato’s centre console and display, seen from above.')]),
         gallery=[(21, 'A Huracán Sterrato in a studio lit in red.'), (20, 'A white Huracán Sterrato below snowy mountains.'),
                  (8, 'A Huracán Sterrato from behind, in a dark studio.'), (3, 'A Huracán Sterrato from above, in a dark studio.'),
                  (13, 'A skier beside a Huracán Sterrato on snow.'), (17, 'A Huracán Sterrato on a snowy road, from above.'),
                  (2, 'A Huracán Sterrato in a studio, rear three-quarter view.'), (6, 'The wheel of a white Huracán Sterrato, close up.'),
                  (5, 'The Sterrato script on the car’s side, close up.')]),
    dict(slug='huracan-tecnica', src='huracan-tecnica-mlp', name='Huracán Tecnica', inv=('Huracán', r'Hurac'),
         hero=(32, 0.62), claim=CLAIM('huracan-tecnica-mlp'), lead=S('huracan-tecnica-mlp', 'overview', 0),
         intro=S('huracan-tecnica-mlp', 'overview', 1, 2), intro_legal=S('huracan-tecnica-mlp', 'overview', 3, 4),
         num=(9, 0.5), nums=NUMS('huracan-tecnica-mlp'),
         ext=dict(img=(21, 0.55), text=S('huracan-tecnica-mlp', 'exterior', 0),
                  cards=[(14, S('huracan-tecnica-mlp', 'exterior', 1), 'A green Huracán Tecnica head-on, in a dark studio.'),
                         (15, S('huracan-tecnica-mlp', 'exterior', 2), 'The rear of a green Huracán Tecnica, in a dark studio.'),
                         (6, S('huracan-tecnica-mlp', 'exterior', 3), 'The side intake of a green Huracán Tecnica, close up.')],
                  alt='An orange Huracán Tecnica on a circuit.'),
         int=dict(img=(10, 0.5), text=S('huracan-tecnica-mlp', 'interior', 0, 1, 4), alt='The Huracán Tecnica cockpit in black and orange.',
                  cards=[(19, S('huracan-tecnica-mlp', 'interior', 2), 'The Huracán Tecnica sports seats in black with green trim.'),
                         (16, S('huracan-tecnica-mlp', 'interior', 3), 'The Huracán Tecnica centre console and touchscreen.')]),
         gallery=[(1, 'A grey Huracán Tecnica on a bridge, in the city.'), (3, 'An orange Huracán Tecnica on a mountain road.'),
                  (8, 'A green Huracán Tecnica in a smoky studio.'), (2, 'A black Huracán Tecnica from behind, on a mountain road.'),
                  (20, 'A black Huracán Tecnica on a winding road at sunset.'), (22, 'A green Huracán Tecnica on a city circuit.'),
                  (17, 'The engine cover of a green Huracán Tecnica, from above.'), (18, 'A grey Huracán Tecnica from above, on track.'),
                  (7, 'A red Huracán Tecnica by a modern building.')]),
    dict(slug='huracan-sto', src='huracan-sto-mlp', name='Huracán STO', inv=('Huracán', r'Hurac'),
         hero=(29, 0.62), claim=CLAIM('huracan-sto-mlp'), lead=S('huracan-sto-mlp', 'overview', 0),
         intro=S('huracan-sto-mlp', 'overview', 1, 2),
         num=(7, 0.5), nums=NUMS('huracan-sto-mlp'),
         ext=dict(img=(13, 0.55), text=S('huracan-sto-mlp', 'exterior', 0),
                  cards=[(21, S('huracan-sto-mlp', 'exterior', 1), 'The rear wing and engine cover of a blue Huracán STO.'),
                         (6, S('huracan-sto-mlp', 'exterior', 2), 'A Huracán STO with its Cofango, the front hood and fenders in one piece, raised.'),
                         (2, S('huracan-sto-mlp', 'exterior', 3), 'A green Huracán STO on a circuit, head-on.')],
                  alt='Four Huracán STO on a circuit.'),
         int=dict(img=(4, 0.5), text=S('huracan-sto-mlp', 'interior', 0, 2), alt='The Huracán STO cockpit in black and blue.',
                  cards=[(20, S('huracan-sto-mlp', 'interior', 1), 'The Huracán STO seats in black and red.'),
                         (10, S('huracan-sto-mlp', 'interior', 3), 'The Huracán STO seats and roll bar, in black and blue.')]),
         gallery=[(1, 'A red Huracán STO at sunset.'), (15, 'A green Huracán STO on a circuit at sunset.'),
                  (8, 'Two Huracán STO in a pit lane, in the sun.'), (3, 'A white Huracán STO at speed.'),
                  (14, 'A blue Huracán STO in the snow.'), (16, 'A blue Huracán STO in a pit garage, its Cofango raised.'),
                  (17, 'A green Huracán STO on a circuit.'), (5, 'Two Huracán STO on a cobbled terrace.'),
                  (18, 'A blue Huracán STO on a circuit at sunset.')]),
    dict(slug='huracan-evo-spyder', src='huracan-evo-spyder-mlp', name='Huracán EVO Spyder', inv=('Huracán', r'Hurac'),
         hero=(6, 0.72), claim=CLAIM('huracan-evo-spyder-mlp'), lead=S('huracan-evo-spyder-mlp', 'overview', 0),
         intro=S('huracan-evo-spyder-mlp', 'overview', 1, 2, 3),
         num=(24, 0.5), nums=NUMS('huracan-evo-spyder-mlp'),
         ext=dict(img=(19, 0.6), text=S('huracan-evo-spyder-mlp', 'exterior', 0, 1),
                  cards=[(22, 'The front aerodynamic details', 'A blue Huracán EVO Spyder head-on, on a mountain road.'),
                         (9, 'The air intake on each side skirt', 'A blue Huracán EVO Spyder under an arcade, rear three-quarter view.'),
                         (17, 'The exhausts', 'A blue Huracán EVO Spyder from behind, on a forest road.')],
                  alt='A green Huracán EVO Spyder in side profile, against a wall of plants.'),
         int=dict(img=(4, 0.5), text=S('huracan-evo-spyder-mlp', 'interior', 1), alt='The Huracán EVO Spyder cockpit, open to the sky.',
                  cards=[(25, S('huracan-evo-spyder-mlp', 'interior', 0), 'The 8.4-inch touchscreen in the centre console.'),
                         (20, S('huracan-evo-spyder-mlp', 'interior', 2), 'A Huracán EVO Spyder seat with the Lamborghini shield, at sunset.')]),
         gallery=[(32, 'A green Huracán EVO Spyder on a road by a lake.'), (3, 'Two Huracán EVO Spyder on a street lined with palazzi.'),
                  (7, 'A blue Huracán EVO Spyder on a mountain road.'), (8, 'A blue Huracán EVO Spyder from above, on a rail bridge.'),
                  (5, 'A blue Huracán EVO Spyder on a country road, from above.'), (2, 'A blue Huracán EVO Spyder from behind, at speed.'),
                  (23, 'The Huracán EVO Spyder cabin by a lake.'), (21, 'The Huracán EVO Spyder dashboard and centre console.'),
                  (1, 'A green Huracán EVO Spyder in a rocky gorge.')]),
    # ---------------- Urus ----------------
    dict(slug='urus-s', src='urus-s-mlp', name='Urus S', inv=('Urus', r'Urus S\b'),
         hero=(26, 0.62), claim=CLAIM('urus-s-mlp'), lead=S('urus-s-mlp', 'overview', 0),
         intro=S('urus-s-mlp', 'overview', 1, 2, 3),
         num=(22, 0.5), nums=NUMS('urus-s-mlp'),
         ext=dict(img=(3, 0.58), text=S('urus-s-mlp', 'exterior', 0),
                  cards=[(21, S('urus-s-mlp', 'exterior', 1), 'The rear of a grey Urus S in a studio.'),
                         (23, S('urus-s-mlp', 'exterior', 2), 'A wheel of the Urus S, close up.'),
                         (5, S('urus-s-mlp', 'exterior', 3), 'A grey Urus S from above, its roof in view.')],
                  alt='A grey Urus S in side profile, in a dark garage.'),
         int=dict(img=(9, 0.5), text=S('urus-s-mlp', 'interior', 0, 1), alt='The Urus S dashboard in brown leather.',
                  cards=[(8, 'Leather surfaces', 'A driver’s hands on the Urus S leather steering wheel.'),
                         (4, 'High-tech Lamborghini equipment', 'The Urus S centre console and drive mode selector.')]),
         gallery=[(1, 'A grey Urus S in the rain at night.'), (19, 'A dark Urus S on a country road.'),
                  (2, 'A grey Urus S in the city.'), (7, 'A grey Urus S from above, in a studio lit in red.'),
                  (20, 'A white Urus S below snowy peaks.'), (10, 'The panoramic roof of a Urus S.'),
                  (25, 'A green Urus S on a coast road.'), (6, 'A Urus S seen through its open roof.'),
                  (24, 'The Urus S cabin in brown leather.')]),
    dict(slug='urus-performante', src='urus-performante-mlp', name='Urus Performante', inv=('Urus', r'Urus Performante'),
         hero=(23, 0.62), claim=CLAIM('urus-performante-mlp'), lead=S('urus-performante-mlp', 'overview', 0),
         intro=S('urus-performante-mlp', 'overview', 1, 2),
         num=(15, 0.5), nums=NUMS('urus-performante-mlp'),
         ext=dict(img=(25, 0.62), text=S('urus-performante-mlp', 'exterior', 0, 1),
                  cards=[(3, 'Lightweight carbon-fiber components', 'A yellow Urus Performante with a carbon bonnet, in a smoky studio.'),
                         (2, 'Sporty, sleek and undeniably bold', 'A green Urus Performante from behind, in a studio.'),
                         (9, 'Proportions that reflect those of a super sports car', 'The wheel arch of a green Urus Performante with the Performante script.')],
                  alt='An orange Urus Performante in side profile on a hilltop at dawn.'),
         int=dict(img=(4, 0.5), text=S('urus-performante-mlp', 'interior', 0, 3), alt='The Urus Performante cockpit in black.',
                  cards=[(7, S('urus-performante-mlp', 'interior', 1), 'The Urus Performante seats with yellow contrast stitching.'),
                         (20, S('urus-performante-mlp', 'interior', 2), 'The Urus Performante steering wheel and dashboard.')]),
         gallery=[(1, 'A yellow Urus Performante in dust at sunset.'), (5, 'A green and a yellow Urus Performante in a studio.'),
                  (6, 'A yellow Urus Performante at night by a track.'), (21, 'A red Urus Performante on a mountain road.'),
                  (22, 'A green Urus Performante from behind, on gravel.'), (17, 'A yellow Urus Performante from above, in a dark studio.'),
                  (19, 'A green Urus Performante in the city, from behind.'), (24, 'The Performante script on the car’s side.'),
                  (26, 'An orange Urus Performante on a hilltop.')]),
    # ---------------- Limited Series ----------------
    dict(slug='countach-lpi-800-4', src='countach-lpi-800-4-mlp', name='Countach LPI 800-4', inv=None,
         hero=(6, 0.75), claim=CLAIM('countach-lpi-800-4-mlp'), lead=S('countach-lpi-800-4-mlp', 'overview', 0),
         intro=S('countach-lpi-800-4-mlp', 'overview', 1, 2),
         num=(8, 0.5), nums=NUMS('countach-lpi-800-4-mlp'),
         ext=dict(img=(26, 0.62), text=S('countach-lpi-800-4-mlp', 'exterior', 0),
                  cards=[(1, S('countach-lpi-800-4-mlp', 'exterior', 1), 'The new Countach LPI 800-4 beside the original Countach, from above.'),
                         (9, S('countach-lpi-800-4-mlp', 'exterior', 2), 'The engine cover vents of a white Countach LPI 800-4, close up.'),
                         (2, S('countach-lpi-800-4-mlp', 'exterior', 3), 'The rear of a white Countach LPI 800-4 at dusk.')],
                  alt='A white Countach LPI 800-4 head-on at dusk, its lights on.'),
         int=dict(img=(4, 0.5), text=S('countach-lpi-800-4-mlp', 'interior', 0, 1, 2), alt='The Countach LPI 800-4 cockpit in black and red.', cards=[]),
         gallery=[(18, 'A white Countach LPI 800-4 before a villa, two earlier Countach beside it.'), (19, 'A Countach LPI 800-4 with its scissor doors up, on an autumn avenue.'),
                  (20, 'A red Countach LPI 800-4 at night in a lit street.'), (22, 'A white Countach LPI 800-4 in a misty hall.'),
                  (7, 'A white Countach LPI 800-4 in a dark studio, front three-quarter view.'), (10, 'The Countach LPI 800-4 seats in red leather.'),
                  (12, 'A white Countach LPI 800-4 under palm trees.'), (21, 'The new Countach beside the original, at speed, from above.'),
                  (3, 'A white Countach LPI 800-4 on a terrace at dusk, the original Countach behind it.')]),
]

# family and special pages: built from sections (build-models-more.py)
FAMILIES = [
    dict(slug='huracan', src='huracan-mlp', name='Huracán', inv=('Huracán', r'Hurac'),
         hero=(14, 0.6), claim=None, lead=S('huracan-mlp', 'overview', 0),
         intro=S('huracan-mlp', 'overview', 1, 2, 3, 4, 5),
         design=dict(img=(2, 0.6), text=S('huracan-mlp', 'exterior', 0, 1), alt='An orange Huracán Tecnica on a mountain road.'),
         models_lead=S('huracan-mlp', 'exterior', 2),
         models=['huracan-sterrato', 'huracan-tecnica', 'huracan-sto', 'huracan-evo-spyder'],
         gallery=[(1, 'A blue Huracán STO in front of a city skyline.'), (11, 'A Huracán Sterrato raising dust below cliffs.'),
                  (12, 'Two Huracán STO on a terrace above a city.'), (13, 'A Huracán Sterrato at sunset.'),
                  (3, 'A red Huracán STO at night, its lights lit.'), (4, 'A Huracán Sterrato in a studio lit in red.')]),
    dict(slug='urus', src='urus-mlp', name='Urus', inv=('Urus', r'Urus'),
         hero=(8, 0.6), claim=None, lead=S('urus-mlp', 'overview', 0),
         intro=S('urus-mlp', 'overview', 1, 2),
         design=dict(img=(33, 0.55, 0.78), text=S('urus-mlp', 'exterior', 0), alt='A Urus raising a cloud of sand in the desert.',
                     cards=[(14, S('urus-mlp', 'exterior', 1), 'A blue Urus on a mountain road below clouds.'),
                            (12, S('urus-mlp', 'exterior', 2, 3), 'A yellow Urus on a forest track.'),
                            (32, S('urus-mlp', 'exterior', 4), 'A black Urus on a country road.')]),
         models_lead=None,
         models=['urus-se', 'urus-se-performante', 'urus-s', 'urus-performante'],
         gallery=[(2, 'A violet Urus at speed on a dirt road.'), (3, 'A green Urus on a mountain road.'),
                  (7, 'A yellow Urus in an olive grove.'), (9, 'A green Urus from behind, by a palazzo.'),
                  (15, 'A blue Urus at speed on gravel.'), (29, 'The rear of a white Urus in the snow.'),
                  (31, 'A yellow Urus in a quarry.'), (10, 'A driver at the wheel of a Urus.'),
                  (11, 'The vents of a violet Urus bonnet, close up.')]),
]

# pages of their own shape: a list of sections (story: a heading, the client's text, a band photo or a main photo)
A, L, Z = 'aventador', 'limited-series-mlp', 'lanzador'
SPECIAL = [
    dict(slug='aventador', src=A, name='Aventador', inv=None,
         hero=(10, 0.62), claim=None, lead=None,
         sections=[
             dict(kind='intro', eyelet='Aventador', heading='Designed to push beyond performance', text=S(A, 'overview', 0, 1, 2, 3)),
             dict(kind='story', key='design', eyelet='Exterior', heading='Design', text=S(A, 'exterior', 0), band='dark',
                  wide=(1, 0.6, 'A gold Aventador SVJ Roadster in a hangar, its reflection on the floor.'),
                  cards=[(24, S(A, 'exterior', 1), 'The Aventador’s V12 under its carbon engine cover, from above.'),
                         (3, 'High-level technology and luxury equipment', 'The Aventador cockpit and steering wheel.')]),
         ],
         gallery=[(2, 'A grey Aventador on a mountain road at sunset.'), (4, 'A green Aventador SVJ on a road through hills.'),
                  (9, 'A blue Aventador Roadster at speed at sunset.'), (11, 'A green Aventador SVJ on a bridge.'),
                  (12, 'A blue Aventador on a mountain road, another behind it.'), (8, 'An Aventador with its scissor doors open.'),
                  (21, 'A white Aventador on a circuit.'), (22, 'A red Aventador at night under an arcade.'),
                  (37, 'A red Aventador on a mountain road.')]),
    dict(slug='limited-series', src=L, name='Limited Series', inv=None,
         hero=(19, 0.62), claim=None, lead=None,
         sections=[
             dict(kind='story', key='countach', eyelet='Limited Series', heading='Countach LPI 800-4', text=S(L, 'countach-lp-800-4', 0, 1, 2, 3), band='black', long=True,
                  wide=(43, 0.6, 'A white Countach LPI 800-4 before a villa, with the Countach that inspired it.'),
                  link=('Explore the Countach LPI 800-4', 'model-countach-lpi-800-4.html')),
             dict(kind='story', key='sian', eyelet='Limited Series', heading='Sián FKP 37', text=S(L, 'sian-fkp-37', 0, 1, 2, 3), band='dark', long=True,
                  wide=(15, 0.6, 'A green Sián FKP 37 from behind, its taillights lit, in a dark studio.'),
                  cards=[(14, None, 'The Y-shaped headlight of the Sián FKP 37, close up.'),
                         (11, None, 'The Sián FKP 37 cockpit in black and tan leather.')]),
             dict(kind='story', key='sian-roadster', eyelet='Limited Series', heading='Sián Roadster', text=S(L, 'sian-roadster', 0, 1, 2), band='black', long=True,
                  wide=(28, 0.62, 'A blue Sián Roadster in side profile, reflected in a dark studio floor.'),
                  cards=[(22, None, 'The rear wheel and taillights of the Sián Roadster, close up.'),
                         (23, None, 'The Sián Roadster cockpit, open to the sky.')]),
         ],
         gallery=[(16, 'A green Sián FKP 37 head-on, between two studio lights.'), (13, 'A Sián FKP 37 on a terrace above a city at dusk.'),
                  (17, 'A green Sián FKP 37 on a runway.'), (26, 'A blue Sián Roadster from behind, at speed.'),
                  (27, 'A blue Sián Roadster from above, in a dark studio.'), (24, 'The engine cover of the Sián Roadster, from above.')]),
    dict(slug='lanzador', src=Z, name='Lanzador', inv=None,
         hero=(1, 0.5), claim=CLAIM(Z), lead=None,
         sections=[
             dict(kind='story', key='concept', eyelet='Lanzador', heading='The concept', text=S(Z, 'overview', 0, 1, 2), band='black', long=True,
                  wide=(2, 0.6, 'The Lanzador in side profile, in a concrete hall.')),
             dict(kind='quote', text=S(Z, 'quote', 0)),
             dict(kind='story', key='technology', eyelet='Lanzador', heading='Technology', text=S(Z, 'technology', 0, 1, 2, 3, 4), band='dark', long=True,
                  main=(4, 0.5, 'The Lanzador steering wheel and dashboard, lit in red.')),
             dict(kind='story', key='aerodynamics', eyelet='Lanzador', heading='Aerodynamics', text=S(Z, 'aerodynamics', 0, 1, 2, 3), band='black', long=True,
                  wide=(5, 0.55, 'The rear of the Lanzador, its taillights lit.')),
             dict(kind='story', key='interior', eyelet='Lanzador', heading='Interior', text=S(Z, 'interior', 0, 1, 2, 3, 4, 5, 6), band='dark', long=True,
                  main=(6, 0.5, 'The Lanzador cabin from above, through the glass roof.')),
         ],
         gallery=[(7, 'The Lanzador in a dark studio, lit in blue.'), (8, 'The front of the Lanzador, close up.'), (10, 'The Lanzador cabin and its two seats.')],
         cta=dict(eyelet='Lamborghini Miami', heading='Contact a Lamborghini Brand Specialist for more information', configure=S(Z, 'cta', 0))),
]
YT = {p: SENT[p]['_yt'][0] for p in SENT if SENT[p].get('_yt')}

# where a tall source is cut to its frame (cards 1.744:1, gallery 16:9): the vertical focal point, 0 top .. 1 bottom
# (checked one by one 6 Nov 2026; the rest stay centred)
FOCUS = {
    ('huracan-sterrato', 'c1'): 0.72, ('huracan-sterrato', 'ic2'): 0.45,
    ('huracan-tecnica', 'ic1'): 0.58, ('huracan-tecnica', 'ic2'): 0.55, ('huracan-tecnica', 'g7'): 0.62, ('huracan-tecnica', 'g8'): 0.62,
    ('huracan-sto', 'c1'): 0.45, ('huracan-sto', 'ic1'): 0.45, ('huracan-sto', 'g9'): 0.64,
    ('huracan-evo-spyder', 'c1'): 0.8, ('huracan-evo-spyder', 'g8'): 0.4,
    ('urus-s', 'g7'): 0.6,
    ('urus-performante', 'ic2'): 0.55, ('urus-performante', 'g7'): 0.7, ('urus-performante', 'g9'): 0.55,
    ('urus', 'g6'): 0.62, ('lanzador', 'g1'): 0.55,
}

# ---------------- Concept (the demo's clp-lamborghini-concept-models page; read 6 Nov 2026) ----------------
import html as _h
import re as _re
_C = {s['id'] or 'hero': s for s in json.loads((RES / 'clp-concept-text.json').read_text(encoding='utf8'))}


def _paras(sec, skip):
    """the section's paragraphs, word for word, after its eyelet and heading lines"""
    return [p.strip() for p in _C[sec]['text'].split('\n\n')[skip:] if p.strip() and not p.strip().isupper()]


_rows = [[_h.unescape(_re.sub(r'<[^>]+>', '', c)).strip() for c in _re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r)]
         for r in _re.findall(r'<tr>(.*?)</tr>', _C['compare']['html'])]
SPECIAL.append(dict(
    slug='concept', src='clp-concept', name='Concept Models', inv=None, cta=False, form_title='Lamborghini models', option='Concept',
    desc='Lamborghini is always looking for new avenues to explore, and its concept models are proof of this. Lamborghini Miami at Prestige Imports, located in North Miami Beach, FL, offers this peek behind the curtain.',
    hero=(14, 0.62), claim=None, lead=None,
    sections=[
        dict(kind='intro', eyelet='Lamborghini Miami', text=' '.join(_paras('overview', 2)).replace('\n', ' ')),
        dict(kind='compare', eyelet='Lamborghini Miami', heading='At a glance', head=_rows[0], rows=_rows[1:]),
        dict(kind='story', key='asterion-estoque', eyelet='Lamborghini Miami', heading='Getting to Know the Lamborghini Asterion and Estoque',
             text=_paras('asterion-estoque', 2)[0], band='dark', long=True,
             cards=[(10, 'Lamborghini Asterion', 'A blue Lamborghini Asterion concept in a dark studio, front three-quarter view.'),
                    (19, 'Lamborghini Estoque', 'The headlight of the grey Lamborghini Estoque concept, close up.')],
             link=('Read more about Lamborghini', 'http://www.prestigeimports.com/blog/category/lamborghini/')),
        dict(kind='tiles', eyelet='Lamborghini Miami', heading='You may also like', models=['aventador', 'huracan']),
    ],
    gallery=[(8, 'A blue Lamborghini Asterion in side profile, in a dark studio.'), (13, 'The Asterion with its door open, its cabin in white leather.'),
             (11, 'The rear of the blue Asterion, its taillights lit.'), (15, 'A grey Lamborghini Estoque in side profile, on white.'),
             (18, 'The rear of the Estoque, on white.'), (9, 'The rear of the Asterion, head-on, on white.')]))
