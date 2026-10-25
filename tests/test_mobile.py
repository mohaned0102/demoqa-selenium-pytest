"""Tests: Handynummer (10 Ziffern, ungültige Eingaben, Pflichtfeld)."""
import pytest

from tests.form_page import PracticeFormPage as P


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
