from .client import execute_access_flow
from .parser import ( extract_form_action, extract_form_inputs, extract_login_errors, extract_qr_code )
from .client import parse_url

def get_qr_code() -> str:
    """Get QR Code from CIE login page"""
    # Executes the CIE access flow to reach the login page
    _, response = execute_access_flow()

    # Extracts and returns the QR code from the response
    return extract_qr_code(response.text)

def execute_login(form_data: dict):
    """Authenticates user into the Service Provider (Agenzia delle Entrate) by inserting credentials in the selected Identity Provider (CIE)"""
    # Executes the CIE access flow to reach the login page
    session, response = execute_access_flow()

    # Extracts the form action URL and input fields from the response
    url = extract_form_action(response.text)
    payload = extract_form_inputs(response.text)
    # Parses the url
    url = parse_url(response.url, url)
    # Updates the payload with credentials
    payload.update(form_data)
    # POST to /idp/login/livello2
    response = session.post(
        url,
        data=payload
    )

    # Check for login errors
    error = extract_login_errors(response.text)

    if error and (error["title"] or error["message"]):
        return None, error
    return "OK", None
