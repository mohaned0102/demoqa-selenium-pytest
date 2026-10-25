"""Tests: Website lädt und alle Felder sind sichtbar."""
from tests.form_page import PracticeFormPage as P


def test_website_loads(form_page):
    driver = form_page.driver
    assert "automation-practice-form" in driver.current_url, f"Falsche URL: {driver.current_url}"
    assert "DEMOQA" in driver.title.upper(), f"Unerwarteter Seitentitel: '{driver.title}'"
    assert "Practice Form" in driver.page_source, "Überschrift 'Practice Form' nicht gefunden"
    for locator in (P.FIRST_NAME, P.LAST_NAME, P.EMAIL, P.MOBILE, P.SUBMIT):
        assert form_page.find(locator).is_displayed(), f"Element {locator[1]} ist nicht sichtbar"
