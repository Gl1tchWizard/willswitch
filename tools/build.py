"""Bouw de site uit de bronbestanden in content/cases/.

Draai: python3 tools/build.py
Resultaat komt in dist/ en is klaar om te publiceren.
"""
import html, json, pathlib, re, datetime, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from switchpage import build_switch
from home import build_home
from scan import build_scan

ROOT = pathlib.Path(__file__).resolve().parent.parent
CASES = ROOT / "content" / "cases"
SITE = ROOT / "site"
DIST = ROOT / "dist"
BASE = "https://willswitch.nl"
TODAY = datetime.date.today()


def load_cases():
    out = []
    for f in sorted(CASES.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n\n(.*)", raw, re.S)
        if not m:
            print(f"  overgeslagen (geen kop): {f.name}")
            continue
        try:
            meta = json.loads(m.group(1))
        except ValueError as e:
            raise SystemExit(f"{f.name}: de kop is geen geldige JSON: {e}")
        body = m.group(2).strip()
        # Tussenkoppen in de body zijn h2: de h1 is de titel van de pagina.
        meta["body"] = re.sub(r"<(/?)h3\b", r"<\1h2", body)
        out.append(meta)
    out.sort(key=lambda c: c.get("order", 999))
    return out


def is_published(case):
    d = case.get("publish_on")
    if not d:
        return True
    try:
        return datetime.date.fromisoformat(d) <= TODAY
    except ValueError:
        raise SystemExit(f"{case['id']}: publish_on {d!r} is geen datum als JJJJ-MM-DD")


def case_datum(case):
    """Een datum per case, overal dezelfde: JSON-LD, article-meta en sitemap."""
    return case.get("publish_on") or case.get("new_since") or "2026-07-01"


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def eerste_zinnen(txt, maxlen=160):
    """De eerste volledige zin(nen), zolang ze samen binnen maxlen blijven.
    De eerste zin gaat altijd mee, ook als die langer is."""
    zinnen = re.split(r"(?<=[.!?])\s+", txt.strip())
    out = ""
    for z in zinnen:
        kandidaat = (out + " " + z).strip()
        if out and len(kandidaat) > maxlen:
            break
        out = kandidaat
    return out


def description(case):
    if case.get("description"):
        return case["description"].strip()
    kaart = case.get("card_body", "")
    if kaart and len(kaart) <= 175:
        return kaart
    return eerste_zinnen(kaart or strip_tags(case["body"]))


def page_title(case):
    """Het achtervoegsel alleen als de title er niet te lang van wordt (Google kapt rond 65)."""
    if case.get("seo_title"):
        return case["seo_title"]
    t = case["title"]
    return f"{t} | Will Switch" if len(t) + 14 <= 65 else t


def jsonld_case(case, d):
    """Article plus BreadcrumbList voor een casepagina."""
    url = f"{BASE}/cases/{case['id']}/"
    gepubliceerd = case_datum(case)
    gewijzigd = gepubliceerd
    artikel = {
        "@type": "Article",
        "@id": f"{url}#article",
        "headline": case["title"],
        "description": d,
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": {"@type": "ImageObject", "url": f"{BASE}/og-image.jpg", "width": 1200, "height": 630},
        "datePublished": gepubliceerd,
        "dateModified": gewijzigd,
        "inLanguage": "nl-NL",
        "articleSection": case.get("eyebrow", ""),
        "author": {"@type": "Person", "name": "Govert Schoof", "url": "https://www.linkedin.com/in/govertschoof/"},
        "publisher": {
            "@type": "Organization", "@id": f"{BASE}/#organization",
            "name": "Will Switch", "url": f"{BASE}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/wordmark.png", "width": 705, "height": 153},
        },
        "isPartOf": {"@type": "WebSite", "@id": f"{BASE}/#website", "name": "Will Switch", "url": f"{BASE}/"},
    }
    kruimels = {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Will Switch", "item": f"{BASE}/switch.html"},
            {"@type": "ListItem", "position": 2, "name": "Praktijk", "item": f"{BASE}/switch.html#verhalen"},
            {"@type": "ListItem", "position": 3, "name": case["title"], "item": url},
        ],
    }
    graph = {"@context": "https://schema.org", "@graph": [artikel, kruimels]}
    return json.dumps(graph, ensure_ascii=False, indent=2)


# ---------- de losse casepagina ----------
PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
{robots}
  <meta name="description" content="{description}">
  <link rel="canonical" href="{base}/cases/{id}/">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="nl_NL">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{base}/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{base}/cases/{id}/">
  <meta property="article:published_time" content="{published}">
  <meta property="article:modified_time" content="{modified}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{base}/og-image.jpg">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180.png">
  <link rel="preload" href="/fonts/AtkinsonNext.woff2" as="font" type="font/woff2" crossorigin>
  <script type="application/ld+json">
{jsonld}
  </script>
  <style>{css}  </style>
</head>
<body>

<header class="top"><div class="w">
  <a class="merk" href="/switch.html"><img src="/wordmark.png" alt="Will Switch" width="705" height="153"><span>Praktijkonderzoek naar<br>digitale autonomie</span></a>
  <nav class="hoofd" aria-label="Hoofdnavigatie"><a class="l" href="/switch.html#verhalen">Praktijk</a><a class="l" href="/switch.html#rapport">Rapport</a><a class="knop" href="/scan/"><span class="lang">Uitstaptoets</span><span class="kort">Toets</span> &rarr;</a></nav>
</div></header>

<main class="case"><div class="w">
  <article class="lees">
    <p class="kicker">{eyebrow}</p>
    <h1>{title}</h1>
    {body}
  </article>

{scanblok}

  <section class="meer" aria-labelledby="meer-kop">
    <h2 id="meer-kop">Meer praktijkverhalen</h2>
    <ul class="register">
{related}
    </ul>
    <p class="alle"><a class="tekstlink" href="/switch.html#overzicht">Alle cases op de hoofdpagina</a></p>
  </section>
</div></main>

<footer class="site"><div class="w">
  <span>Will Switch &middot; willswitch.nl &middot; <a href="/">terug naar de switch</a></span>
  <a class="fonds" href="https://www.sidnfonds.nl/"><span>Onderzoek met steun van</span><img src="/sidnfonds.png" alt="SIDN fonds" width="150" height="28"></a>
</div></footer>
  <!-- Privacyvriendelijke analytics (GoatCounter, geen cookies) -->
  <script data-goatcounter="https://willswitch.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""

# Tokens, header, knoppen en voettekst zijn overgenomen uit tools/switchpage.py.
CSS = """
@font-face {
  font-family:'Atkinson Hyperlegible Next';
  src:url('/fonts/AtkinsonNext.woff2') format('woff2');
  font-weight:200 800; font-style:normal; font-display:swap;
}
:root {
  --papier:#F0EDE6; --warm:#E8E3D6; --wit:#FBFAF7;
  --inkt:#1a1612; --zacht:#4a443c; --vaag:#6b645a;
  --lijn:rgba(26,22,18,.16); --oranje:#E84500; --knop:#D63F00; --link:#B83500;
  --op-inkt:rgba(240,237,230,.78); --op-inkt-2:rgba(240,237,230,.7); --lijn-inkt:rgba(240,237,230,.25);
  --mono:ui-monospace, 'Cascadia Mono', Consolas, Menlo, monospace;
}
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { overflow-x:clip; scrollbar-gutter:stable; scroll-behavior:smooth; }
body {
  background:var(--papier); color:var(--inkt);
  font-family:'Atkinson Hyperlegible Next', system-ui, sans-serif; font-synthesis:none;
  font-size:17px; line-height:1.55;
}
.w { max-width:1280px; margin:0 auto; padding:0 40px; }
a { color:inherit; }
h1, h2, h3 { font-weight:700; }
h1, h2 { text-wrap:balance; }
img { max-width:100%; }
:focus-visible { outline:3px solid var(--knop); outline-offset:3px; }
.mono, .kicker { font-family:var(--mono); font-size:13px; letter-spacing:.02em; line-height:1.6; color:var(--zacht); }

/* knoppen en links */
.knop {
  display:inline-flex; align-items:center; justify-content:center; gap:.55em;
  min-height:44px; padding:0 20px; background:var(--knop); color:#fff; font-weight:700;
  text-decoration:none; font-size:16px; line-height:1.1; border-radius:0;
}
.knop:hover { background:var(--inkt); color:#fff; }
.knop.groot { min-height:56px; padding:0 28px; font-size:18px; }
.tekstlink, .lees p a {
  color:var(--link); font-weight:600; text-decoration:underline;
  text-underline-offset:4px; text-decoration-thickness:1.5px;
}
.tekstlink:hover, .lees p a:hover { color:var(--inkt); }

/* header */
header.top { border-bottom:1px solid var(--inkt); background:var(--papier); }
header.top .w { display:flex; align-items:center; justify-content:space-between; min-height:84px; gap:20px; }
.merk { display:flex; align-items:center; gap:18px; text-decoration:none; }
.merk img { height:36px; width:auto; display:block; }
.merk span { font-family:var(--mono); font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--zacht); line-height:1.5; padding-left:18px; border-left:1px solid var(--inkt); }
nav.hoofd { display:flex; align-items:center; gap:32px; font-size:16px; }
nav.hoofd a.l { text-decoration:none; padding:11px 0; }
nav.hoofd a.l:hover { text-decoration:underline; text-underline-offset:4px; }
nav.hoofd .kort { display:none; }

/* motief */
.ring { position:absolute; border-radius:50%; border:1px solid var(--oranje); pointer-events:none; }

/* de leeskolom */
main.case { padding:64px 0 88px; }
.lees { max-width:640px; }
.lees h1 { max-width:none; }
.lees .kicker { margin-bottom:20px; }
.lees h1 { font-size:clamp(40px, 5vw, 64px); font-weight:800; letter-spacing:-.02em; line-height:1.02; margin-bottom:36px; }
.lees h2 { font-size:32px; line-height:1.1; letter-spacing:-.01em; margin:48px 0 14px; }
.lees h3 { font-size:22px; line-height:1.2; margin:36px 0 10px; }
.lees p { margin-bottom:20px; }
.lees ul, .lees ol { padding-left:24px; margin-bottom:20px; }
.lees li { margin-bottom:6px; }
.lees .case-quote {
  position:relative; margin:48px 0 48px 0; padding-left:28px;
  font-size:30px; font-weight:700; line-height:1.15; letter-spacing:-.01em; color:var(--inkt);
}
.lees .case-quote::before { content:""; position:absolute; left:0; top:-20px; bottom:-20px; width:6px; background:var(--oranje); }
.lees figure { margin:32px 0 36px; }
.lees figure img { width:100%; height:auto; display:block; }
.lees .case-cap { font-family:var(--mono); font-size:13px; letter-spacing:.02em; line-height:1.6; color:var(--zacht); margin:10px 0 0; }
.lees .case-credit { margin-top:40px; padding-top:16px; border-top:1px solid var(--inkt); font-size:15px; color:var(--vaag); }
.lees .case-link-wrap { margin-top:4px; }

/* het toetsblok, op inkt */
.toets {
  position:relative; overflow:hidden; margin-top:72px; padding:44px 48px 48px;
  background:var(--inkt); color:var(--papier);
  display:grid; grid-template-columns:7fr 5fr; gap:48px; align-items:center;
}
.toets > *:not(.ring) { position:relative; }
.toets .ring { width:360px; height:360px; border-width:1.5px; opacity:.55; right:-140px; top:-200px; }
.toets .kicker { color:var(--op-inkt-2); }
.toets h2 { font-size:32px; line-height:1.08; letter-spacing:-.02em; margin-top:8px; }
.toets p { font-size:17px; color:var(--op-inkt); max-width:48ch; margin-top:12px; }
.toets .actie { justify-self:end; display:flex; flex-direction:column; align-items:flex-start; gap:12px; text-align:left; }
.toets .micro { display:block; font-family:var(--mono); font-size:13px; letter-spacing:.02em; color:var(--op-inkt-2); max-width:34ch; line-height:1.5; }

/* meer praktijkverhalen, als register */
.meer { margin-top:80px; }
.meer h2 { font-size:32px; line-height:1.08; letter-spacing:-.02em; }
.register { list-style:none; margin-top:20px; display:grid; grid-template-columns:1fr 1fr; column-gap:48px; }
.register li { border-top:1px solid var(--inkt); }
.register li:nth-last-child(-n+2) { border-bottom:1px solid var(--inkt); }
.register a { display:grid; grid-template-columns:48px 1fr; gap:16px; padding:18px 0; min-height:44px; text-decoration:none; color:inherit; }
.register .n { font-family:var(--mono); font-size:14px; color:var(--link); padding-top:3px; }
.register .kicker { display:block; }
.register b { display:block; font-size:20px; line-height:1.2; margin-top:4px; }
.register a:hover b { text-decoration:underline; text-underline-offset:4px; }
.meer .alle { margin-top:24px; }

/* voet */
footer.site { border-top:3px solid var(--inkt); padding:28px 0 48px; font-size:14px; color:var(--vaag); }
footer.site .w { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px 24px; }
footer.site .fonds { display:inline-flex; align-items:center; gap:12px; text-decoration:none; }
footer.site .fonds img { height:28px; width:auto; display:block; }

/* mobiel */
@media (max-width:820px) {
  .w { padding:0 16px; }
  header.top .w { min-height:64px; }
  .merk { flex-shrink:0; }
  .merk img { max-width:none; height:26px; }
  nav.hoofd .knop { padding:0 14px; }
  .merk span { display:none; }
  nav.hoofd { gap:12px; font-size:15px; }
  nav.hoofd .lang { display:none; }
  nav.hoofd .kort { display:inline; }
  main.case { padding:40px 0 64px; }
  .lees h1 { margin-bottom:28px; }
  .lees h2 { font-size:26px; margin-top:40px; }
  .lees .case-quote { font-size:24px; padding-left:20px; margin:36px 0; }
  .lees .case-quote::before { width:4px; top:-12px; bottom:-12px; }
  .toets { grid-template-columns:1fr; gap:24px; padding:32px 20px 36px; margin-top:56px; }
  .toets .ring { width:240px; height:240px; right:-120px; top:-140px; }
  .toets h2 { font-size:26px; }
  .toets .actie { justify-self:stretch; text-align:left; }
  .toets .knop { width:100%; min-height:52px; }
  .meer { margin-top:56px; }
  .meer h2 { font-size:26px; }
  .register { grid-template-columns:1fr; }
  .register li:nth-last-child(-n+2) { border-bottom:0; }
  .register li:last-child { border-bottom:1px solid var(--inkt); }
  .register a { grid-template-columns:40px 1fr; }
  .register b { font-size:18px; }
  footer.site .w { flex-direction:column; align-items:flex-start; gap:12px; }
}
@media (max-width:400px) { nav.hoofd a.l { display:none; } }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior:auto; }
}
"""


SCAN_AAN = True   # FASE 1: gratis toets is open. Bestellen staat nog uit, zie tools/scan.py

SCANBLOK = """  <section class="toets" aria-labelledby="toets-kop">
    <div class="ring" aria-hidden="true"></div>
    <div>
      <p class="kicker">de uitstaptoets</p>
      <h2 id="toets-kop">Waar staat jouw organisatie?</h2>
      <p>Deze verhalen laten zien wat er mogelijk is. De volgende vraag is wat er bij jou speelt. De uitstaptoets brengt in kaart waar je staat en wat een logische eerste stap is.</p>
    </div>
    <div class="actie">
      <a class="knop groot" href="/scan/">Doe de uitstaptoets &rarr;</a>
      <span class="micro">een kwartier, geen registratie, je antwoorden blijven in je browser</span>
    </div>
  </section>"""


def related_html(others):
    """title en eyebrow zijn platte tekst en worden geëscaped; card_body en body zijn HTML."""
    return "\n".join(
        f'      <li><a href="/cases/{o["id"]}/"><span class="n">{i:02d}</span>'
        f'<span><span class="kicker">{html.escape(o.get("eyebrow", ""))}</span><b>{html.escape(o["title"])}</b></span></a></li>'
        for i, o in enumerate(others, 1))


def soort(case):
    return (case.get("eyebrow") or "").split("·")[0].split("/")[0].strip().lower()


def verwant(case, live):
    """Eerst cases van dezelfde soort (wetgeving, praktijk, ...), dan de rest, nooit zichzelf."""
    zelfde = [o for o in live if o["id"] != case["id"] and soort(o) == soort(case)]
    rest = [o for o in live if o["id"] != case["id"] and o not in zelfde]
    return (zelfde + rest)[:4]


def build():
    cases = load_cases()
    live = [c for c in cases if is_published(c)]
    # Toekomstige cases krijgen alvast een pagina, met noindex en buiten de sitemap.
    # Anders wijst een kaart die op zijn publicatiedatum verschijnt naar een pagina
    # die pas bij de volgende bouw wordt aangemaakt, en dat geeft een 404.
    komend = [c for c in cases if not is_published(c)]
    print(f"{len(cases)} cases, waarvan {len(live)} gepubliceerd op {TODAY}")

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    # vaste bestanden meenemen; de originelen van de webp's en de oude sitemap niet
    OVERSLAAN = {"sitemap.xml", "switch-hero.png", "dsg-viewer.jpg"}
    for f in SITE.glob("*"):
        if f.is_file() and f.name not in OVERSLAAN:
            shutil.copy(f, DIST / f.name)
    ht = SITE / ".htaccess"
    if ht.exists():
        shutil.copy(ht, DIST / ".htaccess")

    # casepagina's
    for c in live + komend:
        vooruit = c in komend
        others = verwant(c, live)
        # relatieve paden naar de root omzetten, de casepagina staat dieper
        body = re.sub(r'href="\?case=([a-z]+)"', r'href="/cases/\1/"', c["body"])
        body = re.sub(r'(src|href|srcset)="(?![a-z][a-z0-9+.-]*:|/|#)', r'\1="/', body)
        d = description(c)
        gepubliceerd = case_datum(c)
        page = PAGE.format(
            robots=('  <meta name="robots" content="noindex">\n' if vooruit else ''),
            scanblok=SCANBLOK if SCAN_AAN else '',
            id=c["id"],
            title=html.escape(c["title"], quote=True),
            page_title=html.escape(page_title(c), quote=True),
            eyebrow=html.escape(c.get("eyebrow", "")),
            description=html.escape(d, quote=True),
            jsonld=jsonld_case(c, d).replace("</", "<\\/"),
            published=gepubliceerd,
            modified=gepubliceerd,
            body=body,
            related=related_html(others),
            base=BASE,
            css=CSS,
        )
        out = DIST / "cases" / c["id"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page, encoding="utf-8")
        print(f"  /cases/{c['id']}/" + ("   (vooruit, noindex tot " + c["publish_on"] + ")" if vooruit else ""))

    # homepage met inhoud onder het portaal
    home = SITE / "index.html"
    if home.exists():
        (DIST / "index.html").write_text(build_home(home.read_text(encoding="utf-8"), live), encoding="utf-8")
        print("  index.html (homepage)")

    # de eigenlijke hoofdpagina, volledig uit het sjabloon
    (DIST / "switch.html").write_text(build_switch(live), encoding="utf-8")
    print("  switch.html (hoofdpagina)")

    # lettertype, zelf gehost
    if (SITE / "fonts").exists():
        shutil.copytree(SITE / "fonts", DIST / "fonts")

    # voorbeeldrapport (vaste pagina)
    rp = SITE / "rapport"
    if rp.exists():
        (DIST / "rapport").mkdir(exist_ok=True)
        for f in rp.glob("*.html"):
            shutil.copy(f, DIST / "rapport" / f.name)
        print("  /rapport/voorbeeld.html")

    # bestelpagina's (vast)
    bp = SITE / "bestel"
    if bp.exists():
        (DIST / "bestel").mkdir(exist_ok=True)
        for f in bp.glob("*.html"):
            shutil.copy(f, DIST / "bestel" / f.name)
        print("  /bestel/")

    # het verhaal van FOSS4G NL (vaste pagina, de hoofdpagina linkt ernaar)
    tp = SITE / "talk"
    if tp.exists():
        shutil.copytree(tp, DIST / "talk")
        print("  /talk/")

    # scanpagina
    (DIST / "scan").mkdir(exist_ok=True)
    (DIST / "scan" / "index.html").write_text(build_scan(), encoding="utf-8")
    print("  /scan/")

    write_sitemap(live)
    print(f"\nKlaar. De site staat in {DIST}")


def write_sitemap(live):
    """lastmod: de bouwdatum voor de pagina's die bij elke bouw veranderen,
    de publicatiedatum voor cases, zodat Google de waarde serieus neemt."""
    urls = [(f"{BASE}/switch.html", "1.0", "weekly", TODAY),
            (f"{BASE}/", "0.5", "monthly", TODAY),
            (f"{BASE}/scan/", "0.9", "monthly", TODAY)]
    if (SITE / "talk").exists():
        urls.append((f"{BASE}/talk/", "0.6", "yearly", "2026-07-09"))
    # /rapport/voorbeeld.html komt in de sitemap zodra bestellen open gaat
    for c in live:
        urls.append((f"{BASE}/cases/{c['id']}/", "0.8", "monthly", case_datum(c)))
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{datum}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        for u, pri, freq, datum in urls)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n", encoding="utf-8")
    print(f"  sitemap.xml met {len(urls)} adressen")


if __name__ == "__main__":
    build()
