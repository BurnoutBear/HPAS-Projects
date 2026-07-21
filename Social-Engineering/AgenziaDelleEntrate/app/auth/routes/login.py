from flask import current_app, render_template
from .. import auth

@auth.route("/", methods=["GET"])
def login():
    """Renders the login page"""
    current_app.logger.info("Rendering login page")
    return render_template("login.html")
