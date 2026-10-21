/* v3 model pages (Oct 2026). The sales enquiry form, with the service form's states (idle,
   invalid with inline messages and a summary, sending, sent, failed); it posts to
   data-endpoint once one exists and until then confirms locally (NOT connected: the client's
   DriveCentric campaign comes later). And the YouTube film, loaded only when asked for. */
(() => {
    const SEND_TIMEOUT = 15000;
    const form = document.querySelector('[data-enquire-form]');
    if (form) {
        const summary = form.querySelector('[data-form-summary]');
        const status = form.querySelector('[data-form-status]');
        const submit = form.querySelector('[data-form-submit]');
        const submitLabel = form.querySelector('[data-submit-label]');
        const done = document.querySelector('[data-form-done]');
        const rules = {
            first: (v) => (v.trim() ? '' : 'Enter your first name.'),
            last: (v) => (v.trim() ? '' : 'Enter your last name.'),
            email: (v) => (!v.trim() ? 'Enter your email address.'
                : /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) ? '' : 'Enter an email address like name@example.com.'),
            phone: (v) => (!v.trim() ? 'Enter your phone number.'
                : v.replace(/\D/g, '').length >= 10 ? '' : 'Enter a phone number with at least 10 digits.'),
            consent: (v, input) => (input.checked ? '' : 'Tick the box to agree to being contacted.')
        };
        const labelOf = (input) => (input.name === 'consent' ? 'Consent'
            : form.querySelector(`label[for="${input.id}"]`).childNodes[0].textContent.trim());
        const check = (input) => {
            const msg = rules[input.name](input.value, input);
            const err = document.getElementById(input.getAttribute('aria-describedby'));
            input.closest('.field').classList.toggle('is-invalid', !!msg);
            input.setAttribute('aria-invalid', msg ? 'true' : 'false');
            if (err) { err.textContent = msg; err.hidden = !msg; }
            return msg;
        };
        Object.keys(rules).forEach((name) => {
            const input = form.elements[name];
            if (input.type === 'checkbox') { input.addEventListener('change', () => { if (input.getAttribute('aria-invalid')) check(input); }); return; }
            input.addEventListener('blur', () => { if (input.value || input.getAttribute('aria-invalid')) check(input); });
            input.addEventListener('input', () => { if (input.getAttribute('aria-invalid') === 'true') check(input); });
        });
        const setBusy = (busy) => {
            submit.setAttribute('aria-busy', busy ? 'true' : 'false');
            submit.disabled = busy;
            submitLabel.textContent = busy ? 'Sending…' : 'Send enquiry';
        };
        const showSent = () => {
            const name = form.elements.first.value.trim();
            done.querySelector('[data-done-name]').textContent = name ? `, ${name}` : '';
            form.hidden = true;
            done.hidden = false;
            done.focus();
        };
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            status.textContent = '';
            const errors = Object.keys(rules).map((name) => ({ input: form.elements[name], msg: check(form.elements[name]) })).filter((x) => x.msg);
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
                status.textContent = 'Your enquiry could not be sent. Please try again, or call sales on (833) 290-5147.';
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
    }

    /* the film: a poster until asked for, then YouTube (no-cookie) with sound, in place */
    document.querySelectorAll('[data-yt]').forEach((box) => {
        box.querySelector('[data-yt-play]').addEventListener('click', () => {
            const f = document.createElement('iframe');
            f.src = `https://www.youtube-nocookie.com/embed/${box.dataset.yt}?autoplay=1&rel=0`;
            f.title = box.dataset.ytTitle;
            f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
            f.allowFullscreen = true;
            box.append(f);
            box.classList.add('is-playing');
            f.focus();
        });
    });
})();
