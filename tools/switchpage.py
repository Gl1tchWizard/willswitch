"""Bouw switch.html, de eigenlijke hoofdpagina.

Post-glitch editorial: de portal in een cirkelmasker met de kop eroverheen,
een dunne zwarte beloftenstrook, 62 stemmen met veel lucht, de wetgeving
als zwarte datasheet, een wit rapportblok met de prijs, de vragen, de
verhalen, het register van alle cases, de peiling, agenda en supporters.

Teksten en maten komen uit de eindspec van 26 september 2026 (notes/).
Wordt aangeroepen vanuit build.py.
"""
import datetime, html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://willswitch.nl"
TODAY = datetime.date.today()
NIEUW_DAGEN = 21

CBW_DATUM = datetime.date(2026, 8, 15)
DATAACT_DATUM = datetime.date(2027, 1, 12)

# Zet op True op de dag dat bestellen opent. Stuurt de besteltekst in het
# prijsblok, de laatste zin van FAQ 4 en de availability in het JSON-LD.
BESTEL_AAN = False

TITEL = "Digitale autonomie voor overheden: de uitstaptoets | Will Switch"
OMSCHRIJVING = ("Kun je nog weg bij je leveranciers? Gratis uitstaptoets voor overheden "
                "langs Cyberbeveiligingswet, Data Act en rijksbreed cloudbeleid. Plus praktijkcases.")
HERO_ALT = ("Astronaut kijkt uit over een Nederlands landschap, helm in de hand, "
            "met een lichtende ring aan de horizon")

BESTEL_TEKST = {
    False: ("Bestellen kan alleen vanuit je eigen toetsuitkomst, want daar wordt het rapport op "
            "geschreven. In deze fase vraag je het aan het eind van de toets per mail aan en krijg "
            "je persoonlijk antwoord van de initiatiefnemer."),
    True: "Bestellen kan aan het eind van de toets, vanuit je eigen uitkomst.",
}

FAQ_BESTELZIN = {
    False: "Bestellen gaat via de uitstaptoets; zolang bestellen nog dicht staat, meld je je daar per mail aan en hoor je wanneer het kan.",
    True: "Bestellen gaat via de uitstaptoets, vanuit je eigen uitkomst.",
}

FAQ = [
    ("Wat is de uitstaptoets?",
     "Een gratis toets van een kwartier, zonder registratie. Je kiest maximaal vijf kritieke systemen en "
     "beantwoordt tien vragen over ketenzorgplicht, overstaprecht en exitplan. Je krijgt direct een beeld "
     "van waar je staat en een eerste stap die daarbij past. Je antwoorden blijven in je browser."),
    ("Voor wie is de uitstaptoets bedoeld?",
     "Voor bestuurders, CIO's, CISO's, informatiemanagers en inkopers van gemeenten, provincies, "
     "waterschappen, het Rijk, zbo's, gemeenschappelijke regelingen en onderwijsinstellingen. Bestuur en "
     "uitvoering kunnen de toets los van elkaar doen en de uitkomsten naast elkaar leggen."),
    ("We hebben de BIO op orde, en het rijkscloudbeleid geldt niet voor gemeenten. Waarom dan dit?",
     "De BIO gaat over je eigen huis. De Cyberbeveiligingswet vraagt sinds 15 augustus 2026 ook iets over "
     "je keten: per leverancier wat er gebeurt bij contracteinde, faillissement of overname, en wie in het "
     "bestuur daarvoor tekent. Dat geldt voor gemeenten, provincies en waterschappen net zo goed als voor "
     "het Rijk. Het cloudbeleid komt daar nog achteraan. De staatssecretaris is daarover met de "
     "medeoverheden in gesprek."),
    ("Wat staat er in het uitstaprapport en wat kost het?",
     "Zeven delen: waar je staat, een uitstapprofiel per kritieke leverancier, een paragraaf voor je "
     "Cbw-risicoanalyse, een agendapunt voor het bestuur, exitclausules voor je volgende aanbesteding, de "
     "eerste negentig dagen en een vergelijking met andere gemeenten. Het rapport kost 750 euro exclusief "
     "btw (907,50 euro inclusief), eenmalig. Een hermeting na een jaar kost 250 euro. "
     + FAQ_BESTELZIN[BESTEL_AAN]),
    ("Is dit juridisch advies? Zijn we hiermee compliant?",
     "Nee, en nee. Het rapport is input voor je eigen risicoanalyse en geen oordeel over naleving van de "
     "Cyberbeveiligingswet, de Data Act of het cloudbeleid. Het benoemt wat je weet, wat je niet weet en "
     "wat je gaat doen. Dat is wat de toezichthouder wil zien. Het oordeel blijft bij jou en je jurist."),
    ("Waar blijven onze gegevens?",
     "Je antwoorden in de toets blijven in je browser. Alleen scores zonder naam gaan naar de server: "
     "organisatietype, rol, aantal systemen en de score per onderwerp. Geen namen, geen leveranciers. "
     "Leveranciersnamen die je voor het rapport opgeeft, staan alleen in jouw rapport en worden na twaalf "
     "maanden verwijderd. Zonder trackingcookies."),
    ("Wat is het verschil met het Volwassenheidsmodel Digitale Autonomie van het DACC?",
     "Het volwassenheidsmodel van het Digitale Autonomie Competentiecentrum beoordeelt een primair proces "
     "op strategie en governance, techniek en leveranciersmanagement. De uitstaptoets kijkt per kritieke "
     "leverancier of je eruit kunt, en legt dat naast de drie kaders met een datum. De twee vullen elkaar "
     "aan: het model zegt hoe volwassen je bent, de toets zegt waar je vastzit."),
]

REGISTER = [
    ("Waar je staat", "Je uitkomst in cijfers, en het verschil in beeld tussen bestuur en uitvoering als beide de toets deden."),
    ("Uitstapprofiel per kritieke leverancier", "Contracteinde, exporteerbare data, alternatief, bestuurlijk eigenaar, en wat de wet daar van je vraagt."),
    ("Paragraaf voor je Cbw-risicoanalyse", "Over te nemen in de structuur die de RDI hanteert: wat je weet, wat je niet weet en wat je gaat doen."),
    ("Agendapunt voor het bestuur", "Drie besluiten, past in een kwartier."),
    ("Exitclausules voor je volgende aanbesteding", "Vier bespreekpunten op basis van de Data Act en de modelclausules van de Europese Commissie, niet juridisch gevalideerd."),
    ("Je eerste negentig dagen", "Drie acties, elk met een eigenaar en een week."),
    ("Vergelijking met andere gemeenten", "Zodra er genoeg metingen zijn om die eerlijk te maken."),
]


# ---------- hulpfuncties ----------

def load_quotes():
    d = ROOT / "content" / "quotes"
    if not d.exists():
        return []
    out = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))]
    out.sort(key=lambda q: q.get("order", 999))
    return out


def is_nieuw(c):
    since = c.get("publish_on") or c.get("new_since")
    if not since:
        return False
    return (TODAY - datetime.date.fromisoformat(since)).days < NIEUW_DAGEN


def kicker_class(eyebrow):
    """Kleur van het vierkantje naar de soort: wetgeving, nieuws, praktijk, inzicht, beleid."""
    soort = (eyebrow or "").split("·")[0].split("/")[0].strip().lower()
    return "k-" + soort if soort in ("wetgeving", "nieuws", "praktijk", "inzicht", "beleid") else "k-overig"


def case_link(ids, cid, tekst, anders="uitleg volgt"):
    """Link naar een casepagina als die bestaat, anders een stille melding."""
    if cid in ids:
        return f'<a class="tekstlink op-inkt" href="/cases/{cid}/">{tekst}</a>'
    return f'<span class="volgt">{anders}</span>'


def overzicht_case(n, c):
    vlag = '<span class="vlag">nieuw</span>' if is_nieuw(c) else ""
    titel = c.get("card_title") or c["title"]
    return f'''      <a class="item" href="/cases/{c['id']}/">
        <span class="num">{n:02d}</span>
        <span class="kop"><span class="kicker {kicker_class(c.get("eyebrow"))}">{c.get("eyebrow", "")}</span>{vlag}
        <h3>{titel}</h3>
        <p>{c.get("card_body", "")}</p>
        <span class="meer">{c.get("cta", "Lees de case")}</span></span>
      </a>'''


def overzicht_quote(n, q):
    body = f'\n        <p>{q["body"]}</p>' if q.get("body") else ""
    attr = f'<span class="attr">{q["attr"]}</span>' if q.get("attr") else ""
    return f'''      <article class="item quote">
        <span class="num">{n:02d}</span>
        <span class="kop"><h3>{q["title"]}</h3>{body}
        <blockquote>{q["quote"]}{attr}</blockquote></span>
      </article>'''


def faq_html():
    out = []
    for vraag, antwoord in FAQ:
        out.append(f'''    <details>
      <summary><h3>{html.escape(vraag)}</h3></summary>
      <div><p>{html.escape(antwoord)}</p></div>
    </details>''')
    return "\n".join(out)


def register_html():
    return "\n".join(
        f'''      <li><span class="n">{i:02d}</span><span><b>{html.escape(k)}</b><span class="uitleg">{html.escape(u)}</span></span></li>'''
        for i, (k, u) in enumerate(REGISTER, 1))


def jsonld(cases):
    datums = [c.get("publish_on") or c.get("new_since") for c in cases]
    datums = [d for d in datums if d]
    gewijzigd = max(datums) if datums else TODAY.isoformat()
    beschikbaar = "https://schema.org/InStock" if BESTEL_AAN else "https://schema.org/PreOrder"
    org = {
        "@type": "Organization", "@id": f"{BASE}/#organization",
        "name": "Will Switch", "alternateName": "willswitch.nl", "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": f"{BASE}/wordmark.png", "width": 705, "height": 153},
        "image": f"{BASE}/og-image.jpg",
        "description": ("Praktijkonderzoek naar digitale autonomie in de Nederlandse publieke sector: wat "
                        "gemeenten, provincies, waterschappen, Rijk, zbo's en onderwijsinstellingen tegenhoudt "
                        "bij de overstap van Big Tech naar open alternatieven, en wat wel werkt."),
        "email": "info@willswitch.nl",
        "areaServed": {"@type": "Country", "name": "Nederland"},
        "knowsAbout": ["digitale autonomie", "digitale soevereiniteit", "Cyberbeveiligingswet", "Data Act",
                       "rijksbreed cloudbeleid", "vendor lock-in", "exitstrategie voor clouddiensten"],
        "founder": {"@type": "Person", "@id": f"{BASE}/#govert-schoof", "name": "Govert Schoof",
                    "jobTitle": "Initiatiefnemer", "sameAs": ["https://www.linkedin.com/in/govertschoof/"]},
        "funder": {"@type": "Organization", "name": "SIDN fonds", "url": "https://www.sidnfonds.nl/"},
        "sameAs": ["https://www.linkedin.com/in/govertschoof/", "https://github.com/Gl1tchWizard/willswitch"],
    }
    site = {"@type": "WebSite", "@id": f"{BASE}/#website", "url": f"{BASE}/", "name": "Will Switch",
            "description": "Praktijkonderzoek naar digitale autonomie in de publieke sector",
            "inLanguage": "nl-NL", "publisher": {"@id": f"{BASE}/#organization"}}
    page = {"@type": "WebPage", "@id": f"{BASE}/switch.html#webpage", "url": f"{BASE}/switch.html",
            "name": "Digitale autonomie voor overheden: de uitstaptoets", "description": OMSCHRIJVING,
            "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{BASE}/#organization"},
            "primaryImageOfPage": {"@type": "ImageObject", "url": f"{BASE}/switch-hero.webp",
                                   "width": 1672, "height": 941, "caption": HERO_ALT},
            "inLanguage": "nl-NL", "datePublished": "2026-09-25", "dateModified": gewijzigd,
            "mainEntity": {"@id": f"{BASE}/scan/#uitstaptoets"}}
    toets = {"@type": "WebApplication", "@id": f"{BASE}/scan/#uitstaptoets", "name": "Uitstaptoets",
             "url": f"{BASE}/scan/", "applicationCategory": "BusinessApplication", "operatingSystem": "Web",
             "isAccessibleForFree": True, "inLanguage": "nl-NL",
             "description": ("Gratis toets van een kwartier, zonder registratie. Toetst per kritieke leverancier "
                             "of een publieke organisatie nog weg kan, langs de Cyberbeveiligingswet, de Data Act "
                             "en het rijksbreed cloudbeleid."),
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
             "provider": {"@id": f"{BASE}/#organization"},
             "audience": {"@type": "Audience", "audienceType": ("Bestuurders, CIO's, CISO's, informatiemanagers en "
                          "inkopers van gemeenten, provincies, waterschappen, Rijk, zbo's en onderwijsinstellingen")}}

    def offer(naam, prijs):
        return {"@type": "Offer", "name": naam, "price": prijs, "priceCurrency": "EUR",
                "priceSpecification": {"@type": "UnitPriceSpecification", "price": prijs,
                                       "priceCurrency": "EUR", "valueAddedTaxIncluded": False},
                "availability": beschikbaar, "url": f"{BASE}/rapport/voorbeeld.html",
                "eligibleRegion": {"@type": "Country", "name": "Nederland"}}
    rapport = {"@type": "Service", "@id": f"{BASE}/rapport/voorbeeld.html#uitstaprapport",
               "name": "Uitstaprapport", "serviceType": "Uitstaprapport digitale autonomie",
               "url": f"{BASE}/rapport/voorbeeld.html",
               "description": ("Rapport na de gratis uitstaptoets, in zeven delen: waar je staat, uitstapprofiel per "
                               "kritieke leverancier, paragraaf voor de Cbw-risicoanalyse, agendapunt voor het "
                               "bestuur, exitclausules voor de volgende aanbesteding, de eerste negentig dagen en "
                               "een vergelijking met andere gemeenten."),
               "provider": {"@id": f"{BASE}/#organization"},
               "areaServed": {"@type": "Country", "name": "Nederland"},
               "audience": {"@type": "Audience", "audienceType": "Gemeenten, provincies, waterschappen, Rijk, zbo's en onderwijsinstellingen"},
               "offers": [offer("Uitstaprapport, eenmalig", "750.00"), offer("Hermeting na een jaar", "250.00")]}
    faq = {"@type": "FAQPage", "@id": f"{BASE}/switch.html#faq",
           "mainEntity": [{"@type": "Question", "name": v,
                           "acceptedAnswer": {"@type": "Answer", "text": a}} for v, a in FAQ]}
    graph = {"@context": "https://schema.org", "@graph": [org, site, page, toets, rapport, faq]}
    return json.dumps(graph, ensure_ascii=False, indent=2)


# ---------- opmaak ----------

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
h1, h2, h3, h4 { font-weight:700; }
h1, h2 { text-wrap:balance; }
img { max-width:100%; }
:focus-visible { outline:3px solid var(--knop); outline-offset:3px; }
.sr-only { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; }
.mono { font-family:var(--mono); font-size:13px; letter-spacing:.02em; line-height:1.6; color:var(--zacht); }
.op-inkt .mono, .mono.op-inkt { color:var(--op-inkt-2); }

/* knoppen en links */
.knop {
  display:inline-flex; align-items:center; justify-content:center; gap:.55em;
  min-height:44px; padding:0 20px; background:var(--knop); color:#fff; font-weight:700;
  text-decoration:none; font-size:16px; line-height:1.1; border-radius:0;
}
.knop:hover { background:var(--inkt); color:#fff; }
.knop.groot { min-height:56px; padding:0 28px; font-size:18px; }
.tekstlink {
  color:var(--link); font-weight:600; text-decoration:underline;
  text-underline-offset:4px; text-decoration-thickness:1.5px;
}
.tekstlink:hover { color:var(--inkt); }
.tekstlink.op-inkt { color:var(--papier); }
.tekstlink.op-inkt:hover { color:#fff; }
.volgt { font-family:var(--mono); font-size:13px; color:var(--op-inkt-2); }

/* header */
header.top { border-bottom:1px solid var(--inkt); background:var(--papier); }
header.top .w { display:flex; align-items:center; justify-content:space-between; min-height:84px; gap:20px; }
.merk { display:flex; align-items:center; gap:18px; text-decoration:none; }
.merk img { height:36px; width:auto; display:block; }
.merk span { font-size:13px; color:var(--zacht); line-height:1.35; padding-left:18px; border-left:1px solid var(--inkt); }
nav.hoofd { display:flex; align-items:center; gap:32px; font-size:16px; }
nav.hoofd a.l { text-decoration:none; padding:10px 0; }
nav.hoofd a.l:hover { text-decoration:underline; text-underline-offset:4px; }
nav.hoofd .kort { display:none; }

/* motief */
.ring { position:absolute; border-radius:50%; border:1px solid var(--oranje); pointer-events:none; }
.lijn { position:absolute; background:var(--oranje); }
.lijn.staand { transform-origin:top; transform:scaleY(0); }
.lijn.liggend { transform-origin:left; transform:scaleX(0); }
.is-in .lijn { transform:none; transition:transform .3s cubic-bezier(.2,.9,.2,1); }
.marge { opacity:0; }
.is-in .marge { opacity:1; transition:opacity .24s steps(3); }
html:not(.js) .lijn { transform:none; }
html:not(.js) .marge { opacity:1; }

/* hero: de portal in een cirkel, de kop eroverheen */
.hero { position:relative; overflow:hidden; min-height:760px; padding:56px 0 64px; background:var(--papier); }
.hero .w { position:relative; display:grid; grid-template-columns:repeat(12, 1fr); gap:24px; align-items:start; }
.staander { position:absolute; top:-57px; left:56%; width:96px; height:420px; background:var(--oranje); z-index:2; }
.hero-tekst { grid-column:1 / 10; grid-row:1; position:relative; z-index:3; }
.hero h1 .vraag {
  display:block; font-family:var(--mono); font-size:15px; font-weight:400;
  letter-spacing:.1em; text-transform:uppercase; line-height:1.6; margin-bottom:28px;
}
.hero h1 .groot {
  display:block; font-size:clamp(80px, 9vw, 120px); font-weight:800; text-transform:uppercase;
  line-height:.88; letter-spacing:-.035em; white-space:nowrap;
}
.hero .lead { margin-top:32px; font-size:24px; line-height:1.3; max-width:30ch; }
.hero .sub { margin-top:16px; font-size:18px; color:var(--zacht); max-width:44ch; line-height:1.5; }
.acties { display:flex; align-items:center; gap:20px; flex-wrap:wrap; }
.hero .acties { margin-top:36px; }
.micro { font-family:var(--mono); font-size:13px; letter-spacing:.02em; color:var(--zacht); max-width:42ch; line-height:1.5; }
.hero-link { margin-top:18px; }
.portal-wrap { grid-column:8 / 13; grid-row:1; position:relative; justify-self:start; width:640px; aspect-ratio:1; margin-top:180px; }
.portal {
  position:relative; z-index:1; width:100%; height:100%; border-radius:50%; overflow:hidden;
  background:#cfd4cf url('/switch-hero.webp') 13% 64% / auto 140% no-repeat;
}
.portal::before, .portal::after, .uitsteek::before, .uitsteek::after {
  content:""; position:absolute; inset:0; background:inherit; opacity:0; pointer-events:none;
}
.uitsteek::before, .uitsteek::after { background:var(--src) center / cover no-repeat; }
.portal::before, .uitsteek::before { clip-path:inset(34% 0 46% 0); transform:translateX(6px); }
.portal::after, .uitsteek::after { clip-path:inset(58% 0 22% 0); transform:translateX(-6px); }
.ring.orbit { width:720px; height:720px; left:-40px; top:-40px; opacity:.35; z-index:0; }

/* beloften: dunne zwarte strook */
.beloften { background:var(--inkt); color:var(--papier); padding:48px 0 52px; }
.beloften .w { display:grid; grid-template-columns:repeat(3, 1fr); gap:0; }
.beloften article { padding:0 32px; }
.beloften article:first-child { padding-left:0; }
.beloften article:last-child { padding-right:0; }
.beloften article + article { border-left:1px solid var(--lijn-inkt); }
.beloften .num { font-family:var(--mono); font-size:13px; color:var(--op-inkt-2); }
.beloften h3 { font-size:22px; line-height:1.15; margin-top:10px; }
.beloften p { font-size:16px; color:var(--op-inkt); max-width:34ch; margin-top:8px; }
.beloften .tekstlink { display:inline-block; margin-top:12px; }

/* stemmen: het getal en de lucht */
.stemmen { position:relative; overflow:hidden; padding:112px 0 96px; }
.stemmen .w { position:relative; display:grid; grid-template-columns:repeat(12, 1fr); gap:24px; }
.stemmen h2 { grid-column:1 / 9; display:grid; grid-template-columns:auto 1fr; gap:32px; align-items:end; }
.stemmen .getal {
  font-size:clamp(160px, 18vw, 260px); font-weight:800; letter-spacing:-.05em; line-height:.85;
  font-variant-numeric:tabular-nums; margin-left:-16px;
}
.stemmen .regels { font-size:56px; font-weight:800; text-transform:uppercase; letter-spacing:-.02em; line-height:.95; padding-bottom:12px; }
.citaat { grid-column:6 / 13; position:relative; margin-top:56px; padding-left:32px; }
.citaat p { font-size:36px; font-weight:700; line-height:1.15; max-width:22ch; }
.citaat .lijn { left:0; top:-80px; bottom:-80px; width:6px; }
.citaat p.bron { margin-top:20px; font-size:13px; font-weight:400; line-height:1.6; max-width:none; }
.citaat .bron .tekstlink { margin-left:12px; font-family:'Atkinson Hyperlegible Next', system-ui, sans-serif; font-size:15px; }
.ring.inkt { border-color:var(--inkt); }
.stemmen .ring { width:640px; height:640px; border-width:1.5px; opacity:.18; left:-260px; top:-200px; }

/* wetgeving: de zwarte datasheet */
.wetgeving { background:var(--inkt); color:var(--papier); padding:80px 0 0; position:relative; }
.wetgeving .rij0 { display:flex; justify-content:space-between; gap:24px; flex-wrap:wrap; font-family:var(--mono); font-size:12px; letter-spacing:.02em; color:var(--op-inkt-2); }
.wetgeving .rij1 { margin-top:24px; display:grid; grid-template-columns:7fr 5fr; gap:48px; align-items:end; }
.wetgeving h2 { font-size:52px; letter-spacing:-.02em; line-height:1.02; }
.wetgeving .intro { font-size:18px; color:rgba(240,237,230,.82); }
.wetgeving .rij2 { margin-top:56px; display:grid; grid-template-columns:4.4fr 7.6fr; gap:48px; align-items:start; }
.ladder { list-style:none; }
.ladder li { margin-bottom:36px; }
.ladder .d { display:block; font-size:64px; font-weight:800; letter-spacing:-.03em; line-height:.95; font-variant-numeric:tabular-nums; }
.ladder .l { display:block; font-family:var(--mono); font-size:13px; color:var(--op-inkt-2); margin-top:8px; }
.ladder .datum { position:relative; display:block; font-size:clamp(88px, 9.6vw, 124px); font-weight:800; letter-spacing:-.045em; line-height:.9; color:var(--oranje); font-variant-numeric:tabular-nums; }
.datum .t { position:relative; display:block; }
.datum .s { position:absolute; inset:0; opacity:0; }
.teller { font-family:var(--mono); font-size:13px; color:var(--op-inkt-2); line-height:1.7; }
.tabelwrap { position:relative; }
.tabelwrap .lijn.liggend { left:0; right:0; top:-2px; height:2px; }
table.datasheet { width:100%; table-layout:fixed; border-collapse:collapse; border-top:2px solid var(--papier); }
.datasheet .c-strook { width:12px; }
.datasheet .c-status { width:88px; }
.datasheet .c-kader { width:40%; }
.datasheet tr { border-bottom:1px solid var(--lijn-inkt); vertical-align:top; }
.datasheet td, .datasheet th { padding:24px 16px; text-align:left; }
.datasheet td.strook { width:12px; padding:0; }
.datasheet td.strook.oranje { background:var(--oranje); transform-origin:top; }
.datasheet td.strook.papier { background:var(--papier); }
.datasheet td.strook.omlijnd { box-shadow:inset 0 0 0 1.5px var(--papier); }
.datasheet td.status { font-family:var(--mono); font-size:12px; text-transform:uppercase; letter-spacing:.06em; color:var(--papier); white-space:nowrap; padding-left:12px; padding-right:8px; }
.datasheet th { padding-left:0; }
.datasheet th h3 { font-size:22px; line-height:1.1; overflow-wrap:anywhere; }
.datasheet th .sub { display:block; font-size:15px; font-weight:400; color:var(--op-inkt-2); margin-top:6px; }
.datasheet th .sinds { display:block; font-family:var(--mono); font-size:12px; font-weight:400; color:var(--op-inkt-2); line-height:1.6; margin-top:14px; }
.datasheet td.wat p { font-size:17px; color:rgba(240,237,230,.86); max-width:48ch; }
.datasheet .vragen { margin-top:18px; }
.datasheet .vragen b { display:block; font-size:15px; margin-bottom:8px; }
.datasheet .vragen ol { padding-left:20px; font-size:16px; line-height:1.45; color:rgba(240,237,230,.86); }
.datasheet .vragen li { margin-bottom:6px; }
.datasheet td.wat { padding-right:0; }
.datasheet td.wat .tekstlink { display:inline-block; margin-top:16px; font-size:16px; }
.balk { margin:64px calc(50% - 50vw) 0; background:var(--papier); color:var(--inkt); min-height:104px; }
.balk .w { display:flex; justify-content:space-between; align-items:center; gap:24px; padding-top:24px; padding-bottom:24px; }
.balk b { display:block; font-size:22px; }
.balk span { font-size:16px; color:var(--zacht); }

/* rapport: het aanbod, wit */
.rapport { background:var(--wit); border-top:3px solid var(--inkt); border-bottom:1px solid var(--inkt); padding:88px 0 96px; }
.rapport .w { display:grid; grid-template-columns:7fr 5fr; gap:64px; align-items:start; }
.kicker { font-family:var(--mono); font-size:13px; letter-spacing:.02em; color:var(--zacht); }
.rapport h2 { font-size:52px; letter-spacing:-.02em; line-height:1.02; max-width:16ch; margin-top:8px; }
.rapport .intro { font-size:20px; color:var(--zacht); max-width:48ch; margin-top:20px; }
.rapport .voorwie { font-size:17px; margin-top:14px; max-width:52ch; }
.rapport h3.klein { font-size:15px; margin-top:40px; }
.register { list-style:none; margin-top:12px; }
.register li { display:grid; grid-template-columns:56px 1fr; gap:16px; padding:16px 0; border-top:1px solid var(--inkt); }
.register li:last-child { border-bottom:1px solid var(--inkt); }
.register .n { font-family:var(--mono); font-size:14px; }
.register b { display:block; font-size:20px; }
.register .uitleg { display:block; font-size:15px; color:var(--zacht); margin-top:4px; }
.prijs { position:sticky; top:24px; background:var(--inkt); color:var(--papier); padding:40px 40px 36px; overflow:hidden; }
.prijs > * { position:relative; }
.prijs .ring { width:320px; height:320px; border-width:1.5px; opacity:.5; right:-160px; top:-160px; }
.prijs .mono { color:var(--op-inkt-2); font-size:12px; }
.bedrag { display:flex; align-items:baseline; gap:12px; margin-top:8px; }
.bedrag .getal { font-size:120px; font-weight:800; letter-spacing:-.04em; line-height:.85; font-variant-numeric:tabular-nums; }
.bedrag span:last-child { font-size:20px; font-weight:700; }
.prijs .btw { margin-top:10px; font-size:13px; color:var(--op-inkt); }
.prijs ul { list-style:none; margin-top:24px; }
.prijs ul li { font-size:16px; padding:10px 0; border-top:1px solid var(--lijn-inkt); }
.prijs h4 { font-size:15px; margin-top:24px; }
.prijs ol { font-size:16px; line-height:1.45; padding-left:20px; margin-top:8px; }
.prijs .knop { width:100%; margin-top:28px; }
.prijs .tekstlink { display:block; margin-top:14px; }
.prijs .bestel { font-size:14px; color:var(--op-inkt); margin-top:20px; line-height:1.5; }
.afzender { margin-top:24px; border-top:2px solid var(--inkt); padding-top:20px; }
.afzender .naam { font-size:22px; font-weight:700; }
.afzender p { font-size:16px; color:var(--zacht); }
.afzender .fonds { display:inline-flex; align-items:center; gap:12px; margin-top:16px; text-decoration:none; font-size:14px; color:var(--vaag); }
.afzender .fonds img, footer.site .fonds img { height:28px; width:auto; display:block; }

/* vragen */
.faq { padding:80px 0 72px; }
.faq .w { display:grid; grid-template-columns:4fr 8fr; gap:48px; align-items:start; }
.faq h2 { font-size:40px; line-height:1.08; letter-spacing:-.02em; }
.faq .hulp { font-size:16px; color:var(--zacht); margin-top:16px; }
.faq details { border-top:1px solid var(--inkt); }
.faq details:last-child { border-bottom:1px solid var(--inkt); }
.faq summary { list-style:none; cursor:pointer; padding:18px 40px 18px 0; position:relative; min-height:44px; }
.faq summary::-webkit-details-marker { display:none; }
.faq summary h3 { font-size:19px; line-height:1.3; display:inline; }
.faq summary::after { content:"+"; position:absolute; right:0; top:14px; font-family:var(--mono); font-size:22px; }
.faq details[open] summary::after { content:"\\2212"; }
.faq details div p { font-size:16px; color:var(--zacht); line-height:1.55; max-width:62ch; padding:0 0 20px; }

/* verhalen */
.verhalen { position:relative; overflow:hidden; padding:96px 0 72px; }
.verhalen .w { position:relative; display:grid; grid-template-columns:5fr 7fr; gap:48px; align-items:start; }
.verhalen h2 { font-size:52px; letter-spacing:-.02em; line-height:1.02; margin-top:8px; }
.verhalen .intro { font-size:18px; color:var(--zacht); max-width:36ch; margin-top:16px; }
.verhalen .intro + .tekstlink { display:inline-block; margin-top:14px; }
.verhalen .ring { width:160px; height:160px; opacity:.4; left:-60px; top:40px; }
.klein-verhalen { margin-top:48px; }
.klein-verhalen article { display:grid; grid-template-columns:160px 1fr; gap:20px; border-top:1px solid var(--inkt); padding:20px 0; }
.tegel { aspect-ratio:4/3; display:flex; flex-direction:column; justify-content:center; padding:14px; }
.tegel.warm { background:var(--warm); }
.tegel.inkt { background:var(--inkt); color:var(--papier); }
.tegel b { font-size:40px; font-weight:800; line-height:1; letter-spacing:-.03em; }
.tegel.inkt b { font-size:26px; }
.tegel .mono { font-size:11px; margin-top:6px; color:inherit; opacity:.75; }
.klein-verhalen h3 { font-size:22px; line-height:1.15; margin-top:4px; }
.klein-verhalen p { font-size:16px; color:var(--zacht); margin-top:6px; }
.klein-verhalen .tekstlink { display:inline-block; margin-top:8px; }
figure.uitsteek { position:relative; margin:0 calc(50% - 50vw) 0 0; }
figure.uitsteek img { width:100%; aspect-ratio:16/10; object-fit:cover; display:block; }
.opschrift { position:absolute; left:0; bottom:0; background:var(--inkt); color:var(--papier); padding:16px 20px; font-family:var(--mono); font-size:12px; line-height:1.6; }
.dsg-tekst { margin-top:24px; }
.dsg-tekst h3 { font-size:30px; line-height:1.1; margin-top:6px; }
.dsg-tekst p { font-size:17px; color:var(--zacht); max-width:60ch; margin-top:8px; }
.dsg-tekst .tekstlink { display:inline-block; margin-top:10px; }

/* overzicht: register */
.overzicht { padding:80px 0 64px; }
.overzicht .kopregel { border-top:2px solid var(--inkt); padding-top:24px; display:grid; grid-template-columns:1fr auto; gap:40px; align-items:end; }
.overzicht h2 { font-size:40px; line-height:1.08; letter-spacing:-.02em; }
.register-lijst { margin-top:24px; display:grid; grid-template-columns:1fr 1fr; column-gap:48px; align-items:start; }
.item { display:grid; grid-template-columns:48px 1fr; gap:16px; padding:20px 0; border-top:1px solid var(--inkt); text-decoration:none; color:inherit; }
.item .num { font-family:var(--mono); font-size:14px; color:var(--link); }
.item .kop { display:block; }
.item .kicker { font-family:inherit; font-size:12px; font-weight:700; color:var(--inkt); letter-spacing:0; }
.item .kicker::before { content:""; display:inline-block; width:8px; height:8px; margin-right:8px; background:var(--inkt); vertical-align:1px; }
.item .k-nieuws::before { background:#2F4F6F; }
.item .k-praktijk::before { background:var(--knop); }
.item .k-inzicht::before { background:transparent; box-shadow:inset 0 0 0 1.5px var(--inkt); }
.item .vlag { font-family:var(--mono); font-size:11px; color:#fff; background:var(--knop); padding:2px 6px; margin-left:8px; }
.item h3 { font-size:20px; line-height:1.2; margin-top:6px; }
.item p { font-size:15px; color:var(--zacht); margin-top:6px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.item .meer { display:inline-block; font-size:15px; font-weight:600; color:var(--link); text-decoration:underline; text-underline-offset:4px; margin-top:8px; }
a.item:hover h3 { text-decoration:underline; text-underline-offset:4px; }
.item.quote { background:var(--warm); padding:20px 16px; }
.item.quote h3 { font-size:16px; }
.item.quote p { font-size:14px; -webkit-line-clamp:3; }
.item.quote blockquote { font-size:18px; font-weight:600; line-height:1.35; margin-top:8px; }
.item.quote blockquote::before { content:"\\201C"; display:block; font-size:44px; line-height:.5; margin:10px 0 6px; }
.item.quote .attr { display:block; font-family:var(--mono); font-size:12px; font-weight:400; color:var(--zacht); margin-top:8px; }

/* peiling, op inkt */
.movement { position:relative; overflow:hidden; background:var(--inkt); color:var(--papier); padding:80px 0 88px; }
.movement .w { position:relative; }
.movement h2 { font-size:48px; line-height:1.08; letter-spacing:-.02em; }
.movement h2::before { content:""; display:inline-block; width:18px; height:18px; border:3px solid var(--oranje); border-radius:50%; margin-right:16px; vertical-align:middle; }
.movement .sub { font-size:17px; color:var(--op-inkt); max-width:52ch; margin-top:10px; }
.movement .sub strong { color:var(--papier); }
.movement .confirm { min-height:1.5em; font-size:16px; margin:16px 0; }
.movement .confirm:empty { display:none; }
.movement-grid { display:grid; grid-template-columns:repeat(5, 1fr); gap:0; margin-top:24px; }
.movement-btn {
  min-height:96px; padding:20px; display:flex; flex-direction:column; justify-content:space-between; align-items:flex-start;
  background:transparent; border:1px solid rgba(240,237,230,.35); margin-left:-1px; border-radius:0;
  font:inherit; font-size:16px; color:var(--papier); cursor:pointer; text-align:left;
  transition:transform .25s ease, background .2s ease;
}
.movement-btn:first-child { margin-left:0; }
.movement-btn:hover { background:rgba(240,237,230,.06); }
.movement-btn .count { font-size:40px; font-weight:800; font-variant-numeric:tabular-nums; color:var(--oranje); line-height:1; }
.movement-btn.selected { background:var(--knop); border-color:var(--knop); color:#fff; }
.movement-btn.selected .count { color:#fff; }
.movement-btn.pulse { transform:scale(1.03); }
.ring.orbit-open { width:620px; height:620px; border-width:1.5px; opacity:.6; right:-200px; top:-300px; }
.ring.orbit-open::before { content:""; position:absolute; top:-4px; left:50%; width:24px; height:8px; background:var(--inkt); }

/* agenda en supporters */
.onder { display:grid; grid-template-columns:1.2fr 1fr; gap:64px; padding-top:72px; padding-bottom:56px; }
.blok h2 { font-size:26px; line-height:1.1; }
.blok .sub { font-size:16px; color:var(--zacht); margin:6px 0 18px; }
.agenda ul { list-style:none; }
.agenda li { display:grid; grid-template-columns:130px 1fr; gap:20px; padding:14px 0; border-top:1px solid var(--inkt); }
.agenda .when { font-family:var(--mono); font-size:14px; }
.agenda .what a { font-weight:600; }
.agenda .where { display:block; font-size:15px; color:var(--vaag); margin-top:2px; }
.credits ul { list-style:none; }
.credits li { padding:12px 0; border-top:1px solid var(--inkt); }
.credits .name { font-weight:700; display:block; }
.credits .context { font-size:15px; color:var(--zacht); }

/* slot en voet */
.slot { border-top:2px solid var(--inkt); padding:64px 0 72px; }
.slot .w { display:grid; grid-template-columns:8fr 4fr; gap:48px; align-items:center; }
.slotzin { font-size:32px; font-weight:700; line-height:1.2; letter-spacing:-.015em; max-width:26ch; }
.slot .micro { display:block; margin-top:12px; }
footer.site { border-top:3px solid var(--inkt); padding:28px 0 48px; font-size:14px; color:var(--vaag); }
footer.site .w { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px 24px; }
footer.site .fonds { display:inline-flex; align-items:center; gap:12px; text-decoration:none; }

/* scrollbeweging zonder JS */
@supports (animation-timeline: view()) {
  .ring.drijft { animation:drijf linear both; animation-timeline:view(); animation-range:entry 0% exit 100%; }
  @keyframes drijf { from { translate:0 60px; } to { translate:0 -60px; } }
  .ring.orbit-open { animation:draai linear both; animation-timeline:view(); }
  @keyframes draai { from { rotate:-8deg; } to { rotate:8deg; } }
}

/* de kraak: 200 ms, een keer per element */
@keyframes kraak-tekst { 0%, 100% { transform:none; } 35% { transform:translateX(-3px); } 70% { transform:translateX(3px); } }
@keyframes flits { 0% { opacity:0; } 40% { opacity:1; } 100% { opacity:0; } }
.kraak .k-tekst { animation:kraak-tekst 200ms steps(3); }
.kraak .portal::before, .kraak .portal::after, .kraak.uitsteek::before, .kraak.uitsteek::after { animation:flits 180ms steps(2); }
.kraak .datum .s:first-of-type { clip-path:inset(0 0 66% 0); transform:translateX(5px); animation:flits 180ms steps(2); }
.kraak .datum .s:last-of-type { clip-path:inset(66% 0 0 0); transform:translateX(-3px); animation:flits 180ms steps(2); }
.tabelwrap td.strook.oranje { transform:scaleY(0); }
.tabelwrap.is-in td.strook.oranje { transform:none; transition:transform .3s cubic-bezier(.2,.9,.2,1); }
html:not(.js) .tabelwrap td.strook.oranje { transform:none; }
@media (hover:hover) {
  .portal:hover::before, .portal:hover::after, .uitsteek:hover::before, .uitsteek:hover::after { animation:flits 180ms steps(2); }
}

/* tussenmaat */
@media (min-width:821px) and (max-width:1000px) {
  .register-lijst { grid-template-columns:1fr; }
  .portal-wrap { width:520px; }
  .ring.orbit { width:600px; height:600px; }
}
@media (max-height:800px) { .prijs { position:static; } }

/* mobiel */
@media (max-width:820px) {
  .w { padding:0 16px; }
  header.top .w { min-height:64px; }
  .merk img { height:30px; }
  .merk span { display:none; }
  nav.hoofd { gap:16px; font-size:15px; }
  nav.hoofd .lang { display:none; }
  nav.hoofd .kort { display:inline; }
  .hero { min-height:0; padding:32px 0 48px; }
  .hero .w { display:block; }
  .staander { top:-33px; left:auto; right:16px; width:56px; height:140px; }
  .hero h1 .vraag { font-size:13px; }
  .hero h1 .groot { font-size:clamp(40px, 13vw, 64px); letter-spacing:-.04em; line-height:.9; white-space:normal; overflow-wrap:anywhere; }
  .portal-wrap { width:88vw; margin-left:24vw; margin-top:-20px; }
  .ring.orbit { display:none; }
  .hero .lead { font-size:20px; margin-top:24px; }
  .hero .sub { font-size:17px; }
  .hero .acties { margin-top:24px; }
  .hero .knop.groot, .prijs .knop, .balk .knop, .slot .knop { width:100%; min-height:52px; }
  .beloften { padding:32px 0 36px; }
  .beloften .w { grid-template-columns:1fr; }
  .beloften article { padding:20px 0; }
  .beloften article + article { border-left:0; border-top:1px solid var(--lijn-inkt); }
  .stemmen { padding:72px 0 64px; }
  .stemmen .w { display:block; }
  .stemmen h2 { grid-template-columns:1fr; gap:8px; }
  .stemmen .getal { font-size:120px; margin-left:-6px; }
  .stemmen .regels { font-size:34px; padding-bottom:0; }
  .citaat { margin-top:40px; padding-left:20px; }
  .citaat p { font-size:26px; }
  .citaat .lijn { width:4px; top:-40px; bottom:-40px; }
  .stemmen .ring { width:360px; height:360px; left:-200px; top:-120px; }
  .wetgeving { padding:48px 0 0; }
  .wetgeving .rij1, .wetgeving .rij2 { grid-template-columns:1fr; gap:24px; }
  .wetgeving h2 { font-size:32px; }
  .ladder .d { font-size:44px; }
  .ladder .datum { font-size:clamp(64px, 22vw, 88px); }
  .datasheet thead, .datasheet colgroup { display:none; }
  table.datasheet, .datasheet tbody, .datasheet tr, .datasheet th, .datasheet td { display:block; width:auto; }
  .datasheet tr { border-top:1px solid var(--lijn-inkt); border-bottom:0; padding:20px 0 20px 16px; position:relative; }
  .datasheet td.strook { position:absolute; left:0; top:0; bottom:0; width:6px; }
  .datasheet td, .datasheet th { padding:0; }
  .datasheet td.status { padding:0; width:auto; display:block; }
  .datasheet th { margin-top:10px; }
  .datasheet th h3 { font-size:24px; }
  .datasheet td.wat { margin-top:12px; }
  .datasheet td.wat p { font-size:16px; }
  .datasheet .vragen ol { font-size:15px; }
  .balk { margin-top:40px; }
  .balk .w { flex-direction:column; align-items:stretch; }
  .rapport { padding:56px 0 64px; }
  .rapport .w { grid-template-columns:1fr; gap:40px; }
  .rapport h2 { font-size:32px; }
  .register li { grid-template-columns:44px 1fr; }
  .register b { font-size:18px; }
  .prijs { position:static; padding:28px 20px; }
  .bedrag .getal { font-size:88px; }
  .faq { padding:56px 0 48px; }
  .faq .w { grid-template-columns:1fr; gap:24px; }
  .faq h2 { font-size:30px; }
  .faq summary h3 { font-size:17px; }
  .verhalen { padding:56px 0 48px; }
  .verhalen .w { grid-template-columns:1fr; gap:32px; }
  .verhalen h2 { font-size:32px; }
  .verhalen .ring { display:none; }
  figure.uitsteek { margin:0 -16px; }
  figure.uitsteek img { aspect-ratio:4/3; }
  .klein-verhalen article { grid-template-columns:1fr; }
  .tegel { aspect-ratio:auto; height:120px; }
  .overzicht { padding:56px 0 40px; }
  .overzicht .kopregel { grid-template-columns:1fr; gap:8px; }
  .overzicht h2 { font-size:30px; }
  .register-lijst { grid-template-columns:1fr; }
  .item { grid-template-columns:40px 1fr; }
  .item h3 { font-size:18px; }
  .movement { padding:56px 0 64px; }
  .movement h2 { font-size:32px; }
  .movement-grid { grid-template-columns:1fr; }
  .movement-btn { min-height:64px; flex-direction:row; align-items:center; margin-left:0; margin-top:-1px; }
  .movement-btn .count { font-size:28px; }
  .ring.orbit-open { width:480px; height:480px; right:-300px; top:-320px; }
  .onder { grid-template-columns:1fr; gap:8px; padding:48px 0 32px; }
  .agenda li { grid-template-columns:1fr; gap:4px; }
  .slot { padding:48px 0 56px; }
  .slot .w { grid-template-columns:1fr; gap:24px; }
  .slotzin { font-size:24px; }
  footer.site .w { flex-direction:column; align-items:flex-start; gap:12px; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior:auto; }
  .kraak .k-tekst, .kraak .datum .s, .portal::before, .portal::after, .uitsteek::before, .uitsteek::after { animation:none !important; }
  .portal::before, .portal::after, .uitsteek::before, .uitsteek::after { display:none; }
  .lijn { transform:none; transition:none; }
  .marge { opacity:1; transition:none; }
  .tabelwrap td.strook.oranje { transform:none; transition:none; }
  .ring.drijft, .ring.orbit-open { animation:none; }
  .movement-btn { transition:none; }
  .movement-btn.pulse { transform:none; }
}
"""


# ---------- vaste onderdelen ----------

KRAAK_SCRIPT = """
  <script>
    /* De kraak: vijf plekken kraken een keer, 200 ms, zodra ze in beeld komen. */
    (function () {
      var root = document.documentElement;
      root.classList.add('js');
      var els = document.querySelectorAll('[data-kraak]');
      var stil = matchMedia('(prefers-reduced-motion: reduce)').matches;
      function aan(el) { el.classList.add('is-in'); }
      if (stil || !('IntersectionObserver' in window)) { els.forEach(aan); return; }
      function kraak(el) {
        if (el.classList.contains('kraak') || el.classList.contains('is-in')) return;
        el.classList.add('kraak');
        setTimeout(function () { el.classList.remove('kraak'); aan(el); }, 200);
      }
      var klaar = document.fonts ? document.fonts.ready : Promise.resolve();
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          io.unobserve(e.target);
          if (e.target.classList.contains('hero')) { klaar.then(function () { kraak(e.target); }); }
          else { kraak(e.target); }
        });
      }, { threshold: 0.2 });
      els.forEach(function (el) { io.observe(el); });
      /* Vangnet: wat na twee seconden nog niet in beeld kwam, staat gewoon aan. */
      setTimeout(function () { els.forEach(function (el) { if (!el.classList.contains('is-in')) { io.unobserve(el); aan(el); } }); }, 2000);
    })();
  </script>
"""

MOVEMENT_SCRIPT = """
  <script>
    // ===== Movement signal section =====
    (function () {
      const API_BASE = 'https://abacus.jasoncameron.dev';
      const NAMESPACE = 'willswitch.nl';
      const STORAGE_KEY = 'willswitch_movement_phase';

      const PHASES = {
        verkennen: 'We verkennen',
        praten:    'We praten erover',
        pilot:     'We draaien een pilot',
        overstap:  'We stappen over',
        verder:    'We zijn al verder'
      };

      const section   = document.getElementById('movement');
      if (!section) return;
      const confirmEl = document.getElementById('movement-confirm');
      const buttons   = section.querySelectorAll('.movement-btn');

      function countEl(phase) {
        return section.querySelector(`[data-phase="${phase}"] [data-count]`);
      }
      function currentCount(phase) {
        const n = parseInt(countEl(phase).textContent, 10);
        return isNaN(n) ? 0 : n;
      }
      function setCount(phase, value) {
        countEl(phase).textContent = value;
      }

      // Friendly confirmation: number + reassurance, not official-data tone
      function confirmationText(phase) {
        const label = PHASES[phase];
        const n = currentCount(phase);
        if (n <= 1) {
          return `Genoteerd: <strong>"${label}"</strong>. Het eerste signaal in deze fase. Anderen volgen vast.`;
        }
        return `Dit patroon zien we vaker. Inmiddels <strong>${n} signalen</strong> in <strong>"${label}"</strong>. Je bent niet de enige.`;
      }

      function highlight(phase, animate) {
        buttons.forEach((b) => b.classList.remove('selected'));
        const btn = section.querySelector(`[data-phase="${phase}"]`);
        if (!btn) return;
        btn.classList.add('selected');
        if (animate) {
          btn.classList.add('pulse');
          setTimeout(() => btn.classList.remove('pulse'), 500);
        }
        confirmEl.innerHTML = confirmationText(phase);
        section.classList.add('has-clicked');
      }

      // Load counts from backend on page load
      async function loadCounts() {
        await Promise.all(
          Object.keys(PHASES).map(async (phase) => {
            try {
              const r = await fetch(`${API_BASE}/get/${NAMESPACE}/beweeg-${phase}`);
              if (r.ok) {
                const data = await r.json();
                setCount(phase, data.value || 0);
              } else {
                setCount(phase, 0);
              }
            } catch (e) {
              setCount(phase, 0);
            }
          })
        );
      }

      async function hit(phase) {
        try {
          const r = await fetch(`${API_BASE}/hit/${NAMESPACE}/beweeg-${phase}`);
          if (r.ok) {
            const data = await r.json();
            setCount(phase, data.value);
          } else {
            setCount(phase, currentCount(phase) + 1);
          }
        } catch (e) {
          setCount(phase, currentCount(phase) + 1);
        }
      }

      // Abacus exposes increment but not decrement on the free tier.
      // When a visitor switches choice we correct the display locally so the
      // numbers stay believable, without pretending to be exact research data.
      function decrementLocal(phase) {
        setCount(phase, Math.max(0, currentCount(phase) - 1));
      }

      async function vote(phase) {
        const previous = localStorage.getItem(STORAGE_KEY);

        if (previous === phase) {
          // same choice clicked again: never double-counts
          highlight(phase, false);
          return;
        }

        if (previous && PHASES[previous]) {
          // switching choice: visually move the signal across
          decrementLocal(previous);
        }

        await hit(phase);
        localStorage.setItem(STORAGE_KEY, phase);
        highlight(phase, true);
      }

      buttons.forEach((btn) => {
        btn.addEventListener('click', () => {
          const phase = btn.dataset.phase;
          if (phase) vote(phase);
        });
      });

      // Initialize: load counts, then restore any prior choice
      loadCounts().then(() => {
        const previous = localStorage.getItem(STORAGE_KEY);
        if (previous && PHASES[previous]) {
          highlight(previous, false);
        }
      });
    })();
  </script>
"""

PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titel}</title>
  <meta name="description" content="{omschrijving}">
  <link rel="canonical" href="{base}/switch.html">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="nl_NL">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="Digitale autonomie voor overheden: de uitstaptoets">
  <meta property="og:description" content="{omschrijving}">
  <meta property="og:image" content="{base}/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{hero_alt}">
  <meta property="og:url" content="{base}/switch.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Digitale autonomie voor overheden: de uitstaptoets">
  <meta name="twitter:description" content="{omschrijving}">
  <meta name="twitter:image" content="{base}/og-image.jpg">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180.png">
  <link rel="preload" href="/fonts/AtkinsonNext.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/switch-hero.webp" as="image" fetchpriority="high">
  <script type="application/ld+json">
{jsonld}
  </script>
  <style>{css}  </style>
</head>
<body>

<header class="top"><div class="w">
  <a class="merk" href="/switch.html"><img src="/wordmark.png" alt="Will Switch" width="705" height="153"><span>Praktijkonderzoek naar<br>digitale autonomie</span></a>
  <nav class="hoofd" aria-label="Hoofdnavigatie"><a class="l" href="#verhalen">Praktijk</a><a class="l" href="#rapport">Rapport</a><a class="knop" href="/scan/"><span class="lang">Uitstaptoets</span><span class="kort">Toets</span> &rarr;</a></nav>
</div></header>

<section class="hero" data-kraak><div class="w">
  <div class="staander" aria-hidden="true"></div>
  <div class="hero-tekst">
    <h1><span class="vraag">Kun je nog weg<br>bij je<br>leveranciers?</span><span class="groot k-tekst">Digitale<br>autonomie.</span></h1>
    <p class="lead">Niet alles hoeft anders. Maar je moet wel kunnen kiezen.</p>
    <p class="sub">Sinds 15 augustus 2026 moet je bestuur die vraag per leverancier kunnen beantwoorden. De gratis uitstaptoets laat in een kwartier zien waar je staat. Het uitstaprapport zegt wat je daarna doet.</p>
    <div class="acties">
      <a class="knop groot" href="/scan/">Doe de gratis uitstaptoets &rarr;</a>
      <span class="micro">een kwartier, geen registratie, je antwoorden blijven in je browser</span>
    </div>
    <p class="hero-link"><a class="tekstlink" href="#verhalen">Bekijk de praktijkverhalen</a></p>
  </div>
  <div class="portal-wrap">
    <div class="ring orbit" aria-hidden="true"></div>
    <div class="portal" role="img" aria-label="{hero_alt}"></div>
  </div>
</div></section>

<section class="beloften">
  <h2 class="sr-only">Wat je hier vindt</h2>
  <div class="w">
    <article><span class="num">01</span><h3>Binnen een kwartier weet je waar je staat</h3><p>Per kritiek systeem weet je wie levert, wanneer het contract afloopt en of iemand weet wat er met je data gebeurt als de leverancier morgen stopt.</p><a class="tekstlink op-inkt" href="/scan/">Doe de uitstaptoets</a></article>
    <article><span class="num">02</span><h3>Je bestuur in positie</h3><p>De Cyberbeveiligingswet maakt het bestuur verantwoordelijk voor de keten. Je krijgt de paragraaf voor de risicoanalyse en het agendapunt waarmee het bestuur dat aantoonbaar oppakt.</p><a class="tekstlink op-inkt" href="#wetgeving">Lees wat de wet vraagt</a></article>
    <article><span class="num">03</span><h3>E&eacute;n eerste stap, geen migratie</h3><p>Niet alles hoeft anders, maar je moet wel kunnen kiezen. Het rapport wijst de dienst aan waar je begint en de drie acties voor de eerste negentig dagen.</p><a class="tekstlink op-inkt" href="#rapport">Bekijk het uitstaprapport</a></article>
  </div>
</section>

<section class="stemmen" data-kraak>
  <div class="ring inkt drijft" aria-hidden="true"></div>
  <div class="w">
    <h2><span class="getal k-tekst">62</span><span class="regels">Stemmen.<br>1 patroon.</span></h2>
    <blockquote class="citaat">
      <div class="lijn staand" aria-hidden="true"></div>
      <p>Het ligt zelden aan de techniek. Het ligt aan wie zich eigenaar voelt.</p>
      <p class="bron mono marge">uit 62 stemmen op FOSS4G NL 2026, Groningen <a class="tekstlink" href="/talk/">Bekijk het verhaal</a></p>
    </blockquote>
  </div>
</section>

<section class="wetgeving" id="wetgeving"><div class="w">
  <div class="rij0"><span>actuele wetgeving, stand {stand}</span><span>bestuur aanspreekbaar sinds 15.08.2026</span></div>
  <div class="rij1">
    <h2>Drie kaders stellen dezelfde vraag: kun je eruit?</h2>
    <p class="intro">Sinds 15 augustus 2026 is het bestuur aanspreekbaar op de leveranciersketen. Wie niet kan aantonen wat er gebeurt bij contracteinde of uitval, loopt bestuurlijk risico.</p>
  </div>
  <div class="rij2">
    <div>
      <ol class="ladder">
        <li><span class="d">15.08.26</span><span class="l">cyberbeveiligingswet, van kracht</span></li>
        <li><span class="datum" data-kraak><span class="t k-tekst">12.01.27</span><span class="s" aria-hidden="true">12.01.27</span><span class="s" aria-hidden="true">12.01.27</span></span><span class="l">data act, overstappen binnen 30 dagen</span></li>
        <li><span class="d">medio 2030</span><span class="l">rijksbreed cloudbeleid, einde overgangstermijn</span></li>
      </ol>
      <p class="teller">{teller_cbw}<br>{teller_dataact}</p>
    </div>
    <div class="tabelwrap" data-kraak>
      <div class="lijn liggend" aria-hidden="true"></div>
      <table class="datasheet" role="table">
        <colgroup><col class="c-strook"><col class="c-status"><col class="c-kader"><col class="c-wat"></colgroup>
        <thead class="sr-only"><tr><th></th><th>status</th><th>kader, sinds en voor wie</th><th>wat je moet kunnen aantonen</th></tr></thead>
        <tbody>
          <tr role="row">
            <td class="strook oranje" role="cell"></td>
            <td class="status" role="cell">nu</td>
            <th scope="row" role="rowheader"><h3>Cyberbeveiligingswet: ketenzorgplicht per leverancier</h3><span class="sub">Van kracht sinds 15 augustus 2026</span><span class="sinds">wet, voor Rijk, zbo's, gemeenten, provincies en waterschappen<br>de zorgplicht geldt al</span></th>
            <td class="wat" role="cell">
              <p>Per leverancier moet je kunnen aantonen wat er gebeurt bij contracteinde, faillissement of overname. Het bestuur is eindverantwoordelijk, en de toezichthouder kan ernaar vragen.</p>
              <div class="vragen"><b>Drie vragen die je vandaag zou moeten kunnen beantwoorden</b>
                <ol>
                  <li>Van welke leveranciers hangt je dienstverlening af, en wanneer lopen die contracten af?</li>
                  <li>Wat gebeurt er met je data als zo'n leverancier stopt?</li>
                  <li>Wie in het bestuur is daarvoor verantwoordelijk, en is dat formeel vastgesteld?</li>
                </ol>
              </div>
              {link_cbw}
            </td>
          </tr>
          <tr role="row">
            <td class="strook papier" role="cell"></td>
            <td class="status" role="cell">12.01.27</td>
            <th scope="row" role="rowheader"><h3>Data Act: overstaprecht zonder overstapkosten</h3><span class="sub">Vanaf 12 januari 2027</span><span class="sinds">eu-verordening, voor iedere afnemer van clouddiensten<br>ook voor lopende contracten</span></th>
            <td class="wat" role="cell"><p>Het recht om binnen dertig dagen over te stappen, ook naar eigen infrastructuur. Vanaf die datum vervallen overstapkosten.</p>{link_dataact}</td>
          </tr>
          <tr role="row">
            <td class="strook omlijnd" role="cell"></td>
            <td class="status" role="cell">2030</td>
            <th scope="row" role="rowheader"><h3>Rijksbreed cloudbeleid: een exitplan per clouddienst</h3><span class="sub">Overgangstermijn tot medio 2030</span><span class="sinds">beleid, voor rijksorganisaties, met medeoverheden in overleg<br>einde overgangstermijn</span></th>
            <td class="wat" role="cell"><p>Een exitplan per clouddienst, ook voor het scenario dat een dienst plotseling wegvalt. Zonder extra budget.</p>{link_cloudbeleid}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="balk"><div class="w">
    <div><b>De uitstaptoets toetst alle drie.</b><span>In een kwartier weet je waar je staat en wat een logische eerste stap is.</span></div>
    <a class="knop groot" href="/scan/">Doe de uitstaptoets &rarr;</a>
  </div></div>
</div></section>

<section class="rapport" id="rapport"><div class="w">
  <div>
    <p class="kicker">het uitstaprapport</p>
    <h2>Van toets naar agendapunt voor het bestuur.</h2>
    <p class="intro">De toets zegt waar je staat. Het rapport zegt wat je daarna doet, per leverancier, in de taal die je bestuur en de toezichthouder verstaan. Het wordt geschreven op jouw toetsuitkomst, aangevuld met een korte intake over je leveranciers. Het is input voor je eigen risicoanalyse, geen oordeel over naleving.</p>
    <p class="voorwie">Voor wethouders en bestuurders, CIO's, CISO's en informatiemanagers bij gemeenten, provincies, waterschappen, Rijk, zbo's en onderwijs.</p>
    <h3 class="klein">Wat je krijgt</h3>
    <ol class="register">
{register}
    </ol>
  </div>
  <div>
    <div class="prijs" data-kraak>
      <div class="ring" aria-hidden="true"></div>
      <h3 class="sr-only">Prijs</h3>
      <p class="mono marge">prijs, eenmalig</p>
      <div class="bedrag"><span class="getal k-tekst">750</span><span>euro</span></div>
      <p class="btw mono marge">excl. btw, 907,50 incl. btw</p>
      <ul>
        <li>Eenmalig, geen abonnement. Factuur op naam van je organisatie.</li>
        <li>Hermeting na een jaar: 250 euro.</li>
        <li>Gratis toets vooraf, een kwartier.</li>
      </ul>
      <h4>Hoe het werkt</h4>
      <ol>
        <li>Doe de gratis uitstaptoets, een kwartier, geen registratie.</li>
        <li>Je krijgt het rapport in zeven delen, geschreven op jouw uitkomst en een korte intake.</li>
        <li>Na een jaar meet je opnieuw en zie je wat er is veranderd.</li>
      </ol>
      <a class="knop groot" href="/scan/">Doe eerst de gratis uitstaptoets</a>
      <a class="tekstlink op-inkt" href="/rapport/voorbeeld.html">Bekijk het voorbeeldrapport</a>
      <p class="bestel">{bestel_tekst}</p>
    </div>
    <div class="afzender">
      <p class="kicker">initiatiefnemer</p>
      <p class="naam">Govert Schoof</p>
      <p>Werkt op het snijvlak van overheid, onderzoek, geo-informatie en digitale autonomie. <a class="tekstlink" href="https://www.linkedin.com/in/govertschoof/" target="_blank" rel="noopener">LinkedIn</a></p>
      <a class="fonds" href="https://www.sidnfonds.nl/" target="_blank" rel="noopener"><span>Onderzoek met steun van</span><img src="/sidnfonds.png" alt="SIDN fonds" width="150" height="28"></a>
    </div>
  </div>
</div></section>

<section class="faq" id="vragen"><div class="w">
  <div>
    <h2>Veelgestelde vragen over de uitstaptoets en het rapport</h2>
    <p class="hulp">Staat je vraag er niet bij? Mail <a class="tekstlink" href="mailto:info@willswitch.nl">info@willswitch.nl</a>.</p>
  </div>
  <div>
{faq}
  </div>
</div></section>

<section class="verhalen" id="verhalen">
  <div class="w">
    <div class="ring" aria-hidden="true"></div>
    <div>
      <p class="kicker">praktijk</p>
      <h2>Van anderen leren.</h2>
      <p class="intro">Organisaties die de stap zetten, en wat ze onderweg tegenkwamen. Eerlijk over wat werkte en wat niet.</p>
      <a class="tekstlink" href="#overzicht">Alle praktijkverhalen</a>
      <div class="klein-verhalen">
        <article>
          <div class="tegel warm" aria-hidden="true"><b>400/50</b><span class="mono">viewers in de lucht / in gebruik</span></div>
          <div><p class="kicker">inzicht</p><h3>Migreer niet alles. Ruim eerst op.</h3><p>Vierhonderd viewers in de lucht, vijftig in gebruik. De grootste valkuil is alles &eacute;&eacute;n-op-&eacute;&eacute;n willen overzetten.</p><a class="tekstlink" href="/cases/wildgroei/">Lees het inzicht over opruimen voor migratie</a></div>
        </article>
        <article>
          <div class="tegel inkt" aria-hidden="true"><b>Proefkonijn</b><span class="mono">nextcloud, eigen diensten</span></div>
          <div><p class="kicker">praktijk, SURF</p><h3>SURF is zelf proefkonijn</h3><p>De IT-co&ouml;peratie van het hoger onderwijs zette zijn eigen diensten over naar Nextcloud, om leden te laten zien dat het kan.</p><a class="tekstlink" href="/cases/surf/">Lees hoe SURF overstapte naar Nextcloud</a></div>
        </article>
      </div>
    </div>
    <div>
      <figure class="uitsteek" style="--src:url(/dsg-viewer.webp)" data-kraak>
        <img src="/dsg-viewer.webp" alt="Kaartviewer van Data Space Groningen" width="1400" height="657" loading="lazy">
        <figcaption class="opschrift marge">data space groningen<br>samen data, meer waarde<br>17 organisaties, 1 open platform</figcaption>
      </figure>
      <div class="dsg-tekst">
        <p class="kicker">praktijk, Groningen</p>
        <h3>Zeventien organisaties, &eacute;&eacute;n open platform</h3>
        <p>Overheden en waterschappen in Groningen delen hun data via een federatief, open source platform. Van overheden, door overheden. Wat het opleverde, en waar het bijna misging.</p>
        <a class="tekstlink" href="/cases/dsg/">Lees de case Data Space Groningen</a>
      </div>
    </div>
  </div>
</section>

<section class="overzicht" id="overzicht"><div class="w">
  <div class="kopregel">
    <h2>Alle cases: wetgeving, nieuws, praktijk en uitspraken</h2>
    <p class="mono">{aantal} onderdelen: wetgeving, nieuws, praktijk, inzicht, beleid en uitspraken</p>
  </div>
  <div class="register-lijst">
{items}
  </div>
</div></section>

<section class="movement" id="movement">
  <div class="ring orbit-open" aria-hidden="true"></div>
  <div class="w">
    <h2>Waar staat jouw organisatie vandaag?</h2>
    <p class="sub"><strong>Doe mee.</strong> E&eacute;n klik, geen registratie, geen mailadres. Een teken dat jullie ergens in deze beweging staan.</p>
    <p class="confirm" id="movement-confirm"></p>
    <div class="movement-grid" id="movement-grid">
      <button class="movement-btn" data-phase="verkennen" type="button"><span class="label">We verkennen</span><span class="count" data-count>&middot;</span></button>
      <button class="movement-btn" data-phase="praten" type="button"><span class="label">We praten erover</span><span class="count" data-count>&middot;</span></button>
      <button class="movement-btn" data-phase="pilot" type="button"><span class="label">We draaien een pilot</span><span class="count" data-count>&middot;</span></button>
      <button class="movement-btn" data-phase="overstap" type="button"><span class="label">We stappen over</span><span class="count" data-count>&middot;</span></button>
      <button class="movement-btn" data-phase="verder" type="button"><span class="label">We zijn al verder</span><span class="count" data-count>&middot;</span></button>
    </div>
  </div>
</section>

<div class="w onder">
  <section class="blok agenda">
    <h2>Agenda</h2>
    <p class="sub">Meepraten? Kom dan naar:</p>
    <ul>
      <li><div class="when">01.10.2026</div><div class="what"><a href="https://leiderschapstop.nl/" target="_blank" rel="noopener">LeiderschapsTop Open Source</a><span class="where">Koorkerk, Middelburg &middot; op uitnodiging</span></div></li>
    </ul>
    <p class="sub" style="margin-top:1.6rem">Geweest:</p>
    <ul>
      <li><div class="when">09.07.2026</div><div class="what"><a href="/talk/">Will Switch: help mee de overheid los te weken van Big Tech</a><span class="where">FOSS4G NL, Groningen &middot; 44 deelnemers stemden live mee, het verhaal staat online</span></div></li>
    </ul>
  </section>
  <section class="blok credits">
    <h2>Supporters van digitale autonomie</h2>
    <p class="sub">Mensen en organisaties die zich openlijk achter de beweging scharen.</p>
    <ul>
      <li><span class="name">Oskar J. Gstrein</span><span class="context">Rijksuniversiteit Groningen, <a href="https://daix.web.rug.nl/" target="_blank" rel="noopener">Data Autonomy Index</a></span></li>
    </ul>
  </section>
</div>

<section class="slot"><div class="w">
  <p class="slotzin">Niet alles hoeft anders. Maar je moet wel kunnen kiezen, en dat begint met weten of je nog weg kunt. Een kwartier, en je weet het.</p>
  <div>
    <a class="knop groot" href="/scan/">Doe de gratis uitstaptoets &rarr;</a>
    <span class="micro">een kwartier, geen registratie, je antwoorden blijven in je browser</span>
  </div>
</div></section>

<footer class="site"><div class="w">
  <span>Will Switch &middot; willswitch.nl &middot; <a href="/">terug naar de switch</a></span>
  <a class="fonds" href="https://www.sidnfonds.nl/" target="_blank" rel="noopener"><span>Onderzoek met steun van</span><img src="/sidnfonds.png" alt="SIDN fonds" width="150" height="28"></a>
</div></footer>
{movement_script}{kraak_script}
  <!-- Privacyvriendelijke analytics (GoatCounter, geen cookies) -->
  <script data-goatcounter="https://willswitch.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def build_switch(cases):
    """Maak switch.html uit de gepubliceerde cases en de quotes.
    De nummering wordt hier geschreven, niet in de browser."""
    ids = [c["id"] for c in cases]
    blokken = []
    n = 0
    for c in cases:
        n += 1
        blokken.append(overzicht_case(n, c))
    for q in load_quotes():
        n += 1
        blokken.append(overzicht_quote(n, q))

    dagen_cbw = (TODAY - CBW_DATUM).days
    dagen_dataact = (DATAACT_DATUM - TODAY).days
    teller_cbw = f"de zorgplicht geldt al {dagen_cbw} dagen" if dagen_cbw >= 0 else "de zorgplicht gaat in op 15.08.2026"
    teller_dataact = (f"nog {dagen_dataact} dagen tot de Data Act" if dagen_dataact > 0
                      else "de Data Act geldt sinds 12.01.2027")

    return PAGE.format(
        base=BASE,
        css=CSS,
        titel=TITEL,
        omschrijving=OMSCHRIJVING,
        hero_alt=HERO_ALT,
        jsonld=jsonld(cases),
        stand=TODAY.strftime("%d.%m.%Y"),
        teller_cbw=teller_cbw,
        teller_dataact=teller_dataact,
        link_cbw=case_link(ids, "cbw", "Wat de Cyberbeveiligingswet van je vraagt"),
        link_dataact=case_link(ids, "dataact", "Wat de Data Act regelt voor je cloudcontract"),
        link_cloudbeleid=case_link(ids, "cloudbeleid", "Wat het rijksbreed cloudbeleid eist"),
        register=register_html(),
        bestel_tekst=BESTEL_TEKST[BESTEL_AAN],
        faq=faq_html(),
        aantal=n,
        items="\n\n".join(blokken),
        movement_script=MOVEMENT_SCRIPT,
        kraak_script=KRAAK_SCRIPT,
    )
