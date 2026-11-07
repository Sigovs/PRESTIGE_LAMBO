/* LAMBORGHINI MIAMI — the menu's Models column (_tools/menu-models.py, assets/css/menu_models.css).
   Each family is a drop-down of its models; one open at a time, a second click closes it.
   On a model's own page the menu opens with its family open. Loaded after main_v2/3/4.js. */
(() => {
    const col = document.querySelector('[data-menu-models]');
    if (!col) return;
    const menu = col.closest('[data-menu]');
    const fams = [...col.querySelectorAll('[data-models-fam]')];
    const home = col.querySelector('.menu__model[aria-current="page"]')?.closest('.menu__fam-item')?.querySelector('[data-models-fam]') || null;

    const set = (open) => fams.forEach((b) => b.setAttribute('aria-expanded', String(b === open)));
    fams.forEach((b) => b.addEventListener('click', () => set(b.getAttribute('aria-expanded') === 'true' ? null : b)));

    // Every opening starts closed, or with the page's own family open
    set(home);
    if (menu) new MutationObserver(() => { if (menu.hidden) set(home); }).observe(menu, { attributes: true, attributeFilter: ['hidden'] });
})();
