# DemoQA Practice Form – UI-Tests mit pytest + Selenium

![Tests](https://github.com/mohaned0102/selenuim-form-testing/actions/workflows/tests.yml/badge.svg)

Automatisierte End-to-End-Tests für das Formular auf
[demoqa.com/automation-practice-form](https://demoqa.com/automation-practice-form).
Die Tests laufen lokal und bei jedem Push automatisch in einer GitHub-Actions-Pipeline.

**Technologien:** Python · pytest · Selenium WebDriver · pytest-html · GitHub Actions

## Was wird getestet?
| Bereich | Tests |
|---|---|
| Website | Seite lädt, Titel, alle Felder sichtbar |
| Vor-/Nachname | Eingabe wird übernommen, Pflichtfeld (leer → ungültig) |
| E-Mail | gültige Adressen akzeptiert, ungültige (`mohaned`, `@`, `ahmed@example` …) abgelehnt |
| Handynummer | 10 Ziffern gültig, zu kurz / Buchstaben ungültig, max. 10 Zeichen, Pflichtfeld |
| Absenden | vollständiges Formular → Bestätigungs-Modal mit richtigen Daten |
| Absenden (ungültig) | unvollständiges Formular → kein Modal |

## Aufbau
```
.github/workflows/
└── tests.yml               CI-Pipeline (GitHub Actions)
conftest.py                 Browser-Setup, Ergebnis-Banner, Screenshots bei Fehlern
pytest.ini                  pytest-Konfiguration
requirements.txt            Abhängigkeiten
tests/
├── form_page.py            Page Object: Locators und Aktionen auf dem Formular
├── test_website.py         Website lädt, Felder sichtbar
├── test_name.py            Vor- und Nachname
├── test_email.py           E-Mail
├── test_mobile.py          Handynummer
├── test_submit.py          vollständiges Formular absenden
└── test_submit_invalid.py  unvollständiges Formular absenden
```

**Page Object Pattern:** Alle Locators und Aktionen liegen in `form_page.py`.
Ändert sich die Seite, muss nur diese eine Datei angepasst werden, nicht jeder Test.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Chrome muss installiert sein. Den passenden ChromeDriver lädt Selenium automatisch.

## Ausführen
```bash
pytest                       # Browser sichtbar, bleibt nach jedem Test 2 s offen
pytest --pause 5             # 5 Sekunden Pause nach jedem Test (gut für Demos)
pytest --pause 0             # ohne Pause
pytest --headless            # ohne Browserfenster
pytest tests/test_email.py   # nur eine Testdatei
pytest -k invalid            # nur Tests, deren Name "invalid" enthält
```

HTML-Testbericht erzeugen:
```bash
pytest --html=report.html --self-contained-html
```

## Ergebnis eines Tests
- **Bestanden:** grünes Banner oben im Browser.
- **Fehlgeschlagen:** rotes Banner mit der Fehlermeldung im Browser, klare Meldung im
  Terminal (z. B. `Ungültige E-Mail 'max@' wird akzeptiert`) und ein Screenshot in
  `screenshots/<testname>.png`.

## CI-Pipeline
Bei jedem Push auf `main` und bei jedem Pull Request führt GitHub Actions automatisch aus:

1. Code auschecken
2. Python 3.12 und Abhängigkeiten installieren
3. Alle Tests headless ausführen (`pytest --headless --pause 0`)
4. HTML-Bericht und Screenshots als **Artefakt** speichern, auch wenn Tests fehlschlagen

So lassen sich fehlgeschlagene Läufe analysieren, ohne die Tests erneut auszuführen:
**Actions** → Run auswählen → **Artifacts** → `test-report`.