"""Maakt de deploy-zip uit dist/ met forward slashes (Compress-Archive in PowerShell 5.1 gebruikt backslashes,
en daar struikelt het uitpakken in Plesk over). Draai eerst tools/build.py.

    python tools/maakzip.py            -> C:/Users/<jij>/Downloads/willswitch-live.zip
"""
import pathlib, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
ZIP = pathlib.Path.home() / "Downloads" / "willswitch-live.zip"

bestanden = sorted(p for p in DIST.rglob("*") if p.is_file())
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for p in bestanden:
        z.write(p, p.relative_to(DIST).as_posix())
namen = zipfile.ZipFile(ZIP).namelist()
assert len(namen) == len(bestanden) and not any("\\" in n for n in namen)
print(f"{ZIP}: {len(namen)} bestanden, gelijk aan dist/")
