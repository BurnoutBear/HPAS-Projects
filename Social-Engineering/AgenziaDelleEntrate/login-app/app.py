from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'university-project-secret'

# Demo credentials (Fisconline/Entratel style — no real data collected)
FAKE_CODICE_FISCALE = 'RSSMRA80A01H501U'
FAKE_PASSWORD       = 'Password1!'
FAKE_PIN            = '12345678'


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('IDToken1', '').strip()
        password = request.form.get('IDToken2', '')
        pin      = request.form.get('IDToken3', '')
        print(f"Attempted login with Codice Fiscale: {username}, Password: {password}, PIN: {pin}")
        if username == FAKE_CODICE_FISCALE and password == FAKE_PASSWORD and pin == FAKE_PIN:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Le credenziali inserite non sono corrette. Verificare codice fiscale, password e PIN.'

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f'''
        <div style="font-family:'Titillium Web',Arial;padding:2rem;max-width:600px;margin:2rem auto">
            <h2 style="color:#06c">Accesso effettuato ✅</h2>
            <p>Benvenuto/a, <strong>{session["user"]}</strong>.</p>
            <p style="color:#555">Questa è una simulazione per il progetto universitario.</p>
            <a href="/logout" style="color:#06c">Disconnettiti</a>
        </div>
    '''


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
