from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, email, password):
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def go_to_register(self):
        register_btn = self.driver.find_element(By.XPATH, "//button[text()='Registrati']")
        register_btn.click()
