from flask import session
from uuid import uuid4
from .flow import LoginFlow

_flows: dict[str, LoginFlow] = {}

def save_flow(flow: LoginFlow) -> str:
    """Saves the login flow in the session and returns a unique flow ID"""
    flow_id = str(uuid4())
    _flows[flow_id] = flow
    return flow_id

def get_flow(flow_id: str) -> LoginFlow | None:
    """Retrieves the login flow from the session using the flow ID"""
    return _flows.get(flow_id)

def remove_flow(flow_id: str):
    """Removes the login flow from the session using the flow ID"""
    _flows.pop(flow_id, None)

def check_login_flow() -> LoginFlow | None:
    """Checks if a login flow exists in the session and returns it along with any error messages"""
    flow_id = session.get("login_flow")

    if flow_id is None:
        return None

    flow = get_flow(flow_id)

    if flow is None:
        session.pop("login_flow", None)
        return None
    
    if flow.is_flow_expired:
        remove_flow(flow_id)
        session.pop("login_flow", None)
        return None

    return flow
