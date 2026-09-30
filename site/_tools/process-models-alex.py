"""Alex's approved model art (MODELS/*.png) -> tile images. Minimal processing:
no recolour, no re-cut, shadows kept as supplied. Each car is scaled (never up) so its
body spans the same 88% of a shared 1200x430 canvas, bottoms on one baseline, with air
above the tallest roof. Outputs site/assets/img/model-art-<slug>-{600,1200}.{webp,png}."""
from PIL import Image
import numpy as np
SRC='MODELS/'
CARS=[('urus-se','image1.png'),('urus-se-performante','image 2.png'),('temerario','image 3.png'),('revuelto','image 4.png')]
W,H,BASE=1200,430,392
BODY=0.88  # lower bound of the 88-92% brief: the supplied shadows run ~1.16x body length, so 90% cut their tails at alpha 38/255; 88% leaves <=23/255 at the canvas edge
for slug,f in CARS:
    im=Image.open(SRC+f).convert('RGBA'); a=np.array(im)[...,3]
    ys,xs=np.where(a>200); bx0,bx1,by1=xs.min(),xs.max(),ys.max()
    s=min(1.0,(BODY*W)/(bx1-bx0+1))
    full=im.crop(im.getbbox()); ox,oy=im.getbbox()[:2]
    full=full.resize((round(full.width*s),round(full.height*s)),Image.LANCZOS)
    # body centre and body bottom in scaled crop coordinates
    cx=((bx0+bx1)/2-ox)*s; bottom=(by1-oy)*s
    out=Image.new('RGBA',(W,H),(0,0,0,0))
    out.alpha_composite(full,(round(W/2-cx), round(BASE-bottom)))
    assert out.getbbox()[1]>0, slug+' clipped at top'
    for w in (1200,600):
        r=out.resize((w,round(H*w/W)),Image.LANCZOS)
        r.save(f'site/assets/img/model-art-{slug}-{w}.webp','WEBP',quality=84,method=6)
        if w==600: r.save(f'site/assets/img/model-art-{slug}-{w}.png',optimize=True)
    print(slug, 'scale', round(s,3), 'top air', out.getbbox()[1])
