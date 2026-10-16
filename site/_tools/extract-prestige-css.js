/* Run in the browser on a Prestige prototype page (prestige-final/srp_v2.html or vdp_v2.html):
   returns the CSS rules from Prestige's own stylesheets whose selectors use ONLY the given classes
   (the classes of that page's <main> plus those its JS adds), in source order, with their @media
   wrappers, each selector prefixed with ".pi " so the copy is scoped to the Lambo mockup's main.
   Rules on html/body/:root and bare element selectors are skipped (the Lambo base owns those).
   Used by site/_tools/build-inventory-mockups.py (output: assets/css/prestige_srp.css / _vdp.css). */
(allowed) => {
    const OK = new Set(allowed);
    const split = (sel) => {            // top-level commas only
        const out = []; let depth = 0, cur = '';
        for (const ch of sel) {
            if (ch === '(') depth++;
            if (ch === ')') depth--;
            if (ch === ',' && depth === 0) { out.push(cur.trim()); cur = ''; } else cur += ch;
        }
        if (cur.trim()) out.push(cur.trim());
        return out;
    };
    const keep = (s) => {
        if (/(^|[\s>+~(])(html|body|:root)\b/.test(s)) return false;
        const classes = [...s.matchAll(/\.([A-Za-z_][\w-]*)/g)].map((m) => m[1]);
        return classes.length > 0 && classes.every((c) => OK.has(c));
    };
    const scope = (s) => '.pi ' + s;
    const walk = (rules, indent = '') => {
        let css = '';
        for (const r of rules) {
            if (r instanceof CSSStyleRule) {
                const sels = split(r.selectorText).filter(keep);
                if (sels.length) css += `${indent}${sels.map(scope).join(',\n' + indent)} { ${r.style.cssText} }\n`;
            } else if (r instanceof CSSMediaRule) {
                const inner = walk(r.cssRules, indent + '    ');
                if (inner) css += `${indent}@media ${r.conditionText} {\n${inner}${indent}}\n`;
            } else if (r instanceof CSSSupportsRule) {
                const inner = walk(r.cssRules, indent + '    ');
                if (inner) css += `${indent}@supports ${r.conditionText} {\n${inner}${indent}}\n`;
            } else if (r instanceof CSSKeyframesRule) {
                css += r.cssText + '\n';
            }
        }
        return css;
    };
    let out = '';
    for (const sheet of document.styleSheets) {
        if (!sheet.href || !/\/assets\/css\//.test(sheet.href)) continue;   // Prestige's own files only
        out += `/* ---- from ${sheet.href.split('/').pop().split('?')[0]} ---- */\n` + walk(sheet.cssRules);
    }
    return out;
}
