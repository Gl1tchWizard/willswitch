# Zo werk je met deze site

## Bouwen en uploaden

1. Bewerk de bron: `content/`, `site/` of `tools/`. Nooit `dist/`.
2. Draai `python tools/build.py` (op Windows heet het `python`, op Linux en Mac
   werkt `python3` ook).
3. Upload de inhoud van `dist/` over `httpdocs` heen op de server. Laat
   bestanden die daar al staan en niet in `dist/` zitten met rust.

De hoofdpagina `switch.html` wordt volledig gegenereerd door
`tools/switchpage.py`, de casepagina's door `tools/build.py`, de toets door
`tools/scan.py`. Er is geen losse bron voor `switch.html` meer.

Bouw ook als er inhoudelijk niets veranderd is maar de datum wel: de teller
"de zorgplicht geldt al N dagen" op de hoofdpagina komt uit de bouwdatum.

## Een nieuwe case toevoegen

Maak een bestand in `content/cases/`, bijvoorbeeld `content/cases/utrecht.html`.
Bovenaan staan de gegevens, daaronder de tekst:

```
---
{
  "id": "utrecht",
  "order": 0,
  "publish_on": "2026-09-16",
  "new_since": null,
  "eyebrow": "Praktijk · Gemeenten",
  "title": "De kop van de case",
  "card_title": "Kortere kop voor het overzicht",
  "card_body": "Twee zinnen die nieuwsgierig maken.",
  "cta": "Lees de case"
}
---

<p>De eerste alinea.</p>
<p class="case-quote">"Een uitspraak die blijft hangen."</p>
<p>De rest van het verhaal.</p>
<p class="case-credit">Met dank aan wie dan ook.</p>
```

Wat de velden doen:

- `order` bepaalt de plek in het overzicht, lager is hoger
- `publish_on` verbergt de case tot die datum, laat leeg voor direct
  (de pagina zelf wordt wel vast gebouwd, met noindex en buiten de sitemap,
  zodat er nooit een 404 ontstaat op de dag dat de kaart verschijnt)
- `new_since` geeft een case drie weken het label "nieuw" zonder hem te verbergen
- `eyebrow` begint met de soort (Wetgeving, Nieuws, Praktijk, Inzicht of Beleid);
  de hoofdpagina kleurt het label daarop
- `title` is de kop op de eigen pagina en in Google
- `card_title` en `card_body` staan in het overzicht
- optioneel: `seo_title` en `description` voor de zoekmachine, als de gewone
  titel en samenvatting daar niet goed voor werken

Daarna bouwen en uploaden.

## Een quote toevoegen

Quotes staan als JSON in `content/quotes/`, met `order`, `title`, `body`
(optioneel), `quote` en `attr`. Ze krijgen geen eigen pagina en verschijnen
onderaan het register op de hoofdpagina.

## Bestellen openzetten

In `tools/switchpage.py` staat `BESTEL_AAN = False`. Zet die op `True` op de
dag dat bestellen opengaat: de besteltekst in het prijsblok, de laatste zin van
de vierde veelgestelde vraag en de beschikbaarheid in de zoekmachinedata
veranderen dan mee. De toets zelf heeft zijn eigen vlaggen in `tools/scan.py`.

## Wat waar staat

- `content/cases/` de cases, hier bewerk je
- `content/quotes/` de quotes
- `site/` vaste bestanden: de poort (`index.html`), het voorbeeldrapport, de
  bestelpagina's, de 404, het lettertype in `fonts/`, beelden en favicons
- `tools/build.py` het bouwscript, met het sjabloon voor casepagina's
- `tools/switchpage.py` het sjabloon voor de hoofdpagina, met de teksten van
  de veelgestelde vragen en het rapportblok
- `tools/scan.py` de uitstaptoets
- `server/` de serverkant van het bestellen, draait nog nergens
- `notes/` aantekeningen en briefings, staat buiten git
- `dist/` het resultaat, niet in versiebeheer

## Beelden

Grote beelden gaan als webp in `site/`, de hoofdpagina gebruikt
`switch-hero.webp` (onder 300 kB) en `dsg-viewer.webp`. De originelen staan
ernaast. `og-image.jpg` (1200 x 630) is het deelbeeld voor LinkedIn.
