"""Tests: Vorname und Nachname (Eingabe, Pflichtfeld)."""
import pytest

from tests.form_page import PracticeFormPage as P


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
