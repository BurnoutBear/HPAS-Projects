from dataclasses import dataclass
from requests import Session, Response

@dataclass
class LoginFlow:
    """Represents the state of a login flow, including the session, response, and any relevant data"""
    session: Session
    response: Response

    username: str | None = None
    password: str | None = None

    qr_code: str | None = None

    @property
    def base_url(self):
        return self.response.url
