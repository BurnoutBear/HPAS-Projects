from flask import current_app, render_template, request
from .. import auth
from ..services.cie import submit_credentials, get_qr_code

@auth.route("/cie", methods=["GET"])
def cie_login():
    current_app.logger.info("CIE selected")
    try:
        qr_code = get_qr_code()
        current_app.logger.info("QR code retrieved successfully")
        return render_template(
            "cie.html",
            qr_code=qr_code,
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
        result, error = submit_credentials(request.form)

        if error and (error["title"] or error["message"]):
            current_app.logger.warning(f"CIE login flow failed: {error}")        
            return render_template(
                "cie.html",
                error={
                    "title": error["title"],
                    "message": error["message"]
                }
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
            }
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
