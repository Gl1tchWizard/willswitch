<?php
// Ontvangt alleen geaggregeerde scores van de gratis toets. Geen namen, geen vrije tekst.
declare(strict_types=1);
require __DIR__ . '/../lib/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_uit(['fout' => 'alleen POST'], 405);
$d = json_in();

$toegestaan_org = ['gemeente','waterschap','provincie','rijk','gr','kennis','anders'];
$toegestaan_rol = ['bestuur','cio','uitvoering','anders'];
$org = in_array($d['org'] ?? '', $toegestaan_org, true) ? $d['org'] : 'anders';
$rol = in_array($d['rol'] ?? '', $toegestaan_rol, true) ? $d['rol'] : 'anders';
$k = fn($v, $max) => max(0, min($max, (int)($d[$v] ?? 0)));

// eenvoudige rem: max 20 inzendingen per ip per dag
$st = db()->prepare('SELECT COUNT(*) c FROM scan WHERE ip_hash = ? AND aangemaakt > NOW() - INTERVAL 1 DAY');
$st->execute([ip_hash()]);
if ((int)$st->fetch()['c'] >= 20) json_uit(['ok' => false], 429);

db()->prepare('INSERT INTO scan (org_type, rol, n_systemen, niet_eu, contract_onb, dek_a, dek_b, dek_c, onbekend, ip_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?)')
    ->execute([$org, $rol, $k('n',5), $k('niet_eu',5), $k('contract_onbekend',5),
               $k('a',100), $k('b',100), $k('c',100), $k('onbekend',10), ip_hash()]);
json_uit(['ok' => true]);
