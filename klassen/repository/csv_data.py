import csv
import logging
import os

from dotenv import dotenv_values

from klassen.repository.csv_converter import StudiengangCSVConverter
from klassen.repository.interface import IStudiengangRepository

# Konfigurationsdatei laden
config = dotenv_values("app.config")
# Dateinamen der CSV-Datei aus Konfiguration lesen
csv_filename = config["CSV_FILE"]
# Konverter initialisieren
converter = StudiengangCSVConverter()


class StudiengangCSVData(IStudiengangRepository):
    """ Liest Daten aus CSV-Datei aus """
    def laden(self):
        """ Semester & Module aus CSV-Datei auslesen """
        logging.info("Versuche CSV-Datei " + str(csv_filename) + " einzulesen.")
        # Liste für Daten erstellen
        data = []
        if os.path.exists(csv_filename):
            # Datei öffnen, wenn vorhanden
            with open(csv_filename, newline='', encoding='utf-8') as csv_file:
                # CSV Daten auslesen
                csv_read = csv.DictReader(csv_file)
                # Daten in die Liste schreiben
                data = list(csv_read)
        # Rückgabe der konvertierten Daten nach Aufruf des Konverters (Studiengang-Objekt)
        return converter.deserialisieren(data)

    def speichern(self, studiengang):
        """ Speichern in CSV-Datei. Nicht erlaubt. """
        # Funktion ist nicht implementiert.
        return NotImplemented
