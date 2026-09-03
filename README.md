# BIZTECH Consulting — site one-page în 5 limbi (RO · EN · SV · FR · DE)

Deschideți `index.html` direct în browser (dublu-click) — funcționează fără server; selectorul cu steaguri din header duce la `en/`, `sv/`, `fr/`, `de/`. Pentru publicare, urcați întregul folder `site/` pe Vercel, Netlify sau orice hosting static (acolo unde este și demo-ul, pe Vercel, este cel mai simplu: *Add New → Project → Upload* folderul `site`).

## Structura

| Fișier | Rol |
|---|---|
| `index.html`, `en/index.html`, `sv/index.html`, `fr/index.html`, `de/index.html` | Paginile pe limbi — **generate** din `_src/` (nu le editați direct; editați textele în `_src/i18n/*.py` și rulați `python3 _src/build.py`) |
| `_src/template_body.html`, `_src/_css.html`, `_src/_sprite.html` | Structura paginii (o singură dată pentru toate limbile), stilurile, icoanele |
| `_src/i18n/ro.py … de.py` | Toate textele, pe chei, câte un fișier pe limbă (`PHONE_ORDER` decide ce telefon apare primul) |
| `_src/build.py` | Generatorul: completează șablonul, scrie `hreflang`, meniul de limbi, schema.org în limba paginii, `sitemap.xml` și `robots.txt`. `CLEAN_URLS = True` la publicare pe server (linkuri `/en/` în loc de `en/index.html`) |
| `assets/flags/*.svg` | Steagurile din selectorul de limbă (din `Media/lang-*-icon.svg`) |
| `politica-confidentialitate.html` | Politica de confidențialitate (deocamdată doar în română; paginile EN/SV/FR/DE trimit la ea) |
| `assets/logo-dark.svg`, `assets/logo-light.svg`, `assets/favicon.ico`, `assets/whatsapp.png` | Logo pentru tema dark / light, favicon, iconul WhatsApp (din `Media/whatsapp-icon.png`, 256 px) |
| `assets/hero-bg.mp4` (1,6 MB), `assets/hero-poster.jpg` | Videoclipul de fundal comprimat la 720p + imaginea statică afișată până se încarcă / pe mobil cu „reduce motion” |
| `assets/img/` | Capturile de ecran folosite în pagină (din `screenshots-landing/web/`) și fotografia portret |

## Formulare → email prin Web3Forms (3 pași)

Site-ul este static (GitHub Pages nu rulează cod pe server), așa că formularele trimit datele la **Web3Forms**, un serviciu gratuit (250 de mesaje/lună) care le livrează ca email pe **biztechconsultingsrl@gmail.com** (adresa afișată vizitatorilor pe site este `contact@biztech.ro`; cele două pot coincide dacă `contact@biztech.ro` redirecționează spre Gmail). Cheia de acces Web3Forms este publică prin construcție (permite doar trimiterea către adresa asociată), deci poate sta liniștită în cod și în repository.

1. Intrați pe **https://web3forms.com**, scrieți `biztechconsultingsrl@gmail.com` în câmpul „Create your Access Key” și apăsați butonul. Cheia (un cod de forma `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) sosește pe email în câteva secunde — verificați și Spam/Promotions.
2. Deschideți `_src/build.py` și puneți cheia între ghilimele la `WEB3FORMS_KEY = ''`.
3. Rulați `python3 _src/build.py` din folderul `site/` — cheia intră în toate cele 5 pagini. Trimiteți un mesaj de test din formular: sosește pe email în sub un minut, cu câmpurile în tabel, „Reply” merge direct la vizitator.

Cât timp cheia este goală, formularele cad pe `mailto:` (se deschide clientul de email al vizitatorului), iar butonul „Sau trimiteți pe WhatsApp” compune mesajul din câmpuri. Protecție anti-spam: câmp invizibil (honeypot) + filtrul Web3Forms; dacă apare spam, în contul Web3Forms se poate activa hCaptcha (necesită o linie în plus în cod).

## Publicare pe GitHub Pages — repository: https://github.com/challymcchallenge/biztech.ro

Conținutul acestui folder (`site/`) este rădăcina repository-ului. Prima publicare, din Git Bash sau PowerShell, pe calculatorul dumneavoastră:

```bash
cd "C:\Users\alinl\Desktop\Claude_CoWork\BIZTECH - Site\site"
git init
git add -A
git commit -m "Site BIZTECH Consulting — RO/EN/SV/FR/DE"
git branch -M main
git remote add origin https://github.com/challymcchallenge/biztech.ro.git
git push -u origin main --force
```

`--force` este necesar o singură dată, pentru că repository-ul are deja un README creat pe GitHub; de la a doua publicare înainte: `git add -A && git commit -m "..." && git push`.

Apoi, pe GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch `main`, folder `/ (root)` → Save.** În 1–2 minute site-ul este live la **https://challymcchallenge.github.io/biztech.ro/** (linkurile din pagini sunt relative, deci funcționează și în acest sub-folder). `.nojekyll` este inclus — fără el GitHub ar ignora folderul `_src/`.

Domeniu propriu (`www.biztech.ro`), când DNS-ul este pregătit: în `_src/build.py` setați `CUSTOM_DOMAIN = 'www.biztech.ro'` și `CLEAN_URLS = True`, rulați build (se creează fișierul `CNAME`), publicați; apoi Settings → Pages → Custom domain → `www.biztech.ro` → Save, bifați **Enforce HTTPS** după ce apare bifa verde. La registrarul domeniului: `CNAME  www → challymcchallenge.github.io` și, pentru `biztech.ro` fără www, 4 înregistrări `A` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`. Nu creați fișierul `CNAME` înainte de a configura DNS-ul: cu el prezent, GitHub redirecționează adresa github.io către domeniu, care încă nu răspunde.

## Google Analytics

Tag-ul oficial `G-P9GCEV3J79` este în `<head>` pe toate paginile, o singură dată, cu **Consent Mode v2**: pornește cu `analytics_storage: denied` și trece pe `granted` când vizitatorul apasă „Accept” în bannerul de cookie-uri (alegerea se memorează). Toate butoanele trimit evenimente (`cta_whatsapp_*`, `cta_meet_*`, `cta_tel_*`, `cta_demo*`, `form_submit`, `form_quick`), fiecare cu limba paginii.

Alte locuri de verificat: `DOMAIN` din `_src/build.py` (acum `https://www.biztech.ro`) este folosit pentru `canonical`, `hreflang`, `og:image`, `sitemap.xml`; dacă publicați provizoriu pe `github.io`, schimbați-l temporar sau lăsați-l — nu strică nimic, doar Google va prefera domeniul final.

## Ce face pagina

- Temă **dark implicit**, comutator ☀/☾ în header, memorată în browser.
- **WhatsApp** este CTA-ul principal: buton verde în fiecare secțiune, buton lipicios dreapta-jos, bulă de mesaj după 6 secunde (o dată pe sesiune), iar pe mobil o bară fixă jos cu WhatsApp · Apel · Meet.
- Caruselul din secțiunea Demo: autoplay la 3 secunde, săgeți și puncte (și pe mobil), swipe; se oprește când treceți cu mouse-ul sau interacționați și repornește după 7 secunde.
- Rezervarea Google Meet duce la `https://calendar.app.google/CpjHNeDtCuGkzk4h8`; demo-ul la `https://smart-ai-dashboard.vercel.app/`.
- Date structurate schema.org (ProfessionalService, Person, FAQPage) pentru Google.
- Fonturi Google (Manrope + Inter) cu fallback pe fonturile sistemului dacă nu se încarcă.
