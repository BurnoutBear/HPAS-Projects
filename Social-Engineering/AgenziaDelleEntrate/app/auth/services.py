import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

URL_AGENZIAENTRATE_LOGIN_GET = "https://iampe.agenziaentrate.gov.it/sam/UI/Login?realm=/agenziaentrate"
URL_CIE_SELECTION_GET = "https://sp.agenziaentrate.gov.it/rp/cie/sel"

def get_credentials(form_data):
    """Extracts and returns the username and password from the provided form data."""
    username = form_data.get('username', '').strip()
    password = form_data.get('password', '').strip()
    if not username or not password:
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

def extract_login_errors(response_text):
    """Extracts login error messages from the response text."""
    soup = BeautifulSoup(response_text, "html.parser")
    status = soup.find(id="statusHandler")
    if not status:
        return None
    title = status.find(id="statusHandlerTitle")
    message = status.find(id="statusHandlerMsg")
    return {
        "title": title.get_text(" ", strip=True) if title else None,
        "message": message.get_text(" ", strip=True) if message else None,
    }

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
    5. Reaches the CIE login form, where the user's credentials are required to complete authentication.
    """
    # Gets username and password
    credentials = get_credentials(form_data)

    # Initializes the session
    s = requests.Session()

    # 1. GET to Agenzia delle Entrate login page
    r = s.get(URL_AGENZIAENTRATE_LOGIN_GET)

    # 2. GET to cie /sel
    r = s.get(URL_CIE_SELECTION_GET)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # Extracts the form action URL and input fields from the response
    try:
        url = extract_form_action(r.text)
        payload = extract_form_inputs(r.text)
    except ValueError as e:
        return None, str(e)
    # 3. POST to /idp/profile/SAML2/POST/SSO
    r = s.post(url, data=payload)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # There's a JS that handles form inputs, but since <noscript> is implemented, use that which sets only default inputs
    # Gets the base URL from the response
    base_url = r.url
    # Extracts the form action URL and input fields from the response
    try:
        url = extract_form_action(r.text)
        payload = extract_form_inputs(r.text)
    except ValueError as e:
        return None, str(e)
    # Parses the url
    url = parse_url(base_url, url)
    # 4. POST to /idp/profile/SAML2/POST/SSO?execution=e1s1
    r = s.post(url, data=payload)

    # The response gives an HTML with a form that contains the next URL to call and its relative payload
    # Gets the base URL from the response
    base_url = r.url
    # Extracts the form action URL and input fields from the response
    try:
        url = extract_form_action(r.text)
        payload = extract_form_inputs(r.text)
    except ValueError as e:
        return None, str(e)
    # Parses the url
    url = parse_url(base_url, url)
    # Updates the payload with credentials
    payload.update(credentials)
    # 5. POST to /idp/login/livello2
    r = s.post(url, data=payload)
    debug_print(url, "POST", r)
    # Check for login errors
    error = extract_login_errors(r.text)
    if error and (error["title"] or error["message"]):
        return None, error

    return "OK", None
