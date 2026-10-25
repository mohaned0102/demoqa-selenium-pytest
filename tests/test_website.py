"""Tests: Website lädt und alle Felder sind sichtbar."""
from tests.form_page import PracticeFormPage as P


def test_website_loads(form_page):
    driver = form_page.driver
    assert "demoqa.com" in driver.current_url, f"Falsche Domain: {driver.current_url}"
    for locator in (P.FIRST_NAME, P.LAST_NAME, P.EMAIL, P.MOBILE, P.SUBMIT):
        assert form_page.find(locator).is_displayed(), f"Element {locator[1]} ist nicht sichtbar"
