/* ============================================================
   LAMBORGHINI MIAMI — main.js
   Lenis (DNA90) · header hide/solid · menu overlay · reveals.
   The page is complete without this file: every hidden state is
   scoped to html.js, and html.js is only set when scripts run.
   ============================================================ */
(() => {
    'use strict';

    const root = document.documentElement;
    if (root.classList.contains('figma')) return; // static capture mode — see index.html
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    /* ---------- Lenis — never constructed under reduced motion ---------- */
    let lenis = null;
    function startLenis() {
        if (lenis || reduceMotion.matches || typeof window.Lenis !== 'function') return;
        lenis = new window.Lenis({
            autoRaf: true,              // no GSAP on this page, so Lenis owns its loop
            anchors: true,             // honours each target's scroll-margin-top (= header height)
            allowNestedScroll: true,
            stopInertiaOnNavigate: true
        });
        window.__lenis = lenis;          // exposed for verification scripts (DNA90)
    }
    function stopLenis() {
        if (!lenis) return;
        lenis.destroy();
        lenis = null;
        window.__lenis = null;
    }
    startLenis();
    reduceMotion.addEventListener('change', () => (reduceMotion.matches ? stopLenis() : startLenis()));

    /* ---------- Header: persistent; goes solid once it has left the hero ----------
       User direction: the header never hides (DESIGN_SYSTEM.md §4 overrides the
       corporate .to-hide pattern). Only its ground changes. */
    const header = document.querySelector('[data-header]');
    const hero = document.querySelector('.hero');
    let ticking = false;

    const photoChapters = [...document.querySelectorAll('.adp')];
    function updateHeader() {
        ticking = false;
        if (!header) return;
        const h = header.offsetHeight;
        const y = window.scrollY;
        // >= : an anchor landing exactly at the end of the hero (#range) must
        // already read as solid. Sub-pixel rounding gets one pixel of slack.
        const heroEnd = hero ? hero.offsetTop + hero.offsetHeight - h : 0;
        // Over a full-bleed photographic chapter the header keeps the hero's
        // gradient treatment instead of an opaque bar across the photograph.
        const overPhoto = photoChapters.some((el) => {
            const r = el.getBoundingClientRect();
            return r.top <= 1 && r.bottom > h + 1;
        });
        header.classList.toggle('is-solid', y >= heroEnd - 1 && !overPhoto);
    }
    window.addEventListener('scroll', () => {
        if (!ticking) { ticking = true; requestAnimationFrame(updateHeader); }
    }, { passive: true });
    window.addEventListener('resize', updateHeader, { passive: true });
    updateHeader();

    /* ---------- Menu overlay ---------- */
    const menu = document.querySelector('[data-menu]');
    const openBtn = document.querySelector('[data-menu-open]');
    const closeBtn = menu?.querySelector('[data-menu-close]');

    function focusables() {
        return [...menu.querySelectorAll('a[href], button:not([disabled])')].filter((el) => el.offsetParent !== null);
    }
    function openMenu() {
        if (!menu) return;
        menu.hidden = false;
        requestAnimationFrame(() => menu.classList.add('is-open'));
        openBtn.setAttribute('aria-expanded', 'true');
        root.style.overflow = 'hidden';
        lenis?.stop();
        closeBtn?.focus();
    }
    function closeMenu(returnFocus = true) {
        if (!menu || menu.hidden) return;
        menu.classList.remove('is-open');
        openBtn.setAttribute('aria-expanded', 'false');
        root.style.overflow = '';
        lenis?.start();
        const done = () => { menu.hidden = true; };
        if (reduceMotion.matches) done(); else setTimeout(done, 300);
        if (returnFocus) openBtn.focus();
    }
    openBtn?.addEventListener('click', openMenu);
    closeBtn?.addEventListener('click', () => closeMenu());
    menu?.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') { e.preventDefault(); closeMenu(); return; }
        if (e.key !== 'Tab') return;
        const items = focusables();
        const first = items[0];
        const last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    // In-page links close the menu, then travel.
    menu?.querySelectorAll('[data-menu-link]').forEach((link) => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (!target) return;
            e.preventDefault();
            closeMenu(false);
            if (lenis) lenis.scrollTo(target);
            else target.scrollIntoView();
            target.setAttribute('tabindex', '-1');
            target.focus({ preventScroll: true });
        });
    });

    /* ---------- Text rise (user direction, Alex): every text element rises into
       place as it enters. Text only — images, cards and grounds stay put.
       Hidden states exist only under html.js + no reduced motion (CSS), and
       every element is released by at least one of: the observer, an anchor
       jump into its section, keyboard focus, or the safety sweep. ---------- */
    const RISE_SEL = [
        'main h2', 'main h3', 'main h4', 'main p', 'main dt', 'main dd',
        'main figcaption', 'main address', 'main .btn',
        '.site-footer p', '.site-footer li', '.site-footer .btn'
    ].join(',');
    const STEP = 70, CAP = 400, DUR = 700;           // mirror of --rise-step, --rise-cap, --dur-rise
    const risers = [...document.querySelectorAll(RISE_SEL)].filter((el) =>
        !el.closest('.hero') && !el.parentElement.closest(RISE_SEL));

    function settle(el) {            // hand the element back to its own transitions (hover etc.)
        el.classList.remove('rv', 'rv--sm', 'is-in');
        el.style.removeProperty('--rv-delay');
    }
    function release(list, stagger, base = 0) {
        list.forEach((el, i) => {
            if (!el.classList.contains('rv') || el.classList.contains('is-in')) return;
            const delay = base + (stagger ? Math.min(i * STEP, CAP) : 0);
            el.style.setProperty('--rv-delay', delay + 'ms');
            el.classList.add('is-in');
            setTimeout(() => settle(el), DUR + delay + 60);
        });
    }

    if (!reduceMotion.matches && 'IntersectionObserver' in window) {
        risers.forEach((el) => {
            el.classList.add('rv');
            if (parseFloat(getComputedStyle(el).fontSize) < 20) el.classList.add('rv--sm');
        });
        const io = new IntersectionObserver((entries) => {
            const batch = entries.filter((e) => e.isIntersecting).map((e) => e.target)
                .sort((x, y) => x.getBoundingClientRect().top - y.getBoundingClientRect().top
                              || x.getBoundingClientRect().left - y.getBoundingClientRect().left);
            batch.forEach((el) => io.unobserve(el));
            release(batch, true);
        }, { threshold: 0.15, rootMargin: '0px 0px 8% 0px' });
        // Text inside a model tile is released by its car (drive-in, below), not by this observer.
        risers.forEach((el) => { if (!el.closest('.model')) io.observe(el); });

        /* ---------- Model drive-in (user direction, Alex; DESIGN_SYSTEM §8) ----------
           Each car rolls in from the left and decelerates into place as its tile
           enters; the tile's text follows DRIVE_LAG later with the ordinary rise.
           The image is decoded before the drive starts, so it never pops in blank. */
        const DRIVE = 1250, DRIVE_STEP = 135, DRIVE_LAG = 200;   // mirror of --dur-drive, --drive-stagger, --drive-text-lag
        const tiles = [...document.querySelectorAll('.model')];
        const ready = new Map();                                  // tile -> Promise(decoded)
        function prepare(tile) {
            if (ready.has(tile)) return ready.get(tile);
            const img = tile.querySelector('.model__car');
            img.loading = 'eager';
            const decoded = (img.complete && img.naturalWidth ? Promise.resolve() : new Promise((r) => {
                img.addEventListener('load', r, { once: true }); img.addEventListener('error', r, { once: true });
            })).then(() => img.decode && img.decode()).catch(() => {});
            // never hold a car back for more than a moment
            const p = Promise.race([decoded, new Promise((r) => setTimeout(r, 1200))]);
            ready.set(tile, p);
            return p;
        }
        function drive(tile, delay) {
            if (tile.dataset.driven) return;
            tile.dataset.driven = '1';
            prepare(tile).then(() => requestAnimationFrame(() => {
                tile.style.setProperty('--dv-delay', delay + 'ms');
                tile.classList.add('is-driven');
                release([...tile.querySelectorAll('.rv')], true, delay + DRIVE_LAG);
                setTimeout(() => {                                   // hand the car back to its hover transition
                    tile.classList.remove('dv', 'is-driven');
                    tile.style.removeProperty('--dv-delay');
                }, DRIVE + delay + 60);
            }));
        }
        function driveRows(list) {                                   // left tile first, per row
            list.sort((x, y) => x.getBoundingClientRect().top - y.getBoundingClientRect().top
                              || x.getBoundingClientRect().left - y.getBoundingClientRect().left);
            let rowTop = null, i = 0;
            list.forEach((t) => {
                const top = Math.round(t.getBoundingClientRect().top);
                if (rowTop === null || Math.abs(top - rowTop) > 8) { rowTop = top; i = 0; }
                drive(t, i++ * DRIVE_STEP);
            });
        }
        tiles.forEach((t) => t.classList.add('dv'));
        const prep = new IntersectionObserver((entries) => entries.forEach((e) => {
            if (e.isIntersecting) { prepare(e.target.closest('.model')); prep.unobserve(e.target); }
        }), { rootMargin: '0px 0px 60% 0px' });
        const dio = new IntersectionObserver((entries) => {
            const batch = entries.filter((e) => e.isIntersecting).map((e) => e.target.closest('.model'));
            entries.forEach((e) => { if (e.isIntersecting) dio.unobserve(e.target); });
            if (batch.length) driveRows(batch);
        }, { threshold: 0.3 });
        tiles.forEach((t) => { const m = t.querySelector('.model__media'); prep.observe(m); dio.observe(m); });
        window.__drive = { tiles, drive };                       // exposed for verification scripts

        // Anchor jumps: everything in the destination section is released at once,
        // so a section never lands blank under the header.
        document.addEventListener('click', (e) => {
            const a = e.target.closest('a[href^="#"]');
            const target = a && a.getAttribute('href').length > 1 && document.querySelector(a.getAttribute('href'));
            if (!target) return;
            const scope = target.closest('section') || target;
            release([...scope.querySelectorAll('.rv')].filter((el) => !el.closest('.model.dv')), false);
            const inScope = tiles.filter((t) => scope.contains(t) || t.contains(scope));
            if (inScope.length) driveRows(inScope);
        });
        // Keyboard focus never waits for choreography.
        document.addEventListener('focusin', (e) => {
            const tile = e.target.closest('.model');
            if (tile) drive(tile, 0);
            const el = e.target.closest('.rv') || e.target.querySelector?.('.rv');
            if (el) release([el], false);
        });
        // Safety sweep: anything already on screen that the observer missed.
        const sweep = () => {
            driveRows(tiles.filter((t) => {                            // same bar as the observer: 30% of the car in view, or already passed
                if (t.dataset.driven) return false;
                const r = t.querySelector('.model__media').getBoundingClientRect();
                return r.bottom < 0 || Math.min(r.bottom, innerHeight) - Math.max(r.top, 0) >= 0.3 * r.height;
            }));
            release(risers.filter((el) => {
                if (!el.classList.contains('rv') || el.classList.contains('is-in') || el.closest('.model.dv')) return false;
                const r = el.getBoundingClientRect();
                return r.top < innerHeight && r.bottom > 0;
            }), false);
        };
        window.addEventListener('load', () => setTimeout(sweep, 1500));
        let sweepT;
        window.addEventListener('scroll', () => { clearTimeout(sweepT); sweepT = setTimeout(sweep, 400); }, { passive: true });
    }

    /* ---------- Hero slider (user direction, Alex): corporate claim-led carousel.
       Crossfade, text rises in on each slide, autoplay with visible progress and a
       pause control; pauses on hover, focus within, hidden tab and off-screen; no
       autoplay under reduced motion. Slide 1 is the LCP; others load when idle. ---------- */
    const heroEl = document.querySelector('[data-hero]');
    const slides = heroEl ? [...heroEl.querySelectorAll('[data-slide]')] : [];
    if (slides.length > 1) {
        const HOLD = 6500;                                   // mirror of --slide-hold
        const dots = [...heroEl.querySelectorAll('[data-go]')];
        const toggle = heroEl.querySelector('[data-toggle]');
        const live = heroEl.querySelector('[data-hero-live]');
        let idx = 0, elapsed = 0, last = 0, raf = 0;
        let userPaused = reduceMotion.matches, hovering = false, focusWithin = false, inView = true;

        const loadSlide = (s) => s.querySelectorAll('[data-srcset],[data-src]').forEach((el) => {
            if (el.dataset.srcset) { el.srcset = el.dataset.srcset; el.removeAttribute('data-srcset'); }
            if (el.dataset.src) { el.src = el.dataset.src; el.removeAttribute('data-src'); }
        });
        const idle = window.requestIdleCallback || ((f) => setTimeout(f, 1200));
        window.addEventListener('load', () => idle(() => slides.slice(1).forEach(loadSlide)));

        slides.forEach((s, i) => { if (i) { s.inert = true; s.setAttribute('aria-hidden', 'true'); } });

        const playing = () => !userPaused && !hovering && !focusWithin && !document.hidden && inView;
        function paint() { dots[idx]?.style.setProperty('--progress', Math.min(elapsed / HOLD, 1)); }
        function tick(t) {
            raf = 0;
            if (!playing()) { last = 0; return; }
            if (last) elapsed += t - last;
            last = t;
            if (elapsed >= HOLD) { go(idx + 1, false); return; }
            paint();
            raf = requestAnimationFrame(tick);
        }
        function run() { if (!raf && playing()) { last = 0; raf = requestAnimationFrame(tick); } }

        function go(n, byUser) {
            n = (n + slides.length) % slides.length;
            if (n === idx) return;
            loadSlide(slides[n]);
            const from = slides[idx], to = slides[n];
            from.classList.remove('is-active'); from.inert = true; from.setAttribute('aria-hidden', 'true');
            to.classList.add('is-active'); to.inert = false; to.removeAttribute('aria-hidden');
            dots[idx]?.removeAttribute('aria-current'); dots[idx]?.style.setProperty('--progress', 0);
            dots[n]?.setAttribute('aria-current', 'true');
            idx = n; elapsed = 0; paint();
            if (byUser || !playing()) live.textContent = to.getAttribute('aria-label');
            if (raf) { cancelAnimationFrame(raf); raf = 0; }
            run();
        }
        function setPaused(p) {
            userPaused = p;
            toggle.setAttribute('aria-label', p ? 'Play slideshow' : 'Pause slideshow');
            toggle.querySelector('use').setAttribute('href', p ? '#i-play' : '#i-pause');
            live.setAttribute('aria-live', p ? 'polite' : 'off');
            run();
        }
        setPaused(userPaused);

        heroEl.querySelector('[data-prev]').addEventListener('click', () => go(idx - 1, true));
        heroEl.querySelector('[data-next]').addEventListener('click', () => go(idx + 1, true));
        dots.forEach((d) => d.addEventListener('click', () => go(+d.dataset.go, true)));
        toggle.addEventListener('click', () => setPaused(!userPaused));
        heroEl.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1, true); }
            if (e.key === 'ArrowLeft') { e.preventDefault(); go(idx - 1, true); }
        });
        heroEl.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') { hovering = true; } });
        heroEl.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') { hovering = false; run(); } });
        heroEl.addEventListener('focusin', () => { focusWithin = true; live.setAttribute('aria-live', 'polite'); });
        heroEl.addEventListener('focusout', (e) => {
            if (!heroEl.contains(e.relatedTarget)) { focusWithin = false; live.setAttribute('aria-live', userPaused ? 'polite' : 'off'); run(); }
        });
        document.addEventListener('visibilitychange', run);
        if ('IntersectionObserver' in window) {
            new IntersectionObserver(([e]) => { inView = e.isIntersecting; run(); }, { threshold: 0.35 }).observe(heroEl);
        }
        // swipe: horizontal only; vertical movement stays with the page (touch-action: pan-y)
        let sx = 0, sy = 0, tracking = false;
        const track = heroEl.querySelector('[data-hero-track]');
        track.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse') { tracking = true; sx = e.clientX; sy = e.clientY; } });
        track.addEventListener('pointerup', (e) => {
            if (!tracking) return; tracking = false;
            const dx = e.clientX - sx, dy = e.clientY - sy;
            if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(idx + (dx < 0 ? 1 : -1), true);
        });
        track.addEventListener('pointercancel', () => { tracking = false; });
        window.__hero = { go: (n) => go(n, true), get index() { return idx; }, pause: () => setPaused(true) };
        run();
    }

    /* ---------- Hero subject box, published for the composition audit ----------
       The car's box inside the rendered photograph, as fractions of the image
       (DESIGN_SYSTEM.md §6). Read-only; nothing on the page depends on it. */
    function publishSubject() {
        const img = document.querySelector('.hero__img');
        if (!img) return;
        const src = img.currentSrc || '';
        const key = /night-p/.test(src) ? 'subjectNight' : /-m-\d+\./.test(src) ? 'subjectTall' : 'subjectWide';
        const f = (img.dataset[key] || '').split(',').map(Number);
        if (f.length !== 4) return;
        let r = img.getBoundingClientRect();
        // measure the drawn picture, not the element box, for contain and cover
        const fit = getComputedStyle(img).objectFit;
        if ((fit === 'contain' || fit === 'cover') && img.naturalWidth) {
            const pick = fit === 'contain' ? Math.min : Math.max;
            const k = pick(r.width / img.naturalWidth, r.height / img.naturalHeight);
            const w = img.naturalWidth * k, hgt = img.naturalHeight * k;
            const pos = getComputedStyle(img).objectPosition.split(' ').map((v) => parseFloat(v) / 100);
            r = { left: r.left + (r.width - w) * pos[0], top: r.top + (r.height - hgt) * pos[1], width: w, height: hgt };
        }
        window.__subject = {
            label: 'Temerario (photograph)',
            left: r.left + f[0] * r.width, top: r.top + f[1] * r.height,
            right: r.left + (f[0] + f[2]) * r.width, bottom: r.top + (f[1] + f[3]) * r.height
        };
    }
    window.addEventListener('load', publishSubject);
    window.addEventListener('resize', publishSubject, { passive: true });

    /* ---------- Hero entrance: after the face is ready, so lines never re-set ---------- */
    const heroImg = document.querySelector('.hero__img');
    const imgReady = heroImg && !heroImg.complete
        ? new Promise((r) => { heroImg.addEventListener('load', r, { once: true }); heroImg.addEventListener('error', r, { once: true }); })
        : Promise.resolve();
    const fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
    const timeout = new Promise((r) => setTimeout(r, 1200));
    Promise.race([Promise.all([fontsReady, imgReady]), timeout]).then(() => root.classList.add('is-loaded'));
})();
