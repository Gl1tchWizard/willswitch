"""De uitstaptoets: gratis scan op /scan/.

Drie verplichtingen, elk met eigen vragen, plus een snelle inventaris die
de concentratie laat zien. Alles draait in de browser. Alleen geaggregeerde
scores gaan naar de server, nooit leveranciersnamen of vrije tekst.

FASE 1: de gratis toets is open. Bestellen staat nog uit; het rapportblok
kondigt aan en telt de interesse.
"""

PAGE = r'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Uitstaptoets: kun je nog weg bij je leveranciers? | Will Switch</title>
  <meta name="description" content="Gratis toets voor gemeenten, waterschappen en andere publieke organisaties. Toetst in een kwartier je ketenafhankelijkheid tegen de Cyberbeveiligingswet, de Data Act en het rijkscloudbeleid. Geen registratie.">
  <link rel="canonical" href="https://willswitch.nl/scan/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="Uitstaptoets: kun je nog weg bij je leveranciers?">
  <meta property="og:description" content="Toets in een kwartier of je organisatie nog weg kan bij haar leveranciers, langs de Cyberbeveiligingswet, de Data Act en het rijksbrede cloudbeleid. Gratis, geen registratie.">
  <meta property="og:image" content="https://willswitch.nl/og-image.jpg">
  <meta property="og:url" content="https://willswitch.nl/scan/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180.png">
  <link rel="preload" href="/fonts/AtkinsonNext.woff2" as="font" type="font/woff2" crossorigin>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Uitstaptoets",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "EUR" },
    "description": "Toetst de ketenafhankelijkheid van publieke organisaties tegen de Cyberbeveiligingswet, de Data Act en het rijkscloudbeleid.",
    "url": "https://willswitch.nl/scan/",
    "provider": { "@type": "Organization", "name": "Will Switch", "url": "https://willswitch.nl/" }
  }
  </script>
  <style>
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
      --ok:#2F6F4E; --warn:#B8760F; --bad:#9E3A30; --onb:#B9B3A8;
      /* aliassen voor de inline stijlen in de markup en het script; die blijven zoals ze zijn */
      --orange:var(--oranje); --ink-faint:var(--vaag);
      --disp:'Atkinson Hyperlegible Next', system-ui, sans-serif;
    }
    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    html { overflow-x:clip; scrollbar-gutter:stable; }
    body {
      background:var(--papier); color:var(--inkt);
      font-family:'Atkinson Hyperlegible Next', system-ui, sans-serif; font-synthesis:none;
      font-size:17px; line-height:1.55;
    }
    a { color:inherit; }
    img { max-width:100%; }
    :focus-visible { outline:3px solid var(--knop); outline-offset:3px; }
    .w { max-width:1280px; margin:0 auto; padding:0 40px; }

    /* header, letterlijk als op de hoofdpagina, zonder de toetsknop */
    header.top { border-bottom:1px solid var(--inkt); background:var(--papier); }
    header.top .w { display:flex; align-items:center; justify-content:space-between; min-height:84px; gap:20px; }
    .merk { display:flex; align-items:center; gap:18px; text-decoration:none; }
    .merk img { height:36px; width:auto; display:block; }
    .merk span { font-size:13px; color:var(--zacht); line-height:1.35; padding-left:18px; border-left:1px solid var(--inkt); }
    nav.hoofd { display:flex; align-items:center; gap:32px; font-size:16px; }
    nav.hoofd a.l { text-decoration:none; padding:10px 0; }
    nav.hoofd a.l:hover { text-decoration:underline; text-underline-offset:4px; }

    /* voortgang: een dunne oranje lijn onder de header */
    .stappen { display:flex; height:3px; background:var(--lijn); }
    .stappen i { flex:1; }
    .stappen i.aan { background:var(--oranje); }

    /* de stappen zelf: een leeskolom in de brede container */
    .wrap > section { max-width:1280px; margin:0 auto; padding:48px 40px 96px; }
    .wrap > section > * { max-width:760px; }

    h1 { font-size:clamp(40px, 5vw, 64px); font-weight:800; letter-spacing:-.02em; line-height:1.02; margin-bottom:24px; text-wrap:balance; }
    h2 { font-size:32px; font-weight:700; line-height:1.1; margin-bottom:12px; text-wrap:balance; }
    h3 { font-size:22px; font-weight:700; line-height:1.15; margin:40px 0 12px; }
    p { color:var(--zacht); margin-bottom:16px; max-width:62ch; }
    p.lead { color:var(--inkt); font-size:20px; line-height:1.4; }
    .klein { font-size:15px; color:var(--vaag); line-height:1.5; }
    .wet {
      margin:28px 0; padding:20px 0; max-width:62ch;
      border-top:1px solid var(--inkt); border-bottom:1px solid var(--inkt);
      font-size:16px; color:var(--zacht);
    }
    .wet b { color:var(--inkt); }
    .wet .bron { display:block; margin-top:14px; font-family:var(--mono); font-size:13px; letter-spacing:.02em; line-height:1.6; color:var(--vaag); }

    /* knoppen */
    button { font:inherit; color:inherit; cursor:pointer; border:0; border-radius:0; background:none; }
    button:disabled { opacity:.35; cursor:not-allowed; }
    .b-primair {
      display:inline-flex; align-items:center; justify-content:center; gap:.55em;
      min-height:48px; padding:0 24px; background:var(--knop); color:#fff;
      font-size:16px; font-weight:700; line-height:1.1; text-decoration:none; border:0; border-radius:0;
    }
    .b-primair:hover:not(:disabled) { background:var(--inkt); color:#fff; }
    #sysstatus b { color:var(--inkt); }
    .b-stil {
      display:inline-flex; align-items:center; min-height:44px; padding:0; background:none;
      color:var(--link); font-size:16px; font-weight:600;
      text-decoration:underline; text-underline-offset:4px; text-decoration-thickness:1.5px;
    }
    .b-stil:hover { color:var(--inkt); }
    .nav { display:flex; justify-content:space-between; align-items:center; gap:16px; margin-top:40px; padding-top:24px; border-top:1px solid var(--inkt); }
    #s6 .nav > a {
      color:var(--link) !important; font-family:inherit !important; font-size:16px !important; font-weight:600;
      letter-spacing:0 !important; text-transform:none !important;
      text-decoration:underline !important; text-underline-offset:4px; text-decoration-thickness:1.5px;
    }
    #s6 .nav > a:hover { color:var(--inkt) !important; }

    /* keuzes: wie en welke organisatie */
    .keuzes { display:grid; gap:8px; margin:20px 0 8px; }
    .keuzes.twee { grid-template-columns:1fr 1fr; }
    .keuze {
      display:flex; align-items:center; gap:14px; min-height:52px; padding:12px 16px;
      background:var(--wit); border:1px solid var(--lijn); text-align:left;
      font-size:16px; line-height:1.3; color:var(--inkt);
    }
    .keuze:hover { border-color:var(--inkt); }
    .keuze.aan { background:var(--inkt); border-color:var(--inkt); color:var(--papier); }
    .keuze .rond { width:16px; height:16px; border:1.5px solid var(--inkt); border-radius:50%; flex:none; }
    .keuze.aan .rond { border-color:var(--papier); background:var(--papier); }

    /* inventaris: de concentratiekaart */
    .kaart { display:grid; grid-template-columns:repeat(auto-fill, minmax(150px, 1fr)); gap:8px; margin:20px 0 12px; }
    .tegel {
      position:relative; min-height:96px; padding:30px 14px 24px;
      background:var(--wit); border:1px solid var(--lijn); text-align:left; color:var(--inkt);
    }
    .tegel:hover { border-color:var(--inkt); }
    .tegel.aan { border-color:var(--inkt); box-shadow:inset 0 0 0 1px var(--inkt); }
    .tegel .naam { display:block; font-size:15px; font-weight:700; line-height:1.3; hyphens:auto; overflow-wrap:anywhere; }
    .tegel .stat { position:absolute; left:14px; right:14px; bottom:12px; height:4px; display:flex; gap:3px; }
    .tegel .stat i { flex:1; background:var(--lijn); }
    .tegel .stat i.o0 { background:var(--bad); } .tegel .stat i.o1 { background:var(--warn); } .tegel .stat i.o2 { background:var(--ok); }
    .tegel .stat i.c0 { background:var(--bad); } .tegel .stat i.c1 { background:var(--warn); } .tegel .stat i.c2 { background:var(--ok); }
    .tegel.aan::after { content:"gekozen"; position:absolute; top:12px; right:14px; font-family:var(--mono); font-size:11px; letter-spacing:.02em; color:var(--zacht); }
    .tegel.klaar::after { content:"ingevuld"; color:var(--ok); }
    .tegel.uit::after { content:none; }
    .tegel.uit { border-color:var(--lijn); box-shadow:none; padding-top:14px; min-height:72px; }

    .sysblok { margin-top:8px; padding:20px 0 4px; border-top:1px solid var(--inkt); }
    .sysblok .kop { display:flex; justify-content:space-between; align-items:baseline; gap:16px; margin-bottom:4px; }
    .sysblok .kop b { font-size:18px; }
    .sysblok .kop .klein { font-family:var(--mono); font-size:13px; letter-spacing:.02em; white-space:nowrap; }
    .vraagje { font-size:16px; margin:14px 0 8px; color:var(--inkt); }
    .opties { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:16px; }
    .opties button { min-height:44px; padding:0 14px; background:var(--wit); border:1px solid var(--lijn); color:var(--zacht); font-size:15px; }
    .opties button:hover { border-color:var(--inkt); color:var(--inkt); }
    .opties button.aan { background:var(--inkt); border-color:var(--inkt); color:var(--papier); }

    /* dimensievragen */
    .vraagkaart { padding:24px 0; border-top:1px solid var(--inkt); }
    .vraagkaart .tekst { font-size:19px; font-weight:600; line-height:1.35; color:var(--inkt); margin-bottom:14px; cursor:pointer; }
    .vraagkaart .toel { display:none; margin-top:12px; font-size:15px; line-height:1.5; color:var(--zacht); }
    .vraagkaart.open .toel { display:block; }
    .antw { display:grid; grid-template-columns:repeat(4, 1fr); gap:8px; }
    .antw button { min-height:44px; padding:0 8px; background:var(--wit); border:1px solid var(--lijn); color:var(--zacht); font-size:15px; }
    .antw button:hover { border-color:var(--inkt); color:var(--inkt); }
    .antw button.a2, .antw button.a1, .antw button.a0, .antw button.ax { background:var(--inkt); border-color:var(--inkt); color:var(--papier); font-weight:700; }

    /* resultaat */
    .kern { margin:24px 0 8px; padding:28px 0; border-top:3px solid var(--inkt); border-bottom:1px solid var(--inkt); }
    .kern .groot { font-size:clamp(56px, 11vw, 112px); font-weight:800; letter-spacing:-.04em; line-height:.9; color:var(--oranje); font-variant-numeric:tabular-nums; }
    .kern .zin { font-size:20px; line-height:1.4; color:var(--inkt); margin-top:16px; max-width:44ch; }
    .concentratie { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin:16px 0 20px; }
    .cijfer { padding:16px 0 4px; border-top:1px solid var(--inkt); }
    .cijfer b { display:block; font-size:40px; font-weight:800; letter-spacing:-.03em; line-height:1; font-variant-numeric:tabular-nums; }
    .cijfer span { display:block; font-size:15px; color:var(--zacht); margin-top:8px; }
    .dekking { margin:12px 0 32px; }
    .dek { padding:14px 0; border-top:1px solid var(--lijn); }
    .dek .lbl { display:flex; justify-content:space-between; align-items:baseline; gap:8px 16px; flex-wrap:wrap; font-size:16px; margin-bottom:10px; }
    .dek .lbl b { font-size:16px; }
    .dek .lbl b span { font-size:15px; }
    .dek .lbl > span { font-family:var(--mono); font-size:13px; letter-spacing:.02em; color:var(--zacht); }
    .dek .staaf { display:flex; height:8px; background:var(--lijn); overflow:hidden; }
    .dek .staaf i { display:block; }
    .dek .staaf .v-ja { background:var(--ok); }
    .dek .staaf .v-deels { background:var(--warn); }
    .dek .staaf .v-nee { background:var(--bad); }
    .dek .staaf .v-onb { background:var(--onb); }
    .dek .klein { margin-top:6px; }
    .stap1 { background:var(--inkt); color:var(--papier); padding:32px 36px; margin:32px 0 8px; }
    .stap1 h2 { color:var(--papier); }
    .stap1 p { color:var(--op-inkt); margin-bottom:0; }
    .deadline { display:grid; grid-template-columns:repeat(3, 1fr); gap:24px; margin:16px 0 32px; }
    .deadline div { padding:16px 0 0; border-top:1px solid var(--inkt); font-size:15px; line-height:1.5; color:var(--zacht); }
    .deadline b { display:block; font-size:22px; font-weight:800; letter-spacing:-.01em; line-height:1.1; color:var(--inkt); margin-bottom:8px; }
    .duo { background:var(--warm); padding:24px; margin:32px 0; }
    #duo-kop { font-size:18px !important; }
    .duo input {
      width:100%; margin-top:12px; padding:12px 14px; border:1px solid var(--lijn); border-radius:0;
      background:var(--wit); color:var(--inkt); font-family:var(--mono); font-size:13px; letter-spacing:.02em;
    }
    .duo .b-stil { margin-top:8px; }
    .kloof { margin-top:16px; display:grid; gap:6px; }
    .kloof div { display:grid; grid-template-columns:1fr auto auto; gap:16px; font-size:15px; align-items:center; }
    .kloof .verschil { color:var(--bad); font-weight:700; }

    /* het rapport: inktblok met de prijs */
    .rapport { background:var(--inkt); color:var(--papier); padding:40px; margin:40px 0 24px; }
    .rapport h2 { color:var(--papier); margin-bottom:8px; }
    .rapport .prijs { font-size:22px; font-weight:700; line-height:1.3; padding-bottom:20px; margin-bottom:20px; border-bottom:1px solid var(--lijn-inkt); }
    .rapport p { color:var(--op-inkt); }
    .rapport ul { list-style:none; margin:16px 0 24px; }
    .rapport li { padding:10px 0; border-top:1px solid var(--lijn-inkt); font-size:16px; }
    .rapport li:last-child { border-bottom:1px solid var(--lijn-inkt); }
    .rapport .klein { color:var(--op-inkt-2); }
    .rapport #link-voorbeeld {
      color:var(--papier) !important; font-family:inherit !important; font-size:16px !important; font-weight:600;
      letter-spacing:0 !important; text-transform:none !important; border-bottom:0 !important;
      text-decoration:underline !important; text-underline-offset:4px; text-decoration-thickness:1.5px;
    }
    .rapport #link-voorbeeld:hover { color:#fff !important; }
    .aanmeld { margin-top:24px; padding-top:24px; border-top:1px solid var(--lijn-inkt); }
    .aanmeld .b-primair, .b-tweede {
      display:inline-flex; align-items:center; justify-content:center; min-height:48px; padding:0 24px;
      margin:0 12px 12px 0; font-size:16px; font-weight:700; line-height:1.1;
      text-decoration:none; border-radius:0; cursor:pointer;
    }
    .aanmeld .b-primair { background:var(--knop); color:#fff; border:0; }
    .aanmeld .b-primair:hover { background:var(--papier); color:var(--inkt); }
    .b-tweede { background:transparent; color:var(--papier); border:1.5px solid var(--papier); }
    .b-tweede:hover { background:var(--papier); color:var(--inkt); }
    .aanmeld .veld { display:block; margin-bottom:12px; }
    .aanmeld .veld span { display:block; font-size:15px; color:var(--op-inkt); margin-bottom:4px; }
    .aanmeld input { width:100%; padding:12px 14px; border:1px solid var(--lijn-inkt); border-radius:0; background:var(--wit); color:var(--inkt); font:inherit; font-size:16px; }
    .aanmeld .keuzes { margin:0 0 16px; }
    .melding { margin-top:12px; font-size:15px; display:none; }
    .melding.goed { display:block; color:var(--papier); }
    .melding.fout { display:block; color:var(--papier); }

    .toast {
      position:fixed; left:50%; bottom:24px; transform:translateX(-50%); max-width:90vw; text-align:center;
      background:var(--inkt); color:var(--papier); padding:14px 20px; font-size:15px;
      opacity:0; pointer-events:none; transition:opacity .3s;
    }
    .toast.zien { opacity:1; }
    .verborgen { display:none !important; }

    /* voettekst, letterlijk als op de hoofdpagina */
    footer.site { border-top:3px solid var(--inkt); padding:28px 0 48px; font-size:14px; color:var(--vaag); }
    footer.site .w { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px 24px; }
    footer.site .fonds { display:inline-flex; align-items:center; gap:12px; text-decoration:none; }
    footer.site .fonds img { height:28px; width:auto; display:block; }

    @media (max-width:820px) {
      .w { padding:0 16px; }
      header.top .w { min-height:64px; }
      .merk img { height:30px; }
      .merk span { display:none; }
      nav.hoofd { gap:16px; font-size:15px; }
      .wrap > section { padding:32px 16px 64px; }
      h2 { font-size:28px; }
      .keuzes.twee { grid-template-columns:1fr; }
      .concentratie, .deadline { grid-template-columns:1fr; gap:12px; }
      .nav .b-primair { flex:1; }
      .stap1, .rapport { padding:28px 20px; }
      .duo { padding:20px 16px; }
      footer.site .w { flex-direction:column; align-items:flex-start; gap:12px; }
    }
    @media (max-width:480px) { .antw { grid-template-columns:1fr 1fr; } }
    @media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
  </style>
</head>
<body>
<div class="wrap">
  <header class="top"><div class="w">
    <a class="merk" href="/switch.html"><img src="/wordmark.png" alt="Will Switch" width="705" height="153"><span>Praktijkonderzoek naar<br>digitale autonomie</span></a>
    <nav class="hoofd" aria-label="Hoofdnavigatie"><a class="l" href="/switch.html#verhalen">Praktijk</a><a class="l" href="/switch.html#rapport">Rapport</a></nav>
  </div></header>
  <div class="stappen" id="stappen" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>

  <!-- 0 · start -->
  <section id="s0">
    <h1>Kun je nog weg bij je leveranciers?</h1>
    <p class="lead">Twee wetten en een beleidskader stellen sinds kort dezelfde vraag, elk vanuit een andere hoek. De meeste organisaties hebben op geen van de drie een compleet antwoord.</p>
    <div class="wet">
      <b>Cyberbeveiligingswet</b>, van kracht sinds 15 augustus 2026. Vraagt een risicoanalyse per leverancier, inclusief wat er gebeurt bij contracteinde, faillissement of overname. Geldt voor het Rijk, ZBO's, gemeenten, provincies en waterschappen.<br><br>
      <b>Data Act</b>, van toepassing sinds 12 september 2025. Geeft je als cloudklant het recht om over te stappen, en verbiedt vanaf 12 januari 2027 overstapkosten. Geldt voor iedere afnemer van clouddiensten.<br><br>
      <b>Rijksbreed cloudbeleid</b>, vastgesteld 3 juli 2026. Dit is beleid, geen wet. Het verplicht rijksorganisaties tot een exitplan, met een overgangstermijn tot medio 2030. Voor gemeenten, provincies en waterschappen geldt het nu nog niet: de staatssecretaris kondigde aan hierover met de medeoverheden in gesprek te gaan.
      <span class="bron">Bronnen: RDI, toelichting zorgplicht toeleveringsketen; Verordening (EU) 2023/2854, hoofdstuk VI; Kamerbrief Herziening Rijksbreed Cloudbeleid (26 643, nr. 1541). Gecontroleerd op 11 september 2026. Dit is geen juridisch advies.</span>
    </div>
    <p>Deze toets duurt een kwartier en vraagt geen registratie. Je krijgt direct je beeld: waar je afhankelijkheden zitten, wat je per onderwerp zelf meldt, en een eerste stap die daarbij past.</p>
    <p class="klein">De toets werkt met je eigen opgave. Er wordt niets gecontroleerd aan de hand van documenten, en er komt geen oordeel uit over naleving. Je antwoorden blijven in je browser. Bij het resultaat sturen we alleen geaggregeerde uitkomsten mee: je rol, je organisatietype, het aantal systemen en de telling per onderwerp. Geen namen, geen leveranciers, geen vrije tekst.</p>
    <div class="nav"><span></span><button class="b-primair" onclick="naar(1)">Start de toets</button></div>
  </section>

  <!-- 1 · wie -->
  <section id="s1" class="verborgen">
    <h2>Wie vult in?</h2>
    <p>Dezelfde toets levert vaak een ander beeld op bij bestuur dan bij uitvoering. Daarom vragen we het.</p>
    <div class="keuzes twee" id="rol"></div>
    <h3>Voor welk type organisatie?</h3>
    <div class="keuzes twee" id="org"></div>
    <div class="nav"><button class="b-stil" onclick="naar(0)">Terug</button><button class="b-primair" id="k1" disabled onclick="naar(2)">Verder</button></div>
  </section>

  <!-- 2 · inventaris -->
  <section id="s2" class="verborgen">
    <h2>Welke systemen zijn kritiek voor je?</h2>
    <p>Kies de systemen waar je organisatie echt van afhankelijk is, maximaal vijf. Per systeem twee feiten: wie levert het, en weet je wanneer het contract afloopt. Meer niet.</p>
    <div class="kaart" id="kaart"></div>
    <p class="klein" id="sysstatus">Kies eerst je systemen, dan verschijnen de vragen eronder.</p>
    <div id="sysvragen"></div>
    <div class="nav"><button class="b-stil" onclick="naar(1)">Terug</button><button class="b-primair" id="k2" disabled onclick="naar(3)">Verder</button></div>
  </section>

  <!-- 3 · ketenzorgplicht -->
  <section id="s3" class="verborgen">
    <h2>Ketenzorgplicht</h2>
    <p>Wat de Cyberbeveiligingswet van je vraagt over bestaande leveranciers. Antwoord voor je organisatie als geheel. Klik op een vraag voor de toelichting.</p>
    <div id="vr-a"></div>
    <div class="nav"><button class="b-stil" onclick="naar(2)">Terug</button><button class="b-primair" id="k3" disabled onclick="naar(4)">Verder</button></div>
  </section>

  <!-- 4 · overstaprecht -->
  <section id="s4" class="verborgen">
    <h2>Overstaprecht</h2>
    <p>Wat de Data Act je geeft als cloudklant, en of je daar gebruik van kunt maken.</p>
    <div id="vr-b"></div>
    <div class="nav"><button class="b-stil" onclick="naar(3)">Terug</button><button class="b-primair" id="k4" disabled onclick="naar(5)">Verder</button></div>
  </section>

  <!-- 5 · exitplan -->
  <section id="s5" class="verborgen">
    <h2>Exitplan</h2>
    <p>Wat het rijkscloudbeleid verplicht stelt, en wat elke organisatie sowieso nodig heeft.</p>
    <div id="vr-c"></div>
    <div class="nav"><button class="b-stil" onclick="naar(4)">Terug</button><button class="b-primair" id="k5" disabled onclick="resultaat();naar(6)">Bekijk je uitkomst</button></div>
  </section>

  <!-- 6 · resultaat -->
  <section id="s6" class="verborgen">
    <h2>Je uitkomst</h2>
    <div class="kern"><div class="groot" id="kern-getal"></div><div class="zin" id="kern-zin"></div></div>

    <h3>Concentratie</h3>
    <div class="concentratie">
      <div class="cijfer"><b id="c-nieteu">0</b><span>van je kritieke systemen bij een leverancier buiten de EU</span></div>
      <div class="cijfer"><b id="c-onbekend">0</b><span>waarvan het contracteinde niet bekend is</span></div>
    </div>
    <div class="kaart" id="kaart-uit"></div>

    <h3>Wat je per onderwerp meldt</h3>
    <p class="klein" style="margin:-0.4rem 0 0.9rem">Dit is je eigen opgave, niet getoetst aan documenten. Onbekend telt apart: het verlaagt je beeld niet, maar het is wel een vraag die nog ergens beantwoord moet worden.</p>
    <div class="dekking" id="dekking"></div>

    <div class="stap1"><h2 id="stap-kop"></h2><p id="stap-tekst"></p></div>

    <h3>De klok</h3>
    <div class="deadline">
      <div><b>12 januari 2027</b>Overstapkosten bij clouddiensten vervallen. Let op: dat betekent niet dat een migratie gratis is. Je eigen uren, testwerk en dubbele licenties blijven.</div>
      <div><b>Medio 2030</b>Einde overgangstermijn rijksbreed cloudbeleid. Dat geldt nu voor rijksorganisaties; over medeoverheden is aangekondigd dat er gesprek komt.</div>
      <div><b>Nu</b>Ketenzorgplicht geldt al. De toezichthouder kan ernaar vragen.</div>
    </div>

    <div class="duo" id="duo">
      <b style="font-size:0.9rem" id="duo-kop">Vergelijk met een collega</b>
      <p class="klein" style="margin-top:0.4rem" id="duo-tekst"></p>
      <input readonly id="duo-link" onclick="this.select()">
      <button class="b-stil" style="padding-left:0" onclick="kopieer()">Kopieer link</button>
      <div class="kloof verborgen" id="kloof"></div>
    </div>

    <div class="rapport">
      <h2>Het uitstaprapport</h2>
      <div class="prijs">750 euro excl. btw, eenmalig. Hermeting na een jaar: 250 euro.</div>
      <p>De toets zegt waar je staat. Het rapport zegt wat je nu moet doen, in de taal die je bestuur en de toezichthouder verstaan. Het wordt geschreven op jouw toetsuitkomst, aangevuld met een korte intake over je leveranciers.</p>
      <ul>
        <li>Uitstapprofiel per kritieke leverancier, met wat de wet daarover van je vraagt</li>
        <li>Kant-en-klare paragraaf voor je Cbw-risicoanalyse</li>
        <li>Agendapunt voor het bestuur, met de drie vragen die het moet beantwoorden</li>
        <li>Exitclausules voor je volgende aanbesteding, op basis van de Data Act</li>
        <li>Je eerste negentig dagen: drie acties, elk met een eigenaar</li>
      </ul>
      <p><a href="/rapport/voorbeeld.html" id="link-voorbeeld" style="color:var(--orange);font-family:var(--disp);font-size:0.75rem;letter-spacing:0.08em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid rgba(232,69,0,0.4)">Bekijk een voorbeeldrapport</a></p>

      <div class="aanmeld" id="aanmeld">
        <p class="klein" style="margin-bottom:0.9rem">Bestellen gaat in deze fase per mail. Vraag het rapport aan, dan krijg je persoonlijk antwoord van de initiatiefnemer. Wil je liever meedenken over wat erin hoort? Dat kan ook.</p>
        <a class="b-primair" id="k-rapport" href="#" onclick="return mailtje('update')">Vraag het rapport aan</a>
        <a class="b-tweede" id="k-pilot" href="#" onclick="return mailtje('pilot')">Ik wil meedenken of meedoen</a>
        <p class="klein" style="margin-top:0.9rem">Dat opent je mailprogramma met een bericht aan info@willswitch.nl. Je uitkomst gaat niet automatisch mee; ik vraag erom als dat nodig is.</p>
      </div>
    </div>

    <p class="klein">Dit resultaat is gebaseerd op je eigen antwoorden en is bedoeld als startpunt voor je eigen risicoanalyse. Er is niets gecontroleerd aan de hand van documenten. Het is geen oordeel over naleving van de Cyberbeveiligingswet, de Data Act of het cloudbeleid, en geen juridisch advies.</p>
    <div class="nav"><button class="b-stil" onclick="location.href='/scan/'">Opnieuw beginnen</button><a href="/switch.html" style="font-family:var(--disp);font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--orange);text-decoration:none">Praktijkverhalen</a></div>
  </section>

  <footer class="site"><div class="w">
    <span>Will Switch &middot; willswitch.nl &middot; <a href="/">terug naar de switch</a></span>
    <a class="fonds" href="https://www.sidnfonds.nl/" target="_blank" rel="noopener"><span>Onderzoek met steun van</span><img src="/sidnfonds.png" alt="SIDN fonds" width="150" height="28"></a>
  </div></footer>
</div>
<div class="toast" id="toast" role="status"></div>

<script>
'use strict';
const ROLLEN = [['bestuur','Bestuur of directie'],['cio','CIO, CISO of informatiemanager'],['uitvoering','Beheer, inkoop of uitvoering'],['anders','Anders']];
const ORGS = [['gemeente','Gemeente'],['waterschap','Waterschap'],['provincie','Provincie'],['rijk','Rijksdienst of ZBO'],['gr','Gemeenschappelijke regeling'],['kennis','Kennisinstelling'],['anders','Anders']];
const SYSTEMEN = [
  ['kantoor','Kantoorsuite, mail en documenten'],['cloud','Cloudinfrastructuur'],['zaak','Zaaksysteem'],
  ['fin','Financieel systeem'],['hr','HR en salaris'],['geo','Geo-informatie'],
  ['identiteit','Identiteit en toegang'],['ot','Procesautomatisering'],['ai','AI-assistenten']
];
const HERKOMST = [['0','Amerikaanse leverancier'],['0b','Andere leverancier buiten de EU'],['1','Leverancier in de EU'],['1b','Nederlandse leverancier'],['2','Open source in eigen beheer']];
const CONTRACT = [['0','Weet ik niet'],['1','Bekend, loopt binnen een jaar af'],['2','Bekend, loopt later af'],['2b','Geen contract, eigen beheer']];

const DIM = {
  a: { naam:'Ketenzorgplicht', wet:'Cyberbeveiligingswet', vragen:[
    ['Is per kritieke leverancier vastgelegd wat de impact op je dienstverlening is als hij wegvalt?',
     'De RDI verwacht een risicoanalyse per bestaande leverancier, gericht op continuiteit. Niet alleen: is hij veilig, maar ook: wat als hij er morgen niet meer is.'],
    ['Is vastgelegd wat er met je data en middelen gebeurt bij contracteinde, faillissement of overname van de leverancier?',
     'Dit noemt de toezichthouder letterlijk als onderdeel van de ketenzorgplicht. Het is de vraag die het vaakst ontbreekt.'],
    ['Heeft het bestuur de aanpak van ketenrisico\'s formeel vastgesteld?',
     'Onder de Cbw is het bestuur eindverantwoordelijk en verplicht getraind. Een aanpak die alleen bij IT ligt, telt niet als vastgesteld beleid.'],
    ['Zit ketenrisico standaard in je inkoopproces voor nieuwe leveranciers?',
     'De zorgplicht geldt voor bestaande leveranciers via risicoanalyse en voor nieuwe via inkoop. Beide moeten geregeld zijn.']
  ]},
  b: { naam:'Overstaprecht', wet:'Data Act', vragen:[
    ['Weet je van je clouddiensten welke data exporteerbaar is, en in welk formaat?',
     'De Data Act verplicht aanbieders om dit in het contract te zetten. Als jij het niet weet, staat het er waarschijnlijk niet in, of heeft niemand het gelezen.'],
    ['Staan in je cloudcontracten opzegtermijn en overgangstermijn zoals de Data Act die voorschrijft?',
     'Maximaal twee maanden opzegtermijn, daarna overstappen binnen dertig dagen, ook naar eigen infrastructuur. Dit geldt ook voor lopende contracten.'],
    ['Is ooit een export of terughaalactie daadwerkelijk getest?',
     'Een recht dat je nooit hebt uitgeoefend is een aanname. Een test van een dag vertelt je meer dan een contract van honderd pagina\'s.']
  ]},
  c: { naam:'Exitplan', wet:'Rijkscloudbeleid', vragen:[
    ['Is er per kritieke dienst een exitplan, inclusief het scenario dat de dienst plotseling wegvalt?',
     'Het rijkscloudbeleid eist dit expliciet, en verplicht melding bij CIO Rijk. Voor medeoverheden volgt hetzelfde. Een migratieplan is niet hetzelfde als een plan voor plotseling wegvallen.'],
    ['Is er een reeel alternatief benoemd, waarmee ook echt gesproken is?',
     'Een alternatief op papier is geen alternatief. De vraag is of iemand het gesprek heeft gevoerd en weet wat een overstap zou kosten.'],
    ['Is er een bestuurlijk eigenaar met mandaat en budget voor de exit?',
     'Uit ons onderzoek onder 62 vakmensen: de grootste blokkade is niet techniek maar dat niemand zich eigenaar voelt. Zonder eigenaar blijft elk plan een plan.']
  ]}
};
const ANTW = [['2','Ja'],['1','Deels'],['0','Nee'],['x','Niemand weet het']];

const S = { rol:null, org:null, sys:[], herkomst:{}, contract:{}, a:{}, b:{}, c:{} };
const el = id => document.getElementById(id);
function toast(t){ const x=el('toast'); x.textContent=t; x.classList.add('zien'); setTimeout(()=>x.classList.remove('zien'),3000); }
function naar(n){
  for(let i=0;i<=6;i++) el('s'+i).classList.toggle('verborgen', i!==n);
  [...el('stappen').children].forEach((b,i)=>b.classList.toggle('aan', i < n));
  window.scrollTo({top:0});
  if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({path:'scan/stap-'+n, event:true});
}

/* 1 */
function keuzeknoppen(cid, lijst, key, single, cb){
  const c=el(cid); c.innerHTML='';
  lijst.forEach(([v,t])=>{
    const b=document.createElement('button'); b.className='keuze'; b.type='button';
    b.innerHTML='<span class="rond"></span>'+t;
    b.onclick=()=>{ S[key]=v; [...c.children].forEach(k=>k.classList.remove('aan')); b.classList.add('aan'); cb&&cb(); };
    c.appendChild(b);
  });
}
keuzeknoppen('rol', ROLLEN, 'rol', true, ()=>el('k1').disabled=!(S.rol&&S.org));
keuzeknoppen('org', ORGS, 'org', true, ()=>el('k1').disabled=!(S.rol&&S.org));

/* 2 */
(function(){
  const k=el('kaart');
  SYSTEMEN.forEach(([id,naam])=>{
    const t=document.createElement('button'); t.className='tegel'; t.type='button'; t.id='t-'+id;
    t.innerHTML='<span class="naam">'+naam+'</span><span class="stat"><i></i><i></i></span>';
    t.onclick=()=>{
      const i=S.sys.indexOf(id);
      if(i>=0){ S.sys.splice(i,1); delete S.herkomst[id]; delete S.contract[id];
        t.className='tegel';
        [...t.querySelector('.stat').children].forEach(b=>b.className='');   /* balkjes leegmaken */ }
      else { if(S.sys.length>=5){ toast('Maximaal vijf. Kies je kritiekste.'); return; } S.sys.push(id); t.classList.add('aan'); }
      bouwSys(); checkK2();
    };
    k.appendChild(t);
  });
})();
function bouwSys(){
  const c=el('sysvragen'); c.innerHTML='';
  S.sys.forEach(id=>{
    const naam=SYSTEMEN.find(s=>s[0]===id)[1];
    const d=document.createElement('div'); d.className='sysblok';
    d.innerHTML='<div class="kop"><b>'+naam+'</b><span class="klein">twee feiten</span></div>'
      +'<div class="vraagje">Wie levert het?</div><div class="opties" data-k="herkomst" data-s="'+id+'">'
      +HERKOMST.map(([v,t])=>'<button type="button" data-v="'+v+'">'+t+'</button>').join('')+'</div>'
      +'<div class="vraagje">Weet je wanneer het contract afloopt?</div><div class="opties" data-k="contract" data-s="'+id+'">'
      +CONTRACT.map(([v,t])=>'<button type="button" data-v="'+v+'">'+t+'</button>').join('')+'</div>';
    d.querySelectorAll('.opties button').forEach(b=>{
      const grp=b.parentElement, k=grp.dataset.k, s=grp.dataset.s;
      if(S[k][s]===b.dataset.v) b.classList.add('aan');
      b.onclick=()=>{ S[k][s]=b.dataset.v; [...grp.children].forEach(x=>x.classList.remove('aan')); b.classList.add('aan'); tegelStatus(s); checkK2(); };
    });
    c.appendChild(d);
  });
}
function tegelStatus(id){
  const t=el('t-'+id); const st=t.querySelector('.stat').children;
  const h=S.herkomst[id], c=S.contract[id];
  st[0].className = h ? 'o'+h[0] : ''; st[1].className = c ? 'c'+c[0] : '';
  t.classList.toggle('klaar', !!(h&&c));
}
function checkK2(){
  const n = S.sys.length;
  const open = S.sys.filter(id=>!S.herkomst[id]||!S.contract[id]);
  const klaar = n>=1 && open.length===0;
  el('k2').disabled = !klaar;
  const st = el('sysstatus');
  if (n===0) st.textContent='Kies eerst je systemen, dan verschijnen de vragen eronder.';
  else if (open.length) {
    const namen = open.map(id=>SYSTEMEN.find(s=>s[0]===id)[1]);
    st.innerHTML='Nog invullen: <b>'+namen.join('</b>, <b>')+'</b>';
  }
  else if (n===1) st.innerHTML='<b>1 systeem ingevuld.</b> Je kunt verder, of er nog een paar kiezen voor een vollediger beeld.';
  else st.innerHTML='<b>'+n+' systemen ingevuld.</b> Je kunt verder.';
}

/* 3,4,5 */
function bouwDim(key, cid, knop){
  const c=el(cid); c.innerHTML='';
  DIM[key].vragen.forEach(([tekst,toel],i)=>{
    const d=document.createElement('div'); d.className='vraagkaart';
    d.innerHTML='<div class="tekst">'+tekst+'</div><div class="antw">'
      +ANTW.map(([v,t])=>'<button type="button" data-v="'+v+'">'+t+'</button>').join('')
      +'</div><div class="toel">'+toel+'</div>';
    d.querySelector('.tekst').onclick=()=>d.classList.toggle('open');
    d.querySelectorAll('.antw button').forEach(b=>{
      b.onclick=()=>{ S[key][i]=b.dataset.v; [...b.parentElement.children].forEach(x=>x.className=''); b.className='a'+b.dataset.v;
        el(knop).disabled = Object.keys(S[key]).length < DIM[key].vragen.length; };
    });
    c.appendChild(d);
  });
}
bouwDim('a','vr-a','k3'); bouwDim('b','vr-b','k4'); bouwDim('c','vr-c','k5');

/* 6 */
function dekking(key){
  /* Telt alleen de vragen die beantwoord zijn. Een 'ik weet het niet' verlaagt de
     score niet, maar wordt apart geteld: onbekend is iets anders dan niet geregeld. */
  const n=DIM[key].vragen.length;
  let pts=0, beantwoord=0, ja=0, deels=0, nee=0, onbekend=0;
  for(let i=0;i<n;i++){
    const v=S[key][i];
    if(v==='x'){ onbekend++; continue; }
    beantwoord++; pts+=Number(v||0);
    if(v==='2') ja++; else if(v==='1') deels++; else nee++;
  }
  return {
    pct: beantwoord ? Math.round(100*pts/(2*beantwoord)) : null,
    ja, deels, nee, onbekend, beantwoord, totaal:n
  };
}
function scores(){
  const nietEU = S.sys.filter(id=>S.herkomst[id] && S.herkomst[id][0]==='0');
  const onbSys = S.sys.filter(id=>S.contract[id]==='0');
  /* de overlap expliciet, in plaats van twee losse tellingen door elkaar halen */
  const nietEUonb = nietEU.filter(id=>S.contract[id]==='0');
  const binnenJaar = S.sys.filter(id=>S.contract[id]==='1');
  const eigen = S.sys.filter(id=>S.herkomst[id]==='2');
  return { n:S.sys.length, nietEU:nietEU.length, onb:onbSys.length,
           nietEUonb:nietEUonb.length, binnenJaar:binnenJaar.length, eigen:eigen.length,
           a:dekking('a'), b:dekking('b'), c:dekking('c') };
}
function resultaat(){
  const r=scores();
  const onbekend = r.a.onbekend + r.b.onbekend + r.c.onbekend;
  const eig = S.c[2];   /* bestuurlijk eigenaar: 2 ja, 1 deels, 0 nee, x onbekend */
  const gem = [r.a.pct, r.b.pct, r.c.pct].filter(v=>v!==null);
  const gemiddeld = gem.length ? Math.round(gem.reduce((a,b)=>a+b,0)/gem.length) : null;
  /* Kernzin: volgt uit wat er is ingevuld, in volgorde van wat het meest opvalt.
     Geen uitspraken over wat een toezichthouder zal vinden of hoe je scoort
     ten opzichte van anderen: daar hebben we de gegevens niet voor. */
  let getal, zin;
  if (onbekend>=3){
    getal=onbekend+' van 10';
    zin='vragen kon je nu niet beantwoorden. Dat hoeft geen probleem te zijn, maar het betekent wel dat het antwoord ergens anders in de organisatie ligt. Uitzoeken wie het weet is je eerste stap.';
  }
  else if (r.nietEUonb>0){
    getal=r.nietEUonb+' van '+r.nietEU;
    zin='systemen bij een leverancier buiten de EU heeft geen bekend contracteinde. Die combinatie maakt plannen lastig: je kunt geen opzegtermijn aanhouden die je niet kent.';
  }
  else if (eig==='0'){
    getal='Geen';
    zin='bestuurlijk eigenaar met mandaat en budget voor de exit, volgens je eigen opgave. Zonder eigenaar blijft elk plan een plan.';
  }
  else if (eig==='1'){
    getal='Deels';
    zin='geregeld eigenaarschap. Er is iemand, maar mandaat of budget ontbreekt. Dat is meestal het punt waarop een exit blijft liggen.';
  }
  else if (eig==='x'){
    getal='Onbekend';
    zin='of er een bestuurlijk eigenaar is voor de exit. Uitzoeken of die er is, en wie het dan is, is een kleine stap met veel gevolg.';
  }
  else if (r.nietEU >= Math.ceil(r.n/2) && r.n>1){
    getal=r.nietEU+' van '+r.n;
    zin='kritieke systemen draait bij een leverancier buiten de EU. Dat is niet per definitie een probleem, maar het bepaalt wel welke regels op je van toepassing zijn.';
  }
  else if (r.b.pct!==null && r.b.pct<50){
    getal=r.b.pct+'%';
    zin='van je antwoorden over het overstaprecht was positief. De Data Act geeft je rechten die je pas kunt gebruiken als je weet wat er in je contract staat.';
  }
  else if (gemiddeld!==null){
    getal=gemiddeld+'%';
    zin='van je antwoorden was positief, gemiddeld over de drie onderwerpen. De basis staat. Leg vast wat je hebt, want dat is wat je later moet laten zien.';
  }
  else { getal='Geen beeld'; zin='op basis van je antwoorden. Vul de toets opnieuw in om een uitkomst te krijgen.'; }
  el('kern-getal').textContent=getal; el('kern-zin').textContent=zin;
  el('c-nieteu').textContent=r.nietEU+' van '+r.n;
  el('c-onbekend').textContent=r.onb+' van '+r.n;
  /* kaart */
  const k=el('kaart-uit'); k.innerHTML='';
  S.sys.forEach(id=>{ const naam=SYSTEMEN.find(s=>s[0]===id)[1]; const d=document.createElement('div'); d.className='tegel uit';
    d.style.cursor='default'; d.innerHTML='<span class="naam">'+naam+'</span><span class="stat"><i class="o'+S.herkomst[id][0]+'"></i><i class="c'+S.contract[id][0]+'"></i></span>'; k.appendChild(d); });
  /* dekking */
  const dk=el('dekking'); dk.innerHTML='';
  ['a','b','c'].forEach(key=>{
    const d=r[key];
    const delen=[];
    if(d.ja) delen.push(d.ja+' geregeld');
    if(d.deels) delen.push(d.deels+' deels');
    if(d.nee) delen.push(d.nee+' niet geregeld');
    if(d.onbekend) delen.push(d.onbekend+' onbekend');
    const div=document.createElement('div'); div.className='dek';
    div.innerHTML='<div class="lbl"><b>'+DIM[key].naam+' <span style="color:var(--ink-faint);font-weight:400">'+DIM[key].wet+'</span></b>'
      +'<span>'+delen.join(' &middot; ')+'</span></div>'
      +'<div class="staaf">'
      +(d.ja?'<i class="v-ja" style="flex:'+d.ja+'"></i>':'')
      +(d.deels?'<i class="v-deels" style="flex:'+d.deels+'"></i>':'')
      +(d.nee?'<i class="v-nee" style="flex:'+d.nee+'"></i>':'')
      +(d.onbekend?'<i class="v-onb" style="flex:'+d.onbekend+'"></i>':'')
      +'</div>';
    dk.appendChild(div); });
  /* eerste stap */
  let kop, tekst;
  if (onbekend>=3){ kop='Zoek uit wie het weet.'; tekst='Op '+onbekend+' vragen was nu geen antwoord. Dat zegt weinig over hoe goed het geregeld is, en veel over waar de kennis zit. Zet de onbeantwoorde vragen op een A4, loop ze langs met inkoop, beheer en de verantwoordelijke bestuurder, en doe de toets daarna opnieuw. Dan weet je pas waar je staat.'; }
  else if (eig==='0' || eig==='x'){ kop='Begin met een eigenaar.'; tekst='Zonder iemand met mandaat en budget blijft elk plan een plan. Wijs een bestuurlijk eigenaar aan voor de exit, en geef die persoon de opdracht om met inkoop en beheer in kaart te brengen wat er bij wegvallen van een leverancier gebeurt.'; }
  else if (r.onb>0){ kop='Haal je contracteindes boven tafel.'; tekst='Van '+r.onb+' kritiek'+(r.onb>1?'e systemen':' systeem')+' weet je niet wanneer het contract afloopt. Dat is het goedkoopste wat je kunt oplossen, en zonder die datum kun je geen opzegtermijn plannen, geen exit voorbereiden en geen aanbesteding op tijd starten.'; }
  else if (r.b.pct<50){ kop='Test een export voor 12 januari 2027.'; tekst='Kies je kleinste clouddienst en haal de data terug. Een dag werk. Je leert wat er exporteerbaar is, in welk formaat, en wat het kost. Na 12 januari mag de leverancier daar niets meer voor rekenen, dus je onderhandelingspositie wordt alleen maar beter.'; }
  else if (r.a.pct<50){ kop='Leg per leverancier het wegval-scenario vast.'; tekst='Eén A4 per kritieke leverancier: wat gebeurt er met onze dienstverlening als hij morgen stopt, en wat gebeurt er met onze data. Dat is exact wat de RDI onder de ketenzorgplicht verstaat, en het is het stuk dat bij de meeste organisaties ontbreekt.'; }
  else if (r.c.pct<75){ kop='Voer één gesprek met een alternatief.'; tekst='Je hebt de basis. Wat ontbreekt is een alternatief waarmee echt gesproken is. Kies je grootste afhankelijkheid en voer één verkennend gesprek. Niet om over te stappen, maar om te weten wat het zou kosten. Dat verandert elke volgende onderhandeling.'; }
  else { kop='Leg vast wat je hebt.'; tekst='Je staat er beter voor dan de meeste organisaties. Zet het op papier, laat het bestuur het vaststellen en plan een jaarlijkse hermeting. Dat is je bewijs richting de toezichthouder, en je zekerheid als er iemand vertrekt.'; }
  el('stap-kop').textContent=kop; el('stap-tekst').textContent=tekst;
  /* duo */
  const ander = S.rol==='bestuur' ? 'iemand uit de uitvoering' : (S.rol==='uitvoering' ? 'je bestuurder' : 'een collega uit een andere laag');
  el('duo-tekst').textContent='Laat '+ander+' dezelfde toets doen via deze link. Je ziet dan waar jullie beeld uiteenloopt, en dat is meestal de plek waar het werk ligt.';
  el('duo-link').value = location.origin+'/scan/?v='+codeer(r);
  toonKloof(r);
  /* rapport */
  stuurScores(r);
  if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({path:'scan/afgerond', event:true});
}
function codeer(r){ return btoa(JSON.stringify({rol:S.rol,org:S.org,n:r.n,sys:S.sys.slice().sort(),
  ne:r.nietEU,ob:r.onb,a:r.a.pct,b:r.b.pct,c:r.c.pct,x:r.a.onbekend+r.b.onbekend+r.c.onbekend})).replace(/=+$/,''); }
function toonKloof(r){
  const p=new URLSearchParams(location.search).get('v'); if(!p) return;
  let o; try{ o=JSON.parse(atob(p)); }catch(e){ return; }
  if(!o||o.rol===S.rol) return;
  const naam=v=>({bestuur:'Bestuur',cio:'CIO',uitvoering:'Uitvoering',anders:'Collega'})[v]||v;
  const mijn=S.sys.slice().sort().join(','), hun=(o.sys||[]).slice().sort().join(',');
  const zelfdeScope = mijn===hun;
  const rijen=[['Ketenzorgplicht',o.a,r.a.pct],['Overstaprecht',o.b,r.b.pct],['Exitplan',o.c,r.c.pct],['Vragen nog te beantwoorden',o.x,r.a.onbekend+r.b.onbekend+r.c.onbekend]];
  const k=el('kloof'); k.classList.remove('verborgen');
  k.innerHTML='<div style="font-weight:700"><span></span><span>'+naam(o.rol)+'</span><span>'+naam(S.rol)+'</span></div>'
    +rijen.map(([l,a,b])=>{ const d=Math.abs(a-b); const groot=(l.startsWith('Vragen')? d>=2 : d>=25);
      const fmt=v=>(v===null||v===undefined)?'-':(l.startsWith('Vragen')?v:v+'%');
      return '<div><span>'+l+'</span><span>'+fmt(a)+'</span><span class="'+(groot?'verschil':'')+'">'+fmt(b)+'</span></div>'; }).join('');
  el('duo-kop').textContent='Verschil in beeld';
  el('duo-tekst').innerHTML='Twee mensen uit dezelfde organisatie, twee beelden. Waar het gemarkeerd is, loopt het uiteen. Dat kan aan eigenaarschap liggen, maar net zo goed aan kennis, interpretatie of aan een andere systeemselectie. Het is een startpunt voor een gesprek, geen conclusie.'
    + (zelfdeScope ? '' : '<br><br><b>Let op:</b> jullie beoordeelden niet dezelfde systemen. Vergelijk de onderwerpen, niet de aantallen.');
}
(function(){ const v=el('link-voorbeeld'); if(v) v.addEventListener('click',()=>{ if(window.goatcounter&&window.goatcounter.count) window.goatcounter.count({path:'scan/voorbeeldrapport',event:true}); }); })();
function kopieer(){ el('duo-link').select(); try{ document.execCommand('copy'); toast('Link gekopieerd'); }catch(e){ toast('Selecteer de link en kopieer hem'); } }
function stuurScores(r){
  /* alleen geaggregeerd, geen namen, geen vrije tekst */
  const body={org:S.org,rol:S.rol,n:r.n,niet_eu:r.nietEU,contract_onbekend:r.onb,a:r.a.pct,b:r.b.pct,c:r.c.pct,onbekend:r.a.onbekend+r.b.onbekend+r.c.onbekend};
  try{ fetch('/api/scan.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),keepalive:true}).catch(()=>{}); }catch(e){}
}
function mailtje(soort){
  const r = scores();
  const rolNaam = {bestuur:'bestuur of directie',cio:'CIO, CISO of informatiemanager',uitvoering:'beheer, inkoop of uitvoering',anders:'anders'}[S.rol] || S.rol;
  const onderwerp = soort==='pilot'
    ? 'Uitstaptoets: ik wil meedenken'
    : 'Uitstaptoets: aanvraag uitstaprapport';
  const regels = [
    soort==='pilot'
      ? 'Ik heb de uitstaptoets gedaan en wil graag meedenken of meedoen aan een pilot.'
      : 'Ik heb de uitstaptoets gedaan en wil het uitstaprapport (750 euro excl. btw) aanvragen.',
    '',
    'Mijn organisatie: ',
    'Mijn rol: ' + rolNaam,
    'Type organisatie: ' + S.org,
    'Aantal kritieke systemen in de toets: ' + r.n,
    '',
    'Waar ik tegenaan loop: ',
    ''
  ];
  location.href = 'mailto:info@willswitch.nl'
    + '?subject=' + encodeURIComponent(onderwerp)
    + '&body=' + encodeURIComponent(regels.join('\n'));
  if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({path:'scan/aanmelding-'+soort, event:true});
  return false;
}
function bestel(){
  /* FASE 0: nog geen bestelling. Zet dit terug naar de bestelpagina zodra betalen aan mag:
     location.href='/bestel/#'+btoa(JSON.stringify(S)).replace(/=+$/,''); */
  /* de klik wordt geteld: dat is het vraagbewijs voor fase 2 */
  toast('Genoteerd. Bestellen gaat in deze fase per mail, zie de knop hierboven.');
  if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({path:'scan/bestel-klik', event:true});
}
/* deep link: v = uitkomst van een ander, rol = vooraf gekozen */
(function(){ const q=new URLSearchParams(location.search); if(q.get('v')) { const o=(()=>{try{return JSON.parse(atob(q.get('v')))}catch(e){return null}})(); if(o){ el('duo-kop').textContent=''; } } })();
</script>
  <!-- Privacyvriendelijke analytics (GoatCounter, geen cookies) -->
  <script data-goatcounter="https://willswitch.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
'''


def build_scan():
    return PAGE
