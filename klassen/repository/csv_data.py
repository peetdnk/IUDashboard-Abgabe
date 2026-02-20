import csv
import logging
import os

from dotenv import dotenv_values

from klassen.repository.csv_converter import StudiengangCSVConverter
from klassen.repository.interface import StudiengangRepository

config = dotenv_values("app.config")

csv_file = config["CSV_FILE"]
converter = StudiengangCSVConverter()


class StudiengangCSVData(StudiengangRepository):

    def laden(self):
        """ Semester & Module aus CSV-Datei auslesen """
        logging.info("Versuche CSV-Datei " + str(csv_file) + " einzulesen.")
        data = []
        if os.path.exists(csv_file):
            with open(csv_file, newline='', encoding='utf-8') as csvfile:
                csv_read = csv.DictReader(csvfile)
                data = list(csv_read)
        return converter.deserialisieren(data)

    def speichern(self, studiengang):
        """ Speichern in CSV-Datei. Nicht erlaubt. """
        return NotImplemented
