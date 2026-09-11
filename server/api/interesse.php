<?php
// Ontvangt aanmeldingen voor updates over het rapport, of interesse in een pilot.
// Bevestigt pas als het is opgeslagen; fouten komen terug bij de gebruiker.
declare(strict_types=1);
require __DIR__ . '/../lib/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_uit(['ok' => false, 'fout' => 'alleen POST'], 405);
$d = json_in();

$email = filter_var(trim((string)($d['email'] ?? '')), FILTER_VALIDATE_EMAIL);
if (!$email) json_uit(['ok' => false, 'fout' => 'ongeldig e-mailadres'], 400);

$soort = in_array($d['soort'] ?? '', ['update', 'pilot'], true) ? $d['soort'] : 'update';

// rem: hooguit vijf aanmeldingen per ip per dag
$st = db()->prepare('SELECT COUNT(*) c FROM interesse WHERE ip_hash = ? AND aangemaakt > NOW() - INTERVAL 1 DAY');
$st->execute([ip_hash()]);
if ((int)$st->fetch()['c'] >= 5) json_uit(['ok' => false, 'fout' => 'te veel aanmeldingen vanaf dit adres'], 429);

try {
    db()->prepare('INSERT INTO interesse (soort, email, org, vraag, org_type, rol, n_systemen, ip_hash)
                   VALUES (?,?,?,?,?,?,?,?)
                   ON DUPLICATE KEY UPDATE soort = VALUES(soort), org = VALUES(org),
                                           vraag = VALUES(vraag), aangemaakt = NOW()')
        ->execute([
            $soort, $email,
            mb_substr(trim((string)($d['org'] ?? '')), 0, 160) ?: null,
            mb_substr(trim((string)($d['vraag'] ?? '')), 0, 300) ?: null,
            preg_replace('/[^a-z]/', '', (string)($d['org_type'] ?? '')) ?: null,
            preg_replace('/[^a-z]/', '', (string)($d['rol'] ?? '')) ?: null,
            max(0, min(9, (int)($d['n'] ?? 0))),
            ip_hash(),
        ]);
} catch (Throwable $e) {
    error_log('interesse opslaan mislukt: ' . $e->getMessage());
    json_uit(['ok' => false, 'fout' => 'opslaan mislukt'], 500);
}

json_uit(['ok' => true]);
