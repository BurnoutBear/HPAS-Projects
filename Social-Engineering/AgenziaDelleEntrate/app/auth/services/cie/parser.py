from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse, urljoin

def parse_url(full_url: str, suffix_url: str) -> str:
    """Parses the full URL and appends the suffix URL to it"""
    parsed = urlparse(full_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    return urljoin(base_url, suffix_url)

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

def extract_form_inputs(response_text: str) -> list[tuple[str, str]]:
    """Extracts all form input fields"""
    form = extract_form(response_text)

    input_tags = []
    for input_tag in form.find_all("input"):
        name = input_tag.get("name")
        # Skip input fields without a name
        if not name:
            continue
        # Skip unchecked radio and checkbox inputs
        input_type = str(input_tag.get("type", "")).lower()
        if input_type in ("radio", "checkbox") and not input_tag.has_attr("checked"):
            continue
        # Finally, add the input field to the list
        input_tags.append((name, input_tag.get("value", "")))
    if not input_tags:
        raise RuntimeError("Form input fields not found")

    return input_tags

def extract_url_and_payload_from_form_and_parse(response_text: str, original_url: str) -> tuple[str, list[tuple[str, str]]]:
    """Extracts the form action URL and input fields from the response text, and parses the URL"""
    suffix_url = extract_form_action(response_text)
    payload = extract_form_inputs(response_text)
    url = parse_url(original_url, suffix_url)
    return url, payload

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

def set_form_value(payload: list[tuple[str, str]], name: str, value: str) -> None:
    """Sets the value of a form input field in the payload"""
    for i, (key, _) in enumerate(payload):
        if key == name:
            payload[i] = (key, value)
            return

    payload.append((name, value))
