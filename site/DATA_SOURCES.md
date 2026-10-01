# Data sources and content ledger: homepage v1

Every fact, figure and promise shown in `index.html` is listed below with its source. This file is the human-readable content ledger (design-dna content-provenance CP1–CP7). The same claims are in machine form in `.gates/content-ledger.json`.

## Status key

- **verified**: taken from a primary source.
- **dated**: true only at the capture date; the date is printed next to it on the page.
- **dealer-stated**: the dealer's own published statement, with no independent confirmation.
- **confirm**: in use, but the client has to confirm it before launch.

## Inventory (live capture, 30 Sep 2026, 17:47–18:05 CDT)

**Method.** The full Lamborghini inventory was captured from lamborghinimiami.com. That covers the SRP plus its XHR pagination, all three pages (52 listings, deduplicated to 26 VINs), the data-layer `VehicleObject`s and every VDP. Everything is in `research/inventory-capture-live/` (`DATA.md`, `vehicles.json`, `raw/`, `photos/`). The earlier capture is in `research/inventory-capture-2026-09-30/`.

**Photos.** Each card uses the car's own photo `-1`: a clean front three-quarter from the dealer's VDP gallery, 1024×768 at most, without the lockup band. Every card was checked by eye: the photo shows the listed model and colour. The cards are cropped to 16:9, clear of the small shield in the bottom-right corner. The two Revuelto and the Huracán cards keep their earlier verified photos. The cards are at most 641 px wide, so the 1024 px source is sharp at 1×, and slightly soft at 2× on high-density screens.

**Certification.** No car is marked certified on the source: `certificationProgram` is empty and `isOEMCertified`/`isDealerCertified` are 0. Nothing on the page is labelled Selezione or CPO.

| Card | VIN | Stock | Colour (as listed) | Odometer | Price (as displayed) | VDP |
|---|---|---|---|---|---|---|
| 2026 Urus SE, New | ZPBUD6ZLXTLA46954 | 10918 | Nero Noctis Metallic | 24 mi | Call For Price, shown as "Price on request" | https://www.lamborghinimiami.com/vehicle-details/new-2026-lamborghini-urus-se-north-miami-beach-fl-id-66267994 |
| 2026 Temerario, New | ZHWUC1ZC1TLA02400 | 10914 | Verde Mercurius Metallic | 37 mi | Call For Price, shown as "Price on request" | https://www.lamborghinimiami.com/vehicle-details/new-2026-lamborghini-temerario---north-miami-beach-fl-id-66311290 |
| 2024 Revuelto, Pre-owned | ZHWUC1ZM0RLA00252 | CJ2602 | Grigio Acheso Matt | 1,411 mi | $741,697 | https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-65607471 |
| 2024 Revuelto, Pre-owned | ZHWUC1ZM3RLA00116 | 86180 | Giallo Metallic (listed; the car's paint plate in its photo 5 reads "Giallo Countach"; the page prints the listing) | 187 mi | $651,697 | https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-65586655 |
| 2024 Urus S, Pre-owned | ZPBUB3ZL3RLA35890 | CJ2630 | Oro Elios Metallic | 537 mi | $286,697 | https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-s-north-miami-beach-fl-id-66092572 |
| 2023 Urus Performante, Pre-owned | ZPBUC3ZL7PLA25115 | CD2536 | Rosso Mars Metallic | 8,794 mi | $291,697 | https://www.lamborghinimiami.com/vehicle-details/used-2023-lamborghini-urus-performante-north-miami-beach-fl-id-64609499 |
| 2020 Urus, Pre-owned | ZPBUA1ZL6LLA06169 | 85991Z | Blu Astraeus Metallic | 4,872 mi | $210,697 | https://www.lamborghinimiami.com/vehicle-details/used-2020-lamborghini-urus---north-miami-beach-fl-id-65769445 |
| 2015 Huracán LP610-4, Pre-owned | ZHWUC1ZF6FLA02875 | 10881A | Nero Nemesis Matt | 18,536 mi | $246,697 | https://www.lamborghinimiami.com/vehicle-details/used-2015-lamborghini-huracan-lp610-4-north-miami-beach-fl-id-66157191 |

**Capture time:** every row is from the same capture, 30 Sep 2026 17:47–18:05 CDT.

**Order.** Pre-owned is ordered by newest year, then price (descending); the two Revueltos come first. At 1024 px and wider this gives two full rows of three. Below 1024 the cards run as a horizontal scroll-snap rail.

### Listing endpoints

- All Lamborghini: https://www.lamborghinimiami.com/lamborghini-miami-fl. The page reports "52 Results", which is about 26 VINs. It also covers three more 2024–25 Revuelto VINs (…01390, …01922, …03103) and a 2015 Huracán, none of which is shown here.
- New: https://www.lamborghinimiami.com/new-vehicles-miami-fl. The only Lamborghinis in it are the Urus SE and the Temerario above; the rest of new stock is Lotus, which is excluded on this page.

### Left out, and why

- **2018 Huracán Performante Spyder, ZHWUS4ZF6JLA10746, removed in the 30 Sep critic pass.** It is listed as Nero Noctis, but its photo shows a mid-grey car.
- **2022 Urus, ZPBUA1ZL8NLA17774, removed in the 30 Sep critic pass.** It is listed as Nero Noctis Matt, but its photo reads as gloss.
- Both follow the same rule as the 2021 Urus: when the listing and its photo disagree, the car is not shown. The page no longer claims that photographs show the listed vehicle.
- The 2015 Huracán LP610-4 was added as the third pre-owned card on Alex's decision. Its listing and its photo agree.

- **2021 Urus, ZPBUA1ZL7MLA15500.** It is listed as "Grigio Keres Matt", but its photo shows a dark green car. The listing contradicts itself, so it is not shown.
- **Three Revuelto VINs.** Their listings have no photos. Showing the two photographed Revueltos is enough; the rest are behind "View all inventory".

### Representative image (retired 30 Sep 2026)

- The 2026 Temerario (stock 10914) now has its own dealer photos (41 in the live capture), and its card uses photo `-1`. The official lamborghini.com green Temerario that stood in for it, and its "Representative image" caption, are gone from the card.

### Price notes

- **Fee statement (source).** The captured listing pages (`srp.html`, `new.html`) print: "Price includes dealer fee of $1447.50 and $299 electronic filing fee. Tax, tag, title and registrations fees are not included and are calculated at time of purchase."
- **Arithmetic check** of the data-layer `sellingPrice` against the printed price:
  - 86180: $649,950 + $1,447.50 + $299 = $651,696.50, printed as **$651,697**
  - CJ2602: $739,950 + $1,747.50 = **$741,697**
  - CJ2630: $284,950 + $1,746.50 = $286,696.50, printed as **$286,697**
  - CD2536: $289,950 + $1,746.50 = **$291,697** (rounded the same way)
  - 85991Z: $208,950 + $1,746.50 = **$210,697** (rounded the same way)
- The page now prints that fee statement next to the prices in `.inventory__note`, replacing the vaguer "applicable fees" line.
- The new Urus SE and Temerario carry a data-layer `sellingPrice` (313,631 and 470,849), but the source shows no public price for them. The page keeps "Price on request" and does not publish those figures.

- Every listed price ends in ",697". That is the source's convention and is reproduced unchanged.
- **Confirm:** Florida §501.976(18) requires specific wording to disclose a predelivery (dealer) fee. The source calls it a "dealer fee"; the client should confirm the statutory wording.

## Model range: tile spec rows (captured from lamborghini.com, 30 Sep 2026)

Every tile shows the same three rows, labelled as the corporate KPI labels them: "Max power (combined ICE+EE)", "Top speed" and "0–100 km/h".

| Model | Max power | Top speed | 0–100 km/h | Source |
|---|---|---|---|---|
| Temerario | 920 CV (677 kW) | 343 km/h | 2.7 s | https://www.lamborghini.com/en-en/models/temerario |
| Revuelto | 1,015 CV (747 kW) | >350 km/h | 2.5 s | https://www.lamborghini.com/en-en/models/revuelto-models/revuelto |
| Urus SE | 800 CV (588 kW; the spec list reads "Max power @ rpm (ICE+EE) 800 CV @ 6000 rpm") | 312 km/h | 3.4 s (published as "3,4 s") | https://www.lamborghini.com/en-en/models/urus/urus-se |
| Urus SE Performante | 812 CV (597 kW) | 312 km/h | 3.3 s (published as "3,3 s") | https://www.lamborghini.com/en-en/models/urus/urus-se-performante |

- The Temerario and Urus SE pages also publish EPA MPG / MPGe figures. The tiles show none, so the EPA note is not needed; if MPG is ever added, it must carry "(EPA)" and "Your mileage will vary".
- **On-page date line removed at Alex's direction.** The line under the range grid ("Figures are manufacturer data published by Automobili Lamborghini, as captured on 30 Sep 2026.") is gone, and the capture date is recorded here instead. The Revuelto SV note is now in the footer legal lines only.

## Model range: manufacturer claims

Source: `research/LAMBORGHINI_CI_RESEARCH.md`, captured from lamborghini.com on 30 Sep 2026.

| Claim on page | Status | Source |
|---|---|---|
| Temerario: 920 CV max power (combined ICE+EE), 343 km/h top speed, 0–100 km/h 2.7 s | verified, dated | CI §1.9 (KPI trio and spec rows, lamborghini.com/en-en/models/temerario) |
| "You can't hide who you are" (Temerario) | verified | CI §5 (claims per model) |
| "The quantum of driving" (Revuelto) | verified | CI §5, shot 01 |
| Revuelto SV: 1,065 CV, limited to 1,963 units | verified | CI §5 (media.lamborghini.com press release) |
| "Revuelto SV: Under approval, not available for sale" | verified | CI §1.9, shot 04 |
| "Dare to live more" (Urus SE, hero slide 4 and Models tile) | verified as a corporate Urus claim (the earlier one), and used on the current dealer Urus SE page; **confirm** reuse with Lamborghini Americas | CI §5; CURRENT_SITE_CONTENT §3.2 |
| "Urus at its peak" (Urus SE Performante) | verified as a corporate Urus claim; **confirm** that it may be reused against the SE Performante | CI §5 |
| Urus SE: 800 CV | **now verified** on lamborghini.com/en-en/models/urus/urus-se (see the tile table). Previously dealer-stated. It comes from the current Urus SE page, which reproduces AL press copy ("first PHEV… 800 CV"). **Confirm** against lamborghini.com | `research/CURRENT_SITE_CONTENT.md` §3.2 |
| Current range = Revuelto, Temerario, Urus SE, Urus SE Performante | verified | CI §5, shot 02 ("Configure your" tabs) |

- **Confirm:** on 30 Sep 2026 the corporate US page read "Revuelto, Revuelto SV: Under approval, not available for sale" (shot 04). That covers both models. Lamborghini Miami lists pre-owned 2024–25 Revuelto units, so this page applies the note to the Revuelto SV only, as the brief instructs. Lamborghini Americas should confirm the correct US wording.
- **Not shown:** no MPG or MPGe figures appear, so no EPA "Your mileage will vary" line is needed. If MPG is added later, it must be labelled "(EPA)" and carry that line (16 CFR 259.4; CI §3.2).

## Dealer facts

| Claim on page | Status | Source |
|---|---|---|
| Address: 14780 Biscayne Boulevard, North Miami Beach, FL 33181 | verified | JSON-LD on lamborghinimiami.com; lamborghini.com dealer page (CI §3.1) |
| Sales (833) 290-5147 · Service (833) 290-5148 | verified | JSON-LD, 30 Sep 2026 |
| Parts (833) 290-5149 | dealer-stated | Header contact panel markup (CURRENT_SITE_CONTENT §4) |
| Sales hours Mon–Fri 9–7, Sat 10–6 · Service hours Mon–Fri 8–5:30 | verified | JSON-LD `openingHours` |
| "Sun closed" (sales) | dealer-stated | "Sunday Closed" in the header markup (CURRENT_SITE_CONTENT §4) |
| "Authorized Lamborghini Dealer" | verified | lamborghini.com/en-en/dealerships/lamborghini-miami (CI §3.1) |
| Lamborghini-certified collision center and paint shop | verified | lamborghini.com dealer page flags `certCollisionCenter: true`, `certPaintShop: true` (CI §3.1) |
| Roadside assistance 1-888-464-6040, 24 hours | **confirm** | Seen only in an image banner on the current service page (CURRENT_SITE_CONTENT §3.4). It may be the Lamborghini national number or a dealer line |
| Selezione Lamborghini: certified pre-owned programme, offered through authorized dealers | verified | lamborghini.com/en-en/models/pre-owned (CI §5). The page links to the programme only and makes **no** claim that particular vehicles are Selezione-certified |
| Genuine Lamborghini parts | dealer-stated | Service page: "only use genuine OEM factory-approved parts" |
| Legal entity: Prestige Motorcar Imports, Inc. | verified | lamborghini.com dealer page JSON-LD (CI §3.1) |
| "A division of Prestige Imports" | dealer-stated | Footer of the current site |
| Irv David founded Prestige Imports in Miami in 1977; it began at a gas station he owned | dealer-stated | `/our-story`; `/careers` ("since 1977"); the Prestige logo "EST 1977" |
| 1980 West Dixie Highway store · 1983 land on Biscayne · 1986 showroom opening | dealer-stated | `/our-story` photo captions |
| Brett David has led the business since 2007 | dealer-stated | `/our-story` |
| Ride2Revive Foundation created in 2011 by Brett and Brooke David | dealer-stated | `/our-story` |
| Lamborghini Miami showroom completed in 2020 | dealer-stated, **confirm** | `/our-story` caption says 2020. Secondary sources give the reopening as 28 Jan 2022 (CI §3.1). Confirm which date the client wants |

## Deliberately excluded (unsupported or stale)

- "Largest Lamborghini service department in the country": unverified superlative (CP6).
- "South Florida's only Factory-Certified Collision Center": unverified superlative. Replaced by the verified "Lamborghini-certified".
- "Over 40 years" and "over 45 years": they contradict each other. The page uses the year 1977 instead of a count.
- "92 reviews / 5 stars": an outdated count.
- The "Ad Personam Studio" on site: unverified. The page describes Lamborghini's programme and the conversation with the sales team, and makes no claim about a studio.
- "World's first dealer in the newer showroom design": a secondary source only.
- Exotics & Espresso (monthly meet): there is no evidence it is still running.
- Tecnomar, and every other brand (Lotus, Pagani and so on): out of scope for this page.
- Staff names: no titles are published anywhere.

## Imagery

**Models band and phone hero:** these use official lamborghini.com images. `research/press-images/MANIFEST.md` lists each file with its source URL, alt text, retrieval date and the by-eye model check. The media centre (media.lamborghini.com) redirects to the homepage and cannot be reached.

| File(s) in `assets/img/` | Source original | Treatment |
|---|---|---|
| `hero-temerario-*` | `hero/hero_temerario-blue-front-3q-dark_1920x707.jpg` (official AL; no watermark) | Desktop uses the full frame. Mobile is cropped to x 760–1920 |
| `adp-cabin-l-*`, `adp-cabin-p-*` | `models/urus-se/urus-se_interior-dashboard-orange_5000x3333.jpg` (official AL; shield watermark) | Two authored crops, both clear of the watermark: landscape 5000×2800 and portrait 2000×2733 |
| `service-workshop-*` | `service/service_workshop-white-bays-technician_1697x2121.jpg` (dealer-shot) | Cropped to remove the watermark |
| `showroom-aerial-night-*` | `showroom-facility/facility_lamborghini-miami-showroom-aerial-night_1980x1114.png` (dealer-shot) | Cropped to remove the watermark |
| `archive-1980/1983/1986-*` | `showroom-facility/history-under-1600/…_640x427.jpg` (dealer archive) | Native size, shown at 320 CSS px or less |
| `inv-*` | Primary VDP photos (see the inventory table above) | Cropped to 16:9 above the lockup band |
| `logo-lamborghini-miami-lockup.png` | `logos/logo_lamborghini-miami-lockup-shield-black-text_1406x360.png` (the dealer lockup, hosted by Roadster) | Unmodified. **Note:** it carries the pre-2024 3D shield |
| `logo-prestige-imports-white.png` | `logos/logo_prestige-imports-est-1977-white_318x146.png` | Unmodified |
| `bull.svg` | `corp-site-shots/ref-logo-corp-header-bull.svg` (the lamborghini.com header bull) | Unmodified. Its use by the dealer must be covered by Lamborghini's dealer CI |

Every crop is reproducible with `site/_tools/process-images.py`. The originals are never modified.


## Hero copy (dealership slides, 30 Sep 2026)

Each claim on the hero slides, and its source. There are no superlatives, and nothing is invented.

| Slide | Line on the page | Basis |
|---|---|---|
| 1 | "14780 Biscayne Boulevard, North Miami Beach" | dealer address (see Contact) |
| 2 | "920 CV · 343 km/h · 0–100 km/h 2.7 s" | Models ledger (lamborghini.com Temerario page) |
| 3 | "New and pre-owned Lamborghini, on Biscayne Boulevard." | the inventory captured on this page (New and Used listings) and the dealer address |
| 4 | "Scheduled service, genuine parts, Lamborghini-certified collision and paint." | Service section sources: lamborghini.com dealer page `certCollisionCenter: true`, `certPaintShop: true`; dealer service and parts pages |
| 4 | "Care for every mile" (title) | A tagline, not a factual claim |
| 5 | "A family house since 1977" / "Prestige Imports, founded in Miami by Irv David in 1977." | Dealer-stated: `/our-story` (founded by Irv David), `/careers` ("second-generation family-owned … since 1977"), footer "A division of the Prestige Imports family" |


## Certified collision center section (30 Sep 2026)

| Claim on the page | Status | Source |
|---|---|---|
| "Lamborghini-certified collision repair center and paint shop"; "Certified paint shop" | verified | lamborghini.com Lamborghini Miami dealer page: `certCollisionCenter: true`, `certPaintShop: true` (CI §3.1) |
| "Repairs follow Lamborghini-approved procedures, with original Lamborghini parts" | dealer-stated | `/ccrc`, "The Certified Difference": Original Lamborghini Parts · Lamborghini approved repair procedures |
| Paintwork: polishing, refinishing, spot repair; liveries, painted and adhesive, for special-edition Lamborghinis; steel and aluminium repair; re-installation of components | dealer-stated | `/ccrc`, "PAINTWORK REPAIRS" and "STEEL AND ALUMINUM REPAIRS" |
| Phone (833) 290-5148 | dealer-stated | The service number (JSON-LD, service page). The site lists no separate collision number |

**Not used:**
- "South Florida's only Factory-Certified Collision Center" (an unverified superlative)
- The TÜV certification of the paint shop. It appears on `/ccrc` as the dealer's own claim, is unverified, and is left off the page.

The image is the Prestige Imports group paint-booth photograph (see MANIFEST). The page carries no caption (Alex); the alt text describes the scene only, and the image is not presented as the Lamborghini Miami body shop. `collision_hero_sept26.jpg` was rejected: it shows a Lotus, and this page excludes other brands.

## v2 range showcase (index_v2.html only, 1 Oct 2026)

- Model names, claims and figures are carried over unchanged from the v1 range tiles (sources above). The claims are Lamborghini's corporate claims: Revuelto "The quantum of driving", Temerario "You can't hide who you are", Urus SE "Dare to live more", Urus SE Performante "Urus at its peak".
- "Explore model" links, each checked with an HTTP request on 1 Oct 2026:
  - `https://www.lamborghini.com/en-en/models/revuelto`: 301 to the Revuelto page, then 200.
  - `https://www.lamborghini.com/en-en/models/temerario`: 200.
  - `https://www.lamborghini.com/en-en/models/urus/urus-se`: 200.
  - `https://www.lamborghini.com/en-en/models/urus/urus-se-performante`: 200.
  - The shorter `/models/urus-se` forms return 404 and are not used.
- "View inventory" goes to `#inventory`. The brief said `#showroom`, but no such anchor exists on the page, and the inventory section is `#inventory`.
