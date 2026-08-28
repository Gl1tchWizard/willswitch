"""Bouw de site uit de bronbestanden in content/cases/.

Draai: python3 tools/build.py
Resultaat komt in dist/ en is klaar om te publiceren.
"""
import json, pathlib, re, datetime, shutil, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from library import build_library
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
        raw = f.read_text()
        m = re.match(r"---\n(.*?)\n---\n\n(.*)", raw, re.S)
        if not m:
            print(f"  overgeslagen (geen kop): {f.name}")
            continue
        meta = json.loads(m.group(1))
        meta["body"] = m.group(2).strip()
        out.append(meta)
    out.sort(key=lambda c: c.get("order", 999))
    return out


def is_published(case):
    d = case.get("publish_on")
    if not d:
        return True
    return datetime.date.fromisoformat(d) <= TODAY


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def description(case):
    txt = case.get("card_body") or strip_tags(case["body"])
    return (txt[:157] + "...") if len(txt) > 160 else txt


# ---------- de losse casepagina ----------
PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Will Switch</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{base}/cases/{id}/">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{base}/og-image.jpg">
  <meta property="og:url" content="{base}/cases/{id}/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Space+Mono&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {headline_json},
    "description": {description_json},
    "datePublished": "{published}",
    "author": {{ "@type": "Person", "name": "Govert Schoof" }},
    "publisher": {{ "@type": "Organization", "name": "Will Switch", "url": "{base}/" }},
    "mainEntityOfPage": "{base}/cases/{id}/"
  }}
  </script>
  <style>
{css}
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/">Will Switch</a>
    <a href="/switch.html">alle praktijkverhalen</a>
  </header>

  <main class="case">
    <p class="eyebrow">{eyebrow}</p>
    <h1>{title}</h1>
    {body}

    <section class="next">
      <h2>Waar staat jouw organisatie?</h2>
      <p>Deze verhalen laten zien wat er mogelijk is. De volgende vraag is
      wat er bij jou speelt. De scan brengt in kaart waar je staat en wat
      een logische eerste stap is.</p>
      <a class="cta" href="/scan/">Doe de autonomie-scan</a>
    </section>

    <nav class="more">
      <span>Meer praktijkverhalen</span>
      <ul>
{related}
      </ul>
    </nav>
  </main>

  <footer>
    <span>Will Switch &middot; willswitch.nl</span>
    <span>Onderzoek met steun van het <a href="https://www.sidn.nl/pioniersfonds" target="_blank" rel="noopener">SIDN Pioniersfonds</a></span>
  </footer>
</body>
</html>
"""

CSS = """
    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    :root {
      --orange:#E84500; --paper:#F0EDE6; --paper-warm:#E8E3D6;
      --ink:#1a1612; --ink-soft:#4a443c; --ink-faint:rgba(26,22,18,0.45);
      --rule:rgba(26,22,18,0.12);
    }
    body {
      background:var(--paper); color:var(--ink);
      font-family:'Space Mono', monospace; line-height:1.6;
    }
    .topbar {
      display:flex; justify-content:space-between; align-items:center;
      max-width:44rem; margin:0 auto; padding:2rem 1.5rem 0;
      font-family:'Orbitron', monospace; font-size:0.7rem;
      letter-spacing:0.25em; text-transform:uppercase;
    }
    .topbar a { color:var(--ink-faint); text-decoration:none; }
    .topbar a:hover { color:var(--orange); }
    .topbar .brand { color:var(--ink); }
    main.case { max-width:44rem; margin:0 auto; padding:3rem 1.5rem 4rem; }
    .eyebrow {
      font-family:'Orbitron', monospace; font-size:0.66rem;
      letter-spacing:0.18em; text-transform:uppercase;
      color:var(--orange); margin-bottom:0.8rem;
    }
    h1 {
      font-family:'Orbitron', monospace;
      font-size:clamp(1.6rem, 4vw, 2.4rem); font-weight:700;
      line-height:1.15; margin-bottom:1.6rem;
    }
    main.case h3 {
      font-family:'Orbitron', monospace; font-size:1.15rem; font-weight:700;
      margin:2.4rem 0 0.9rem; color:var(--ink);
    }
    main.case p { font-size:0.95rem; color:var(--ink-soft); margin-bottom:1.1rem; }
    main.case p a { color:var(--orange); text-decoration:none;
      border-bottom:1px solid rgba(232,69,0,0.4); }
    main.case p a:hover { color:var(--ink); border-color:var(--ink); }
    .case-quote {
      font-size:1.05rem; color:var(--orange); font-weight:700;
      padding-left:1rem; border-left:3px solid var(--orange); margin:1.6rem 0;
    }
    figure { margin:1.8rem 0; }
    figure img { width:100%; height:auto; display:block;
      border-radius:6px; border:1px solid var(--rule); }
    .case-cap { font-size:0.72rem; color:var(--ink-faint); margin-top:0.5rem; }
    .case-credit {
      margin-top:1.8rem; padding-top:1.2rem; border-top:1px solid var(--rule);
      font-size:0.8rem; color:var(--ink-faint);
    }
    .case-credit a, .case-link-wrap a { color:var(--orange); text-decoration:none;
      border-bottom:1px solid rgba(232,69,0,0.4); }
    .case-link-wrap { margin-top:1.6rem; }
    .next {
      margin-top:3.5rem; padding:2rem 1.75rem;
      background:var(--paper-warm); border:1px solid var(--rule); border-radius:4px;
    }
    .next h2 {
      font-family:'Orbitron', monospace; font-size:1.1rem;
      margin-bottom:0.8rem;
    }
    .next p { font-size:0.9rem; }
    .cta {
      display:inline-block; margin-top:0.8rem;
      background:var(--orange); color:var(--paper); text-decoration:none;
      font-family:'Orbitron', monospace; font-size:0.75rem; font-weight:700;
      letter-spacing:0.12em; text-transform:uppercase;
      padding:0.9rem 1.5rem; border-radius:3px;
    }
    .cta:hover { background:var(--ink); }
    .more { margin-top:3rem; padding-top:1.5rem; border-top:1px solid var(--rule); }
    .more span {
      font-family:'Orbitron', monospace; font-size:0.62rem;
      letter-spacing:0.16em; text-transform:uppercase; color:var(--ink-faint);
    }
    .more ul { list-style:none; margin-top:0.8rem; }
    .more li { margin-bottom:0.5rem; }
    .more a { color:var(--ink); text-decoration:none; font-size:0.9rem;
      border-bottom:1px solid var(--rule); }
    .more a:hover { color:var(--orange); border-color:var(--orange); }
    footer {
      max-width:44rem; margin:0 auto; padding:2rem 1.5rem 3rem;
      border-top:1px solid var(--rule);
      display:flex; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;
      font-size:0.68rem; letter-spacing:0.1em; text-transform:uppercase;
      color:var(--ink-faint);
    }
    footer a { color:var(--ink-faint); }
    @media (max-width:600px) { footer { flex-direction:column; } }
"""


def build():
    cases = load_cases()
    live = [c for c in cases if is_published(c)]
    print(f"{len(cases)} cases, waarvan {len(live)} gepubliceerd op {TODAY}")

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    # vaste bestanden meenemen
    for f in SITE.glob("*"):
        if f.is_file():
            shutil.copy(f, DIST / f.name)

    # casepagina's
    for c in live:
        others = [o for o in live if o["id"] != c["id"]][:4]
        related = "\n".join(
            f'        <li><a href="/cases/{o["id"]}/">{o["title"]}</a></li>'
            for o in others)
        # relatieve paden naar de root omzetten, de casepagina staat dieper
        body = re.sub(r'href="\?case=([a-z]+)"', r'href="/cases/\1/"', c["body"])
        body = re.sub(r'(src|href)="(?!https?://|/|#)', r'\1="/', body)
        d = description(c)
        page = PAGE.format(
            id=c["id"],
            title=c["title"],
            eyebrow=c.get("eyebrow", ""),
            description=d.replace('"', "&quot;"),
            headline_json=json.dumps(c["title"], ensure_ascii=False),
            description_json=json.dumps(d, ensure_ascii=False),
            published=c.get("publish_on") or c.get("new_since") or "2026-07-01",
            body=body,
            related=related,
            base=BASE,
            css=CSS,
        )
        out = DIST / "cases" / c["id"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page)
        print(f"  /cases/{c['id']}/")

    # homepage met inhoud onder het portaal
    home = SITE / "index.html"
    if home.exists():
        (DIST / "index.html").write_text(build_home(home.read_text(), live))
        print("  index.html (homepage)")

    # casebibliotheek met links naar de eigen pagina's
    src = SITE / "switch.html"
    if src.exists():
        (DIST / "switch.html").write_text(build_library(src.read_text(), live))
        print("  switch.html (casebibliotheek)")

    # scanpagina
    (DIST / "scan").mkdir(exist_ok=True)
    (DIST / "scan" / "index.html").write_text(build_scan())
    print("  /scan/")

    write_sitemap(live)
    print(f"\nKlaar. De site staat in {DIST}")


def write_sitemap(live):
    urls = [(f"{BASE}/", "1.0", "weekly"),
            (f"{BASE}/switch.html", "0.9", "weekly"),
            (f"{BASE}/scan/", "0.9", "monthly")]
    for c in live:
        urls.append((f"{BASE}/cases/{c['id']}/", "0.8", "monthly"))
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>"
        for u, pri, freq in urls)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n")
    print(f"  sitemap.xml met {len(urls)} adressen")


if __name__ == "__main__":
    build()
