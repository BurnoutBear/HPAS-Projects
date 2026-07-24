from requests import Session, exceptions
from .constants import URL_AGENZIAENTRATE_LOGIN, URL_CIE_SELECTION, URL_CHECK_QR_CODE, URL_SCANNED_QR_CODE, URL_CHECK_PUSH
from .parser import parse_url, extract_url_and_payload_from_form_and_parse, set_form_value
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
    response = session.get(URL_AGENZIAENTRATE_LOGIN)

    # 2. GET to cie /sel
    response = session.get(URL_CIE_SELECTION)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    url, payload = extract_url_and_payload_from_form_and_parse(response.text, response.url)
    # 3. POST to /idp/profile/SAML2/POST/SSO
    response = session.post(url, data=payload)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # There's a JS that handles form inputs, but since <noscript> is implemented, use that which sets only default inputs
    url, payload = extract_url_and_payload_from_form_and_parse(response.text, response.url)
    # 4. POST to /idp/profile/SAML2/POST/SSO?execution=e1s1
    response = session.post(url, data=payload)

    return LoginFlow(session=session, response=response, login_page_url=response.url, login_page_text=response.text)

def access_again_login_page(login_flow: LoginFlow) -> None:
    """Visits the CIE login page again"""
    login_flow.response = login_flow.session.get(login_flow.login_page_url)

def post_credentials(login_flow: LoginFlow, credentials: dict) -> None:
    """Posts the credentials to the CIE login page and retrieves the response"""
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.login_page_text, login_flow.login_page_url)
    # Updates the payload with credentials
    for key, value in credentials.items():
        set_form_value(payload, key, value)
    # POST to /idp/login/livello2
    login_flow.response = login_flow.session.post(url, data=payload)

def get_qr_code_status(login_flow: LoginFlow) -> None:
    """Retrieves the status of the QR code scan from the CIE login page"""
    check_url = parse_url(login_flow.login_page_url, URL_CHECK_QR_CODE)
    try:
        login_flow.response = login_flow.session.get(check_url, timeout=5)
    except exceptions.ConnectionError:
        return None

def submit_scanned_qr_code(login_flow: LoginFlow) -> None:
    """Submits the scanned QR code to the CIE login page"""
    scanned_url = parse_url(login_flow.login_page_url, URL_SCANNED_QR_CODE)
    login_flow.response = login_flow.session.get(scanned_url)

def confirm_access(login_flow: LoginFlow) -> None:
    """Confirms the access to the Service Provider (Agenzia delle Entrate)"""
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.response.text, login_flow.response.url)
    #Updates the payload with the confirmation input
    set_form_value(payload, "_eventId_proceed", "Prosegui")
    # POST to /idp/profile/SAML2/POST/SSO?execution=e1s4
    login_flow.response = login_flow.session.post(url, data=payload)
    print(login_flow.response.text) # TODO: extract info
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.response.text, login_flow.response.url)
    # POST to https://sp.agenziaentrate.gov.it/sp/AssertionConsumerService7
    login_flow.response = login_flow.session.post(url, data=payload)
    print(login_flow.response.text) # TODO: extract info
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.response.text, login_flow.response.url)
    # POST to https://sp.agenziaentrate.gov.it/sam/Consumer/metaAlias/agenziaentrate/age-sp
    login_flow.response = login_flow.session.post(url, data=payload)
    login_flow.completed = True
