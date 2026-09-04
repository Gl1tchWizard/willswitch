<?php
// Minimale Mollie-koppeling zonder SDK: twee aanroepen, meer is niet nodig.
declare(strict_types=1);

function mollie_req(string $methode, string $pad, ?array $body = null): array {
    global $CFG;
    $ch = curl_init('https://api.mollie.com/v2' . $pad);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CUSTOMREQUEST  => $methode,
        CURLOPT_HTTPHEADER     => ['Authorization: Bearer ' . $CFG['mollie']['key'], 'Content-Type: application/json'],
        CURLOPT_POSTFIELDS     => $body ? json_encode($body) : null,
        CURLOPT_TIMEOUT        => 15,
    ]);
    $r = curl_exec($ch);
    if ($r === false) throw new RuntimeException('mollie onbereikbaar');
    $d = json_decode($r, true);
    if (!is_array($d) || isset($d['status']) && is_int($d['status']) && $d['status'] >= 400) {
        throw new RuntimeException('mollie: ' . ($d['detail'] ?? 'fout'));
    }
    return $d;
}
function mollie_maak_betaling(array $b): array { return mollie_req('POST', '/payments', $b); }
function mollie_haal_betaling(string $id): array { return mollie_req('GET', '/payments/' . rawurlencode($id)); }
