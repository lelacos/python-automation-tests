LOGIN_HEADER_XPATH = "//h2[normalize-space()='Accedi']"
REGISTER_HEADER_XPATH = "//h2[normalize-space()='Crea account']"
LIST_VIEW_HEADER_XPATH = "//h2[normalize-space()='Partite']"
PLAYER_DASHBOARD_BUTTON_XPATH = "//button[normalize-space()='+ Nuova partita']"
ORGANIZER_DASHBOARD_BUTTON_XPATH = "//button[normalize-space()='Gestione campi']"
ORGANIZER_VIEW_HEADER_XPATH = "//h2[normalize-space()='Gestione campi e partite']"
LOGOUT_BUTTON_XPATH = "//button[normalize-space()='Logout']"


def error_toast_xpath(message):
    return f"//div[@role='alert' and normalize-space()='{message}']"
