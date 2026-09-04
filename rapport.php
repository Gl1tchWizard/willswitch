<?php
// Maakt de pdf. Gebruikt dompdf (composer require dompdf/dompdf), pure PHP, geen systeemafhankelijkheden.
// Het HTML-sjabloon is dezelfde opbouw als site/rapport/voorbeeld.html, gevuld met de echte antwoorden.
declare(strict_types=1);
require_once __DIR__ . '/../vendor/autoload.php';
use Dompdf\Dompdf;

function rapport_maak(array $b, array $data): string {
    global $CFG;
    $toets = $data['toets']; $lev = $data['leveranciers'] ?? '';
    // -- hier komt dezelfde regelset als in de scan (scores, kernzin, eerste stap) --
    // -- en de uitstapprofielen per systeem met de leveranciersnamen uit $lev --
    $html = rapport_html($b, $toets, $lev);   // zie rapport_html.php, het sjabloon
    $pdf = new Dompdf(['isRemoteEnabled' => false, 'defaultFont' => 'DejaVu Sans']);
    $pdf->loadHtml($html); $pdf->setPaper('A4'); $pdf->render();
    $pad = rtrim($CFG['opslag'], '/') . '/' . $b['token'] . '.pdf';
    file_put_contents($pad, $pdf->output());
    return $pad;
}
