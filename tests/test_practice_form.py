"""Tests für das DemoQA Practice Form: Website, Vor-/Nachname, E-Mail, Handynummer."""
import pytest

from tests.form_page import PracticeFormPage as P


# ---------- 1. Website ----------

def test_website_loads(form_page):
    driver = form_page.driver
    assert "automation-practice-form" in driver.current_url, f"Falsche URL: {driver.current_url}"
    assert "DEMOQA" in driver.title.upper(), f"Unerwarteter Seitentitel: '{driver.title}'"
    assert "Practice Form" in driver.page_source, "Überschrift 'Practice Form' nicht gefunden"
    for locator in (P.FIRST_NAME, P.LAST_NAME, P.EMAIL, P.MOBILE, P.SUBMIT):
        assert form_page.find(locator).is_displayed(), f"Element {locator[1]} ist nicht sichtbar"


# ---------- 2. Vorname & Nachname ----------

def test_name_fields_accept_input(form_page):
    form_page.type(P.FIRST_NAME, "Max")
    form_page.type(P.LAST_NAME, "Mustermann")

    first = form_page.find(P.FIRST_NAME).get_attribute("value")
    last = form_page.find(P.LAST_NAME).get_attribute("value")
    assert first == "Max", f"Vorname: erwartet 'Max', bekommen '{first}'"
    assert last == "Mustermann", f"Nachname: erwartet 'Mustermann', bekommen '{last}'"
    assert form_page.is_valid(P.FIRST_NAME), "Gültiger Vorname wird als ungültig markiert"
    assert form_page.is_valid(P.LAST_NAME), "Gültiger Nachname wird als ungültig markiert"


@pytest.mark.parametrize("field", [P.FIRST_NAME, P.LAST_NAME], ids=["vorname", "nachname"])
def test_name_is_required(form_page, field):
    form_page.fill_required()
    form_page.find(field).clear()
    form_page.submit()
    assert not form_page.is_valid(field), f"Leeres Feld {field[1]} wird als gültig akzeptiert"
    assert not form_page.modal_is_shown(timeout=2), "Formular wurde trotz leerem Pflichtfeld abgeschickt"


# ---------- 3. E-Mail ----------

@pytest.mark.parametrize("email", ["max@example.com", "max.mustermann@tu-dortmund.de"])
def test_valid_email(form_page, email):
    form_page.type(P.EMAIL, email)
    assert form_page.is_valid(P.EMAIL), f"Gültige E-Mail '{email}' wird abgelehnt"


@pytest.mark.parametrize("email", ["max", "max@", "max@example", "@example.com", "max example@mail.com"])
def test_invalid_email(form_page, email):
    form_page.fill_required(email=email)
    form_page.submit()
    assert not form_page.is_valid(P.EMAIL), f"Ungültige E-Mail '{email}' wird akzeptiert"
    assert not form_page.modal_is_shown(timeout=2), f"Formular wurde mit E-Mail '{email}' abgeschickt"


# ---------- 4. Handynummer ----------

def test_valid_mobile(form_page):
    form_page.type(P.MOBILE, "0123456789")
    assert form_page.is_valid(P.MOBILE), "Gültige Nummer '0123456789' wird abgelehnt"


@pytest.mark.parametrize("mobile", ["12345", "abcdefghij", "01234abcde"])
def test_invalid_mobile(form_page, mobile):
    form_page.fill_required(mobile=mobile)
    form_page.submit()
    assert not form_page.is_valid(P.MOBILE), f"Ungültige Handynummer '{mobile}' wird akzeptiert"
    assert not form_page.modal_is_shown(timeout=2), f"Formular wurde mit Nummer '{mobile}' abgeschickt"


def test_mobile_max_10_digits(form_page):
    value = form_page.type(P.MOBILE, "012345678999").get_attribute("value")
    assert value == "0123456789", f"Feld sollte auf 10 Ziffern begrenzt sein, enthält aber '{value}'"


def test_mobile_is_required(form_page):
    form_page.fill_required()
    form_page.find(P.MOBILE).clear()
    form_page.submit()
    assert not form_page.is_valid(P.MOBILE), "Leere Handynummer wird als gültig akzeptiert"


# ---------- 5. Komplettes Formular absenden ----------

def test_submit_form_successfully(form_page):
    form_page.fill_required(first="Max", last="Mustermann", email="max@example.com", mobile="0123456789")
    form_page.submit()

    assert form_page.modal_is_shown(), "Bestätigungsfenster erscheint nicht nach dem Absenden"
    title = form_page.find(P.MODAL_TITLE).text
    assert title == "Thanks for submitting the form", f"Unerwarteter Titel im Modal: '{title}'"

    result = form_page.result_table()
    expected = {
        "Student Name": "Max Mustermann",
        "Student Email": "max@example.com",
        "Mobile": "0123456789",
        "Gender": "Male",
    }
    for key, value in expected.items():
        assert result.get(key) == value, f"{key}: erwartet '{value}', bekommen '{result.get(key)}'"
