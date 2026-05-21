import json
import logging
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
API_BASE = "http://localhost:8080"


def open_profile_page(driver):
    logger.info("Open Profile page")
    profile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Profilo']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", profile_button)
    driver.execute_script("arguments[0].click();", profile_button)
    assert_profile_page_visible(driver)


def assert_profile_page_visible(driver):
    logger.info("Assert Profile page is displayed")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(normalize-space(),'Profilo di')]"))
    )


def assert_profile_identity(driver, email, role, skill_level=None):
    logger.info("Assert profile identity: email=%s role=%s", email, role)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, f"//*[contains(normalize-space(),'{email}')]"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(),'Nome utente:') or contains(normalize-space(),'Nome struttura:')]"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(),'Citta:')]"))
    )
    role_row = driver.find_element(By.XPATH, "//p[contains(normalize-space(),'Ruolo:')]")
    assert role in role_row.text
    if skill_level is not None:
        level_row = driver.find_element(By.XPATH, "//p[contains(normalize-space(),'Livello:')]")
        assert skill_level in level_row.text
    else:
        assert len(driver.find_elements(By.XPATH, "//p[contains(normalize-space(),'Livello:')]")) == 0


def open_profile_editor(driver):
    logger.info("Open Profile editor")
    driver.find_element(By.XPATH, "//button[normalize-space()='Modifica profilo']").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Salva modifiche']"))
    )


def update_profile(driver, email, display_name, city):
    logger.info("Update profile data")
    _field(driver, "Email").clear()
    _field(driver, "Email").send_keys(email)
    display_input = _field(driver, "Nome utente")
    display_input.clear()
    display_input.send_keys(display_name)
    _field(driver, "Citta").clear()
    _field(driver, "Citta").send_keys(city)
    driver.find_element(By.XPATH, "//button[normalize-space()='Salva modifiche']").click()
    _wait_for_current_user_value(driver, "email", email)


def update_skill_level(driver, skill_level):
    logger.info("Update skill level: %s", skill_level)
    Select(driver.find_element(By.XPATH, "//label[normalize-space()='Livello']/following-sibling::select")).select_by_value(skill_level)
    driver.find_element(By.XPATH, "//button[normalize-space()='Salva modifiche']").click()
    _wait_for_current_user_value(driver, "skillLevel", skill_level)


def change_password(driver, current_password, new_password):
    logger.info("Change profile password")
    _field(driver, "Password attuale").clear()
    _field(driver, "Password attuale").send_keys(current_password)
    _field(driver, "Nuova password").clear()
    _field(driver, "Nuova password").send_keys(new_password)
    driver.find_element(By.XPATH, "//button[normalize-space()='Salva modifiche']").click()


def assert_success_toast(driver, message):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[role='alert']"), message)
    )


def assert_error_toast(driver, message):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "[role='alert']"), message)
    )


def assert_current_user(driver, expected):
    logger.info("Assert current user: %s", expected)
    payload = driver.execute_async_script(
        """
        const callback = arguments[arguments.length - 1];
        fetch(arguments[0], { credentials: 'include' })
          .then(async (response) => callback(JSON.stringify({ status: response.status, body: await response.json() })))
          .catch((error) => callback(JSON.stringify({ error: String(error) })));
        """,
        f"{API_BASE}/api/auth/me"
    )
    data = json.loads(payload)

    assert "error" not in data, data.get("error")
    assert data["status"] == 200
    body = data["body"]
    for key, value in expected.items():
        if key == "imageUrl":
            if value:
                assert body.get("imageUrl")
            else:
                assert not body.get("imageUrl")
        else:
            assert body[key] == value


def attempt_organizer_skill_level_update(driver):
    logger.info("Attempt organizer skill level update")
    payload = driver.execute_async_script(
        """
        const callback = arguments[arguments.length - 1];
        fetch(arguments[0], {
          method: 'PUT',
          credentials: 'include',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ skillLevel: 'INTERMEDIATE' })
        }).then(async (response) => callback(JSON.stringify({ status: response.status, text: await response.text() })))
          .catch((error) => callback(JSON.stringify({ error: String(error) })));
        """,
        f"{API_BASE}/api/users/me"
    )
    data = json.loads(payload)

    assert "error" not in data, data.get("error")
    assert data["status"] == 400
    assert "skill level" in data["text"]


def upload_valid_profile_image(driver):
    logger.info("Upload valid profile image")
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(_fixture("profile.svg"))
    WebDriverWait(driver, 10).until(lambda d: _current_user(d).get("imageUrl"))
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "img[src*='/uploads/']"))
    )


def upload_invalid_profile_file(driver):
    logger.info("Upload invalid profile file")
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(_fixture("profile.txt"))
    assert_error_toast(driver, "Seleziona un'immagine valida.")
    assert_current_user(driver, {"imageUrl": False})


def assert_reviews_section(driver):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(normalize-space(),'Dicono di te')]"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(),'Rating medio:')]"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(),'Da:')]"))
    )
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(),'Ottima partita!') or contains(normalize-space(),'Match equilibrato e divertente.')]"))
    )


def assert_pending_reviews_section(driver):
    header = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[normalize-space()='Recensioni da lasciare']"))
    )
    section = header.find_element(By.XPATH, "./ancestor::div[contains(@class,'card')][1]")
    section.find_element(By.XPATH, ".//button[normalize-space()='Apri partita']").click()
    review_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Scrivi una recensione']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", review_button)
    driver.execute_script("arguments[0].click();", review_button)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(),'Nuova recensione')]"))
    )


def logout_from_profile(driver):
    driver.find_element(By.XPATH, "//button[normalize-space()='Logout']").click()


def _field(driver, label):
    return driver.find_element(By.XPATH, f"//label[normalize-space()='{label}']/following-sibling::input")


def _fixture(name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fixtures", name))


def _current_user(driver):
    payload = driver.execute_async_script(
        """
        const callback = arguments[arguments.length - 1];
        fetch(arguments[0], { credentials: 'include' })
          .then(async (response) => callback(JSON.stringify(await response.json())))
          .catch((error) => callback(JSON.stringify({ error: String(error) })));
        """,
        f"{API_BASE}/api/auth/me"
    )
    return json.loads(payload)


def _wait_for_current_user_value(driver, key, value):
    WebDriverWait(driver, 10).until(lambda d: _current_user(d).get(key) == value)
