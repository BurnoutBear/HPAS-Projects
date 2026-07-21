from flask import current_app, render_template, request, session
from .. import auth
from ..services.cie import access_login_page, submit_credentials
from ..services.flow import save_flow, remove_flow, check_login_flow

@auth.route("/cie", methods=["GET"])
def cie_login():
    current_app.logger.info("CIE selected")
    try:
        flow_id = session.pop("login_flow", None)
        if flow_id:
            remove_flow(flow_id)

        login_flow = access_login_page()
        session["login_flow"] = save_flow(login_flow)
        current_app.logger.info("CIE login page accessed successfully")

        return render_template(
            "cie.html",
            qr_code=login_flow.qr_code,
            error=None
        )

    except Exception:
        current_app.logger.exception("Unexpected error during QR code retrieval")
        return render_template(
            "cie.html",
            qr_code=None,
            error={
                "title": "Error",
                "message": "An unexpected error occurred. Please try again later."
            }
        )

@auth.route("/cie/login_credentials", methods=["POST"])
def cie_login_credentials():
    current_app.logger.info("CIE login credentials submitted")
    try:
        login_flow, error = check_login_flow()
        if not login_flow:
            return render_template(
                "cie.html",
                error=error,
                qr_code=None,
                username=request.form.get("username"),
                password=request.form.get("password")
            )

        error = submit_credentials(login_flow, request.form)

        if error:
            current_app.logger.warning(f"CIE login flow failed: {error}")        
            return render_template(
                "cie.html",
                error={
                    "title": error["title"],
                    "message": error["message"]
                },
                qr_code=login_flow.qr_code,
                username=request.form.get("username"),
                password=request.form.get("password")
            )

        current_app.logger.info("CIE login flow executed successfully")
        return render_template(
            "cie_2fa.html"
        )

    except Exception:
        current_app.logger.exception("Unexpected error during CIE login")
        return render_template(
            "cie.html",
            error={
                "title": "Error",
                "message": "An unexpected error occurred. Please try again later."
            },
            qr_code=None,
            username=request.form.get("username"),
            password=request.form.get("password")
        )
    
@auth.route("/cie/login_2fa", methods=["POST"])
def cie_login_2fa():
    current_app.logger.info("CIE login 2FA submitted")
    # TODO: Implement the logic to handle the 2FA process
    return render_template(
        "cie.html"
    )

@auth.route("/cie/login_qr", methods=["POST"])
def cie_login_qr():
    current_app.logger.info("CIE login QR scanned")
    # TODO: Implement the logic to handle the QR code scanning and authentication process
    return render_template(
        "cie.html"
    )

@auth.route("/cie/login_card", methods=["GET"])
def cie_login_card():
    current_app.logger.info("CIE login card")
    # TODO: Implement the logic to handle the card login process
    return render_template(
        "cie.html"
    )
