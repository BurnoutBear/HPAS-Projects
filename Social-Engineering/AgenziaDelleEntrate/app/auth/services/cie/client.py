from requests import Session, exceptions
from .constants import URL_AGENZIAENTRATE_LOGIN, URL_CIE_SELECTION, URL_CONTACT_PHONE_2FA, URL_PUSH_2FA_SMS, URL_CHECK_PUSH_2FA, URL_PUSH_2FA, URL_CHECK_QR_CODE, URL_SCANNED_QR_CODE
from .parser import parse_url, get_query_string, extract_url_and_payload_from_form_and_parse, extract_sensitive_data_from_saml_response, set_form_value
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

    login_page_url_query_string = get_query_string(response.url)

    return LoginFlow(session=session, response=response, login_page_url=response.url, login_page_url_query_string=login_page_url_query_string, login_page_text=response.text)

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

def contact_user_phone(login_flow: LoginFlow, method: str | None) -> None:
    """Contacts the user phone for 2FA notification to the CIE login page"""
    url = parse_url(login_flow.login_page_url, URL_CONTACT_PHONE_2FA)
    if method is None:
        login_flow.response = login_flow.session.post(url)
    else:
        payload = {"cnl": method}
        login_flow.response = login_flow.session.post(url, data=payload)

def submit_push_2fa_sms(login_flow: LoginFlow, otp1: str, otp2: str, otp3: str, otp4: str) -> None:
    """Submits the 2FA SMS confirmation to the CIE login page"""
    url = parse_url(login_flow.login_page_url, URL_PUSH_2FA_SMS)
    payload = {"otp1": otp1, "otp2": otp2, "otp3": otp3, "otp4": otp4}
    login_flow.response = login_flow.session.post(url, data=payload)

def get_2fa_status(login_flow: LoginFlow) -> None:
    """Retrieves the status of the 2FA confirmation from the CIE login page"""
    url = parse_url(login_flow.login_page_url, URL_CHECK_PUSH_2FA)
    try:
        login_flow.response = login_flow.session.get(url, timeout=5)
    except exceptions.ConnectionError:
        return None

def submit_push_2fa(login_flow: LoginFlow) -> None:
    """Submits the 2FA push confirmation to the CIE login page"""
    url = parse_url(login_flow.login_page_url, URL_PUSH_2FA)
    login_flow.response = login_flow.session.get(url)

def get_qr_code_status(login_flow: LoginFlow) -> None:
    """Retrieves the status of the QR code scan from the CIE login page"""
    url = parse_url(login_flow.login_page_url, URL_CHECK_QR_CODE)
    try:
        login_flow.response = login_flow.session.get(url, timeout=5)
    except exceptions.ConnectionError:
        return None

def submit_scanned_qr_code(login_flow: LoginFlow) -> None:
    """Submits the scanned QR code to the CIE login page"""
    url = parse_url(login_flow.login_page_url, URL_SCANNED_QR_CODE)
    login_flow.response = login_flow.session.get(url)

def confirm_access(login_flow: LoginFlow) -> None:
    """Confirms the access to the Service Provider (Agenzia delle Entrate)"""
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.response.text, login_flow.response.url)
    #Updates the payload with the confirmation input
    set_form_value(payload, "_eventId_proceed", "Prosegui")
    # POST to /idp/profile/SAML2/POST/SSO?execution=e1s4
    login_flow.response = login_flow.session.post(url, data=payload)
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.response.text, login_flow.response.url)
    # Extracts the SAMLResponse from the payload and retrieves sensitive data
    saml_response = next(value for name, value in payload if name == "SAMLResponse")
    login_flow.sensitive_data = extract_sensitive_data_from_saml_response(saml_response)
    # POST to https://sp.agenziaentrate.gov.it/sp/AssertionConsumerService7
    login_flow.response = login_flow.session.post(url, data=payload)
    url, payload = extract_url_and_payload_from_form_and_parse(login_flow.response.text, login_flow.response.url)
    # POST to https://sp.agenziaentrate.gov.it/sam/Consumer/metaAlias/agenziaentrate/age-sp
    login_flow.response = login_flow.session.post(url, data=payload)
    login_flow.completed = True
