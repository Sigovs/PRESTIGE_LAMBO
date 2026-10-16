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
