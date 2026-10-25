"""Tests: ungültiges Formular absenden → Formular darf NICHT abgeschickt werden."""
import pytest

from tests.form_page import PracticeFormPage as P


def test_submit_empty_form(form_page):
    form_page.submit()

    assert not form_page.modal_is_shown(timeout=2), "Leeres Formular wurde abgeschickt"
    for field in (P.FIRST_NAME, P.LAST_NAME, P.MOBILE):
        assert not form_page.is_valid(field), f"Leeres Pflichtfeld {field[1]} wird als gültig akzeptiert"


def test_submit_without_gender(form_page):
    form_page.type(P.FIRST_NAME, "Max")
    form_page.type(P.LAST_NAME, "Mustermann")
    form_page.type(P.MOBILE, "0123456789")
    form_page.submit()

    assert not form_page.is_valid(P.GENDER_MALE_INPUT), "Fehlendes Geschlecht wird als gültig akzeptiert"
    assert not form_page.modal_is_shown(timeout=2), "Formular wurde ohne Geschlecht abgeschickt"


@pytest.mark.parametrize(
    "data",
    [
        {"first": ""},
        {"last": ""},
        {"email": "max@"},
        {"mobile": "12345"},
        {"mobile": "abcdefghij"},
    ],
    ids=["ohne-vorname", "ohne-nachname", "falsche-email", "nummer-zu-kurz", "nummer-buchstaben"],
)
def test_submit_with_invalid_data(form_page, data):
    form_page.fill_required(**data)
    form_page.submit()

    assert not form_page.modal_is_shown(timeout=10), f"Formular wurde mit ungültigen Daten {data} abgeschickt"
