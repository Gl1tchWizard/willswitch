<?php
// Mollie roept dit aan als de betaalstatus verandert. We vertrouwen de body niet,
// maar halen de status zelf op bij Mollie. Dat is de aanbevolen werkwijze.
declare(strict_types=1);
require __DIR__ . '/../lib/db.php';
require __DIR__ . '/../lib/mollie.php';

$id = $_POST['id'] ?? '';
if (!preg_match('/^tr_[A-Za-z0-9]+$/', $id)) { http_response_code(400); exit; }

$b = mollie_haal_betaling($id);
$tok = $b['metadata']['token'] ?? '';
$status = match ($b['status'] ?? '') {
    'paid'                              => 'betaald',
    'failed', 'canceled', 'expired'     => 'mislukt',
    default                             => null,
};
if ($status && $tok) {
    db()->prepare('UPDATE bestelling SET status = ? WHERE token = ? AND status = "open"')->execute([$status, $tok]);
}
http_response_code(200);
// levering gebeurt niet hier maar in cron.php, zodat een trage pdf de webhook nooit laat time-outen
