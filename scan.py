"""De uitstaptoets: gratis scan op /scan/.

Drie verplichtingen, elk met eigen vragen, plus een snelle inventaris die
de concentratie laat zien. Alles draait in de browser. Alleen geaggregeerde
scores gaan naar de server, nooit leveranciersnamen of vrije tekst.

FASE 0 (test): noindex staat aan, bestelknop toont een melding.
"""

PAGE = r'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Uitstaptoets: kun je nog weg bij je leveranciers? | Will Switch</title>
  <meta name="description" content="Gratis toets voor gemeenten, waterschappen en andere publieke organisaties. Toetst in een kwartier je ketenafhankelijkheid tegen de Cyberbeveiligingswet, de Data Act en het rijkscloudbeleid. Geen registratie.">
  <meta name="robots" content="noindex,nofollow">
  <link rel="canonical" href="https://willswitch.nl/scan/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="Uitstaptoets: kun je nog weg bij je leveranciers?">
  <meta property="og:description" content="Toets in een kwartier je ketenafhankelijkheid tegen drie wettelijke verplichtingen. Gratis, geen registratie.">
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
    <p class="lead">Drie wetten stellen sinds kort dezelfde vraag, elk vanuit een andere hoek. De meeste organisaties hebben op geen van de drie een compleet antwoord.</p>
    <div class="wet">
      Sinds 15 augustus 2026 verplicht de Cyberbeveiligingswet je om per kritieke leverancier te weten wat er gebeurt bij contracteinde, faillissement of overname. De Data Act geeft je sinds september 2025 het recht om binnen dertig dagen over te stappen, en verbiedt vanaf 12 januari 2027 overstapkosten. En het rijkscloudbeleid eist een exitplan, ook voor het scenario dat een dienst plotseling wegvalt.
      <span class="bron">Bronnen: RDI, toelichting zorgplicht toeleveringsketen; Verordening (EU) 2023/2854, hoofdstuk VI; Kamerbrief Herziening Rijksbreed Cloudbeleid, juli 2026</span>
    </div>
    <p>Deze toets duurt een kwartier en vraagt geen registratie. Je krijgt direct je concentratiebeeld, ziet per verplichting wat je kunt aantonen en krijgt een eerste stap. Je antwoorden blijven in je browser; alleen scores zonder naam of leverancier gaan naar de server.</p>
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
    <p>Kies er drie tot vijf. Per systeem twee feiten: wie levert het, en weet je wanneer het contract afloopt. Meer niet.</p>
    <div class="kaart" id="kaart"></div>
    <p class="klein">Kies eerst je systemen, dan verschijnen de vragen eronder.</p>
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

    <h3>Wat je per verplichting kunt aantonen</h3>
    <div class="dekking" id="dekking"></div>

    <div class="stap1"><h2 id="stap-kop"></h2><p id="stap-tekst"></p></div>

    <h3>De klok</h3>
    <div class="deadline">
      <div><b>12 januari 2027</b>Overstapkosten bij clouddiensten zijn verboden. Ook voor lopende contracten.</div>
      <div><b>Medio 2030</b>Einde overgangstermijn rijkscloudbeleid. Medeoverheden volgen.</div>
      <div><b>Nu</b>Ketenzorgplicht geldt al. De toezichthouder kan ernaar vragen.</div>
    </div>

    <div class="duo" id="duo">
      <b style="font-size:0.9rem" id="duo-kop">Zie je mandaatkloof</b>
      <p class="klein" style="margin-top:0.4rem" id="duo-tekst"></p>
      <input readonly id="duo-link" onclick="this.select()">
      <button class="b-stil" style="padding-left:0" onclick="kopieer()">Kopieer link</button>
      <div class="kloof verborgen" id="kloof"></div>
    </div>

    <div class="rapport">
      <h2>Het uitstaprapport</h2>
      <div class="prijs">750 euro excl. btw, eenmalig. Pdf in je mailbox binnen een werkdag.</div>
      <p>De toets zegt waar je staat. Het rapport zegt wat je nu moet doen, in de taal die je bestuur en de toezichthouder verstaan.</p>
      <ul>
        <li>Uitstapprofiel per kritieke leverancier, met wat de wet daarover van je vraagt</li>
        <li>Kant-en-klare paragraaf voor je Cbw-risicoanalyse</li>
        <li>Agendapunt voor het bestuur, met de drie vragen die het moet beantwoorden</li>
        <li>Exitclausules voor je volgende aanbesteding, op basis van de Data Act</li>
        <li>Je eerste negentig dagen: drie acties, elk met een eigenaar</li>
      </ul>
      <p class="klein" id="rapport-noot"></p>
      <button class="b-primair" id="k-rapport" onclick="bestel()">Bestel het rapport</button>
    </div>

    <p class="klein">Dit resultaat is input voor je eigen risicoanalyse. Het is geen oordeel over naleving van de Cyberbeveiligingswet of andere wetgeving.</p>
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
      if(i>=0){ S.sys.splice(i,1); delete S.herkomst[id]; delete S.contract[id]; t.className='tegel'; }
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
function checkK2(){ el('k2').disabled = !(S.sys.length>=3 && S.sys.every(id=>S.herkomst[id]&&S.contract[id])); }

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
  const n=DIM[key].vragen.length; let pts=0, onbekend=0;
  for(let i=0;i<n;i++){ const v=S[key][i]; if(v==='x') onbekend++; else pts+=Number(v||0); }
  return { pct: Math.round(100*pts/(2*n)), onbekend };
}
function scores(){
  const nietEU=S.sys.filter(id=>S.herkomst[id]&&S.herkomst[id][0]==='0').length;
  const onb=S.sys.filter(id=>S.contract[id]==='0').length;
  const binnenJaar=S.sys.filter(id=>S.contract[id]==='1').length;
  const eigen=S.sys.filter(id=>S.herkomst[id]==='2').length;
  return { n:S.sys.length, nietEU, onb, binnenJaar, eigen, a:dekking('a'), b:dekking('b'), c:dekking('c') };
}
function resultaat(){
  const r=scores();
  const kloof=r.a.onbekend+r.b.onbekend+r.c.onbekend;
  /* kernzin */
  let getal, zin;
  if (kloof>=3){ getal=kloof+' van 10'; zin='vragen kon niemand in je organisatie beantwoorden. Dat is geen kennisprobleem maar een eigenaarschapsprobleem, en het is de eerste bevinding die een toezichthouder zal doen.'; }
  else if (r.nietEU>=Math.ceil(r.n/2) && r.onb>0){ getal=r.nietEU+' van '+r.n; zin='kritieke systemen draait bij een leverancier buiten de EU, en van '+r.onb+' daarvan weet je niet wanneer het contract afloopt. Dat is de combinatie waar drie wetten tegelijk op wijzen.'; }
  else if (S.c[2]!=='2'){ getal='Geen'; zin='bestuurlijk eigenaar met mandaat en budget voor de exit. Alles wat je verder geregeld hebt, hangt daardoor in de lucht.'; }
  else if (r.b.pct<50){ getal=r.b.pct+'%'; zin='dekking op je overstaprecht. De Data Act geeft je rechten die je nu niet kunt uitoefenen omdat je ze niet kent of nooit hebt getest.'; }
  else { getal=Math.round((r.a.pct+r.b.pct+r.c.pct)/3)+'%'; zin='gemiddelde dekking over de drie verplichtingen. De basis staat. Leg vast wat je hebt, want dat is je bewijs.'; }
  el('kern-getal').textContent=getal; el('kern-zin').textContent=zin;
  el('c-nieteu').textContent=r.nietEU+' van '+r.n; el('c-onbekend').textContent=r.onb;
  /* kaart */
  const k=el('kaart-uit'); k.innerHTML='';
  S.sys.forEach(id=>{ const naam=SYSTEMEN.find(s=>s[0]===id)[1]; const d=document.createElement('div'); d.className='tegel uit';
    d.style.cursor='default'; d.innerHTML='<span class="naam">'+naam+'</span><span class="stat"><i class="o'+S.herkomst[id][0]+'"></i><i class="c'+S.contract[id][0]+'"></i></span>'; k.appendChild(d); });
  /* dekking */
  const dk=el('dekking'); dk.innerHTML='';
  ['a','b','c'].forEach(key=>{ const d=r[key]; const div=document.createElement('div'); div.className='dek';
    div.innerHTML='<div class="lbl"><b>'+DIM[key].naam+' <span style="color:var(--ink-faint);font-weight:400">'+DIM[key].wet+'</span></b><span>'+d.pct+'%</span></div><div class="balk"><i></i></div>'
      +'<div class="klein">'+(d.onbekend? d.onbekend+' vraag'+(d.onbekend>1?'en':'')+' kon niemand beantwoorden.':(d.pct>=75?'Aantoonbaar. Leg het vast.':d.pct>=40?'Gedeeltelijk. Hier zit werk.':'Nauwelijks aantoonbaar. Dit hoort bovenaan je risicoanalyse.'))+'</div>';
    dk.appendChild(div); requestAnimationFrame(()=>requestAnimationFrame(()=>div.querySelector('.balk i').style.width=d.pct+'%')); });
  /* eerste stap */
  let kop, tekst;
  if (kloof>=2){ kop='Begin met een eigenaar.'; tekst='Zolang niemand de vragen kan beantwoorden, is elk plan een plan. Wijs een bestuurlijk eigenaar aan, geef die een middag met inkoop en IT, en laat de toets opnieuw doen. Dat is je eerste aantoonbare stap onder de Cbw.'; }
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
}
function codeer(r){ return btoa(JSON.stringify({rol:S.rol,org:S.org,n:r.n,ne:r.nietEU,ob:r.onb,a:r.a.pct,b:r.b.pct,c:r.c.pct,x:r.a.onbekend+r.b.onbekend+r.c.onbekend})).replace(/=+$/,''); }
function toonKloof(r){
  const p=new URLSearchParams(location.search).get('v'); if(!p) return;
  let o; try{ o=JSON.parse(atob(p)); }catch(e){ return; }
  if(!o||o.rol===S.rol) return;
  const naam=v=>({bestuur:'Bestuur',cio:'CIO',uitvoering:'Uitvoering',anders:'Collega'})[v]||v;
  const rijen=[['Ketenzorgplicht',o.a,r.a.pct],['Overstaprecht',o.b,r.b.pct],['Exitplan',o.c,r.c.pct],['Vragen die niemand kon beantwoorden',o.x,r.a.onbekend+r.b.onbekend+r.c.onbekend]];
  const k=el('kloof'); k.classList.remove('verborgen');
  k.innerHTML='<div style="font-weight:700"><span></span><span>'+naam(o.rol)+'</span><span>'+naam(S.rol)+'</span></div>'
    +rijen.map(([l,a,b])=>{ const d=Math.abs(a-b); const groot=(l.startsWith('Vragen')? d>=2 : d>=25);
      return '<div><span>'+l+'</span><span>'+a+(l.startsWith('Vragen')?'':'%')+'</span><span class="'+(groot?'verschil':'')+'">'+b+(l.startsWith('Vragen')?'':'%')+'</span></div>'; }).join('');
  el('duo-kop').textContent='Jullie mandaatkloof';
  el('duo-tekst').textContent='Twee mensen uit dezelfde organisatie, twee beelden. Waar het rood is, loopt het meer dan een kwart uiteen. Daar begint het gesprek.';
}
function kopieer(){ el('duo-link').select(); try{ document.execCommand('copy'); toast('Link gekopieerd'); }catch(e){ toast('Selecteer de link en kopieer hem'); } }
function stuurScores(r){
  /* alleen geaggregeerd, geen namen, geen vrije tekst */
  const body={org:S.org,rol:S.rol,n:r.n,niet_eu:r.nietEU,contract_onbekend:r.onb,a:r.a.pct,b:r.b.pct,c:r.c.pct,onbekend:r.a.onbekend+r.b.onbekend+r.c.onbekend};
  try{ fetch('/api/scan.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),keepalive:true}).catch(()=>{}); }catch(e){}
}
function bestel(){
  /* FASE 0: nog geen bestelling. Zet dit terug naar de bestelpagina zodra betalen aan mag:
     location.href='/bestel/#'+btoa(JSON.stringify(S)).replace(/=+$/,''); */
  toast('Het rapport is nog niet te bestellen. Deze toets is in test.');
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
