from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PracticeFormPage:
    FIRST_NAME = (By.ID, "firstName")
    LAST_NAME = (By.ID, "lastName")
    EMAIL = (By.ID, "userEmail")
    MOBILE = (By.ID, "userNumber")
    GENDER_MALE = (By.CSS_SELECTOR, "label[for='gender-radio-1']")
    SUBMIT = (By.ID, "submit")
    MODAL_TITLE = (By.ID, "example-modal-sizes-title-lg")
    RESULT_ROWS = (By.CSS_SELECTOR, ".modal-body table tbody tr")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        # Werbebanner/Footer überdecken oft den Submit-Button
        self.driver.execute_script(
            "document.querySelectorAll('#fixedban, footer, iframe').forEach(e => e.remove());"
        )

    def find(self, locator):
        return self.driver.find_element(*locator)

    def type(self, locator, text):
        field = self.find(locator)
        field.clear()
        field.send_keys(text)
        return field

    def click(self, locator):
        # JS-Klick, damit überlappende Elemente den Klick nicht abfangen
        self.driver.execute_script("arguments[0].click();", self.find(locator))

    def is_valid(self, locator):
        """HTML5-Validierung des Browsers abfragen (required, pattern, minlength ...)."""
        return self.driver.execute_script("return arguments[0].checkValidity();", self.find(locator))

    def submit(self):
        self.click(self.SUBMIT)

    def fill_required(self, first="Max", last="Mustermann", mobile="0123456789", email=None):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        if email is not None:
            self.type(self.EMAIL, email)
        self.click(self.GENDER_MALE)
        self.type(self.MOBILE, mobile)

    def modal_is_shown(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.MODAL_TITLE))
            return True
        except Exception:
            return False

    def result_table(self):
        """Ergebnis-Tabelle im Modal als dict: {'Student Name': 'Max Mustermann', ...}"""
        rows = self.driver.find_elements(*self.RESULT_ROWS)
        result = {}
        for row in rows:
            label, value = row.find_elements(By.TAG_NAME, "td")
            result[label.text] = value.text
        return result
