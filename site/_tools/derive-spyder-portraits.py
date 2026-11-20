#!/usr/bin/env python3
"""Temerario Spyder (20 Nov 2026): the two upright frames the model template needs on phones, cut from
lamborghini.com's own landscape frames (the site publishes no upright hero or interior for this model).
Straight crops only: nothing is extended, blended or added (Alex rejected a composited hero, 20 Nov).

    python _tools/derive-spyder-portraits.py

hero-p     the hero's own frame (Alex's 1920x1080, 20 Nov), cut at the phone band's 0.85 (the home slider's
           system) around the car, which fits it whole (the car spans 800-1690 of 1920).
interior-p the cockpit still, cut upright around the wheel and seats.

Writes derived_hero-p.jpg and derived_interior-p.jpg into ___OCT changes/sources/models/temerario-spyder/
(gitignored), where process-model-photos.py picks them up."""
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parent.parent.parent / '___OCT changes' / 'sources' / 'models' / 'temerario-spyder'
RATIO = 786 / 1200   # the template's upright frame


def upright(name, cx, out, ratio=RATIO):
    im = Image.open(SRC / name).convert('RGB')
    w = round(im.height * ratio)
    x0 = min(max(0, round(cx - w / 2)), im.width - w)
    im.crop((x0, 0, x0 + w, im.height)).save(SRC / out, quality=92)
    print(out, (x0, 0, x0 + w, im.height))


upright('alex_model_d.jpg', 1245, 'derived_hero-p.jpg', 0.85)   # Alex's frame (NEW SLIDER/Temerario Spyder model d.jpg): the rear three-quarter, taillight and rear wheel
upright('interior_Temerario_04-Interior-H_Chapter-Main_Still-B.png', 1320, 'derived_interior-p.jpg')
