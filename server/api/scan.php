<?php
// Ontvangt alleen tellingen van de gratis scan. Geen namen, geen leveranciers, geen vrije tekst.
declare(strict_types=1);
require __DIR__ . '/../lib/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_uit(['fout' => 'alleen POST'], 405);
$d = json_in();

$kies = fn($v, $lijst) => in_array($d[$v] ?? '', $lijst, true) ? $d[$v] : 'anders';
$org  = $kies('org',  ['gemeente','waterschap','provincie','rijk','gr','vr','kennis','anders']);
$rol  = $kies('rol',  ['bestuur','cio','uitvoering','anders']);
$doel = $kies('doel', ['risico','verlenging','continuiteit','bestuur','orientatie']);
$k = fn($v, $max) => max(0, min($max, (int)($d[$v] ?? 0)));

// antwoorden op de vijf organisatievragen, als 'ja,nee,x,deels,ja'
$o = array_slice(explode(',', (string)($d['o'] ?? '')), 0, 5);
$o = implode(',', array_map(fn($a) => in_array($a, ['ja','deels','nee','x'], true) ? $a : '', $o));

// eenvoudige rem: max 20 inzendingen per ip per dag
$st = db()->prepare('SELECT COUNT(*) c FROM scan WHERE ip_hash = ? AND aangemaakt > NOW() - INTERVAL 1 DAY');
$st->execute([ip_hash()]);
if ((int)$st->fetch()['c'] >= 20) json_uit(['ok' => false], 429);

db()->prepare('INSERT INTO scan (org_type, rol, doel, n_systemen, niet_eu, contract_onb, binnen_jaar, stil, weet_niet, org_antw, ip_hash)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)')
    ->execute([$org, $rol, $doel, $k('n',5), $k('niet_eu',5), $k('contract_onb',5),
               $k('binnen_jaar',5), $k('stil',5), $k('weet_niet',25), $o, ip_hash()]);
json_uit(['ok' => true]);
