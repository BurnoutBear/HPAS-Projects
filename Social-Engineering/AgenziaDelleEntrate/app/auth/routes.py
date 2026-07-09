from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .services import execute_cie_login_flow

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def login():
    current_app.logger.info("Rendering login page")
    return render_template('login.html')

@auth.route('/spid', methods=['GET', 'POST'])
def spid_login():
    current_app.logger.info("SPID selected")
    return render_template('spid.html')

@auth.route('/cie', methods=['GET', 'POST'])
def cie_login():
    current_app.logger.info("CIE selected")
    error = None

    if request.method == 'POST':
        result, error = execute_cie_login_flow(request.form)
        
        if not error:
            current_app.logger.info(f"CIE login flow executed successfully: {result}")
            return render_template('cie_success.html', result=result)

        else:
            current_app.logger.error(f"CIE login flow failed: {error}")        
            return render_template('cie_error.html', error=error)

    return render_template('cie.html', error=error)

@auth.route('/cns', methods=['GET', 'POST'])
def cns_login():
    current_app.logger.info("CNS selected")
    return render_template('cns.html')

@auth.route('/fisconlineEntratel', methods=['POST'])
def fisconlineEntratel_login():
    current_app.logger.info("FisconlineEntratel selected")
    return render_template('login.html')

@auth.route('/sister', methods=['POST'])
def sister_login():
    current_app.logger.info("Sister selected")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    current_app.logger.info("Logout successful")
    session.clear()
    return redirect(url_for('auth.login'))
