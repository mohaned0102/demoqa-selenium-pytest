"""Tests: E-Mail-Feld (gültige und ungültige Adressen)."""
import pytest

from tests.form_page import PracticeFormPage as P


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
