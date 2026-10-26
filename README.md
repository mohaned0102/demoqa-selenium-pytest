# DemoQA Practice Form: UI-Tests mit pytest und Selenium

![Tests](https://github.com/mohaned0102/selenuim-form-testing/actions/workflows/tests.yml/badge.svg)

Übungsprojekt zur Testautomatisierung, entstanden neben meinem Informatikstudium an der TU Dortmund: End-to-End-Tests für das Formular auf [demoqa.com/automation-practice-form](https://demoqa.com/automation-practice-form). Die Tests laufen lokal und bei jedem Push automatisch in GitHub Actions.

**Technologien:** Python · pytest · Selenium WebDriver · pytest-html · GitHub Actions

## Was getestet wird

| Bereich | Tests |
|---|---|
| Website | Seite lädt, URL stimmt, alle Felder sind sichtbar |
| Vor- und Nachname | Eingabe wird übernommen, leeres Pflichtfeld ist ungültig |
| E-Mail | gültige Adressen werden akzeptiert, ungültige (`mohaned`, `@`, `ahmed@example` …) abgelehnt |
| Handynummer | 10 Ziffern sind gültig, zu kurze Nummern und Buchstaben sind ungültig, maximal 10 Zeichen, Pflichtfeld |
| Absenden | vollständiges Formular öffnet das Bestätigungs-Modal mit den richtigen Daten |
| Absenden (ungültig) | bei unvollständigem Formular erscheint kein Modal |

## Projektstruktur

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

Für die Struktur nutze ich das Page Object Pattern. Alle Locators und Aktionen stehen in `form_page.py`. Wenn sich die Seite ändert, muss ich nur diese Datei anpassen und nicht jeden einzelnen Test.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Chrome muss installiert sein. Den passenden ChromeDriver lädt Selenium automatisch.

## Tests ausführen

```bash
pytest                       # Browser sichtbar, bleibt nach jedem Test 2 s offen
pytest --pause 5             # 5 Sekunden Pause nach jedem Test (gut für Demos)
pytest --pause 0             # ohne Pause
pytest --headless            # ohne Browserfenster
pytest tests/test_email.py   # nur eine Testdatei
pytest -k invalid            # nur Tests, deren Name "invalid" enthält
```

Einen HTML-Testbericht erzeugt man so:

```bash
pytest --html=report.html --self-contained-html
```

## Testergebnisse

Wenn ein Test besteht, erscheint oben im Browser ein grünes Banner. Schlägt er fehl, zeigt der Browser ein rotes Banner mit der Fehlermeldung. Im Terminal steht dann eine verständliche Meldung, zum Beispiel `Ungültige E-Mail 'max@' wird akzeptiert`, und unter `screenshots/<testname>.png` wird ein Screenshot gespeichert.

## CI-Pipeline

Bei jedem Push auf `main` und bei jedem Pull Request führt GitHub Actions diese Schritte aus:

1. Code auschecken
2. Python 3.12 und die Abhängigkeiten installieren
3. Alle Tests headless ausführen (`pytest --headless --pause 0`)
4. HTML-Bericht und Screenshots als Artefakt speichern, auch wenn Tests fehlschlagen

Dadurch kann ich einen fehlgeschlagenen Lauf analysieren, ohne die Tests neu zu starten: unter Actions den Run öffnen und bei Artifacts `test-report` herunterladen.

## Herausforderungen

- **Versteckte Radio-Buttons:** Bei der Auswahl des Geschlechts ist das eigentliche `<input>` versteckt, geklickt wird auf das `<label>`. Für die Validierung mit `checkValidity()` braucht man aber das `<input>`. Deshalb verwende ich zwei Locators: einen zum Klicken und einen zum Prüfen.
- **Änderung auf der Website:** Ein Test schlug plötzlich fehl, weil demoqa.com den Seitentitel geändert hatte. Ich habe geprüft, ob das ein Fehler oder eine gewollte Änderung ist, und den Test auf ein stabileres Merkmal umgestellt, nämlich die URL statt des Titels.

## Was ich dabei geübt habe

In diesem Projekt habe ich geübt, UI-Tests mit pytest zu strukturieren und Selenium für Browser-Tests einzusetzen. Neben den positiven Fällen teste ich auch ungültige Eingaben, zum Beispiel E-Mail-Adressen ohne Domain oder Handynummern mit Buchstaben, weil ein Formular falsche Eingaben genauso zuverlässig behandeln muss wie richtige.

Mit dem Page Object Pattern habe ich Testlogik und Locators getrennt. Über GitHub Actions laufen die Tests automatisch headless, und Bericht und Screenshots stehen nach jedem Lauf als Artefakt bereit.