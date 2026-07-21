from .client import access_again_login_page, execute_access_flow, post_credentials
from .parser import extract_qr_code, extract_login_errors
from ..flow import LoginFlow

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
    login_flow = access_again_login_page(login_flow)

    # Extracts the QR code from the response
    login_flow.set_qr_code(extract_qr_code(login_flow.response.text))

def submit_credentials(login_flow: LoginFlow, credentials: dict) -> dict | None:
    """Authenticates user into the Service Provider (Agenzia delle Entrate) by inserting credentials in the selected Identity Provider (CIE)"""
    login_flow.username = credentials.get("username")
    login_flow.password = credentials.get("password")

    # Posts the credentials to the CIE login page and retrieves the response
    login_flow = post_credentials(login_flow, credentials)

    # Check for login errors
    error = extract_login_errors(login_flow.response.text)

    return error
