from tests.steps.account_steps import login_user, open_login_page
from tests.steps.match_discovery_steps import (
    apply_invalid_date_range,
    assert_badge_results,
    assert_city_results,
    assert_default_filters,
    assert_invalid_date_range_error,
    assert_match_list_loaded,
    filter_by_after,
    filter_by_before,
    filter_by_city,
    filter_by_match_type,
    filter_by_open_status,
    filter_by_skill_level,
    open_match_list_page,
    reset_filters,
)


def test_default_match_list_is_loaded(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    assert_match_list_loaded(driver)


def test_matches_can_be_filtered_by_city(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_city(driver, "Torino")
    assert_city_results(driver, "Torino")


def test_matches_can_be_filtered_by_start_date(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_after(driver, "2030-01-01", "00:00")
    assert_match_list_loaded(driver)


def test_matches_can_be_filtered_by_end_date(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_before(driver, "2030-01-01", "23:59")
    assert_match_list_loaded(driver)


def test_invalid_date_range_is_rejected(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    apply_invalid_date_range(driver)
    assert_invalid_date_range_error(driver)


def test_matches_can_be_filtered_by_skill_level(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_skill_level(driver, "INTERMEDIATE")
    assert_badge_results(driver, "INTERMEDIATE")


def test_matches_can_be_filtered_by_match_type(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_match_type(driver, "SINGLES")
    assert_badge_results(driver, "SINGLES")


def test_matches_can_be_filtered_by_open_status(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_open_status(driver, "OPEN")
    assert_badge_results(driver, "Aperta")


def test_filters_can_be_reset(driver, base_url):
    open_login_page(driver, base_url)
    login_user(driver, "player@test.it", "password")
    open_match_list_page(driver)
    filter_by_city(driver, "Torino")
    reset_filters(driver)
    assert_default_filters(driver)
