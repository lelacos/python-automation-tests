from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")
        self.display_name_input = (By.CSS_SELECTOR, "input[type='text']")
        self.city_input = (By.CSS_SELECTOR, "input[role='combobox']")
        self.role_select = (By.TAG_NAME, "select")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_registration_data(self, email, password, name, city, role="PLAYER"):
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.display_name_input).send_keys(name)
        self.driver.find_element(*self.city_input).send_keys(city + Keys.ENTER)
        select = Select(self.driver.find_element(*self.role_select))
        select.select_by_value(role)

    def submit(self):
        self.driver.find_element(*self.submit_button).click()

    def password_is_valid(self):
        field = self.driver.find_element(*self.password_input)
        return self.driver.execute_script("return arguments[0].checkValidity();", field)

    def password_validation_message(self):
        field = self.driver.find_element(*self.password_input)
        return self.driver.execute_script("return arguments[0].validationMessage;", field)
