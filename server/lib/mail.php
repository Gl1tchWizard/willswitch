<?php
// Verstuurt via de eigen Plesk-mailserver met PHPMailer (composer require phpmailer/phpmailer).
// Vereist SPF, DKIM en DMARC op willswitch.nl, anders belandt het in spam. Plesk regelt DKIM met een vinkje.
declare(strict_types=1);
require_once __DIR__ . '/../vendor/autoload.php';
use PHPMailer\PHPMailer\PHPMailer;

function mail_rapport(array $b, string $pdf, ?string $factuur): void {
    global $CFG;
    $m = new PHPMailer(true);
    $m->isSMTP(); $m->Host = $CFG['mail']['host']; $m->Port = $CFG['mail']['port'];
    $m->CharSet = 'UTF-8';
    $m->setFrom($CFG['mail']['from'], $CFG['mail']['from_naam']);
    $m->addAddress($b['email'], $b['naam']);
    if (!empty($CFG['mail']['bcc'])) $m->addBCC($CFG['mail']['bcc']);
    $m->Subject = 'Je uitstaprapport, ' . $b['org'];
    $m->Body = "Beste {$b['naam']},\n\nHierbij het uitstaprapport voor {$b['org']}.\n\n"
             . "Het rapport is input voor jullie eigen risicoanalyse en geen oordeel over naleving van wetgeving.\n\n"
             . "Tip: laat een collega uit een andere laag van de organisatie de gratis toets doen op willswitch.nl/scan/. "
             . "De mandaatkloof die daaruit komt is vaak het eerste gesprek dat je wilt voeren.\n\n"
             . "Hartelijke groet,\nGovert Schoof\nWill Switch, willswitch.nl";
    $m->addAttachment($pdf, 'uitstaprapport-' . preg_replace('/[^a-z0-9]+/i', '-', $b['org']) . '.pdf');
    if ($factuur) $m->addAttachment($factuur, 'factuur-' . $b['factuurnr'] . '.pdf');
    $m->send();
}
