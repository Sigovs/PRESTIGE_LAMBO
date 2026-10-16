/* ============================================================
   LAMBORGHINI MIAMI — service page (service.html)
   Service request form (every state: idle, invalid, sending, sent,
   failed) and the location map. main_v2.js carries Lenis, the header,
   the menu and the text staircase. Without JS the form is a plain
   form and the map box stays empty; the address is printed beside it.
   ============================================================ */
(() => {
    'use strict';

    /* ---------- Service request form ---------- */
    const form = document.querySelector('[data-service-form]');
    if (form) {
        const summary = form.querySelector('[data-form-summary]');
        const status = form.querySelector('[data-form-status]');
        const submit = form.querySelector('[data-form-submit]');
        const submitLabel = form.querySelector('[data-submit-label]');
        const done = document.querySelector('[data-form-done]');
        const SEND_TIMEOUT = 15000;   // ms: the sending state never runs without an end
        const thisYear = new Date().getFullYear();

        const rules = {
            // fields and wording follow the Prestige Imports forms (first/last name, phone required,
            // preferred contact, the contact consent)
            first: (v) => (v.trim() ? '' : 'Enter your first name.'),
            last: (v) => (v.trim() ? '' : 'Enter your last name.'),
            email: (v) => (!v.trim() ? 'Enter your email address.'
                : /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? '' : 'Enter an email address like name@example.com.'),
            phone: (v) => (!v.trim() ? 'Enter your phone number.'
                : v.replace(/\D/g, '').length >= 10 ? '' : 'Enter a phone number with at least 10 digits.'),
            year: (v) => {
                if (!v.trim()) return '';
                const y = Number(v);
                return /^\d{4}$/.test(v.trim()) && y >= 1963 && y <= thisYear + 1 ? '' : `Enter a four-digit year between 1963 and ${thisYear + 1}.`;
            },
            consent: (v, input) => (input.checked ? '' : 'Tick the box to agree to being contacted.')
        };
        const labelOf = (input) => (input.name === 'consent' ? 'Consent'
            : form.querySelector(`label[for="${input.id}"]`).childNodes[0].textContent.trim());

        function check(input) {
            const rule = rules[input.name];
            if (!rule) return '';
            const msg = rule(input.value, input);
            const field = input.closest('.field');
            const err = document.getElementById(input.getAttribute('aria-describedby'));
            field.classList.toggle('is-invalid', !!msg);
            input.setAttribute('aria-invalid', msg ? 'true' : 'false');
            if (err) { err.textContent = msg; err.hidden = !msg; }
            return msg;
        }

        // Validate on leaving a field; once a field has been flagged, re-check as the visitor types.
        Object.keys(rules).forEach((name) => {
            const input = form.elements[name];
            if (input.type === 'checkbox') { input.addEventListener('change', () => { if (input.getAttribute('aria-invalid')) check(input); }); return; }
            input.addEventListener('blur', () => { if (input.value || input.getAttribute('aria-invalid')) check(input); });
            input.addEventListener('input', () => { if (input.getAttribute('aria-invalid') === 'true') check(input); });
        });

        function setBusy(busy) {
            submit.setAttribute('aria-busy', busy ? 'true' : 'false');
            submit.disabled = busy;
            submitLabel.textContent = busy ? 'Sending…' : 'Send request';
        }

        function showSent() {
            const name = form.elements.first.value.trim();
            done.querySelector('[data-done-name]').textContent = name ? `, ${name}` : '';
            form.hidden = true;
            done.hidden = false;
            done.focus();
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            status.textContent = '';
            const errors = Object.keys(rules)
                .map((name) => ({ input: form.elements[name], msg: check(form.elements[name]) }))
                .filter((x) => x.msg);
            if (errors.length) {
                summary.innerHTML = '';
                const head = document.createElement('strong');
                head.textContent = errors.length === 1 ? 'One field needs attention:' : `${errors.length} fields need attention:`;
                const list = document.createElement('ul');
                errors.forEach(({ input, msg }) => {
                    const li = document.createElement('li');
                    const a = document.createElement('a');
                    a.href = `#${input.id}`;
                    a.textContent = `${labelOf(input)}: ${msg}`;
                    a.addEventListener('click', (ev) => { ev.preventDefault(); input.focus(); });
                    li.append(a);
                    list.append(li);
                });
                summary.append(head, list);
                summary.hidden = false;
                summary.focus();
                return;
            }
            summary.hidden = true;

            // The platform (All Auto Network) supplies the endpoint; until then the request
            // is confirmed locally so every state can be reviewed.
            const endpoint = form.dataset.endpoint;
            if (!endpoint) { showSent(); return; }

            setBusy(true);
            const ctrl = new AbortController();
            const timer = setTimeout(() => ctrl.abort(), SEND_TIMEOUT);
            try {
                const res = await fetch(endpoint, { method: 'POST', body: new FormData(form), signal: ctrl.signal });
                if (!res.ok) throw new Error(String(res.status));
                showSent();
            } catch (err) {
                // the visitor's input stays in the form; the failure is said, never shown as success
                status.textContent = 'Your request could not be sent. Please try again, or call service on (833) 290-5148.';
            } finally {
                clearTimeout(timer);
                setBusy(false);
            }
        });

        document.querySelector('[data-form-again]')?.addEventListener('click', () => {
            form.reset();
            form.querySelectorAll('.field').forEach((f) => f.classList.remove('is-invalid'));
            form.querySelectorAll('[aria-invalid]').forEach((i) => i.removeAttribute('aria-invalid'));
            form.querySelectorAll('.field__error').forEach((p) => { p.hidden = true; p.textContent = ''; });
            done.hidden = true;
            form.hidden = false;
            form.elements.first.focus();
        });

        // "Arrange pickup" ticks the pickup box on its way to the form.
        document.querySelectorAll('[data-prefill="pickup"]').forEach((a) => a.addEventListener('click', () => {
            const box = form.elements.pickup;
            if (box) box.checked = true;
        }));
    }

    /* ---------- Map: Leaflet + OpenStreetMap, as on the Prestige Imports service page ---------- */
    function initMap() {
        const el = document.getElementById('service-map');
        if (!el || typeof window.L === 'undefined' || el.dataset.ready) return;
        el.dataset.ready = '1';
        const L = window.L;
        const coords = [25.913485, -80.15750349];   // JSON-LD geo, lamborghinimiami.com
        const touch = window.matchMedia('(pointer: coarse)').matches;
        const map = L.map(el, {
            scrollWheelZoom: false,   // the wheel stays with the page (Lenis)
            dragging: !touch,         // one finger scrolls the page on phones; zoom buttons still work
            tap: false,
            attributionControl: true
        }).setView(coords, 16);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
        map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');   // no flag: the page carries no other hue
        L.marker(coords, {
            icon: L.divIcon({ className: '', html: '<span class="map-pin"></span>', iconSize: [24, 24], iconAnchor: [12, 12] }),
            title: 'Lamborghini Miami',
            alt: 'Lamborghini Miami'
        }).addTo(map);
    }
    // Leaflet loads deferred, before this file; build the map when it comes near the screen.
    const mapEl = document.getElementById('service-map');
    if (mapEl && 'IntersectionObserver' in window) {
        const mio = new IntersectionObserver((entries) => {
            if (entries.some((e) => e.isIntersecting)) { mio.disconnect(); initMap(); }
        }, { rootMargin: '400px 0px' });
        mio.observe(mapEl);
    } else initMap();
})();
