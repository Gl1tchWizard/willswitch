"""Haal de cases uit switch.html en schrijf ze weg als losse bronbestanden.

Eenmalig script: na deze migratie zijn de bestanden in content/cases/ de bron.
"""
import re, json, pathlib, html as htmllib

SRC = pathlib.Path("/mnt/user-data/outputs/switch.html")
OUT = pathlib.Path("content/cases")
OUT.mkdir(parents=True, exist_ok=True)

doc = SRC.read_text()

# 1) metadata uit de kaarten in het grid
cards = {}
for m in re.finditer(
    r'<article class="card[^"]*"([^>]*)>(.*?)</article>', doc, re.S):
    attrs, body = m.group(1), m.group(2)
    cid = re.search(r'data-case="([a-z]+)"', attrs)
    if not cid:
        continue
    cid = cid.group(1)
    pub = re.search(r'data-publish-on="([\d-]+)"', attrs)
    since = re.search(r'data-new-since="([\d-]+)"', attrs)
    h3 = re.search(r'<h3>(.*?)</h3>', body, re.S)
    para = re.search(r'<p class="card-body">(.*?)</p>', body, re.S)
    more = re.search(r'<span class="case-more">(.*?)</span>', body, re.S)
    cards[cid] = {
        "id": cid,
        "publish_on": pub.group(1) if pub else None,
        "new_since": since.group(1) if since else None,
        "card_title": htmllib.unescape(h3.group(1).strip()) if h3 else "",
        "card_body": htmllib.unescape(para.group(1).strip()) if para else "",
        "cta": htmllib.unescape(more.group(1).strip()) if more else "Lees de case",
    }

# 2) de volledige inhoud uit de verborgen blokken
for m in re.finditer(
    r'<div class="case-data" id="case-([a-z]+)" hidden>(.*?)\n  </div>', doc, re.S):
    cid, body = m.group(1), m.group(2)
    if cid not in cards:
        cards[cid] = {"id": cid, "publish_on": None, "new_since": None,
                      "card_title": "", "card_body": "", "cta": "Lees de case"}
    eyebrow = re.search(r'<p class="case-eyebrow">(.*?)</p>', body, re.S)
    h2 = re.search(r'<h2>(.*?)</h2>', body, re.S)
    cards[cid]["eyebrow"] = htmllib.unescape(eyebrow.group(1).strip()) if eyebrow else ""
    cards[cid]["title"] = htmllib.unescape(h2.group(1).strip()) if h2 else ""
    # bewaar de body-html zoals hij is, dat is de inhoud van de case
    inner = body
    inner = re.sub(r'<p class="case-eyebrow">.*?</p>\s*', '', inner, flags=re.S)
    inner = re.sub(r'<h2>.*?</h2>\s*', '', inner, flags=re.S)
    cards[cid]["body_html"] = inner.strip()

order = [c for c in re.findall(r'data-case="([a-z]+)"', doc) if c in cards]
seen, ordered = set(), []
for c in order:
    if c not in seen:
        seen.add(c); ordered.append(c)

for i, cid in enumerate(ordered):
    c = cards[cid]
    c["order"] = i
    fm = {k: c[k] for k in
          ("id", "order", "publish_on", "new_since", "eyebrow", "title",
           "card_title", "card_body", "cta")}
    text = "---\n" + json.dumps(fm, ensure_ascii=False, indent=2) + "\n---\n\n" + c["body_html"] + "\n"
    (OUT / f"{cid}.html").write_text(text)

print(f"{len(ordered)} cases weggeschreven:")
for cid in ordered:
    c = cards[cid]
    print(f"  {c['order']:>2}  {cid:<16} {c['publish_on'] or c['new_since'] or '-':<12} {c['title'][:52]}")
