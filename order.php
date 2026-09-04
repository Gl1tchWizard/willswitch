<?php
// Maakt een bestelling aan en stuurt door naar Mollie.
declare(strict_types=1);
require __DIR__ . '/../lib/db.php';
require __DIR__ . '/../lib/mollie.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_uit(['fout' => 'alleen POST'], 405);
$d = json_in();

$email = filter_var($d['email'] ?? '', FILTER_VALIDATE_EMAIL);
$org   = trim((string)($d['org'] ?? ''));
$naam  = trim((string)($d['naam'] ?? ''));
$toets = $d['toets'] ?? null;
if (!$email || $org === '' || $naam === '' || !is_array($toets) || empty($toets['sys'])) {
    json_uit(['fout' => 'onvolledig'], 400);
}
$org_type = preg_replace('/[^a-z]/', '', (string)($toets['org'] ?? 'anders')) ?: 'anders';
$bedrag   = (int)$CFG['prijs'];
$tok      = token();

$payload = json_encode([
    'toets' => $toets,
    'leveranciers' => mb_substr((string)($d['leveranciers'] ?? ''), 0, 1000),
], JSON_UNESCAPED_UNICODE);

db()->prepare('INSERT INTO bestelling (token, status, org, org_type, naam, functie, email, kvk, referentie, bedrag_cent, antwoorden)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)')
    ->execute([$tok, 'open', mb_substr($org,0,160), $org_type, mb_substr($naam,0,120),
               mb_substr((string)($d['functie'] ?? ''),0,120), $email,
               preg_replace('/\D/', '', (string)($d['kvk'] ?? '')) ?: null,
               mb_substr((string)($d['ref'] ?? ''),0,80) ?: null,
               $bedrag, versleutel($payload)]);

$incl = (int) round($bedrag * (1 + $CFG['btw'] / 100));
$betaling = mollie_maak_betaling([
    'amount'      => ['currency' => 'EUR', 'value' => number_format($incl / 100, 2, '.', '')],
    'description' => 'Will Switch uitstaprapport',
    'redirectUrl' => $CFG['site'] . '/bestel/klaar.html?t=' . $tok,
    'webhookUrl'  => $CFG['site'] . '/api/webhook.php',
    'method'      => 'ideal',
    'metadata'    => ['token' => $tok],
]);
db()->prepare('UPDATE bestelling SET mollie_id = ? WHERE token = ?')->execute([$betaling['id'], $tok]);
json_uit(['checkout' => $betaling['_links']['checkout']['href']]);
