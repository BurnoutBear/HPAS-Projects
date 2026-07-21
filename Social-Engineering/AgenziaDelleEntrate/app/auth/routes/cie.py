from flask import current_app, render_template, request, redirect, url_for
from .. import auth
from ..services.cie import access_login_page, get_new_qr_code, submit_credentials
from ..services.flow import save_flow, check_login_flow

DEFAULT_ERROR = {"title": "Error", "message": "An unexpected error occurred. Please try again later"}

@auth.route("/cie", methods=["GET"])
def cie_login():
    """Renders the CIE login page with QR code and handles the login flow"""
    try:
        current_app.logger.info("CIE selected")

        login_flow = check_login_flow()
        if not login_flow:
            login_flow = access_login_page()
            save_flow(login_flow)

        if login_flow.is_qr_expired:
            get_new_qr_code(login_flow)

        current_app.logger.info("CIE login page accessed successfully")
        return render_template("cie.html", qr_code=login_flow.qr_code, qr_expiration=login_flow.qr_remaining_ms, error=None), 200

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login page access")
        return render_template("cie.html", qr_code=None, qr_expiration=None, error=DEFAULT_ERROR), 500

@auth.route("/cie/login_credentials", methods=["POST"])
def cie_login_credentials():
    """Handles the submission of CIE login credentials and manages the login flow"""
    try:
        current_app.logger.info("CIE login credentials submitted")

        login_flow = check_login_flow()
        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        error = submit_credentials(login_flow, request.form)

        if error:
            current_app.logger.warning(f"CIE login flow failed: {error}")
            return render_template("cie.html", qr_code=login_flow.qr_code, qr_expiration=login_flow.qr_remaining_ms, error=error, username=login_flow.username, password=login_flow.password), 400

        current_app.logger.info("CIE login flow executed successfully")
        return render_template("cie_2fa.html"), 200
    except Exception:
        current_app.logger.exception("Unexpected error during CIE login credentials submission")
        return render_template("cie.html", qr_code=None, qr_expiration=None, error=DEFAULT_ERROR), 500

@auth.route("/cie/login_2fa", methods=["POST"])
def cie_login_2fa():
    current_app.logger.info("CIE login 2FA submitted")
    # TODO: Implement the logic to handle the 2FA process
    return render_template("cie.html")

@auth.route("/cie/qr", methods=["GET", "POST"])
def cie_login_qr():
    try:
        login_flow = check_login_flow()
        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        if request.method == "POST":
            current_app.logger.info("CIE login QR scanned")
            # TODO: Implement the logic to handle the QR code scanning and authentication process
            return render_template("cie.html"), 200

        get_new_qr_code(login_flow)
        current_app.logger.info("CIE login QR refreshed")
        return redirect(url_for("auth.cie_login"))

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login QR")
        return render_template("cie.html", qr_code=None, qr_expiration=None, error=DEFAULT_ERROR), 500

@auth.route("/cie/login_card", methods=["GET"])
def cie_login_card():
    current_app.logger.info("CIE login card")
    # TODO: Implement the logic to handle the card login process
    return render_template("cie.html")
