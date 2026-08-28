"""Bouw de casebibliotheek (switch.html) uit de bron.

De kaarten linken naar echte pagina's in plaats van popups te openen.
Wordt aangeroepen vanuit build.py.
"""
import re, datetime

TODAY = datetime.date.today()


def card_html(c, published_ids):
    """Eén kaart in het overzicht, als link naar de eigen pagina."""
    classes = ["card", "span-2", "card-case"]
    attrs = ""
    # de nieuw-gloed blijft werken op basis van de publicatiedatum
    since = c.get("publish_on") or c.get("new_since")
    if since:
        days = (TODAY - datetime.date.fromisoformat(since)).days
        if days < 21:
            classes.append("card-new")
            attrs += f' data-new-since="{since}"'
    flag = '\n        <span class="card-flag">nieuw</span>' if "card-new" in classes else ""
    title = c.get("card_title") or c["title"]
    body = c.get("card_body", "")
    cta = c.get("cta", "Lees de case")
    return f'''      <a class="{' '.join(classes)}" href="/cases/{c['id']}/"{attrs}>{flag}
        <span class="num">00</span>
        <h3>{title}</h3>
        <p class="card-body">{body}</p>
        <span class="case-more">{cta}</span>
      </a>'''


def build_library(source_html, cases):
    """Vervang het kaartenraster en haal de popup-machinerie eruit."""
    doc = source_html
    ids = [c["id"] for c in cases]

    # 1) nieuw kaartenraster
    cards = "\n\n".join(card_html(c, ids) for c in cases)
    doc = re.sub(
        r'(<div class="cards">)(.*?)(\n    </div>)',
        lambda m: m.group(1) + "\n\n" + cards + m.group(3),
        doc, count=1, flags=re.S)

    # 2) verborgen case-inhoud weg, die staat nu op de eigen pagina's
    doc = re.sub(
        r'\n  <!-- Hidden case content.*?(?=\n  <!--|\n</body>)', "\n", doc, flags=re.S)
    doc = re.sub(
        r'\n  <div class="case-data" id="case-[a-z]+" hidden>.*?\n  </div>\n', "\n",
        doc, flags=re.S)

    # 3) de modal en de bijbehorende scripts weg
    doc = re.sub(r'\n  <!-- Case popup -->.*?\n  </div>\n', "\n", doc, flags=re.S)
    doc = re.sub(r'\n    /\* === Case popup === \*/.*?\n    \}\);', "", doc, flags=re.S)

    # 4) nummering: de kaarten krijgen hun nummer bij het laden
    nummering = '''
    /* === Nummering van de zichtbare kaarten === */
    (function () {
      var n = 0;
      document.querySelectorAll('.cards .card').forEach(function (card) {
        n++;
        var num = card.querySelector('.num');
        if (num) num.textContent = ('0' + n).slice(-2);
      });
    })();
'''
    doc = doc.replace("  </script>", nummering + "  </script>", 1)

    # 5) kaarten zijn nu links, dus de knop-rollen eruit
    doc = doc.replace(' role="button" tabindex="0"', "")

    # 6) kaarten zijn links: geen onderstreping, kleur van de kaart behouden
    doc = doc.replace("    .card-case {\n      cursor: pointer;\n    }",
"""    .card-case {
      cursor: pointer;
      display: block;
      text-decoration: none;
      color: inherit;
    }
    .card-case h3, .card-case .card-body, .card-case .num {
      text-decoration: none;
    }""")

    # css die alleen bij de popup hoorde
    for sel in ("case-modal", "case-modal-backdrop", "case-modal-panel",
                "case-modal-close", "case-share", "case-share-label",
                "case-share-btn"):
        doc = re.sub(r"\n    \.%s(\[[^\]]*\])?(:hover|:focus-visible)?\s*\{[^}]*\}" % sel,
                     "", doc)
    doc = re.sub(r"\n    /\* === Case (popup / modal|share bar) === \*/", "", doc)

    # de case-data opmaak hoort nu bij de casepagina's
    for sel in ("case-eyebrow", "case-quote", "case-link-wrap", "case-credit",
                "case-cap"):
        doc = re.sub(r"\n    \.case-data \.%s(:hover)?\s*\{[^}]*\}" % sel, "", doc)
    doc = re.sub(r"\n    \.case-data (h2|p|figure|img)\s*\{[^}]*\}", "", doc)
    doc = re.sub(r"\n    \.case-data p a(:hover)?\s*\{[^}]*\}", "", doc)
    doc = re.sub(r"\n    \.case-data \.(case-link-wrap|case-credit) a(:hover)?\s*\{[^}]*\}",
                 "", doc)
    doc = re.sub(r"\n    /\* === Popup image === \*/", "", doc)

    return doc
