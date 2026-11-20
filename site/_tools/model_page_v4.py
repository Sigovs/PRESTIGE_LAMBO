"""The v4 layer over build-model-pages.py's output (20 Nov 2026).

The v3 model pages were built by build-model-pages.py on 21 Oct, then changed in place: the client's 22 Oct round
(US spelling "Inquire", a ZIP field for the CRM, Schedule service and Ad Personam pages of their own), the
all-models menu (menu-models.py) and newer CSS/JS versions. This module re-applies exactly those changes to a
fresh build, so the builder's output equals the committed pages again and can be re-run safely.
Check: python _tools/build-model-pages.py --check  (builds in memory and compares with the pages on disk)."""
import re

ZIP_ROW = '''                    <!-- v4 (22 Oct, client): ZIP code, for the CRM -->
                    <div class="form__row">
                        <div class="field">
                            <label class="field__label" for="enq-zip">ZIP code <span class="field__req">(required)</span></label>
                            <input class="field__input" id="enq-zip" name="zip" type="text" autocomplete="postal-code" inputmode="numeric" maxlength="10" required aria-describedby="enq-zip-err">
                            <p class="field__error" data-no-rise id="enq-zip-err" hidden></p>
                        </div>
'''


def v4(html, page_name):
    s = html
    # US spelling (client, 22 Oct)
    for a, b in (('enquire', 'inquire'), ('Enquire', 'Inquire'), ('ENQUIRE', 'INQUIRE'),
                 ('enquiry', 'inquiry'), ('Enquiry', 'Inquiry')):
        s = s.replace(a, b)
    s = s.replace('(as index_v3.html)', '(as index_v4.html)')
    # pages of their own
    s = s.replace('href="service.html#request">Schedule service', 'href="schedule-service.html">Schedule service')
    s = s.replace('href="index_v3.html#ad-personam"', 'href="ad-personam.html"')
    # ZIP before the model select, the two side by side
    m = re.search(r'( {20}<div class="field">\n {24}<label class="field__label" for="enq-model">Model</label>\n.*?</select>\n {20}</div>\n)', s, re.S)
    if m and 'id="enq-zip"' not in s:
        block = ''.join('    ' + ln if ln.strip() else ln for ln in m.group(1).splitlines(True))
        s = s[:m.start()] + ZIP_ROW + block + '                    </div>\n' + s[m.end():]
    # current versions, and the menu's own CSS/JS
    s = re.sub(r'main_v3\.css\?v=\d+', 'main_v3.css?v=326', s)
    s = re.sub(r'service_v2\.css\?v=\d+', 'service_v2.css?v=22', s)
    s = re.sub(r'model_v3\.js\?v=\d+', 'model_v3.js?v=11', s)
    if 'menu_models.css' not in s:
        s = s.replace('<link rel="stylesheet" href="assets/css/main_v3.css?v=326">',
                      '<link rel="stylesheet" href="assets/css/main_v3.css?v=326">\n    <link rel="stylesheet" href="assets/css/menu_models.css?v=7">', 1)
    if 'menu_models.js' not in s:
        s = s.replace('<script src="assets/js/model_v3.js?v=11" defer></script>',
                      '<script src="assets/js/menu_models.js?v=1" defer></script>\n<script src="assets/js/model_v3.js?v=11" defer></script>', 1)
    # the menu marks this page's model and its family (as menu-models.py does)
    link = f'<a class="menu__model" href="{page_name}">'
    if link in s:
        s = s.replace(link, f'<a class="menu__model" href="{page_name}" aria-current="page">', 1)
        i = s.index(f'href="{page_name}" aria-current="page"')
        j = s.rfind('data-models-fam aria-expanded="false" aria-controls="', 0, i)
        k = s.index('"', j + len('data-models-fam aria-expanded="false" aria-controls="'))
        if not s[k + 1:].startswith(' data-current'):
            s = s[:k + 1] + ' data-current' + s[k + 1:]
    return s
