from flask import session
from uuid import uuid4
from .flow import LoginFlow

_flows: dict[str, LoginFlow] = {}

def save_flow(flow: LoginFlow) -> str:
    flow_id = str(uuid4())
    _flows[flow_id] = flow
    return flow_id

def get_flow(flow_id: str) -> LoginFlow | None:
    return _flows.get(flow_id)

def remove_flow(flow_id: str):
    _flows.pop(flow_id, None)

def check_login_flow() -> tuple[LoginFlow | None, dict | None]:
    flow_id = session.get("login_flow")

    if flow_id is None:
        return None, {
            "title": "Error",
            "message": "No login flow found. Please start the login process again."
        }

    flow = get_flow(flow_id)

    if flow is None:
        return None, {
            "title": "Error",
            "message": "Login flow not found. Please start the login process again."
        }

    return flow, None
