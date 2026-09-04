-- Will Switch uitstaptoets: databaseschema (MySQL 8 / MariaDB 10.6+)
-- Twee tabellen. Bewust weinig: alleen wat nodig is om te meten en te leveren.

-- 1. Geaggregeerde toetsscores. Anoniem, nooit verwijderd, voedt de benchmark.
CREATE TABLE scan (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  aangemaakt    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  org_type      VARCHAR(20)  NOT NULL,   -- gemeente, waterschap, ...
  rol           VARCHAR(20)  NOT NULL,   -- bestuur, cio, uitvoering, anders
  n_systemen    TINYINT UNSIGNED NOT NULL,
  niet_eu       TINYINT UNSIGNED NOT NULL,
  contract_onb  TINYINT UNSIGNED NOT NULL,
  dek_a         TINYINT UNSIGNED NOT NULL,   -- ketenzorgplicht, 0-100
  dek_b         TINYINT UNSIGNED NOT NULL,   -- overstaprecht
  dek_c         TINYINT UNSIGNED NOT NULL,   -- exitplan
  onbekend      TINYINT UNSIGNED NOT NULL,   -- vragen die niemand kon beantwoorden
  ip_hash       CHAR(16) NOT NULL,           -- afgekapte sha256 van ip + dagzout, alleen tegen misbruik
  INDEX (org_type, aangemaakt)
);

-- 2. Bestellingen. Bevat persoonsgegevens en de volledige antwoorden (versleuteld).
--    Wordt na 12 maanden geleegd door een ingeroosterde taak (zie cron.php).
CREATE TABLE bestelling (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  token         CHAR(43) NOT NULL UNIQUE,    -- base64url van 32 willekeurige bytes, dient als toegangssleutel
  aangemaakt    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status        ENUM('open','betaald','geleverd','mislukt','verlopen') NOT NULL DEFAULT 'open',
  org           VARCHAR(160) NOT NULL,
  org_type      VARCHAR(20)  NOT NULL,
  naam          VARCHAR(120) NOT NULL,
  functie       VARCHAR(120),
  email         VARCHAR(190) NOT NULL,
  kvk           VARCHAR(12),
  referentie    VARCHAR(80),
  bedrag_cent   INT UNSIGNED NOT NULL,
  mollie_id     VARCHAR(40),                 -- tr_xxx
  antwoorden    BLOB NOT NULL,               -- AES-256-GCM versleuteld JSON van de toets plus leveranciersnamen
  rapport_pad   VARCHAR(255),                -- pad naar de gegenereerde pdf, buiten de webroot
  factuurnr     VARCHAR(20),
  geleverd_op   DATETIME,
  INDEX (status), INDEX (aangemaakt)
);
