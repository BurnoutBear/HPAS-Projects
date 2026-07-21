from requests import Session, exceptions
from time import sleep
from .constants import URL_AGENZIAENTRATE_LOGIN_GET, URL_CIE_SELECTION_GET, URL_CHECK_QR, URL_CHECK_PUSH
from .parser import extract_form_action, extract_form_inputs, parse_url
from ..flow import LoginFlow

def execute_access_flow() -> LoginFlow:
    """
    Handles the access flow for reaching the selected Identity Provider (CIE)
    1. Initializes the session performing a GET to Agenzia delle Entrate login page
    2. Simulates CIE selection by performing a GET to /sel, retrieving the AuthnRequest SAML (generated and signed by the SP)
    3. Performs a POST to the IdP's /SSO delivering the AuthnRequest SAML (POST binding)
    4. Handles Shibboleth's internal multi-step flow via /SSO?execution (session/localStorage handshake), reaching the login page
    """
    # Initializes the session
    session = Session()

    # 1. GET to Agenzia delle Entrate login page
    response = session.get(URL_AGENZIAENTRATE_LOGIN_GET)

    # 2. GET to cie /sel
    response = session.get(URL_CIE_SELECTION_GET)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # Extracts the form action URL and input fields from the response
    url = extract_form_action(response.text)
    payload = extract_form_inputs(response.text)
    # 3. POST to /idp/profile/SAML2/POST/SSO
    response = session.post(url, data=payload)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # There's a JS that handles form inputs, but since <noscript> is implemented, use that which sets only default inputs
    # Extracts the form action URL and input fields from the response
    url = extract_form_action(response.text)
    payload = extract_form_inputs(response.text)
    # Parses the url
    url = parse_url(response.url, url)
    # 4. POST to /idp/profile/SAML2/POST/SSO?execution=e1s1
    response = session.post(url, data=payload)

    return LoginFlow(session=session, response=response, base_url=response.url, base_text=response.text)

def access_again_login_page(login_flow: LoginFlow) -> None:
    """Visits the CIE login page again"""
    login_flow.response = login_flow.session.get(login_flow.base_url)

def post_credentials(login_flow: LoginFlow, credentials: dict) -> None:
    """Posts the credentials to the CIE login page and retrieves the response"""
    # Extracts the form action URL and input fields from the response
    url = extract_form_action(login_flow.base_text)
    payload = extract_form_inputs(login_flow.base_text)
    # Parses the url
    url = parse_url(login_flow.base_url, url)
    # Updates the payload with credentials
    payload.update(credentials)
    # POST to /idp/login/livello2
    login_flow.response = login_flow.session.post(url, data=payload)

def get_qr_code_status(login_flow: LoginFlow) -> None:
    """Retrieves the status of the QR code scan from the CIE login page"""
    check_url = parse_url(login_flow.base_url, URL_CHECK_QR)
    try:
        login_flow.response = login_flow.session.get(check_url, timeout=5)
    except exceptions.ConnectionError:
        return None

def wait_for_push_confirmation(login_flow: LoginFlow, base_url: str, interval: int = 5, timeout: int = 120) -> None:
    """Polling on push confirmation endpoint until status is not WAIT or timeout is reached"""
    check_url = parse_url(base_url, URL_CHECK_PUSH)
    elapsed = 0

    while elapsed < timeout:
        login_flow.response = login_flow.session.get(check_url)
        data = login_flow.response.json()

        status = data.get("status")
        if status != "WAIT":
            return

        sleep(interval)
        elapsed += interval

    raise TimeoutError("User did not confirm the push notification within the timeout period")
