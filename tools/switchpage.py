"""Bouw switch.html, de eigenlijke hoofdpagina.

Van boven naar beneden: header, beeldstrook, hero, waarom nu (de drie
kaders), van anderen leren, het volledige overzicht van cases en quotes,
de peiling, agenda, supporters, initiatiefnemer.

De teksten van het bovenste deel komen uit notes/prototype/asym.html en
zijn letterlijk overgenomen. Wordt aangeroepen vanuit build.py.
"""
import datetime, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://willswitch.nl"
TODAY = datetime.date.today()
NIEUW_DAGEN = 21


# ---------- hulpfuncties ----------

def load_quotes():
    d = ROOT / "content" / "quotes"
    if not d.exists():
        return []
    out = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))]
    out.sort(key=lambda q: q.get("order", 999))
    return out


def is_nieuw(c):
    since = c.get("publish_on") or c.get("new_since")
    if not since:
        return False
    return (TODAY - datetime.date.fromisoformat(since)).days < NIEUW_DAGEN


def case_link(ids, cid, tekst, anders="Uitleg volgt"):
    """Link naar een casepagina als die bestaat, anders een stille melding."""
    if cid in ids:
        return f'<a class="tekstlink" href="/cases/{cid}/">{tekst}</a>'
    return f'<span class="volgt">{anders}</span>'


def kicker_class(eyebrow):
    """Kleur van het label naar de soort: Wetgeving, Nieuws, Praktijk, Inzicht, Beleid."""
    soort = (eyebrow or "").split("·")[0].split("/")[0].strip().lower()
    return "k-" + soort if soort in ("wetgeving", "nieuws", "praktijk", "inzicht", "beleid") else "k-overig"


def overzicht_case(n, c):
    vlag = '<span class="vlag">nieuw</span>' if is_nieuw(c) else ""
    titel = c.get("card_title") or c["title"]
    return f'''      <a class="item" href="/cases/{c['id']}/">
        <span class="num">{n:02d}</span>{vlag}
        <span class="kicker {kicker_class(c.get("eyebrow"))}">{c.get("eyebrow", "")}</span>
        <h3>{titel}</h3>
        <p>{c.get("card_body", "")}</p>
        <span class="meer">{c.get("cta", "Lees de case")}</span>
      </a>'''


def overzicht_quote(n, q):
    body = f'\n        <p>{q["body"]}</p>' if q.get("body") else ""
    attr = f'<span class="attr">{q["attr"]}</span>' if q.get("attr") else ""
    return f'''      <article class="item quote">
        <span class="num">{n:02d}</span>
        <h3>{q["title"]}</h3>{body}
        <blockquote>{q["quote"]}{attr}</blockquote>
      </article>'''


# ---------- opmaak ----------

CSS = """
@font-face {
  font-family:'Atkinson Hyperlegible Next';
  src:url('/fonts/AtkinsonNext.woff2') format('woff2');
  font-weight:200 800; font-style:normal; font-display:swap;
}
:root {
  --papier:#F0EDE6; --warm:#E8E3D6; --wit:#FBFAF7;
  --inkt:#1a1612; --zacht:#4a443c; --vaag:#6b645a;
  --lijn:rgba(26,22,18,.16); --oranje:#E84500; --knop:#D63F00; --link:#B83500;
}
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  background:var(--papier); color:var(--inkt);
  font-family:'Atkinson Hyperlegible Next', system-ui, sans-serif;
  font-size:17px; line-height:1.55;
}
.w { max-width:1120px; margin:0 auto; padding:0 40px; }
a { color:inherit; }
h1, h2, h3 { font-weight:700; }
:focus-visible { outline:3px solid var(--knop); outline-offset:3px; }

/* knoppen en links */
.knop {
  display:inline-flex; align-items:center; justify-content:center; gap:.55em;
  min-height:44px; background:var(--knop); color:#fff; font-weight:700;
  text-decoration:none; border-radius:5px; padding:12px 20px; font-size:16px; line-height:1.1;
}
.knop:hover { background:var(--inkt); }
.knop.groot { padding:18px 28px; font-size:19px; }
.tekstlink {
  color:var(--link); font-weight:600; text-decoration:underline;
  text-underline-offset:4px; text-decoration-thickness:1.5px;
}
.tekstlink:hover { color:var(--inkt); }

/* header */
header.top { border-bottom:1px solid var(--lijn); background:var(--papier); }
header.top .w { display:flex; align-items:center; justify-content:space-between; min-height:84px; gap:20px; }
.merk { display:flex; align-items:center; gap:18px; text-decoration:none; }
.merk img { height:36px; width:auto; display:block; }
.merk span { font-size:13px; color:var(--vaag); line-height:1.35; padding-left:18px; border-left:1px solid var(--lijn); }
nav.hoofd { display:flex; align-items:center; gap:28px; font-size:16px; }
nav.hoofd a.l { text-decoration:none; padding:10px 0; }
nav.hoofd a.l:hover { text-decoration:underline; text-underline-offset:4px; }

/* hero: de astronaut en de ring links, de tekst rechts op de lucht */
.hero {
  background:#cfd4cf url('/switch-hero.webp') center 78% / cover no-repeat;
  min-height:620px; display:flex; align-items:center;
}
.hero .w { width:100%; display:grid; grid-template-columns:1fr minmax(0, 580px); }
.hero-tekst {
  grid-column:2; margin:56px 0; padding:40px 40px 36px;
  background:rgba(240,237,230,.86); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px);
  border-radius:6px; box-shadow:0 20px 50px rgba(26,22,18,.12);
}
.hoek { font-size:13px; letter-spacing:.14em; text-transform:uppercase; font-weight:700; line-height:1.7; }
.hoek::after { content:""; display:block; width:28px; height:2px; background:var(--oranje); margin-top:10px; }
.hero-tekst .hoek { margin-bottom:22px; }
h1 { font-size:52px; line-height:1.05; letter-spacing:-.01em; }
.hero p.sub { font-size:19px; color:var(--zacht); margin:16px 0 26px; max-width:36ch; }
.acties { display:flex; align-items:center; gap:20px; flex-wrap:wrap; }
.meta { font-size:15px; color:var(--vaag); }
.hoek.drie { margin-top:28px; font-weight:400; color:var(--zacht); }
.hoek.drie::after { display:none; }

/* manifest: het citaat, met de ring als motief */
.manifest { position:relative; overflow:hidden; padding-top:52px; padding-bottom:44px; }
.manifest p { position:relative; font-size:30px; line-height:1.25; font-weight:700; max-width:26ch; letter-spacing:-.01em; }
.manifest small { position:relative; display:block; margin-top:14px; font-size:14px; color:var(--vaag); }
.ring { position:absolute; border:2px solid var(--oranje); border-radius:50%; pointer-events:none; }
.manifest .ring { width:300px; height:300px; right:40px; top:-110px; opacity:.5; }
.manifest .ring.klein { width:110px; height:110px; right:330px; top:60px; opacity:.3; border-width:1.5px; }

/* sectiekop */
.sectiekop { display:grid; grid-template-columns:1fr 1.1fr auto; gap:40px; align-items:end; padding:52px 0 28px; border-top:1px solid var(--inkt); }
.sectiekop h2 { font-size:40px; line-height:1.08; letter-spacing:-.01em; display:flex; align-items:center; gap:16px; }
.sectiekop h2::before, .movement h2::before { content:""; flex:none; width:18px; height:18px; border:3px solid var(--oranje); border-radius:50%; }
.sectiekop p { color:var(--zacht); font-size:16px; max-width:44ch; }

/* pijlers, asymmetrisch */
.pijlers { display:grid; grid-template-columns:1.25fr 1fr; gap:20px; padding-bottom:20px; }
.pijler { background:var(--wit); border:1px solid var(--lijn); border-radius:6px; padding:30px 30px 26px; display:flex; flex-direction:column; }
.pijler.groot { padding:36px 36px 30px; }
.stapel { display:grid; gap:20px; }
.soort { display:inline-block; align-self:flex-start; font-size:13px; font-weight:700; padding:4px 10px; border-radius:999px; margin-bottom:22px; }
.soort.wet { background:var(--inkt); color:#fff; }
.soort.eu { background:#2F4F6F; color:#fff; }
.soort.bel { border:1.5px solid var(--inkt); }
.moment { font-weight:700; color:var(--oranje); line-height:1; letter-spacing:-.01em; }
.groot .moment { font-size:64px; margin-bottom:8px; }
.stapel .moment { font-size:38px; margin-bottom:6px; }
.pijler h3 { line-height:1.15; margin-bottom:6px; }
.groot h3 { font-size:30px; }
.stapel h3 { font-size:23px; }
.sinds { font-size:15px; color:var(--vaag); margin-bottom:18px; }
.pijler p.wat { color:var(--zacht); font-size:16.5px; margin-bottom:auto; }
.groot p.wat { font-size:18px; }
.drievragen { margin-top:24px; padding:18px 20px; background:var(--warm); border-radius:4px; }
.drievragen b { display:block; font-size:15px; margin-bottom:10px; }
.drievragen ol { padding-left:20px; font-size:15.5px; color:var(--zacht); }
.drievragen li { margin-bottom:6px; }
.pijler .voet .volgt { font-style:italic; }
.pijler .voet { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-top:22px; padding-top:16px; border-top:1px solid var(--lijn); font-size:15px; color:var(--vaag); }
.cta { position:relative; overflow:hidden; margin:20px 0 0; display:flex; align-items:center; justify-content:space-between; gap:24px; background:var(--inkt); color:var(--papier); border-radius:6px; padding:26px 30px; }
.cta .ring { width:320px; height:320px; right:300px; top:-170px; opacity:.35; }
.cta > div, .cta > a { position:relative; }
.cta b { display:block; font-size:22px; margin-bottom:4px; }
.cta span { font-size:16px; color:rgba(240,237,230,.78); }
.cta .knop { flex:none; }

/* verhalen, asymmetrisch met beeld */
.verhalen { display:grid; grid-template-columns:1.25fr 1fr; gap:28px; padding-bottom:24px; }
.verhaal { display:flex; flex-direction:column; }
.verhaal .beeld { background:var(--warm); border-radius:4px; overflow:hidden; }
.verhaal .beeld img { width:100%; height:100%; object-fit:cover; display:block; }
.verhaal.groot .beeld { aspect-ratio:16/11; margin-bottom:18px; }
.klein { display:grid; gap:24px; align-content:start; }
.klein .verhaal { display:grid; grid-template-columns:1fr; gap:20px; }
.klein .verhaal.met-beeld { grid-template-columns:200px 1fr; }
.klein .beeld { aspect-ratio:4/3; }
.kicker { font-size:13px; font-weight:700; color:var(--link); margin-bottom:6px; }
.verhaal h3 { line-height:1.15; margin-bottom:8px; }
.verhaal.groot h3 { font-size:28px; }
.klein h3 { font-size:20px; }
.verhaal p { color:var(--zacht); font-size:16px; margin-bottom:10px; }

/* overzicht van alle cases en quotes */
.overzicht { display:grid; grid-template-columns:repeat(3, 1fr); gap:16px; padding-bottom:24px; }
.item {
  position:relative; display:flex; flex-direction:column; gap:8px;
  background:var(--wit); border:1px solid var(--lijn); border-radius:6px;
  padding:22px 22px 20px; text-decoration:none; color:inherit;
  transition:transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
a.item:hover { border-color:var(--inkt); transform:translateY(-3px); box-shadow:0 10px 24px rgba(26,22,18,.10); }
.item .num { font-size:14px; font-weight:700; color:var(--oranje); margin-bottom:4px; }
.item .vlag { position:absolute; top:18px; right:18px; font-size:12px; font-weight:700; background:var(--oranje); color:#fff; padding:3px 8px; border-radius:999px; }
.item .kicker { align-self:flex-start; font-size:12px; font-weight:700; padding:3px 9px; border-radius:999px; background:var(--warm); color:var(--inkt); margin-bottom:2px; }
.item .k-wetgeving, .item .k-beleid { background:var(--inkt); color:#fff; }
.item .k-nieuws { background:#2F4F6F; color:#fff; }
.item .k-praktijk { background:var(--knop); color:#fff; }
.item .k-inzicht { background:transparent; border:1.5px solid var(--inkt); }
.item h3 { font-size:19px; line-height:1.2; }
.item p { font-size:15px; color:var(--zacht); }
.item .meer { margin-top:auto; padding-top:10px; font-size:15px; font-weight:600; color:var(--link); text-decoration:underline; text-underline-offset:4px; }
.item.quote { background:var(--warm); }
.item.quote blockquote { margin-top:auto; padding-top:6px; font-size:16px; font-weight:600; line-height:1.4; }
.item.quote blockquote::before { content:"\\201C"; display:block; font-size:64px; line-height:.55; color:var(--oranje); margin:10px 0 6px; }
.item.quote .attr { display:block; margin-top:8px; font-size:13px; font-weight:400; color:var(--vaag); }

/* peiling, op inkt */
.movement { position:relative; overflow:hidden; background:var(--inkt); color:var(--papier); padding:60px 0 64px; margin-top:24px; }
.movement .ring { width:520px; height:520px; right:-140px; top:-260px; opacity:.28; }
.movement .ring.klein { width:200px; height:200px; right:360px; top:140px; opacity:.18; }
.movement .w { position:relative; }
.movement h2 { font-size:40px; line-height:1.08; letter-spacing:-.01em; margin-bottom:10px; display:flex; align-items:center; gap:16px; }
.movement .sub { color:rgba(240,237,230,.75); font-size:16px; max-width:52ch; margin-bottom:22px; }
.movement .sub strong { color:var(--papier); }
.movement .confirm { min-height:1.5em; font-size:16px; color:var(--papier); margin-bottom:16px; }
.movement .confirm:empty { display:none; }
.movement-grid { display:grid; grid-template-columns:repeat(5, 1fr); gap:12px; }
.movement-btn {
  min-height:64px; display:flex; flex-direction:column; align-items:flex-start; gap:6px;
  background:transparent; border:1px solid rgba(240,237,230,.35); border-radius:6px; padding:16px 18px;
  font:inherit; font-size:16px; text-align:left; color:var(--papier); cursor:pointer;
  transition:transform .25s ease, background .2s ease, border-color .2s ease;
}
.movement-btn:hover { border-color:var(--papier); background:rgba(240,237,230,.06); }
.movement-btn .count { font-size:26px; font-weight:700; color:var(--oranje); line-height:1; }
.movement-btn.selected { background:var(--knop); border-color:var(--knop); color:#fff; }
.movement-btn.selected .count { color:#fff; }
.movement-btn.pulse { transform:scale(1.03); }

/* agenda, supporters, initiatiefnemer: naast elkaar */
.onder { display:grid; grid-template-columns:1.2fr 1fr; gap:56px; padding:56px 0 40px; }
.blok h2 { font-size:26px; line-height:1.1; margin-bottom:6px; }
.blok .sub { color:var(--zacht); font-size:16px; margin-bottom:18px; }
.blok + .blok { margin-top:40px; }
.agenda ul { list-style:none; }
.agenda li { display:grid; grid-template-columns:150px 1fr; gap:20px; padding:14px 0; border-top:1px solid var(--lijn); }
.agenda .when { font-weight:700; color:var(--oranje); }
.agenda .what a { font-weight:600; }
.agenda .where { display:block; font-size:15px; color:var(--vaag); margin-top:2px; }
.credits ul { list-style:none; }
.credits li { padding:12px 0; border-top:1px solid var(--lijn); }
.credits .name { font-weight:700; display:block; }
.credits .context { font-size:15px; color:var(--zacht); }
.initiator .label { font-size:13px; font-weight:700; color:var(--vaag); margin-bottom:6px; }
.initiator .name { font-size:22px; font-weight:700; }
.initiator .desc { color:var(--zacht); font-size:16px; max-width:52ch; margin:4px 0 10px; }
footer.site { border-top:1px solid var(--inkt); padding:24px 0 40px; font-size:14px; color:var(--vaag); }
footer.site .w { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px 24px; }
footer.site .fonds { display:inline-flex; align-items:center; gap:12px; text-decoration:none; }
footer.site .fonds img { height:28px; width:auto; display:block; }

/* mobiel */
@media (max-width:820px) {
  .w { padding:0 20px; }
  header.top .w { flex-wrap:wrap; padding-top:14px; padding-bottom:14px; }
  .merk span { display:none; }
  nav.hoofd { gap:18px; }
  .hero { display:block; min-height:0; background:none; }
  .hero::before { content:""; display:block; aspect-ratio:4/3; background:#cfd4cf url('/switch-hero.webp') 28% 85% / cover no-repeat; }
  .hero .w { grid-template-columns:1fr; }
  .hero-tekst { grid-column:1; margin:0; padding:28px 0 8px; background:none; backdrop-filter:none; -webkit-backdrop-filter:none; box-shadow:none; border-radius:0; }
  .hero-tekst .hoek { margin-bottom:14px; }
  .hero p.sub { font-size:17px; }
  .hoek.drie { margin-top:20px; }
  .manifest { padding-top:36px; padding-bottom:32px; }
  .manifest p { font-size:24px; }
  .manifest .ring { right:-170px; top:-150px; opacity:.35; }
  .manifest .ring.klein { display:none; }
  .sectiekop, .pijlers, .verhalen, .movement-grid, .onder { grid-template-columns:1fr; }
  .onder { gap:8px; padding:40px 0 24px; }
  .movement { padding:44px 0 48px; }
  .movement .ring { right:-260px; top:-300px; }
  .movement .ring.klein { display:none; }
  .cta .ring { display:none; }
  .sectiekop { gap:12px; padding:40px 0 20px; }
  .overzicht { grid-template-columns:1fr; }
  h1 { font-size:38px; }
  .sectiekop h2, .movement h2 { font-size:30px; }
  .groot .moment { font-size:48px; }
  .pijler.groot { padding:26px 22px 22px; }
  .cta { flex-direction:column; align-items:flex-start; }
  .klein .verhaal.met-beeld { grid-template-columns:1fr; }
  .agenda li { grid-template-columns:1fr; gap:4px; }
}
@media (min-width:821px) and (max-width:1000px) {
  .overzicht { grid-template-columns:repeat(2, 1fr); }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior:auto; }
  .movement-btn, .item { transition:none; }
  .movement-btn.pulse { transform:none; }
  a.item:hover { transform:none; }
}
"""


# ---------- vaste onderdelen ----------

MOVEMENT_SCRIPT = """
  <script>
    // ===== Movement signal section =====
    (function () {
      const API_BASE = 'https://abacus.jasoncameron.dev';
      const NAMESPACE = 'willswitch.nl';
      const STORAGE_KEY = 'willswitch_movement_phase';

      const PHASES = {
        verkennen: 'We verkennen',
        praten:    'We praten erover',
        pilot:     'We draaien een pilot',
        overstap:  'We stappen over',
        verder:    'We zijn al verder'
      };

      const section   = document.getElementById('movement');
      if (!section) return;
      const confirmEl = document.getElementById('movement-confirm');
      const buttons   = section.querySelectorAll('.movement-btn');

      function countEl(phase) {
        return section.querySelector(`[data-phase="${phase}"] [data-count]`);
      }
      function currentCount(phase) {
        const n = parseInt(countEl(phase).textContent, 10);
        return isNaN(n) ? 0 : n;
      }
      function setCount(phase, value) {
        countEl(phase).textContent = value;
      }

      // Friendly confirmation: number + reassurance, not official-data tone
      function confirmationText(phase) {
        const label = PHASES[phase];
        const n = currentCount(phase);
        if (n <= 1) {
          return `Genoteerd: <strong>"${label}"</strong>. Het eerste signaal in deze fase. Anderen volgen vast.`;
        }
        return `Dit patroon zien we vaker. Inmiddels <strong>${n} signalen</strong> in <strong>"${label}"</strong>. Je bent niet de enige.`;
      }

      function highlight(phase, animate) {
        buttons.forEach((b) => b.classList.remove('selected'));
        const btn = section.querySelector(`[data-phase="${phase}"]`);
        if (!btn) return;
        btn.classList.add('selected');
        if (animate) {
          btn.classList.add('pulse');
          setTimeout(() => btn.classList.remove('pulse'), 500);
        }
        confirmEl.innerHTML = confirmationText(phase);
        section.classList.add('has-clicked');
      }

      // Load counts from backend on page load
      async function loadCounts() {
        await Promise.all(
          Object.keys(PHASES).map(async (phase) => {
            try {
              const r = await fetch(`${API_BASE}/get/${NAMESPACE}/beweeg-${phase}`);
              if (r.ok) {
                const data = await r.json();
                setCount(phase, data.value || 0);
              } else {
                setCount(phase, 0);
              }
            } catch (e) {
              setCount(phase, 0);
            }
          })
        );
      }

      async function hit(phase) {
        try {
          const r = await fetch(`${API_BASE}/hit/${NAMESPACE}/beweeg-${phase}`);
          if (r.ok) {
            const data = await r.json();
            setCount(phase, data.value);
          } else {
            setCount(phase, currentCount(phase) + 1);
          }
        } catch (e) {
          setCount(phase, currentCount(phase) + 1);
        }
      }

      // Abacus exposes increment but not decrement on the free tier.
      // When a visitor switches choice we correct the display locally so the
      // numbers stay believable, without pretending to be exact research data.
      function decrementLocal(phase) {
        setCount(phase, Math.max(0, currentCount(phase) - 1));
      }

      async function vote(phase) {
        const previous = localStorage.getItem(STORAGE_KEY);

        if (previous === phase) {
          // same choice clicked again: never double-counts
          highlight(phase, false);
          return;
        }

        if (previous && PHASES[previous]) {
          // switching choice: visually move the signal across
          decrementLocal(previous);
        }

        await hit(phase);
        localStorage.setItem(STORAGE_KEY, phase);
        highlight(phase, true);
      }

      buttons.forEach((btn) => {
        btn.addEventListener('click', () => {
          const phase = btn.dataset.phase;
          if (phase) vote(phase);
        });
      });

      // Initialize: load counts, then restore any prior choice
      loadCounts().then(() => {
        const previous = localStorage.getItem(STORAGE_KEY);
        if (previous && PHASES[previous]) {
          highlight(previous, false);
        }
      });
    })();
  </script>
"""

PAGE = """<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Will Switch: digitale autonomie in de praktijk</title>
  <meta name="description" content="Praktijkonderzoek naar digitale autonomie in de publieke sector. Voorbeelden die werken, en wat de overstap van Big Tech naar open alternatieven tegenhoudt.">
  <link rel="canonical" href="{base}/switch.html">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Will Switch">
  <meta property="og:title" content="Will Switch: digitale autonomie in de praktijk">
  <meta property="og:description" content="Praktijkonderzoek naar digitale autonomie in de publieke sector. Voorbeelden die werken, en wat de overstap tegenhoudt.">
  <meta property="og:image" content="{base}/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:url" content="{base}/switch.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Will Switch: digitale autonomie in de praktijk">
  <meta name="twitter:description" content="Praktijkonderzoek naar digitale autonomie in de publieke sector.">
  <meta name="twitter:image" content="{base}/og-image.jpg">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180.png">
  <link rel="preload" href="/fonts/AtkinsonNext.woff2" as="font" type="font/woff2" crossorigin>
  <style>{css}  </style>
</head>
<body>

<header class="top"><div class="w">
  <a class="merk" href="/switch.html"><img src="/wordmark.png" alt="Will Switch" width="705" height="153"><span>Praktijkonderzoek naar<br>digitale autonomie</span></a>
  <nav class="hoofd" aria-label="Hoofdnavigatie"><a class="l" href="#verhalen">Praktijk</a><a class="knop" href="/scan/">Uitstaptoets &rarr;</a></nav>
</div></header>

<section class="hero" role="img" aria-label="Astronaut kijkt uit over een Nederlands landschap, helm in de hand"><div class="w">
  <div class="hero-tekst">
    <div class="hoek">Kun je nog weg bij je leveranciers?</div>
    <h1>Digitale autonomie.<br>Zo werkt het in de praktijk.</h1>
    <p class="sub">Wat publieke organisaties tegenhoudt bij de overstap van Big Tech naar open alternatieven, en wat wel werkt.</p>
    <div class="acties">
      <a class="knop groot" href="/scan/">Doe de uitstaptoets &rarr;</a>
      <span class="meta">15 minuten, geen registratie</span>
    </div>
    <div class="acties" style="margin-top:14px"><a class="tekstlink" href="#verhalen">Bekijk de praktijkverhalen</a></div>
    <div class="hoek drie">Twee wetten. E&eacute;n beleidskader. E&eacute;n toets.</div>
  </div>
</div></section>

<section class="manifest-band"><div class="w manifest">
  <span class="ring" aria-hidden="true"></span><span class="ring klein" aria-hidden="true"></span>
  <p>Het ligt zelden aan de techniek. Het ligt aan wie zich eigenaar voelt.</p>
  <small>Uit 62 stemmen op FOSS4G NL 2026</small>
</div></section>

<section class="w" id="waarom">
  <div class="sectiekop">
    <h2>Actuele wetgeving</h2>
    <p>Let op: het bestuur is sinds 15 augustus 2026 aanspreekbaar op de leveranciersketen. Wie niet kan aantonen wat er gebeurt bij contracteinde of uitval, loopt bestuurlijk risico.</p>
  </div>
  <div class="pijlers">
    <article class="pijler groot">
      <span class="soort wet">Wet</span>
      <div class="moment">Nu</div>
      <h3>Cyberbeveiligingswet</h3>
      <p class="sinds">Van kracht sinds 15 augustus 2026, voor Rijk, zbo's, gemeenten, provincies en waterschappen</p>
      <p class="wat">Per leverancier moet je kunnen aantonen wat er gebeurt bij contracteinde, faillissement of overname. Het bestuur is eindverantwoordelijk, en de toezichthouder kan ernaar vragen.</p>
      <div class="drievragen">
        <b>Drie vragen die je vandaag zou moeten kunnen beantwoorden</b>
        <ol>
          <li>Van welke leveranciers hangt je dienstverlening af, en wanneer lopen die contracten af?</li>
          <li>Wat gebeurt er met je data als zo'n leverancier stopt?</li>
          <li>Wie in het bestuur is daarvoor verantwoordelijk, en is dat formeel vastgesteld?</li>
        </ol>
      </div>
      <div class="voet"><span>De zorgplicht geldt al</span>{link_cbw}</div>
    </article>
    <div class="stapel">
      <article class="pijler">
        <span class="soort eu">EU-verordening</span>
        <div class="moment">12 januari 2027</div>
        <h3>Data Act</h3>
        <p class="sinds">Voor iedere afnemer van clouddiensten</p>
        <p class="wat">Het recht om binnen dertig dagen over te stappen, ook naar eigen infrastructuur. Vanaf die datum vervallen overstapkosten.</p>
        <div class="voet"><span>Ook voor lopende contracten</span>{link_dataact}</div>
      </article>
      <article class="pijler">
        <span class="soort bel">Beleid</span>
        <div class="moment">Medio 2030</div>
        <h3>Rijksbreed cloudbeleid</h3>
        <p class="sinds">Voor rijksorganisaties, met medeoverheden in overleg</p>
        <p class="wat">Een exitplan per clouddienst, ook voor het scenario dat een dienst plotseling wegvalt. Zonder extra budget.</p>
        <div class="voet"><span>Einde overgangstermijn</span>{link_cloudbeleid}</div>
      </article>
    </div>
  </div>
  <div class="cta">
    <span class="ring" aria-hidden="true"></span>
    <div><b>De uitstaptoets toetst alle drie</b><span>In een kwartier weet je waar je staat en wat een logische eerste stap is.</span></div>
    <a class="knop groot" href="/scan/">Doe de uitstaptoets &rarr;</a>
  </div>
</section>

<section class="w" id="verhalen">
  <div class="sectiekop">
    <h2>Van anderen leren</h2>
    <p>Organisaties die de stap zetten, en wat ze onderweg tegenkwamen. Eerlijk over wat werkte en wat niet.</p>
    <a class="tekstlink" href="#overzicht">Alle praktijkverhalen</a>
  </div>
  <div class="verhalen">
    <article class="verhaal groot">
      <div class="beeld"><img src="/dsg-viewer.webp" alt="Kaartviewer van Data Space Groningen" width="1400" height="657" loading="lazy"></div>
      <div class="kicker">Praktijk &middot; Groningen</div>
      <h3>Zeventien organisaties, &eacute;&eacute;n open platform</h3>
      <p>Overheden en waterschappen in Groningen delen hun data via een federatief, open source platform. Van overheden, door overheden. Wat het opleverde, en waar het bijna misging.</p>
      <a class="tekstlink" href="/cases/dsg/">Lees de case</a>
    </article>
    <div class="klein">
      <article class="verhaal">
        <div><div class="kicker">Inzicht</div><h3>Migreer niet alles. Ruim eerst op.</h3><p>Vierhonderd viewers in de lucht, vijftig in gebruik. De grootste valkuil is alles &eacute;&eacute;n-op-&eacute;&eacute;n willen overzetten.</p><a class="tekstlink" href="/cases/wildgroei/">Lees het inzicht</a></div>
      </article>
      <article class="verhaal">
        <div><div class="kicker">Praktijk &middot; SURF</div><h3>SURF is zelf proefkonijn</h3><p>De IT-co&ouml;peratie van het hoger onderwijs zette zijn eigen diensten over naar Nextcloud, om leden te laten zien dat het kan.</p><a class="tekstlink" href="/cases/surf/">Lees de case</a></div>
      </article>
    </div>
  </div>
</section>

<section class="w" id="overzicht">
  <div class="sectiekop">
    <h2>Cases</h2>
    <p>Wetgeving, nieuws, praktijkverhalen en uitspraken</p>
    <span class="meta">{aantal} onderdelen</span>
  </div>
  <div class="overzicht">
{items}
  </div>
</section>

<section class="movement" id="movement">
<span class="ring" aria-hidden="true"></span><span class="ring klein" aria-hidden="true"></span>
<div class="w">
  <h2>Waar staat jouw organisatie vandaag?</h2>
  <p class="sub"><strong>Doe mee.</strong> E&eacute;n klik, geen registratie, geen mailadres. Een teken dat jullie ergens in deze beweging staan.</p>
  <p class="confirm" id="movement-confirm"></p>
  <div class="movement-grid" id="movement-grid">
    <button class="movement-btn" data-phase="verkennen" type="button"><span class="label">We verkennen</span><span class="count" data-count>&middot;</span></button>
    <button class="movement-btn" data-phase="praten" type="button"><span class="label">We praten erover</span><span class="count" data-count>&middot;</span></button>
    <button class="movement-btn" data-phase="pilot" type="button"><span class="label">We draaien een pilot</span><span class="count" data-count>&middot;</span></button>
    <button class="movement-btn" data-phase="overstap" type="button"><span class="label">We stappen over</span><span class="count" data-count>&middot;</span></button>
    <button class="movement-btn" data-phase="verder" type="button"><span class="label">We zijn al verder</span><span class="count" data-count>&middot;</span></button>
  </div>
</div></section>

<div class="w onder">
<section class="blok agenda">
  <h2>Agenda</h2>
  <p class="sub">Meepraten? Kom dan naar:</p>
  <ul>
    <li>
      <div class="when">1 oktober 2026</div>
      <div class="what">
        <a href="https://leiderschapstop.nl/" target="_blank" rel="noopener">LeiderschapsTop Open Source</a>
        <span class="where">Koorkerk, Middelburg &middot; op uitnodiging</span>
      </div>
    </li>
  </ul>
  <p class="sub" style="margin-top:1.6rem">Geweest:</p>
  <ul>
    <li>
      <div class="when">9 juli 2026</div>
      <div class="what">
        <a href="/talk/">Will Switch: help mee de overheid los te weken van Big Tech</a>
        <span class="where">FOSS4G NL, Groningen &middot; 44 deelnemers stemden live mee, het verhaal staat online</span>
      </div>
    </li>
  </ul>
</section>

<div>
<section class="blok credits">
  <h2>Supporters van digitale autonomie</h2>
  <p class="sub">Mensen en organisaties die zich openlijk achter de beweging scharen.</p>
  <ul>
    <li>
      <span class="name">Oskar J. Gstrein</span>
      <span class="context">Rijksuniversiteit Groningen, <a href="https://daix.web.rug.nl/" target="_blank" rel="noopener">Data Autonomy Index</a></span>
    </li>
  </ul>
</section>

<section class="blok initiator">
  <p class="label">Initiatiefnemer</p>
  <p class="name">Govert Schoof</p>
  <p class="desc">Werkt op het snijvlak van overheid, onderzoek, geo-informatie en digitale autonomie.</p>
  <p><a class="tekstlink" href="https://www.linkedin.com/in/govertschoof/" target="_blank" rel="noopener">LinkedIn</a></p>
</section>
</div>
</div>

<footer class="site"><div class="w">
  <span>Will Switch &middot; willswitch.nl &middot; <a href="/">terug naar de switch</a></span>
  <a class="fonds" href="https://www.sidnfonds.nl/" target="_blank" rel="noopener"><span>Onderzoek met steun van</span><img src="/sidnfonds.png" alt="SIDN fonds" width="150" height="28"></a>
</div></footer>
{movement_script}
  <!-- Privacyvriendelijke analytics (GoatCounter, geen cookies) -->
  <script data-goatcounter="https://willswitch.goatcounter.com/count"
          async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def build_switch(cases):
    """Maak switch.html uit de gepubliceerde cases en de quotes.
    De nummering wordt hier geschreven, niet in de browser."""
    ids = [c["id"] for c in cases]
    blokken = []
    n = 0
    for c in cases:
        n += 1
        blokken.append(overzicht_case(n, c))
    for q in load_quotes():
        n += 1
        blokken.append(overzicht_quote(n, q))
    return PAGE.format(
        base=BASE,
        css=CSS,
        link_cbw=case_link(ids, "cbw", "Lees wat het betekent"),
        link_dataact=case_link(ids, "dataact", "Lees meer"),
        link_cloudbeleid=case_link(ids, "cloudbeleid", "Lees meer"),
        aantal=n,
        items="\n\n".join(blokken),
        movement_script=MOVEMENT_SCRIPT,
    )
