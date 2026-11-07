"""Every copy scrim, eased (Alex, 6 Nov 2026: "absolutely smooth, no visible edge"). A two- or three-stop linear scrim
bends where its last stop meets 0, and the eye reads that bend as an edge. Each one becomes a C1-continuous curve with
the same start, middle and end: an ease from the start alpha to the middle one (flat at both ends), then a smootherstep
from the middle alpha to 0. Darker than before over the copy column, lighter only at the far end. Idempotent: a scrim
already eased (more than four stops) is left alone.

    python _tools/smooth-scrims.py"""
import math
import re
from pathlib import Path

CSS = Path(__file__).resolve().parents[1] / 'assets' / 'css'


def smoother(t):
    return t * t * t * (t * (6 * t - 15) + 10)


def fmt(x):
    return f'{x:.3f}'.rstrip('0').rstrip('.') or '0'


def eased(direction, a0, m, mid, end, n1=4, n2=10):
    """a0, m: alpha expressions (numbers as str, or var() expressions); mid, end: positions (e.g. '34%' or var(...))."""
    num = lambda s: re.fullmatch(r'[\d.]+', s) is not None
    pos_num = lambda s: re.fullmatch(r'[\d.]+%', s) is not None
    stops = []

    def alpha(k_from_a0, k_m):        # alpha = a0*k1 + m*k2
        if num(a0) and num(m):
            return fmt(float(a0) * k_from_a0 + float(m) * k_m)
        parts = []
        if k_from_a0: parts.append(f'{a0} * {fmt(k_from_a0)}')
        if k_m: parts.append(f'{m} * {fmt(k_m)}')
        return f'calc({" + ".join(parts) or "0"})'

    def pos(a, b, t):                  # a + (b - a) * t
        if pos_num(a) and pos_num(b):
            return fmt(float(a[:-1]) + (float(b[:-1]) - float(a[:-1])) * t) + '%'
        return f'calc({a} + ({b} - {a}) * {fmt(t)})'

    for i in range(n1):                # 0 -> mid: cosine ease a0 -> m
        t = i / n1
        k = (1 - math.cos(math.pi * t)) / 2
        stops.append(f'rgb(0 0 0 / {alpha(1 - k, k)}) {pos("0%", mid, t) if t else "0%"}')
    for i in range(n2 + 1):            # mid -> end: smootherstep m -> 0
        t = i / n2
        k = 1 - smoother(t)
        a = alpha(0, k) if k > 0.0005 else '0'
        stops.append(f'rgb(0 0 0 / {a}) {mid if t == 0 else (end if t == 1 else pos(mid, end, t))}')
    return f'linear-gradient({direction}, ' + ', '.join(stops) + ')'


STOP = r'rgb\(0 0 0 / ([^)]*?(?:\([^)]*\)[^)]*?)*)\)\s+([^,)]+(?:\([^)]*\))?[^,)]*)'
GRAD = re.compile(r'linear-gradient\((90deg|0deg|180deg),\s*((?:' + STOP + r'\s*,\s*){2,3}' + STOP + r')\)')


def fix(m):
    direction, body = m.group(1), m.group(2)
    stops = re.findall(STOP, body)
    if len(stops) > 4:
        return m.group(0)
    (a0, p0), *rest = [(a.strip(), p.strip()) for a, p in stops]
    if p0 != '0%' or rest[-1][0] not in ('0',):
        return m.group(0)               # not a scrim from an edge to clear
    mid_a, mid_p = rest[0]
    end_p = rest[-1][1]
    return eased(direction, a0, mid_a, mid_p, end_p)


FILES = ['model_v3.css', 'about_v2.css', 'main_v2.css', 'main_v3.css', 'main_v4.css']
for name in FILES:
    f = CSS / name
    s = f.read_text(encoding='utf8')
    n = 0

    def sub(m):
        global n
        r = fix(m)
        n += r != m.group(0)
        return r
    out = GRAD.sub(sub, s)
    if out != s:
        f.write_text(out, encoding='utf8', newline='')
    print(name, n, 'scrims eased')


def eased2(direction, a0, end, n=10):
    """a one-stop fade (alpha a0 at the edge -> 0 at end), as a smootherstep."""
    pos_num = re.fullmatch(r'[\d.]+%', end) is not None
    out = []
    for i in range(n + 1):
        t = i / n
        k = 1 - smoother(t)
        a = (fmt(float(a0) * k) if re.fullmatch(r'[\d.]+', a0) else f'calc({a0} * {fmt(k)})') if k > 0.0005 else '0'
        p = '0%' if t == 0 else end if t == 1 else (fmt(float(end[:-1]) * t) + '%' if pos_num else f'calc({end} * {fmt(t)})')
        out.append(f'rgb(0 0 0 / {a}) {p}')
    return f'linear-gradient({direction}, ' + ', '.join(out) + ')'


# pass 2: the scrims written with custom properties, the one-stop fades, and the model hero's wider falloff
EXPLICIT = {
    'linear-gradient(90deg, rgb(0 0 0 / var(--scrim-a, 0.8)) 0%, rgb(0 0 0 / calc(var(--scrim-a, 0.8) * 0.7)) var(--scrim-mid, 34%), rgb(0 0 0 / 0) var(--scrim-end, 62%))':
        eased('90deg', 'var(--scrim-a, 0.8)', 'calc(var(--scrim-a, 0.8) * 0.7)', 'var(--scrim-mid, 34%)', 'var(--scrim-end, 62%)'),
    'linear-gradient(90deg, rgb(0 0 0 / var(--adp-scrim-a)) 0%, rgb(0 0 0 / calc(var(--adp-scrim-a) * var(--adp-scrim-k))) var(--adp-scrim-mid), rgb(0 0 0 / 0) var(--adp-scrim-end))':
        eased('90deg', 'var(--adp-scrim-a)', 'calc(var(--adp-scrim-a) * var(--adp-scrim-k))', 'var(--adp-scrim-mid)', 'var(--adp-scrim-end)'),
    'linear-gradient(180deg, rgb(0 0 0 / var(--vig-a, 1)) 0%, rgb(0 0 0 / 0) var(--vig-top, 30%))': eased2('180deg', 'var(--vig-a, 1)', 'var(--vig-top, 30%)'),
    'linear-gradient(0deg,   rgb(0 0 0 / var(--vig-a, 1)) 0%, rgb(0 0 0 / 0) var(--vig-bottom, 36%))': eased2('0deg', 'var(--vig-a, 1)', 'var(--vig-bottom, 36%)'),
}
for d in ('180deg', '0deg'):
    for a, e in (('0.5', '22%'), ('0.55', '22%'), ('0.55', '30%'), ('0.45', '25%')):
        EXPLICIT[f'linear-gradient({d}, rgb(0 0 0 / {a}) 0%, rgb(0 0 0 / 0) {e})'] = eased2(d, a, e)
HERO_90 = re.compile(r'linear-gradient\(90deg, rgb\(0 0 0 / 0\.86\) 0%, [^;]*?rgb\(0 0 0 / 0\) 54%\)')
for name in FILES:
    f = CSS / name
    s = f.read_text(encoding='utf8'); o = s
    for a, b in EXPLICIT.items():
        s = s.replace(a, b)
    if name == 'model_v3.css':       # the copy column's falloff, 34% -> 72% instead of 54%: no bend to see
        s = HERO_90.sub(lambda m: eased('90deg', '0.86', '0.76', '34%', '72%'), s)
    if s != o:
        f.write_text(s, encoding='utf8', newline='')
    print(name, 'pass 2', 'changed' if s != o else 'unchanged')
