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
| Display L (model names in the range) | 120/110 → 56/52 | Ultra, 700 | UPPER | OBSERVED: desktop 120/110 (CI §1.3 `model__title`).<br>DECISION: mobile is raised from 48/38 to 56/52, because four stacked names need more mass than one |
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

Text over photography is placed only in fields that are dark at capture: the black studio field of the hero and the dark cabin in the Ad Personam image. A gradient scrim is a sibling layer, never a child of the copy. Ratios measured on the render are in the report.

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
| DECISION (user direction, Alex, 30 Sep 2026) | **The header never hides.** It stays fixed and visible at every width, and only its ground changes: transparent gradient over the hero, then solid `#181818`. This overrides the OBSERVED corporate `.to-hide` hide-on-scroll pattern (CI §1.7).<br>Consequences:<br>• every in-page target carries `scroll-margin-top: var(--header-h)` (104 / 80 px), which Lenis `anchors` also honours<br>• the full-size Ad Personam chapter is the one exception: it lands flush (`scroll-margin-top: 0`) and clears the header with its own padding, `header-h + 16…56 px`<br>Surface timing stays at 0.3 s ease-out, as observed |
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
| DECISION | Icons are a single set: 24 px, stroke 1.5, square caps. The shapes are an arrow →, an external arrow ↗, a phone, and the burger/close.<br>The hexagon, which corporate uses for arrow buttons, is **not** used: this page has no carousel, and a hexagon with no job would be decoration |
| DECISION | Arrow hover: the arrow moves 4 px right over 0.25 s ease-out. Its focus-visible state is identical to its hover |
| DECISION | Focus: a 2 px `#1e90ff` outline with a 3 px offset, on every interactive element |

---

## 6. Images: composition and cropping

| | |
|---|---|
| OBSERVED | Imagery is dark, low-key, cinematic film stills: cars on black or studio plates, not catalogue cut-outs (CI §1.10) |
| DECISION | **One grade:** low-key, dark field. The hero (Temerario, black studio) and Ad Personam (Urus SE cabin) share it. The workshop and archive photographs are documentary, and each sits in its own chapter |
| DECISION | Hero: full-screen *scene*, not full-frame *object*. The black studio field is the text-safe zone. The car enters from the right at about 55–60% of the frame width.<br>• Desktop, ≥1200: a **diagonal**. The frame's light falls from lower-left to upper-right, so the identity mass takes the upper-left, the car the lower-right, the CTAs sit in the photograph's own black field at lower-left, and the air between the masses is bounded by both. Measured A1: 94.9% event coverage, competition 0.<br>• Desktop crop: the whole 1920×707 frame, anchored bottom-right, with the top edge feathered into the black.<br>• Mobile and portrait-tablet crop: a separate file, `hero-temerario-m`, cropped at x 760–1920 so the whole front 3/4 fits, sitting under the headline |
| DECISION | No "Pictured" caption in the hero. The car carries its own TEMERARIO plate in frame, and the caption measured 1.47:1 over the lit blue floor |
| DECISION (user direction, Alex, 30 Sep 2026) | **Ad Personam is full-size on every screen:**<br>• full-bleed image<br>• `min-height: 100vh`, with `100svh` layered on top so mobile browser chrome cannot crop it<br>• content composed inside the frame<br>Two crops are authored from the 5000 px original, both clear of the watermark:<br>• **landscape** `adp-cabin-l`, 5000×2800: the whole windscreen band is the text field. Title sits left, lead and actions right, in one band under the header; the cabin owns the lower field<br>• **portrait** `adp-cabin-p`, 2000×2733: the wheel is centred between dark bands. On phones the title is above the wheel and the lead and actions are below it; on portrait tablets the whole block sits in the lower band<br>The scrims are sibling layers that only even out what the crop leaves. Measured at the 98th-percentile background pixel, every text element is 10.9:1 or better at 1440, 1920, 1024, 768 and 390 |
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
| 2 | **The range**: four current models | `#fff` | A typographic index of four rows. Each row has a folio, the name at Display L, the corporate claim, the documented facts, and actions. DECISION: this follows corporate's "THE QUANTUM OF DRIVING" giant-claim-on-white carousel (shot 02/04), set as an index so all four read without a carousel |
| 3 | **Inventory**: in the showroom | `#181818` | Left: group labels (New / Pre-owned). Right: a two-column grid of cards on `#000`, in **dealer adaptation of the Selezione search card**. The card carries title, colour line, 16:9 photo, an Odometer row with a rule, an accent price and a View vehicle button |
| 4 | **Ad Personam** | full-bleed photograph | Full-size chapter (100svh) on every screen, and the page's one full-bleed moment after the hero. Landscape and portrait crops are authored separately (§6) |
| 5 | **Service & ownership** | `#181818` | Portrait workshop photograph with a service list set as **technical-specification rows**. These are corporate's label/value rows with 1 px `#626262` rules (shot 07), carrying departments and phone numbers instead of engine data |
| 6 | **The house**: showroom and heritage | `#fff` | Dealer lockup, the introduction, the night aerial, and a dated strip of archive prints |
| 7 | **Visit** and **footer** | `#000` | Address, departmental phones and hours as a tabular spec, directions; then the footer and the legal lines |

---

## 8. Motion

| | |
|---|---|
| OBSERVED | Buttons and links: 0.2–0.25 s ease / ease-out.<br>Fades: opacity 0.3–0.5 s ease-out.<br>Reveals: transform + opacity 0.5 s ease-out.<br>Header: 1 s linear hide (CI §1.8) |
| OBSERVED | Corporate offers an "Allow animations" toggle (CI §1.7) |
| DECISION | Duration tokens: `--dur-fast` 200 ms, `--dur-base` 300 ms, `--dur-reveal` 500 ms. Easing: `--ease-out` cubic-bezier(.2,.7,.2,1) and `--ease-in` cubic-bezier(.4,0,1,1) |
| DECISION | Reveals: blocks rise 24 px and fade in over 500 ms, once, when 15% visible. The hero headline reveals on load (lines staggered 80 ms). Content is visible without JS: the hidden state exists only under `html.js`. Nothing animates a layout property |
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
- **A1, the first screen.** On desktop A1 passes at 94.9%. On mobile it measures **78.0%**, below the 90% floor. The remainder is the brief's mandated 24 px gutters, the 48 px clearance under the 80 px header, and the fixed 1.74:1 aspect of the only suitable Temerario frame. Competition is 0. This is recorded as a known shortfall, not a pass.
