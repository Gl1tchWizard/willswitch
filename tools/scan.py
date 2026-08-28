"""De scanpagina.

Nu nog een vindbare landingspagina met de uitleg. De vragen en de
uitkomst komen hier later in, op dezelfde plek en hetzelfde adres.
"""

PAGE = '''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Autonomie-scan: waar staat jouw organisatie? | Will Switch</title>
  <meta name="description" content="Breng in kaart hoe afhankelijk je organisatie is van Big Tech, waar je ruimte hebt en wat een logische eerste stap is. Gratis, zonder registratie.">
  <link rel="canonical" href="https://willswitch.nl/scan/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="Autonomie-scan: waar staat jouw organisatie?">
  <meta property="og:description" content="Breng in kaart hoe afhankelijk je organisatie is van Big Tech en wat een logische eerste stap is.">
  <meta property="og:image" content="https://willswitch.nl/og-image.jpg">
  <meta property="og:url" content="https://willswitch.nl/scan/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Space+Mono&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Autonomie-scan",
    "description": "Breng in kaart hoe afhankelijk je organisatie is van Big Tech en wat een logische eerste stap is.",
    "url": "https://willswitch.nl/scan/",
    "isPartOf": { "@type": "WebSite", "name": "Will Switch", "url": "https://willswitch.nl/" }
  }
  </script>
  <style>
    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    :root {
      --orange:#E84500; --paper:#F0EDE6; --paper-warm:#E8E3D6;
      --ink:#1a1612; --ink-soft:#4a443c; --ink-faint:rgba(26,22,18,0.45);
      --rule:rgba(26,22,18,0.12);
    }
    body { background:var(--paper); color:var(--ink);
      font-family:'Space Mono', monospace; line-height:1.6; }
    .topbar {
      display:flex; justify-content:space-between; align-items:center;
      max-width:46rem; margin:0 auto; padding:2rem 1.5rem 0;
      font-family:'Orbitron', monospace; font-size:0.7rem;
      letter-spacing:0.25em; text-transform:uppercase;
    }
    .topbar a { color:var(--ink-faint); text-decoration:none; }
    .topbar a:hover { color:var(--orange); }
    .topbar .brand { color:var(--ink); }
    main { max-width:46rem; margin:0 auto; padding:3.5rem 1.5rem 4rem; }
    .marker {
      font-family:'Orbitron', monospace; font-size:0.68rem;
      letter-spacing:0.28em; text-transform:uppercase;
      color:var(--orange); margin-bottom:1.2rem;
    }
    h1 {
      font-family:'Orbitron', monospace;
      font-size:clamp(1.7rem, 4.2vw, 2.6rem); font-weight:700;
      line-height:1.15; margin-bottom:1.4rem;
    }
    p { font-size:0.95rem; color:var(--ink-soft); margin-bottom:1.1rem; max-width:40rem; }
    p.lead { font-size:1.08rem; color:var(--ink); }
    h2 {
      font-family:'Orbitron', monospace; font-size:1.15rem;
      margin:2.5rem 0 0.9rem;
    }
    ol { margin:0 0 1.5rem 1.2rem; }
    ol li { font-size:0.95rem; color:var(--ink-soft); margin-bottom:0.7rem; }
    .panel {
      margin-top:2.5rem; padding:2rem 1.85rem;
      background:var(--paper-warm); border:1px solid var(--rule); border-radius:4px;
    }
    .panel h2 { margin-top:0; }
    .soon {
      display:inline-block; font-family:'Orbitron', monospace;
      font-size:0.62rem; letter-spacing:0.16em; text-transform:uppercase;
      color:var(--orange); border:1px solid rgba(232,69,0,0.45);
      background:rgba(232,69,0,0.08); padding:0.25rem 0.6rem;
      border-radius:2px; margin-bottom:0.9rem;
    }
    .cta {
      display:inline-block; margin-top:0.9rem;
      background:var(--orange); color:var(--paper); text-decoration:none;
      font-family:'Orbitron', monospace; font-size:0.75rem; font-weight:700;
      letter-spacing:0.12em; text-transform:uppercase;
      padding:0.95rem 1.6rem; border-radius:3px;
    }
    .cta:hover { background:var(--ink); }
    .cta.ghost {
      background:transparent; color:var(--orange);
      border:1px solid rgba(232,69,0,0.5);
    }
    .cta.ghost:hover { background:var(--orange); color:var(--paper); }
    footer {
      max-width:46rem; margin:0 auto; padding:2rem 1.5rem 3rem;
      border-top:1px solid var(--rule);
      display:flex; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;
      font-size:0.68rem; letter-spacing:0.1em; text-transform:uppercase;
      color:var(--ink-faint);
    }
    footer a { color:var(--ink-faint); }
    @media (max-width:600px) { footer { flex-direction:column; } }
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/">Will Switch</a>
    <a href="/switch.html">praktijkverhalen</a>
  </header>

  <main>
    <p class="marker">autonomie-scan</p>
    <h1>Waar staat jouw organisatie?</h1>

    <p class="lead">De meeste organisaties weten wel dat ze afhankelijk zijn.
    Wat ze niet weten is hoe erg, waar precies, en welke stap het meest
    oplevert. Daar is deze scan voor.</p>

    <p>Uit de gesprekken voor dit onderzoek komt steeds hetzelfde beeld naar
    voren: de techniek is zelden het probleem. Het loopt vast op de vraagkant.
    Op wat er wordt uitgevraagd, op wie zich eigenaar voelt van de stap, en op
    de aanname dat overstappen alles tegelijk betekent.</p>

    <h2>Wat de scan doet</h2>
    <ol>
      <li>Brengt in kaart waar je afhankelijkheden zitten en hoe zwaar ze wegen.</li>
      <li>Laat zien waar je nu al ruimte hebt, ook zonder groot migratieproject.</li>
      <li>Geeft een logische eerste stap die past bij waar je staat.</li>
      <li>Zet je uitkomst naast die van vergelijkbare organisaties.</li>
    </ol>

    <div class="panel">
      <span class="soon">binnenkort</span>
      <h2>De scan wordt nu gebouwd</h2>
      <p>De vragen komen rechtstreeks uit het onderzoek en worden getoetst met
      de organisaties die eraan meewerken. Zodra de scan klaar is, staat hij
      hier.</p>
      <p>In de tussentijd: de praktijkverhalen laten zien wat er elders al
      gebeurt, en wat daar wel en niet werkte.</p>
      <a class="cta" href="/switch.html">Bekijk de praktijkverhalen</a>
    </div>

    <h2>Voor wie</h2>
    <p>Voor gemeenten, waterschappen, provincies, kennisinstellingen en andere
    publieke organisaties die willen weten waar ze staan. De scan is gratis en
    vraagt geen registratie.</p>
  </main>

  <footer>
    <span>Will Switch &middot; willswitch.nl</span>
    <span>Onderzoek met steun van het <a href="https://www.sidn.nl/pioniersfonds" target="_blank" rel="noopener">SIDN Pioniersfonds</a></span>
  </footer>
</body>
</html>
'''


def build_scan():
    return PAGE
