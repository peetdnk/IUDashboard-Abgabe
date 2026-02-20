import logging
import os

from dotenv import dotenv_values
from flask import json

from klassen.domain.studiengang import Studiengang
from klassen.repository.interface import StudiengangRepository
from klassen.repository.json_converter import StudiengangJSONConverter

config = dotenv_values("app.config")

json_file = config["JSON_FILE"]
converter = StudiengangJSONConverter()


class StudiengangJSONData(StudiengangRepository):
    """ Übernimmt das Speichern und Laden einer JSON-Datei """

    def speichern(self, studiengang: Studiengang):
        """ Speichert den serialisierten Studiengang in eine Datei """
        data = converter.serialisieren(studiengang)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info("Studiengang in JSON-Datei gespeichert.")

    def laden(self):
        """ Lädt Studiengang aus einer JSON-Datei """
        # Prüfen ob JSON-Datei existiert, wenn nicht abbrechen und None zurückgeben
        if not os.path.exists(json_file):
            return None
        # JSON-Datei laden und inhalt in daten speichern
        with open(json_file, 'r', encoding='utf-8') as f:
            daten = json.load(f)
        return converter.deserialisieren(daten)

