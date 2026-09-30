# Lamborghini Miami: design system (homepage v1)

**What this is:** the working system for the Lamborghini Miami dealer subsite. It is reconstructed from evidence about the current Lamborghini corporate website. It is **not** an official Lamborghini specification, and nothing here claims brand compliance. Dealer web standards are not public (research §3.3), so this system has to be checked with Lamborghini Americas before launch.

**Tags used on every line:**
- **OBSERVED**: measured or seen on a live Lamborghini property. The source is given as a research section (`CI §x` = `research/LAMBORGHINI_CI_RESEARCH.md`) or a screenshot in `research/corp-site-shots/`, abbreviated `shot NN`.
- **DECISION**: our own call, with the reason.

**Where the values live:** `assets/css/tokens.css` is the single source of truth. Every value below is a token there.

**Dialect:** there is no stored design-dna dialect for this build. The build uses a brief-derived dialect called **"Lamborghini corporate"**, taken from the evidence below. Where it disagrees with a design-dna invariant, the invariant wins, and the yield is recorded in §10.

---

## 1. Typography

### 1.1 Typeface

| | |
|---|---|
| OBSERVED | The corporate typeface is **Lambotype**: variable, with `wdth` 0–100 and `wght` 300–900. Its named widths are UltraCnd (wdth 0), Cnd (wdth 50) and Normal (wdth 100). The font file says "exclusively for Lamborghini", and the Terms of Use protect the fonts (CI §1.2, §3.1) |
| OBSERVED | Corporate fallback stack: `LamboType, Roboto, "Helvetica Neue", Arial` (CI §1.2) |
| DECISION | **Lambotype is not downloaded or self-hosted.** It is proprietary, and no licence has been granted to us |
| DECISION | Stand-in: **Roboto Flex** (Google Fonts, variable). Its axes are `wdth` 25–151, `wght` 100–1000 and `opsz`. It is from the same family as corporate's own fallback, and it is the only free face whose width axis can reproduce the three-width system |
| DECISION | Everything goes through **one family token, `--font-brand`**. Swapping to a licensed Lambotype is one line in `tokens.css`, plus remapping the three width tokens (see the commented `@font-face` scaffold there) |
| DECISION | The widths are tuned by eye against shots 01, 06 and 07:<br>• `--wdth-ultra: 25` (the Roboto Flex minimum) stands in for UltraCnd<br>• `--wdth-cnd: 60` stands in for Cnd<br>• `--wdth-normal: 100`<br>At wdth 25, Roboto Flex is slightly wider than Lambotype UltraCnd, so display sizes run one token step smaller where a line would otherwise break |

### 1.2 Role scale

Sizes are in px, desktop → mobile. "Cnd" and "Ultra" are the width tokens from §1.1.

| Role | Size / line-height | Width, weight | Case | Source |
|---|---|---|---|---|
| Display XL (hero H1) | 120/110 → 80/70 | Ultra, 700 | UPPER | OBSERVED: hero title (CI §1.3, shot 01/03) |
| Model name (range tiles) | 56/52 → 48/46 (fluid below 356 px) | Ultra, 700 | UPPER | OBSERVED: `model__title` in "Configure your" runs 120/110 desktop and 48/38 mobile (CI §1.3).<br>DECISION: 56 on desktop, because four names share one band and the photograph, not the name, is now the dominant in each tile |
| Banner title (chapter openers) | 80/80 → 48/46 | Ultra, 700 | UPPER | OBSERVED: `lam-banner__title` is 80/90 Cnd (CI §1.3).<br>DECISION: set Ultra instead, so each chapter opener belongs to the same voice as the display names; leading is tightened because the lines are single words |
| Section title (h2 smart title) | 40/46 → 28/38 | Normal, 700 | UPPER | OBSERVED (CI §1.3 "MODELS") |
| Eyelet / kicker | 27/37 → 18/28 | Normal, 700 | UPPER | OBSERVED (CI §1.3) |
| Card title (inventory) | 27/37 → 24/32 | Normal, 700 | Title case, e.g. "2024 Revuelto" | OBSERVED on the Selezione search: H3 27/37, 700, sentence case (Playwright, 30 Sep 2026) |
| Lead | 18/28 | Normal, 400 | Sentence | OBSERVED (CI §1.3) |
| Body | 16/24 | Normal, 400 | Sentence | OBSERVED (CI §1.3) |
| Spec label | 18/28 → 16/24 | Normal, 400, `--text-3` | UPPER | OBSERVED (CI §1.9, shot 07) |
| Spec value | 18/28 → 16/24 | Cnd, 700 | UPPER | OBSERVED (CI §1.9, shot 07) |
| Nav, buttons | 16/24 (nav 18/28 in the menu) | Cnd, 700 | UPPER | OBSERVED (CI §1.3, §1.5) |
| Legal / utility | **14/22** | Normal, 400 | Sentence | OBSERVED: corporate sets 12/22 on mobile (CI §1.3).<br>DECISION: raised to 14, because of the design-dna I7 functional-text floor |

- **Tracking.** OBSERVED: corporate uses `letter-spacing: normal` everywhere (CI §1.3). DECISION:
  - Uppercase at 40px and below is tracked at **0.08em** (design-dna typography I4).
  - Uppercase display at 48px and above stays at **0**, which is the I3 optical correction for large, condensed type. See §10.
- **Figures.** DECISION: prices, mileage, phone numbers, hours and KPI values use `tabular-nums` (I5).
- **Line breaks.** DECISION:
  - Display lines are broken by hand ("LAMBORGHINI / MIAMI").
  - Headings use `text-wrap: balance`.
  - Body text uses `text-wrap: pretty` with a measure of 60ch or less.

---

## 2. Colour and contrast

| | |
|---|---|
| OBSERVED | Palette: monochrome black and white with a neutral grey ramp:<br>`#fff #f5f5f5 #dcdcdc #c4c4c4 #ababab #969696 #7d7d7d #626262 #494949 #313131 #181818 #000` (CI §1.4) |
| OBSERVED | Accent: `#FFC000` on dark and `#917300` on light.<br>Hover: `#997300` (dark) and `#423500` (light).<br>Focus: `#1e90ff` (CI §1.4) |
| OBSERVED | Surfaces:<br>• dark: surface-0 `#000`, surface-1 `#181818`<br>• light: surface-0 `#fff` |
| OBSERVED | On Selezione, prices are set in the accent `#FFC000`, 27px bold, on black cards (Playwright capture, 30 Sep 2026) |
| DECISION | **No other hue is allowed.** The current site's `#ffcc00` and `#1c75bc` are dropped. Colour in the photography is the only other colour on the page |
| DECISION | Light bands use **`#ffffff`, not `#f5f5f5`**. On `#f5f5f5`, both the `#917300` accent text (4.14:1) and the `#1e90ff` focus ring (2.97:1) fail. On `#fff` they measure 4.51:1 and 3.24:1 |
| DECISION | The accent is spent in exactly three places:<br>• the primary action on each band (accent button)<br>• inventory prices<br>• the active or hover rule under text links<br>It is never used as decoration |

**Measured pairs** (WCAG 2.x ratios, computed from the tokens; the composited checks are in the verification log):

| Pair | Ratio | Use |
|---|---|---|
| `#f5f5f5` on `#000` | 19.26 | text-1 on surface-0 |
| `#f5f5f5` on `#181818` | 16.29 | text-1 on surface-1 |
| `#c4c4c4` on `#181818` | 10.18 | spec labels |
| `#969696` on `#181818` | 6.00 | text-5, the lowest grey allowed on dark |
| `#7d7d7d` on `#181818` | 4.31 | **not used for text** |
| `#ffc000` on `#000` / `#181818` | 12.79 / 10.82 | prices, accent |
| `#000` on `#ffc000` | 12.79 | accent button label, dark band |
| `#181818` on `#fff` | 17.4 | text on light |
| `#626262` on `#fff` | 6.1 | text-4 on light |
| `#fff` on `#917300` | 4.51 | accent button label, light band (AA) |
| `#1e90ff` on `#000` / `#181818` / `#fff` | 6.49 / 5.49 / 3.24 | focus ring, non-text: needs 3:1 or more |

Text over photography is placed only in fields that are dark at capture: the black studio field of the hero and the dark diffuser band of the Ad Personam image. A gradient scrim is a sibling layer, never a child of the copy. Ratios measured on the render are in the report.

---

## 3. Grid and spacing

| | |
|---|---|
| OBSERVED | Bootstrap `.container`, max-width 1320 at 1440 (65 px side margin); 24 px gutter; 12 columns (CI §1.6) |
| OBSERVED | Mobile container padding is 24 px (CI §1.6) |
| OBSERVED | Spacing scale: 4 · 8 · 16 · 24 · 32 · 40 · 48 · 56 · 64 · 72 · 80 · 88 (CI §1.6) |
| OBSERVED | Section padding: 64/0/64 and 40/0/40 (CI §1.6) |
| DECISION | Grid: 12 columns, 24 px gutter, and a container of `min(1320px, 100% − 2×page gutter)`. The page gutter is 24 px below 768, 40 px from 768 to 1199, and 60 px from 1200 |
| DECISION | Two extra spacing steps: **120** and **160**, both multiples of the 8 px base. The observed 64 px section padding works on corporate's model pages, which alternate short bands. On a dealer homepage with seven chapters it compresses the pauses, so section padding is 120 top / 160 bottom on desktop and 72/96 on mobile. Sections exhale downward |
| DECISION | Internal gaps are always smaller than external ones: 8/16 within a group, 24–48 between groups, 120–160 between sections |

---

## 4. Header and navigation

| | |
|---|---|
| OBSERVED | Fixed header, **104 px desktop / 80 px mobile**, z-index 1040 (CI §1.7) |
| OBSERVED | Layout: burger with the "MENU" label on the left, bull-only logo (57×59) in the centre, search on the right (shot 01) |
| OBSERVED | Over the hero, a gradient runs from `#181818` to transparent. On scroll a solid surface-1 layer fades in (`opacity .3s ease-out`). The header hides on scroll-down with `translateY(-100%)`, `transform 1s linear` (CI §1.7) |
| OBSERVED | Menu: a full-screen overlay; level-1 items in 18 px Cnd Bold (CI §1.7) |
| DECISION | The bull is centred, using the corporate header SVG (`assets/img/bull.svg`). It is not redrawn or recoloured |
| DECISION | Dealer essentials are always visible, because a dealer's job is the phone and the stock:<br>• Left: MENU · NEW · PRE-OWNED · SERVICE (at 1200 px and up).<br>• Right: the sales phone plus a CONTACT link.<br>• Below 1200 px: MENU and a phone icon (a `tel:` link) |
| DECISION | Search is dropped: this dealer site has no site search. Inventory search lives on the inventory page, and a search icon that went nowhere would be a dead end |
| DECISION (user direction, Alex, 30 Sep 2026) | **The header never hides.** It stays fixed and visible at every width, and only its ground changes. This overrides the OBSERVED corporate `.to-hide` pattern (CI §1.7).<br>Ground by position:<br>• over the hero, and over the full-bleed Ad Personam photograph: the transparent gradient<br>• everywhere else: solid `#181818`<br>It turns solid at `scrollY ≥ heroEnd − 1`, so an anchor landing exactly on #range is already solid.<br>**It also turns solid as soon as any hero content comes within 8 px of its bottom edge** (coordinator decision, following the corporate solid-on-scroll layer, CI §1.7). Content means the active slide's copy and actions, and the controls. At rest the hero keeps the transparent header.<br>• The test uses where the content is heading, not only where it is: Lenis' target for a wheel glide, the measured velocity × 350 ms for a native or touch fling, and the swept span in between. So the 300 ms fade starts early enough, and it is re-run on the wheel or touch gesture itself.<br>• Where the copy rests closer than 64 px to the header (landscape phones, 21 px), the solid layer arrives at once (`--hdr-fade: 0ms`) rather than fading.<br>• Over Ad Personam the header stays transparent, except for the stretch in which its copy would pass under it.<br>• Verified at 1440×900, 1024×768, 390×844, 375×667 and 844×390, sampling every frame of a Lenis scroll through the hero and through Ad Personam (both directions): the solid layer's opacity was ≥ 0.95 on every frame in which hero or ADP text or buttons overlapped the header (one frame at 1024 read 0.949). Anchors still land at the header height with the right ground; #ad-personam lands clear.<br>Every in-page target carries `scroll-margin-top: var(--header-h)` (104 / 80 px), which Lenis `anchors` honours. Ad Personam lands flush and clears the header with its own padding.<br>Verified at 7 viewports that all 8 anchors land at `top = header height` with the correct ground |
| DECISION | The solid layer comes on only once the header has left the hero, not on the first scrolled pixel. That keeps an opaque bar from cutting across live content (design-dna U-rule) |
| DECISION | The menu overlay is a `<dialog>`-style panel:<br>• marked `data-lenis-prevent`<br>• closes on Escape<br>• returns focus to the trigger |

---

## 5. Buttons, links and icons

| | |
|---|---|
| OBSERVED | Button variants (CI §1.5):<br>• **primary**: white on dark / black on light<br>• **accent**: `#FFC000` with black text on dark; `#917300` with white text on light<br>• **secondary**: 1 px outline<br>• **tertiary**: text with a 1 px bottom border<br>`border-radius: 0` for all |
| OBSERVED | Height: **72 px** (large) or **56 px** (medium).<br>Padding: 24 or 16 px.<br>Label: 16/24, uppercase, Cnd Bold, with a trailing icon and a 24 px gap (CI §1.5) |
| OBSERVED | Below 767.98 px, buttons go full width (CI §1.5) |
| OBSERVED | Hover states:<br>• primary: → `#c4c4c4` on dark, → `#494949` on light<br>• accent: → the accent hover token<br>Transitions: 0.2–0.25 s (CI §1.5, §1.8) |
| OBSERVED | Selezione's "VIEW DETAILS" button: white, 44 px high, 18 px (Playwright, 30 Sep 2026) |
| DECISION | Icons are a single set: 24 px, stroke 1.5, square caps. The shapes are an arrow →, an external arrow ↗, a phone, pause and play, and the burger/close.<br>The **hexagon arrow buttons are now reinstated** (48×52, corporate `btn-icon-special`), because the hero carousel gives them a job |
| DECISION | Arrow hover: the arrow moves 4 px right over 0.25 s ease-out. Its focus-visible state is identical to its hover |
| DECISION | Focus: a 2 px `#1e90ff` outline with a 3 px offset, on every interactive element |
| DECISION | Tap targets are at least 44×44 px, while type keeps its size:<br>• inline links (phone numbers, spec links, menu phones) grow with `padding-block: 12px` and an equal negative margin<br>• header controls and nav links have `min-width: 44px`<br>• each spec row holds at most one link, so the grown targets never overlap<br>Verified: no visible link or button below 44 px at any of the 7 viewports |
| DECISION | "Price on request" uses the price role (27/37) in `#c4c4c4` grey, not the accent |

---

## 6. Images: composition and cropping

| | |
|---|---|
| OBSERVED | Imagery is dark, low-key, cinematic film stills: cars on black or studio plates, not catalogue cut-outs (CI §1.10) |
| DECISION | **One grade:** low-key, dark field. The hero (Temerario, black studio) and Ad Personam (the Revuelto rear at sunset, Alex's frame) share it. The workshop and archive photographs are documentary, and each sits in its own chapter |
| DECISION (user direction, Alex, 30 Sep 2026) | **The hero is a five-slide carousel**, after the corporate claim-led model carousel (CI §1.1, shots 01/03).<br>**Slides:**<br>1. The dealer slide (unchanged frames)<br>2. Temerario — "You can't hide who you are"<br>3. Revuelto — "The quantum of driving"<br>4. Urus SE — "Dare to live more" (the documented earlier Urus claim)<br>5. Urus SE Performante — "Urus at its peak"<br>**One text structure on every slide** (Alex, 30 Sep 2026), so the crossfade and the centring stay steady:<br>• an eyelet (slide 1 "Authorized Lamborghini Dealer", model slides the model name)<br>• a title in exactly two authored lines on every slide and at every width (`.hero__line`, `nowrap`): Lamborghini / Miami · You can't hide / who you are · The quantum / of driving · Dare to / live more · Urus at / its peak<br>• one supporting line: the address on slide 1; on model slides a key-figures line from the Models ledger (e.g. "920 CV · 343 km/h · 0–100 km/h 2.7 s"), in `--grey-1` so it holds 4.5:1 over photographs<br>• exactly two actions: View inventory / Enquire, or Explore the model ↗ / Enquire. The third "In our inventory" link was removed, since the inventory is one scroll away.<br>All titles share one size per viewport (`--hero-title-fs`): 120 px from 1200, 80 px from 768, min(64 px, width ÷ 4.3) on phones, 48 px on phones ≤ 700 px tall, 40 px on landscape phones.<br>**Composition:** copy and actions form one `.hero__group`, centred vertically in the free field:<br>• landscape (≥ 768 landscape, or ≥ 1200): between the header's bottom edge and the top of the control row<br>• portrait (< 1200): between the photo field's car band (`--hero-scene-h × --photo-k`) and the control row<br>`--ctrl-b` and `--ctrl-h` are the control row's own offset and height, so the field ends exactly where the controls begin. Measured: gapTop = gapBottom on every landscape viewport (1440: 148/148, 1920: 238/238, 1024: 135/135, 844×390: 21/21).<br>**Images (rebuilt 30 Sep 2026 at Alex's direction, "take several good images from the folder"):** every slide is a full-bleed photograph; the Urus SE side-profile band is gone.<br>1. Dealer: Alex's own edit of img8, `slide 1d.jpg` (the car shifted right, the left darkened), on landscape and portrait tablets, with a light scrim only (0.5); the night-circuit Temerario on phones<br>2. Temerario: Alex's gallery2 (Sant'Agata sign at sunset), cropped so the sign leaves the frame<br>3. Revuelto: Alex's img6 aerial at every size<br>4. Urus SE: the official rocks-at-sunset frame (urus_se/gallery/4d) on landscape; the orange dust frame on phones<br>5. Urus SE Performante: unchanged (lime, night)<br>**Alex's rule:** a title or button may overlap a non-critical part of the car (roofline, rear haunch, background), but never the face or front, the badge or the wheels, provided worst-pixel contrast holds through a restrained left scrim. Sources and crops are in MANIFEST. Desktop frames are full-bleed with a constructed left scrim; Urus SE uses its side-profile band lower-right. Phones use a shorter photo field (`min(58svh, 118vw)`) with a per-slide authored `object-position`.<br>**Behaviour:**<br>• crossfade 800 ms (`--dur-slide`); the text rises in with the rise tokens<br>• autoplay 6.5 s per slide (`--slide-hold`), with numbered progress segments 01–05 and a pause/play control<br>• autoplay pauses on hover, on focus within, on a hidden tab and when the hero is off-screen, and never starts under reduced motion<br>• hexagon prev/next, ←/→ keys, horizontal swipe (`touch-action: pan-y`, so vertical scrolling stays with the page)<br>• ARIA carousel pattern (region / slide "n of 5"), inactive slides `inert` + `aria-hidden`, and a live region that is polite only when not autoplaying<br>• slide 1 is the only preloaded image (LCP); the other slides' images load on idle<br>Without JS, only slide 1 exists. `?figma&slide=N` shows slide N alone, with its images loaded.<br>**Legibility (re-measured after the image rebuild):** all slides pass at all eight viewports; the per-slide minima are in the report. Earlier measurement: worst-pixel contrast was measured per slide at 1920, 1440, 1024, 768, 390, 375, 320 and 844×390. Titles are at least 4.4:1 (large text, needs 3:1); eyelets, the supporting line and the button labels are at least 4.68:1. Temerario desktop framing moved to `20% 50%` with scrim 0.84, and the tablet-landscape scrim 0.9 now outranks the per-slide values. On landscape phones the Urus SE band narrows to 50%, so the centred actions clear the car. Over photographs the secondary button carries a 64% black fill, and a quiet floor gradient sits under the controls |
| DECISION | **Phone hero (portrait, below 768 px).** An authored frame: the yellow Temerario on a night circuit (official lamborghini.com gallery image, crop x 950–2450). It is a full-width photographic field of `min(74svh, 160vw)`, or 66svh on phones 600 px tall or less. The car sits in the upper field at about 90% of the width, and the copy stands in the dark asphalt below it. There is one primary action (View inventory); Enquire becomes a 44 px text link. The desktop keeps the blue Temerario, so the colour differs by format by design (authored mobile frame, DM10 / GI8) |
| DECISION | Hero: full-screen *scene*, not full-frame *object*. The black studio field is the text-safe zone.<br>• **Landscape and ≥1200 px:** copy and actions form one mass, upper-left, with actions 32 px under the copy. The car owns the lower-right diagonal. The lower-left black is the photograph's own studio field (the image box spans the full width), not page void.<br>• **Portrait (phones, portrait tablets):** the photograph is **in flow** as the middle row between copy and actions (`object-fit: contain`), so it can never run under the text.<br>• **Short phones (height ≤ 700 px) and landscape phones (height ≤ 600 px):** compressed display size and medium buttons, so both actions fit above the fold.<br>• Crops: desktop uses the full 1920×707 frame with a feathered top; portrait uses `hero-temerario-m`, x 760–1920 |
| DECISION | No "Pictured" caption in the hero. The car carries its own TEMERARIO plate in frame, and the caption measured 1.47:1 over the lit blue floor |
| DECISION (user direction, Alex, 30 Sep 2026) | **Ad Personam: exactly one screen, the copy at the bottom, pinned.**<br>• **Image:** Alex's `NEW IMAGES/img2` (the rear of a yellow Revuelto at sunset: taillight, haunch, diffuser), a craft and detail frame for "colours, materials and details". It replaces the Urus SE cabin, whose files stay on disk. There are two authored crops: `adp-rear-l` (the full frame) and `adp-rear-p` (the taillight column, x 40–80%). gallery5 was considered and not used: its lower field is bright yellow paint, which cannot hold text at the bottom.<br>• **Height:** `height: 100svh` (100vh fallback). Measured equal to the viewport at 1920×1080, 1440×900, 1024×768, 768×1024, 390×844, 375×667, 320×568 and 844×390; nothing sits below the fold and nothing scrolls inside it.<br>• **Copy:** eyelet, title, lead and both actions form one group anchored to the bottom, left on the container. The bottom padding is `--adp-pad-b`: 64 px from 768, 40 px on phones, 24 px on landscape phones.<br>• **Landscape:** full bleed at `100% 50%` (the wheel pushed left). The title sits left and the lead and actions right, bottom-aligned on the dark diffuser band, with a restrained sibling bottom gradient (0.78 → 0 over 58%; on landscape phones 0.9 → 0.76 at 62% → 0).<br>• **Portrait:** the frame is in flow and takes exactly the height the copy leaves, fading to black at its foot, so the copy stands on black. On phones ≤ 600 px tall the lead steps to 14/22.<br>• **Worst-pixel contrast** (text made transparent, brightest pixel under each box): eyelet ≥ 10.6:1, title ≥ 12.4:1, lead ≥ 10.3:1, secondary button label ≥ 17.4:1, at all eight viewports.<br>• **Pinned (Alex):** the section is `position: sticky; top: 0` inside `.adp-pin`, which wraps Ad Personam and Service and bounds the pin. Service (`z-index: 1`, opaque #181818) scrolls up over the held frame. This is pure CSS, so Lenis drives it natively; `body` uses `overflow-x: clip`, which does not break sticky. As Service covers the frame it dims to 55% (`--adp-cover`, set in main.js; not under reduced motion, where only the sticky remains). The anchor `#ad-personam` sits on the wrapper, because a stuck element reports top 0 and cannot be scrolled to by its own box.<br>• **Header:** transparent over the uncovered frame; solid once Service's top edge reaches the header. With the copy at the bottom of a pinned frame it never passes under the header.
| DECISION | Watermarks: the official images carry a stamped "Lamborghini Miami" shield at the bottom right. Every crop removes it (`_tools/process-images.py`); **no image is shown with a stamp** |
| DECISION | Inventory photos top out at 1024×768 and carry a footer band. They are cropped to 16:9 above the band, and never displayed wider than about 512 CSS px, so 2× displays get the native 1024 px |
| DECISION | Archive prints are 640×427. They are shown at 320 CSS px or less, as prints, never enlarged |
| DECISION | **No image stands in for a model it is not.** Revuelto and Urus SE Performante have no official image in the asset set, so the range is typographic (§7). The one new Temerario in stock has no photographs yet, so its card uses a typographic plate marked "Photography in preparation" |

---

## 7. Section layouts

Corporate composes its home page as "hero → models → dealer locator → configure → legal" (CI §1.1). The dealer adaptation keeps that order and inserts the dealer's own chapters.

| # | Section | Ground | Layout |
|---|---|---|---|
| 1 | **Hero**: the dealer identity over the Temerario scene | `#000` | Headline mass lower-left, model caption and CTA cluster; full-screen scene |
| 2 | **The range**: four current models | `#fff` | A 2×2 grid, one column on phones. Each tile holds **Alex's approved model art** (`MODELS/image1.png` Urus SE, `image 2.png` Urus SE Performante, `image 3.png` Temerario, `image 4.png` Revuelto), all facing right, on white.<br>• Processing is resize-and-export only (`_tools/process-models-alex.py`): built-in shadows kept, no recolour, no re-cut, never upscaled (scale 0.94–0.96). Every body spans the same 88% of a shared 1200×430 canvas, body bottoms sit on one baseline (y 392), with 35–132 px of air above the roofs. Output: webp at 600/1200 w + 600 w png fallback.<br>• 88% rather than 90% because the supplied shadows run about 1.16× body length: at 90% their tails were cut at the canvas edge at alpha 38/255; at 88% the residue is ≤ 23/255.<br>• `.model__media` has aspect-ratio 1200/430, equal to the art, so `object-fit: contain` never crops at any width.<br>• The earlier normalised cut-outs (`cut-*`, `_tools/process-cutouts.py`) are retired from the page and kept on disk.<br>• Every tile carries the **same standard block**: folio and name, the claim, three spec rows (Max power (combined ICE+EE) · Top speed · 0–100 km/h), then **two solid buttons** (Alex, 30 Sep 2026): Enquire → as the solid primary (`#000` fill, white text, 21:1) and Configure ↗ as the solid secondary (`.btn--solid`: `#dcdcdc` fill, `#000` text, 15.3:1; hover `#c4c4c4`, 12.2:1).<br>• Both are medium buttons: 56 px tall, 16 px padding, square corners. The `#917300` accent fill is not used here, because white on it is below 4.5:1 at 16 px.<br>• Layout: split 50/50 across the tile, and on one line across both tiles of a row (bottom-aligned at ≥ 1200, and a fourth subgrid row on tablets). They stack full width below 360 px, where a half would be 125 px and too narrow for CONFIGURE ↗.<br>• Focus: the global 2 px `#1e90ff` ring at a 3 px offset, on both buttons.<br>• On tablets the tiles share row lines through CSS subgrid, so a two-line name never pushes one spec block below its neighbour's.<br>• Hover and focus: the model name takes the accent colour, and nothing moves. The 6 px car travel was removed on 30 Sep 2026 at Alex's direction: while scrolling, tiles passing under a resting cursor toggled it, so the cars "twitched". The only car motion is the one-time drive-in on entry (§8).<br>• The on-page source/date line was removed at Alex's direction; the provenance lives in DATA_SOURCES. The Revuelto SV note is in the footer only |
| 3 | **Inventory**: in the showroom | `#181818` | Its own section. The group headings (New / Pre-owned) sit inline above their grids at every width, with no left rail, so the cards take the full 12 columns. Rows always fill: New (2 cards) is a pair from 768 px, and Pre-owned (3 cards) is a trio from 1024 px; below 1024 Pre-owned stacks to one column rather than leave an orphan. Cards in a row are equal height and share one 16:9 image ratio. Cards are a **dealer adaptation of the Selezione search card**: title, colour and stock line, photo, an Odometer row with a rule, an accent price and a View vehicle button. The VIN is left on the VDP and in DATA_SOURCES (operational detail). The fee basis is printed under the grids |
| 4 | **Ad Personam** | full-bleed photograph | One-screen chapter (100svh), pinned while Service slides over it; the copy group sits at the bottom. The yellow Revuelto rear at sunset (Alex's img2), with authored landscape and portrait crops (§6) |
| 5 | **Service & ownership** | `#181818` | Portrait workshop photograph with a service list set as **technical-specification rows**. These are corporate's label/value rows with 1 px `#626262` rules (shot 07), carrying departments and phone numbers instead of engine data |
| 6 | **The house**: showroom and heritage | `#fff` | Dealer lockup, the introduction, the night aerial, and a dated strip of archive prints. **The lockup is a stand-in:** the unaltered 2024 bull, shown through a CSS mask in `currentColor`, plus "LAMBORGHINI MIAMI" set in type. It replaces the pre-2024 3D shield PNG so the page speaks one identity generation. Swap it for the official 2024 dealer lockup when that arrives |
| 7 | **Visit** and **footer** | `#000` | Address, departmental phones and hours as a tabular spec, directions; then the footer and the legal lines |

---

## 8. Motion

| | |
|---|---|
| OBSERVED | Buttons and links: 0.2–0.25 s ease / ease-out.<br>Fades: opacity 0.3–0.5 s ease-out.<br>Reveals: transform + opacity 0.5 s ease-out.<br>Header: 1 s linear hide (CI §1.8) |
| OBSERVED | Corporate offers an "Allow animations" toggle (CI §1.7) |
| DECISION | Duration tokens: `--dur-fast` 200 ms, `--dur-base` 300 ms, `--dur-reveal` 500 ms. Easing: `--ease-out` cubic-bezier(.2,.7,.2,1) and `--ease-in` cubic-bezier(.4,0,1,1) |
| DECISION (user direction, Alex, 30 Sep 2026) | **Every text element rises into place as it enters.** This covers headings, eyelets, paragraphs, spec rows (each `dt`/`dd`), card titles, meta and prices, captions, footer items, and buttons (each button as a whole).<br>• Tokens: `--rise` 28 px (text ≥ 20 px), `--rise-sm` 16 px (smaller text), `--dur-rise` 700 ms, `--ease-rise` cubic-bezier(0.2, 0.7, 0.2, 1) (= `--ease-out`), `--rise-step` 70 ms sibling stagger, `--rise-cap` 400 ms maximum wait.<br>• Trigger: IntersectionObserver, threshold 0.15, rootMargin `0px 0px 8% 0px` (fires just before the element is in view), once per element.<br>• The hero uses the same rise on load.<br>• Only transform and opacity animate; the classes are removed once the rise completes, so hover transitions come back.<br>**Tension with motion-judgment MJ7** (comprehension never waits on choreography), and how it is contained:<br>• the trigger fires early<br>• the stagger is capped at 400 ms<br>• an anchor jump releases the whole destination section at once (measured opacity is at least 0.83 within 250 ms of landing)<br>• keyboard focus reveals the focused element instantly<br>• a safety sweep releases anything on screen that the observer missed<br>Under reduced motion no classes are added (everything static and visible). With JS off, or in `?figma`, nothing is ever hidden.<br>Line-by-line masking of display titles was **not** done: it would need text splitting that is fragile under font swap and `text-wrap: balance` |
| DECISION (user direction, Alex, 30 Sep 2026) | **Model tiles: each car drives in from the left and rolls to a stop** (Alex: the range "appears too abruptly"). The cars face right, so they arrive from behind.<br>• Tokens: `--drive-distance` −15 % of the tile width (−96 px at 1440, −49 px at 390), `--dur-drive` 1250 ms on `--ease-drive` cubic-bezier(0.16, 1, 0.3, 1); opacity 0 → 1 over `--dur-drive-fade` 600 ms (`--ease-out`), so the car is seen rolling, not ghosting. The second tile of a row follows after `--drive-stagger` 135 ms, left tile first. The baked-in shadow travels with the car.<br>• The tile's text follows with the ordinary rise, starting `--drive-text-lag` 200 ms after its car. The 70 ms step and 400 ms cap still apply, so the last line of a tile starts ≤ 600 ms after its car.<br>• Trigger: 30 % of the car's box in view (IntersectionObserver). A second observer 60 % below the fold switches the image to eager and `decode()`s it, and the drive waits for that decode (at most 1.2 s), so a car never starts blank and then pops in.<br>• Transform and opacity only. The travel is clipped by `.model__media { overflow: hidden }`, so it never reaches the page width. The classes are removed when the drive ends; the car then has no hover motion (see §7).<br>• An anchor jump into the range, keyboard focus in a tile, and the safety sweep (same 30 % bar) all drive the tile, so nothing stays hidden.<br>• Reduced motion: no drive, cars at rest from the start. With JS off, or in `?figma`: final state |
| DECISION (defect fix, 30 Sep 2026) | **The slider controls leave with the hero.** Before this, the control row (01–05, pause, arrows) showed through the transparent header while the hero scrolled out. The header is unchanged.<br>• The row's opacity follows its distance above the header's bottom edge (104 / 80 px). It fades over `--ctrl-fade` 96 px of travel and reaches 0 `--ctrl-gap` 8 px before it touches the header, then comes back on scroll-up.<br>• Opacity only, set from the scroll handler (Lenis drives native scroll), so it happens in the same frame. Below 0.5 it takes no pointer events; at 0 it is `inert`.<br>• Reduced motion: a plain hide once it is under the gap, with no fade |
| DECISION (user direction, Alex, 30 Sep 2026) | **Hero text slides in from the left** on first load and on every slide change, replacing the rise.<br>• Every line moves on its own: eyelet, each title line, the supporting line and the action row. Each starts at `--hero-in-x` −48 px with opacity 0 and arrives over `--dur-hero-in` 750 ms on `--ease-drive`, staggered by `--hero-step` 80 ms top to bottom (capped at `--hero-cap` 400 ms).<br>• The outgoing slide's lines fade over `--dur-hero-out` 250 ms without travel, and the incoming lines start only after that, so the two sets never overlap. The image crossfade (800 ms) is unchanged.<br>• Measured at 1440 and 390: outgoing opacity is 0.04 at 150 ms and 0 at 300 ms; the first incoming line is at −31 px / 0.36 at 300 ms, and all lines are settled by 1.2 s.<br>• Reduced motion: no travel and no hidden state; the text is simply present |
| DECISION | Smooth scroll uses **Lenis** (design-dna DNA90):<br>• `autoRaf: true` (there is no GSAP on the page)<br>• `anchors: true`<br>• not constructed under `prefers-reduced-motion: reduce`<br>• the menu overlay is marked `data-lenis-prevent` |
| DECISION | Reduced motion is designed, not switched off:<br>• reveals are replaced by the final state<br>• button arrows change colour instead of moving<br>• Lenis is off, so scrolling is native<br>The header is persistent at all times anyway (§4) |

---

## 9. Responsive behaviour

| | |
|---|---|
| OBSERVED | Mobile: header 80 px, container padding 24 px, full-width buttons, hero title 80/70 (CI §1.3, §1.5, §1.6) |
| DECISION | Breakpoints: 768 and 1200 (px)<br>• **Hero**: recomposed on mobile — headline at the top, car beneath, CTA stack at the bottom.<br>• **Range**: rows stack as name → claim → facts → actions.<br>• **Inventory**: one column of cards; the group labels become inline headings.<br>• **Service**: the image moves above the spec rows.<br>• **House**: the archive prints scroll horizontally *inside* their own strip (`data-lenis-prevent`), never the page |

---

## 10. Where design-dna invariants bent the corporate evidence

- **I7, the 14 px floor.** Corporate legal and utility text is 12 px on mobile. Here it is 14 px.
- **I4, uppercase tracking.** Corporate uppercase is untracked. Here uppercase at 40 px and below is tracked at 0.08em. Display uppercase at 48 px and above stays at 0, applying I3 (large type is optically tightened). The two invariants overlap at display size, and the resolution is recorded here rather than silently.
- **Colour I1.** `#917300` fails AA on `#f5f5f5`, so light bands use `#fff`.
- **U10 and the opaque-surface rule.** The header's solid layer is tied to leaving the hero, not to the first scrolled pixel.
- **A1, the first screen.** Passes: 94.9% on desktop and 90.5% on mobile, with competition 0. The slider controls are declared as part of the governing event, as its interface mass. On mobile the history was 78.0% → 80.4% → 89.8% → 85.4% (the controls row added) → 90.5%.
