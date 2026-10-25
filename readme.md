# DemoQA Practice Form – UI-Tests mit pytest + Selenium

Automatisierte End-to-End-Tests für das Formular auf
https://demoqa.com/automation-practice-form.

## Was wird getestet?
| Bereich | Tests |
|---|---|
| Website | Seite lädt, Titel, alle Felder sichtbar |
| Vor-/Nachname | Eingabe wird übernommen, Pflichtfeld (leer → ungültig) |
| E-Mail | gültige Adressen akzeptiert, ungültige (`max`, `max@`, `max@example` …) abgelehnt |
| Handynummer | 10 Ziffern gültig, zu kurz / Buchstaben ungültig, max. 10 Zeichen, Pflichtfeld |
| Absenden | komplettes Formular → Bestätigungs-Modal mit richtigen Daten |

## Aufbau
```
conftest.py               Browser-Setup, Ergebnis-Banner, Screenshots bei Fehlern
tests/form_page.py        Page Object: Locators + Aktionen auf dem Formular
tests/test_practice_form.py   die eigentlichen Testfälle
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Chrome muss installiert sein. Den passenden ChromeDriver lädt Selenium automatisch.

## Ausführen
```bash
pytest                    # Browser sichtbar, bleibt nach jedem Test 2 s offen
pytest --pause 5          # 5 Sekunden Pause nach jedem Test (gut für Demos)
pytest --pause 0          # ohne Pause
pytest --headless         # ohne Browserfenster
pytest -k email           # nur die E-Mail-Tests
```

## Ergebnis eines Tests
- **Bestanden:** grünes Banner oben im Browser.
- **Fehlgeschlagen:** rotes Banner mit der Fehlermeldung im Browser, klare Meldung im
  Terminal (z. B. `Ungültige E-Mail 'max@' wird akzeptiert`) und ein Screenshot in
  `screenshots/<testname>.png`.
