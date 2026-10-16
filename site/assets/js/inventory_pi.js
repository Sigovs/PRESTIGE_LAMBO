/* ============================================================
   LAMBORGHINI MIAMI — inventory mockups (srp.html, vdp.html): the additions to
   Prestige's own behaviour (prestige_srp.js, prestige_vdp.js):
   - the lead dialog behind "Check Availability" / "Schedule Consultation" (SRP cards, client)
     and INQUIRE (VDP panel, as Prestige);
     submission is SIMULATED — forms_v2.js confirms locally, there is no endpoint
   - the VDP photo's previous / next buttons step through the listing's photographs
   ============================================================ */
(() => {
    'use strict';
    const $ = (s, r = document) => r.querySelector(s);
    const $$ = (s, r = document) => [...r.querySelectorAll(s)];

    /* ---------- lead dialog ---------- */
    const dlg = $('#lead');
    if (dlg) {
        const form = $('#lead-form');
        let opener = null;
        const KIND = {
            availability: { label: 'Check availability', msg: (v, s) => `Is the ${v} (stock ${s}) still available?` },
            consultation: { label: 'Schedule consultation', msg: (v, s) => `I would like to schedule a consultation about the ${v} (stock ${s}).` },
            inquire: { label: 'Inquire', msg: (v, s) => `I would like more information about the ${v} (stock ${s}).` }   // the VDP's INQUIRE (Prestige)
        };
        function open(btn) {
            const kind = btn.dataset.leadOpen;
            const { vehicle, stock, vin } = btn.dataset;
            window.__leadForms?.reset(form);
            $('[data-lead-kind]', dlg).textContent = KIND[kind].label;
            $('[data-lead-vehicle]', dlg).textContent = vehicle;
            $('[data-lead-stock]', dlg).textContent = `Stock ${stock} · VIN ${vin}`;
            const set = (n, v) => { $(`[data-lead-field="${n}"]`, form).value = v; };
            set('request', kind); set('vehicle', vehicle); set('stock', stock); set('vin', vin);
            set('message', KIND[kind].msg(vehicle, stock));
            $$('[data-lead-only]', form).forEach((el) => {
                const on = el.dataset.leadOnly === kind;
                el.hidden = !on;
                $$('input, select', el).forEach((i) => { i.disabled = !on; });
            });
            opener = btn;
            dlg.showModal();
            window.__lenis?.stop();
            $('#lead-first').focus();
        }
        const close = () => { if (dlg.open) dlg.close(); };
        dlg.addEventListener('close', () => { window.__lenis?.start(); opener?.focus(); });
        $$('[data-lead-open]').forEach((b) => b.addEventListener('click', (e) => { e.preventDefault(); open(b); }));
        $$('[data-lead-close]', dlg).forEach((b) => b.addEventListener('click', close));
        dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });   // backdrop
    }

    /* ---------- SRP: the real result set behind Prestige's controls ----------
       prestige_srp.js (Prestige's search5.js) runs the dropdowns, chips, badges, sort label and
       page links, and calls window.__srpApply() wherever Prestige "reshuffled". Here the cards are
       filtered by the checked options (input name = the card's data attribute), the keyword and
       the ?condition= state the New / Pre-owned links carry; then sorted and paged, 12 per page. */
    const grid = $('.srp-grid');
    if (grid) {
        const PAGE = 12;
        const cards = $$(':scope > li', grid);
        const original = cards.slice();
        const count = $('.srp-intro__count b');
        const pager = $('.pagination');
        const pageLinks = $$('.pagination__link:not(.pagination__link--nav)', pager);
        const [prevLink, nextLink] = [$$('.pagination__link--nav', pager)[0], $$('.pagination__link--nav', pager).pop()];
        const empty = $('[data-srp-empty]');
        const key = $('.key-search');
        let lastSig = '';

        const SORTS = {
            'Recently listed': (a, b) => (b.dataset.date > a.dataset.date ? 1 : -1),
            'Price · low to high': (a, b) => (Number(a.dataset.price) || Infinity) - (Number(b.dataset.price) || Infinity),
            'Price · high to low': (a, b) => (Number(b.dataset.price) || -1) - (Number(a.dataset.price) || -1),
            'Year · newest first': (a, b) => Number(b.dataset.year) - Number(a.dataset.year),
            'Mileage · lowest first': (a, b) => Number(a.dataset.miles) - Number(b.dataset.miles)
        };
        const activePage = () => Number(($('.pagination__link--active', pager) || {}).textContent) || 1;
        function setPage(n) {
            pageLinks.forEach((a) => {
                const on = Number(a.textContent) === n;
                a.classList.toggle('pagination__link--active', on);
                if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
            });
        }
        function apply() {
            const checked = $$('.filter-bar input[type="checkbox"]:checked');
            const groups = {};
            checked.forEach((b) => { (groups[b.name] = groups[b.name] || []).push(b.value); });
            const words = (key?.value || '').toLowerCase().split(/\s+/).filter(Boolean);
            const sortLabel = ($('.sort__option--active') || {}).textContent?.trim() || '';
            const sig = JSON.stringify([groups, words, sortLabel]);
            if (sig !== lastSig) { setPage(1); lastSig = sig; }       // a new query starts on page 1

            const sorted = SORTS[sortLabel] ? original.slice().sort(SORTS[sortLabel]) : original.slice();
            const hits = sorted.filter((li) => Object.entries(groups).every(([k, vals]) => vals.includes(li.dataset[k]))
                && words.every((w) => li.dataset.text.includes(w)));
            const pages = Math.max(1, Math.ceil(hits.length / PAGE));
            let page = Math.min(activePage(), pages);
            setPage(page);

            sorted.forEach((li) => grid.append(li));
            const shown = new Set(hits.slice((page - 1) * PAGE, page * PAGE));
            cards.forEach((li) => { li.hidden = !shown.has(li); });

            if (count) count.textContent = hits.length;
            if (empty) empty.hidden = hits.length > 0;
            pageLinks.forEach((a) => { a.hidden = Number(a.textContent) > pages; });
            if (prevLink) prevLink.classList.toggle('pagination__link--disabled', page <= 1);
            if (nextLink) nextLink.classList.toggle('pagination__link--disabled', page >= pages);
            if (pager) pager.hidden = hits.length === 0;
        }
        window.__srpApply = apply;

        const step = (d) => (e) => {
            e.preventDefault();
            setPage(activePage() + d);
            apply();
            grid.scrollIntoView({ block: 'start' });
        };
        prevLink?.addEventListener('click', step(-1));
        nextLink?.addEventListener('click', step(1));
        key?.addEventListener('input', apply);
        key?.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); apply(); } });
        $('.stock-btn')?.addEventListener('click', (e) => { e.preventDefault(); apply(); });
        $('[data-srp-clear]')?.addEventListener('click', () => {
            if (key) key.value = '';
            const all = $('.filter-chips .chip-clear');
            if (all && $('.filter-chips .chip')) all.click(); else apply();
        });

        // New / Pre-owned: the navigation links carry ?condition=new|used
        const cond = { new: 'New', used: 'Pre-owned' }[new URLSearchParams(location.search).get('condition')];
        const box = cond && $(`input[name="cond"][value="${cond}"]`);
        if (box) { box.checked = true; box.dispatchEvent(new Event('change', { bubbles: true })); }
        apply();
    }

    /* ---------- VDP photo: previous / next ---------- */
    const img = $('[data-stage-img]');
    if (img) {
        const photos = $$('.vdp-photos__item img').map((i) => i.getAttribute('src'));
        const n = $('[data-stage-n]');
        const base = img.alt.replace(/, photograph \d+ of \d+$/, '');
        let k = Number(img.dataset.start) || 0;
        const show = (i) => {
            k = (i + photos.length) % photos.length;
            img.src = photos[k];
            img.alt = `${base}, photograph ${k + 1} of ${photos.length}`;
            if (n) n.textContent = k + 1;
        };
        $('.vdp-gallery__nav--prev')?.addEventListener('click', (e) => { e.preventDefault(); show(k - 1); });
        $('.vdp-gallery__nav--next')?.addEventListener('click', (e) => { e.preventDefault(); show(k + 1); });
    }
})();
