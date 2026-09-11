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
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
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
    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    :root {
      --orange:#E84500; --paper:#F0EDE6; --paper-warm:#E8E3D6; --white:#FBFAF7;
      --ink:#1a1612; --ink-soft:#4a443c; --ink-faint:rgba(26,22,18,0.45);
      --rule:rgba(26,22,18,0.14);
      --ok:#2F6F4E; --warn:#B8760F; --bad:#B3453A;
      --mono:'Space Mono', monospace; --disp:'Orbitron', monospace;
    }
    html { font-size:16px; }
    body { background:var(--paper); color:var(--ink); font-family:var(--mono); line-height:1.6; }
    .wrap { max-width:46rem; margin:0 auto; padding:0 1.5rem 5rem; }
    .topbar {
      display:flex; justify-content:space-between; align-items:center;
      padding:2rem 0 1.2rem; border-bottom:2px solid var(--ink);
      font-family:var(--disp); font-size:0.7rem; letter-spacing:0.22em; text-transform:uppercase;
    }
    .topbar a { color:var(--ink); text-decoration:none; }
    .topbar a:hover { color:var(--orange); }
    .topbar .sub { color:var(--ink-faint); }

    .stappen { display:flex; gap:5px; margin:1.6rem 0 2.4rem; }
    .stappen i { flex:1; height:4px; background:var(--rule); }
    .stappen i.aan { background:var(--orange); }

    h1 { font-family:var(--disp); font-size:clamp(1.6rem, 4.4vw, 2.5rem); font-weight:700; line-height:1.12; margin-bottom:1.1rem; }
    h2 { font-family:var(--disp); font-size:clamp(1.15rem, 3vw, 1.5rem); font-weight:700; line-height:1.2; margin-bottom:0.8rem; }
    h3 { font-family:var(--disp); font-size:0.95rem; font-weight:700; margin:1.6rem 0 0.6rem; }
    p { color:var(--ink-soft); font-size:0.95rem; margin-bottom:1rem; max-width:40rem; }
    p.lead { color:var(--ink); font-size:1.05rem; }
    .klein { font-size:0.82rem; color:var(--ink-faint); }
    .wet {
      border-left:3px solid var(--orange); padding:0.9rem 1.1rem; margin:1.4rem 0;
      background:var(--white); font-size:0.88rem; color:var(--ink-soft);
    }
    .wet .bron { display:block; margin-top:0.5rem; font-size:0.72rem; color:var(--ink-faint); }

    button { font-family:var(--disp); font-size:0.74rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; cursor:pointer; border:none; border-radius:3px; padding:0.95rem 1.5rem; transition:background 0.15s ease, transform 0.06s ease; }
    button:active { transform:translateY(1px); }
    button:focus-visible { outline:3px solid var(--orange); outline-offset:2px; }
    button:disabled { opacity:0.35; cursor:not-allowed; }
    .b-primair { background:var(--orange); color:var(--paper); }
    .b-primair:hover:not(:disabled) { background:var(--ink); }
    #sysstatus b { color:var(--ink); }
    .b-stil { background:none; color:var(--ink-faint); padding:0.95rem 0.5rem; letter-spacing:0.06em; }
    .b-stil:hover { color:var(--ink); }
    .nav { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-top:2rem; }

    .keuzes { display:grid; gap:0.6rem; margin:1.2rem 0; }
    .keuzes.twee { grid-template-columns:1fr 1fr; }
    .keuze { display:flex; align-items:center; gap:0.8rem; background:var(--white); border:1px solid var(--rule); padding:0.95rem 1.1rem; cursor:pointer; text-align:left; font:inherit; font-size:0.9rem; color:var(--ink); border-radius:3px; letter-spacing:0; text-transform:none; }
    .keuze:hover { border-color:var(--ink); }
    .keuze.aan { border-color:var(--orange); background:#FBEDE5; box-shadow:inset 0 0 0 1px var(--orange); }
    .keuze .rond { width:16px; height:16px; border:2px solid var(--rule); border-radius:50%; flex:none; }
    .keuze.aan .rond { border-color:var(--orange); background:radial-gradient(circle, var(--orange) 45%, transparent 50%); }
    @media (max-width:560px) { .keuzes.twee { grid-template-columns:1fr; } }

    /* inventaris: de concentratiekaart */
    .kaart { display:grid; grid-template-columns:repeat(auto-fill, minmax(140px, 1fr)); gap:0.6rem; margin:1.2rem 0 0.4rem; }
    .tegel { background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:0.8rem 0.85rem; min-height:92px; cursor:pointer; text-align:left; font:inherit; letter-spacing:0; text-transform:none; position:relative; color:var(--ink); }
    .tegel:hover { border-color:var(--ink); }
    .tegel.aan { border-color:var(--ink); border-width:2px; padding:calc(0.8rem - 1px) calc(0.85rem - 1px); }
    .tegel .naam { font-size:0.82rem; font-weight:700; line-height:1.3; display:block; }
    .tegel .stat { position:absolute; left:0.85rem; right:0.85rem; bottom:0.7rem; height:6px; display:flex; gap:3px; }
    .tegel .stat i { flex:1; background:var(--rule); border-radius:1px; }
    .tegel .stat i.o0 { background:var(--bad); } .tegel .stat i.o1 { background:var(--warn); } .tegel .stat i.o2 { background:var(--ok); }
    .tegel .stat i.c0 { background:var(--bad); } .tegel .stat i.c1 { background:var(--warn); } .tegel .stat i.c2 { background:var(--ok); }
    .tegel.aan::after { content:"gekozen"; position:absolute; top:0.5rem; right:0.6rem; font-family:var(--disp); font-size:0.52rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--orange); }
    .tegel.klaar::after { content:"ingevuld"; color:var(--ok); }
    .tegel.uit::after { content:none; }
    .tegel.uit { border-color:var(--rule); }

    .sysblok { background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:1.1rem 1.2rem; margin-bottom:0.9rem; }
    .sysblok .kop { display:flex; justify-content:space-between; align-items:baseline; gap:1rem; margin-bottom:0.6rem; }
    .sysblok .kop b { font-size:0.92rem; }
    .sysblok .kop .klein { font-family:var(--disp); font-size:0.58rem; letter-spacing:0.12em; text-transform:uppercase; }
    .vraagje { font-size:0.85rem; margin:0.7rem 0 0.4rem; color:var(--ink); }
    .opties { display:flex; flex-wrap:wrap; gap:0.4rem; }
    .opties button { font-family:var(--mono); font-size:0.78rem; font-weight:400; letter-spacing:0; text-transform:none; background:var(--paper); color:var(--ink-soft); border:1px solid var(--rule); padding:0.5rem 0.75rem; border-radius:3px; }
    .opties button:hover { border-color:var(--ink); color:var(--ink); }
    .opties button.aan { background:var(--ink); color:var(--paper); border-color:var(--ink); }

    /* dimensievragen */
    .vraagkaart { background:var(--white); border:1px solid var(--rule); border-radius:3px; padding:1.1rem 1.2rem; margin-bottom:0.8rem; }
    .vraagkaart .tekst { font-size:0.92rem; color:var(--ink); margin-bottom:0.7rem; }
    .vraagkaart .toel { font-size:0.78rem; color:var(--ink-faint); margin-top:0.55rem; display:none; }
    .vraagkaart.open .toel { display:block; }
    .antw { display:grid; grid-template-columns:repeat(4, 1fr); gap:0.4rem; }
    .antw button { font-family:var(--mono); font-size:0.76rem; font-weight:400; letter-spacing:0; text-transform:none; background:var(--paper); color:var(--ink-soft); border:1px solid var(--rule); padding:0.6rem 0.3rem; border-radius:3px; }
    .antw button:hover { border-color:var(--ink); color:var(--ink); }
    .antw button.a2 { background:#E6F0EA; border-color:var(--ok); color:var(--ok); font-weight:700; }
    .antw button.a1 { background:#F6EEDC; border-color:var(--warn); color:var(--warn); font-weight:700; }
    .antw button.a0 { background:#F6E6E4; border-color:var(--bad); color:var(--bad); font-weight:700; }
    .antw button.ax { background:var(--paper-warm); border-color:var(--ink-soft); color:var(--ink); font-weight:700; }
    @media (max-width:480px) { .antw { grid-template-columns:1fr 1fr; } }

    /* resultaat */
    .kern { border:2px solid var(--ink); background:var(--white); padding:1.4rem 1.5rem; margin:1.6rem 0; }
    .kern .groot { font-family:var(--disp); font-size:2.4rem; font-weight:700; line-height:1; color:var(--orange); }
    .kern .zin { font-size:0.98rem; color:var(--ink); margin-top:0.6rem; }
    .dekking { margin:1.6rem 0; }
    .dek { margin-bottom:1rem; }
    .dek .lbl { display:flex; justify-content:space-between; align-items:baseline; font-size:0.85rem; margin-bottom:0.35rem; }
    .dek .lbl b { font-family:var(--disp); font-size:0.78rem; }
    .dek .lbl span { font-family:var(--disp); font-size:0.78rem; color:var(--ink-faint); }
    .dek .balk { height:12px; background:var(--rule); border-radius:2px; overflow:hidden; }
    .dek .staaf { display:flex; height:14px; border-radius:2px; overflow:hidden; background:var(--rule); }
    .dek .staaf i { display:block; }
    .dek .staaf .v-ja { background:var(--ok); }
    .dek .staaf .v-deels { background:var(--warn); }
    .dek .staaf .v-nee { background:var(--bad); }
    .dek .staaf .v-onb { background:#B9B3A8; }
    .dek .lbl span { font-family:var(--mono); font-size:0.76rem; letter-spacing:0; }
    .dek .balk i { display:block; height:100%; width:0; background:var(--orange); transition:width 0.6s ease; }
    .dek .klein { margin-top:0.35rem; }
    .concentratie { display:grid; grid-template-columns:1fr 1fr; gap:0.7rem; margin:1.2rem 0; }
    .cijfer { background:var(--paper-warm); border:1px solid var(--rule); padding:0.9rem 1rem; }
    .cijfer b { font-family:var(--disp); font-size:1.5rem; display:block; line-height:1; }
    .cijfer span { font-size:0.78rem; color:var(--ink-soft); }
    .stap1 { background:var(--ink); color:var(--paper); padding:1.4rem 1.5rem; margin:1.8rem 0; }
    .stap1 h2 { color:var(--paper); }
    .stap1 p { color:rgba(240,237,230,0.8); }
    .deadline { display:flex; gap:0.8rem; flex-wrap:wrap; margin:1.2rem 0; }
    .deadline div { flex:1; min-width:160px; background:var(--white); border:1px solid var(--rule); padding:0.8rem 0.9rem; font-size:0.8rem; }
    .deadline b { font-family:var(--disp); font-size:0.85rem; color:var(--orange); display:block; margin-bottom:0.2rem; }
    .duo { background:var(--white); border:1px dashed var(--ink-faint); padding:1.1rem 1.2rem; margin:1.4rem 0; }
    .duo input { width:100%; font-family:var(--mono); font-size:0.8rem; padding:0.6rem 0.7rem; border:1px solid var(--rule); background:var(--paper); margin-top:0.6rem; }
    .kloof { margin-top:0.8rem; display:grid; gap:0.4rem; }
    .kloof div { display:grid; grid-template-columns:1fr auto auto; gap:0.8rem; font-size:0.8rem; align-items:center; }
    .kloof .verschil { color:var(--bad); font-weight:700; }
    .rapport { background:var(--paper-warm); border:1px solid var(--rule); padding:1.5rem; margin:2rem 0 1rem; }
    .rapport ul { list-style:none; margin:0.8rem 0 1.2rem; }
    .rapport li { padding:0.4rem 0; border-bottom:1px solid var(--rule); font-size:0.88rem; }
    .aanmeld { margin-top:1.2rem; padding-top:1.2rem; border-top:1px solid var(--rule); }
    .aanmeld .b-primair, .aanmeld .b-tweede {
      display:inline-block; text-decoration:none; margin:0 0.5rem 0.5rem 0;
      font-family:var(--disp); font-size:0.74rem; font-weight:700;
      letter-spacing:0.1em; text-transform:uppercase;
      padding:0.95rem 1.5rem; border-radius:3px; cursor:pointer;
    }
    .aanmeld .b-primair { background:var(--orange); color:var(--paper); border:1px solid var(--orange); }
    .aanmeld .b-primair:hover { background:var(--ink); border-color:var(--ink); }
    .b-tweede {
      font-family:var(--disp); font-size:0.74rem; font-weight:700; letter-spacing:0.1em;
      text-transform:uppercase; padding:0.95rem 1.5rem; border-radius:3px;
      background:transparent; color:var(--orange); border:1px solid rgba(232,69,0,0.5);
    }
    .b-tweede:hover { background:var(--orange); color:var(--paper); }
    .aanmeld .veld { display:block; margin-bottom:0.7rem; }
    .aanmeld .veld span { display:block; font-size:0.78rem; color:var(--ink-soft); margin-bottom:0.25rem; }
    .aanmeld .veld span i { color:var(--ink-faint); font-style:normal; }
    .aanmeld input { width:100%; font-family:var(--mono); font-size:0.88rem; padding:0.65rem 0.75rem;
      border:1px solid var(--rule); background:var(--white); color:var(--ink); border-radius:3px; }
    .aanmeld input:focus { outline:2px solid var(--orange); border-color:var(--orange); }
    .aanmeld .keuzes { margin:0 0 0.9rem; }
    .aanmeld .keuze { padding:0.7rem 0.9rem; font-size:0.85rem; }
    .melding { margin-top:0.7rem; font-size:0.84rem; display:none; }
    .melding.goed { display:block; color:var(--ok); }
    .melding.fout { display:block; color:var(--bad); }
    .rapport .prijs { font-family:var(--disp); font-size:0.8rem; color:var(--ink-faint); margin-bottom:0.6rem; }
    .toast { position:fixed; left:50%; bottom:1.5rem; transform:translateX(-50%); background:var(--ink); color:var(--paper); padding:0.8rem 1.2rem; font-size:0.82rem; opacity:0; pointer-events:none; transition:opacity 0.3s; max-width:90vw; text-align:center; }
    .toast.zien { opacity:1; }
    .verborgen { display:none !important; }
    footer { margin-top:3rem; padding-top:1.2rem; border-top:1px solid var(--rule); font-size:0.7rem; color:var(--ink-faint); line-height:1.8; }
    @media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
  </style>
</head>
<body>
<div class="wrap">
  <header class="topbar">
    <a href="/">Will Switch</a>
    <span class="sub">uitstaptoets</span>
  </header>
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
      <div class="prijs">in ontwikkeling</div>
      <p>De toets zegt waar je staat. Het rapport zegt wat je nu moet doen, in de taal die je bestuur en de toezichthouder verstaan. Het wordt op dit moment gebouwd, samen met de organisaties die aan dit onderzoek meewerken.</p>
      <ul>
        <li>Uitstapprofiel per kritieke leverancier, met wat de wet daarover van je vraagt</li>
        <li>Kant-en-klare paragraaf voor je Cbw-risicoanalyse</li>
        <li>Agendapunt voor het bestuur, met de drie vragen die het moet beantwoorden</li>
        <li>Exitclausules voor je volgende aanbesteding, op basis van de Data Act</li>
        <li>Je eerste negentig dagen: drie acties, elk met een eigenaar</li>
      </ul>
      <p><a href="/rapport/voorbeeld.html" id="link-voorbeeld" style="color:var(--orange);font-family:var(--disp);font-size:0.75rem;letter-spacing:0.08em;text-transform:uppercase;text-decoration:none;border-bottom:1px solid rgba(232,69,0,0.4)">Bekijk een voorbeeldrapport</a></p>

      <div class="aanmeld" id="aanmeld">
        <p class="klein" style="margin-bottom:0.9rem">Het rapport bestaat nog niet en wordt waarschijnlijk betaald. Wil je horen wanneer het er is, of meedenken over wat erin hoort? Stuur een mail, dan zet ik je op de lijst.</p>
        <a class="b-primair" id="k-rapport" href="#" onclick="return mailtje('update')">Hou me op de hoogte</a>
        <a class="b-tweede" id="k-pilot" href="#" onclick="return mailtje('pilot')">Ik wil meedenken of meedoen</a>
        <p class="klein" style="margin-top:0.9rem">Dat opent je mailprogramma met een bericht aan info@willswitch.nl. Je uitkomst gaat niet automatisch mee; ik vraag erom als dat nodig is.</p>
      </div>
    </div>

    <p class="klein">Dit resultaat is gebaseerd op je eigen antwoorden en is bedoeld als startpunt voor je eigen risicoanalyse. Er is niets gecontroleerd aan de hand van documenten. Het is geen oordeel over naleving van de Cyberbeveiligingswet, de Data Act of het cloudbeleid, en geen juridisch advies.</p>
    <div class="nav"><button class="b-stil" onclick="location.href='/scan/'">Opnieuw beginnen</button><a href="/switch.html" style="font-family:var(--disp);font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;color:var(--orange);text-decoration:none">Praktijkverhalen</a></div>
  </section>

  <footer>
    Will Switch, praktijkonderzoek naar digitale autonomie in de publieke sector.<br>
    Gebouwd met open source, gehost in Nederland, zonder trackingcookies.
  </footer>
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
    : 'Uitstaptoets: hou me op de hoogte van het rapport';
  const regels = [
    soort==='pilot'
      ? 'Ik heb de uitstaptoets gedaan en wil graag meedenken of meedoen aan een pilot.'
      : 'Ik heb de uitstaptoets gedaan en hoor graag wanneer het rapport er is.',
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
  toast('Genoteerd. Het rapport is nog in ontwikkeling; via willswitch.nl hoor je wanneer het er is.');
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
