from flask import session
from uuid import uuid4
from .flow import LoginFlow

_flows: dict[str, LoginFlow] = {}

def save_flow(flow: LoginFlow) -> None:
    """Saves the login flow in the internal storage and the session"""
    flow_id = str(uuid4())
    _flows[flow_id] = flow
    session["login_flow"] = flow_id

def get_flow(flow_id: str) -> LoginFlow | None:
    """Retrieves the login flow from the internal storage using the flow ID"""
    return _flows.get(flow_id)

def remove_flow(flow_id: str) -> None:
    """Removes the login flow from the internal storage and the session using the flow ID"""
    _flows.pop(flow_id, None)
    session.pop("login_flow", None)

def check_login_flow() -> LoginFlow | None:
    """Checks if a login flow exists in the session and returns it. If it does not exist or is expired, removes it and returns None."""
    flow_id = session.get("login_flow")

    if flow_id is None:
        return None

    flow = get_flow(flow_id)

    if flow is None:
        session.pop("login_flow", None)
        return None

    if flow.is_flow_expired or flow.completed:
        remove_flow(flow_id)
        return None

    return flow
