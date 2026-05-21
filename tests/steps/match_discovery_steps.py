import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

logger = logging.getLogger(__name__)


def open_match_list_page(driver):
    logger.info("Open Match list page")
    driver.find_element(By.XPATH, "//button[.//span[normalize-space()='TennisMatch']]").click()
    assert_match_list_loaded(driver)


def assert_match_list_loaded(driver):
    logger.info("Assert Match list is loaded")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Partite']"))
    )
    WebDriverWait(driver, 10).until_not(
        EC.presence_of_element_located((By.XPATH, "//*[normalize-space()='Caricamento...']"))
    )
    assert_match_list_has_content(driver)


def filter_by_city(driver, city):
    logger.info("Filter matches by city: %s", city)
    city_input = driver.find_element(By.CSS_SELECTOR, "input[role='combobox']")
    city_input.clear()
    city_input.send_keys(city)
    city_input.send_keys(Keys.ENTER)
    city_input.send_keys(Keys.ESCAPE)
    apply_filters(driver)


def filter_by_after(driver, date, time):
    logger.info("Filter matches by start date")
    _set_input_value(driver, "input[type='date']", 0, date)
    _set_input_value(driver, "input[type='time']", 0, time)
    apply_filters(driver)


def filter_by_before(driver, date, time):
    logger.info("Filter matches by end date")
    _set_input_value(driver, "input[type='date']", 1, date)
    _set_input_value(driver, "input[type='time']", 1, time)
    apply_filters(driver)


def filter_by_skill_level(driver, skill_level):
    logger.info("Filter matches by skill level: %s", skill_level)
    Select(driver.find_elements(By.CSS_SELECTOR, "select")[0]).select_by_value(skill_level)
    apply_filters(driver)


def filter_by_match_type(driver, match_type):
    logger.info("Filter matches by match type: %s", match_type)
    Select(driver.find_elements(By.CSS_SELECTOR, "select")[1]).select_by_value(match_type)
    apply_filters(driver)


def filter_by_open_status(driver, status):
    logger.info("Filter matches by open status: %s", status)
    Select(driver.find_elements(By.CSS_SELECTOR, "select")[2]).select_by_value(status)
    apply_filters(driver)


def apply_invalid_date_range(driver):
    logger.info("Apply invalid date range")
    _set_input_value(driver, "input[type='date']", 0, "2030-01-02")
    _set_input_value(driver, "input[type='time']", 0, "10:00")
    _set_input_value(driver, "input[type='date']", 1, "2030-01-01")
    _set_input_value(driver, "input[type='time']", 1, "09:00")
    _click_button(driver, "Applica")


def reset_filters(driver):
    logger.info("Reset match filters")
    _click_button(driver, "Azzera")
    assert_match_list_loaded(driver)


def assert_city_results(driver, city):
    logger.info("Assert city results: %s", city)
    assert_cards_or_empty(driver, lambda cards: [
        _assert_text_contains(card.find_element(By.TAG_NAME, "h3").text, city) for card in cards
    ])


def assert_badge_results(driver, label):
    logger.info("Assert badge results: %s", label)
    assert_cards_or_empty(driver, lambda cards: [
        card.find_element(By.XPATH, f".//span[normalize-space()='{label}']") for card in cards
    ])


def assert_invalid_date_range_error(driver):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[@role='alert' and normalize-space()='La data di fine deve essere successiva alla data di inizio.']",
        ))
    )


def assert_default_filters(driver):
    city_value = driver.find_element(By.CSS_SELECTOR, "input[role='combobox']").get_attribute("value")
    assert city_value
    assert Select(driver.find_elements(By.CSS_SELECTOR, "select")[2]).first_selected_option.get_attribute("value") == "OPEN"
    assert_match_list_has_content(driver)


def apply_filters(driver):
    _click_button(driver, "Applica")
    WebDriverWait(driver, 10).until_not(
        EC.presence_of_element_located((By.XPATH, "//*[normalize-space()='Caricamento...']"))
    )
    assert_match_list_has_content(driver)


def assert_match_list_has_content(driver):
    WebDriverWait(driver, 10).until(
        lambda d: d.find_elements(By.XPATH, "//p[contains(normalize-space(),'match trovati.')]")
        or d.find_elements(By.XPATH, "//p[normalize-space()='Nessuna partita trovata.']")
    )


def assert_cards_or_empty(driver, assert_cards):
    cards = _match_cards(driver)
    if cards:
        assert_cards(cards)
    else:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[normalize-space()='Nessuna partita trovata.']"))
        )


def _match_cards(driver):
    return driver.find_elements(By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),' card ') and .//h3]")


def _set_input_value(driver, selector, index, value):
    driver.execute_script(
        """
        const input = document.querySelectorAll(arguments[0])[arguments[1]];
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(input, arguments[2]);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        """,
        selector,
        index,
        value,
    )


def _click_button(driver, label):
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{label}']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    driver.execute_script("arguments[0].click();", button)


def _assert_text_contains(text, expected):
    assert expected in text
