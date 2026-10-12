"""De gratis scan op /scan/.

Vier stappen: wie en waarvoor, de belangrijkste systemen met vier feiten per systeem,
vijf vragen over de organisatie, en een uitslag met hooguit drie aandachtspunten
(jouw antwoord, mogelijk gevolg, eerste actie). Geen scores, geen kleuren voor goed of fout.

Vragen over de organisatie en vragen per systeem blijven gescheiden: uit een antwoord
voor de hele organisatie trekken we geen conclusie over een systeem.

Alles draait in de browser. Alleen geaggregeerde tellingen gaan naar de server,
nooit leveranciersnamen of vrije tekst.
"""

PAGE = r'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gratis scan: hoe afhankelijk ben je van je ICT-leveranciers? | Will Switch</title>
  <meta name="description" content="Gratis scan voor gemeenten, waterschappen en andere publieke organisaties. Ontdek in tien minuten waar je afhankelijk bent van ICT-leveranciers, wat je daarover nog niet weet en waar je het beste kunt beginnen. Geen account nodig.">
  <link rel="canonical" href="https://willswitch.nl/scan/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="Als je ICT-leverancier de prijs verhoogt, de voorwaarden verandert of stopt: wat kun je dan nog?">
  <meta property="og:description" content="Gratis scan voor gemeenten en waterschappen. In tien minuten zie je waar je afhankelijk bent, wat je nog niet weet en waar je begint.">
  <meta property="og:image" content="https://willswitch.nl/og-image.jpg">
  <meta property="og:url" content="https://willswitch.nl/scan/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Space+Grotesk:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Scan ICT-afhankelijkheid",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" },
    "description": "Gratis scan voor publieke organisaties: waar ben je afhankelijk van ICT-leveranciers, wat weet je nog niet en waar begin je.",
    "url": "https://willswitch.nl/scan/",
    "provider": { "@type": "Organization", "name": "Will Switch", "url": "https://willswitch.nl/" }
  }
  </script>
  <style>
    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    :root {
      --orange:#E84500; --knop:#C23A00; --paper:#F0EDE6; --warm:#E8E3D6; --white:#FBFAF7;
      --ink:#1a1612; --soft:#4a443c; --faint:#6f685e; --rule:rgba(26,22,18,0.14);
      --sans:'Space Grotesk', system-ui, sans-serif; --mono:'Space Mono', monospace; --merk:'Orbitron', sans-serif;
    }
    html { font-size:17px; }
    body { background:var(--paper); color:var(--ink); font-family:var(--sans); line-height:1.55; }
    .wrap { max-width:46rem; margin:0 auto; padding:0 1.5rem 5rem; }
    a { color:var(--ink); }
    .topbar { display:flex; justify-content:space-between; align-items:center; padding:1.6rem 0 1rem; border-bottom:2px solid var(--ink); }
    .topbar a { font-family:var(--merk); font-weight:700; font-size:0.78rem; letter-spacing:0.16em; text-transform:uppercase; text-decoration:none; }
    .topbar a:hover { color:var(--orange); }
    .topbar span { font-family:var(--mono); font-size:0.74rem; color:var(--faint); }

    .stappen { display:flex; gap:5px; margin:1.4rem 0 2.2rem; }
    .stappen i { flex:1; height:4px; background:var(--rule); }
    .stappen i.aan { background:var(--orange); }

    h1 { font-size:clamp(1.85rem, 4.6vw, 2.75rem); font-weight:700; line-height:1.1; letter-spacing:-0.015em; margin:2.2rem 0 1rem; }
    h2 { font-size:clamp(1.25rem, 3vw, 1.55rem); font-weight:700; line-height:1.2; letter-spacing:-0.01em; margin-bottom:0.7rem; }
    h3 { font-size:1.05rem; font-weight:700; margin:1.6rem 0 0.5rem; }
    p { color:var(--soft); margin-bottom:1rem; max-width:40rem; }
    p.lead { color:var(--ink); font-size:1.15rem; line-height:1.5; }
    .klein { font-size:0.85rem; color:var(--faint); }
    .label { font-family:var(--mono); font-size:0.68rem; letter-spacing:0.05em; text-transform:uppercase; color:var(--faint); }
    section.blok { margin-top:3rem; }

    button { font:inherit; cursor:pointer; }
    .b-primair, a.b-primair { display:inline-block; background:var(--knop); color:#fff; border:none; border-radius:3px; padding:0.95rem 1.5rem; font-weight:700; font-size:1rem; text-decoration:none; }
    .b-primair:hover:not(:disabled) { background:var(--ink); }
    .b-primair:disabled { opacity:0.35; cursor:not-allowed; }
    .b-tweede, a.b-tweede { display:inline-block; background:transparent; color:var(--ink); border:1px solid var(--ink); border-radius:3px; padding:0.9rem 1.3rem; font-weight:500; text-decoration:none; }
    .b-tweede:hover { background:var(--ink); color:var(--paper); }
    .b-stil { background:none; border:none; color:var(--faint); padding:0.9rem 0.4rem; }
    .b-stil:hover { color:var(--ink); }
    button:focus-visible, a:focus-visible { outline:3px solid var(--orange); outline-offset:2px; }
    .start { display:flex; align-items:center; gap:1.2rem; flex-wrap:wrap; margin:1.6rem 0 0.4rem; }
    .start .klein { margin:0; }
    .nav { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-top:2rem; }

    /* herken je dit */
    .tabs { display:flex; gap:0.4rem; margin:0.8rem 0 1rem; }
    .tabs button { background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:0.45rem 0.9rem; font-size:0.9rem; color:var(--soft); }
    .tabs button[aria-pressed="true"] { background:var(--ink); border-color:var(--ink); color:var(--paper); }
    .herken { list-style:none; display:grid; grid-template-columns:1fr 1fr; gap:0.6rem; }
    .herken li { background:var(--white); border:1px solid var(--rule); padding:0.9rem 1rem; font-size:0.95rem; line-height:1.45; }
    @media (max-width:600px) { .herken { grid-template-columns:1fr; } }

    /* keuzes */
    .keuzes { display:grid; gap:0.5rem; margin:0.8rem 0 1.4rem; }
    .keuzes.twee { grid-template-columns:1fr 1fr; }
    .keuze { display:flex; align-items:center; gap:0.7rem; background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:0.8rem 1rem; text-align:left; color:var(--ink); font-size:0.95rem; }
    .keuze:hover { border-color:var(--ink); }
    .keuze .rond { width:16px; height:16px; border:2px solid var(--faint); border-radius:50%; flex:none; }
    .keuze[aria-pressed="true"] { border-color:var(--ink); box-shadow:inset 0 0 0 1px var(--ink); }
    .keuze[aria-pressed="true"] .rond { border-color:var(--ink); background:radial-gradient(circle, var(--ink) 45%, transparent 50%); }
    @media (max-width:560px) { .keuzes.twee { grid-template-columns:1fr; } }

    .kaart { display:grid; grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); gap:0.5rem; margin:1rem 0 0.6rem; }
    .tegel { position:relative; background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:0.8rem 0.85rem 1.6rem; min-height:84px; text-align:left; color:var(--ink); font-size:0.9rem; font-weight:500; line-height:1.3; }
    .tegel:hover { border-color:var(--ink); }
    .tegel[aria-pressed="true"] { border-color:var(--ink); box-shadow:inset 0 0 0 1px var(--ink); }
    .tegel .st { position:absolute; left:0.85rem; bottom:0.55rem; font-family:var(--mono); font-size:0.64rem; letter-spacing:0.04em; text-transform:uppercase; color:var(--faint); }

    .sysblok { background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:1.1rem 1.2rem; margin-bottom:0.9rem; }
    .sysblok > b { display:block; font-size:1.02rem; margin-bottom:0.2rem; }
    .vraagje { font-size:0.92rem; margin:0.85rem 0 0.4rem; color:var(--ink); }
    .vraagje i { font-style:normal; color:var(--faint); font-size:0.85rem; }
    .opties { display:flex; flex-wrap:wrap; gap:0.35rem; }
    .opties button { background:var(--paper); color:var(--soft); border:1px solid var(--rule); border-radius:3px; padding:0.45rem 0.7rem; font-size:0.88rem; }
    .opties button:hover { border-color:var(--ink); color:var(--ink); }
    .opties button[aria-pressed="true"] { background:var(--ink); color:var(--paper); border-color:var(--ink); }

    .vraagkaart { background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:1.1rem 1.2rem; margin-bottom:0.8rem; }
    .vraagkaart .tekst { font-size:1rem; color:var(--ink); margin-bottom:0.7rem; }
    .vraagkaart details { margin-top:0.6rem; font-size:0.86rem; color:var(--faint); }
    .vraagkaart summary { cursor:pointer; color:var(--soft); }
    .vraagkaart details p { font-size:0.86rem; color:var(--faint); margin:0.4rem 0 0; }
    .antw { display:grid; grid-template-columns:repeat(4, 1fr); gap:0.35rem; }
    .antw button { background:var(--paper); color:var(--soft); border:1px solid var(--rule); border-radius:3px; padding:0.55rem 0.3rem; font-size:0.9rem; }
    .antw button:hover { border-color:var(--ink); color:var(--ink); }
    .antw button[aria-pressed="true"] { background:var(--ink); color:var(--paper); border-color:var(--ink); }
    @media (max-width:480px) { .antw { grid-template-columns:1fr 1fr; } }

    /* uitslag */
    .punt { background:var(--white); border:1px solid var(--rule); border-left:4px solid var(--ink); padding:1.1rem 1.25rem 1.2rem; margin-bottom:0.9rem; }
    .punt .kop { display:flex; justify-content:space-between; align-items:baseline; gap:1rem; }
    .punt h3 { margin:0; font-size:1.1rem; line-height:1.3; }
    .punt .nr { font-family:var(--mono); color:var(--faint); margin-right:0.4rem; }
    .chip { font-family:var(--mono); font-size:0.64rem; letter-spacing:0.05em; text-transform:uppercase; border:1px solid currentColor; padding:0.12rem 0.45rem; white-space:nowrap; }
    .chip.gemeld { color:#7a5a12; }
    .chip.onbekend { color:var(--soft); border-style:dashed; }
    .punt dl { display:grid; grid-template-columns:9rem 1fr; gap:0.5rem 1rem; margin-top:0.85rem; }
    .punt dt { font-family:var(--mono); font-size:0.68rem; letter-spacing:0.04em; text-transform:uppercase; color:var(--faint); padding-top:0.25rem; }
    .punt dd { font-size:0.97rem; color:var(--ink); }
    .punt dd.actie { font-weight:700; }
    .punt.dicht dl { display:none; }
    @media (max-width:560px) { .punt dl { grid-template-columns:1fr; gap:0.15rem; } .punt dt { padding-top:0.5rem; } }
    .voorbeeld { border:1px dashed var(--faint); padding:1rem; background:rgba(251,250,247,0.5); }
    .voorbeeld .label { display:block; margin-bottom:0.7rem; }

    .overzicht { width:100%; border-collapse:collapse; font-size:0.88rem; margin:0.6rem 0 0.4rem; }
    .overzicht th { text-align:left; font-family:var(--mono); font-size:0.66rem; font-weight:400; letter-spacing:0.04em; text-transform:uppercase; color:var(--faint); padding:0.4rem 0.5rem; border-bottom:1px solid var(--ink); }
    .overzicht td { padding:0.55rem 0.5rem; border-bottom:1px solid var(--rule); vertical-align:top; }
    .overzicht td.onb { color:var(--faint); font-style:italic; }
    .tabelrol { overflow-x:auto; }
    .open { background:var(--white); border:1px solid var(--rule); padding:1rem 1.2rem; margin:0.6rem 0; }
    .open ol { margin-left:1.2rem; }
    .open li { margin-bottom:0.35rem; font-size:0.95rem; }
    .duo { background:var(--white); border:1px dashed var(--faint); padding:1.1rem 1.2rem; margin:1rem 0; }
    .duo input { width:100%; font-family:var(--mono); font-size:0.8rem; padding:0.6rem 0.7rem; border:1px solid var(--rule); background:var(--paper); margin-top:0.6rem; }
    .kloof { margin-top:0.8rem; }
    .kloof .gv { border-top:1px solid var(--rule); padding:0.7rem 0; }
    .kloof .gv b { display:block; font-size:0.95rem; }
    .kloof .gv span { display:block; font-size:0.88rem; color:var(--soft); }
    .vervolg { background:var(--warm); border:1px solid var(--rule); padding:1.5rem; margin:2.4rem 0 1rem; }
    .vervolg .status { display:inline-block; font-family:var(--mono); font-size:0.7rem; letter-spacing:0.05em; text-transform:uppercase; border:1px solid var(--soft); color:var(--soft); padding:0.15rem 0.5rem; margin-bottom:0.8rem; }
    .vervolg ul { margin:0.4rem 0 1.2rem 1.2rem; }
    .vervolg li { margin-bottom:0.3rem; font-size:0.95rem; }
    .vervolg li.past { font-weight:700; }
    .vervolg .knoppen { display:flex; gap:0.6rem; flex-wrap:wrap; }

    details.wet { background:var(--white); border-left:3px solid var(--orange); padding:0.9rem 1.1rem; margin:0.8rem 0; }
    details.wet summary { cursor:pointer; font-weight:700; }
    details.wet p { font-size:0.92rem; margin:0.7rem 0 0; }
    details.wet .bron { font-size:0.8rem; color:var(--faint); }

    .toast { position:fixed; left:50%; bottom:1.5rem; transform:translateX(-50%); background:var(--ink); color:var(--paper); padding:0.8rem 1.2rem; font-size:0.9rem; opacity:0; pointer-events:none; transition:opacity 0.3s; max-width:90vw; text-align:center; }
    .toast.zien { opacity:1; }
    .verborgen { display:none !important; }
    footer { margin-top:3rem; padding-top:1.2rem; border-top:1px solid var(--rule); font-size:0.82rem; color:var(--faint); line-height:1.7; }
    @media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
  </style>
</head>
<body>
<div class="wrap">
  <header class="topbar">
    <a href="/switch.html">Will Switch</a>
    <span>gratis scan</span>
  </header>
  <div class="stappen verborgen" id="stappen" aria-hidden="true"><i></i><i></i><i></i><i></i></div>

  <!-- 0 · opening -->
  <section id="s0">
    <h1>Als je ICT-leverancier de prijs verhoogt, de voorwaarden verandert of stopt: wat kun je dan nog?</h1>
    <p class="lead">Ontdek in tien minuten waar je gemeente of waterschap afhankelijk is van ICT-leveranciers, wat je daarover nog niet weet en waar je het beste kunt beginnen.</p>
    <div class="start">
      <button class="b-primair" onclick="naar(1)">Start de gratis scan</button>
      <p class="klein">10 minuten. Geen account. Je antwoorden blijven in je browser.</p>
    </div>

    <section class="blok" aria-labelledby="herken-kop">
      <h2 id="herken-kop">Herken je dit?</h2>
      <div class="tabs" role="group" aria-label="Type organisatie">
        <button type="button" aria-pressed="true" data-tab="gemeente">Gemeente</button>
        <button type="button" aria-pressed="false" data-tab="waterschap">Waterschap</button>
      </div>
      <ul class="herken" data-voor="gemeente">
        <li>Het contract voor het zaaksysteem loopt volgend jaar af. Niemand weet precies wat erin staat over verlengen.</li>
        <li>De licenties voor de kantoorsoftware worden duurder, en een alternatief is nooit bekeken.</li>
        <li>De belastingapplicatie draait bij één leverancier en twee collega's weten hoe het werkt.</li>
        <li>Het bestuur vraagt om een risicoanalyse van de leveranciers, en je weet niet waar je moet beginnen.</li>
      </ul>
      <ul class="herken verborgen" data-voor="waterschap">
        <li>De besturing van de gemalen hangt aan één leverancier. Wat er gebeurt als die stopt, staat nergens.</li>
        <li>Het pakket voor heffing en invordering moet opnieuw worden aanbesteed, en niemand kent het contract van binnen.</li>
        <li>De leverancier gaat over op alleen nog cloud, met nieuwe voorwaarden en een nieuwe prijs.</li>
        <li>Het bestuur vraagt om een risicoanalyse van de leveranciers, en je weet niet waar je moet beginnen.</li>
      </ul>
    </section>

    <section class="blok" aria-labelledby="uitkomst-kop">
      <h2 id="uitkomst-kop">Wat je na tien minuten hebt</h2>
      <p>Hooguit drie aandachtspunten, steeds met jouw antwoord, wat dat kan betekenen en een eerste actie. Daaronder een overzicht van je antwoorden en een lijst met wat je nog niet weet.</p>
      <div class="voorbeeld">
        <span class="label">Voorbeeld van een uitslag, fictieve gemeente</span>
        <div class="punt">
          <div class="kop"><h3><span class="nr">1</span>Wat als het zaaksysteem een week uitvalt?</h3><span class="chip gemeld">gemeld</span></div>
          <dl>
            <dt>Jouw antwoord</dt><dd>Als het zaaksysteem een week niet werkt, ligt het werk volgens jou stil bij vergunningen en het sociaal domein. Scenario's voor het wegvallen van een leverancier zijn er in het algemeen niet.</dd>
            <dt>Mogelijk gevolg</dt><dd>Bij een storing, faillissement of gedwongen overstap moet je dan improviseren, terwijl inwoners er direct last van hebben.</dd>
            <dt>Eerste actie</dt><dd class="actie">Schrijf voor het zaaksysteem op één A4 wat er gebeurt als de leverancier stopt: wat valt stil, hoe werk je tijdelijk door en wie neemt welk besluit.</dd>
          </dl>
        </div>
        <div class="punt dicht"><div class="kop"><h3><span class="nr">2</span>Het contract voor de cloudomgeving loopt binnen een jaar af</h3><span class="chip gemeld">gemeld</span></div></div>
        <div class="punt dicht"><div class="kop"><h3><span class="nr">3</span>Waar zit de kennis?</h3><span class="chip onbekend">nog onbekend</span></div></div>
      </div>
    </section>

    <section class="blok" aria-labelledby="waarom-kop">
      <h2 id="waarom-kop">Waarom dit nu speelt</h2>
      <p>Afhankelijkheid van leveranciers is geen nieuw onderwerp. Wel nieuw is dat drie kaders er tegelijk naar vragen.</p>
      <details class="wet">
        <summary>Cyberbeveiligingswet, Data Act en rijksbreed cloudbeleid</summary>
        <p><b>Cyberbeveiligingswet</b>, van kracht sinds 15 augustus 2026. Vraagt onder meer beleid voor de beveiliging van je leveranciersketen, en het bestuur moet de maatregelen goedkeuren. De RDI adviseert daarbij per leverancier te bepalen wat het betekent als die wegvalt, en af te spreken wat er met je gegevens gebeurt bij contracteinde, faillissement of overname. Geldt voor onder meer gemeenten, provincies en waterschappen. Veiligheidsregio's vallen er niet onder.</p>
        <p><b>Data Act</b>, van toepassing sinds 12 september 2025. Geeft je als afnemer van clouddiensten het recht om over te stappen. Vanaf 12 januari 2027 mag de leverancier daar geen overstapkosten meer voor rekenen.</p>
        <p><b>Rijksbreed cloudbeleid</b>, vastgesteld 3 juli 2026. Beleid, geen wet. Het vraagt van rijksorganisaties een exitplan per clouddienst, ook voor het geval dat een dienst plotseling wegvalt. Voor gemeenten, provincies en waterschappen geldt het niet verplicht; andere overheden wordt aangeraden het te volgen, en het kabinet wil met hen naar overheidsbreed cloudbeleid.</p>
        <p class="bron">Bronnen: Cyberbeveiligingswet (Stb. 2026, 187), art. 5, 8, 21 en 24; Cyberbeveiligingsbesluit (Stb. 2026, 189), art. 10 en 35; RDI, toeleveringsketen en cyberbeveiliging; Verordening (EU) 2023/2854, art. 25, 29, 30 en 50; Kamerbrief Herziening Rijksbreed Cloudbeleid 2026 (26 643, nr. 1541). Gecontroleerd op 9 oktober 2026. Dit is geen juridisch advies.</p>
      </details>
    </section>

    <section class="blok" aria-labelledby="daarna-kop">
      <h2 id="daarna-kop">En daarna?</h2>
      <p>Will Switch onderzocht wat publieke organisaties nodig hebben om grip te krijgen op hun ICT-leveranciers. In fase twee helpen we mee: we werken je antwoorden uit tot een dossier met een risicoanalyse, een beslisnotitie en een actielijst, voor €750 excl. btw. De eerste organisaties doen mee als pilot en bepalen mee hoe het dossier eruit komt te zien.</p>
      <p><a href="/rapport/voorbeeld.html" id="link-voorbeeld">Bekijk het voorbeeld van een uitgewerkt dossier</a> of <a href="/pilot/">lees wat de pilot inhoudt</a>.</p>
    </section>

    <div class="start">
      <button class="b-primair" onclick="naar(1)">Start de gratis scan</button>
    </div>
    <p class="klein" style="margin-top:1.2rem">De scan werkt met je eigen antwoorden. Niets wordt gecontroleerd aan de hand van documenten en er komt geen oordeel over naleving uit. Bij de uitslag sturen we alleen tellingen mee, zoals je organisatietype en het aantal systemen. Geen namen, geen leveranciers, geen vrije tekst.</p>
  </section>

  <!-- 1 · wie en waarvoor -->
  <section id="s1" class="verborgen">
    <h2>Voor welke organisatie vul je dit in?</h2>
    <div class="keuzes twee" id="org"></div>
    <p class="klein" id="org-noot" style="display:none"></p>
    <h3>Wat is je rol?</h3>
    <div class="keuzes twee" id="rol"></div>
    <h3>Waarvoor wil je de uitkomst gebruiken?</h3>
    <p class="klein" style="margin-bottom:0">Dan zetten we de punten die daarbij horen bovenaan.</p>
    <div class="keuzes" id="doel"></div>
    <div class="nav"><button class="b-stil" onclick="naar(0)">Terug</button><button class="b-primair" id="k1" disabled onclick="naar(2)">Verder</button></div>
  </section>

  <!-- 2 · systemen -->
  <section id="s2" class="verborgen">
    <h2>Welke systemen zijn het belangrijkst voor jullie werk?</h2>
    <p>Kies er hooguit vijf. Per systeem stellen we vier korte vragen. Weet je iets niet, kies dan "weet ik niet": dat is ook een uitkomst.</p>
    <div class="kaart" id="kaart"></div>
    <p class="klein" id="sysstatus">Kies eerst je systemen, dan verschijnen de vragen eronder.</p>
    <div id="sysvragen"></div>
    <div class="nav"><button class="b-stil" onclick="naar(1)">Terug</button><button class="b-primair" id="k2" disabled onclick="naar(3)">Verder</button></div>
  </section>

  <!-- 3 · organisatie -->
  <section id="s3" class="verborgen">
    <h2>Vijf vragen over de organisatie als geheel</h2>
    <p>Deze gaan niet over één systeem, maar over hoe jullie het in het algemeen geregeld hebben.</p>
    <div id="orgvragen"></div>
    <div class="nav"><button class="b-stil" onclick="naar(2)">Terug</button><button class="b-primair" id="k3" disabled onclick="resultaat();naar(4)">Bekijk je uitkomst</button></div>
  </section>

  <!-- 4 · uitslag -->
  <section id="s4" class="verborgen">
    <h2>Je uitkomst</h2>
    <p id="uit-intro"></p>
    <div id="punten"></div>
    <p class="klein">Alles hierboven volgt uit je eigen antwoorden. <b>Gemeld</b> betekent: zo heb je het opgegeven, niet gecontroleerd. <b>Nog onbekend</b> betekent: hier ontbreekt informatie.</p>

    <h3>Je antwoorden per systeem</h3>
    <div class="tabelrol"><table class="overzicht" id="overzicht"></table></div>

    <h3>Wat je nog niet weet</h3>
    <div class="open" id="open"></div>

    <div class="duo" id="duo">
      <b id="duo-kop">Vergelijk met een collega</b>
      <p class="klein" style="margin:0.4rem 0 0" id="duo-tekst"></p>
      <input readonly id="duo-link" onclick="this.select()" aria-label="Link om te delen">
      <button class="b-stil" style="padding-left:0" onclick="kopieer('duo-link','Link gekopieerd')">Kopieer link</button>
      <div class="kloof verborgen" id="kloof"></div>
    </div>

    <div class="vervolg">
      <span class="status">Fase twee · pilot · €750 excl. btw</span>
      <h2>Daarna: je dossier uitwerken</h2>
      <p id="vervolg-doel"></p>
      <ul id="vervolg-lijst"></ul>
      <p>Will Switch onderzocht wat hiervoor nodig is, en helpt in fase twee concreet mee. Je vult een aanvullende vragenlijst in, en krijgt een uitgewerkt dossier voor je eigen organisatie, zoals het voorbeeld, met een bewerkbaar werkdocument. De eerste organisaties doen mee als pilot.</p>
      <div class="knoppen">
        <a class="b-primair" href="/pilot/">Meedoen met de pilot</a>
        <a class="b-tweede" href="/rapport/voorbeeld.html">Bekijk het voorbeeld</a>
        <a class="b-tweede" href="#" onclick="return mailtje('update')">Hou me op de hoogte</a>
      </div>
      <p class="klein" style="margin:0.9rem 0 0">Op de pilotpagina staan prijs, levering en voorwaarden, en een aanmeldformulier. "Hou me op de hoogte" opent je mailprogramma; je antwoorden gaan niet automatisch mee.</p>
    </div>

    <p class="klein">Deze uitkomst is een startpunt voor je eigen analyse. Er is niets gecontroleerd aan de hand van documenten. Het is geen oordeel over naleving van wet- of regelgeving, en geen juridisch advies.</p>
    <div class="nav"><button class="b-stil" onclick="location.href='/scan/'">Opnieuw beginnen</button><a href="/switch.html">Praktijkverhalen</a></div>
  </section>

  <footer>
    Will Switch, praktijkonderzoek naar digitale autonomie in de publieke sector.<br>
    Gebouwd met open source, gehost in Nederland, zonder trackingcookies.
  </footer>
</div>
<div class="toast" id="toast" role="status"></div>

<script>
'use strict';
const ORGS = [['gemeente','Gemeente'],['waterschap','Waterschap'],['provincie','Provincie'],['vr','Veiligheidsregio'],['gr','Gemeenschappelijke regeling'],['rijk','Rijksdienst of ZBO'],['kennis','Kennisinstelling'],['anders','Anders']];
const ROLLEN = [['bestuur','Bestuur of directie'],['cio','CIO, CISO of informatiemanager'],['uitvoering','Beheer, inkoop of uitvoering'],['anders','Anders']];
const DOELEN = [['risico','Een risicoanalyse, bijvoorbeeld voor de Cyberbeveiligingswet'],['verlenging','Een contract dat afloopt of verlengd wordt'],['continuiteit','Een continuïteits- of exitplan'],['bestuur','Een voorstel aan directie of bestuur'],['orientatie','Oriënteren, nog geen concreet dossier']];
const DOELNAAM = {risico:'een risicoanalyse', verlenging:'een contractverlenging', continuiteit:'een continuïteitsplan', bestuur:'een voorstel aan directie of bestuur', orientatie:'een eerste oriëntatie'};

const BASIS = [['kantoor','Kantoorsuite, mail en documenten'],['cloud','Cloud en hosting'],['zaak','Zaaksysteem'],['fin','Financieel systeem'],['hr','HR en salaris'],['identiteit','Identiteit en toegang'],['geo','Geo-informatie']];
const EXTRA = {
  gemeente:   [['burgerzaken','Burgerzaken (BRP, reisdocumenten)'],['sociaal','Sociaal domein (Wmo, Jeugd, Participatie)'],['belastingen','Belastingen en WOZ']],
  waterschap: [['ot','Procesautomatisering (gemalen, zuiveringen)'],['heffing','Heffing en invordering'],['meet','Meetnet en peilbeheer']],
  provincie:  [['ot','Bediening van bruggen, sluizen en tunnels'],['subsidie','Subsidiebeheer'],['vth','Vergunningen, toezicht en handhaving']],
  vr:         [['crisis','Crisisbeheersing en -communicatie'],['brandweer','Brandweersystemen']],
  anders:     [['ot','Procesautomatisering']]
};
const DIENSTEN = {
  gemeente:   [['inwoners','Dienstverlening aan inwoners'],['sociaal','Sociaal domein'],['belasting','Belastingen en betalingen'],['vergunning','Vergunningen en handhaving'],['ruimte','Openbare ruimte'],['intern','Interne bedrijfsvoering']],
  waterschap: [['water','Waterbeheer (gemalen, peil, keringen)'],['zuivering','Zuivering'],['heffing','Heffing en invordering'],['vergunning','Vergunningen en handhaving'],['crisis','Calamiteiten'],['intern','Interne bedrijfsvoering']],
  provincie:  [['wegen','Wegen, vaarwegen en bediening'],['subsidie','Subsidies'],['vergunning','Vergunningen en handhaving'],['ruimte','Ruimte en natuur'],['intern','Interne bedrijfsvoering']],
  vr:         [['crisis','Crisisbeheersing'],['brandweer','Brandweerzorg'],['ghor','GHOR'],['intern','Interne bedrijfsvoering']],
  anders:     [['primair','Primaire dienstverlening'],['contact','Contact met burgers of klanten'],['intern','Interne bedrijfsvoering']]
};
const VOOR_WIE = {gemeente:'inwoners', waterschap:'inwoners en bedrijven', provincie:'inwoners en bedrijven', vr:'inwoners'};

const HERKOMST = [['vs','Amerikaanse leverancier'],['buiten','Andere leverancier buiten de EU'],['eu','Leverancier in de EU'],['nl','Nederlandse leverancier'],['eigen','Eigen beheer'],['x','Weet ik niet']];
const CONTRACT = [['jaar','Loopt binnen een jaar af'],['later','Loopt later af'],['geen','Geen contract, eigen beheer'],['x','Weet ik niet']];
const DOORWERK = [['ja','Ja, grotendeels'],['beperkt','Beperkt, met handwerk'],['nee','Nee, het werk ligt stil'],['x','Weet ik niet']];
const ANTW = [['ja','Ja'],['deels','Deels'],['nee','Nee'],['x','Weet ik niet']];

const VRAGEN = [
  { id:'eigenaar', tekst:'Is er iemand in de leiding verantwoordelijk voor de afhankelijkheid van leveranciers, met mandaat om maatregelen te nemen?',
    toel:'Zonder eigenaar blijven acties liggen bij wie toevallig tijd heeft. Onder de Cyberbeveiligingswet moet het bestuur, bij een gemeente het college, de beveiligingsmaatregelen goedkeuren, ook die voor de leveranciersketen.',
    kort:'Eigenaar in de leiding', open:'Wie in de leiding is verantwoordelijk voor de afhankelijkheid van leveranciers?',
    gesprek:'Wie is volgens ieder van jullie de eigenaar, en heeft die ook mandaat?' },
  { id:'scenario', tekst:'Is per belangrijke leverancier vastgelegd wat er gebeurt als die stopt, failliet gaat of wordt overgenomen?',
    toel:'De RDI adviseert om per leverancier te bepalen wat het betekent als die wegvalt. Het hoeft geen dik plan te zijn; één A4 per leverancier met wat er stilvalt en hoe je tijdelijk doorwerkt, is een goed begin.',
    kort:'Vastgelegd wegvalscenario', open:'Is er per belangrijke leverancier vastgelegd wat er gebeurt als die stopt?',
    gesprek:'Waar liggen die scenario\'s, en voor welke leveranciers?' },
  { id:'export', tekst:'Hebben jullie ooit echt gegevens teruggehaald uit een systeem of clouddienst, als test?',
    toel:'Een recht op je gegevens is pas zeker als je het een keer hebt uitgeoefend. De Data Act geeft afnemers van clouddiensten dat recht; een test laat zien wat je in de praktijk terugkrijgt.',
    kort:'Export getest', open:'Is ooit getest of we onze gegevens volledig terug kunnen halen?',
    gesprek:'Welke test was dat, en wat kwam eruit?' },
  { id:'contract', tekst:'Weet je wat jullie contracten zeggen over opzeggen, verlengen en overstappen?',
    toel:'Bij een prijsverhoging of nieuwe voorwaarden bepaalt het contract je ruimte. Voor clouddiensten stelt de Data Act grenzen aan opzegtermijnen en overstapkosten.',
    kort:'Contractafspraken bekend', open:'Wat zeggen onze belangrijkste contracten over opzeggen, verlengen en overstappen?',
    gesprek:'Wie heeft de contracten hierop gelezen?' },
  { id:'alternatief', tekst:'Is voor een belangrijk systeem ooit een alternatief verkend, met een echt gesprek?',
    toel:'Wie weet wat overstappen zou kosten, onderhandelt anders. Het gaat niet om overstappen, maar om weten dat het kan.',
    kort:'Alternatief verkend', open:'Is voor onze belangrijkste systemen ooit een alternatief verkend?',
    gesprek:'Met welke partij is gesproken, en staat dat ergens?' }
];

const S = { org:null, rol:null, doel:null, sys:[], herkomst:{}, contract:{}, dienst:{}, doorwerk:{}, v:{} };
const el = id => document.getElementById(id);
const gc = path => { if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({path:path, event:true}); };
function toast(t){ const x=el('toast'); x.textContent=t; x.classList.add('zien'); setTimeout(()=>x.classList.remove('zien'),3000); }
function naar(n){
  for (let i=0;i<=4;i++) el('s'+i).classList.toggle('verborgen', i!==n);
  el('stappen').classList.toggle('verborgen', n===0);
  [...el('stappen').children].forEach((b,i)=>b.classList.toggle('aan', i < n));
  if (n===2) bouwKaart();
  window.scrollTo({top:0});
  gc('scan/stap-'+n);
}

/* 0 · herken je dit */
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-pressed', x===b ? 'true' : 'false'));
  document.querySelectorAll('.herken').forEach(u=>u.classList.toggle('verborgen', u.dataset.voor!==b.dataset.tab));
});

/* 1 · wie en waarvoor */
function keuzeknoppen(cid, lijst, key, cb){
  const c=el(cid); c.innerHTML='';
  lijst.forEach(([v,t])=>{
    const b=document.createElement('button'); b.className='keuze'; b.type='button'; b.setAttribute('aria-pressed','false');
    b.innerHTML='<span class="rond"></span>'+t;
    b.onclick=()=>{ const oud=S[key]; S[key]=v; [...c.children].forEach(k=>k.setAttribute('aria-pressed', k===b ? 'true' : 'false')); cb && cb(oud); };
    c.appendChild(b);
  });
}
const checkK1 = ()=>{ el('k1').disabled = !(S.org && S.rol && S.doel); };
keuzeknoppen('org', ORGS, 'org', oud=>{
  if (oud && oud!==S.org) { S.sys=[]; S.herkomst={}; S.contract={}; S.dienst={}; S.doorwerk={}; }
  const noot=el('org-noot'), vr=S.org==='vr';
  noot.style.display = vr ? '' : 'none';
  noot.textContent = vr ? 'De Cyberbeveiligingswet geldt niet voor veiligheidsregio\'s. De vragen zijn voor jullie net zo bruikbaar, bijvoorbeeld als een systeem voor crisiscommunicatie wegvalt. De Data Act geldt wel.' : '';
  checkK1();
});
keuzeknoppen('rol', ROLLEN, 'rol', checkK1);
keuzeknoppen('doel', DOELEN, 'doel', checkK1);

/* 2 · systemen */
const typeVan = () => EXTRA[S.org] ? S.org : 'anders';
const systemen = () => EXTRA[typeVan()].concat(BASIS);
const diensten = () => DIENSTEN[DIENSTEN[S.org] ? S.org : 'anders'];
const naamSys = id => (systemen().find(s=>s[0]===id) || [id,id])[1];
const kortSys = id => naamSys(id).replace(/\s*\(.*\)$/, '');
/* naam in een lopende zin: "als het zaaksysteem een week niet werkt" */
const PROZA = { kantoor:'de kantoorsuite', cloud:'de cloudomgeving', zaak:'het zaaksysteem', fin:'het financiële systeem', hr:'het HR- en salarissysteem',
  identiteit:'het systeem voor identiteit en toegang', geo:'de geo-informatie', burgerzaken:'het burgerzakensysteem', sociaal:'het systeem voor het sociaal domein',
  belastingen:'het belastingsysteem', ot:'de procesautomatisering', heffing:'het systeem voor heffing en invordering', meet:'het meetnet',
  subsidie:'het subsidiesysteem', vth:'het VTH-systeem', crisis:'het crisissysteem', brandweer:'het brandweersysteem' };
const deSys = id => PROZA[id] || kortSys(id).toLowerCase();
const kleinSys = deSys;
const compleet = id => S.herkomst[id] && S.contract[id] && S.doorwerk[id] && (S.dienst[id]||[]).length;

function bouwKaart(){
  const k=el('kaart'); k.innerHTML='';
  systemen().forEach(([id,naam])=>{
    const t=document.createElement('button'); t.className='tegel'; t.type='button'; t.id='t-'+id;
    t.setAttribute('aria-pressed', S.sys.includes(id) ? 'true' : 'false');
    t.innerHTML=naam+'<span class="st"></span>';
    t.onclick=()=>{
      const i=S.sys.indexOf(id);
      if (i>=0) { S.sys.splice(i,1); delete S.herkomst[id]; delete S.contract[id]; delete S.dienst[id]; delete S.doorwerk[id]; }
      else { if (S.sys.length>=5) { toast('Hooguit vijf. Kies de belangrijkste.'); return; } S.sys.push(id); }
      bouwKaart(); bouwSys(); checkK2();
    };
    k.appendChild(t);
  });
  S.sys.forEach(tegelStatus);
  bouwSys(); checkK2();
}
function groep(id, key, lijst, vraag, multi){
  return '<div class="vraagje">'+vraag+'</div><div class="opties" role="group" data-k="'+key+'" data-s="'+id+'"'+(multi?' data-multi="1"':'')+'>'
    + lijst.map(([v,t])=>'<button type="button" data-v="'+v+'" aria-pressed="false">'+t+'</button>').join('') + '</div>';
}
function bouwSys(){
  const c=el('sysvragen'); c.innerHTML='';
  S.sys.forEach(id=>{
    const d=document.createElement('div'); d.className='sysblok';
    d.innerHTML='<b>'+naamSys(id)+'</b>'
      + groep(id,'herkomst',HERKOMST,'Wie levert het?')
      + groep(id,'contract',CONTRACT,'Wanneer loopt het contract af?')
      + groep(id,'dienst',diensten().concat([['x','Weet ik niet']]),'Welk werk hangt ervan af? <i>Meer keuzes mogelijk.</i>',true)
      + groep(id,'doorwerk',DOORWERK,'Als dit systeem een week niet werkt, kunnen jullie dan doorwerken?');
    d.querySelectorAll('.opties').forEach(grp=>{
      const k=grp.dataset.k, s=grp.dataset.s, multi=!!grp.dataset.multi;
      const toon=()=>[...grp.children].forEach(x=>{ const aan = multi ? (S[k][s]||[]).includes(x.dataset.v) : S[k][s]===x.dataset.v; x.setAttribute('aria-pressed', aan ? 'true' : 'false'); });
      [...grp.children].forEach(b=>b.onclick=()=>{
        const v=b.dataset.v;
        if (multi) {
          let lijst=(S[k][s]||[]).slice();
          if (v==='x') lijst = lijst.includes('x') ? [] : ['x'];
          else { lijst=lijst.filter(x=>x!=='x'); lijst = lijst.includes(v) ? lijst.filter(x=>x!==v) : lijst.concat([v]); }
          S[k][s]=lijst;
        } else S[k][s]=v;
        toon(); tegelStatus(s); checkK2();
      });
      toon();
    });
    c.appendChild(d);
  });
}
function tegelStatus(id){ const t=el('t-'+id); if (t) t.querySelector('.st').textContent = compleet(id) ? 'ingevuld' : 'gekozen'; }
function checkK2(){
  const open=S.sys.filter(id=>!compleet(id));
  el('k2').disabled = !(S.sys.length && !open.length);
  const st=el('sysstatus');
  if (!S.sys.length) st.textContent='Kies eerst je systemen, dan verschijnen de vragen eronder.';
  else if (open.length) st.innerHTML='Nog invullen: <b>'+open.map(kortSys).join('</b>, <b>')+'</b>';
  else st.textContent = S.sys.length===1 ? 'Eén systeem ingevuld. Je kunt verder, of er nog een kiezen.' : S.sys.length+' systemen ingevuld. Je kunt verder.';
}

/* 3 · organisatie */
(function(){
  const c=el('orgvragen');
  VRAGEN.forEach(q=>{
    const d=document.createElement('div'); d.className='vraagkaart';
    d.innerHTML='<div class="tekst">'+q.tekst+'</div><div class="antw" role="group">'
      + ANTW.map(([v,t])=>'<button type="button" data-v="'+v+'" aria-pressed="false">'+t+'</button>').join('')
      + '</div><details><summary>Waarom vragen we dit?</summary><p>'+q.toel+'</p></details>';
    d.querySelectorAll('.antw button').forEach(b=>b.onclick=()=>{
      S.v[q.id]=b.dataset.v;
      [...b.parentElement.children].forEach(x=>x.setAttribute('aria-pressed', x===b ? 'true' : 'false'));
      el('k3').disabled = Object.keys(S.v).length < VRAGEN.length;
    });
    c.appendChild(d);
  });
})();

/* 4 · uitslag */
const lijst = a => a.length<=1 ? a.join('') : a.slice(0,-1).join(', ')+' en '+a[a.length-1];
const hoofd = s => s.charAt(0).toUpperCase()+s.slice(1);
/* werk in een lopende zin: "ligt het werk stil bij vergunningen en het sociaal domein" */
const DPROZA = { inwoners:'de dienstverlening aan inwoners', sociaal:'het sociaal domein', belasting:'belastingen', vergunning:'vergunningen',
  ruimte:'de openbare ruimte', intern:'de interne bedrijfsvoering', water:'het waterbeheer', zuivering:'de zuivering', heffing:'de heffing',
  crisis:'calamiteiten', wegen:'de wegen en vaarwegen', subsidie:'subsidies', ghor:'de GHOR', brandweer:'de brandweerzorg',
  primair:'de primaire dienstverlening', contact:'het contact met burgers of klanten' };
function dienstWoorden(ids){
  const set=[];
  ids.forEach(id=>(S.dienst[id]||[]).forEach(v=>{ if (v!=='x' && !set.includes(v)) set.push(v); }));
  return set.map(v=>DPROZA[v] || v);
}
function dienstLabels(id){ const L=diensten(); return (S.dienst[id]||[]).filter(v=>v!=='x').map(v=>L.find(x=>x[0]===v)[1].replace(/\s*\(.*\)$/,'')); }
function weetNiet(){
  let n=0;
  S.sys.forEach(id=>{ ['herkomst','contract','doorwerk'].forEach(k=>{ if (S[k][id]==='x') n++; }); if ((S.dienst[id]||[]).includes('x')) n++; });
  VRAGEN.forEach(q=>{ if (S.v[q.id]==='x') n++; });
  return n;
}
function punten(){
  const P=[], v=S.v, d=S.doel, extra=(doelen,n)=>doelen.includes(d) ? n : 0;
  const wie = VOOR_WIE[S.org] || 'de mensen voor wie jullie werken';
  const stil=S.sys.filter(id=>S.doorwerk[id]==='nee'), beperkt=S.sys.filter(id=>S.doorwerk[id]==='beperkt');
  const jaar=S.sys.filter(id=>S.contract[id]==='jaar'), cOnb=S.sys.filter(id=>S.contract[id]==='x');
  const hOnb=S.sys.filter(id=>S.herkomst[id]==='x');
  const extern=S.sys.filter(id=>S.herkomst[id] && S.herkomst[id]!=='eigen');
  const n=weetNiet();

  if ((stil.length || beperkt.length) && v.scenario!=='ja') {
    const ids = stil.length ? stil : beperkt, meer = ids.length>1;
    const werk = dienstWoorden(ids);
    const toestand = stil.length ? 'ligt het werk volgens jou stil' : 'kan het werk volgens jou alleen beperkt door, met handwerk';
    /* scenario is een vraag over de organisatie als geheel: zo formuleren, niet als feit over dit systeem */
    const sc = {nee:'Scenario\'s voor het wegvallen van een leverancier zijn er in het algemeen niet.', deels:'Scenario\'s voor het wegvallen van een leverancier zijn er in het algemeen maar deels.', x:'Of er in het algemeen scenario\'s zijn voor het wegvallen van een leverancier, weet je niet.'}[v.scenario];
    P.push({ prio:(stil.length?90:72)+extra(['continuiteit','risico'],10), label: v.scenario==='x' ? 'onbekend' : 'gemeld',
      titel:'Wat als '+lijst(ids.map(deSys))+' een week '+(meer?'uitvallen':'uitvalt')+'?',
      antwoord:'Als '+lijst(ids.map(deSys))+' een week niet '+(meer?'werken':'werkt')+', '+toestand+(werk.length?' bij '+lijst(werk):'')+'. '+sc,
      gevolg:'Bij een storing, faillissement of gedwongen overstap moet je dan improviseren, terwijl '+wie+' er direct last van hebben.',
      actie:'Schrijf voor '+deSys(ids[0])+' op één A4 wat er gebeurt als de leverancier stopt: wat valt stil, hoe werk je tijdelijk door en wie neemt welk besluit.' });
  }
  if (jaar.length && (v.contract!=='ja' || v.alternatief!=='ja')) {
    const meer=jaar.length>1;
    const zin2 = v.contract!=='ja' ? ' Wat jullie contracten in het algemeen zeggen over verlengen en overstappen, weet je '+({deels:'maar deels', nee:'niet goed', x:'niet'}[v.contract])+'.' : '';
    const zin3 = v.alternatief!=='ja' ? ' Alternatieven voor belangrijke systemen zijn in het algemeen '+({deels:'maar deels', nee:'niet', x:'voor zover je weet niet'}[v.alternatief])+' verkend.' : '';
    const cloud = jaar.some(id=>['cloud','kantoor'].includes(id));
    P.push({ prio:85+extra(['verlenging'],15), label:'gemeld',
      titel:'Het contract voor '+lijst(jaar.map(kleinSys))+' loopt binnen een jaar af',
      antwoord:'Het contract voor '+lijst(jaar.map(deSys))+' loopt binnen een jaar af.'+zin2+zin3,
      gevolg:'Wie laat begint, kan vaak alleen nog verlengen, op de voorwaarden van de leverancier. Een nieuwe aanbesteding kost al snel maanden.',
      actie:'Zet einddatum, opzegtermijn en verlengingsregeling op een rij en besluit op tijd of je verlengt, heronderhandelt of opnieuw uitvraagt.'+(cloud?' Gaat het om een clouddienst, dan mag de leverancier vanaf 12 januari 2027 geen overstapkosten meer rekenen.':'') });
  }
  if (cOnb.length) {
    P.push({ prio:74+(cOnb.length>1?4:0)+extra(['verlenging','risico'],8), label:'onbekend',
      titel:'Wanneer lopen de contracten af?',
      antwoord:'Van '+lijst(cOnb.map(deSys))+' weet je niet wanneer het contract afloopt.',
      gevolg:'Zonder einddatum mis je makkelijk de opzegtermijn. Dan wordt het contract vaak vanzelf verlengd, en is het moment om te onderhandelen voorbij.',
      actie:'Vraag inkoop of contractbeheer naar de einddatum en opzegtermijn van '+(cOnb.length>1?'deze systemen':deSys(cOnb[0]))+'.' });
  }
  if (v.eigenaar!=='ja') {
    const t = {nee:'Er is volgens jou niemand in de leiding met mandaat voor de afhankelijkheid van leveranciers.', deels:'Er is iemand verantwoordelijk, maar zonder duidelijk mandaat.', x:'Je weet niet of iemand in de leiding hiervoor verantwoordelijk is.'}[v.eigenaar];
    P.push({ prio:({nee:80, deels:64, x:70}[v.eigenaar])+extra(['bestuur'],15)+extra(['risico'],5), label: v.eigenaar==='x' ? 'onbekend' : 'gemeld',
      titel:'Wie is verantwoordelijk?', antwoord:t,
      gevolg:'Dan blijven acties liggen bij wie toevallig tijd heeft, en komt een besluit over verlengen of overstappen te laat op tafel.',
      actie:'Leg aan directie of bestuur voor wie dit onderwerp krijgt, met mandaat om een heronderhandeling of overstap voor te bereiden.' });
  }
  if (n>=3) {
    P.push({ prio:(n>=5?89:n>=4?84:71)+extra(['risico','bestuur'],5), label:'onbekend',
      titel:'Waar zit de kennis?',
      antwoord:'Op '+n+' vragen was je antwoord "weet ik niet".',
      gevolg:'Dat zegt weinig over hoe goed het geregeld is. Het zegt wel dat de kennis verspreid zit, en voor een risicoanalyse of bestuursvoorstel heb je die antwoorden eerst nodig.',
      actie:'Neem de lijst met open vragen hieronder mee naar inkoop, beheer en de verantwoordelijke manager. Doe de scan daarna nog eens.' });
  }
  if (v.export!=='ja' && extern.length) {
    const t = {nee:'Jullie hebben nooit getest of je gegevens echt terug kunt halen uit een systeem.', deels:'Of je gegevens terug kunt halen, is maar voor een deel getest.', x:'Je weet niet of ooit is getest of je gegevens terug kunt halen.'}[v.export];
    P.push({ prio:60+extra(['continuiteit'],12), label: v.export==='x' ? 'onbekend' : 'gemeld',
      titel:'Krijg je je gegevens terug?', antwoord:t,
      gevolg:'Of een overstap kan, blijkt dan pas als het moet. Welke gegevens je terugkrijgt, in welk formaat en tegen welke kosten, weet je nu niet.',
      actie:'Kies één systeem en haal een volledige export terug in een testomgeving. Noteer wat ontbreekt.' });
  }
  if (!jaar.length && v.contract!=='ja') {
    const t = {nee:'Je weet niet goed wat de contracten zeggen over opzeggen, verlengen en overstappen.', deels:'Je weet maar deels wat de contracten zeggen over opzeggen, verlengen en overstappen.', x:'Je weet niet of iemand de contracten hierop kent.'}[v.contract];
    P.push({ prio:58+extra(['verlenging'],10), label: v.contract==='x' ? 'onbekend' : 'gemeld',
      titel:'Welke ruimte geven je contracten?', antwoord:t,
      gevolg:'Dan weet je ook niet welke ruimte je hebt als een leverancier de prijs verhoogt of de voorwaarden verandert.',
      actie:'Laat voor de belangrijkste contracten de opzegtermijn, de verlengingsregeling en de afspraken over overstappen op een rij zetten.' });
  }
  if (!jaar.length && v.alternatief!=='ja') {
    P.push({ prio:55+extra(['verlenging','bestuur'],8), label: v.alternatief==='x' ? 'onbekend' : 'gemeld',
      titel:'Weet je wat overstappen zou kosten?',
      antwoord: v.alternatief==='x' ? 'Je weet niet of ooit een alternatief is verkend.' : (v.alternatief==='deels' ? 'Een alternatief is maar deels verkend.' : 'Voor geen enkel belangrijk systeem is een alternatief verkend.'),
      gevolg:'Bij een prijsverhoging of nieuwe voorwaarden heb je dan weinig om tegenover te zetten.',
      actie:'Voer voor je grootste afhankelijkheid één verkennend gesprek met een andere aanbieder, alleen om te weten wat overstappen zou kosten.' });
  }
  if (hOnb.length) {
    P.push({ prio:50, label:'onbekend', titel:'Wie levert het?',
      antwoord:'Van '+lijst(hOnb.map(deSys))+' weet je niet wie het levert.',
      gevolg:'Dan weet je ook niet welke risico\'s en regels spelen, bijvoorbeeld bij een overname of een leverancier buiten de EU.',
      actie:'Vraag beheer of inkoop wie de leverancier is en waar de gegevens staan.' });
  }
  if (!P.length) {
    P.push({ prio:10, label:'gemeld', titel:'Maak aantoonbaar wat je hebt',
      antwoord:'Je meldt dat eigenaar, scenario\'s, exporttest, contractafspraken en alternatieven geregeld zijn.',
      gevolg:'Dat is een goede basis. Bij een risicoanalyse of vragen van een toezichthouder telt wel alleen wat op papier staat.',
      actie:'Verzamel de stukken waaruit dit blijkt, zodat het van gemeld naar aantoonbaar gaat.' });
  }
  return P.sort((a,b)=>b.prio-a.prio).slice(0,3);
}
const ESC = s => String(s).replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function puntHtml(p, i){
  return '<div class="punt"><div class="kop"><h3><span class="nr">'+(i+1)+'</span>'+ESC(p.titel)+'</h3><span class="chip '+p.label+'">'+(p.label==='gemeld'?'gemeld':'nog onbekend')+'</span></div>'
    + '<dl><dt>Jouw antwoord</dt><dd>'+ESC(p.antwoord)+'</dd><dt>Mogelijk gevolg</dt><dd>'+ESC(p.gevolg)+'</dd><dt>Eerste actie</dt><dd class="actie">'+ESC(p.actie)+'</dd></dl></div>';
}
const tekstVan = (lijstje, v) => { const r=lijstje.find(x=>x[0]===v); return r ? r[1] : '-'; };
function openVragen(){
  const q=[];
  S.sys.forEach(id=>{
    const n=deSys(id);
    if (S.herkomst[id]==='x') q.push('Wie levert '+n+', en waar staan de gegevens?');
    if (S.contract[id]==='x') q.push('Wanneer loopt het contract voor '+n+' af, en wat is de opzegtermijn?');
    if ((S.dienst[id]||[]).includes('x')) q.push('Welk werk hangt af van '+n+'?');
    if (S.doorwerk[id]==='x') q.push('Kunnen we een week doorwerken als '+n+' uitvalt?');
  });
  VRAGEN.forEach(v=>{ if (S.v[v.id]==='x') q.push(v.open); });
  return q;
}
function resultaat(){
  el('uit-intro').textContent = 'Je gaf aan dat je de uitkomst wilt gebruiken voor '+DOELNAAM[S.doel]+'. Hieronder de punten die daarvoor het meest tellen, op basis van je antwoorden.';
  el('punten').innerHTML = punten().map(puntHtml).join('');
  /* overzicht per systeem: alleen feiten, geen kleuren */
  const cel = (t, onb) => '<td'+(onb?' class="onb"':'')+'>'+ESC(t)+'</td>';
  el('overzicht').innerHTML = '<thead><tr><th>Systeem</th><th>Leverancier</th><th>Contract</th><th>Werk dat ervan afhangt</th><th>Een week zonder</th></tr></thead><tbody>'
    + S.sys.map(id=>{
        const w=(S.dienst[id]||[]), wt = w.includes('x') ? 'weet ik niet' : dienstLabels(id).join('; ');
        return '<tr><td><b>'+ESC(naamSys(id))+'</b></td>'
          + cel(tekstVan(HERKOMST,S.herkomst[id]), S.herkomst[id]==='x')
          + cel(tekstVan(CONTRACT,S.contract[id]), S.contract[id]==='x')
          + cel(wt, w.includes('x'))
          + cel(tekstVan(DOORWERK,S.doorwerk[id]), S.doorwerk[id]==='x') + '</tr>';
      }).join('') + '</tbody>';
  const q=openVragen();
  el('open').innerHTML = q.length
    ? '<p style="margin-bottom:0.6rem">Neem deze vragen mee naar inkoop, beheer en de verantwoordelijke manager.</p><ol>'+q.map(x=>'<li>'+ESC(x)+'</li>').join('')+'</ol>'
      + '<textarea id="open-tekst" class="verborgen" aria-hidden="true">'+ESC(q.map((x,i)=>(i+1)+'. '+x).join('\n'))+'</textarea>'
      + '<button class="b-stil" style="padding-left:0" onclick="kopieer(\'open-tekst\',\'Lijst gekopieerd\')">Kopieer de lijst</button>'
    : '<p style="margin:0">Je had overal een antwoord op. Let wel: dat is je eigen beeld, nog niet gecontroleerd.</p>';
  /* vervolg: het document dat bij het doel past komt bovenaan */
  const docs = [['risico','Bewerkbare concepttekst voor je risicoanalyse'],['bestuur','Concept-beslisnotitie voor directie of bestuur'],['verlenging','Vragen voor je leveranciers en aandachtspunten voor inkoop'],['continuiteit','Actielijst met voorgestelde verantwoordelijken, termijnen en bewijsstukken'],['alle','Overzicht van afhankelijkheden en mogelijke gevolgen per systeem']];
  docs.sort((a,b)=>(b[0]===S.doel)-(a[0]===S.doel));
  el('vervolg-lijst').innerHTML = docs.map(([k,t])=>'<li'+(k===S.doel?' class="past"':'')+'>'+t+'</li>').join('');
  el('vervolg-doel').textContent = S.doel==='orientatie'
    ? 'Het betaalde vervolg werkt je antwoorden uit tot stukken die je kunt delen met directie, inkoop of je leverancier.'
    : 'Je werkt aan '+DOELNAAM[S.doel]+'. Het betaalde vervolg werkt je antwoorden daarvoor uit tot stukken die je kunt delen.';
  /* vergelijk met een collega */
  const ander = S.rol==='bestuur' ? 'iemand uit de uitvoering' : (S.rol==='uitvoering' ? 'je leidinggevende of bestuurder' : 'een collega uit een andere laag');
  el('duo-tekst').textContent = 'Laat '+ander+' dezelfde scan doen via deze link. Je ziet dan bij welke vragen jullie verschillend antwoorden, en dat zijn meestal de punten om over te praten.';
  el('duo-link').value = location.origin+'/scan/?v='+codeer();
  toonKloof();
  stuurTelling();
  gc('scan/afgerond');
}
function codeer(){ return btoa(JSON.stringify({rol:S.rol, org:S.org, sys:S.sys.slice().sort(), o:VRAGEN.map(q=>S.v[q.id]||'')})).replace(/=+$/,''); }
function toonKloof(){
  const p=new URLSearchParams(location.search).get('v'); if (!p) return;
  let o; try { o=JSON.parse(atob(p)); } catch(e) { return; }
  if (!o || !Array.isArray(o.o)) return;
  const verschil = VRAGEN.map((q,i)=>({q, hun:o.o[i], mijn:S.v[q.id]})).filter(x=>x.hun && x.mijn && x.hun!==x.mijn);
  const naam = r => ({bestuur:'bestuur', cio:'CIO of informatiemanager', uitvoering:'uitvoering', anders:'collega'})[r] || 'collega';
  const k=el('kloof'); k.classList.remove('verborgen');
  el('duo-kop').textContent='Waar jullie verschillend antwoorden';
  el('duo-tekst').textContent = verschil.length
    ? 'Je collega ('+naam(o.rol)+') antwoordde op '+verschil.length+' van de vijf organisatievragen anders dan jij. Dat is geen oordeel over wie gelijk heeft, maar een agenda voor een gesprek.'
    : 'Je collega ('+naam(o.rol)+') gaf op alle vijf de organisatievragen hetzelfde antwoord als jij.';
  const t = v => tekstVan(ANTW, v).toLowerCase();
  k.innerHTML = verschil.map(x=>'<div class="gv"><b>'+ESC(x.q.kort)+'</b><span>Jij: '+t(x.mijn)+'. Je collega: '+t(x.hun)+'.</span><span>Vraag voor het gesprek: '+ESC(x.q.gesprek)+'</span></div>').join('')
    + ((o.sys||[]).slice().sort().join()!==S.sys.slice().sort().join() ? '<p class="klein" style="margin-top:0.6rem">Let op: jullie kozen niet dezelfde systemen.</p>' : '');
}
function kopieer(id, melding){ const x=el(id); x.classList.remove('verborgen'); x.select(); let ok=false; try { ok=document.execCommand('copy'); } catch(e) {} if (id!=='duo-link') x.classList.add('verborgen'); toast(ok ? melding : 'Selecteer de tekst en kopieer hem'); }
function stuurTelling(){
  /* alleen tellingen: geen namen, geen leveranciers, geen vrije tekst */
  const tel = f => S.sys.filter(f).length;
  const body = { org:S.org, rol:S.rol, doel:S.doel, n:S.sys.length,
    niet_eu:tel(id=>['vs','buiten'].includes(S.herkomst[id])), contract_onb:tel(id=>S.contract[id]==='x'),
    binnen_jaar:tel(id=>S.contract[id]==='jaar'), stil:tel(id=>S.doorwerk[id]==='nee'),
    weet_niet:weetNiet(), o:VRAGEN.map(q=>S.v[q.id]||'').join(',') };
  try { fetch('/api/scan.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),keepalive:true}).catch(()=>{}); } catch(e) {}
}
function mailtje(soort){
  const rolNaam = (ROLLEN.find(r=>r[0]===S.rol)||['',S.rol])[1];
  const orgNaam = (ORGS.find(r=>r[0]===S.org)||['',S.org])[1];
  const onderwerp = soort==='pilot' ? 'Scan: ik wil meedoen met de pilot' : 'Scan: hou me op de hoogte';
  const regels = [
    soort==='pilot' ? 'Ik heb de scan gedaan en wil graag meedoen met de pilot (dossier voor €750 excl. btw).' : 'Ik heb de scan gedaan en hoor graag meer over het vervolg.',
    '', 'Mijn organisatie: ', 'Type organisatie: '+orgNaam, 'Mijn rol: '+rolNaam,
    'Waarvoor ik het nodig heb: '+(DOELEN.find(x=>x[0]===S.doel)||['',''])[1], '', 'Waar ik tegenaan loop: ', '' ];
  location.href = 'mailto:info@willswitch.nl?subject='+encodeURIComponent(onderwerp)+'&body='+encodeURIComponent(regels.join('\n'));
  gc('scan/aanmelding-'+soort);
  return false;
}
(function(){ const v=el('link-voorbeeld'); if (v) v.addEventListener('click',()=>gc('scan/voorbeeldrapport')); })();
</script>
  <!-- Privacyvriendelijke analytics (GoatCounter, geen cookies) -->
  <script data-goatcounter="https://willswitch.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
'''


def build_scan():
    return PAGE
