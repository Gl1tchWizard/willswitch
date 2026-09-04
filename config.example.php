<?php
// Kopieer naar config.php (staat in .gitignore) en vul in. Nooit committen.
return [
  'db'       => ['dsn' => 'mysql:host=localhost;dbname=willswitch;charset=utf8mb4', 'user' => '', 'pass' => ''],
  'mollie'   => ['key' => 'test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'],   // live_ voor productie
  'site'     => 'https://willswitch.nl',
  'mail'     => ['host' => 'localhost', 'port' => 25, 'from' => 'rapport@willswitch.nl', 'from_naam' => 'Will Switch',
                 'bcc' => 'govert@willswitch.nl'],   // bcc: jij krijgt een kopie van elke levering
  'geheim'   => '',   // 32 bytes hex voor AES-256-GCM: openssl rand -hex 32
  'prijs'    => 75000, // in centen, excl. btw
  'btw'      => 21,
  'bewaar'   => 365,   // dagen tot persoonsgegevens en antwoorden worden gewist
  'opslag'   => __DIR__ . '/../../opslag',   // pdf's, buiten httpdocs
];
