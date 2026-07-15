from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse, urljoin

def extract_form(response_text: str) -> Tag:
    """Extracts the form element"""
    soup = BeautifulSoup(response_text, "html.parser")

    form = soup.find("form")
    if not form:
        raise RuntimeError("Form not found")

    return form

def extract_form_action(response_text: str) -> str:
    """Extracts the form action URL"""
    form = extract_form(response_text)

    action = form.get("action")
    if not action:
        raise RuntimeError("Form action URL not found")

    return str(action)

def extract_form_inputs(response_text: str) -> dict:
    """Extracts all form input fields"""
    form = extract_form(response_text)

    inputs = {}
    for input in form.find_all("input"):
        name = input.get("name")
        if name:
            inputs[name] = input.get("value", "")
    if not inputs:
        raise RuntimeError("Form input fields not found")

    return inputs

def extract_qr_code(response_text: str) -> str:
    """Extracts the QR code from the response text"""
    soup = BeautifulSoup(response_text, "html.parser")

    img = soup.find("img", alt="QR code")
    if not img:
        raise RuntimeError("QR code not found")

    src = str(img["src"])
    if not src.startswith("data:image/png;base64,"):
        raise RuntimeError("Unexpected QR format")

    return src.split(",", 1)[1].strip()

def extract_login_errors(response_text: str) -> dict | None:
    """Extracts login error messages from the response text"""
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

def parse_url(base_url: str, url: str) -> str:
    """Parses the provided URL and returns the absolute URL based on the base URL"""
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    return urljoin(root, url)
