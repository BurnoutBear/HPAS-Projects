from requests import Session, Response
from .constants import ( URL_AGENZIAENTRATE_LOGIN_GET, URL_CIE_SELECTION_GET )
from .parser import ( extract_form_action, extract_form_inputs, parse_url )

def execute_access_flow() -> tuple[Session, Response]:
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
    response = session.get(
        URL_AGENZIAENTRATE_LOGIN_GET
    )

    # 2. GET to cie /sel
    response = session.get(
        URL_CIE_SELECTION_GET
    )

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # Extracts the form action URL and input fields from the response
    url = extract_form_action(response.text)
    payload = extract_form_inputs(response.text)
    # 3. POST to /idp/profile/SAML2/POST/SSO
    response = session.post(
        url,
        data=payload
    )

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # There's a JS that handles form inputs, but since <noscript> is implemented, use that which sets only default inputs
    # Extracts the form action URL and input fields from the response
    url = extract_form_action(response.text)
    payload = extract_form_inputs(response.text)
    # Parses the url
    url = parse_url(response.url, url)
    # 4. POST to /idp/profile/SAML2/POST/SSO?execution=e1s1
    response = session.post(
        url,
        data=payload
    )

    return session, response
