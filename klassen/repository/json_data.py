import logging
import os

from dotenv import dotenv_values
from flask import json

from klassen.domain.studiengang import Studiengang
from klassen.repository.interface import IStudiengangRepository
from klassen.repository.json_converter import StudiengangJSONConverter
# Konfigurationsdatei laden
config = dotenv_values("app.config")
# Dateinamen der JSON-Datei aus Konfiguration lesen
json_filename = config["JSON_FILE"]
# Konverter initialisieren
converter = StudiengangJSONConverter()


class StudiengangJSONData(IStudiengangRepository):
    """ Übernimmt das Speichern und Laden einer JSON-Datei """

    def speichern(self, studiengang: Studiengang):
        """ Speichert den serialisierten Studiengang in eine Datei """
        # Konverter aufrufen und Rückgabe-Daten in data speichern
        data = converter.serialisieren(studiengang)
        # JSON-Datei öffnen, wenn nicht vorhanden, erzeugen
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            # Daten mit der Funktion json.dump() in die Datei schreiben.
            json.dump(data, json_file, indent=4, ensure_ascii=False) # indent=4 -> bessere lesbarkeit, ensure_ascii=False -> keine Unicode Konvertierung
            logging.info("Studiengang in JSON-Datei gespeichert.")

    def laden(self):
        """ Lädt Studiengang aus einer JSON-Datei """
        # Prüfen ob JSON-Datei existiert, wenn nicht abbrechen und None zurückgeben
        if not os.path.exists(json_filename):
            return None
        # JSON-Datei laden und inhalt in daten speichern
        with open(json_filename, 'r', encoding='utf-8') as json_file:
            daten = json.load(json_file)
        # Konverter zum deserialiseren aufrufen und Rückgabe der von Konverter erhaltenen Daten (Studiengang Objekt)
        return converter.deserialisieren(daten)

