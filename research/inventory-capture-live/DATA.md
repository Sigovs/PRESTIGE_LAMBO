# Lamborghini Miami inventory: live capture

**Captured:** 30 Sep 2026, 17:47–18:05 CDT (22:47–23:05 UTC), from https://www.lamborghinimiami.com/. Fetched with curl using a Chrome user agent. Playwright was used only to find the pagination endpoint.
**Scope:** research only. Nothing under `site/` was touched.

## Method

- **The SRP HTML holds only the first 20 cards.** The page loads the rest over XHR from `/inventory?make[]=Lamborghini&limit=20&offset={0,20,40}&_modules[]=323193&_modules[]=323194`, which returns JSON. All three pages are saved in `raw/lambo-offset-*.raw`, with the extracted card HTML and JS in `*.cards.html` and `*.js.html`.
- **Cross-check against the whole inventory.** `/inventory?limit=50&offset=0..150` returned 167 listings in total (18 new + 149 used; `raw/all-*.raw`). Filtering those to make = Lamborghini gives the same 52 listings and 26 VINs, so no Lamborghini sits outside the make filter.
- **Field sources.** All fields come from the dealer's data-layer `VehicleObject_<vuid>` (`raw/vehicle-objects.json`) and from each VDP (`raw/vdp/<stock>.html`), which supplies the JSON-LD `itemCondition`, the printed price and the photo list.
- **Deduplication.** Every VIN appears twice (two vuids, stock prefixes `ICC80512-` and `ICC80512-1-`), so 52 listings reduce to **26 distinct VINs**. Both VDP URLs return HTTP 200 for every VIN.
- **Photos.** The VDP serves some galleries under the `ICC80512-1-` path at 640×480. The same hash under `ICC80512-` serves 1024×768, the largest available. `vehicles.json → photos` holds the 1024 URLs, and `photos_as_served_on_vdp` holds the originals.
- **Condition and certification.** The site states only New or Used: the URL prefix, `isNew`, and schema.org `NewCondition` / `UsedCondition`. **No car is marked certified.** `certificationProgram` is empty, `isOEMCertified` and `isDealerCertified` are 0, and "Selezione" appears on no VDP. The word "Certified" on these pages refers only to the collision centre and paint shop.
- **Fee statement.** The VDP text reads: "Price includes dealer fee of $1447.50 and $299 electronic filing fee. Tax, tag, title and registrations fees are not included and are calculated at time of purchase." SRP cards read "Sale Price $X · Dealer Fee + $1,448 · Electronic Filing Fee + $299". **Every** used car reconciles: sellingPrice + 1,447.50 + 299 = displayed price, with the .50 rounded up. That is why every price ends in ,697.
- **Trim.** A "." in the trim column is literally what the site shows (e.g. "2024 Lamborghini Revuelto ."). It is left blank in the table below.

## Photo conventions (all dealer photos)

- **Photo 0** is a front three-quarter with the **dealer lockup band** across the bottom ~20%: black band, "Prestige Imports | Lamborghini Miami" logos, and the line "14780 Biscayne Boulevard North Miami Beach, FL 33181 | sales@prestigeimports.com | (305) 947-1000". It is saved as `photos/<stock>-primary-lockup.jpg`.
- **Photos 1 onwards** have no band, but carry a small "LAMBORGHINI MIAMI" shield bug in the bottom-right corner.
- Every car is shot on the same showroom turntable against a white curtain. These are real cars: there are no placeholders, renders or "coming soon" images.
- **Downloaded set.** `photos/<stock>-1.jpg` is a clean front three-quarter with no band. `-2` is the profile, or a second three-quarter view. `-3` is the rear three-quarter, or a doors-up / front view where no rear shot is early in the gallery. The gallery index used for each is in `vehicles.json → downloaded`.

## All distinct Lamborghinis (26 VINs)

Price is shown as the site displays it. `sellingPrice` is the data-layer value. Mileage is in miles. "Home" marks the cars already on the homepage.

| Stock | Year | Model / trim | Cond. (site) | Exterior (listed) | Interior (listed) | Miles | Price displayed | sellingPrice | VIN | Photos | Home | Verdict | Note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 10914 | 2026 | Temerario | New | Verde Mercurius Metallic | not listed | 37 | Call For Price | 470,849 | ZHWUC1ZC1TLA02400 | 41 | YES | **USE** | NEW since the last check: it now has 41 real studio photos of a green Temerario, matching Verde Mercurius. |
| 10918 | 2026 | Urus SE | New | Nero Noctis Metallic | not listed | 24 | Call For Price | 313,631 | ZPBUD6ZLXTLA46954 | 56 | YES | **USE** | Gloss black Urus SE (SE rear light bar visible in photos 10–11); matches Nero Noctis. |
| 10881A | 2015 | Huracan LP610-4 | Used | Nero Nemesis Matt | Rosso Alala/Nero Ade | 18,536 | Sale Price $246,697 | 244,950 | ZHWUC1ZF6FLA02875 | 44 | YES | **USE** | Photo matches listed model and colour. |
| CJ2607 | 2018 | Huracan Performante Spyder | Used | Nero Noctis | Nero Cosmus | 8,104 | Sale Price $411,697 | 409,950 | ZHWUS4ZF6JLA10746 | 51 |  | **EXCLUDE** | Listed Nero Noctis; every photo shows a mid-grey car (unchanged from 30 Sep). |
| 86180 | 2024 | Revuelto | Used | Giallo Metallic | Nero Ade | 187 | Sale Price $651,697 | 649,950 | ZHWUC1ZM3RLA00116 | 54 | YES | **USE** | Yellow Revuelto matches. Note: the paint plate in photo 5 reads "Giallo Countach", while the listing says "Giallo Metallic". |
| CJ2602 | 2024 | Revuelto | Used | Grigio Acheso Matt | Nero Ade | 1,411 | Sale Price $741,697 | 739,950 | ZHWUC1ZM0RLA00252 | 58 | YES | **USE** | Photo matches listed model and colour. |
| CJ2626 | 2024 | Revuelto | Used | Giallo Metallic | Nero Ade | 788 | Sale Price $681,697 | 679,950 | ZHWUC1ZM6RLA01390 | 0 |  | **NO PHOTO** | Listing has 0 photos. |
| CJ2627 | 2025 | Revuelto | Used | not listed | not listed | 2,090 | Sale Price $701,697 | 699,950 | ZHWUC1ZM5SLA01922 | 0 |  | **NO PHOTO** | Listing has 0 photos; exterior colour not listed. |
| CJ2632 | 2025 | Revuelto | Used | not listed | not listed | 1,337 | Sale Price $711,697 | 709,950 | ZHWUC1ZM1SLA03103 | 0 |  | **NO PHOTO** | Listing has 0 photos; exterior colour not listed. |
| 86115X | 2019 | Urus | Used | Nero Helene Metallic | Bianco Polar/Nero Ade | 48,786 | Sale Price $168,697 | 166,950 | ZPBUA1ZL6KLA02248 | 55 |  | **USE** | Photo matches listed model and colour. |
| 85991Z | 2020 | Urus | Used | Blu Astraeus Metallic | Nero Ade | 4,872 | Sale Price $210,697 | 208,950 | ZPBUA1ZL6LLA06169 | 56 |  | **USE** | Photo matches listed model and colour. |
| CJ2597 | 2021 | Urus | Used | Grigio Keres Matt | not listed | 45,700 | Sale Price $186,697 | 184,950 | ZPBUA1ZL7MLA15500 | 54 |  | **EXCLUDE** | Listed Grigio Keres Matt; every photo shows a dark green gloss car (unchanged). |
| 86168X | 2022 | Urus | Used | Nero Noctis Matt | Nero Ade/Verde Scandal | 31,094 | Sale Price $211,697 | 209,950 | ZPBUA1ZL8NLA17774 | 55 |  | **EXCLUDE** | Listed Nero Noctis Matt; photos show gloss black, and the car's own paint plate (photo 11) reads "Nero Noctis", no Matt (unchanged). |
| 86065X | 2023 | Urus Performante | Used | Rosso Anteros Metallic | not listed | 6,530 | Sale Price $288,697 | 286,950 | ZPBUC3ZL7PLA26846 | 59 |  | **USE** | Photo matches listed model and colour. |
| CD2536 | 2023 | Urus Performante | Used | Rosso Mars Metallic | Nero Cosmus/Rosso Alala | 8,794 | Sale Price $291,697 | 289,950 | ZPBUC3ZL7PLA25115 | 60 |  | **USE** | Photo matches listed model and colour. |
| 86197J | 2023 | Urus S | Used | Grigio Keres Metallic | Nero Ade | 13,662 | Sale Price $248,697 | 246,950 | ZPBUB3ZL8PLA26387 | 52 |  | **USE** | Photo matches listed model and colour. |
| 10913A | 2023 | Urus S | Used | Grigio Hati Metallic | Nero Ade/Blu Amon | 17,564 | Sale Price $245,697 | 243,950 | ZPBUB3ZL2PLA27647 | 56 |  | **USE** | The paint reads near-white; the paint plate (photo 12) reads "GRIGIO HATI", which matches the listing. |
| 86104X | 2024 | Urus Performante | Used | Giallo Auge Metallic | Nero Cosmus/Giallo Taurus | 15,289 | Sale Price $278,697 | 276,950 | ZPBUC3ZL0RLA29400 | 60 |  | **USE** | Photo matches listed model and colour. |
| 86184J | 2024 | Urus Performante | Used | Giallo Auge Metallic | Nero Cosmus/Giallo Taurus | 12,819 | Sale Price $306,697 | 304,950 | ZPBUC3ZL2RLA29012 | 60 |  | **USE** | Photo matches listed model and colour. |
| 86198X | 2024 | Urus Performante | Used | Grigio Hati Metallic | Nero Cosmus/Blu Cepheus | 13,329 | Sale Price $309,697 | 307,950 | ZPBUC3ZL4RLA32901 | 60 |  | **USE** | Performante details present (carbon bonnet, vented hood). The paint reads near-white, but the car's paint plate (photo 21) reads "Grigio Hati", which matches the listing. Treat it as a pale grey, not white. |
| 86073X | 2024 | Urus S | Used | Nero Helene Metallic | Nero Ade | 5,313 | Sale Price $261,697 | 259,950 | ZPBUB3ZL3RLA35081 | 56 |  | **USE** | Photo matches listed model and colour. |
| 86196X | 2024 | Urus S | Used | Rosso Efesto Metallic | Nero Ade/Rosso Rea | 4,515 | Sale Price $271,697 | 269,950 | ZPBUB3ZL7RLA35245 | 55 |  | **USE** | Photo matches listed model and colour. |
| 86218 | 2024 | Urus S | Used | Rosso Efesto Metallic | Nero Ade/Rosso Alala | 7,171 | Sale Price $271,697 | 269,950 | ZPBUB3ZL0RLA34146 | 55 |  | **USE** | Photo matches listed model and colour. |
| CJ2630 | 2024 | Urus S | Used | Oro Elios Metallic | Terra Asia Vintage | 537 | Sale Price $286,697 | 284,950 | ZPBUB3ZL3RLA35890 | 49 |  | **USE** | Photo matches listed model and colour. |
| 86230X | 2024 | Urus S | Used | Verde Mantis Metallic | Nero Ade | 5,811 | Sale Price $266,697 | 264,950 | ZPBUB3ZLXRLA30573 | 0 |  | **NO PHOTO** | Listing has 0 photos. |
| CJ2622 | 2025 | Urus SE | Used | Grigio Keres Metallic | Nero Ade | 9,160 | Sale Price $291,697 | 289,950 | ZPBUD6ZL2SLA36854 | 56 |  | **USE** | Photo matches listed model and colour. |

**Counts:** 167 listings site-wide; 52 Lamborghini listings = **26 distinct VINs** (2 New, 24 Used, 0 certified). **USE 19 · EXCLUDE 3 · NO PHOTO 4.**

- **New cars:** 10914 Temerario and 10918 Urus SE. Both show "Call For Price". Their data-layer sellingPrice is 470,849 and 313,631 respectively, and neither is published.
- **Engine and transmission:** see `vehicles.json`.
- **Interior:** "not listed" means the field is empty on the site. That applies to 10914, 10918, CJ2597, 86065X, CJ2627 and CJ2632.

## The 5 cars already on the homepage (vs 30 Sep capture)

| Stock | Car | Still listed? | Price | Mileage | Change |
|---|---|---|---|---|---|
| 10918 | 2026 Urus SE, New, Nero Noctis Metallic | Yes | Call For Price (sellingPrice 313,631) | 24 | None |
| 10914 | 2026 Temerario, New, Verde Mercurius Metallic | Yes | Call For Price (sellingPrice 470,849) | 37 | **Now has 41 real photos** (previously none). The "Representative image" can be replaced with `photos/10914-1.jpg` (clean front three-quarter, green, matching the listing) |
| 86180 | 2024 Revuelto, Used, Giallo Metallic | Yes | $651,697 (649,950) | 187 | None. Note that the paint plate in the car's own photo 5 reads "Giallo Countach" |
| CJ2602 | 2024 Revuelto, Used, Grigio Acheso Matt | Yes | $741,697 (739,950) | 1,411 | None |
| 10881A | 2015 Huracán LP610-4, Used, Nero Nemesis Matt | Yes | $246,697 (244,950) | 18,536 | None |

- **Previously excluded cars.** CJ2607, CJ2597 and 86168X are still listed, and their photo mismatches are unchanged.
- **Revuelto CJ2626 and the 2025 Revuelto listings.** CJ2627 and CJ2632 still have no photos.
- **Coverage of the earlier capture.** The 30 Sep capture files contain only first-page VINs (11). The 15 other VINs (mostly Urus) are not in that capture's saved pages, so this capture cannot say whether they are newly added or were simply not captured before. Their `dateInStock` values are in `vehicles.json`.

## Recommended homepage set (8, optional 9th)

The set mixes new and pre-owned stock, keeps each model family distinct, spreads the colours, and uses only cars whose photos are strong and whose listing matches the photo.

| # | Stock | Car | Cond. | Colour | Miles | Price as displayed | Lead photo |
|---|---|---|---|---|---|---|---|
| 1 | 10914 | 2026 Temerario | New | Verde Mercurius Metallic | 37 | Call For Price | photos/10914-1.jpg |
| 2 | 10918 | 2026 Urus SE | New | Nero Noctis Metallic | 24 | Call For Price | photos/10918-1.jpg |
| 3 | 86180 | 2024 Revuelto | Used | Giallo Metallic | 187 | $651,697 | photos/86180-1.jpg |
| 4 | CJ2602 | 2024 Revuelto | Used | Grigio Acheso Matt | 1,411 | $741,697 | photos/CJ2602-1.jpg |
| 5 | 10881A | 2015 Huracán LP610-4 | Used | Nero Nemesis Matt | 18,536 | $246,697 | photos/10881A-1.jpg |
| 6 | CD2536 | 2023 Urus Performante | Used | Rosso Mars Metallic | 8,794 | $291,697 | photos/CD2536-1.jpg |
| 7 | CJ2630 | 2024 Urus S | Used | Oro Elios Metallic (int. Terra Asia Vintage) | 537 | $286,697 | photos/CJ2630-1.jpg |
| 8 | 85991Z | 2020 Urus | Used | Blu Astraeus Metallic | 4,872 | $210,697 | photos/85991Z-1.jpg |
| 9 (opt.) | CJ2622 | 2025 Urus SE | Used | Grigio Keres Metallic | 9,160 | $291,697 | photos/CJ2622-1.jpg |

**Alternates** (all USE):

- 86184J: 2024 Urus Performante, Giallo Auge, $306,697
- 86104X: 2024 Urus Performante, Giallo Auge, $278,697
- 86198X: 2024 Urus Performante, Grigio Hati (reads white; carbon bonnet; blue calipers), $309,697
- 86065X: 2023 Urus Performante, Rosso Anteros, $288,697
- 86196X and 86218: 2024 Urus S, Rosso Efesto, $271,697
- 86197J: 2023 Urus S, Grigio Keres, $248,697
- 86073X: 2024 Urus S, Nero Helene, $261,697
- 10913A: 2023 Urus S, Grigio Hati, $245,697
- 86115X: 2019 Urus, Nero Helene, $168,697

**Recommendation notes:**

- **Selezione.** No car may be labelled Selezione or certified; the site does not say so.
- **Grigio Hati.** If either Grigio Hati car is used, print the listed name. Do not describe the car as white.

## VDP URLs (first vuid per VIN; the second vuid also resolves)

- 10914: https://www.lamborghinimiami.com/vehicle-details/new-2026-lamborghini-temerario---north-miami-beach-fl-id-66311290
- 10918: https://www.lamborghinimiami.com/vehicle-details/new-2026-lamborghini-urus-se-north-miami-beach-fl-id-66267994
- 10881A: https://www.lamborghinimiami.com/vehicle-details/used-2015-lamborghini-huracan-lp610-4-north-miami-beach-fl-id-66157191
- CJ2607: https://www.lamborghinimiami.com/vehicle-details/used-2018-lamborghini-huracan-performante-spyder-north-miami-beach-fl-id-65671487
- 86180: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-65586655
- CJ2602: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-65607471
- CJ2626: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-revuelto---north-miami-beach-fl-id-66036427
- CJ2627: https://www.lamborghinimiami.com/vehicle-details/used-2025-lamborghini-revuelto---north-miami-beach-fl-id-66046886
- CJ2632: https://www.lamborghinimiami.com/vehicle-details/used-2025-lamborghini-revuelto---north-miami-beach-fl-id-66140666
- 86115X: https://www.lamborghinimiami.com/vehicle-details/used-2019-lamborghini-urus---north-miami-beach-fl-id-64896339
- 85991Z: https://www.lamborghinimiami.com/vehicle-details/used-2020-lamborghini-urus---north-miami-beach-fl-id-65769445
- CJ2597: https://www.lamborghinimiami.com/vehicle-details/used-2021-lamborghini-urus---north-miami-beach-fl-id-65526016
- 86168X: https://www.lamborghinimiami.com/vehicle-details/used-2022-lamborghini-urus---north-miami-beach-fl-id-65586654
- 86065X: https://www.lamborghinimiami.com/vehicle-details/used-2023-lamborghini-urus-performante-north-miami-beach-fl-id-64609264
- CD2536: https://www.lamborghinimiami.com/vehicle-details/used-2023-lamborghini-urus-performante-north-miami-beach-fl-id-64609499
- 86197J: https://www.lamborghinimiami.com/vehicle-details/used-2023-lamborghini-urus-s-north-miami-beach-fl-id-65722563
- 10913A: https://www.lamborghinimiami.com/vehicle-details/used-2023-lamborghini-urus-s-north-miami-beach-fl-id-66061050
- 86104X: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-performante-north-miami-beach-fl-id-64712893
- 86184J: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-performante-north-miami-beach-fl-id-65638078
- 86198X: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-performante-north-miami-beach-fl-id-65810522
- 86073X: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-s-north-miami-beach-fl-id-64609274
- 86196X: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-s-north-miami-beach-fl-id-65991015
- 86218: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-s-north-miami-beach-fl-id-66023228
- CJ2630: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-s-north-miami-beach-fl-id-66092572
- 86230X: https://www.lamborghinimiami.com/vehicle-details/used-2024-lamborghini-urus-s-north-miami-beach-fl-id-66170890
- CJ2622: https://www.lamborghinimiami.com/vehicle-details/used-2025-lamborghini-urus-se-north-miami-beach-fl-id-65991008

## Files

- `vehicles.json`: one record per VIN with every field above, plus both vuids and VDP URLs, the full-size photo URL list, the downloaded files, the verdict, and `on_homepage_now`.
- `photos/`: `<stock>-1..3.jpg` (1024×768, no lockup band, small corner bug) and `<stock>-primary-lockup.jpg` (photo 0, with the band), for all 22 cars that have photos.
- `raw/`: the SRP HTML (`lamborghini-miami-fl.html`, `new-vehicles-miami-fl.html`, `used-vehicles-miami-fl.html`); the XHR JSON pages; `vehicle-objects.json` (all 52 data-layer records); `vdp/<stock>.html` (26 VDPs); `vdp-parsed.json`; and `vins-live.txt`.
