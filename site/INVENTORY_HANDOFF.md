# Lamborghini Miami — SRP and VDP mockups: developer handoff

**Mockups:** `site/srp.html` (inventory results) and `site/vdp.html` (one representative vehicle: 2024 Revuelto, stock CJ2602). Each page has a desktop and a phone layout.
**Built:** 16 Oct 2026.

## Where the layout and the look come from

- **Structure and behaviour:** the latest Prestige Imports build on the AAN demo (`prestigeimports.aandemo.com/current-inventory/`). The order of blocks, the controls and the two card CTAs are Prestige's, so the two sites behave the same.
- **Look:** the Lamborghini Miami v2 system (`DESIGN_SYSTEM.md`):
  - Roboto Flex in its three widths, standing in for Lambotype;
  - black, `#181818` and white grounds;
  - the `#FFC000` accent only on prices and the primary action;
  - square corners, spec rows, no shadows;
  - the same header, menu and footer as `service.html`.

## Client requests built in (feedback of 16 Oct 2026)

| Request | Where | Implementation |
|---|---|---|
| Click-to-call where it says "Call for price" | SRP cards, VDP panel | `<a class="price__call" href="tel:+18332905147">Call for price</a>`, the sales line. It replaces the plain text the platform prints today. |
| Two CTAs, "Confirm availability" and "Schedule a consultation" | Every SRP card, the VDP panel, related cards | **Check availability** (accent, primary) and **Schedule consultation** (outline). The labels match the Prestige demo. Both open one lead dialog (see below). |
| Bold key stats in the VDP description | VDP › About this vehicle | `**text**` renders as `<strong>`. A whole line in `**` becomes a sub-heading, and the first one becomes the lead. **The live platform prints the asterisks literally today** (seen on prestigeimports.com and lamborghinimiami.com VDPs). Staff already type them, so rendering them is the whole fix. |

## SRP

1. **Intro:** the eyelet "Inventory", the title "The current selection" and the vehicle count.
2. **Filter bar:**
   - Keyword search, then dropdowns for Condition, Year, Model, Trim and Price, then **All filters** and **Sort**.
   - From 1024 px the bar sticks under the header.
   - Dropdown panels float, so opening one never moves the results. A panel that would leave the screen hangs from its trigger's right edge.
   - **All filters** opens in flow (Body style, Exterior colour, Mileage, Drivetrain) and pushes the results down, as on the demo.
   - Active filters show as removable chips, with "Clear all".
   - On phones the triggers sit in a two-column grid, with Sort across the full width.
3. **Card**, after the demo card:
   - photo (16:9) with a New / Pre-owned tag;
   - name;
   - mileage · gearbox;
   - Exterior, Interior, Engine and Stock rows;
   - price, or "Call for price";
   - the two CTAs.

   The card grid is 3 columns from 1200 px, 2 from 768 px and 1 on phones.
4. **States:**
   - no photo: a "Photography in preparation" plate (CJ2626);
   - "Call for price" (the two new cars);
   - empty results: a message and a "Clear all filters" link;
   - pagination.
5. **Footnote:** the fee statement, as published on the listings.

## VDP

1. Breadcrumb.
2. **Summary:**
   - Photo stage, with previous / next, swipe and the ←/→ keys, plus a count.
   - A strip of five thumbnails under the stage.
   - The panel: condition, name, price, then spec rows (Exterior, Interior, Engine, Transmission, Drivetrain, Mileage, Stock, VIN), then the two CTAs.
   - The action bar: Share (the native share sheet, or copy the link) · Text us (`sms:`) · the sales phone · **Start buying** (the Roadster storefront, `shop.lamborghinimiami.com`).
   - From 1200 px the photo and the panel sit 7 : 5, and the stage fills the height the panel leaves above the strip.
3. **Accordions**, as Prestige: About this vehicle (open), Options & equipment (the listing's 132 items), Finance calculator.
   - The calculator has **no default rate**. It computes only from figures the visitor enters, and says so in its footnote.
4. **Gallery:** 12 photos, then "Show all 58 photos". A thumbnail sets the stage and scrolls to it.
5. **Related vehicles:** the same card as the SRP.

## Lead dialog (both CTAs)

- **Fields:** first and last name, email and phone (all required), Preferred contact (Call / Text / Email), message (prefilled with the car and its stock number), and the consent in Prestige's exact words. These are the same fields as the service form.
- **Schedule consultation** adds Preferred date and Preferred time.
- **Hidden fields** carry `request` (availability | consultation), `vehicle`, `stock` and `vin`.
- **States:** invalid (a message under each field, plus a linked summary that takes focus), sending (with a 15 s timeout), sent, failed (the input is kept).
- **Behaviour:**
  - native `<dialog>`, closed by Escape or a backdrop click;
  - focus returns to the button that opened it;
  - full screen on phones;
  - Lenis is paused while it is open.
- **No endpoint yet:** `data-endpoint=""`, so the mockup confirms locally. **Wire it to the CRM before launch.**

## Mockup simplifications, not to copy into production

- **Card links:** every card links to the one mockup VDP. Production links each card to its own VDP.
- **Filtering:** it runs on the 12 cards on the page. The count shows the inventory total (26) until a filter is applied, and then the number of matching cards on this page. Production filters server-side, and the counts beside each option come from the feed.
- **Data:** cars, prices, photos and texts are the dealer's own listings as captured on 30 Sep 2026 (`research/inventory-capture-live`).
- **Photos:**
  - Card photos are local 16:9 crops that stop above the small shield in the corner.
  - The VDP stage and gallery hotlink the dealer CDN (`cdn-ds.com`), so the shield shows in the corner of those frames, as it does on the live site.
  - Photo 0 (the frame with the dealer lockup band) is not used as the opening view.
- **Description copy:** it is shown as the dealer wrote it. It quotes 1,414 miles and "Stock #ATA00252", while the listing data says 1,411 and CJ2602. That is a feed-copy issue to raise with the client.

## Files

| File | What it is |
|---|---|
| `srp.html`, `vdp.html` | The mockups. They are **generated**: edit `_tools/build-inventory-mockups.py` and run it from the project root. |
| `assets/css/inventory_v2.css` | SRP, VDP and dialog styles. |
| `assets/css/forms_v2.css` | Form fields, shared with the lead dialog. A copy of the service page's form styles. |
| `assets/js/inventory_v2.js` | Dropdowns, filtering, chips, sort, search, dialog, stage and gallery, share, calculator. |
| `assets/js/forms_v2.js` | Lead form validation and states. |
| `assets/img/inv/` | The 16:9 card crops. |
