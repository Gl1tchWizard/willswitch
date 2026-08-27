# Zo werk je met deze site

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
  "eyebrow": "Praktijk / Gemeenten",
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
- `title` is de kop op de eigen pagina en in Google
- `card_title` en `card_body` staan in het overzicht

Draai daarna `python3 tools/build.py` en push. De casepagina, het overzicht
en de sitemap worden bijgewerkt.

## Een case aanpassen

Bewerk het bestand in `content/cases/`, draai het script, push. Nooit de
bestanden in `dist/` aanpassen, want die worden bij de volgende bouw
overschreven.

## Wat waar staat

- `content/cases/` de cases, hier bewerk je
- `site/` vaste bestanden zoals de homepage en afbeeldingen
- `tools/build.py` het script dat de site maakt
- `dist/` het resultaat, niet in versiebeheer
