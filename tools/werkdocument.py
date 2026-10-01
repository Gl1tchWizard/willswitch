"""Zet het voorbeeld-werkdocument om naar DOCX en ODT, met LibreOffice.

Bron:  content/werkdocument/ravensmeer.html
Uit:   site/rapport/werkdocument-ravensmeer.docx en .odt (build.py zet ze in dist/rapport/)

Draai dit na een wijziging in de bron:  python tools/werkdocument.py
Vereist LibreOffice. De uitkomst staat in git, dus de gewone build heeft LibreOffice niet nodig.
"""
import pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRON = ROOT / "content" / "werkdocument" / "ravensmeer.html"
UIT = ROOT / "site" / "rapport"
NAAM = "werkdocument-ravensmeer"
FORMATEN = {"docx": "docx:MS Word 2007 XML", "odt": "odt:writer8"}


def soffice():
    for kandidaat in (shutil.which("soffice"), r"C:\Program Files\LibreOffice\program\soffice.exe",
                      "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if kandidaat and pathlib.Path(kandidaat).exists():
            return kandidaat
    sys.exit("LibreOffice (soffice) niet gevonden.")


def main():
    exe = soffice()
    with tempfile.TemporaryDirectory() as tmp:
        profiel = pathlib.Path(tmp, "profiel").as_uri()   # eigen profiel: werkt ook als LibreOffice al openstaat
        for ext, filter_ in FORMATEN.items():
            subprocess.run([exe, f"-env:UserInstallation={profiel}", "--headless",
                            "--infilter=HTML (StarWriter)", "--convert-to", filter_,
                            "--outdir", tmp, str(BRON)], check=True, capture_output=True)
            shutil.copy(pathlib.Path(tmp, f"{BRON.stem}.{ext}"), UIT / f"{NAAM}.{ext}")
            print(f"  {NAAM}.{ext}")


if __name__ == "__main__":
    main()
