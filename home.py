"""Bouw de homepage: het portaal blijft, er komt inhoud onder.

Het portaal is de sfeer en de doorgang. Daaronder komt wat Google kan
lezen en wat een bezoeker kan doen: de scan, en de nieuwste verhalen.
"""
import re, datetime

TODAY = datetime.date.today()

META = '''  <title>Will Switch: van afhankelijkheid naar keuzevrijheid</title>
  <meta name="description" content="Praktijkonderzoek naar digitale autonomie in de publieke sector. Wat overheden tegenhoudt bij de overstap van Big Tech naar open alternatieven, en wat wel werkt.">'''

SECTION_CSS = '''
    /* === Inhoud onder het portaal === */
    .below {
      position: relative; z-index: 10;
      background: #F0EDE6; color: #1a1612;
      font-family: 'Space Mono', monospace;
    }
    .below .inner { max-width: 52rem; margin: 0 auto; padding: 5rem 1.5rem; }
    .below h2 {
      font-family: 'Orbitron', monospace;
      font-size: clamp(1.4rem, 3.4vw, 2.1rem); font-weight: 700;
      line-height: 1.2; margin-bottom: 1.2rem; color: #1a1612;
    }
    .below p { font-size: 0.95rem; line-height: 1.7; color: #4a443c; margin-bottom: 1rem; max-width: 44rem; }
    .below .lead { font-size: 1.05rem; }
    .below .marker {
      font-family: 'Orbitron', monospace; font-size: 0.68rem;
      letter-spacing: 0.28em; text-transform: uppercase;
      color: #E84500; margin-bottom: 1.2rem;
    }
    .scan-block {
      margin-top: 3rem; padding: 2.2rem 2rem;
      background: #E8E3D6; border: 1px solid rgba(26,22,18,0.12); border-radius: 4px;
    }
    .scan-block h3 {
      font-family: 'Orbitron', monospace; font-size: 1.15rem;
      margin-bottom: 0.7rem; color: #1a1612;
    }
    .scan-cta {
      display: inline-block; margin-top: 1rem;
      background: #E84500; color: #F0EDE6; text-decoration: none;
      font-family: 'Orbitron', monospace; font-size: 0.75rem; font-weight: 700;
      letter-spacing: 0.12em; text-transform: uppercase;
      padding: 0.95rem 1.6rem; border-radius: 3px;
      transition: background 0.2s ease;
    }
    .scan-cta:hover { background: #1a1612; }
    .recent { margin-top: 3.5rem; }
    .recent ul { list-style: none; border-top: 1px solid rgba(26,22,18,0.12); }
    .recent li { border-bottom: 1px solid rgba(26,22,18,0.12); }
    .recent a {
      display: block; padding: 1.1rem 0; text-decoration: none; color: #1a1612;
      transition: color 0.2s ease;
    }
    .recent a:hover { color: #E84500; }
    .recent .k {
      font-family: 'Orbitron', monospace; font-size: 0.95rem;
      line-height: 1.3; display: block; margin-bottom: 0.3rem;
    }
    .recent .s { font-size: 0.85rem; color: #4a443c; }
    .below .allelinks {
      display: inline-block; margin-top: 1.5rem;
      font-family: 'Orbitron', monospace; font-size: 0.72rem;
      letter-spacing: 0.1em; text-transform: uppercase;
      color: #E84500; text-decoration: none;
      border-bottom: 1px solid rgba(232,69,0,0.4); padding-bottom: 2px;
    }
    .below .allelinks:hover { color: #1a1612; border-color: #1a1612; }
'''


SCAN_AAN = False   # FASE 0: zet op True zodra de scan open mag

SCANBLOK = '''      <div class="scan-block">
        <h3>Waar staat jouw organisatie?</h3>
        <p>De uitstaptoets brengt in kaart hoe afhankelijk je bent van je leveranciers,
        wat de wet daarover van je vraagt en wat een logische eerste stap is. Kost een
        kwartier, geen registratie nodig.</p>
        <a class="scan-cta" href="/scan/">Doe de toets</a>
      </div>'''

def section_html(cases):
    items = "\n".join(
        f'''          <li><a href="/cases/{c['id']}/">
            <span class="k">{c.get('card_title') or c['title']}</span>
            <span class="s">{c.get('card_body','')}</span>
          </a></li>''' for c in cases[:4])
    scanblok = SCANBLOK if SCAN_AAN else ''
    return f'''
  <section class="below">
    <div class="inner">
      <p class="marker">het onderzoek</p>
      <h2>Waarom blijven publieke organisaties hangen bij Big Tech?</h2>
      <p class="lead">De alternatieven bestaan allang. Open source, Europees, in de
      praktijk bewezen. Toch blijft de overstap bij veel gemeenten, waterschappen en
      kennisinstellingen liggen.</p>
      <p>Will Switch onderzoekt waar dat op vastloopt. Uit de gesprekken tot nu toe
      komt steeds hetzelfde beeld: het ligt zelden aan de techniek. Het ligt aan de
      vraagkant, aan wat organisaties durven vragen en aan wie zich eigenaar voelt
      van de stap.</p>
      <p>Op deze site verzamel ik de voorbeelden die werken en de drempels die er
      in de praktijk echt toe doen. Niet anti-Big Tech, wel pro-keuzevrijheid.</p>

{scanblok}

      <div class="recent">
        <p class="marker">uit de praktijk</p>
        <ul>
{items}
        </ul>
        <a class="allelinks" href="/switch.html">Alle praktijkverhalen</a>
      </div>
    </div>
  </section>
'''


def build_home(source_html, cases):
    doc = source_html

    # titel en omschrijving die vertellen waar het over gaat
    doc = re.sub(r'  <title>.*?</title>\n(  <meta name="description"[^>]*>\n)?',
                 META + "\n", doc, count=1, flags=re.S)

    # opmaak voor het nieuwe blok
    doc = doc.replace("  </style>", SECTION_CSS + "  </style>", 1)

    # inhoud onder het portaal
    doc = doc.replace("  <script>", section_html(cases) + "\n  <script>", 1)

    # het portaal mag niet langer de hele hoogte claimen, anders zie je
    # de inhoud eronder niet staan
    doc = doc.replace("body {\n      min-height: 100%;",
                      "body {\n      min-height: 100%;\n      overflow-y: auto;")

    return doc
