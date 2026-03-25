from tests.steps.account_steps import (
    open_login_page,
    open_register_page,
    login_user,
    logout_user,
    register_user,
    assert_login_page_visible,
    assert_player_dashboard,
    assert_organizer_dashboard,
    assert_list_view_loaded,
    assert_organizer_view_loaded,
    assert_error_toast,
    assert_register_page_visible,
    assert_password_rejected_by_client,
    assert_authenticated_user,
)
from tests.data.account_factory import build_account, unique_suffix


def test_register_player_success(driver, base_url):
    open_register_page(driver, base_url)

    account = build_account(role="PLAYER", prefix="new_player", city="Cagliari")

    register_user(
        driver=driver,
        email=account["email"],
        password=account["password"],
        display_name=account["display_name"],
        city=account["city"],
        role=account["role"],
    )

    assert_player_dashboard(driver)
    assert_authenticated_user(driver, expected_role="PLAYER", expected_skill_level="INTERMEDIATE")


def test_register_organizer_success(driver, base_url):
    open_register_page(driver, base_url)

    account = build_account(role="ORGANIZER", prefix="new_org", city="Milano")

    register_user(
        driver=driver,
        email=account["email"],
        password=account["password"],
        display_name=account["display_name"],
        city=account["city"],
        role=account["role"],
    )

    assert_organizer_dashboard(driver)
    assert_authenticated_user(driver, expected_role="ORGANIZER")


def test_register_existing_email_fails(driver, base_url):
    open_register_page(driver, base_url)

    email = "player@test.it"
    password = "secret1"
    display_name = f"UniqueName{unique_suffix()}"
    city = "Cagliari"

    register_user(
        driver=driver,
        email=email,
        password=password,
        display_name=display_name,
        city=city,
        role="PLAYER",
    )

    assert_error_toast(driver, "Email gi\u00e0 in uso")


def test_register_existing_display_name_fails(driver, base_url):
    open_register_page(driver, base_url)

    email = f"unique_email_{unique_suffix()}@test.it"
    password = "secret1"
    display_name = "Player Demo"
    city = "Cagliari"

    register_user(
        driver=driver,
        email=email,
        password=password,
        display_name=display_name,
        city=city,
        role="PLAYER",
    )

    assert_error_toast(driver, "Display name gi\u00e0 in uso")


def test_register_short_password_is_rejected(driver, base_url):
    open_register_page(driver, base_url)

    email = f"shortpwd_{unique_suffix()}@test.it"
    password = "12345"
    display_name = f"ShortPwd{unique_suffix()}"
    city = "Cagliari"

    register_user(
        driver=driver,
        email=email,
        password=password,
        display_name=display_name,
        city=city,
        role="PLAYER",
    )

    assert_password_rejected_by_client(driver)
    assert_register_page_visible(driver)


def test_valid_player_login(driver, base_url):
    open_login_page(driver, base_url)

    email = "player@test.it"
    password = "password"

    assert_login_page_visible(driver)
    login_user(driver, email=email, password=password)

    assert_list_view_loaded(driver)


def test_valid_organizer_login(driver, base_url):
    open_login_page(driver, base_url)

    email = "organizer@test.it"
    password = "password"

    assert_login_page_visible(driver)
    login_user(driver, email=email, password=password)

    assert_organizer_view_loaded(driver)


def test_login_with_wrong_credentials_fails(driver, base_url):
    open_login_page(driver, base_url)

    email = "player@test.it"
    password = "wrongpass"

    assert_login_page_visible(driver)
    login_user(driver, email=email, password=password)

    assert_error_toast(driver, "Credenziali non valide")
    assert_login_page_visible(driver)


def test_logout_returns_user_to_login_page(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="player@test.it", password="password")

    assert_list_view_loaded(driver)
    logout_user(driver)

    assert_login_page_visible(driver)


def test_player_session_persists_after_refresh(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="player@test.it", password="password")

    assert_list_view_loaded(driver)
    driver.refresh()

    assert_list_view_loaded(driver)


def test_organizer_session_persists_after_refresh(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="organizer@test.it", password="password")

    assert_organizer_view_loaded(driver)
    driver.refresh()

    assert_organizer_view_loaded(driver)
