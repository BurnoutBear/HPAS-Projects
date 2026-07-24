from dataclasses import dataclass, field
from time import monotonic
from requests import Session, Response

TTL_FLOW = 300
TTL_QR_CODE = 120

@dataclass
class LoginFlow:
    """Represents the state of a login flow, including the session, response, and any relevant data"""
    session: Session
    response: Response
    login_page_url: str
    login_page_text: str

    username: str | None = None
    password: str | None = None

    completed: bool = False

    qr_code: str | None = None
    qr_expires_at: float = field(default_factory=lambda: monotonic() + TTL_QR_CODE)

    flow_expires_at: float = field(default_factory=lambda: monotonic() + TTL_FLOW)

    def __post_init__(self):
        self.qr_expires_at = min(self.qr_expires_at, self.flow_expires_at)

    def set_qr_code(self, qr_code: str) -> None:
        self.qr_code = qr_code
        self.qr_expires_at = min(monotonic() + TTL_QR_CODE, self.flow_expires_at)

    @property
    def qr_remaining_ms(self) -> int:
        return max(0, int((self.qr_expires_at - monotonic()) * 1000))

    @property
    def flow_remaining_ms(self) -> int:
        return max(0, int((self.flow_expires_at - monotonic()) * 1000))

    @property
    def is_qr_expired(self) -> bool:
        return self.qr_expires_at <= monotonic()

    @property
    def is_flow_expired(self) -> bool:
        return self.flow_expires_at <= monotonic()
