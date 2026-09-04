<?php
// Ingeroosterde taak in Plesk, elke 5 minuten:  php /pad/naar/server/cron.php
// Doet twee dingen: levert betaalde bestellingen, en ruimt oude gegevens op.
declare(strict_types=1);
require __DIR__ . '/lib/db.php';
require __DIR__ . '/lib/rapport.php';
require __DIR__ . '/lib/mail.php';

// 1. leveren
$st = db()->query("SELECT * FROM bestelling WHERE status = 'betaald' ORDER BY aangemaakt LIMIT 5");
foreach ($st as $b) {
    try {
        $data = json_decode(ontsleutel($b['antwoorden']), true);
        $pdf  = rapport_maak($b, $data);                 // schrijft pdf naar opslag, geeft pad terug
        $nr   = $b['factuurnr'] ?: factuurnummer();
        $fac  = factuur_maak($b, $nr);
        mail_rapport($b, $pdf, $fac);
        db()->prepare("UPDATE bestelling SET status='geleverd', rapport_pad=?, factuurnr=?, geleverd_op=NOW() WHERE id=?")
            ->execute([$pdf, $nr, $b['id']]);
    } catch (Throwable $e) {
        error_log('levering mislukt voor ' . $b['token'] . ': ' . $e->getMessage());
        // blijft op betaald staan, wordt volgende ronde opnieuw geprobeerd; jij ziet het in de log
    }
}

// 2. opruimen: persoonsgegevens en antwoorden wissen na de bewaartermijn, rij blijft voor de boekhouding
db()->prepare("UPDATE bestelling SET naam='', functie=NULL, email='', kvk=NULL, referentie=NULL, antwoorden='', rapport_pad=NULL
               WHERE aangemaakt < NOW() - INTERVAL ? DAY AND email <> ''")->execute([(int)$CFG['bewaar']]);
// open bestellingen die nooit betaald zijn: na 7 dagen markeren als verlopen
db()->exec("UPDATE bestelling SET status='verlopen' WHERE status='open' AND aangemaakt < NOW() - INTERVAL 7 DAY");

function factuurnummer(): string {
    $jaar = date('Y');
    $st = db()->prepare("SELECT COUNT(*) c FROM bestelling WHERE factuurnr LIKE ?"); $st->execute(["WS-$jaar-%"]);
    return sprintf('WS-%s-%04d', $jaar, (int)$st->fetch()['c'] + 1);
}
