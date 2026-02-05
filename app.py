import logging
import os

from flask.cli import load_dotenv
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from classes import StudiengangManager, StudiengangUIHelfer

# Variablen für secret_key und Kennwort aus .env Datei laden
load_dotenv()
# Erstellen des Haupt-Objekts
app = Flask(__name__)
# Notwendig für Session-Cookie und Flash-Nachrichten
app.secret_key = os.getenv("SECRET_KEY")

# Kennwort als Hash-Wert für die Login-Seite aus .env Datei lesen
PASSWORD = os.getenv("PASSWORD_HASH")

# Instanziierung StudiengangManager und StudiengangUIHelfer
manager = StudiengangManager()
uihelfer = StudiengangUIHelfer()

# Logging Konfiguration, Ausgabe in Datei, Datei wird bei jedem Start überschrieben, nur Fehler werden geschrieben, Formatierung
logging.basicConfig(filename='dashboard.log', filemode='w', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Dashboard
@app.route('/')
def dashboard():
    # Studiengang Laden oder Erstellen.
    # Rückgabe der Dashboardseite inklusive Variablen Zuweisung vom Studiengang zum HTML.
    studiengang = manager.hole_studiengang()
    return render_template(
        'dashboard.html',
        sg=manager.hole_studiengang(),
        tage_vergangen=studiengang.berechne_vergangene_tage(),
        tage_ziel=studiengang.ziele['zeit'].zeitziel_in_tagen,
        zeitbalken_fortschritt=uihelfer.zeit_fortschritt(studiengang),
        zeitbalken_farbe=uihelfer.ziel_fortschritt_farbe('zeit', studiengang),
        module_abgeschlossen=studiengang.berechne_abgeschlossene_module(),
        erreichte_credits=studiengang.berechne_erreichte_credits(),
        notenschnitt_aktuell=f"{studiengang.berechne_notendurchschnitt():.1f}".replace('.', ','),
        notenschnitt_ziel=f"{studiengang.ziele['note'].notenschnitt:.1f}".replace('.', ','),
        notenbalken_farbe=uihelfer.ziel_fortschritt_farbe('note', studiengang),
        credit_fortschritt=uihelfer.credits_fortschritt(studiengang),
        module_fortschritt=uihelfer.modul_fortschritt(studiengang)
    )

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Kennwortabfrage wenn "Login" gedrückt wird
        if check_password_hash(PASSWORD, request.form['password']):
            # Wenn das eingegebene Kennwort mit dem Hash übereinstimmt, wird ein Session-Cookie gesetzt und an die Seite zum Bearbeiten weitergeleitet.
            session['logged_in'] = True
            logging.info("Benutzer erfolgreich eingeloggt.")
            return redirect(url_for('bearbeiten'))
        else:
            # Wenn Kennwort nicht stimmt, Variable error setzen und Fehler ausgeben.
            error = 'Falsches Passwort'
            logging.warning("Benutzer hat ein falsches Passwort verwendet.")
    return render_template('login.html', error=error)

# Logout
@app.route('/logout')
def logout():
    # Session-Cookie löschen und zum Dashboard weiterleiten
    session.pop('logged_in', None)
    logging.info("Benutzer erfolgreich ausgeloggt.")
    return redirect(url_for('dashboard'))

# Bearbeiten
@app.route('/edit', methods=['GET', 'POST'])
def bearbeiten():
    # Wenn Session-Cookie nicht da ist, wird an die Seite zum Login weitergeleitet
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Studiengang laden
    studiengang = manager.hole_studiengang()
    if request.method == 'POST':
        # Nach drücken auf Speichern wird versucht den Studiengang aus den Formulardaten zu aktualisieren.
        # Tritt kein Fehler wird eine positive Meldung gespeichert und auf der Hauptseite angezeigt.
        try:
            manager.aktualisieren_aus_formular(studiengang, request.form)
            flash("Änderungen erfolgreich gespeichert!", "success")
            return redirect(url_for('dashboard'))
        # Bei Fehler wird eine negative Meldung gespeichert und ausgegeben. Der Fehler wird in die Log-Datei geschrieben.
        except Exception as e:
            fehlermeldung = f"Speichern fehlgeschlagen: dashboard.log überprüfen."
            flash(fehlermeldung, 'danger')
            logging.error({str(e)})
            # erneutes ausgeben der bearbeiten.html mit den alten Werten.
            return render_template(
                'bearbeiten.html',
                sg=studiengang,
                ziel_tage=studiengang.ziele['zeit'].zeitziel_in_tagen,
                ziel_note=studiengang.ziele['note'].notenschnitt
            )
    return render_template(
        'bearbeiten.html',
        sg=studiengang,
        ziel_tage=studiengang.ziele['zeit'].zeitziel_in_tagen,
        ziel_note=studiengang.ziele['note'].notenschnitt
    )

# Auf allen verfügbaren Netzwerk-Schnittstellen auf Port 80 lauschen
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
