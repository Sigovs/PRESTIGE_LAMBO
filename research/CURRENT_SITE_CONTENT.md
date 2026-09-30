# Lamborghini Miami: current site content audit

**Site:** https://www.lamborghinimiami.com/
**Captured:** 2026-09-30, from the raw HTML of 55 URLs (40 in `sitemap-static.xml` plus every nav and footer link). This covers 44 distinct pages once redirects and aliases are merged, plus 1 VDP and the Roadster digital-showroom page.
**Method:** `curl` with a Chrome UA, visible text extracted per page, and the chrome (header and footer text shared by 30+ pages) stripped out. Nothing on the site was submitted or changed.
**Images:** see `images-current-site/MANIFEST.md`.

> **Conventions.** Quotes in "…" are verbatim, typos included. **[UNVERIFIED]** means the site claims it and nothing else here confirms it. **[OBSERVED]** means I saw it in the markup or an image rather than in body copy. Inventory figures are a snapshot from 30 Sep 2026.

---

## 1. Platform and vendors

| Layer | Vendor | Evidence |
|---|---|---|
| CMS / website | **DealerFire "Engine 6"** (part of **DealerSocket**, now Solera) | Footer: "Next-Generation Engine 6 Custom Dealer Website powered by DealerFire. Part of the DealerSocket portfolio of advanced automotive technology products." All assets are on `cdn-ds.com`. |
| Digital retail ("Digital Showroom") | **Roadster** (CDK Global) Express Storefront | `shop.lamborghinimiami.com` and `shop.prestigeimports.com`. Assets come from `dealer-partner-assets.roadster.com`. |
| Blog | DealerFire Blogs (WordPress) | `/blog`: one default post, "Hello world!", dated June 6, 2016. |
| Vehicle history | Carfax | Badges on SRPs and VDPs |
| Window sticker / vehicle packet | iPacket (`autoipacket.com`) | VDP link `ipacket.info/{VIN}` |
| Chat | ActivEngage (`go.activengage.com`) | Script |
| Analytics | Google Tag Manager, New Relic | Scripts |
| Scroll/animation libs | AOS, jCarousel, Magnific Popup, Pannellum (360 viewer), Bootstrap, jQuery | `cdn-ds.com/e6-static/...` |
| Reviews widget | Aggregates Google, DealerRater and Cars.com | `/lamborghini-miami-dealership-customer-reviews` |
| Parent-group shop | `prestigeimports.store/lamborghini` ("Boutique") | Nav link |

URL hygiene is poor. Live URLs include `/copy-of-car-service-miami-fl` (the main Service page), `/copy-of-copy-of-car-service-miami-fl` (the Collision Center) and `/2` (the finance application). Many pages use "Miami, Fl" / "North miami beach Fl" as the breadcrumb or H1 prefix.

---

## 2. Sitemap and navigation tree

### Primary nav (header mega-menu)
```
Home  /
Models
├─ Temerario ........................ /temerario
├─ Revuelto ......................... /revuelto  → 301 → /revuelto-miami-fl   (an INVENTORY SEARCH page, not a model page)
├─ Huracán .......................... /huracan-mlp
│   ├─ Huracán Sterrato ............. /huracan-sterrato-mlp
│   ├─ Huracán Tecnica .............. /huracan-tecnica-mlp
│   ├─ Huracán STO .................. /huracan-sto-mlp
│   └─ Huracán EVO Spyder ........... /huracan-evo-spyder-mlp
├─ Urus ............................. /urus-mlp
│   ├─ Urus SE ...................... /urus-se-mlp
│   ├─ Urus S ....................... /urus-s-mlp
│   └─ Urus Performante ............. /urus-performante-mlp
├─ Marine
│   └─ "Lamborghini Miami presents Tecnomar for Lamborghini 63"  /tecnomar63
├─ Aventador ........................ /aventador
├─ Limited Series ................... /limited-series-mlp
│   └─ Countach LPI 800-4 ........... /countach-lpi-800-4-mlp
└─ Concept .......................... /clp-lamborghini-concept-models-north-miami-beach-fl
    └─ Lanzador ..................... /lanzador
Inventory ........................... /cars-for-sale-miami-fl
├─ Lamborghini ...................... /lamborghini-miami-fl
├─ Other Brands ..................... /cars-for-sale-miami-fl
└─ DIGITAL SHOWROOM ................. https://shop.lamborghinimiami.com/inventory/used
    ├─ Shop All Models .............. https://shop.lamborghinimiami.com/inventory/used
    └─ How It Works ................. https://shop.lamborghinimiami.com/how_it_works
Service ............................. /copy-of-car-service-miami-fl
├─ Our Services ..................... /copy-of-car-service-miami-fl        (alias /our-services-lm)
├─ Certified Collision Repair Center  /copy-of-copy-of-car-service-miami-fl (alias /ccrc)
├─ Schedule Service ................. /schedule-car-maintenance-or-auto-repair-miami-fl (alias /schedule-service)
├─ Order Parts ...................... /auto-parts-miami-fl                  (alias /order-parts)
└─ Service and Parts Specials ....... /car-coupons-miami-fl                 (alias /service-specials)
Boutique ............................ https://www.prestigeimports.store/lamborghini  (external)
About Us ............................ /about-lamborghini-miami-in-miami-fl
├─ Our Dealership ................... /about-lamborghini-miami-in-miami-fl  (alias /our-dealership)
├─ Our Story ........................ /our-story
├─ Testimonials ..................... /lamborghini-miami-dealership-customer-reviews (alias /testimonials)
├─ Employment ....................... /automotive-jobs-in-miami-fl          (alias /careers)
├─ Contact .......................... /contact-lamborghini-miami-in-miami-fl (alias /contact-us)
├─ Our Blog ......................... /blog
└─ Join the Club .................... https://www.lamborghini.com/en-en/club-form/US  (external, AL Club form)
Header utility: Map "14780 Biscayne Boulevard North, North Miami Beach, FL" · "Today 9-7pm" · (833) 290-5147
```

### Footer quick-links
`NEW` /new-vehicles-miami-fl · `PRE-OWNED` /used-vehicles-miami-fl · `SPECIALS` /manager-specials-in-miami-fl · **`FINANCE` /car-loans-in-miami-fl → 404 "Oops! This page doesn't exist!"** · `SERVICE` /copy-of-car-service-miami-fl · `PARTS` /auto-parts-miami-fl · `ABOUT US` · Privacy · Sitemap. Social: Facebook (`facebook.com/lamborghinimiami.prestigeimports`), Instagram (`@lamborghinimiami`), YouTube (`@lamborghiniofmiami`).

### Pages linked from the sitemap but not from the nav
- `/trade-in` → `/trade-in-car-miami-fl` ("Value Your Trade")
- `/co-applicant-finance` → `/2` (the credit application; it is the only working finance page)
- `/car-finder` → `/find-a-car-in-miami-fl`
- `/clp-reserve-lamborghini-urus-north-miami-beach-fl` (the 2017 Urus pre-launch reservation page, still live)
- `/reserve-yours-today` (a bare form)
- `/covid-19-response` (still live)
- `/huracan` → `/huracan-miami-fl` (Huracán inventory SRP)
- `/privacy`, `/sitemap`
- **VDPs:** `/vehicle-details/{used|new}-{year}-{make}-{model}---north-miami-beach-fl-id-{n}`. 162 are in `sitemap-vehicle.xml`.

### Not on the site at all (see §6)
There is no Revuelto model page, no Selezione Lamborghini / certified pre-owned page, no Ad Personam page, no Lounge page, no events or news page, no staff page, no financing landing page, no warranty page and no specials content.

---

## 3. Page by page

### 3.1 Home `/`
- **Title:** "New and Used Vehicle Dealership North Miami Beach FL | Lamborghini Miami"
- **Meta description:** "Lamborghini Miami is a new and pre-owned Lamborghini dealership in Miami, FL, that serves customers in South Florida and ships vehicles as far as Texas and Chicago!"
- **Section outline:**
  1. **Promo tiles above the hero:** "Certified Collision Center" and "Certified Paint Shop", both linking to /ccrc and both using small yellow icons.
  2. **Hero slider, 2 slides:**
     - "LAMBORGHINI URUS SE / DESIGNED BY NEW DESIRES" (orange Urus SE in a light box).
     - "LAMBORGHINI TEMERARIO / DARE TO LIVE MORE" (blue Temerario side profile).
     - Note that "DESIGNED BY NEW DESIRES" is AL's Lanzador tagline, and "DARE TO LIVE MORE" is also the Urus SE page's tagline, so the taglines are mismatched.
  3. **Three promo banners (1440x450, text baked into the images):** "TEMERARIO", "URUS S" and "URUS PERFORMANTE".
  4. **Digital showroom block:** "Welcome to the Lamborghini of your dreams." / "100% Online Experience" / "SHOP OUR DIGITAL SHOWROOM" / "Instant Pricing - No Hassle - Build Your Deal Online". CTAs are "START SHOPPING" → `shop.prestigeimports.com/inventory` (the parent group's store, not the Lamborghini one) and "SEE HOW IT WORKS".
  5. **"Featured vehicles" carousel:** 10 cards, but only 5 cars (each appears twice; see §5). They are a 2019 Urus at $168,697, a 2021 Urus at $186,697, a 2020 Urus at $210,697, a 2022 Urus at $211,697 and a 2023 Urus S at $245,697. CTAs are "Details" and "Save".
  6. **Brand copy block** under "#### Its all in the name / LAMBORGHINI MIAMI", with three H3s:
     - **"EXOTIC SELECTION"**: "…all of the newest Lamborghini models direct from Italy, including the Huracán, Aventador, and Urus." (Aventador and Huracán are both out of production.) It also mentions pre-owned cars from other brands and boats: "Tecnomar, Pardo, Iguana Yachts, Midnight Express, and VanDutch."
     - **"WORLD-CLASS SERVICE"**: financing, delivery, customisation. "In our Ad Personam Studio, materials, paint, designs, and more can all be customized, and our showroom is the ideal place to start the process." This is the only Ad Personam claim on the site. **[UNVERIFIED: whether a dedicated AP studio exists on site]**
     - **"VIP EXPERIENCE"**: "…it's our tailored, straightforward approach and incredible selection of exotics that continues to bring our customers back for their second, third and fourth sports car."
  7. **YouTube embed:** `VJcHAsXsy_o`.
- **Forms:** none apart from the global chat.

### 3.2 Model pages (templated "MLP")
Every MLP follows the same template:
- a hero with the model name and tagline;
- OVERVIEW, EXTERIOR and INTERIOR copy blocks, each rendered twice (a desktop and a mobile copy, so the text is duplicated in the HTML);
- a YouTube embed;
- a gallery;
- "# Lamborghini {Model} in North Miami Beach, FL";
- "### Check Availability" with an "inquire" CTA;
- "### Customize your {Model}" linking to "{MODEL} CONFIGURATOR" on `configurator.lamborghini.com`;
- a carousel of related inventory.

The body copy is paraphrased or copied from AL press material. None of it is dealer-authored.

| Page | Hero tagline (verbatim) | Notable content / issues |
|---|---|---|
| `/temerario` | "TEMERARIO / YOU CAN'T HIDE WHO YOU ARE" | Stats: "MAX POWER (combined ICE+EE) 920 CV · MAX. SPEED 343 km/h · 0-100 km/h 2.7s". Sections: OVERVIEW, EXTERIOR, INTERIOR, "FEEL THE ENGINE", "CENTRO STILE", "ALLEGGERITA PACKAGE" ("reduces the car's weight by over 25 kg… +67% total downforce and +62% of aero efficiency"), "CONNECT WITH YOUR TEMERARIO" (Telemetry 2.0, Memories Recorder, Dashcam, AR Navigation), "SPACEFRAME". Bottom headline: "Lamborghini Temerario **coming to** North Miami Beach, FL" (stale). Images are small: Monterey Car Week shots at 720px plus Mitja Borkert sketches. YouTube `l0TLgCZAwns`. |
| `/revuelto` | — | **No model page.** It redirects to the Revuelto inventory SRP. |
| `/huracan-mlp` | "MODELS / HURACÁN" | Family page with a variant chooser (Sterrato, Tecnica, STO, EVO Spyder). **The first gallery image is an Aventador SVJ.** Inventory carousel: 2015 Huracán LP610-4 at $246,697 and 2018 Huracán Performante Spyder at $411,697. |
| `/huracan-sterrato-mlp` | "HURACÁN STERRATO / BEYOND THE CONCRETE" | Standard template. The Huracán is out of production. |
| `/huracan-tecnica-mlp` | "HURACÁN TECNICA / TAKE ALL YOUR SOULS TO DRIVE" | Standard template. |
| `/huracan-sto-mlp` | "HURACÁN STO / BASED ON A TRUE STORY" | Standard template. |
| `/huracan-evo-spyder-mlp` | "HURACÁN EVO SPYDER / EVERY DAY AMPLIFIED" | "640 hp naturally aspirated V10". |
| `/urus-mlp` | "MODELS / URUS" | Family page with Urus S and Urus Performante choosers. **Urus SE is missing from the chooser.** |
| `/urus-se-mlp` | Hero renders as "URUS S" + "E" / "DARE TO LIVE MORE" | **Copy error:** the first OVERVIEW/EXTERIOR/INTERIOR set is the **Urus S** copy, followed by the correct Urus SE copy ("first PHEV… 800 CV… 80% emission reduction"). It hosts the site's best photography: 10 official Urus SE images at 4000–5000px. |
| `/urus-s-mlp` | "URUS S / FOR BAR RAISERS ONLY" | Standard template. |
| `/urus-performante-mlp` | "URUS PERFORMANTE / FOR BAR RAISERS ONLY" | The `<title>` wrongly says "Lamborghini Urus **S** in North Miami Beach FL", and the tagline is duplicated from Urus S. |
| `/aventador` | "MODELS / AVENTADOR / DESIGNED TO PUSH BEYOND PERFORMANCE" | Variants: SVJ, SVJ Roadster, LP 780-4 Ultimae, Ultimae RDS. The DESIGN paragraph is truncated mid-sentence: "…crafted by skilled artisans using". The model is discontinued. |
| `/limited-series-mlp` | "MODELS / LIMITED SERIES" | Countach LPI 800-4 ("only 112 units"), Sián FKP 37 ("63 units", ">350 km/h") and Sián Roadster. The chooser label reads "COUNTACH LP 800-4" (typo). |
| `/countach-lpi-800-4-mlp` | "COUNTACH LPI 800-4 / FUTURE IS OUR LEGACY" | Heritage colours are named: Giallo Countach, Impact White, Viola Pasifae, Blu Uranus. |
| `/clp-lamborghini-concept-models-...` | (no hero) | Old SEO landing copy about the **Asterion and Estoque** concepts ("might just be the next future legends"), followed by "View Lamborghini Inventory" and a 20-car carousel. Dated. |
| `/lanzador` | "DESIGNED BY NEW DESIRES / LAMBORGHINI LANZADOR" | A good long-form press rewrite covering Monterey Car Week, "Direzione Cor Tauri", "Ultra GT", ">1 megawatt" and LDVI. Quote: "With this concept, we are ushering in a new car segment, the Ultra GT…" (Stephan Winkelmann). CTAs: "Contact a Lamborghini Brand Specialist" / "Inquire", "Create Your Lamborghini" / "Configurator". Strong images at 5000px. |
| `/tecnomar63` | "THE FUTURE IS TODAY / DISCOVER THE ULTIMATE AUTOMOTIVE YACHT" | Long copy covering 2× MAN V12 at 2000 hp, 60 knots and 24 t for 63 ft; the Lounge, One Cabin and Two Cabin versions; and "Colors and materials are, 100% customizable through the program Ad Personam." Spec strip: "128 Engine Bore (mm) · 24 Engine Displacement (L) · 2000 Max Output (hp) · 2300 Rated Speed (rpm) · 18 Width (ft) · 63 Length (ft) · 41 Cruising Speed (KN) · 60 Max Speed (KN)". Has an inquiry form (name, phone, email, contact preference, comments). Typos: "avant-guarde", "Centro Stiel". |

### 3.3 Inventory
| URL | Label | Count (30 Sep 2026) | Notes |
|---|---|---|---|
| `/cars-for-sale-miami-fl` (and `/inventory`) | All | **163 results** | Price facet $0–$1,252,000; year 1965–2027 |
| `/new-vehicles-miami-fl` | New | **16** | 14 × **Lotus Emira** (2026) and 2 × Urus SE. New Lamborghini stock is almost absent. |
| `/used-vehicles-miami-fl` | Pre-owned | **147** | Mixed makes |
| `/lamborghini-miami-fl` | Lamborghini | **50** | Urus 36, Revuelto 10, Huracán 4 |
| `/revuelto-miami-fl` | Revuelto | 10 | 2024–2025, priced roughly $650k–$742k |
| `/huracan-miami-fl` | Huracán | 4 | |

- **Make facet (whole inventory):** Porsche 38 · Lamborghini 50 · Lotus 15 · Ferrari 11 · Mercedes-Benz 9 · Rolls-Royce 6 · BMW 5 · Dodge 4 · Land Rover 3 (+1 "LAND ROVER") · McLaren 3 · Chevrolet 3 · Aston Martin 2 · Audi 2 · Bentley 2 · Cadillac 2 · BACKDRAFT 2 · Koenigsegg 1 (Jesko) · Maserati 1 · Mini 1 · Shelby 1 · Volkswagen 1. These add up to 163.
- **Every vehicle is listed twice [OBSERVED].** Each VIN appears under two stock prefixes (`ICC80512-` and `ICC80512-1-`) with two VDP IDs. The 10 Revuelto listings are 5 unique VINs. **Real unique counts are therefore about half:** roughly 25 Lamborghinis and roughly 80 cars in total.
- All prices end in "…,697" (e.g. $168,697), which suggests a pricing convention or feed markup.
- **SRP template:** a left filter rail (price, mileage, MPG, year, make, model, trim, colour) and cards with Carfax badge, "Details" and "Save".
- **VDP template (sampled 2024 Revuelto, id 65586655):** gallery of 40 photos at 1024x768, shot in-house on a turntable against a curtain backdrop with a "Lamborghini Miami" shield watermark; the hero frame carries a footer lockup "Prestige Imports | LAMBORGHINI MIAMI · 14780 Biscayne Boulevard North Miami Beach, FL 33181 | sales@prestigeimports.com | (305) 947-1000" [OBSERVED in image]. Sections are "ABOUT THIS VEHICLE", "EQUIPMENT DETAIL", "VEHICLE INFO" and "Request Additional Information", followed by a Carfax link, an iPacket link, "Value your trade" and "Confirm Availability".
- **Digital Showroom (Roadster):** `shop.lamborghinimiami.com`, titled "How it Works | Lamborghini Miami". It is an online deal builder. The homepage CTA sends users to the parent store `shop.prestigeimports.com` instead.
- **Certified pre-owned:** there is **no "Selezione Lamborghini" CPO programme page or badge anywhere.**

### 3.4 Service `/copy-of-car-service-miami-fl`
- **H1:** "Why Choose Us Over the Average Garage?"
- **Claims:**
  - "We're the **largest Lamborghini service department in the country**…" **[UNVERIFIED]**
  - They service "Audi, Aston Martin, Bentley, BMW, Ferrari, Lamborghini, Lotus, Maserati, Mercedes-Benz, Pagani, Porsche, Rolls-Royce, Land Rover".
  - "only use genuine OEM factory-approved parts".
  - "We have a very large supply of parts in stock."
- **"What We Offer":** "Service pickup and delivery", "Sanitation of your vehicle's interior and exterior", "Detailing".
- **"## Schedule Service in Miami, FL":** copy about keeping appointments short.
- **Other elements:**
  - an image banner reading "24 Hour Lamborghini Road Side Assistance 1-888-464-6040" [OBSERVED in image];
  - a Prestige transporter photo;
  - two workshop photos;
  - "Service Coupons", which is empty;
  - YouTube `MuIQOgsmC7c`.
- **Service phone:** (833) 290-5148.

### 3.5 Certified Collision Repair Center `/ccrc` (served at `/copy-of-copy-of-car-service-miami-fl`)
- **Title:** "South Florida's Only Factory-Certified Collision Repair Center Miami, FL"
- **Hero:** "LAMBORGHINI MIAMI / CERTIFIED COLLISION REPAIR CENTER / # We'll be there when you need us."
- **Copy:** "As **South Florida's only Factory-Certified Collision Center**, there is no equal…" **[UNVERIFIED]**. It adds "You're still in control."
- **"The Certified Difference":** Original Lamborghini Parts · Lamborghini Factory-Trained Technicians · State-of-the-art equipment · Lamborghini approved repair procedures · Certified Results.
- **"PAINTWORK REPAIRS":** the "Certified Paint Shop" is "guaranteed by the **TÜV** certification body". Services listed: painting (polishing, refinishing and spot repairs), "Application of liveries (painted and adhesive) for special-edition Lamborghinis", and re-installation of components.
- **"STEEL AND ALUMINUM REPAIRS":** TÜV-certified procedures.
- **Images:** one AL workshop image and a placeholder camera icon. There are no photos of the actual body shop.

### 3.6 Schedule Service `/schedule-car-maintenance-or-auto-repair-miami-fl`
- **H1:** "Schedule Service"
- **Copy:** one generic paragraph.
- **Form:** the scheduler form or widget is loaded by JS, so its fields were not captured by curl. **[UNVERIFIED which scheduler]**

### 3.7 Parts `/auto-parts-miami-fl`
- **H1:** "Order Parts For Your Vehicle"
- **Form:** name, email, phone, Year/Make/Model, "Comments (Please include VIN for more accurate matching)*", contact preference. Submit button: "Send order request".
- **Parts phone:** (833) 290-5149 [OBSERVED in header markup].

### 3.8 Service & Parts Specials `/car-coupons-miami-fl`
- **H1:** "Coupons"
- **Body:** "There are currently no coupons available at this time. Please check back soon!"

### 3.9 Manager's Specials `/manager-specials-in-miami-fl`
- **H1:** "Manager's Specials"
- **Copy:** "…some of our best deals on new and used vehicles **in the Oshkosh area**." This is unedited platform boilerplate from another dealer's template.
- **Body:** "No offer found".

### 3.10 Finance
- `/car-loans-in-miami-fl` is the footer "FINANCE" link and returns **404**.
- `/co-applicant-finance` → `/2`:
  - **H1:** "Get Online Pre-Approval for Financing in Miami, FL"
  - **Copy:** "No matter your credit situation, the Lamborghini Miami financing specialists can help…"
  - **Form:** a long credit application (applicant info, residence, employment, co-applicant).
- There is no lease information, no Lamborghini Financial Services mention and no calculator page.

### 3.11 Trade-in `/trade-in-car-miami-fl`
- **H1:** "Buy or Trade Your Vehicle in North Miami Beach, FL"
- **Copy:** calls itself a "tool… to calculate the estimated trade-in value", but it is a plain lead form: year, make, model, trim, miles, VIN, drivetrain, notes and contact.
- **Weak copy:** the page gives "Honda… Toyota CAMRY / Ford EXPEDITION" as examples.

### 3.12 Car Finder `/find-a-car-in-miami-fl`
- **H1:** "Get New Matches via Email"
- **Form:** type (New/Used), year, make, model, mileage, price and contact details.

### 3.13 About / Our Dealership `/about-lamborghini-miami-in-miami-fl`
- **H1:** "Local Dealership in North Miami Beach, FL"
- **Copy:**
  - "Lamborghini Miami has been a staple here in Miami and throughout South Florida for **over 40 years**!" This conflicts with the 1977 founding date and with Our Story's "over 45 years". The Lamborghini franchise itself is not 40 years old; the heritage belongs to Prestige Imports.
  - Positions the store as a **pre-owned** dealer: "explore our excellent inventory of pre-owned Lamborghini models".
  - "the Prestige Imports Difference": support through shopping, purchase, maintenance and "trade-in or buy-back".
  - Community: "works with **Ride 2 Revive** to host special events for terminally ill children".
  - Shipping: "ship these vehicles nationwide—frequently sending models as far away as Chicago and various cities throughout Texas".
- **Also on the page:**
  - a "Testimonials" snippet with 5 reviews;
  - "#### Department hours" (hours load by JS);
  - an "Ask A Question" form (name, email, phone, comments, contact preference);
  - an aerial night image of the showroom.

### 3.14 Our Story `/our-story`
This is the richest dealer-specific content on the site. Worth keeping and rewriting.
- **Founding:** "Over 45 years ago, Prestige Imports established itself… Founded by **Irv David**." It "started from a gas station that Mr. David owned evolving into a dealership selling used European cars". He opened "one of the first exotic car dealerships in Florida".
- **Leadership:** "Upon Irv David's tragic passing in **2007**, his then 19-year-old son, **Brett**… assuming his father's position as **CEO** of Prestige Imports."
- **Famous builds:** "Lamborghini Miami, which famously introduced the **Sharpie Lamborghini** and **AU79 Aventador**".
- **Sister franchises (dated copy):** "Pagani of Miami, one of only three licensed dealers in the country, Lotus of Miami, offering the Evora, Exige, and Elise; and most recently KARMA Miami with the new Revero due for deliveries." The Lotus models and Karma are stale. **[UNVERIFIED current status]**
- **Events:** "Prestige Imports recently introduced **Exotics & Espresso**, a monthly meet & greet event…" **[UNVERIFIED whether still running]**
- **Charity:** MyWish4U, Joe DiMaggio Children's Hospital and Chai Lifeline. The **Prestigious Heart Fund** was set up with the American Heart Association. **Ride2Revive Foundation** was created in 2011 by Brett and his sister **Brooke**.
- **Brands:** "In addition to Audi, Lamborghini, Pagani, and Lotus… Certified Pre-Owned… Aston Martin, Bentley, BMW, Ferrari, Jaguar, Land Rover, Maserati, Mercedes Benz, Porsche, and Rolls Royce."
- **Quote:** "Being a second-generation dealership during this astonishing technological era allows us to redefine our focus… we continue to instill our core belief which is to provide the highest level of service and product to our customers." – Brett David
- **"## Our History in Pictures" captions (verbatim):**
  - "1980, Irv David proudly standing in-front of the original Prestige Imports on West Dixie Highway."
  - "Irv grew Prestige Imports to have Miami's finest exotic used-car inventory."
  - "1983 when Irv purchased the land on Biscayne Boulevard, where a simple trailer served as a temporary sales office."
  - "1985, as the construction of the new Prestige Imports showroom was coming to life."
  - "1986, outside the grand opening of the new Prestige Imports Showroom."
  - "1986, when Irv had the grand opening of the new Prestige Imports showroom and birthed Miami's supercar scene."
  - "2002, the construction of the Prestige Audi building at 14780 Biscayne Blvd."
  - "2020, the completion of the all new Lamborghini Miami showroom."
  - "2020, our CEO Brett David overseeing his family's dreams continue to grow."
- **Caveat:** the photos are only 640x427.

### 3.15 Testimonials `/lamborghini-miami-dealership-customer-reviews`
- **H1:** "How Are We Doing?"
- **Summary:** "**92 Testimonials**, 5 out of 5 stars" (92 five-star, 0 others). Sources: Google, DealerRater and Cars.com. Sort options: Highest rated / Most recent.
- **Dates:** the reviews shown are mostly 2021–2023. The About page shows newer ones ("Over a month ago").
- **Staff named in reviews:** see §4.

### 3.16 Employment `/automotive-jobs-in-miami-fl`
- **H1:** "Join the Lamborghini Miami Team!"
- **Copy:** "…a second-generation family-owned luxury car dealership that's been consistently delivering exceptional customer service **since 1977**." It ends "Click below to review the current openings:", but the openings list or iframe did not render in the static HTML. **[UNVERIFIED]**

### 3.17 Contact `/contact-lamborghini-miami-in-miami-fl`
- **H1:** "We Would Love To Hear From You"
- **Content:** a Location block, Sales and Service hours (loaded by JS; the static text only shows "Open Wednesdays until 7:00 pm" and "Open Wednesdays until 5:30 pm") and the service phone.
- **Form:** "Ask A Question".
- **Meta description:** calls it "a **pre-owned** dealership".

### 3.18 Other
- **`/blog`:** "Lamborghini Miami - Official Blog". The only post is "Hello world! … Welcome to DealerFire Blogs. This is your first post. Edit or delete it, then start blogging!" (June 6, 2016, "By Product Expert").
- **`/covid-19-response`:** "OUR RESPONSE to COVID-19". Offers at-home test drives and pickup/drop-off, and has a "Send Us a Message" form with a department select. Obsolete.
- **`/clp-reserve-lamborghini-urus-north-miami-beach-fl`:** "Reserve Your Lamborghini Urus". Tells visitors the Urus will be unveiled "on December 4th" (2017). Contains "## Since We Made It Possible" and "OUR DNA. MAKING THE IMPOSSIBLE POSSIBLE." Obsolete.
- **`/reserve-yours-today`:** a bare "Reserve Yours Today!" form (name, email, phone, contact preference).
- **`/privacy`:** a generic privacy notice.
- **`/sitemap`:** an HTML sitemap that lists "Unlinked Pages".

---

## 4. Facts ledger

| Fact | Value | Source |
|---|---|---|
| Legal/trading name | Lamborghini Miami, "A division of the Prestige Imports family." | Footer (all pages) |
| Address | 14780 Biscayne Boulevard North, North Miami Beach, FL 33181 | Footer; JSON-LD on `/contact-us` |
| Geo | 25.913485, -80.15750349 | JSON-LD |
| Main / Sales phone | (833) 290-5147 | Header, JSON-LD |
| Service phone | (833) 290-5148 | JSON-LD, service page |
| Parts phone | (833) 290-5149 | Header contact panel markup [OBSERVED] |
| Other numbers | (305) 947-1000 and sales@prestigeimports.com (Prestige Imports) | VDP photo footer [OBSERVED in image]. The 833 numbers look like call-tracking lines. **[UNVERIFIED]** |
| Roadside assistance | "24 Hour Lamborghini Road Side Assistance 1-888-464-6040" | Service page banner image [OBSERVED] |
| Sales hours | Mon–Fri 09:00–19:00, Sat 10:00–18:00, Sun closed | JSON-LD `openingHours` on the contact page; header "Today 9-7pm"; "Sunday Closed" in header markup |
| Service hours | Mon–Fri 08:00–17:30 (Sat/Sun not listed, so presumably closed) | JSON-LD |
| Departments | Main Store, Sales, Service, Parts, Collision/Paint (CCRC) | Header panel, nav |
| Founded | 1977 (Prestige Imports). The logo says "EST 1977"; careers says "since 1977" | `/automotive-jobs-in-miami-fl`, PI logo |
| Founder | Irv David (died 2007) | `/our-story` |
| CEO | Brett David (took over at 19, in 2007) | `/our-story` |
| Family | Brooke David (sister; co-founded Ride2Revive in 2011) | `/our-story` |
| Sites/buildings | 1980: original store on West Dixie Hwy · 1983: Biscayne Blvd land bought · 1986: Prestige showroom opened · 2002: Prestige Audi building at 14780 Biscayne · **2020: new Lamborghini Miami showroom completed** | `/our-story` captions |
| Famous projects | "Sharpie Lamborghini", "AU79 Aventador" | `/our-story` |
| Sister brands | Pagani of Miami ("one of only three licensed dealers in the country"), Lotus of Miami, Karma Miami (stale), Audi (historical) | `/our-story`. **[UNVERIFIED current]** New inventory is 14 Lotus Emira, so Lotus is still live. |
| Service claim | "largest Lamborghini service department in the country" | Service page **[UNVERIFIED]** |
| Collision claim | "South Florida's only Factory-Certified Collision Center"; TÜV-certified paint shop | `/ccrc` **[UNVERIFIED]** |
| Ad Personam | "In our Ad Personam Studio…" | Home **[UNVERIFIED]** |
| Reviews | 92 testimonials, 5.0 average (Google / DealerRater / Cars.com) | `/lamborghini-miami-dealership-customer-reviews` |
| Community / events | Ride2Revive Foundation; Exotics & Espresso (monthly meet); MyWish4U; Joe DiMaggio Children's Hospital; Chai Lifeline; Prestigious Heart Fund (AHA) | `/our-story`, About |
| Delivery reach | Ships nationwide, "frequently… Chicago and various cities throughout Texas" | About, homepage meta |
| Marine | Tecnomar for Lamborghini 63; also "Pardo, Iguana Yachts, Midnight Express, and VanDutch" | Home, `/tecnomar63` |
| Social | IG @lamborghinimiami · FB lamborghinimiami.prestigeimports · YT @lamborghiniofmiami | Footer |
| Staff names (**no staff page; titles are not stated anywhere**) | **Ciprian "Cip" Keresztesi** (sales; the most-mentioned name in reviews) · **Sheelah** (sales, sold a new Urus) · **John** ("John in service") · **Lisa**, **Eddie** (roles not stated) · **Brett** (David, CEO) | Review text on `/testimonials` and About. **[UNVERIFIED roles]** |

---

## 5. What's weak or generic vs. worth keeping

### Weak, broken or generic (fix or drop)
1. **Identity confusion.** The meta descriptions and About copy call the store "a **pre-owned** dealership". New Lamborghini inventory is 2 cars, while new Lotus is 14. The site never says plainly that it is an authorised Lamborghini dealer.
2. **Stale or discontinued models dominate the nav:**
   - Aventador, Huracán (5 pages) and Countach/Sián are discontinued.
   - Temerario still says "coming to" Miami.
   - The concept page covers the Asterion and Estoque, from 2014–15.
   - The Urus reservation page is from 2017.
3. **No Revuelto page.** The flagship V12 links straight to an inventory search.
4. **Copy errors:**
   - The Urus SE page carries Urus S copy and a broken hero ("URUS S / E").
   - The Urus Performante page has the Urus S `<title>` and tagline.
   - The Huracán gallery shows an Aventador.
   - Aventador copy is truncated mid-sentence.
   - The limited-series chooser says "COUNTACH LP 800-4".
   - The homepage uses the Lanzador tagline for the Urus SE.
   - Typos: "Its all in the name", "vehcles", "avant-guarde", "Centro Stiel".
5. **Boilerplate leaks:**
   - Manager's Specials says "…deals… in the **Oshkosh** area".
   - The blog is DealerFire's default "Hello world!" from 2016.
   - The trade-in page uses Honda and Camry examples.
   - The service meta mentions "oil changes to exhaust repair".
6. **Dead ends:**
   - FINANCE (footer) returns 404.
   - Coupons: "no coupons available".
   - Specials: "No offer found".
   - Careers: the openings list does not render.
   - The COVID page is still live.
7. **Inconsistent heritage numbers:** "over 40 years" (About), "Over 45 years ago" (Our Story), "since 1977" (Careers). Since 1977 is 49 years as of 2026.
8. **Every car is double-listed** (two stock IDs per VIN). This inflates the counts and clutters the featured carousels.
9. **The model-page copy is AL press text**, duplicated in the HTML for mobile, with no dealer voice. Weak SEO value and no local angle.
10. **Brand assets:**
    - There is no SVG logo.
    - The header "logo" is a 320x30 white **text** PNG.
    - The only true lockup (old gradient shield + "LAMBORGHINI MIAMI") lives on the Roadster subdomain and predates the 2024 flat-shield CI.
    - Promo banners have text baked into the images.
11. **Two different "shop online" destinations:** `shop.lamborghinimiami.com` (nav) and `shop.prestigeimports.com` (homepage CTA).
12. **URL slugs** such as `copy-of-copy-of-car-service-miami-fl` and `/2`.
13. **Headless-browser behaviour [UNVERIFIED].** In the Playwright session the homepage twice ended up on lamborghini.com (the Urus page, then the Revuelto models page) without any interaction. Curl never showed a redirect, and the cause was not isolated: it could be a script, a hero link, or bot handling. Worth re-testing in a normal browser before assuming the live site behaves this way.

### Worth keeping (strong raw material)
1. **The Prestige/David family heritage story:** gas station to exotic pioneer; 1977; Irv and Brett David; the Biscayne Blvd timeline from 1983, 1986, 2002 and 2020; the period photos. It is authentic, specific and exclusive to this dealer.
2. **Famous dealer projects:** the **Sharpie Lamborghini** and the **AU79 Aventador**. They are named but not told; a redesign could expand them into features.
3. **Aftersales credentials:** the factory-certified Collision Repair Center, the TÜV-certified Paint Shop (including special-edition liveries), the "largest Lamborghini service department" claim (needs verification), 24-hour roadside assistance, the enclosed transporter fleet, and pickup and delivery.
4. **The Tecnomar for Lamborghini 63 / marine angle.** It is unique to Miami, and the yacht imagery includes Miami-skyline shots.
5. **Community:** Ride2Revive, Exotics & Espresso, and the charities.
6. **Social proof:** 92 five-star reviews, recurring named advisors, and national shipping (Chicago, Texas).
7. **Photography:** 5000px official Urus SE and Lanzador sets, the showroom aerial at night, and the bright service-hall shots. The in-house turntable studio gives consistent inventory photography, though only at 1024px.
8. **Lanzador page copy.** A well-structured long-form model story; a good model for how the other pages could read.

---

## 6. Content gaps (for the redesign brief)
- **Revuelto** model page, and a proper **Temerario** page (the car has launched, so drop "coming to").
- **Selezione Lamborghini** certified pre-owned programme: warranty, inspection and badge. Nothing exists today.
- **Ad Personam:** there is only one sentence on the homepage. There is no studio page, no process and no imagery. **[Verify whether the showroom has an AP lounge]**
- **Events / Lamborghini lifestyle:** Exotics & Espresso, Esperienza/Academy driving experiences, Squadra Corse, owner events, the Lamborghini Club link (currently external only).
- **Team:** staff and brand specialists with titles and photos (the only staff photo is one of Brett David at 640px). A leadership page for Brett David.
- **Showroom / facility:** the 2020 showroom has no dedicated page and no daylight hi-res exterior (only 640px and one night aerial); likewise the service hall and the collision/paint shop.
- **Financing & leasing:** a working finance landing page, Lamborghini Financial Services, lease specials, a calculator.
- **Specials** (currently empty), **service menu or pricing**, **warranty/extended warranty**, **maintenance programme**.
- **Hours, map and directions** as real on-page content (at present JS-injected, with contradictory "Open Wednesdays until…" text).
- **News / blog:** there is no real editorial.
- **Accurate new-vehicle offer:** allocation, order process, configurator hand-off, delivery experience.
- **Parent-brand context:** how Lamborghini Miami sits within Prestige Imports (Pagani, Lotus and pre-owned exotics) without diluting the Lamborghini experience.
- **De-duplicated, accurate inventory counts**, and a "Lamborghini-only" pre-owned view as the default.

---

## 7. Page inventory audited
Home · Temerario · Huracán family + 4 variants · Urus family + 3 variants · Aventador · Limited Series · Countach · Concept · Lanzador · Tecnomar 63 · Revuelto SRP · Huracán SRP · All / New / Used / Lamborghini SRPs · 1 VDP (2024 Revuelto) · Service · CCRC · Schedule Service · Parts · Service Specials · Manager Specials · Finance (404) · Credit app (/2) · Trade-in · Car Finder · About · Our Story · Testimonials · Careers · Contact · Blog · COVID · Urus Reserve CLP · Reserve Yours Today · Privacy · HTML Sitemap · Roadster "How it Works". **That is 44 distinct pages, plus 1 VDP and 1 external Roadster page.**
