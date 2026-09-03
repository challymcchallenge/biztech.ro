#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generează paginile site-ului din template + fișierele de limbă.
   Rulare:  python3 _src/build.py   (din folderul site/)
   Ieșire:  index.html (RO), en/index.html, sv/index.html, fr/index.html, de/index.html
"""
import json, os, re, sys, importlib, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'i18n'))
DOMAIN = 'https://www.biztech.ro'
CLEAN_URLS = False          # True la publicare pe server (GitHub Pages) → linkurile devin /en/ în loc de en/index.html
WEB3FORMS_KEY = '795d0f5c-7b79-46c2-8b6d-91dd0be8b95b'          # cheia de acces primită pe email de la https://web3forms.com (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx); goală = formularele cad pe mailto
CUSTOM_DOMAIN = ''          # ex. 'www.biztech.ro' → scrie fișierul CNAME pentru GitHub Pages; gol = fără CNAME
DEMO_URL = 'https://smart-ai-dashboard.vercel.app/'
MEET_URL = 'https://calendar.app.google/CpjHNeDtCuGkzk4h8'
PHONES = {'ro': ('+40772295031', '+40 772 295 031', 'cta_tel_ro'), 'se': ('+46720123475', '+46 720 123 475', 'cta_tel_se')}
LANGS = ['ro', 'en', 'sv', 'fr', 'de']
GA = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-P9GCEV3J79"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', { 'analytics_storage': 'denied', 'ad_storage': 'denied', 'ad_user_data': 'denied', 'ad_personalization': 'denied', 'wait_for_update': 500 });
  gtag('js', new Date());
  gtag('config', 'G-P9GCEV3J79', { 'anonymize_ip': true });
</script>'''
HEAD = '''<!DOCTYPE html>
<html lang="{{lang}}" data-theme="dark">
<head>
''' + GA + '''
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{meta_title}}</title>
<meta name="description" content="{{meta_desc}}">
<link rel="icon" href="{{base}}assets/favicon.ico">
<link rel="canonical" href="{{canonical}}">
{{hreflang}}
<meta property="og:type" content="website">
<meta property="og:title" content="{{meta_title}}">
<meta property="og:description" content="{{og_desc}}">
<meta property="og:image" content="''' + DOMAIN + '''/assets/img/hero-desktop.png">
<meta property="og:locale" content="{{locale}}">
<meta name="theme-color" content="#1E1829">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
'''
JS_KEYS = ['wa_general','wa_demo','slide_n','err_email','subj_case','body_case','ok_quick','err_quick','f_name','f_company_short','f_phone','f_interest_short','f_system_short','f_message_short','err_required','subj_contact','ok_contact','err_contact','wa_hi_name','wa_hi','wa_interest','wa_system']

def url_for(lang):            # URL absolut (canonical / hreflang)
    return DOMAIN + '/' + ('' if lang == 'ro' else lang + '/')
def href_for(lang, base):     # link relativ din pagina curentă
    if CLEAN_URLS: return base + ('' if lang == 'ro' else lang + '/') or './'
    return base + ('index.html' if lang == 'ro' else lang + '/index.html')
def unescape(s): return s.replace('&amp;', '&')

def build(lang):
    m = importlib.import_module(lang); T = dict(m.T)
    base = '' if lang == 'ro' else '../'
    order = m.PHONE_ORDER
    # telefoane
    tel_links = {k: f'<a href="tel:{PHONES[k][0]}" data-track="{PHONES[k][2]}">{PHONES[k][1]}</a>' for k in PHONES}
    T['header_phones_html'] = ''.join(tel_links[k] for k in order)
    T['hero_call_html'] = T['hero_call_prefix'] + ' ' + ' · '.join(f'<a href="tel:{PHONES[k][0]}">{PHONES[k][1]}</a> ({T["country_"+k]})' for k in order)
    T['ch_tel_html'] = '<br>'.join(f'{T["country_"+k]} {PHONES[k][1]}' for k in order)
    T['company_phones_html'] = ' · '.join(f'<a href="tel:{PHONES[k][0]}">{PHONES[k][1]}</a> ({k.upper()})' for k in order)
    T['footer_phones_html'] = ' · '.join(f'<a href="tel:{PHONES[k][0]}">{PHONES[k][1]}</a>' for k in order)
    T['tel_primary'] = PHONES[order[0]][0]
    # constante
    T.update(base=base, lang=lang, lang_code=lang.upper(), demo_url=DEMO_URL, meet_url=MEET_URL, web3forms_key=WEB3FORMS_KEY,
             policy_href=base + 'politica-confidentialitate.html',
             mailto_case='mailto:contact@biztech.ro?subject=' + urllib.parse.quote(T['subj_case'], safe=''))
    # selector de limbă
    names = {l: importlib.import_module(l).NAME for l in LANGS}
    on = lambda l: ' class="on"' if l == lang else ''
    T['lang_menu'] = ''.join(f'<a href="{href_for(l, base)}" hreflang="{l}" lang="{l}"{on(l)}><img class="flag" src="{base}assets/flags/{l}.svg" alt="">{names[l]}<span class="code">{l.upper()}</span></a>' for l in LANGS)
    T['lang_list_footer'] = ''.join(f'<li><a href="{href_for(l, base)}" hreflang="{l}" lang="{l}"{on(l)}><img class="flag" src="{base}assets/flags/{l}.svg" alt="">{names[l]}</a></li>' for l in LANGS)
    # JSON-LD
    faq = [{"@type": "Question", "name": unescape(T[f'faq{i}_q']), "acceptedAnswer": {"@type": "Answer", "text": unescape(re.sub('<[^>]+>', '', T[f'faq{i}_a']))}} for i in range(1, 9)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfessionalService", "@id": DOMAIN + "/#org", "name": "BIZTECH Consulting SRL", "url": url_for(lang), "email": "contact@biztech.ro",
         "telephone": [PHONES['ro'][0], PHONES['se'][0]],
         "address": {"@type": "PostalAddress", "streetAddress": "B-dul Republicii, Bloc 30, Scara 1, Parter", "addressLocality": "Târgu Jiu", "addressRegion": "Gorj", "postalCode": "217459", "addressCountry": "RO"},
         "areaServed": ["RO", "SE"], "openingHours": "Mo-Su 09:00-18:00", "founder": [{"@id": DOMAIN + "/#alin"}, {"@id": DOMAIN + "/#george"}], "inLanguage": lang, "description": unescape(T['jsonld_desc'])},
        {"@type": "Person", "@id": DOMAIN + "/#alin", "name": "Alin Labau", "jobTitle": unescape(T['jsonld_job']), "worksFor": {"@id": DOMAIN + "/#org"}, "sameAs": ["https://www.linkedin.com/in/alin-labau/"]},
        {"@type": "Person", "@id": DOMAIN + "/#george", "name": "George Lăbău", "jobTitle": unescape(T['g_role']), "worksFor": {"@id": DOMAIN + "/#org"}},
        {"@type": "FAQPage", "mainEntity": faq}]}
    T['jsonld'] = json.dumps(ld, ensure_ascii=False)
    T['js_product'] = json.dumps(T['product'], ensure_ascii=False)
    T['js_i18n'] = json.dumps({k: unescape(T[k]) for k in JS_KEYS}, ensure_ascii=False)
    # asamblare
    hreflang = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{url_for(l)}">' for l in LANGS) + f'\n<link rel="alternate" hreflang="x-default" href="{url_for("en")}">'
    T.update(canonical=url_for(lang), hreflang=hreflang, locale=m.LOCALE)
    head = HEAD
    css = open(os.path.join(HERE, '_css.html'), encoding='utf-8').read()
    sprite = open(os.path.join(HERE, '_sprite.html'), encoding='utf-8').read()
    body = open(os.path.join(HERE, 'template_body.html'), encoding='utf-8').read()
    html = head + css + '\n</head>\n<body>\n' + sprite + body
    missing = set()
    def sub(mo):
        k = mo.group(1)
        if k not in T: missing.add(k); return mo.group(0)
        return str(T[k])
    html = re.sub(r'{{([a-z0-9_]+)}}', sub, html)
    if missing: raise SystemExit(f'[{lang}] chei lipsă: {sorted(missing)}')
    out = os.path.join(SITE, 'index.html') if lang == 'ro' else os.path.join(SITE, lang, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print(f'[{lang}] → {os.path.relpath(out, SITE)}  ({len(html):,} caractere)')

def write_sitemap():
    import datetime
    today = datetime.date.today().isoformat()
    urls = ''.join(f'  <url><loc>{url_for(l)}</loc><lastmod>{today}</lastmod>' + ''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{url_for(x)}"/>' for x in LANGS) + '</url>\n' for l in LANGS)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + f'  <url><loc>{DOMAIN}/politica-confidentialitate.html</loc><lastmod>{today}</lastmod></url>\n</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(xml)
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\nDisallow: /_src/\nSitemap: {DOMAIN}/sitemap.xml\n')
    open(os.path.join(SITE, '.nojekyll'), 'w').close()          # GitHub Pages: fără procesare Jekyll (altfel ignoră folderele cu _)
    if CUSTOM_DOMAIN: open(os.path.join(SITE, 'CNAME'), 'w').write(CUSTOM_DOMAIN + '\n')
    print('sitemap.xml + robots.txt + .nojekyll' + (' + CNAME' if CUSTOM_DOMAIN else ''))

if __name__ == '__main__':
    for l in (sys.argv[1:] or LANGS):
        try: importlib.import_module(l)
        except ModuleNotFoundError: print(f'[{l}] fișier de limbă lipsă — sărit'); continue
        build(l)
    if not sys.argv[1:]: write_sitemap()
