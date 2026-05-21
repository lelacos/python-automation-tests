from tests.data.account_factory import build_account, unique_suffix
from tests.steps.account_steps import (
    assert_login_page_visible,
    assert_organizer_view_loaded,
    login_user,
    open_login_page,
    open_register_page,
    register_user,
)
from tests.steps.profile_steps import (
    assert_current_user,
    assert_error_toast,
    assert_pending_reviews_section,
    assert_profile_identity,
    assert_reviews_section,
    attempt_organizer_skill_level_update,
    change_password,
    logout_from_profile,
    open_profile_editor,
    open_profile_page,
    update_profile,
    update_skill_level,
    upload_invalid_profile_file,
    upload_valid_profile_image,
)


def test_player_can_view_own_profile(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="player@test.it", password="password")
    open_profile_page(driver)
    assert_profile_identity(driver, "player@test.it", "PLAYER", "INTERMEDIATE")


def test_organizer_can_view_own_profile(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="organizer@test.it", password="password")
    assert_organizer_view_loaded(driver)
    open_profile_page(driver)
    assert_profile_identity(driver, "organizer@test.it", "ORGANIZER")


def test_user_can_update_profile_data(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="PLAYER", prefix="profile_update", city="Torino")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    open_profile_editor(driver)

    suffix = unique_suffix()
    updated = {
        "email": f"profile_updated_{suffix}@test.it",
        "displayName": f"ProfileUpdated{suffix}",
        "city": "Milano",
    }

    update_profile(driver, updated["email"], updated["displayName"], updated["city"])
    assert_current_user(driver, updated)


def test_player_can_update_skill_level(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="PLAYER", prefix="skill_update", city="Torino")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    open_profile_editor(driver)
    update_skill_level(driver, "ADVANCED")
    assert_current_user(driver, {"skillLevel": "ADVANCED"})


def test_organizer_cannot_update_skill_level(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="ORGANIZER", prefix="org_skill", city="Milano")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    attempt_organizer_skill_level_update(driver)


def test_user_can_change_password(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="PLAYER", prefix="pwd_update", city="Torino")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    open_profile_editor(driver)
    change_password(driver, account["password"], "newsecret1")
    logout_from_profile(driver)
    driver.find_element("xpath", "//button[normalize-space()='Accedi']").click()
    assert_login_page_visible(driver)
    login_user(driver, account["email"], "newsecret1")
    open_profile_page(driver)
    assert_profile_identity(driver, account["email"], "PLAYER", "INTERMEDIATE")


def test_wrong_current_password_is_rejected(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="PLAYER", prefix="pwd_wrong", city="Torino")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    open_profile_editor(driver)
    change_password(driver, "wrongpass", "newsecret1")
    assert_error_toast(driver, "Password attuale non corretta")
    logout_from_profile(driver)
    driver.find_element("xpath", "//button[normalize-space()='Accedi']").click()
    assert_login_page_visible(driver)
    login_user(driver, account["email"], account["password"])
    open_profile_page(driver)
    assert_profile_identity(driver, account["email"], "PLAYER", "INTERMEDIATE")


def test_user_can_upload_valid_profile_image(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="PLAYER", prefix="image_ok", city="Torino")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    upload_valid_profile_image(driver)
    assert_current_user(driver, {"imageUrl": True})


def test_non_image_profile_upload_is_rejected(driver, base_url):
    open_register_page(driver, base_url)
    account = build_account(role="PLAYER", prefix="image_bad", city="Torino")
    register_user(driver, account["email"], account["password"], account["display_name"], account["city"], account["role"])

    open_profile_page(driver)
    upload_invalid_profile_file(driver)


def test_user_can_view_received_reviews(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="player@test.it", password="password")
    open_profile_page(driver)
    assert_reviews_section(driver)


def test_player_can_view_pending_review_matches(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, email="player@test.it", password="password")
    open_profile_page(driver)
    assert_pending_reviews_section(driver)
