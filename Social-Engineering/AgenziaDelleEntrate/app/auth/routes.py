from flask import render_template, request, current_app
from . import auth
from .services.cie import execute_login, get_qr_code

@auth.route('/', methods=['GET'])
def login():
    current_app.logger.info("Rendering login page")
    return render_template(
        'login.html'
    )

@auth.route('/cie', methods=['GET', 'POST'])
def cie_login():
    if request.method == 'POST':
        current_app.logger.info("CIE selected - POST")
        try:
            result, error = execute_login(request.form)
            if not error:
                current_app.logger.info("CIE login flow executed successfully")
                return render_template(
                    'cie.html',
                    result=result
                )
            else:
                current_app.logger.warning(f"CIE login flow failed: {error}")        
                return render_template(
                    'cie.html',
                    error=error
                )
        except Exception as e:
            current_app.logger.exception("Unexpected error during CIE login")
            return render_template(
                'cie.html',
                error="An unexpected error occurred."
            )

    current_app.logger.info("CIE selected - GET")
    try:
        qr_code = get_qr_code()
        current_app.logger.info("QR code retrieved successfully")
        return render_template(
            'cie.html',
            qr_code=qr_code
        )
    except Exception as e:
        current_app.logger.exception("Unexpected error during QR code retrieval")
        return render_template(
            'cie.html',
            error="An unexpected error occurred."
        )

@auth.route('/cie/qr', methods=['POST'])
def cie_login_qr():
    current_app.logger.info("CIE QR scanned")
    # TODO: Implement the logic to handle the QR code scanning and authentication process
    return render_template(
        'cie.html'
    )
