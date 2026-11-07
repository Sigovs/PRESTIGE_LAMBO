/* LAMBORGHINI MIAMI — About and Our Story (about.html, our-story.html), after main_v2.js.
   The held film of the archive (Our Story); the testimonials on About are plain cards, no script.
   Lenis drives native scroll, so plain scroll events are enough; one rAF per frame. */
(() => {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const figma = document.documentElement.classList.contains('figma');

    /* ---------- Our history in pictures: the held film (from 768, motion allowed) ---------- */
    const film = document.querySelector('[data-film]');
    if (!film || figma) return;
    const pin = film.querySelector('[data-film-pin]');
    const stage = film.querySelector('[data-film-stage]');
    const track = film.querySelector('[data-film-track]');
    const frames = [...track.children];
    const ghost = film.querySelector('[data-film-ghost]');
    const now = film.querySelector('[data-film-now]');
    const fill = film.querySelector('[data-film-fill]');
    const ticks = [...film.querySelectorAll('[data-film-tick]')];
    const years = frames.map((f) => f.dataset.year);
    const wide = matchMedia('(min-width: 768px)');
    let on = false, dist = 0, centres = [], active = -1, raf = 0;

    // the rule runs in years, first print to last; each decade sits where it falls
    const y0 = +years[0], y1 = +years[years.length - 1];
    const at = (y) => (y - y0) / (y1 - y0);
    const placeTicks = () => {
        ticks.forEach((t) => t.style.setProperty('--at', `${(at(+t.dataset.filmTick) * 100).toFixed(2)}%`));
    };
    const measure = () => {
        track.style.transform = 'none';
        const vw = stage.clientWidth;
        dist = Math.max(0, track.scrollWidth - vw);
        // progress 0 puts the first frame's centre on the stage centre, 1 the last one's
        centres = frames.map((f) => f.offsetLeft + f.offsetWidth / 2);
        const first = centres[0] - vw / 2, last = centres[centres.length - 1] - vw / 2;
        film._from = Math.max(0, first);
        film._to = Math.min(dist, last);
        pin.style.height = `${(film._to - film._from) + innerHeight}px`;
    };
    const setYear = (i) => {
        if (i === active) return;
        active = i;
        const y = years[i];
        now.textContent = y;
        if (reduce) { ghost.textContent = y; return; }
        ghost.classList.add('is-out');
        clearTimeout(ghost._t);
        ghost._t = setTimeout(() => { ghost.textContent = y; ghost.classList.remove('is-out'); }, 160);
    };
    const frame = () => {
        raf = 0;
        if (!on) return;
        const top = pin.getBoundingClientRect().top;
        const span = film._to - film._from;
        const p = span > 0 ? Math.min(1, Math.max(0, -top / span)) : 0;
        const x = film._from + p * span;
        track.style.transform = `translate3d(${-x}px, 0, 0)`;
        const c = x + stage.clientWidth / 2;
        let best = 0;
        centres.forEach((v, i) => { if (Math.abs(v - c) < Math.abs(centres[best] - c)) best = i; });
        setYear(best);
        fill.style.setProperty('--p', at(+years[best]).toFixed(4));
        ticks.forEach((t) => t.classList.toggle('is-past', +years[best] >= +t.dataset.filmTick));
        // depth: each print drifts a little against the travel, more the further it is from centre
        frames.forEach((f, i) => {
            const d = (centres[i] - c) / stage.clientWidth;
            if (Math.abs(d) < 1.2) f.querySelector('.film__print img').style.setProperty('--px', `${(d * -28).toFixed(1)}px`);
        });
    };
    const ask = () => { if (!raf) raf = requestAnimationFrame(frame); };
    const setup = () => {
        const want = wide.matches && !reduce;
        if (want && !on) {
            film.classList.add('is-pinned');
            on = true;
            // the prints are lazy: load the strip now, it is about to travel through the screen
            frames.forEach((f) => f.querySelectorAll('img[loading="lazy"]').forEach((img) => { img.loading = 'eager'; }));
            // the page staircase would hide the frames' captions; the film shows its own text
            film.querySelectorAll('.rv').forEach((el) => el.classList.remove('rv', 'rv--sm'));
        } else if (!want && on) {
            film.classList.remove('is-pinned');
            on = false;
            pin.style.height = '';
            track.style.transform = '';
        }
        if (on) { measure(); placeTicks(); ask(); }
    };
    setup();
    addEventListener('scroll', ask, { passive: true });
    addEventListener('resize', () => { setup(); ask(); });
    wide.addEventListener('change', setup);
    addEventListener('load', () => { if (on) { measure(); ask(); } });
    track.querySelectorAll('img').forEach((img) => img.addEventListener('load', () => { if (on) { measure(); ask(); } }, { once: true }));
})();
