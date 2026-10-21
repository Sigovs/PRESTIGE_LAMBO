#!/usr/bin/env python3
"""v3 model pages (Oct 2026): official lamborghini.com model imagery -> web sizes.
Sources (downloaded from www.lamborghini.com/en-en/models/<model>, gitignored):
    ___OCT changes/sources/models/<slug>/
    python3 _tools/process-model-photos.py revuelto

Writes assets/img/models/<slug>-<role>-<w>.{jpg,webp}. Never upscales."""
from pathlib import Path
import sys
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets' / 'img' / 'models'
OUT.mkdir(parents=True, exist_ok=True)

SETS = {
    'revuelto': [
        # role, source file, widths
        ('hero', 'Revuelto_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-A-last-optim.jpg', (2400, 1600, 1000)),
        ('hero-p', 'Revuelto_02-Exterior-V_Chapter-Main_Still-B_Config-Alt-A-optim.jpg', (786,)),
        ('exterior', 'banner-desktop.jpg', (2160, 1440)),
        ('exterior-p', 'banner-mobile.jpg', (750,)),
        ('ext-headlight', 'Revuelto_02-Exterior-H_Card-Headlight-last-optim.jpg', (1200, 800)),
        ('ext-rear', 'Revuelto_02-Exterior-H_Card-Rear-last-optim.jpg', (1200, 800)),
        ('ext-engine', 'Revuelto_02-Exterior-H_Card-EngineBay-last-optim.jpg', (1200, 800)),
        ('interior', 'Revuelto_03-Interior-H_Chapter-Main_Still-B-optim.jpg', (2400, 1600, 1000)),
        ('interior-p', 'Revuelto_03-Interior-V_Chapter-Main_Still-B-optim.jpg', (786,)),
        ('int-wheel', 'Revuelto_03-Interior-H_Card-DrivingModes_Still-optim.jpg', (1200, 800)),
        ('int-passenger', 'Revuelto_03-Interior-H_Card-PassengerDisplay_Still-optim.jpg', (1200, 800)),
        ('int-engine', 'Revuelto_00-Mecha-H_Card-Engine-last-optim.jpg', (1200, 800)),
        ('gallery-1', 'gallery1-desktop.jpg', (1600, 900)),
        ('gallery-2', 'gallery2-desktop.jpg', (1600, 900)),
        ('gallery-3', 'gallery3-desktop.jpg', (1600, 900)),
        ('gallery-4', 'gallery4-desktop.jpg', (1600, 900)),
        ('gallery-5', 'gallery5-desktop.jpg', (1600, 900)),
        ('gallery-6', 'Revuelto_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-B-last-optim.jpg', (1600, 900)),
        ('gallery-7', 'Revuelto_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-C-last-optim.jpg', (1600, 900)),
        ('gallery-8', 'AR-desktop.jpg', (1600, 900)),
        ('gallery-9', 'Revuelto_01-Aero-H_Card-RearSpoiler_Opened-last-optim.jpg', (1600, 900)),
        ('gallery-10', 'Revuelto_03-Interior-H_Card-VirtualCockpit_Still-last-optim.jpg', (1600, 900)),
    ],
    'revuelto-sv': [
        ('hero', 'model_details_new__revuelto_sv__gallery1__s1_d.jpg', (2400, 1600, 1000)),
        ('hero-p', 'model_details_new__revuelto_sv__gallery1__s1_m.jpg', (786,)),
        ('exterior', 'model_details_new__revuelto_sv__banner__banner-desktop.jpg', (2160, 1440)),
        ('exterior-p', 'model_details_new__revuelto_sv__banner__banner-mobile.jpg', (750,)),
        ('ext-front', 'model_details_new__revuelto_sv__gallery1__s3_d.jpg', (1200, 800)),
        ('ext-rear', 'model_details_new__revuelto_sv__gallery1__s4_d.jpg', (1200, 800)),
        ('ext-aero', 'model_details_new__revuelto_sv__aero__RevueltoSV_01-Aero-H_Card-Downforce-last-optim.jpg', (1200, 800)),
        ('int-engine', 'model_details_new__revuelto_sv__RevueltoSV_00-Mecha-H_Card-Engine-last-optim.jpg', (1200, 800)),
        ('interior', 'model_details_new__revuelto_sv__interior__RevueltoSV_03-Interior-H_Chapter-Main_Still-B-last-optim.jpg', (2400, 1600, 1000)),
        ('interior-p', 'model_details_new__revuelto_sv__interior__RevueltoSV_03-Interior-V_Chapter-Main_Still-B-last-optim.jpg', (786,)),
        ('int-driver', 'model_details_new__revuelto_sv__interior__RevueltoSV_03-Interior-H_Card-Pilota_Still-last-optim.jpg', (1200, 800)),
        ('int-seats', 'model_details_new__revuelto_sv__interior__RevueltoSV_03-Interior-H_Card-Sedili_Still-last-optim.jpg', (1200, 800)),
        ('gallery-1', 'model_details_new__revuelto_sv__gallery1__s2_d.jpg', (1600, 900)),
        ('gallery-2', 'model_details_new__revuelto_sv__gallery1__s5_d.jpg', (1600, 900)),
        ('gallery-3', 'model_details_new__revuelto_sv__gallery1__s6_d.jpg', (1600, 900)),
        ('gallery-4', 'model_details_new__revuelto_sv__gallery1__s7_d.jpg', (1600, 900)),
        ('gallery-5', 'model_details_new__revuelto_sv__gallery1__s8_d.jpg', (1600, 900)),
        ('gallery-6', 'model_details_new__revuelto_sv__performance__RevueltoSV_00-Mecha-H_Card-CFK-last-optim.jpg', (1600, 900)),
        ('gallery-7', 'model_details_new__revuelto_sv__performance__RevueltoSV_00-Mecha-H_Card-Tires-last-optim.jpg', (1600, 900)),
        ('gallery-8', 'model_details_new__revuelto_sv__aero__RevueltoSV_01-Aero-H_Card-BrakeCooling-last-optim.jpg', (1600, 900)),
        ('gallery-9', 'model_details_new__revuelto_sv__performance__RevueltoSV_00-Mecha-H_Card-Brakes-last-optim.jpg', (1600, 900)),
    ],
    'temerario': [
        ('hero', 'model_details_new__temerario_2__config-alt__30_04_2026__Temerario_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-A-last-optim.jpg', (2400, 1600, 1000)),
        ('hero-p', 'model_details_new__temerario_2__config-alt__30_04_2026__Temerario_02-Exterior-V_Chapter-Main_Still-B_Config-Alt-A-last-optim.jpg', (786,)),
        ('exterior', 'model_details__temerario__banner-desktop.jpg', (2160, 1440)),
        ('exterior-p', 'model_details__temerario__banner-mobile.jpg', (750,)),
        ('ext-headlight', 'model_details_new__temerario_2__still_exterior__Temerario_02-Exterior-H_Card-Headlight-last-optim.jpg', (1200, 800)),
        ('ext-rear', 'model_details_new__temerario_2__still_exterior__Temerario_02-Exterior-H_Card-Rear-last-optim.jpg', (1200, 800)),
        ('ext-engine', 'model_details_new__temerario_2__still_exterior__Temerario_02-Exterior-H_Card-Engine-last-optim.jpg', (1200, 800)),
        ('int-engine', 'model_details_new__temerario_2__mecha__Temerario_00-Mecha-H_Card-Powertrain-last.jpg', (1200, 800)),
        ('interior', 'model_details_new__temerario_2__Temerario_04-Interior-H_Chapter-Main_Still-B-optim.jpg', (2400, 1600, 1000)),
        ('interior-p', 'model_details_new__temerario_2__Temerario_04-Interior-V_Chapter-Main_Still-B-optim.jpg', (786,)),
        ('int-wheel', 'model_details_new__temerario_2__Temerario_04-Interior-H_Card-DrivingModes.jpg', (1200, 800)),
        ('int-passenger', 'model_details_new__temerario_2__Temerario_04-Interior-H_Card-PassengerDisplay.jpg', (1200, 800)),
        ('gallery-1', 'model_details__temerario__2025__07_29_refresh__gallery1-desktop.jpg', (1600, 900)),
        ('gallery-2', 'model_details__temerario__2025__07_29_refresh__gallery2-desktop.jpg', (1600, 900)),
        ('gallery-3', 'model_details__temerario__2025__07_29_refresh__gallery4-desktop.jpg', (1600, 900)),
        ('gallery-4', 'model_details__temerario__2025__07_29_refresh__gallery5-desktop.jpg', (1600, 900)),
        ('gallery-5', 'model_details__temerario__2025__07_29_refresh__gallery3-desktop.jpg', (1600, 900)),
        ('gallery-6', 'model_details_new__temerario_2__config-alt__30_04_2026__Temerario_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-B-last-optim.jpg', (1600, 900)),
        ('gallery-7', 'model_details_new__temerario_2__config-alt__30_04_2026__Temerario_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-C-last-optim.jpg', (1600, 900)),
        ('gallery-8', 'model_details_new__temerario_2__still_aero__27_03_2026__Temerario_01-Aero-H_Card-Wing-last-optim.jpg', (1600, 900)),
        ('gallery-9', 'model_details_new__temerario_2__aero__Temerario_01-Aero-H_Card-Front-last.jpg', (1600, 900)),
    ],
    'urus-se': [
        ('hero', 'model_details_new__urus_se_2__alt-config__optim_22-05__Urus_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-B_27-03.jpg', (2400, 1600, 1000)),
        ('hero-p', 'model_details_new__urus_se_2__Urus_02-Exterior-V_Chapter-Main_Still-B_Config-Alt-B-optim.jpg', (786,)),
        ('exterior', 'model_details__urus_se__banner-desktop.jpg', (2160, 1440)),
        ('exterior-p', 'model_details__urus_se__banner-mobile.jpg', (750,)),
        ('ext-headlight', 'model_details_new__urus_se_2__cross-fade__Urus_01-Exterior-H_Card-Headlight-last-optim.jpg', (1200, 800)),
        ('ext-rear', 'model_details_new__urus_se_2__cross-fade__Urus_01-Exterior-H_Card-Rear-last-optim.jpg', (1200, 800)),
        ('ext-wheel', 'model_details_new__urus_se_2__cross-fade__new__Urus_02-Exterior-H_Card-Wheel-last-optim.jpg', (1200, 800)),
        ('int-engine', 'model_details_new__urus_se_2__cross-fade__Urus_04-Powertrain-H_Card-Engine-last-optim.jpg', (1200, 800)),
        ('interior', 'model_details_new__urus_se_2__Urus_03-Interior-H_Card-Connectivity_Loop-optim.jpg', (2400, 1600, 1000)),
        ('interior-p', 'model_details_new__urus_se_2__Urus_03-Interior-V_Card-Connectivity_Loop-optim.jpg', (786,)),
        ('int-selector', 'model_details_new__urus_se_2__Urus_03-Interior-H_Card-Tamburo_Loop-optim.jpg', (1200, 800)),
        ('int-screen', 'model_details_new__urus_se_2__Urus_03-Interior-H_Card-Hmi_Loop-optim.jpg', (1200, 800)),
        ('gallery-1', 'model_details__urus_se__gallery__1d.jpg', (1600, 900)),
        ('gallery-2', 'model_details__urus_se__gallery__2d.jpg', (1600, 900)),
        ('gallery-3', 'model_details__urus_se__gallery__3d.jpg', (1600, 900)),
        ('gallery-4', 'model_details__urus_se__gallery__4d.jpg', (1600, 900)),
        ('gallery-5', 'model_details__urus_se__gallery__5d.jpg', (1600, 900)),
        ('gallery-6', 'model_details__urus_se__AR-desktop.jpg', (1600, 900)),
        ('gallery-7', 'model_details_new__urus_se_2__alt-config__optim_22-05__Urus_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-C_27-03.jpg', (1600, 900)),
        ('gallery-8', 'model_details_new__urus_se_2__cross-fade__Urus_02-Aero-H_Card-RearSpoiler-last-optim.jpg', (1600, 900)),
        ('gallery-9', 'model_details_new__urus_se_2__cross-fade__Urus_01-Exterior-H_Card-Roof-last-optim.jpg', (1600, 900)),
    ],
    'urus-se-performante': [
        ('hero', 'model_details_new__urus_se_performante__exterior__alt-config__UrusSE-Performante_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-A-last-optim.jpg', (2400, 1600, 1000)),
        ('hero-p', 'model_details_new__urus_se_performante__exterior__alt-config__UrusSE-Performante_02-Exterior-V_Chapter-Main_Still-B_Config-Alt-A-last-optim.jpg', (786,)),
        ('exterior', 'model_details_new__urus_se_performante__banner__banner.jpg', (2160, 1440)),
        ('exterior-p', 'model_details_new__urus_se_performante__banner__bannermobile.jpg', (750,)),
        ('ext-front', 'model_details_new__urus_se_performante__exterior__UrusSE-Performante_02-Exterior-H_Card-ParaurtiAnteriore-last-optim.jpg', (1200, 800)),
        ('ext-bonnet', 'model_details_new__urus_se_performante__exterior__UrusSE-Performante_02-Exterior-H_Card-Cofano-last-optim.jpg', (1200, 800)),
        ('ext-spoiler', 'model_details_new__urus_se_performante__exterior__UrusSE-Performante_02-Exterior-H_Card-Spoiler-last-optim.jpg', (1200, 800)),
        ('int-engine', 'model_details_new__urus_se_performante__mecha__UrusSE-Performante_00-Mecha-H_Card-Engine-last-optim.jpg', (1200, 800)),
        ('interior', 'model_details_new__urus_se_performante__interior__02_07__UrusSE-Performante_03-Interior-H_Chapter-Main_Still-B-last-optim.jpg', (2400, 1600, 1000)),
        ('interior-p', 'model_details_new__urus_se_performante__interior__02_07__UrusSE-Performante_03-Interior-V_Chapter-Main_Tr-AB-last-optim.jpg', (786,)),
        ('int-wheel', 'model_details_new__urus_se_performante__interior__02_07__UrusSE-Performante_03-Interior-H_Card-Volante_Still-last-optim.jpg', (1200, 800)),
        ('int-seats', 'model_details_new__urus_se_performante__interior__02_07__UrusSE-Performante_03-Interior-H_Card-Trim_Still-last-optim.jpg', (1200, 800)),
        ('gallery-0', 'model_details__urus__urus_perf__gallery__04_09_26__1d.jpg', (1600, 900)),
        ('gallery-1', 'model_details__urus__urus_perf__gallery__04_09_26__2d.jpg', (1600, 900)),
        ('gallery-2', 'model_details__urus__urus_perf__gallery__04_09_26__3d.jpg', (1600, 900)),
        ('gallery-3', 'model_details__urus__urus_perf__gallery__04_09_26__4d.jpg', (1600, 900)),
        ('gallery-4', 'model_details__urus__urus_perf__gallery__04_09_26__5d.jpg', (1600, 900)),
        ('gallery-5', 'model_details_new__urus_se_performante__URUS_SE_PERFORMANTE.jpg', (1600, 900)),
        ('gallery-6', 'model_details_new__urus_se_performante__exterior__alt-config__UrusSE-Performante_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-B-last-optim.jpg', (1600, 900)),
        ('gallery-7', 'model_details_new__urus_se_performante__exterior__alt-config__UrusSE-Performante_02-Exterior-H_Chapter-Main_Still-B_Config-Alt-C-last-optim.jpg', (1600, 900)),
        ('gallery-8', 'model_details_new__urus_se_performante__aero__UrusSE-Performante_01-Aero-H_Card-FlussiLaterali-last-optim.jpg', (1600, 900)),
        ('gallery-9', 'model_details_new__urus_se_performante__mecha__UrusSE-Performante_00-Mecha-H_Card-Brakes-last-optim.jpg', (1600, 900)),
    ],
}

for slug in (sys.argv[1:] or ['revuelto']):
  SRC = ROOT.parent / '___OCT changes' / 'sources' / 'models' / slug
  for role, name, widths in SETS[slug]:
    im = Image.open(SRC / name).convert('RGB')
    for w in widths:
        tw = min(w, im.width)   # never upscaled; the file keeps the width the page asks for
        r = im if tw == im.width else im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS)
        r.save(OUT / f'{slug}-{role}-{w}.jpg', quality=80, optimize=True, progressive=True)
        r.save(OUT / f'{slug}-{role}-{w}.webp', quality=78, method=6)
    print(role, im.size, widths)
