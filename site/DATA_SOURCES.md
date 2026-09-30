# Data sources and content ledger: homepage v1

Every fact, figure and promise shown in `index.html` is listed below with its source. This file is the human-readable content ledger (design-dna content-provenance CP1–CP7). The same claims are in machine form in `.gates/content-ledger.json`.

## Status key

- **verified**: taken from a primary source.
- **dated**: true only at the capture date; the date is printed next to it on the page.
- **dealer-stated**: the dealer's own published statement, with no independent confirmation.
- **confirm**: in use, but the client has to confirm it before launch.

## Inventory (captured 30 Sep 2026)

**Method.** Each listing page was fetched with `curl` using a Chrome user agent, and the schema.org JSON-LD on the page was parsed. The raw captures are in `research/inventory-capture-2026-09-30/`:
- `srp.html`
- `new.html`
- `vdp-jsonld.json`
- `photos/`

**Deduplication.** Every VIN is listed twice on the source site, under stock prefixes `ICC80512-` and `ICC80512-1-`. One card is shown per VIN.

**Photos.** Each card uses the primary photo of that VIN. The footer band carrying the Prestige / Lamborghini Miami lockup is cropped off. Photos are 1024×768 at most.

| Card | VIN | Stock | Colour (as listed) | Odometer | Price (as listed) | Source URL |
|---|---|---|---|---|---|---|
| 2026 Urus SE, New | ZPBUD6ZLXTLA46954 | 10918 | Nero Noctis Metallic | 24 mi | none listed, shown as "Price on request" | https://www.lamborghinimiami.com/vehicle-details/new-2026-lamborghini-urus-se-north-miami-beach-fl-id-66267994 |
| 2026 Temerario, New | ZHWUC1ZC1TLA02400 | 10914 | Verde Mercurius Metallic | 37 mi | none listed, shown as "Price on request" | https://www.lamborghinimiami.com/vehicle-details/new-2026-lamborghini-temerario---north-miami-beach-fl-id-66311290 |
| 2024 Revuelto, Pre-owned | ZHWUC1ZM3RLA00116 | 86180 | Giallo Metallic | 187 mi | $651,697 | https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-65586655 |
| 2024 Revuelto, Pre-owned | ZHWUC1ZM0RLA00252 | CJ2602 | Grigio Acheso Matt | 1,411 mi | $741,697 | https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-65607471 |
| 2018 Huracán Performante Spyder, Pre-owned | ZHWUS4ZF6JLA10746 | CJ2607 | Nero Noctis | 8,104 mi | $411,697 | https://www.lamborghinimiami.com/vehicle-details/used-2018-lamborghini-huracan-performante-spyder-north-miami-beach-fl-id-65671487 |
| 2022 Urus, Pre-owned | ZPBUA1ZL8NLA17774 | 86168X | Nero Noctis Matt | 31,094 mi | $211,697 | https://www.lamborghinimiami.com/vehicle-details/used-2022-lamborghini-urus---north-miami-beach-fl-id-65586654 |

### Listing endpoints

- All Lamborghini: https://www.lamborghinimiami.com/lamborghini-miami-fl. The page reports "52 Results", which is about 26 VINs. It also covers three more 2024–25 Revuelto VINs (…01390, …01922, …03103) and a 2015 Huracán, none of which is shown here.
- New: https://www.lamborghinimiami.com/new-vehicles-miami-fl. The only Lamborghinis in it are the Urus SE and the Temerario above; the rest of new stock is Lotus, which is excluded on this page.

### Left out, and why

- **2021 Urus, ZPBUA1ZL7MLA15500.** It is listed as "Grigio Keres Matt", but its photo shows a dark green car. The listing contradicts itself, so it is not shown.
- **Three Revuelto VINs.** Their listings have no photos. Showing the two photographed Revueltos is enough; the rest are behind "View all inventory".
- **2026 Temerario.** It is shown even though it has no photos, because it is the only new Temerario. Its card carries a visibly-labelled plate, "Photography in preparation", instead of a borrowed image (CP4, CP7).

### Price notes

- Every listed price ends in ",697". That is the source's convention and is reproduced unchanged.
- **Confirm:** Florida §501.976(16) requires an advertised price to include all fees except tax, tag, registration and title. We cannot tell whether the listed prices meet this, so the page prints no "includes fees" statement. It says "Price, availability and applicable fees are subject to change; please confirm with our sales team." The client must confirm the pricing basis, and whether the §501.976(18) predelivery-fee disclosure applies.

## Model range: manufacturer claims

Source: `research/LAMBORGHINI_CI_RESEARCH.md`, captured from lamborghini.com on 30 Sep 2026.

| Claim on page | Status | Source |
|---|---|---|
| Temerario: 920 CV max power (combined ICE+EE), 343 km/h top speed, 0–100 km/h 2.7 s | verified, dated | CI §1.9 (KPI trio and spec rows, lamborghini.com/en-en/models/temerario) |
| "You can't hide who you are" (Temerario) | verified | CI §5 (claims per model) |
| "The quantum of driving" (Revuelto) | verified | CI §5, shot 01 |
| Revuelto SV: 1,065 CV, limited to 1,963 units | verified | CI §5 (media.lamborghini.com press release) |
| "Revuelto SV: Under approval, not available for sale" | verified | CI §1.9, shot 04 |
| "Urus at its peak" (Urus SE Performante) | verified as a corporate Urus claim; **confirm** that it may be reused against the SE Performante | CI §5 |
| Urus SE: plug-in hybrid, 800 CV | dealer-stated. It comes from the current Urus SE page, which reproduces AL press copy ("first PHEV… 800 CV"). **Confirm** against lamborghini.com | `research/CURRENT_SITE_CONTENT.md` §3.2 |
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

| File(s) in `assets/img/` | Source original | Treatment |
|---|---|---|
| `hero-temerario-*` | `hero/hero_temerario-blue-front-3q-dark_1920x707.jpg` (official AL; no watermark) | Desktop uses the full frame. Mobile is cropped to x 760–1920 |
| `adp-urus-se-cabin-*` | `models/urus-se/urus-se_interior-dashboard-orange_5000x3333.jpg` (official AL; shield watermark) | Cropped to remove the watermark. Mobile has a separate 4:5 crop |
| `service-workshop-*` | `service/service_workshop-white-bays-technician_1697x2121.jpg` (dealer-shot) | Cropped to remove the watermark |
| `showroom-aerial-night-*` | `showroom-facility/facility_lamborghini-miami-showroom-aerial-night_1980x1114.png` (dealer-shot) | Cropped to remove the watermark |
| `archive-1980/1983/1986-*` | `showroom-facility/history-under-1600/…_640x427.jpg` (dealer archive) | Native size, shown at 320 CSS px or less |
| `inv-*` | Primary VDP photos (see the inventory table above) | Cropped to 16:9 above the lockup band |
| `logo-lamborghini-miami-lockup.png` | `logos/logo_lamborghini-miami-lockup-shield-black-text_1406x360.png` (the dealer lockup, hosted by Roadster) | Unmodified. **Note:** it carries the pre-2024 3D shield |
| `logo-prestige-imports-white.png` | `logos/logo_prestige-imports-est-1977-white_318x146.png` | Unmodified |
| `bull.svg` | `corp-site-shots/ref-logo-corp-header-bull.svg` (the lamborghini.com header bull) | Unmodified. Its use by the dealer must be covered by Lamborghini's dealer CI |

Every crop is reproducible with `site/_tools/process-images.py`. The originals are never modified.
