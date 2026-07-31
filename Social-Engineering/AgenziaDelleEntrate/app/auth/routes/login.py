from flask import current_app, render_template, session
from .. import auth
from ..services.flow import remove_flow

@auth.route("/", methods=["GET"])
def login():
    """Renders the login page"""
    flow_id = session.get("login_flow")
    if flow_id:
        remove_flow(flow_id)
    current_app.logger.info("Rendering login page")
    return render_template("login.html"), 200
