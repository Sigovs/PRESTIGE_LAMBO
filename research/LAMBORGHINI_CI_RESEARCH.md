# Lamborghini CI research: corporate site, brand identity, dealer-site rules

**For:** the lamborghinimiami.com redesign (Lamborghini Miami, part of Prestige Imports Miami)
**Researched:** 30 Sep 2026. The live site was rendered in Playwright at 1440×900 and 390×844, with a US geo-IP. The raw CSS was pulled with curl.
**How to read this:** every claim is tagged **[V]** verified (with its source), **[I]** inferred (with the reasoning), or **[?]** unknown / needs to be asked.
Screenshots are in `research/corp-site-shots/`.

---

## 0. Summary

| Topic | Finding |
|---|---|
| Corporate typeface | **Lambotype**, *not* "Lamborghini Roma". It is a custom neo-grotesk by **Character Type** (Henning Skibbe), made with the agency **Strichpunkt**. The font's own metadata reads: "© Character Type, Henning Skibbe, 2023, **exclusively for Lamborghini**". It is a variable font with two axes, `wdth` 0–100 and `wght` 300–900 **[V]** |
| Can dealers use Lambotype? | It is not sold at retail. However, a dealer-platform build called **"Lambotype for OpenRoad"** (static Light, Regular, Bold and Black, each with italics) is live on the **Lamborghini Palm Beach** site, served from the DealerSocket CDN. That means the font *does* reach dealer vendors through some channel **[V]**. Whether Lamborghini Miami or our agency may use it is **[?]**. We must get it from Lamborghini Americas together with the licence terms |
| Colours | Monochrome black/white with a neutral grey ramp. The **gold/yellow accent is `#FFC000` on dark surfaces and `#917300` on light surfaces**. The full token file is Lamborghini Design Tokens v1.5.0 (13/02/2025) **[V]** |
| Logo | The 2024 logo (announced 28 Mar 2024) is flat and two-tone, with a wider wordmark. **The bull may now stand alone without the shield on digital touchpoints.** The corporate header shows only a white bull (57×59 px), with no shield and no wordmark **[V]** |
| Dealer sites | **There is no evidence of a mandated platform.** Five US and international dealer sites run on five different stacks: DealerSocket/DealerFire, Dealer.com, Dealer eProcess, DealerMasters and a custom Next.js build. What they *do* share is a dealer lockup (the bull without shield plus "LAMBORGHINI [CITY]") and the "Authorized/Authorised Dealer" wording **[V/I]** |
| Written dealer-web rules | **None are public.** The corporate Terms of Use prohibit any use of the marks, logos *and fonts* without written authorisation **[V]**. Dealer CI and website standards are not published and have to be requested **[?]** |

---

## 1. Corporate site: design specs (lamborghini.com/en-en)

Source for everything in this section: live render of https://www.lamborghini.com/en-en and https://www.lamborghini.com/en-en/models/temerario, plus https://www.lamborghini.com/tokens.css. Values come from `getComputedStyle` and the stylesheets, captured 30 Sep 2026.

### 1.1 Stack and structure

| Item | Value |
|---|---|
| Framework | Next.js (`/_next/static/...`), components styled with Emotion (`css-xxxx` classes), Bootstrap grid underneath (`.container`, `d-lg-flex`), Drupal back end (`/node/1457`, "paragraph:*" bundles) **[V]** |
| Token file | `/tokens.css`, header comment: "Release of Lamborghini Design Tokens Version 1.5.0 – 13/02/2025" **[V]** |
| Themes | `.dark` and `.light` classes on sections switch the whole token set. The site alternates dark and light bands **[V]** |
| Main IA (burger menu) | MODELS · OWNERSHIP · DEALERSHIPS · BEYOND · COMPANY · MOTORSPORT · MUSEUM · STORE. Second level includes Design, History, Financial services, Warranty extension, Driving Programs, Lounge, Club. Utilities: Languages, **Text size**, **Allow animations** (a motion toggle) **[V]** |
| Homepage sequence | Full-bleed video hero with eyelet, giant title and CTA → "MODELS" carousel (claim-led slides: "THE QUANTUM OF DRIVING", "URUS AT ITS PEAK", "YOU CAN'T HIDE WHO YOU ARE") with the actions Explore / Start configuration / Enquire → "DEALER LOCATOR" band → "CONFIGURE YOUR [model]" tabs → legal footer (shot 02) **[V]** |
| Model page sequence (Temerario) | Hero → intro paragraph → 3 KPI figures → chapters (Powertrain, Aerodynamics, Exterior, Alleggerita, Interior) with hotspots → TECHNICAL SPECIFICATIONS → "DISCOVER MORE" CTA band **[V]** |

### 1.2 Fonts: every @font-face

| family | src | weight/style | display |
|---|---|---|---|
| `LamboType` | `/fonts/2024/lambotype-web-variable/Lambotype-Variable.woff` (woff), `…/Lambotype-Variable.woff2` (woff2) | normal / normal (variable) | swap |
| `Lambo-icons` | `/fonts/icons/Lambo-icons.ttf?hqv35s`, `.woff`, `.svg` | normal | block |

Also loaded: `Open Sans 700`, used only by the OneTrust cookie banner.
Fallback stack: `LamboType, Roboto, "Helvetica Neue", Arial` **[V]**

**Font file metadata**, read from the name table of the WOFF with fontTools **[V]**:
- Copyright: "Character Type, Henning Skibbe, 2023, exclusively for Lamborghini". Vendor ID `CHTY`. Version 1.005. Designers: Henning Skibbe, Oleksandr Parkhomovskyy, Philipp Neumeyer, Jakob Fangmeier, Sebastian Carewe. `fsType` = 8, which is "editable embedding" and is not a licence to redistribute.
- Axes: `wdth` 0 → 100 (default 100); `wght` 300 → 900 (default 300).
- Named instances: UltraCnd {Light, Regular, Bold, Black} at wdth 0 · Cnd {…} at wdth 50 · Normal {Light, Regular, Bold, Black} at wdth 100. The corporate tokens also name an Italic. 645 glyphs.
- The foundry page describes it as three widths × four weights, 24 styles, 205 languages (Latin Ext., Cyrillic, Greek), with 12° angled terminals, deep ink traps and hexagon/three-armed-star construction: https://charactertype.com/typefaces/lamborghini/ **[V]**

**How the site uses the width axis**, via `font-variation-settings` **[V]**:
- `"wdth" 0, "wght" 700` (Ultra-condensed Bold) for giant display titles and model names.
- `"wdth" 50, "wght" 700` (Condensed Bold) for nav items, buttons, spec values and banner titles.
- `"wght" 700` at normal width for eyelets and section headings.
- `"wght" 400` at normal width for body text.

### 1.3 Type scale in use

**All display and heading text is `text-transform: uppercase` and `letter-spacing: normal`**. The one tracking token is `--letter-spacing-2: 0.36px`. Body text is sentence case.

| Role (class) | Desktop 1440: size / line-height | Mobile 390: size / line-height | Axis settings | Case |
|---|---|---|---|---|
| Hero title `lam-hero-slide__title` (h1) | 120 / 110 px | 80 / 70 px | wdth 0, wght 700 | UPPER |
| Model title in "Configure your" `model__title` | 120 / 110 | 48 / 38 | wdth 0, wght 700 | UPPER |
| Carousel claim `carousel-item__model` | 120 / 110 | 48 / 38 | wdth 0, wght 700 | UPPER |
| KPI value `card-kpi__value` (e.g. "677") | 120 / 110 | n/a | wdth 0, wght 700 | – |
| Banner title `lam-banner__title` ("DEALER LOCATOR") | 80 / 90 | 34 / 44 | wdth 50 → normal at mobile, wght 700 | UPPER |
| Section/chapter title `tech-section__title`, `chapter-header__title` | 54 / 64 | n/a | wght 700 (normal width) | UPPER |
| Smart title h4 ("MODELS") | 40 / 46 | 28 / 38 | wght 700 | UPPER |
| Eyelet / kicker `lam-hero-slide__eyelet` | 27 / 37 | 18 / 28 | wght 700 | UPPER |
| KPI unit and caption `card-kpi__label/__info` | 24 / 34 | n/a | wdth 100, wght 400 | none |
| Intro/lead paragraph | 18 / 28 | n/a | wght 400 | none |
| Nav items (burger) | 18 / 28 | 18 / 28 | wdth 50, wght 700 | UPPER |
| Spec label `lam-list-item__subtitle` | 18 / 28 | n/a | wght 400 | UPPER |
| Spec value `lam-list-item__value-text` | 18 / 28 | n/a | wdth 50, wght 700 | UPPER |
| Body (`body`) | 16 / 24 | 16 / 24 | 400 | none |
| Footer legal text | 16 / 26 | 12 / 22 | 400 | none |
| Buttons | 16 / 24 | 16 / 24 | Condensed Bold look (inherits) | UPPER in markup |
| Utility (Languages, "Allow animations") | 12 / 22 | 12 / 22 | 400 | UPPER / none |
| Emissions disclosure bar | 16 / 20 | n/a | 400 | none |

**Token scale** (`tokens.css`) **[V]**:
- Font sizes: 10, 12, 16, 18, 24, 27, 28, 34, 36, 40, 48, 50, 54, 60, 70, 80, 90, 120, 136 px.
- Line heights: 20, 22, 26, 28, 34, 37, 38, 44, 46, 50, 60, 64, 70, 80, 90, 100, 110, 126 px.
- Named families: `'Lambotype Variable'`, `… Bold`, `… UltraCnd Bold`, `… UltraCnd Black`, `… Cnd Bold`, `… Regular`, `… Italic`.

### 1.4 Colour: tokens and what is actually rendered

**Brand and accent tokens** **[V]** (tokens.css)

| Token | `.dark` theme | `.light` theme |
|---|---|---|
| `--global-brand-brand-1` | `#ffffff` | `#000000` |
| `--global-brand-brand-2` | `#000000` | `#ffffff` |
| `--global-active-active-1` (accent) | **`#ffc000`** | **`#917300`** |
| `--global-active-active-2` | `#cc9a00` | `#665100` |
| `--global-active-active-3` | `#997300` | `#423500` |
| `--interactive-accent-accent-default / hover / pressed` | `#ffc000` / `#997300` / `#cc9a00` | `#917300` / `#423500` / `#665100` |
| `--typography-label-accent-1` | `#ffc000` | `#917300` |
| `--interactive-base-base-focus-border` | `#1e90ff` | `#1e90ff` |

**Grey ramp** (dark theme; the light theme runs the same values in reverse):
`#ffffff` (0) · `#f5f5f5` · `#dcdcdc` · `#c4c4c4` · `#ababab` · `#969696` · `#7d7d7d` · `#626262` · `#494949` · `#313131` · `#181818` · `#000000` (11) **[V]**

**Surfaces, text and strokes** **[V]**

| Token | dark | light |
|---|---|---|
| surface-0 / 1 / 2 / 3 | `#000000` / `#181818` / `#313131` / `#494949` | `#ffffff` / `#f5f5f5` / `#dcdcdc` / `#c4c4c4` |
| text-1 … text-5 | `#f5f5f5` `#dcdcdc` `#c4c4c4` `#ababab` `#969696` | `#181818` `#313131` `#494949` `#626262` `#7d7d7d` |
| stroke-1 … stroke-4 | `#7d7d7d` `#626262` `#494949` `#313131` | `#969696` `#ababab` `#c4c4c4` `#dcdcdc` |
| Signal: alert / warning / info / success | `#e62d37` / `#ff822d` / `#2d73d7` / `#37d200` | `#dc1e28` / `#f5a500` / `#2328ff` / `#23a046` |

**Gradients:** `--gradient-1` `linear-gradient(180deg,#18181833 0%,#181818 100%)`; `--gradient-bottom` `linear-gradient(180deg,#00000000 0%,#000000 100%)`; `--gradient-header` `linear-gradient(180deg,#f5f5f5 0%,#18181800 100%)`; and others in tokens.css **[V]**

**Opacity steps:** 0–1 in 0.1 increments **[V]**

**Colours actually rendered on the homepage**, counted across every element **[V]**:
- Text: `#202020` (402 elements, the body default), `#ffffff` (254), `#000000` (202), `#f5f5f5` (69), then `#555`, `#7d7d7d`, `#dcdcdc`, `#969696`, `#494949`.
- Backgrounds: `#ffffff`, `#000000`, `#181818`, `#917300` (accent button on light), `#ffc000` (accent button on dark), plus rgba black overlays at 0.25, 0.5 and 0.7.
- The blues and greens in the raw counts come from the OneTrust cookie widget, not the brand.

### 1.5 Buttons (Emotion classes `btn-*`)

| Variant | Fill / text | Border | Hover | Pressed |
|---|---|---|---|---|
| `btn-primary` | base-default (white on dark / black on light) with text base-default-2 | none | bg → base-hover (`#c4c4c4` dark / `#494949` light) | base-pressed |
| `btn-accent` | `#ffc000` (dark) / `#917300` (light); text `#000` on dark, `#fff` on light | none | bg → accent-hover (`#997300` / `#423500`) | accent-pressed |
| `btn-secondary` | transparent | 1px solid base-default | border → base-hover; bg → on-surface-5; text → base-hover | – |
| `btn-tertiary` | transparent, text link | **bottom border only** 1px; no side padding | same as secondary | – |
| `btn-ghost` | transparent, text only | none | text → base-hover | – |
| `btn-icon-special` | **hexagon SVG** (`.hexagon-bg`) fill/stroke, used for carousel arrows and icon buttons | – | fill changes | – |

| Size | Height | Padding | Icon gap |
|---|---|---|---|
| `btn-large` | **72 px (4.5rem)** | 24 px | 24 px |
| `btn-medium` | 56 px | 16 px | 16 px |

- **border-radius 0.** Radius tokens exist (4, 8 and 16 px) but buttons do not use them.
- Labels are uppercase, 16/24, and carry a trailing icon: an arrow, a hexagon-cube for "configure", or an envelope for "enquire".
- Below 767.98 px, buttons go full width (`min-width:100%`) with centred content.
- Transition: `all` (the durations are listed in §1.8) **[V]**

### 1.6 Grid, containers and spacing

| Item | Value |
|---|---|
| Container | Bootstrap `.container`, **max-width 1320 px** at 1440 (content x = 65 px at a 1425 px viewport) **[V]** |
| Gutter | 12 px per column side (24 px gutter) on desktop. Mobile container padding is 24 px each side (content 327 px wide at 390) **[V]** |
| Column maxima seen | 33.33 %, 41.67 %, 66.67 %, 25 % (12-column Bootstrap) **[V]** |
| Spacing scale (`--scale-spacing-*`) | 0 · 4 · 8 · 16 · 24 · 32 · 40 · 48 · 56 · 64 · 72 · 80 · 88 px; `--scale-spacing-grid` 60 px **[V]** |
| Section padding seen | 64/0/64 and 40/0/40 (desktop); 40/0/40 (mobile). KPI card padding 56/24/24/56 **[V]** |
| Borders | stroke tokens 0/1/2/4/8 px. Spec rows use a **1 px bottom rule in `#626262`**, 16 px vertical padding **[V]** |

### 1.7 Header and navigation

| Item | Value |
|---|---|
| Height | **104 px desktop / 80 px mobile**; `position: fixed; z-index: 1040` **[V]** |
| Layout | Burger icon + "MENU" label (18 px Condensed Bold, uppercase) on the left · **bull-only logo, centred, 57×59 px** (`/sites/it-en/files/DAM/lamborghini/logos/2024/03_26/logo_header_01.svg`, single white fill, viewBox 70×72) · search icon on the right. Icons are 24 px, stroke style **[V]** |
| Background | Initially `linear-gradient(#181818 → rgba(24,24,24,0))` over the hero. On scroll the `.full-bg` class fades a solid `surface-1` `::before` layer in: `opacity 0.3s ease-out` **[V]** |
| Hide/show | `.to-hide { transform: translateY(-100%) }` with `transition: transform 1s linear`, so the header hides on scroll-down **[V]** (the exact trigger logic is **[I]**) |
| Pages without a hero | Content gets `padding-top: 6.5rem` (5rem on mobile) **[V]** |
| Menu | Full-screen overlay. Level-1 items sit in three columns (416 px each), 18 px Condensed Bold, 16 px vertical padding **[V]** |

### 1.8 Motion

| Seen on | Value |
|---|---|
| Buttons, links | `all 0.2s ease-in`, `all 0.25s ease-out`, `all 0.2s ease` |
| Fades | `opacity 0.3s ease-in-out / ease-out`, `opacity 0.5s ease-out` |
| Reveals | `transform, opacity 0.5s ease-out`; `transform 0.5s ease-out` |
| Header | `transform 1s linear` (hide); `height, padding 0.3s ease-out` |
| User control | An "Allow animations" toggle in the menu, plus a "Text size" control **[V]** |

The hero is a full-bleed autoplay video. There is no evidence of a smooth-scroll library in the corporate CSS **[I]**.

### 1.9 How specs and KPIs are presented (Temerario, shots 06–07)

- **KPI trio, centred:** a value at 120 px Ultra-condensed Bold, with the unit set beside it at 24 px Regular ("677 kW", "343 km/h", "2.7 s"). A caption sits below in 24 px grey `#969696` ("Max power (combined ICE+EE)", "Max speed", "0-100 km/h"). There are no dividers and no cards. It is presented as pure type on `#181818` **[V]**
- **TECHNICAL SPECIFICATIONS:** a two-column split.
  - Left column: a 54 px uppercase title and an "ALL SPECIFICATION +" primary button that expands the full list.
  - Right column: a list of rows (`ul.tech-section__tech-data > li.lam-list-item`). Each row has an UPPERCASE label in 18 px Regular `#c4c4c4` on the left, the value right-aligned in 18 px Condensed Bold `#f5f5f5`, and a 1 px `#626262` bottom rule.
  - Rows shown to a US visitor: Displacement 3995.2 cm3 (243.8 cu in) · Max power 920 CV/677 kW · Top speed 343 km/h · 0-100 km/h 2.7 s · Combined fuel economy (gasoline only)* 16 MPG (EPA) · Combined fuel economy (electricity+gasoline)* 24 MPGe (EPA) **[V]**
- **Fixed emissions bar (US geo):** an `aside.fixed-bottom` on black at z-index 1030 with 12 px padding and 16 px text: "Combined energy consumption: Combined fuel economy (electricity+gasoline): 24 MPGe; Combined fuel economy (gasoline only): 16 MPG; Your mileage will vary." The corporate site keeps the EPA disclosure permanently on screen on model pages **[V]**
- Other disclaimers on the homepage: "Revuelto, Revuelto SV: Under approval, not available for sale; Your mileage will vary." and "The vehicle is not yet offered for sale and is therefore not subject to Directive 1999/94/EC…" **[V]**

### 1.10 Imagery and UI motifs

- Dark, cinematic, low-key imagery: motion-blur light trails and night tracks, cars isolated on black or on desert or salt-flat plates. Models are presented as film stills rather than catalogue cut-outs, apart from configurator thumbnails **[V]** (shots 01, 05, 06)
- The **hexagon** is the recurring UI motif: carousel arrows, the "configure" icon and icon buttons. Dealer sites reuse it too (Palm Beach and Beverly Hills quick-link icons) **[V]**
- **Model logotypes** (e.g. the REVUELTO script with an Italian-tricolore underline) appear as image assets above the claim in the model carousel (shot 03) **[V]**. In running UI, model names are set in Lambotype uppercase.

---

## 2. The 2024 brand identity refresh

| Fact | Source |
|---|---|
| Announced **28 March 2024**. It was the first logo update in more than 20 years **[V]** | https://www.thedrive.com/news/lamborghini-is-the-latest-to-fall-victim-to-the-flat-logo-trend ; https://www.businesslive.co.za/bd/life/motoring/2024-03-28-watch-lamborghinis-iconic-logo-gets-a-revamp/ |
| The asset folder on lamborghini.com is dated `logos/2024/03_26/` **[V]** | live HTML |
| Rationale: to express the "brave", "unexpected" and "authentic" values of the mission **"Driving Humans Beyond"**, as part of the **Direzione Cor Tauri** strategy **[V]** | https://mobilityoutlook.com/news/automobili-lamborghini-unveils-new-corporate-identity-logo ; https://marketech-apac.com/lamborghinis-revamped-corporate-identity-to-better-reflect-brave-and-unexpected-values-of-company/ |
| Logo: flat and two-tone instead of 3D gold, with a **broader Lamborghini wordmark** **[V]** | same as above; https://news.dupontregistry.com/lamborghini/lamborghini-refreshes-branding-new-logo |
| Colours: **black and white confirmed as primary**; **yellow and a newly introduced gold used as accents** **[V]**. The live tokens match this: `#FFC000` yellow-gold on dark, `#917300` gold on light | mobilityoutlook (above); tokens.css |
| **The bull appears without the shield for the first time, on digital touchpoints (website, social)** **[V]** | thedrive (above); mobilityoutlook (above) |
| New official typeface **Lambotype** by Character Type, in the redesign led by **Strichpunkt** (Design Director Nicola Wetzel). A new icon suite was made with Lamborghini Centro Stile **[V]** | https://charactertype.com/typefaces/lamborghini/ ; https://generatordesign.com/2024/04/04/the-new-look-of-corporate-lamborghini/ |
| A **brand portal** with all the CI/CD elements was set up for brand communications. Whether dealers can reach it is **[?]** | https://www.exchange4media.com/marketing-news/lamborghini-revs-up-new-identity-internet-underwhelmed-133468.html (search-summary level only; not verified on a primary page) |
| The official press release URL (lamborghini.com/en-en/news/automobili-lamborghini-launches-its-new-corporate-look) **now redirects to the homepage**. The news archive appears to have been removed | curl, 30 Sep 2026 |

**About "Lamborghini Roma":** no evidence found. The corporate font is Lambotype. "Roma" typefaces from Canada Type and CAST exist but have no connection to Lamborghini **[V: negative search]**.

---

## 3. Dealer / retailer rules

### 3.1 What is verified

| Item | Detail | Source |
|---|---|---|
| Terminology | lamborghini.com uses **"Dealerships"** (nav), **"Authorized Lamborghini Dealers"** and "Authorized Dealerships and Service Centers". Dubai uses "Authorised Dealer for Lamborghini Dubai". Corporate does not use "retailer" | https://www.lamborghini.com/en-en/dealerships/lamborghini-miami ; https://www.lamborghini.com/en-en/models/pre-owned ; lamborghini-dubai.com |
| Official dealer micro-page | lamborghini.com hosts **its own page for Lamborghini Miami** (`/en-en/dealerships/lamborghini-miami`) with tabs NEW CAR / PRE-OWNED / ACCESSORIES / SERVICE, a contact iframe form (`/resource/form/dealer_2026/iframe/50716`) and schema.org `AutoDealer`. Recorded facts: dealer ID **50716**; legal entity **Prestige Motorcar Imports, Inc.**, 14780 Biscayne Blvd, North Miami Beach FL 33181; phone +1 (833) 290-5147; flags **certCollisionCenter: true, certPaintShop: true**. That page carries **no link to lamborghinimiami.com** | curl of that page (JSON-LD and page data) |
| Official CPO inventory | `preowned.lamborghini.com/dealer/50716/lamborghini_miami/` | same page |
| Trademarks | Terms of Use: "'Automobili Lamborghini' is a word mark and figurative mark owned by Lamborghini; the logos used on this site are also registered… The use and reproduction in any form and manner of the above-mentioned brands and logos is strictly prohibited." The site's IP clause names **"fonts, graphic design… icons"** as protected. Reuse needs "express written authorization" | https://www.lamborghini.com/en-en/privacy-legal |
| Corporate footer legal line | "Copyright © 2026 Automobili Lamborghini S.p.A. a company with sole shareholder subject to the management and coordination of AUDI AG. All rights reserved." | live footer |
| Geo emissions note | "The consumption and emissions values in the website refer to your geographical IP… contact your dealer to get valid consumption and emissions information in your area." This effectively passes that responsibility to dealers | live footer |
| Showroom CI history | A new dealer CI started in 2016 (the Bristol showroom was first): illuminated shield on a black façade, black totem with the bull, polygons, raw surfaces | https://media.lamborghini.com/english/latest-news/lamborghini-opens-in-bristol-first-dealership--in-new-corporate-design/s/910a0bca-6efb-4c0d-b057-a843d02c9e1b ; https://lambocars.com/lamborghini-dealerships-new-corporate-identity-north-america/ |
| **Lamborghini Miami = the world's first dealer in the newer showroom design** | Reopened 28 Jan 2022, with Stephan Winkelmann and dealer principal Brett David. 38,000 sq ft; "The New Bull Pen" service centre (billed as the largest Lamborghini service centre in the Western Hemisphere); Ad Personam studio | search summaries of https://www.lamborghini.com/en-en/news/lamborghini-miami-a-new-design-for-the-showroom (now redirects) and https://www.lambocars.com/web-stories/lamborghini-miami-s-showroom-overhaul-reveals-what-the-brand-s-retail-future-loo/ . Direct fetch failed, so treat the details as **[V-secondary]** |

### 3.2 US and Florida legal requirements (these apply whatever Lamborghini's CI says)

| Requirement | Detail | Source |
|---|---|---|
| FL advertised price | The advertised price must "include all fees or charges that the customer must pay, including freight or destination charge, dealer preparation charge…". Taxes, tag, registration and title may be excluded (§501.976(16)) | https://www.flsenate.gov/Laws/Statutes/2025/501.976 |
| FL predelivery fee | Required disclosure text: "This charge represents costs and profit to the dealer for items such as inspecting, cleaning, and adjusting vehicles, and preparing documents related to the sale." (§501.976(18)) | same |
| EPA fuel economy | If any fuel-economy figure is shown, identify it as an **EPA estimate**, state the driving mode (city/hwy/combined), and match it to the claim (16 CFR 259.4). Corporate follows this with "(EPA)" labels and "Your mileage will vary" | https://www.law.cornell.edu/cfr/text/16/259.4 ; live Temerario page |
| Privacy | CCPA-style consent patterns are standard on peer sites (e.g. the ComplyAuto banner on Newport Beach). Florida has its own rules. Confirm the approach with the client's counsel **[I]** | lambonb.com render |

### 3.3 Not public (unknown, must be requested) **[?]**

- Whether Lamborghini Americas runs a **dealer digital / website certification programme** or an approved-vendor list (as Audi, Porsche and Mazda do). Nothing public was found.
- **Dealer logo lockup artwork and rules** (bull + "LAMBORGHINI MIAMI": sizes, clear space, minimum size, colourways, and co-branding with Prestige Imports).
- **Lambotype licence** for dealer web use. "Lambotype for OpenRoad" suggests Lamborghini distributes a dealer package. We need our own files and licence terms.
- Access to the **brand portal**: image library, model logotypes, approved photography, video, icons.
- **Co-op / advertising guidelines**, pricing rules (MSRP vs "call for price"), and rules on "offers" pages.
- Mandatory disclaimers text: EPA figures, "under approval" models, Selezione T&Cs.
- Rules for **model names in page titles and SEO**, and **domain / naming policy** (Lamborghini has taken action over domains; see the Carscoops report on a 2023 suit against a Nashville dealer over its domain: https://www.carscoops.com/2023/10/lamborghini-sues-nashville-luxury-car-dealer-over-website-domain-name-again/amp/).
- Whether Lamborghini **must approve** the site before launch.

---

## 4. Benchmarks: other official dealer sites

Rendered 30 Sep 2026 at 1440. Screenshots are `corp-site-shots/bench-*.png`.

| Dealer | Platform | Type | Palette | Structure | Premium? |
|---|---|---|---|---|---|
| **Lamborghini Miami** (current) | DealerSocket / DealerFire (`cdn-ds.com`, "builder2 / e6" templates) **[V]** | Roboto + Abel (Google Fonts) | `#3c3939`, `#cecece`, `#ffcc00` | Generic dealer template | Low. It does not use the corporate type |
| **Lamborghini Palm Beach** | DealerSocket / DealerFire (same CDN) **[V]** | **"Lambotype for OpenRoad"**, headings 32–40 px Bold uppercase **[V]** | `#ffffff`, `#000`, `#181818` | Dark bar header; bull + "LAMBORGHINI PALM BEACH" lockup; hero; hexagon quick links (NEW CAR / PRE-OWNED / SERVICE / ACCESSORIES); featured inventory | Medium. Right font, template layout |
| **Lamborghini Dallas** | Dealer.com (DDC fonts, `ddc-icons`) **[V]** | "DDC Heading Font Face" | black / `#202020` | Phone utility bar; lockup; inventory search overlay on hero; "Secure Credit Application" | Low. Reads like a search portal |
| **Lamborghini Newport Beach** (lambonb.com) | Dealer eProcess (`cdn.dealereprocess.org`) + ComplyAuto **[V]** | Roboto | yellow CTA on black | Inventory search, "Current offers", model tiles (still lists Tecnica / STO) | Low. Outdated line-up, loud yellow |
| **Lamborghini Beverly Hills** | DealerMasters (Gatsby 5.16, autohub.io) **[V]** | Inter + AvenirNext | `#102c42`, greys | Lockup; slider hero ("ORDER THE TEMERARIO HERE AT BEVERLY HILLS"); hexagon CTA; editorial "NEW CAR" block with a diagonal image crop | Medium. More editorial, generic sans |
| **Lamborghini Dubai** (Ultimate Motors) | Custom Next.js + Seez platform **[V]** | Roboto (the corporate fallback); Almarai for Arabic | `#202020`, `#181818`, `#f5f5f5`, which are corporate greys | Mirrors the corporate IA and claims ("YOU CAN'T HIDE WHO YOU ARE", "DARE TO LIVE MORE"); full-bleed video hero "AUTHORISED DEALER FOR LAMBORGHINI DUBAI"; full model / limited-series / concept menu; UNICA app link | **Highest.** Closest to corporate: video, restraint, corporate greys and claims, bilingual |

**What they share:**
- The dealer lockup: bull without shield, in white, plus "LAMBORGHINI [CITY]" in a wide sans. Dallas, Palm Beach, Beverly Hills and Dubai all use it. This is consistent with Lamborghini supplying the lockup **[I]**.
- "[City]" naming.
- Black header bar.
- Hexagon icons.

**What differs:** the platform, the typeface and the layout. So **no mandated template is evident** **[I]**.

**Why Dubai feels more premium:**
- It uses corporate tokens and claims.
- It has fewer and larger elements.
- It opens with video rather than a search widget.
- It has no inventory search and no finance widgets above the fold.

The HR Owen Lamborghini page (London) runs on generic WordPress/Elementor with Open Sans under the group brand (https://www.hrowen.co.uk/lamborghini/). **[V]**

---

## 5. Current line-up and official naming (lamborghini.com/en-en/models, 30 Sep 2026)

| Group | Names as styled on corporate nav and page copy | Source |
|---|---|---|
| Revuelto family | **Revuelto**, **Revuelto SV** (world debut at The Quail during Monterey Car Week, Aug 2026; 1,065 CV; limited to 1,963 units). Corporate note: "Revuelto, Revuelto SV: Under approval, not available for sale" for this geo | lamborghini.com/en-en/models/revuelto-models ; https://media.lamborghini.com/English/latest-news/automobili-lamborghini-holds-world-debut-of-revuelto-sv-at-the-quail--a-motorsports-gathering/s/e7945c16-94f5-4975-a2ac-a816924b10f0 ; https://english.news18a.com/m/news/english_265173.html |
| Urus | **Urus SE**, **Urus SE Performante** | lamborghini.com/en-en/models/urus |
| Temerario | **Temerario** (twin-turbo V8 HPEV, 920 CV). **Alleggerita** package | lamborghini.com/en-en/models/temerario |
| Few-off | **Fenomeno**, **Fenomeno Roadster**, **Countach LPI 800-4**, **Sián Roadster**, **Sián FKP 37** | models page links |
| Concept | **Terzo Millennio**, **Asterion**, **Estoque** | models page links |
| Claims per model | Revuelto: "THE QUANTUM OF DRIVING". Urus: "URUS AT ITS PEAK" (earlier "DARE TO LIVE MORE"). Temerario: "YOU CAN'T HIDE WHO YOU ARE". Revuelto (earlier): "FROM NOW ON" | live site; Dubai |
| CPO | **Selezione Lamborghini** — "Selezione Lamborghini Certified Pre-Owned program", "only available at the Authorized Dealerships and Service Centers". Warranty 12–24 months; 24/7 roadside assistance | https://www.lamborghini.com/en-en/models/pre-owned |
| Personalisation | **Ad Personam** (programme); **Ad Personam Studio** (Sant'Agata) | https://www.lamborghini.com/en-en/customization |
| Motorsport | **Lamborghini Squadra Corse** (the page is titled "Squadra Corse – Motorsport") | https://www.lamborghini.com/en-en/motorsport |
| Lounge | **Lamborghini Lounge**: Lounge NYC (533 W 26th St), Lounge Tokyo (Roppongi), plus temporary lounges. **Not a dealer format** | https://www.lamborghini.com/en-en/lamborghini-lounge |
| Other owner programmes in nav | Financial services, Warranty extension, Driving Programs, Club, Museum, Store; the **UNICA** app (on the Dubai site) | live nav |

**Casing:**
- In display UI, corporate sets every model name in Lambotype uppercase ("REVUELTO SV").
- In running text, model names are in title case ("Temerario", "Urus SE Performante").
- Accents are kept: "Sián", "Huracán".
- Model logotypes (script badges) are separate image assets from the brand portal **[V]/[I]**.

---

## 6. Implications for the redesign

### Hard constraints (treat as non-negotiable until Lamborghini says otherwise)

1. **Do not redraw, recolour or modify the bull or the wordmark.** Use only supplied artwork: the dealer lockup "LAMBORGHINI MIAMI" and the standalone bull. The bull-without-shield is the digital convention. The marks and logos are registered, and any use is prohibited without authorisation.
2. **Do not self-host Lambotype from lamborghini.com or copy another dealer's CDN build.** Fonts are explicitly protected IP and the file says "exclusively for Lamborghini". Get the dealer font package and licence first. Fallback: Roboto, which is corporate's own fallback stack.
3. **Palette: stay monochrome** (black, `#181818`, the corporate grey ramp, white) with **a single gold/yellow accent**: `#FFC000` on dark, `#917300` on light. Do not introduce other brand hues. The current site's `#ffcc00` and `#1c75bc` should go.
4. **US disclosures:**
   - EPA-labelled MPG/MPGe wherever figures appear (corporate uses a fixed bar on model pages).
   - "Under approval / not available for sale" notes for unhomologated models.
   - Florida all-inclusive advertised price and predelivery-fee wording on inventory and offers.
5. **Use official names exactly:** Selezione Lamborghini (CPO), Ad Personam, Squadra Corse, Revuelto SV, Urus SE Performante. Use "Authorized Lamborghini Dealer" language.
6. **Do not call the showroom a "Lamborghini Lounge".** That is a corporate venue format.

### Freedoms (probably ours, because peers vary widely)

- Platform and stack. Peers use five different vendors, so no mandated template is evident. Confirm this.
- Layout, IA, editorial storytelling, local content: Miami, the 2022 first-in-world showroom, the Bull Pen service centre, the Ad Personam studio, certified collision and paint.
- Photography of our own showroom and inventory.
- Motion: corporate itself uses restrained fades and translates of 0.2–0.5 s, a hide-on-scroll header and an "Allow animations" toggle.
- The level of premium. Dubai shows that a dealer can sit close to corporate.

### Aligning with corporate (recommended, not required)

- A 72 px square-cornered button family (primary, accent, secondary, tertiary-underline).
- Uppercase display type with the condensed/normal width contrast.
- The 120/110 KPI treatment for specs, and label/value spec rows with 1 px rules.
- The 1320 px container on a 12-column / 24 px gutter grid.
- A 104/80 px fixed header with the bull centred.
- The hexagon as the icon motif.

---

## 7. Questions for the client and Lamborghini Americas

1. Is there a **Lamborghini Americas dealer digital standard**, a certification or an approved-vendor list for dealer websites? Does Lamborghini need to **approve** the site or its design before launch?
2. Can we have the **dealer CI / brand portal access**: the Lamborghini Miami lockup (SVG, colourways, clear space, minimum size), the standalone bull, model logotypes, photography, video and the icon set?
3. **Lambotype licence:** is there a dealer web-font package (like "Lambotype for OpenRoad")? What are its terms: domains, self-hosting, which widths (is the variable font with UltraCnd/Cnd included)?
4. **Co-branding:** how may Prestige Imports / Prestige Motorcar Imports, Inc. appear on a Lamborghini-branded site (footer only? a separate lockup)? Is the domain lamborghinimiami.com held under a Lamborghini agreement?
5. **Pricing and offers policy:** can we show MSRP or selling prices for new allocations? Are there rules for "offers", finance and lease content (Lamborghini Financial Services)?
6. The **required disclaimer set** (EPA, homologation, Selezione T&Cs, trademark notice) and who keeps it current.
7. **Inventory and CPO feeds:** must Selezione listings come from preowned.lamborghini.com (dealer 50716)? Must the "configure" and "enquire" actions go to the corporate configurator and the dealer_2026 form?
8. Should lamborghini.com's own Miami dealer page link to the new site? Who asks for that?
9. Which **model claims and campaign lines** ("The Quantum of Driving", "You can't hide who you are") may dealers reuse, and for how long?
10. Photography and usage rights for the 2022 showroom, and for any corporate press images we reuse.

---

## Sources (primary first)

- Live corporate site, CSS and tokens: https://www.lamborghini.com/en-en · https://www.lamborghini.com/tokens.css · https://www.lamborghini.com/en-en/models/temerario · https://www.lamborghini.com/en-en/models
- Font file: https://www.lamborghini.com/fonts/2024/lambotype-web-variable/Lambotype-Variable.woff (name table read locally)
- Character Type, Lamborghini typeface: https://charactertype.com/typefaces/lamborghini/
- Terms of Use and trademarks: https://www.lamborghini.com/en-en/privacy-legal
- Miami dealer page: https://www.lamborghini.com/en-en/dealerships/lamborghini-miami
- Selezione: https://www.lamborghini.com/en-en/models/pre-owned · Ad Personam: https://www.lamborghini.com/en-en/customization · Lounge: https://www.lamborghini.com/en-en/lamborghini-lounge · Squadra Corse: https://www.lamborghini.com/en-en/motorsport
- 2024 identity: https://www.thedrive.com/news/lamborghini-is-the-latest-to-fall-victim-to-the-flat-logo-trend · https://mobilityoutlook.com/news/automobili-lamborghini-unveils-new-corporate-identity-logo · https://generatordesign.com/2024/04/04/the-new-look-of-corporate-lamborghini/ · https://www.exchange4media.com/marketing-news/lamborghini-revs-up-new-identity-internet-underwhelmed-133468.html
- Dealer CI: https://media.lamborghini.com/english/latest-news/lamborghini-opens-in-bristol-first-dealership--in-new-corporate-design/s/910a0bca-6efb-4c0d-b057-a843d02c9e1b · https://lambocars.com/lamborghini-dealerships-new-corporate-identity-north-america/ · https://www.lambocars.com/web-stories/lamborghini-miami-s-showroom-overhaul-reveals-what-the-brand-s-retail-future-loo/
- Revuelto SV: https://media.lamborghini.com/English/latest-news/automobili-lamborghini-holds-world-debut-of-revuelto-sv-at-the-quail--a-motorsports-gathering/s/e7945c16-94f5-4975-a2ac-a816924b10f0
- Florida §501.976: https://www.flsenate.gov/Laws/Statutes/2025/501.976 · FTC 16 CFR 259.4: https://www.law.cornell.edu/cfr/text/16/259.4
- Benchmarks: lamborghinimiami.com · lamborghinipalmbeach.com (font CSS: https://cdn-ds.com/builder2/fonts/Lambotype%20for%20OpenRoad/styles.css) · lamborghinidallas.com · lambonb.com · lamborghinibeverlyhills.com · lamborghini-dubai.com/en · hrowen.co.uk/lamborghini/
