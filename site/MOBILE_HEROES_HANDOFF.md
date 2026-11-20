# Model pages on phones: hero images and layout (handoff, 20 Nov 2026)

**What is wrong on the demo:** on phones the model page hero shows an upright crop of the photograph full screen,
under a dark scrim and the text, so the car is mostly hidden (sky, walls, floor). Fix it on every model page.

**Target (prototype, open on a phone or at 390 px wide):** https://sigovs.github.io/PRESTIGE_LAMBO/site/model-temerario.html, and any page below.
All 19 model pages on a phone, as they should look: [handoff-model-heroes-mobile.jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/handoff-model-heroes-mobile.jpg)

## The rule
On phones (portrait, up to 767 px wide) the model hero follows **the home slider's model slide** exactly:
- a photo band `min(58svh, 118vw)` tall (460 px on a 390 × 844 phone), from the top of the screen under the header;
- the phone image fills the band (`object-fit: cover`), its lower part fading to black from 62 %;
- the copy starts over that fade: eyebrow 16 px, model name `min(4rem, (100vw − gutters) / 4.3)` (64 px), claim;
- **Inquire** full width, 72 px tall; **Configure yours** and **View inventory** as one row of text links under it;
- the lead paragraph comes after the actions.
- Short phones (up to 700 px tall): the home slider's short-phone values (name 48 px, button 56 px, eyebrow 14 px).

Desktop and tablets do not change.

## 1. CSS
Add this to the model page stylesheet (it is the end of `site/assets/css/model_v3.css` in the repo, now `?v=24`):

```css
/* ---------- phones upright: the model hero on the home slider's system (Alex, 20 Nov 2026) ----------
   "One size, one system": on phones the model hero is laid out exactly as a model slide of the home carousel
   (index_v4, main_v4.css): a photo band min(58svh, 118vw) from the top of the screen under the header, the upright
   frame (hero-p) cover-fitted and fading out from 62 %, the eyelet starting over that fade (13 % of the band up),
   eyelet 16 px, title min(4rem, (100vw - gutters) / 4.3) at 0.875, actions --btn-h-lg tall (--btn-h-md on short
   phones). The page's own extras keep their place after it: Configure and View inventory share one text row,
   and the lead follows the actions, so the actions sit where the home slide has them. */
@media (max-width: 767.98px) and (orientation: portrait) {
    .mbig { display: block; min-height: 0; padding-top: 0; --band: min(58svh, 118vw); }
    .mbig::after, .mbig__inner::before { display: none; }
    .mbig__media { position: relative; inset: auto; height: var(--band); }
    .mbig__img {
        object-fit: cover; object-position: 50% var(--m-y, 50%);
        -webkit-mask-image: linear-gradient(180deg, #000 0%, #000 62%, transparent 100%);
        mask-image: linear-gradient(180deg, #000 0%, #000 62%, transparent 100%);
    }
    .mbig__inner { margin-top: calc(var(--band) * -0.13); padding-top: 0; padding-bottom: var(--sp-40); gap: var(--sp-16); }
    .mbig__eyelet { font-size: var(--fs-16); line-height: var(--lh-24); }
    .mbig__name { font-size: min(4rem, calc((100vw - 2 * var(--page-gutter)) / 4.3)); line-height: 0.875; }
    .mbig__lead { order: 10; }
    .mbig__actions { display: flex; flex-wrap: wrap; align-items: flex-end; column-gap: var(--sp-8); row-gap: var(--sp-8); margin-top: var(--sp-16); }
    .mbig__actions .btn--accent { flex-basis: 100%; min-height: var(--btn-h-lg); }
    .mbig__actions .btn--secondary {
        width: auto; min-height: var(--tap); padding-inline: 0; gap: var(--sp-8);
        background: none; border-width: 0 0 var(--stroke-1); border-color: var(--grey-0);
    }
    .mbig__actions .btn--secondary, .mbig__actions .btn--tertiary { min-height: var(--tap); }
}
/* short phones (375×667), as the home slider (main_v4.css "Short phones"): md actions, 14 px eyelet,
   title min(3rem, …/4.3), copy gap 8, 16 before the actions */
@media (max-width: 767.98px) and (orientation: portrait) and (max-height: 700px) {
    .mbig__actions .btn--accent { min-height: var(--btn-h-md); }
    .mbig__eyelet { font-size: var(--fs-14); line-height: var(--lh-22); }
    .mbig__name { font-size: min(3rem, calc((100vw - 2 * var(--page-gutter)) / 4.3)); }
    .mbig__inner { gap: var(--sp-8); }
    .mbig__actions { margin-top: var(--sp-8); }
}
```

## 2. The phone image of each model page
In the hero `<picture>`, the first `<source>` is the phone image:

```html
<source media="(max-width: 767.98px) and (orientation: portrait)" type="image/webp" srcset="…the file below…">
```

Use these files (each was chosen so the **whole car** fits the band; most are new):

| Model | Demo page | Phone image |
|---|---|---|
| Temerario | [/temerario/](https://lamborghinimiami.aandemo.com/temerario/) | [temerario-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/temerario-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/temerario-hero-p-786.jpg) |
| Temerario Spyder | (new page, not on the demo yet) | [temerario-spyder-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/temerario-spyder-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/temerario-spyder-hero-p-786.jpg) |
| Revuelto | [/revuelto/](https://lamborghinimiami.aandemo.com/revuelto/) | [revuelto-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/revuelto-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/revuelto-hero-p-786.jpg) |
| Revuelto Sv | [/revuelto-sv/](https://lamborghinimiami.aandemo.com/revuelto-sv/) | [revuelto-sv-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/revuelto-sv-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/revuelto-sv-hero-p-786.jpg) |
| Urus Se | [/urus-se-mlp/](https://lamborghinimiami.aandemo.com/urus-se-mlp/) | [urus-se-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-se-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-se-hero-p-786.jpg) |
| Urus Se Performante | [/urus-se-performante/](https://lamborghinimiami.aandemo.com/urus-se-performante/) | [urus-se-performante-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-se-performante-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-se-performante-hero-p-786.jpg) |
| Huracan | [/huracan-mlp/](https://lamborghinimiami.aandemo.com/huracan-mlp/) | [huracan-hero-p-1020.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-hero-p-1020.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-hero-p-1020.jpg) |
| Huracan Sterrato | [/huracan-sterrato-mlp/](https://lamborghinimiami.aandemo.com/huracan-sterrato-mlp/) | [huracan-sterrato-hero-p-850.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-sterrato-hero-p-850.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-sterrato-hero-p-850.jpg) |
| Huracan Tecnica | [/huracan-tecnica-mlp/](https://lamborghinimiami.aandemo.com/huracan-tecnica-mlp/) | [huracan-tecnica-hero-p-850.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-tecnica-hero-p-850.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-tecnica-hero-p-850.jpg) |
| Huracan Sto | [/huracan-sto-mlp/](https://lamborghinimiami.aandemo.com/huracan-sto-mlp/) | [huracan-sto-hero-p-1020.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-sto-hero-p-1020.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-sto-hero-p-1020.jpg) |
| Huracan Evo Spyder | [/huracan-evo-spyder-mlp/](https://lamborghinimiami.aandemo.com/huracan-evo-spyder-mlp/) | [huracan-evo-spyder-hero-p-1020.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-evo-spyder-hero-p-1020.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/huracan-evo-spyder-hero-p-1020.jpg) |
| Urus | [/urus-mlp/](https://lamborghinimiami.aandemo.com/urus-mlp/) | [urus-hero-p-680.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-hero-p-680.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-hero-p-680.jpg) |
| Urus S | [/urus-s-mlp/](https://lamborghinimiami.aandemo.com/urus-s-mlp/) | [urus-s-hero-p-1020.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-s-hero-p-1020.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-s-hero-p-1020.jpg) |
| Urus Performante | [/urus-performante-mlp/](https://lamborghinimiami.aandemo.com/urus-performante-mlp/) | [urus-performante-hero-p-850.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-performante-hero-p-850.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/urus-performante-hero-p-850.jpg) |
| Aventador | [/aventador/](https://lamborghinimiami.aandemo.com/aventador/) | [aventador-hero-p-680.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/aventador-hero-p-680.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/aventador-hero-p-680.jpg) |
| Limited Series | [/limited-series-mlp/](https://lamborghinimiami.aandemo.com/limited-series-mlp/) | [limited-series-hero-p-707.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/limited-series-hero-p-707.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/limited-series-hero-p-707.jpg) |
| Countach Lpi 800 4 | [/countach-lpi-800-4-mlp/](https://lamborghinimiami.aandemo.com/countach-lpi-800-4-mlp/) | [countach-lpi-800-4-hero-p-1020.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/countach-lpi-800-4-hero-p-1020.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/countach-lpi-800-4-hero-p-1020.jpg) |
| Concept | [/clp-lamborghini-concept-models-north-miami-beach-fl/](https://lamborghinimiami.aandemo.com/clp-lamborghini-concept-models-north-miami-beach-fl/) | [concept-hero-p-1020.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/concept-hero-p-1020.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/concept-hero-p-1020.jpg) |
| Lanzador | [/lanzador/](https://lamborghinimiami.aandemo.com/lanzador/) | [lanzador-hero-p-786.webp](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/lanzador-hero-p-786.webp) · [jpg](https://sigovs.github.io/PRESTIGE_LAMBO/site/assets/img/models/lanzador-hero-p-786.jpg) |

## 3. Home page
The home slider gets a new **Temerario Spyder** slide (2nd of 10): https://sigovs.github.io/PRESTIGE_LAMBO/site/index_v4.html (markup in `index_v4.html`,
`.hero__slide--spyder`; images `assets/img/slide-temerario-spyder-1920/1280.*`). Its page is https://sigovs.github.io/PRESTIGE_LAMBO/site/model-temerario-spyder.html.

## Checks (please report each)
- [ ] On a 390 × 844 phone every model page shows the whole car in the top band, the name, claim, Inquire and both text links on the first screen.
- [ ] Each model page uses the phone image from the table (not the desktop image, not the old crop).
- [ ] Desktop (1440, 1920) and tablets look exactly as before.
- [ ] No horizontal scroll on phones.
