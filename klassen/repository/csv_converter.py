import datetime
import logging

from klassen.domain.modul import Modul
from klassen.domain.pruefungsleistung import Pruefungsleistung
from klassen.domain.semester import Semester
from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_note import NotenZiel
from klassen.domain.ziel_zeit import ZeitZiel


class StudiengangCSVConverter:
    @staticmethod
    def deserialisieren(csv_read):
        """ Wandelt Daten aus CSV-Datei in einen Studiengang um. """
        # Standardwerte
        start_datum = datetime.datetime.now()
        titel = "Neuer Studiengang"
        logging.info("Versuche CSV-Datei einzulesen.")
        # Prüfen ob CSV-Datei existiert, wenn ja, öffnen und einlesen
        semester_dict = {}
        for zeile in csv_read:
            # Moduldaten zeilenweise einlesen und zwischenspeichern
            sem_num = int(zeile['Semester'])
            mod_titel = zeile['Modul']
            mod_credits = int(zeile['ECTS'])
            mod_pruefung_str = zeile['Pruefungsleistung']
            # Objekte erstellen
            pruefungsleistung = Pruefungsleistung(mod_pruefung_str)
            modul = Modul(mod_titel, mod_credits, pruefungsleistung)
            # Semester anlegen, wenn es nicht existiert
            if sem_num not in semester_dict:
                semester_dict[sem_num] = []
            # Modul dem Semester hinzufügen
            semester_dict[sem_num].append(modul)
        if not semester_dict:
            logging.info("CSV-Datei nicht vorhanden. Erstelle einen leeren Studiengang.")
        # Wenn keine CSV-Datei existiert ist semester_dict leer, somit wird semester_list ebenfalls leer
        semester_list = []
        for num in sorted(semester_dict.keys()):
            semester_list.append(Semester(num, semester_dict[num]))
        # Ziele auf 0 setzen
        ziele_dict = {
            "zeit": ZeitZiel(int(0)),
            "note": NotenZiel(float(0.0))
        }
        logging.info("Neuer Studiengang erstellt.")
        # Studiengang erstellen und zurückgeben
        return Studiengang(titel, semester_list, start_datum, ziele_dict)