<?php
declare(strict_types=1);
$CFG = require __DIR__ . '/config.php';

function db(): PDO {
    static $pdo = null;
    global $CFG;
    if ($pdo === null) {
        $pdo = new PDO($CFG['db']['dsn'], $CFG['db']['user'], $CFG['db']['pass'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}

function json_in(): array {
    $raw = file_get_contents('php://input');
    $d = json_decode($raw ?: '', true);
    return is_array($d) ? $d : [];
}

function json_uit(array $d, int $status = 200): never {
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($d, JSON_UNESCAPED_UNICODE);
    exit;
}

function token(): string {
    return rtrim(strtr(base64_encode(random_bytes(32)), '+/', '-_'), '=');
}

function ip_hash(): string {
    // zout wisselt per dag, dus niet terug te herleiden na vandaag
    $zout = date('Y-m-d');
    return substr(hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . $zout), 0, 16);
}

// AES-256-GCM: de antwoorden staan versleuteld in de database
function versleutel(string $tekst): string {
    global $CFG;
    $sleutel = hex2bin($CFG['geheim']);
    $iv = random_bytes(12);
    $tag = '';
    $c = openssl_encrypt($tekst, 'aes-256-gcm', $sleutel, OPENSSL_RAW_DATA, $iv, $tag);
    return $iv . $tag . $c;
}
function ontsleutel(string $blob): string {
    global $CFG;
    $sleutel = hex2bin($CFG['geheim']);
    $iv = substr($blob, 0, 12); $tag = substr($blob, 12, 16); $c = substr($blob, 28);
    return openssl_decrypt($c, 'aes-256-gcm', $sleutel, OPENSSL_RAW_DATA, $iv, $tag) ?: '';
}
