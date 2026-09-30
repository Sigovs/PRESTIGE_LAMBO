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
            anchors: true,
            allowNestedScroll: true,
            stopInertiaOnNavigate: true
        });
    }
    function stopLenis() {
        if (!lenis) return;
        lenis.destroy();
        lenis = null;
    }
    startLenis();
    reduceMotion.addEventListener('change', () => (reduceMotion.matches ? stopLenis() : startLenis()));

    /* ---------- Header: solid after the hero, hide on scroll-down ---------- */
    const header = document.querySelector('[data-header]');
    const hero = document.querySelector('.hero');
    let lastY = window.scrollY;
    let ticking = false;
    let menuOpen = false;

    function updateHeader() {
        ticking = false;
        if (!header) return;
        const y = window.scrollY;
        const h = header.offsetHeight;
        const heroEnd = hero ? hero.offsetTop + hero.offsetHeight - h : 0;

        // Solid only once the header has left the hero — an opaque bar never
        // cuts across the hero's live scene.
        header.classList.toggle('is-solid', y > heroEnd);

        // Hide on scroll-down past the first screen; reveal on any scroll-up.
        if (!menuOpen && !reduceMotion.matches) {
            const delta = y - lastY;
            if (y > h * 2 && delta > 4) header.classList.add('is-hidden');
            else if (delta < -4 || y <= h) header.classList.remove('is-hidden');
        } else {
            header.classList.remove('is-hidden');
        }
        lastY = y;
    }
    window.addEventListener('scroll', () => {
        if (!ticking) { ticking = true; requestAnimationFrame(updateHeader); }
    }, { passive: true });
    window.addEventListener('resize', updateHeader, { passive: true });
    updateHeader();

    // Keyboard focus inside a hidden header brings it back.
    header?.addEventListener('focusin', () => header.classList.remove('is-hidden'));

    /* ---------- Menu overlay ---------- */
    const menu = document.querySelector('[data-menu]');
    const openBtn = document.querySelector('[data-menu-open]');
    const closeBtn = menu?.querySelector('[data-menu-close]');

    function focusables() {
        return [...menu.querySelectorAll('a[href], button:not([disabled])')].filter((el) => el.offsetParent !== null);
    }
    function openMenu() {
        if (!menu) return;
        menuOpen = true;
        menu.hidden = false;
        requestAnimationFrame(() => menu.classList.add('is-open'));
        openBtn.setAttribute('aria-expanded', 'true');
        root.style.overflow = 'hidden';
        lenis?.stop();
        closeBtn?.focus();
    }
    function closeMenu(returnFocus = true) {
        if (!menu || menu.hidden) return;
        menuOpen = false;
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

    /* ---------- Hero entrance: after the face is ready, so lines never re-set ---------- */
    const heroImg = document.querySelector('.hero__img');
    const imgReady = heroImg && !heroImg.complete
        ? new Promise((r) => { heroImg.addEventListener('load', r, { once: true }); heroImg.addEventListener('error', r, { once: true }); })
        : Promise.resolve();
    const fontsReady = document.fonts ? document.fonts.ready : Promise.resolve();
    const timeout = new Promise((r) => setTimeout(r, 1200));
    Promise.race([Promise.all([fontsReady, imgReady]), timeout]).then(() => root.classList.add('is-loaded'));
})();
