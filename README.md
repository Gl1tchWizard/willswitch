# Will Switch

Praktijkonderzoek naar digitale autonomie in de publieke sector.
Voorbeelden die werken, en wat de overstap van Big Tech naar open
alternatieven tegenhoudt.

Met steun van het SIDN Pioniersfonds. https://willswitch.nl

## Hoe deze repo werkt

De cases zijn de bron. Elke case staat als los bestand in `content/cases/`,
met bovenaan de gegevens (titel, datum, samenvatting) en daaronder de tekst.

Het script `tools/build.py` maakt daar de site van: een eigen vindbare pagina
per case, de casebibliotheek, de sitemap en de verwijzingen naar de scan.

Nieuwe case toevoegen:

1. Maak een bestand in `content/cases/`
2. Draai `python3 tools/build.py`
3. Commit en push

De rest gaat vanzelf.

## Mappen

- `content/cases/` de cases, dit is wat je bewerkt
- `site/` vaste onderdelen die niet gegenereerd worden
- `tools/` het bouwscript
- `dist/` de gegenereerde site, niet in versiebeheer
