#!/usr/bin/env python3
"""Fail if any var(--x) used in CSS, JS or index.html has no definition.
An undefined custom property inside a `transition` shorthand makes the whole
declaration invalid at computed-value time (it becomes `0s`), so every entrance
pops instead of moving -- which is exactly what happened when --ease-drive was
retired on 30 Sep 2026. Run before every commit: python3 _tools/check-vars.py"""
import re, sys, pathlib
site = pathlib.Path(__file__).resolve().parent.parent
# Each page is checked against its own stylesheet and script only, so a token that
# exists in v2 can never mask one missing from v1 (and the other way round).
SETS = {
    'v1': ['index.html', 'assets/css/tokens.css', 'assets/css/main.css', 'assets/js/main.js'],
    'v2': ['index_v2.html', 'assets/css/tokens_v2.css', 'assets/css/main_v2.css', 'assets/js/main_v2.js'],
    'service': ['service.html', 'assets/css/tokens_v2.css', 'assets/css/main_v2.css', 'assets/css/service_v2.css', 'assets/js/main_v2.js', 'assets/js/service_v2.js'],
    'inventory-srp': ['srp.html', 'assets/css/tokens_v2.css', 'assets/css/main_v2.css', 'assets/css/forms_v2.css', 'assets/css/prestige_srp.css', 'assets/css/inventory_pi.css', 'assets/js/main_v2.js', 'assets/js/forms_v2.js', 'assets/js/inventory_pi.js'],
    'inventory-vdp': ['vdp.html', 'assets/css/tokens_v2.css', 'assets/css/main_v2.css', 'assets/css/forms_v2.css', 'assets/css/prestige_vdp.css', 'assets/css/inventory_pi.css', 'assets/js/main_v2.js', 'assets/js/forms_v2.js', 'assets/js/inventory_pi.js'],
}
fail = False
for name, rels in SETS.items():
  files = [site / r for r in rels if (site / r).exists()]
  if not files: continue
  defined, used = set(), {}
  for f in files:
    t = f.read_text(encoding='utf-8')
    defined |= set(re.findall(r'(--[\w-]+)\s*:', t))                                  # CSS declarations + inline style="--x: …"
    defined |= set(re.findall(r'setProperty\(\s*[\'"`](--[\w-]+)', t))               # set from JS
    for m in re.finditer(r'var\(\s*(--[\w-]+)\s*(,)?', t):
        used.setdefault(m.group(1), []).append((f.name, t.count('\n', 0, m.start()) + 1, bool(m.group(2))))
  # a stray or missing brace silently swallows the next rule (v2, 1 Oct 2026: the inventory
  # header CTA rule was dropped this way), so every stylesheet must balance
  for f in files:
    if f.suffix != '.css': continue
    d, line, inc, i, t = 0, 1, False, 0, f.read_text(encoding='utf-8')
    while i < len(t):
      if not inc and t.startswith('/*', i): inc = True; i += 2; continue
      if inc and t.startswith('*/', i): inc = False; i += 2; continue
      ch = t[i]
      if ch == '\n': line += 1
      if not inc and ch == '{': d += 1
      if not inc and ch == '}':
        d -= 1
        if d < 0: print(f'[{name}] STRAY BRACE {f.name}:{line}'); fail = True; d = 0
      i += 1
    if d > 0: print(f'[{name}] UNCLOSED BRACE in {f.name} ({d})'); fail = True
  bad = {k: v for k, v in used.items() if k not in defined and not all(fb for _, _, fb in v)}
  soft = {k: v for k, v in used.items() if k not in defined and k not in bad}
  for k, v in sorted(bad.items()):
    print(f'[{name}] UNDEFINED {k}: ' + ', '.join(f'{n}:{l}' for n, l, _ in v[:6]))
  print(f'[{name}] {len(used)} custom properties used, {len(defined)} defined, {len(bad)} undefined without fallback'
        + (f', {len(soft)} undefined but always with a fallback ({", ".join(sorted(soft))})' if soft else ''))
  fail = fail or bool(bad)
sys.exit(1 if fail else 0)
