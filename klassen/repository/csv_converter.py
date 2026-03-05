import datetime
import logging

from klassen.domain.modul import Modul
from klassen.domain.pruefungsleistung import Pruefungsleistung
from klassen.domain.semester import Semester
from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_note import NotenZiel
from klassen.domain.ziel_zeit import ZeitZiel


class StudiengangCSVConverter:
    """ Erstellt einen Studiengang, liest optional eine CSV-Datei ein """
    @staticmethod
    def deserialisieren(csv_read):
        """ Wandelt Daten aus CSV-Datei in Module um """
        # Standardwerte setzen, welche nicht in der CSV-Datei stehen (müssen im Webinterface angepasst werden)
        start_datum = datetime.datetime.now() # Aktuelles Datum als Start-Datum setzen
        # Ziele auf 0 setzen
        ziele_dict = {
            "zeit": ZeitZiel(int(0)),
            "note": NotenZiel(float(0.0))
        }
        titel = "Neuer Studiengang"
        # Dictionary für die Semester Daten erstellen
        semester_dict = {}
        # Semester Liste erstellen
        semester_list = []
        # Wenn Daten erhalten dann Zeile für Zeile auslesen
        if csv_read:
            logging.info("Erstelle Studiengang aus CSV-Datei.")
            for zeile in csv_read:
                # Moduldaten zeilenweise einlesen und in einem Dictionary zwischenspeichern
                sem_num = int(zeile['Semester'])
                mod_titel = zeile['Modul']
                mod_credits = int(zeile['ECTS'])
                mod_pruefung_str = zeile['Pruefungsleistung']
                # Prüfungsleistung erstellen
                pruefungsleistung = Pruefungsleistung(mod_pruefung_str)
                # Modul erstellen
                modul = Modul(mod_titel, mod_credits, pruefungsleistung)
                # Semester als Liste anlegen, wenn es nicht existiert
                if sem_num not in semester_dict:
                    semester_dict[sem_num] = []
                # Modul dem Semester hinzufügen
                semester_dict[sem_num].append(modul)
            # Aus den eingelesenen Daten Semester Objekte erstellen und an die Semester Liste anhängen
            for num in sorted(semester_dict.keys()):
                semester_list.append(Semester(num, semester_dict[num]))
        else:
            logging.info("CSV-Datei nicht vorhanden. Erstelle einen leeren Studiengang.")
        logging.info("Neuer Studiengang erstellt.")
        # Studiengang erstellen und zurückgeben
        return Studiengang(titel,start_datum, semester_list, ziele_dict)