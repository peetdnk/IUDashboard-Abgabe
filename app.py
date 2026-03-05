import logging

from dotenv import dotenv_values
from flask import Flask, request, session

from klassen.controller.handler import StudiengangHandler
from klassen.controller.service.manager import StudiengangManager
from klassen.controller.service.service import StudiengangService
from klassen.repository.csv_data import StudiengangCSVData
from klassen.repository.json_data import StudiengangJSONData
from klassen.view.view import StudiengangAnsicht

# Konfigurationsdatei laden
config = dotenv_values("app.config")

# Erstellen des Haupt-Objekts
dashboard_app = Flask(__name__)
# Notwendig für Session-Cookie und Flash-Nachrichten
dashboard_app.secret_key = config["SECRET_KEY"]

# Kennwort als Hash-Wert für die Login-Seite aus .env Datei lesen
password = config["PASSWORD_HASH"]

# Instanziierung Studiengangverwaltung
speicher = StudiengangJSONData() # Speichern und Laden im JSON Format
importer = StudiengangCSVData() # Laden der CSV-Datei
service = StudiengangService() # Berechnungen zum Studiengang (bspw. abgeschlossene Module)
manager = StudiengangManager(speicher, importer) # Verwaltet den Studiengang, erstellt, lädt, speichert
handler = StudiengangHandler() # Aktualisierung über Webformular
ansicht = StudiengangAnsicht() # Gibt die Flask Templates zur Ansicht aus (HTML)

# Logging Konfiguration, Ausgabe in Datei, Datei wird bei jedem Start überschrieben, nur Fehler werden geschrieben, Formatierung
logging.basicConfig(filename='dashboard.log', filemode='w', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


# Dashboard
@dashboard_app.route('/')
def dashboard():
    # Aufruf der Ansicht -> Rückgabe: Flask Template für das Dashboard
    # manager -> Laden des Studiengangs
    # service -> Berechnungen für das Dashboard
    return ansicht.dashboard(manager, service)


# Login
@dashboard_app.route('/login', methods=['GET', 'POST'])
def login():
    # Aufruf der Ansicht für den Login -> Rückgabe: Flask Template für Login Seite
    # session -> Speichern des Cookies für Login
    # request -> GET zum Anzeigen der Seite, POST für Login
    # password -> Authentifizierung des Users, wird aus Config als Hash geladen
    return ansicht.login(session, request, password)


# Logout
@dashboard_app.route('/logout')
def logout():
    # Aufruf der Ansicht für Logout -> Rückgabe: Weiterleitung zum Dashboard
    # session -> löschen des Cookies für Login
    return ansicht.logout(session)


# Bearbeiten
@dashboard_app.route('/edit', methods=['GET', 'POST'])
def bearbeiten():
    # Aufruf der Ansicht für Bearbeiten -> Rückgabe: Flask-Template fürs Bearbeiten oder Weiterleitung zum Login
    # session -> Prüfung, ob Authentifiziert
    # request -> GET zum Anzeigen der Seite, POST für Aktualisierung der Daten
    # handler -> verantwortlich für die Weitergabe der Daten nach Aktualisierung über Webformular
    # manager -> Laden des Studiengangs
    return ansicht.bearbeiten(session, request, handler, manager)


# Auf allen verfügbaren Netzwerk-Schnittstellen auf Port 5000 lauschen
if __name__ == '__main__':
    dashboard_app.run(host="0.0.0.0", port=5000)
