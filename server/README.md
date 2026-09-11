# Serverkant van de uitstaptoets

Draait op Plesk met PHP 8.4. Drie endpoints, een cron, een database.

## Inrichten, eenmalig

1. Database aanmaken in Plesk (Databases), schema laden: `server/sql/schema.sql`
2. `server/lib/config.example.php` kopieren naar `config.php` en invullen
   - `geheim`: `openssl rand -hex 32` (SSH-terminal in Plesk)
   - Mollie: testsleutel uit het Mollie-dashboard, later de livesleutel
3. In de SSH-terminal, in de map `server/`: `composer require dompdf/dompdf phpmailer/phpmailer`
4. Map `opslag/` aanmaken naast `httpdocs`, niet erin. Daar komen de pdf's.
5. `server/api/` uploaden naar `httpdocs/api/`, de rest van `server/` buiten de webroot
6. Ingeroosterde taak in Plesk, elke 5 minuten: `php /var/www/vhosts/willswitch.nl/server/cron.php`
7. In Plesk bij Mail: DKIM aanzetten voor willswitch.nl. SPF en DMARC in DNS.
8. Mollie-account aanvragen (KvK en bankrekening nodig). Webhook-url: `https://willswitch.nl/api/webhook.php`

## Hoe het stroomt

```
gratis toets (browser)
   |
   |-- scores zonder naam --> POST /api/scan.php --> tabel scan (anoniem, blijft)
   |
   '-- "bestel" --> /bestel/#antwoorden (in de hash, niet in serverlogs)
                        |
                        '-- POST /api/order.php --> tabel bestelling (antwoorden versleuteld)
                                |
                                '-- Mollie iDEAL --> webhook.php haalt status op --> "betaald"
                                                                                       |
                        cron.php (elke 5 min) <------------------------------------------'
                            |-- dompdf maakt pdf uit hetzelfde sjabloon als /rapport/voorbeeld.html
                            |-- factuur
                            '-- PHPMailer via Plesk-SMTP --> klant, bcc naar jou --> status "geleverd"

na 365 dagen: cron wist persoonsgegevens en antwoorden, rij blijft voor de boekhouding
```

## Wat waar staat en waarom

- Antwoorden gaan pas naar de server als iemand bestelt. Tot dan staan ze in de browser.
- De bestelling komt binnen via de url-hash, niet via de query, zodat leveranciersnamen niet in de serverlogs belanden.
- Antwoorden staan versleuteld in de database (AES-256-GCM). De sleutel staat in config.php, buiten de webroot.
- Pdf's staan in `opslag/`, buiten de webroot. Ze zijn alleen bereikbaar via de mail.
- De webhook vertrouwt niets uit de aanroep; hij haalt de status zelf op bij Mollie.
- Levering gebeurt in de cron, niet in de webhook. Een trage pdf kan de webhook dan nooit laten time-outen.
- Alles wat na levering misgaat, blijft staan op "betaald" en wordt de volgende ronde opnieuw geprobeerd. Jij ziet het in de foutlog van Plesk.

## Waarom deze keuzes

- **Mollie** en niet Stripe: Nederlands, iDEAL zonder omwegen, en het past bij het verhaal van de site.
- **Eigen mailserver** en niet een Amerikaanse maildienst: past bij het verhaal, en met DKIM en SPF is de bezorging prima. Loopt het toch in spam, dan is Mailjet (EU-regio) de uitwijk.
- **dompdf** en niet een externe pdf-dienst: pure PHP, geen data die de server verlaat.
- **Geen accounts**: de token in de mail is de toegang. Minder te beveiligen, minder te ondersteunen.

## Nog te maken

- `server/lib/rapport_html.php`: het sjabloon. Zelfde opbouw als `site/rapport/voorbeeld.html`, gevuld uit de antwoorden. Dezelfde regels als in de scan (kernzin, eerste stap) hergebruiken.
- `factuur_maak()`: eenvoudige pdf-factuur met je eenmanszaakgegevens, btw-nummer, factuurnummer.
- `site/voorwaarden.html`: leveringsvoorwaarden. Kern: input voor risicoanalyse, geen conformiteitsoordeel, geen juridisch advies, herroepingsrecht vervalt bij levering van het rapport.

## Voordat er een factuur uitgaat

- Eenmanszaak inschrijven, btw-nummer
- Melding nevenwerkzaamheden bij de RUG
- Mollie live-sleutel (pas na verificatie van je bankrekening)
