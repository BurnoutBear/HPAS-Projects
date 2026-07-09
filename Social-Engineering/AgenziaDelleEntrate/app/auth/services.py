import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

URL_AGENZIAENTRATE_LOGIN_GET = "https://iampe.agenziaentrate.gov.it/sam/UI/Login?realm=/agenziaentrate"
URL_CIE_SELECTION_GET = "https://sp.agenziaentrate.gov.it/rp/cie/sel"

def get_credentials(form_data):
    """Extracts and returns the username and password from the provided form data."""
    username = form_data.get('username', '').strip()
    password = form_data.get('password', '').strip()
    username = 'RSSMRA80A01H501U'
    password = 'Password1!'
    return {
        "username": username,
        "password": password
    }

def extract_form(response_text):
    """Extracts the form element"""
    soup = BeautifulSoup(response_text, "html.parser")
    form = soup.find("form")
    if not form:
        raise ValueError("Form not found.")
    return form

def extract_form_action(response_text):
    """Extracts the form action URL"""
    form = extract_form(response_text)
    action = form.get("action")
    if not action:
        raise ValueError("Form action URL not found.")
    return str(action)

def extract_form_inputs(response_text):
    """Extracts all form input fields"""
    form = extract_form(response_text)
    inputs = {}
    for input in form.find_all("input"):
        name = input.get("name")
        if name:
            inputs[name] = input.get("value", "")
    if not inputs:
        raise ValueError("Form input fields not found.")
    return inputs

def parse_url(base_url, url):
    """Parses the provided URL and returns the absolute URL based on the base URL."""
    parsed_url = urlparse(base_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return urljoin(base_url, url)

def debug_print(url, method, r):
    """Prints debug information for the given URL, method and response."""
    print("------------------------------------------------------------------------------")
    print(f"Request to {url} with method {method} returned status code {r.status_code}:")
    print(f"Response cookies: {r.cookies}")
    print(f"Response headers: {r.headers}")
    print(f"Response content: {r.text}")

def execute_cie_login_flow(form_data):
    """
    Handles the login flow for authenticating user into the Service Provider (Agenzia delle Entrate) through the selected Identity Provider (CIE).
    1. Initializes the session performing a GET to Agenzia delle Entrate login page;
    2. Simulates CIE selection by performing a GET to /sel, retrieving the AuthnRequest SAML (generated and signed by the SP);
    3. Performs a POST to the IdP's /SSO delivering the AuthnRequest SAML (POST binding);
    4. Handles Shibboleth's internal multi-step flow via /SSO?execution (session/localStorage handshake);
    5. Reaches the CIE login form, where the user's credentials (or physical card) are required to complete authentication.
    """
    error = None

    # Gets username and password
    credentials = get_credentials(form_data)

    # Initializes the session
    s = requests.Session()

    # 1. GET to Agenzia delle Entrate login page
    r = s.get(URL_AGENZIAENTRATE_LOGIN_GET)
    
    # 2. GET to cie /sel
    r = s.get(URL_CIE_SELECTION_GET)

    # Extracts the form action URL and input fields from the response
    try:
        url = extract_form_action(r.text)
        payload = extract_form_inputs(r.text)
    except ValueError as e:
        return None, str(e)
    # 3. POST to /SSO
    r = s.post(url, data=payload)
    debug_print(url, "POST", r)

    # Gets the base URL from the response
    base_url = r.url
    # Extracts the form action URL from the response
    try:
        url = extract_form_action(r.text)
    except ValueError as e:
        return None, str(e)
    # Parses the url
    url = parse_url(base_url, url)
    # 4. GET to /SSO?execution
    r = s.get(url)
    debug_print(url, "GET", r)

    # 4. POST to /SSO?execution
    payload = {
        "shib_idp_ls_exception.shib_idp_session_ss": "",
        "shib_idp_ls_success.shib_idp_session_ss": "true",
        "shib_idp_ls_value.shib_idp_session_ss": "",

        "shib_idp_ls_exception.shib_idp_persistent_ss": "",
        "shib_idp_ls_success.shib_idp_persistent_ss": "true",
        "shib_idp_ls_value.shib_idp_persistent_ss": "",

        "shib_idp_ls_supported": "true",
        "_eventId_proceed": ""
    }
    r = s.post(url, data=payload)
    debug_print(url, "POST", r)
    
    return None, error
