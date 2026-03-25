import logging
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from tests.selectors.account_selectors import (
    LOGIN_HEADER_XPATH,
    REGISTER_HEADER_XPATH,
    LIST_VIEW_HEADER_XPATH,
    PLAYER_DASHBOARD_BUTTON_XPATH,
    ORGANIZER_DASHBOARD_BUTTON_XPATH,
    ORGANIZER_VIEW_HEADER_XPATH,
    LOGOUT_BUTTON_XPATH,
    error_toast_xpath,
)

logger = logging.getLogger(__name__)
API_BASE = "http://localhost:8080"


def open_login_page(driver, base_url):
    logger.info("Open Login page")
    driver.get(base_url)
    assert_login_page_visible(driver)


def assert_login_page_visible(driver):
    logger.info("Assert Login form is displayed")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, LOGIN_HEADER_XPATH))
    )


def open_register_page(driver, base_url):
    logger.info("Open Register page")
    driver.get(base_url)
    LoginPage(driver).go_to_register()
    assert_register_page_visible(driver)


def assert_register_page_visible(driver):
    logger.info("Assert Register form is displayed")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, REGISTER_HEADER_XPATH))
    )


def register_user(driver, email, password, display_name, city, role):
    logger.info(
        "Fill register form: email=%s display_name=%s city=%s role=%s",
        email,
        display_name,
        city,
        role,
    )
    register_page = RegisterPage(driver)
    register_page.enter_registration_data(
        email=email,
        password=password,
        name=display_name,
        city=city,
        role=role,
    )
    logger.info("Submit registration form")
    register_page.submit()


def login_user(driver, email, password):
    logger.info("Fill login form: email=%s", email)
    login_page = LoginPage(driver)
    login_page.login(email, password)


def assert_list_view_loaded(driver):
    logger.info("Assert LIST view is loaded")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, LIST_VIEW_HEADER_XPATH))
    )


def assert_player_dashboard(driver):
    logger.info("Assert PLAYER dashboard")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, PLAYER_DASHBOARD_BUTTON_XPATH))
    )


def assert_organizer_dashboard(driver):
    logger.info("Assert ORGANIZER dashboard")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ORGANIZER_DASHBOARD_BUTTON_XPATH))
    )


def assert_organizer_view_loaded(driver):
    logger.info("Assert ORGANIZER view is loaded")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ORGANIZER_VIEW_HEADER_XPATH))
    )


def logout_user(driver):
    logger.info("Click Logout")
    driver.find_element(By.XPATH, LOGOUT_BUTTON_XPATH).click()


def assert_error_toast(driver, message):
    logger.info("Assert error toast: %s", message)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, error_toast_xpath(message))
        )
    )


def assert_password_rejected_by_client(driver):
    logger.info("Assert password is invalid according to client validation")
    register_page = RegisterPage(driver)
    assert not register_page.password_is_valid()
    assert register_page.password_validation_message()


def assert_authenticated_user(driver, expected_role, expected_skill_level=None):
    logger.info(
        "Assert authenticated user session: role=%s skill_level=%s",
        expected_role,
        expected_skill_level,
    )
    payload = driver.execute_async_script(
        """
        const callback = arguments[arguments.length - 1];
        fetch(arguments[0], { credentials: 'include' })
          .then(async (response) => {
                let body = null;
                try {
                  body = await response.json();
            } catch (error) {
              body = null;
            }
            callback(JSON.stringify({ status: response.status, body }));
              })
              .catch((error) => callback(JSON.stringify({ error: String(error) })));
        """
        ,
        f"{API_BASE}/api/auth/me"
    )
    data = json.loads(payload)

    assert "error" not in data, data.get("error")
    assert data["status"] == 200
    assert data["body"]["role"] == expected_role
    if expected_skill_level is not None:
        assert data["body"]["skillLevel"] == expected_skill_level
