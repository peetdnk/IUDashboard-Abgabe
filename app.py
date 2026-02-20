import logging
import os

from flask.cli import load_dotenv
from flask import Flask, request, session

from klassen.controller.handler import StudiengangHandler
from klassen.controller.service.manager import StudiengangManager
from klassen.controller.service.service import StudiengangService
from klassen.repository.csv_data import StudiengangCSVData
from klassen.repository.json_data import StudiengangJSONData
from klassen.view.view import StudiengangAnsicht

# Variablen für secret_key und Kennwort aus .env Datei laden
load_dotenv()
# Erstellen des Haupt-Objekts
dashboard_app = Flask(__name__)
# Notwendig für Session-Cookie und Flash-Nachrichten
dashboard_app.secret_key = os.getenv("SECRET_KEY")

# Kennwort als Hash-Wert für die Login-Seite aus .env Datei lesen
password = os.getenv("PASSWORD_HASH")

# Instanziierung Studiengangverwaltung
speicher = StudiengangJSONData()
importer = StudiengangCSVData()
service = StudiengangService()
manager = StudiengangManager(speicher, importer)
handler = StudiengangHandler()
ansicht = StudiengangAnsicht()

# Logging Konfiguration, Ausgabe in Datei, Datei wird bei jedem Start überschrieben, nur Fehler werden geschrieben, Formatierung
logging.basicConfig(filename='dashboard.log', filemode='w', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# Dashboard
@dashboard_app.route('/')
def dashboard():
    # Studiengang Laden oder Erstellen.
    # Rückgabe der Dashboardseite inklusive Variablen Zuweisung vom Studiengang zum HTML.
    return ansicht.dashboard(manager, service)


# Login
@dashboard_app.route('/login', methods=['GET', 'POST'])
def login():
    return ansicht.login(session, request, password)


# Logout
@dashboard_app.route('/logout')
def logout():
    # Session-Cookie löschen und zum Dashboard weiterleiten
    return ansicht.logout(session)


# Bearbeiten
@dashboard_app.route('/edit', methods=['GET', 'POST'])
def bearbeiten():
    # Wenn Session-Cookie nicht da ist, wird an die Seite zum Login weitergeleitet
    return ansicht.bearbeiten(session, request, handler, manager)


# Auf allen verfügbaren Netzwerk-Schnittstellen auf Port 80 lauschen
if __name__ == '__main__':
    dashboard_app.run(host="0.0.0.0", port=80)
