"""Test: komplettes Formular absenden und Bestätigung prüfen."""
from tests.form_page import PracticeFormPage as P


def test_submit_form_successfully(form_page):
    form_page.fill_required(first="mohaned", last="ouni", email="mohaned.ouni@tu-dortmund.de", mobile="0123456789")
    form_page.submit()

    assert form_page.modal_is_shown(), "Bestätigungsfenster erscheint nicht nach dem Absenden"
    title = form_page.find(P.MODAL_TITLE).text
    assert title == "Thanks for submitting the form", f"Unerwarteter Titel im Modal: '{title}'"

    result = form_page.result_table()
    expected = {
        "Student Name": "Mohaned ouni",
        "Student Email": "mohaned.ouni@tu-dortmund.de",
        "Mobile": "0123456789",
        "Gender": "Male",
    }
    for key, value in expected.items():
        assert result.get(key) == value, f"{key}: erwartet '{value}', bekommen '{result.get(key)}'"
