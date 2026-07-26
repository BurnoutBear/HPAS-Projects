from flask import current_app, jsonify, render_template, request, redirect, session, url_for
from .. import auth
from ..services.cie import access_login_page, get_new_qr_code, submit_credentials, check_2fa, retrieve_access_after_push_2fa, check_qr_code, retrieve_access_after_qr_code_scan
from ..services.flow import save_flow, check_login_flow
from ..services.cie.constants import URL_AGENZIAENTRATE_PORTALE

@auth.route("/cie_login", methods=["GET"])
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

        error = session.pop("cie_login_error", None)

        current_app.logger.info("CIE login page accessed successfully")
        return render_template("cie.html", qr_code=login_flow.qr_code, qr_expiration=login_flow.qr_remaining_ms, username=login_flow.username, password=login_flow.password, error=error), 200

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login page access")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/get_qr_code", methods=["GET"])
def cie_login_get_qr_code():
    """Refreshes the QR code for the CIE login page"""
    try:
        login_flow = check_login_flow()
        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        get_new_qr_code(login_flow)

        current_app.logger.info("CIE login QR refreshed")
        return redirect(url_for("auth.cie_login"))

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login QR")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/credentials", methods=["POST"])
def cie_login_credentials():
    """Handles the submission of CIE login credentials and renders the 2FA page"""
    try:
        current_app.logger.info("CIE login credentials submitted")

        login_flow = check_login_flow()

        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        error = submit_credentials(login_flow, request.form)

        if error:
            session["cie_login_error"] = error
            current_app.logger.warning(f"CIE login flow failed: {error}")
            return redirect(url_for("auth.cie_login"))

        if not login_flow.username or not login_flow.password:
            raise ValueError("Username or password is not set in the login flow")

        current_app.logger.info("CIE login flow executed successfully")
        return render_template("cie_2fa.html"), 200

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login credentials submission")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/check_2fa", methods=["GET"])
def cie_login_check_2fa():
    """Checks if the 2FA has been confirmed and returns the result"""
    try:
        current_app.logger.info("CIE login 2FA check requested")

        login_flow = check_login_flow()

        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        status = check_2fa(login_flow)

        current_app.logger.info(f"CIE login 2FA status: {status}")
        return jsonify(status), 200

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login 2FA check")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/push_2fa", methods=["GET"])
def cie_login_push_2fa():
    """Handles the submission of the 2FA push confirmation and retrieves access to the Service Provider (Agenzia delle Entrate)"""
    try:
        current_app.logger.info("CIE login 2FA push submitted")

        login_flow = check_login_flow()

        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        retrieve_access_after_push_2fa(login_flow)

        return redirect(URL_AGENZIAENTRATE_PORTALE)
    
    except Exception:
        current_app.logger.exception("Unexpected error during CIE login 2FA push submission")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/check_qr_code", methods=["GET"])
def cie_login_check_qr_code():
    """Checks if the QR code has been scanned and returns the result"""
    try:
        current_app.logger.info("CIE login QR code check requested")

        login_flow = check_login_flow()

        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        status = check_qr_code(login_flow)

        current_app.logger.info(f"CIE login QR code status: {status}")
        return jsonify(status), 200

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login QR code check")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/scanned_qr_code", methods=["GET"])
def cie_login_scanned_qr_code():
    """Handles the submission of the scanned QR code and retrieves access to the Service Provider (Agenzia delle Entrate)"""
    try:
        current_app.logger.info("CIE login scanned QR code submitted")

        login_flow = check_login_flow()

        if not login_flow:
            return redirect(url_for("auth.cie_login"))

        retrieve_access_after_qr_code_scan(login_flow)

        return redirect(URL_AGENZIAENTRATE_PORTALE)
    
    except Exception:
        current_app.logger.exception("Unexpected error during CIE login scanned QR code submission")
        return render_template("cie_error.html"), 500

@auth.route("/cie_login/card", methods=["GET"])
def cie_login_card():
    current_app.logger.info("CIE login card")
    # TODO: Implement the logic to handle the card login process
    return render_template("cie.html")
