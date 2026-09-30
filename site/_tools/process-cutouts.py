"""Normalise the model cut-outs into one family (run from the project root).
- Sources: research/cutouts-from-figma/img*_raw1.png (from Alex's Figma; lamborghini.com chooser renders)
  and research/press-images/urus-se_cutout-side-orange_1350x390.png (lamborghini.com homepage).
- Original soft ground shadows are removed (low-alpha pixels away from the body) and one generated
  contact shadow is drawn under every car, so the set reads as one.
- Scale: one px-per-mm for all cars, from nominal body length (internal scaling only, never displayed),
  so the family keeps its real proportions; every car sits on the same baseline, centred.
Outputs site/assets/img/cut-<slug>-{800,1600}.{webp,png}."""
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
R='research/'
CARS=[('temerario', R+'cutouts-from-figma/img3_raw1.png', 4706),
      ('revuelto', R+'cutouts-from-figma/img4_raw1.png', 4947),
      ('urus-se', R+'press-images/urus-se_cutout-side-orange_1350x390.png', 5123),
      ('urus-se-performante', R+'cutouts-from-figma/img2_raw1.png', 5137),
      ('revuelto-sv', R+'cutouts-from-figma/img1_raw1.png', 4947)]   # stored for later, not on the page
W,H,BASE = 1600, 560, 520
PX_PER_MM = 1400/5137
for slug, src, length in CARS:
    im=Image.open(src).convert('RGBA'); a=np.array(im)
    alpha=a[...,3].astype(float)
    body=alpha>200
    # keep antialiased edge pixels next to the body, drop the soft shadow elsewhere
    near=np.array(Image.fromarray((body*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)))>0
    a[...,3]=np.where(near, a[...,3], 0).astype('uint8')
    # remove an opaque painted ground shadow: climb from the bottom while the span
    # between the wheels is opaque (that is shadow on the ground, not car)
    h,w=a.shape[:2]; mid=a[:, int(w*.42):int(w*.58), 3] > 128
    ys_body=np.where(body.any(axis=1))[0]; y=ys_body.max()
    while y > ys_body.min() and mid[y].any(): y -= 1
    if y < ys_body.max():
        a[y+1:,:,3]=0; body[y+1:,:]=False
    im=Image.fromarray(a)
    ys,xs=np.where(body); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    car=im.crop((x0,y0,x1+1,y1+1))
    s=PX_PER_MM*length/car.width
    car=car.resize((round(car.width*s), round(car.height*s)), Image.LANCZOS)
    out=Image.new('RGBA',(W,H),(0,0,0,0))
    # generated contact shadow: soft ellipse under the wheels
    sh=Image.new('L',(W,H),0); d=ImageDraw.Draw(sh)
    cx=W//2; half=car.width*0.46
    d.ellipse((cx-half, BASE-10, cx+half, BASE+14), fill=120)
    sh=sh.filter(ImageFilter.GaussianBlur(10))
    shadow=Image.new('RGBA',(W,H),(0,0,0,0)); shadow.putalpha(sh)
    out.alpha_composite(shadow)
    out.alpha_composite(car,(cx-car.width//2, BASE-car.height))
    for w in (1600,800):
        r=out.resize((w, round(H*w/W)), Image.LANCZOS)
        r.save(f'site/assets/img/cut-{slug}-{w}.webp','WEBP',quality=82,method=6)
        if w == 800: r.save(f'site/assets/img/cut-{slug}-{w}.png',optimize=True)
    print(slug, car.size)
