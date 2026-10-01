#!/usr/bin/env python3
"""Fail if any var(--x) used in CSS, JS or index.html has no definition.
An undefined custom property inside a `transition` shorthand makes the whole
declaration invalid at computed-value time (it becomes `0s`), so every entrance
pops instead of moving -- which is exactly what happened when --ease-drive was
retired on 30 Sep 2026. Run before every commit: python3 _tools/check-vars.py"""
import re, sys, pathlib
site = pathlib.Path(__file__).resolve().parent.parent
files = [site / 'index.html', *sorted((site / 'assets').rglob('*.css')), *sorted((site / 'assets').rglob('*.js'))]
defined, used = set(), {}
for f in files:
    t = f.read_text(encoding='utf-8')
    defined |= set(re.findall(r'(--[\w-]+)\s*:', t))                                  # CSS declarations + inline style="--x: …"
    defined |= set(re.findall(r'setProperty\(\s*[\'"`](--[\w-]+)', t))               # set from JS
    for m in re.finditer(r'var\(\s*(--[\w-]+)\s*(,)?', t):
        used.setdefault(m.group(1), []).append((f.name, t.count('\n', 0, m.start()) + 1, bool(m.group(2))))
bad = {k: v for k, v in used.items() if k not in defined and not all(fb for _, _, fb in v)}
soft = {k: v for k, v in used.items() if k not in defined and k not in bad}
for k, v in sorted(bad.items()):
    print(f'UNDEFINED {k}: ' + ', '.join(f'{n}:{l}' for n, l, _ in v[:6]))
print(f'{len(used)} custom properties used, {len(defined)} defined, {len(bad)} undefined without fallback'
      + (f', {len(soft)} undefined but always with a fallback ({", ".join(sorted(soft))})' if soft else ''))
sys.exit(1 if bad else 0)
