/* ============================================================
   LAMBORGHINI MIAMI — main.js
   Lenis (DNA90) · header hide/solid · menu overlay · reveals.
   The page is complete without this file: every hidden state is
   scoped to html.js, and html.js is only set when scripts run.
   ============================================================ */
(() => {
    'use strict';

    const root = document.documentElement;
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

    /* ---------- Reveals: once, at 15% visible ---------- */
    const revealed = document.querySelectorAll('[data-reveal]');
    if ('IntersectionObserver' in window && !reduceMotion.matches) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-in');
                io.unobserve(entry.target);
            });
        }, { threshold: 0.15, rootMargin: '0px 0px -5% 0px' });
        revealed.forEach((el) => io.observe(el));
    } else {
        revealed.forEach((el) => el.classList.add('is-in'));
    }

    /* ---------- Hero subject box, published for the composition audit ----------
       The car's box inside the rendered photograph, as fractions of the image
       (DESIGN_SYSTEM.md §6). Read-only; nothing on the page depends on it. */
    function publishSubject() {
        const img = document.querySelector('.hero__img');
        if (!img) return;
        const tall = /-m-\d+\./.test(img.currentSrc || '');
        const f = (img.dataset[tall ? 'subjectTall' : 'subjectWide'] || '').split(',').map(Number);
        if (f.length !== 4) return;
        let r = img.getBoundingClientRect();
        // with object-fit: contain (portrait layouts) measure the drawn picture,
        // not the letterboxed element box; object-position is 50% 100%
        if (getComputedStyle(img).objectFit === 'contain' && img.naturalWidth) {
            const k = Math.min(r.width / img.naturalWidth, r.height / img.naturalHeight);
            const w = img.naturalWidth * k, hgt = img.naturalHeight * k;
            r = { left: r.left + (r.width - w) / 2, top: r.bottom - hgt, width: w, height: hgt };
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
