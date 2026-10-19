# Lamborghini Miami — SRP and VDP mockups: developer handoff

**Pages:** `site/srp.html` and `site/vdp.html` (the VDP shows a 2024 Revuelto, stock CJ2602). Both are **developer mockups**.
**Round:** 5, 16 Oct 2026.
**Side-by-side review:** `site/review/round5/index.html`. Each pair puts the Prestige AAN demo and this mockup at the same viewport (1440×900 and 390×844), with the accordions and the calculator expanded.

## The rule for these pages

They **are** the latest Prestige SRP and VDP, built from Prestige's own markup and layout CSS, with the Lamborghini header, footer, fonts, colours and component styling applied over them.

Only the client's three requests change what the pages do:

1. **Click-to-call on "Call for price":** a `tel:` link to the sales line, (833) 290-5147.
2. **Two CTAs, "Check Availability" and "Schedule Consultation", on every SRP card**, as on the demo. Both open one lead dialog.
   - The VDP keeps Prestige's single **INQUIRE** in the panel, since the Prestige VDP has no Check Availability. INQUIRE opens the same dialog as a general inquiry.
3. **Bold in the VDP description:** `**…**` renders as `<strong>`. The live platform prints the asterisks today. Nothing else in the text is restyled.

## Where everything comes from

| Layer | Source |
|---|---|
| Markup | The `<main>` of `prestige-final/srp_v2.html` and `vdp_v2.html` (the build the AAN demo runs), copied by `_tools/build-inventory-mockups.py`. Only data, links and the items listed below are substituted |
| Layout CSS | `assets/css/prestige_srp.css` and `prestige_vdp.css`: Prestige's own rules (from `tokens.css`, `main.css`, `srp.css`, `vdp.css`) for exactly the classes those pages use. They were pulled from the browser by `_tools/extract-prestige-css.js` (saved as `_tools/prestige-extract-*.css`), scoped to `.pi`, with custom properties renamed to `--pi-*` |
| Lamborghini layer | `assets/css/inventory_pi.css`, scoped to `.pi`. It sets the `--pi-*` values (dark grounds, Lamborghini greys, Roboto Flex) and the Lamborghini type and components (see below). It also holds the measured demo deltas and the lead dialog |
| Behaviour | Prestige's own JS: `prestige_srp.js` (= `search5.js`) and `prestige_vdp.js` (= `vdp.js`), which runs the calculator and the Related arrows. Added on top: `inventory_pi.js` (the lead dialog and the photo arrows) and `forms_v2.js` (form validation) |
| Icons | Prestige's Phosphor set inside the layout, as on Prestige. The Lamborghini sprite is used in the header and footer |

## What the Lamborghini layer changes (styling only)

- **Grounds:** the page is `#181818`; cards and panels are `#000`; hairlines are `#494949`.
- **Text:** `#f5f5f5`, `#c4c4c4` and `#969696` (all AA on these grounds).
- **Type:** Roboto Flex throughout.
  - The intro title is set as the Lamborghini banner: ultra-condensed and uppercase, at Prestige's 50 px.
  - Prestige's dark "INVENTORY" stamp becomes the Lamborghini eyelet.
  - Functional text has a 14 px floor. Prestige sets 10–13 px for labels, buttons and spec labels, so those are raised to 14.
  - Uppercase labels use the Lamborghini tracking (0.08em).
- **Buttons:** square, condensed bold capitals at 14 px, at Prestige's geometry. Hover is a colour change instead of Prestige's sweep.
  - **Check Availability** carries the accent `#FFC000`; it is the primary action.
  - Solid buttons are white; outline buttons are white-on-dark.
- **Corners and shadows:** everything is square, with no shadows. That covers cards, accordion chips, Related arrows and photo arrows.
- **Prices:** in the accent. "Call for Price" is styled exactly as a price; it is a `tel:` link.
- **Vehicle-history reports:** the reports this car's listing offers: CARFAX, AutoCheck and iPacket, as in Prestige's bar.
  - CARFAX is the **official value badge the dealer serves for this car**, "Show me the CARFAX · 1 Owner" (`partnerstatic.carfax.com/img/valuebadge/1own.svg`, saved as `assets/img/pi/carfax-1own.svg`). Only its viewBox is trimmed to the badge.
  - AutoCheck and iPacket are Prestige's marks, unchanged.
  - Each badge sits on a white tile of one height (48 px desktop, 40 px phone). A badge is never recoloured.
- **Class clash:** both systems use a class called `.spec`. The Lamborghini `.spec` (spec-row list) draws a top rule; inside `.pi` that rule is switched off.

## Where the demo differs from the prototype CSS: the demo wins (measured at 1440×900)

- **SRP:**
  - keyword search above the filter row (527 + 118 px, 37 px tall on the demo; 44 px here, the touch target);
  - card photo 3:2 (423×283), card body inset 16 / 12 / 18, 16 px between the CTAs;
  - "Sort: All";
  - All filters reads Body · Exterior color · Trans · Drivetrain, with **Apply**.
- **VDP:**
  - no Prestige Certified block, because the car is not certified;
  - no disclaimer paragraph under the description, and no footnotes under the SRP grid or the VDP (the demo has none; the dealer's own text carries the fee line);
  - the calculator opens with the vehicle price filled in;
  - on phones Clear Form sits above Calculate Payments;
  - Options & equipment is listed alphabetically;
  - Related card titles carry the condition ("Used …" / "New …").
- **Phones:** side padding 12 px on the SRP and 16 px on the VDP, as the demo renders at 390. The prototype CSS says 20.

## Kept from earlier rounds at Alex's request

- **VDP photo:** never stretched and never cropped.
  - The photo cell is at least 4:3, the studio frame's own ratio, and it stretches with the panel. Where the panel is taller (narrower desktops), the frame is contained on black, so both columns always end on one line.
  - Measured: 1440, 597 | 597; 1280, 584 | 584; 1920, 657 | 657.
  - The panel's insets are tightened (16 / 24, 30 px spec rows).
- **Opening photo:** the first full-car exterior frame, photo 2 of 58.

## Content

- **Data:** the dealer's listings as captured on 30 Sep 2026 (`research/inventory-capture-live`).
  - The SRP carries **all 26 Lamborghinis**, recently listed first, all on one page with no pagination, as on the demo (the prototype `srp_v2.html` has pagination; the demo does not). Every card links to the one mockup VDP.
  - Four listings have no photographs yet and show the plate: CJ2626, CJ2627, CJ2632 and 86230X.
  - Three listings have colours their photos do not match: CJ2607, CJ2597 and 86168X. They are shown as the feed has them. This is a feed issue for the client.
- **Related vehicles:** six cars, all with photographs.
- **No photo:** a car without photographs (CJ2626) shows the Lamborghini "Photography in preparation" plate where the demo shows its "Coming soon" frame.
- **Bold demonstration:** the dealer's CJ2602 text has no HP or torque figure. One line is inserted, marked `data-mockup-insert`: "Maximum combined power: **1,015 CV (747 kW)**, the manufacturer figure for the Revuelto."
  - Source: lamborghini.com, captured 30 Sep 2026.
  - The figure is not converted to hp.
  - No verified torque figure exists in the ledger, so **none is shown**.
  - In production, staff type `**…**` in the listing description and the template renders it.
- **Calculator:** it has **no default APR**. The demo prefills 8.99%, which we cannot verify. The vehicle price and loan amount come from the listing. Calculate and Clear Form behave exactly as on Prestige (`vdp.js`).
- **Filtering, sorting and search are real in the mockup.**
  - `prestige_srp.js` (Prestige's `search5.js`) still runs the dropdowns, chips, badges and sort label. Its random "reshuffle" is replaced by `window.__srpApply()` in `inventory_pi.js`.
  - That function filters the cards by the checked options (each option's `name` is a card `data-` attribute), the keyword and the condition. It then sorts (recently listed, price, year, mileage), updates the count and shows an empty state.
  - **New / Pre-owned:** the navigation links carry `srp.html?condition=new` or `?condition=used`. This ticks a Condition filter (Prestige markup, kept out of the visible row because the demo has none), which shows as a removable chip: New gives 2 cars, Pre-owned 24.
  - Production filters server-side.

## Lead dialog — form submission is SIMULATED

- **Fields:** the Prestige fields: first and last name, email, phone, preferred contact (Call / Text / Email), message (prefilled with the car and its stock number), and the consent in Prestige's exact wording. "Schedule Consultation" adds a preferred date and time.
- **Hidden fields:** `request`, `vehicle`, `stock` and `vin`.
- **No endpoint:** `data-endpoint=""`. A valid request goes nowhere, and the confirmation states this on screen: "Developer mockup: submission is simulated. Nothing was sent; the form has no endpoint yet."
- **With an endpoint set:** `forms_v2.js` POSTs `FormData`, shows "Sending…", times out after 15 s, and on failure keeps the input. **Wire it to the CRM before launch.**
- The service page's request form is simulated the same way.

## Regenerating

From the project root: `python3 site/_tools/build-inventory-mockups.py`. Edit the generator or `inventory_pi.css`, never `srp.html`, `vdp.html` or `prestige_*.css`.

To refresh the Prestige CSS, run `_tools/extract-prestige-css.js` in the browser on `prestige-final/srp_v2.html` and `vdp_v2.html`, with each page's class list. Save the output to `_tools/prestige-extract-*.css`.
