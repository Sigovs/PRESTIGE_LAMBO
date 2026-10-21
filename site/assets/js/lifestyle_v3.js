/* v3 Lifestyle page (Oct 2026). The hero loop: armed after load, its file chosen for the
   frame, playing only while on screen and the tab is visible; reduced motion keeps the
   poster. The film lightbox: every [data-film-open] opens it, with the client's file
   (data-src, streamed from their Dropbox) or a YouTube embed (data-yt, no-cookie); the page
   does not scroll while it is open; Esc, the close button or a click on the black close it,
   and focus returns to the button that opened it. */
(() => {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const portrait = window.matchMedia('(max-width: 1199.98px) and (orientation: portrait)').matches;
    const root = document.documentElement;

    const loop = document.querySelector('[data-loop]');
    if (loop) {
        if (portrait && loop.dataset.posterM) loop.poster = loop.dataset.posterM;
        let inView = true, open = false;
        const sync = () => {
            if (reduce || !loop.getAttribute('src')) return;
            if (inView && !open && !document.hidden) loop.play().catch(() => {}); else if (!loop.paused) loop.pause();
        };
        const arm = () => { if (reduce) return; loop.src = portrait ? loop.dataset.srcM : loop.dataset.srcD; sync(); };
        loop.addEventListener('canplay', sync);
        window.addEventListener('load', () => setTimeout(arm, 300));
        if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { inView = e.isIntersecting; sync(); }, { threshold: 0.01 }).observe(loop);
        document.addEventListener('visibilitychange', sync);
        window.__lifestyleLoop = { hold: (v) => { open = v; sync(); } };
    }

    const dlg = document.querySelector('[data-film]');
    const stage = dlg && dlg.querySelector('[data-film-stage]');
    if (!dlg || !stage || !dlg.showModal) return;
    let opener = null;
    const shut = () => {
        stage.querySelector('video')?.pause();
        dlg.classList.remove('is-open');
        setTimeout(() => { if (dlg.open) dlg.close(); stage.innerHTML = ''; opener?.focus({ preventScroll: true }); }, reduce ? 0 : 300);
        root.classList.remove('is-film');
        window.__lenis?.start();
        window.__lifestyleLoop?.hold(false);
    };
    document.querySelectorAll('[data-film-open]').forEach((btn) => btn.addEventListener('click', () => {
        opener = btn;
        stage.innerHTML = '';
        dlg.setAttribute('aria-label', btn.dataset.filmTitle || 'Film');
        if (btn.dataset.yt) {
            const f = document.createElement('iframe');
            f.className = 'film__v';
            f.src = `https://www.youtube-nocookie.com/embed/${btn.dataset.yt}?autoplay=1&rel=0`;
            f.title = btn.dataset.filmTitle || 'Film';
            f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
            f.allowFullscreen = true;
            stage.append(f);
        } else {
            const v = document.createElement('video');
            v.className = 'film__v';
            v.controls = true; v.playsInline = true; v.preload = 'auto';
            if (btn.dataset.poster) v.poster = btn.dataset.poster;
            v.src = btn.dataset.src;
            stage.append(v);
            v.play().catch(() => {});
        }
        window.__lifestyleLoop?.hold(true);
        window.__lenis?.stop();
        root.classList.add('is-film');
        dlg.showModal();
        requestAnimationFrame(() => dlg.classList.add('is-open'));
    }));
    dlg.querySelector('[data-film-close]').addEventListener('click', shut);
    dlg.addEventListener('cancel', (e) => { e.preventDefault(); shut(); });
    dlg.addEventListener('click', (e) => { if (e.target === dlg) shut(); });
})();
