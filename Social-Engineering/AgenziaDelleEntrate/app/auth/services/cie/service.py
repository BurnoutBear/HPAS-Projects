from .client import execute_access_flow, post_credentials
from .parser import extract_qr_code, extract_login_errors

def get_qr_code() -> str:
    """Get QR Code from CIE login page"""
    # Executes the CIE access flow to reach the login page
    _, response = execute_access_flow()

    # Extracts and returns the QR code from the response
    return extract_qr_code(response.text)

def submit_credentials(credentials: dict) -> tuple:
    """Authenticates user into the Service Provider (Agenzia delle Entrate) by inserting credentials in the selected Identity Provider (CIE)"""
    # Executes the CIE access flow to reach the login page
    session, response = execute_access_flow()

    # Posts the credentials to the CIE login page and retrieves the response
    session, response = post_credentials(session, response, credentials)

    # Check for login errors
    error = extract_login_errors(response.text)

    if error and (error["title"] or error["message"]):
        return None, error
    return "OK", None
