/* ============================================================
   LAMBORGHINI MIAMI — lead forms (v2 system)
   Every [data-lead-form] on the page: validation, error summary,
   sending (with a timeout), sent, failed. Shared by service.html
   (service request) and the inventory pages (Check availability /
   Schedule consultation). Fields and wording follow the Prestige forms.
   Without JS a form is a plain form.

   Markup contract:
     <form data-lead-form data-endpoint="" data-done="#id-of-confirmation" data-fail="…">
       [data-form-summary] [data-form-status] [data-form-submit] > [data-submit-label]
     <div id="id-of-confirmation" data-form-done> … [data-done-name] … [data-form-again]
   window.__leadForms.reset(form) returns a form to its first state.
   ============================================================ */
(() => {
    'use strict';

    const SEND_TIMEOUT = 15000;   // ms: the sending state never runs without an end
    const thisYear = new Date().getFullYear();
    const rules = {
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

    function setup(form) {
        const summary = form.querySelector('[data-form-summary]');
        const status = form.querySelector('[data-form-status]');
        const submit = form.querySelector('[data-form-submit]');
        const submitLabel = form.querySelector('[data-submit-label]');
        const idleLabel = submitLabel.textContent;
        const done = document.querySelector(form.dataset.done);
        const present = Object.keys(rules).filter((name) => form.elements[name]);

        const labelOf = (input) => (input.name === 'consent' ? 'Consent'
            : form.querySelector(`label[for="${input.id}"]`).childNodes[0].textContent.trim());

        function check(input) {
            const msg = rules[input.name](input.value, input);
            const field = input.closest('.field');
            const err = document.getElementById(input.getAttribute('aria-describedby'));
            field.classList.toggle('is-invalid', !!msg);
            input.setAttribute('aria-invalid', msg ? 'true' : 'false');
            if (err) { err.textContent = msg; err.hidden = !msg; }
            return msg;
        }

        // Validate on leaving a field; once a field has been flagged, re-check as the visitor types.
        present.forEach((name) => {
            const input = form.elements[name];
            if (input.type === 'checkbox') { input.addEventListener('change', () => { if (input.getAttribute('aria-invalid')) check(input); }); return; }
            input.addEventListener('blur', () => { if (input.value || input.getAttribute('aria-invalid')) check(input); });
            input.addEventListener('input', () => { if (input.getAttribute('aria-invalid') === 'true') check(input); });
        });

        function setBusy(busy) {
            submit.setAttribute('aria-busy', busy ? 'true' : 'false');
            submit.disabled = busy;
            submitLabel.textContent = busy ? 'Sending…' : idleLabel;
        }

        function showSent() {
            const name = form.elements.first ? form.elements.first.value.trim() : '';
            const slot = done.querySelector('[data-done-name]');
            if (slot) slot.textContent = name ? `, ${name}` : '';
            form.hidden = true;
            done.hidden = false;
            done.focus();
        }

        function reset() {
            form.reset();
            form.querySelectorAll('.field').forEach((f) => f.classList.remove('is-invalid'));
            form.querySelectorAll('[aria-invalid]').forEach((i) => i.removeAttribute('aria-invalid'));
            form.querySelectorAll('.field__error').forEach((p) => { p.hidden = true; p.textContent = ''; });
            summary.hidden = true;
            status.textContent = '';
            done.hidden = true;
            form.hidden = false;
        }
        form.__reset = reset;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            status.textContent = '';
            const errors = present
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
                status.textContent = form.dataset.fail || 'Your request could not be sent. Please try again.';
            } finally {
                clearTimeout(timer);
                setBusy(false);
            }
        });

        done.querySelector('[data-form-again]')?.addEventListener('click', () => {
            reset();
            (form.elements.first || form.querySelector('input'))?.focus();
        });
    }

    document.querySelectorAll('[data-lead-form]').forEach(setup);
    window.__leadForms = { reset: (form) => form.__reset && form.__reset() };
})();
