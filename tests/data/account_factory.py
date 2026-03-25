import time


def unique_suffix():
    return int(time.time())


def build_account(role, prefix, city):
    ts = unique_suffix()
    email = f"{prefix}_{ts}@test.it"
    password = "secret1"
    display_name = f"{prefix.capitalize()}{ts}"
    return {
        "email": email,
        "password": password,
        "display_name": display_name,
        "city": city,
        "role": role,
    }
