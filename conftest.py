import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from tests.form_page import PracticeFormPage

URL = os.getenv("BASE_URL", "https://demoqa.com/automation-practice-form")
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


def pytest_addoption(parser):
    parser.addoption("--pause", type=float, default=2.0,
                     help="Sekunden, die der Browser nach jedem Test offen bleibt (Standard: 2)")
    parser.addoption("--headless", action="store_true",
                     help="Browser ohne sichtbares Fenster starten")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Merkt sich das Ergebnis jedes Tests, damit die Fixture es nach dem Test lesen kann."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.test_report = report


@pytest.fixture
def driver(request):
    """Startet für jeden Test einen frischen Chrome-Browser und schließt ihn danach."""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        # nötig in Docker/CI (z. B. GitHub Actions), wo Chrome als root läuft
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Optional: eigener Chrome/Chromedriver-Pfad, sonst lädt Selenium Manager ihn automatisch
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]
    service = Service(os.getenv("CHROMEDRIVER")) if os.getenv("CHROMEDRIVER") else Service()

    drv = webdriver.Chrome(options=options, service=service)
    drv.implicitly_wait(5)
    yield drv

    report = getattr(request.node, "test_report", None)
    if report is not None:
        _show_result(drv, request.node.name, report)
        time.sleep(request.config.getoption("--pause"))
    drv.quit()


def _show_result(drv, test_name, report):
    """Zeigt im Browser ein grünes/rotes Banner und speichert bei Fehlern einen Screenshot."""
    if report.passed:
        _banner(drv, f"✅ BESTANDEN: {test_name}", "", "#2e7d32")
        return

    crash = getattr(report.longrepr, "reprcrash", None)
    message = crash.message.splitlines()[0] if crash else "Unbekannter Fehler"
    _banner(drv, f"❌ FEHLGESCHLAGEN: {test_name}", message, "#c62828")

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    path = SCREENSHOT_DIR / f"{test_name}.png"
    drv.save_screenshot(str(path))
    print(f"\n❌ Test '{test_name}' fehlgeschlagen: {message}\n   Screenshot: {path}")


def _banner(drv, title, detail, color):
    try:
        drv.execute_script(
            """
            const b = document.createElement('div');
            b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;padding:16px;'
                + 'font:bold 20px sans-serif;color:#fff;text-align:center;background:' + arguments[2];
            b.textContent = arguments[0];
            if (arguments[1]) {
                const d = document.createElement('div');
                d.style.fontSize = '15px';
                d.textContent = arguments[1];
                b.appendChild(d);
            }
            document.body.appendChild(b);
            """,
            title, detail, color,
        )
    except Exception:
        pass  # Banner ist nur Deko, darf den Testlauf nie abbrechen


@pytest.fixture
def form_page(driver):
    """Öffnet das Formular und entfernt Werbung, die Klicks blockieren kann."""
    page = PracticeFormPage(driver)
    page.open(URL)
    return page
