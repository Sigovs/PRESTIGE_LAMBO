/* ============================================================
   LAMBORGHINI MIAMI — inventory MOCKUPS (srp.html, vdp.html)
   SRP: dropdowns (one open at a time, outside click closes), real
   filtering of the cards on the page by data attributes, chips, sort,
   keyword search, All filters, empty state. Both pages: the lead dialog
   behind "Check availability" / "Schedule consultation". VDP: photo
   stage, gallery, share, finance calculator. main_v2.js carries Lenis,
   the header and the menu; forms_v2.js validates the lead form.
   Without JS: dropdowns still open (<details>), every card shows, the
   CTA buttons do nothing — production replaces them with links.
   ============================================================ */
(() => {
    'use strict';
    const $ = (s, r = document) => r.querySelector(s);
    const $$ = (s, r = document) => [...r.querySelectorAll(s)];

    /* ---------- dropdowns ---------- */
    const drops = $$('.filter-bar details');
    drops.forEach((d) => d.addEventListener('toggle', () => {
        if (!d.open) return;
        drops.forEach((o) => { if (o !== d) o.open = false; });
        // a panel that would leave the screen hangs from the trigger's right edge instead
        const panel = d.querySelector('.filter__panel');
        if (!panel) return;
        panel.classList.remove('is-flipped');
        if (panel.getBoundingClientRect().right > document.documentElement.clientWidth - 8) panel.classList.add('is-flipped');
    }));
    document.addEventListener('click', (e) => drops.forEach((d) => { if (d.open && !d.contains(e.target)) d.open = false; }));
    document.addEventListener('keydown', (e) => {
        if (e.key !== 'Escape') return;
        const open = drops.find((d) => d.open);
        if (open) { open.open = false; open.querySelector('summary').focus(); }
    });

    /* ---------- filtering (SRP) ---------- */
    const grid = $('.srp-results .srp-grid');
    if (grid) {
        const cards = $$(':scope > li', grid);
        const count = $('[data-result-count]');
        const TOTAL = count ? count.textContent : '';
        const chips = $('[data-chips]');
        const clearAll = $('[data-chips-clear]', chips);
        const empty = $('[data-empty]');
        const q = $('#srp-q');
        const boxes = $$('.filter-bar input[type="checkbox"]');
        const labelOf = (box) => box.closest('.filter__option').querySelector('span').textContent;

        function apply() {
            const groups = {};
            boxes.filter((b) => b.checked).forEach((b) => { (groups[b.name] = groups[b.name] || []).push(b.value); });
            const words = (q.value || '').toLowerCase().split(/\s+/).filter(Boolean);
            let shown = 0;
            cards.forEach((li) => {
                const ok = Object.entries(groups).every(([k, vals]) => vals.includes(li.dataset[k]))
                    && words.every((w) => li.dataset.text.includes(w));
                li.hidden = !ok;
                if (ok) shown++;
            });
            const filtering = Object.keys(groups).length || words.length;
            count.textContent = filtering ? shown : TOTAL;   // mockup: counts the cards on this page once filtering
            empty.hidden = shown > 0;
            // trigger state
            $$('.filter').forEach((f) => f.classList.toggle('has-value', !!$('input:checked', f)));
            // chips
            $$('.chip', chips).forEach((c) => c.remove());
            boxes.filter((b) => b.checked).forEach((b) => {
                const c = document.createElement('button');
                c.type = 'button';
                c.className = 'chip';
                c.innerHTML = '<span></span><svg class="icon" aria-hidden="true"><use href="#i-close"/></svg>';
                c.firstChild.textContent = labelOf(b);
                c.setAttribute('aria-label', `Remove filter: ${labelOf(b)}`);
                c.addEventListener('click', () => { b.checked = false; apply(); });
                chips.insertBefore(c, clearAll);
            });
            clearAll.hidden = !boxes.some((b) => b.checked);
        }
        boxes.forEach((b) => b.addEventListener('change', apply));
        $$('.filter__clear').forEach((btn) => btn.addEventListener('click', () => {
            const scope = btn.closest('.filter, .filter-all');
            $$('input:checked', scope).forEach((b) => { b.checked = false; });
            apply();
        }));
        $$('[data-chips-clear]').forEach((btn) => btn.addEventListener('click', () => {
            boxes.forEach((b) => { b.checked = false; });
            q.value = '';
            apply();
        }));
        $('.srp-search').addEventListener('submit', (e) => { e.preventDefault(); apply(); });
        q.addEventListener('input', apply);

        // All filters: in flow under the row
        const allBtn = $('[data-all-toggle]');
        const allPanel = $('#filter-all');
        allBtn.addEventListener('click', () => {
            const open = allPanel.hidden;
            allPanel.hidden = !open;
            allBtn.setAttribute('aria-expanded', String(open));
        });
        $('[data-all-close]').addEventListener('click', () => { allPanel.hidden = true; allBtn.setAttribute('aria-expanded', 'false'); allBtn.focus(); });

        // sort
        const keys = [['date', -1], ['price', 1], ['price', -1], ['year', -1], ['miles', 1]];
        $$('.sort__option').forEach((opt, k) => opt.addEventListener('click', () => {
            $$('.sort__option').forEach((o) => o.classList.toggle('is-active', o === opt));
            $('.sort__value').textContent = opt.textContent;
            opt.closest('details').open = false;
            const [key, dir] = keys[k];
            const val = (li) => (key === 'date' ? li.dataset.sortDate : Number(li.dataset['sort' + key[0].toUpperCase() + key.slice(1)]));
            cards.slice().sort((a, b) => {
                let x = val(a), y = val(b);
                if (key === 'price') { if (!x) return 1; if (!y) return -1; }   // "Call for price" goes last either way
                return (x > y ? 1 : x < y ? -1 : 0) * dir;
            }).forEach((li) => grid.append(li));
        }));

        // header "New" / "Pre-owned" land here with a hash
        const preset = { '#new': 'New', '#used': 'Pre-owned' }[location.hash];
        if (preset) { const b = boxes.find((x) => x.name === 'condition' && x.value === preset); if (b) { b.checked = true; apply(); } }
    }

    /* ---------- lead dialog: "Check availability" / "Schedule consultation" ---------- */
    const dlg = $('#lead');
    if (dlg) {
        const form = $('#lead-form');
        let opener = null;
        const KIND = {
            availability: { label: 'Check availability', msg: (v, s) => `Is the ${v} (stock ${s}) still available?` },
            consultation: { label: 'Schedule consultation', msg: (v, s) => `I would like to schedule a consultation about the ${v} (stock ${s}).` }
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
        function close() { if (dlg.open) dlg.close(); }
        dlg.addEventListener('close', () => { window.__lenis?.start(); opener?.focus(); });
        $$('[data-lead-open]').forEach((b) => b.addEventListener('click', () => open(b)));
        $$('[data-lead-close]', dlg).forEach((b) => b.addEventListener('click', close));
        dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });   // backdrop
    }

    /* ---------- VDP: photo stage + gallery ---------- */
    const stage = $('[data-stage]');
    if (stage) {
        const photos = JSON.parse($('[data-photos]', stage).textContent);
        const img = $('[data-stage-img]', stage);
        const n = $('[data-stage-n]', stage);
        const base = img.alt.replace(/, photograph \d+ of \d+$/, '');
        const thumbs = $$('.vdp-thumb');
        let k = Number(img.dataset.start) || 0;
        function show(i) {
            k = (i + photos.length) % photos.length;
            img.src = photos[k];
            img.alt = `${base}, photograph ${k + 1} of ${photos.length}`;
            n.textContent = k + 1;
            thumbs.forEach((t, j) => t.classList.toggle('is-current', j === k));
            new Image().src = photos[(k + 1) % photos.length];   // the next one is ready when asked for
        }
        $('[data-stage-prev]', stage).addEventListener('click', () => show(k - 1));
        $('[data-stage-next]', stage).addEventListener('click', () => show(k + 1));
        stage.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') show(k - 1);
            if (e.key === 'ArrowRight') show(k + 1);
        });
        thumbs.forEach((t) => t.addEventListener('click', () => {
            show(Number(t.dataset.photo));
            const y = stage.getBoundingClientRect().top + window.scrollY - document.querySelector('[data-header]').offsetHeight - 16;
            window.__lenis ? window.__lenis.scrollTo(y) : window.scrollTo({ top: y });
        }));
        thumbs[k]?.classList.add('is-current');
        // touch swipe on the stage
        let x0 = null;
        stage.addEventListener('touchstart', (e) => { x0 = e.touches[0].clientX; }, { passive: true });
        stage.addEventListener('touchend', (e) => {
            if (x0 === null) return;
            const dx = e.changedTouches[0].clientX - x0;
            if (Math.abs(dx) > 40) show(k + (dx < 0 ? 1 : -1));
            x0 = null;
        });
        const more = $('[data-gallery-more]');
        more?.addEventListener('click', () => { $$('[data-more]').forEach((li) => { li.hidden = false; }); more.hidden = true; });
    }

    /* ---------- VDP: share ---------- */
    const share = $('[data-share]');
    if (share) {
        const status = $('[data-share-status]');
        share.addEventListener('click', async () => {
            const data = { title: document.title, url: location.href };
            try {
                if (navigator.share) { await navigator.share(data); return; }
                await navigator.clipboard.writeText(location.href);
                status.textContent = 'Link copied';
            } catch (e) {
                if (e && e.name !== 'AbortError') status.textContent = 'Copy the link from the address bar';
            }
            setTimeout(() => { status.textContent = ''; }, 3000);
        });
    }

    /* ---------- VDP: finance calculator (an estimate from the figures entered) ---------- */
    const calc = $('[data-calc]');
    if (calc) {
        const num = (el) => Number(String(el.value).replace(/[^\d.]/g, '')) || 0;
        const money = (v) => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        const out = () => {
            const loan = Math.max(0, num($('[data-calc-price]', calc)) - num($('[data-calc-down]', calc)));
            const r = num($('[data-calc-apr]', calc)) / 1200;
            const m = Number($('[data-calc-term]', calc).value);
            $('[data-calc-loan]', calc).textContent = loan ? money(loan) : '—';
            const pay = !loan ? 0 : r ? loan * r / (1 - Math.pow(1 + r, -m)) : loan / m;
            $('[data-calc-monthly]', calc).textContent = loan && $('[data-calc-apr]', calc).value !== '' ? money(pay) : '—';
        };
        calc.addEventListener('input', out);
        calc.addEventListener('submit', (e) => e.preventDefault());
        out();
    }
})();
