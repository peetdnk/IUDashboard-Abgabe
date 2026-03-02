import datetime
import logging

from klassen.domain.modul import Modul
from klassen.domain.pruefungsleistung import Pruefungsleistung
from klassen.domain.semester import Semester
from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_note import NotenZiel
from klassen.domain.ziel_zeit import ZeitZiel


class StudiengangJSONConverter:
    """ Konvertiert JSON-Daten in Dictionary und vice-versa """
    @staticmethod
    def deserialisieren(daten):
        """ Deserialisieren der JSON-Daten. Bekommt Daten und erstellt einen Studiengang. """
        # Semester Liste erstellen
        semester_liste = []
        # Durch Semester-Liste aus JSON Daten iterieren
        for sem_data in daten['semester']:
            # Modul-Liste erstellen
            modul_liste = []
            # Durch Modul-Liste innerhalb der Semester-Liste aus JSON Daten iterieren
            for mod_data in sem_data['module']:
                # Objekte anlegen und an Modul-Liste anhängen
                # Prüfungsleistung erstellen und Daten hinzufügen
                pruefungsleistung = Pruefungsleistung(mod_data['pruefungsleistung'])
                # Prüfung, ob eine Note eingetragen ist
                if mod_data['note'] is not None:
                    pruefungsleistung.setze_note(float(mod_data['note'])) # Wenn eine Note in den JSON-Daten eingetragen ist, wird diese in float gewandelt und gesetzt
                else:
                    pruefungsleistung.setze_note(mod_data['note']) # Wenn keine Note vorhanden ist, None übernehmen und setzen
                # festlegen, ob das Modul anerkannt ist
                pruefungsleistung.setze_anerkannt(bool(mod_data['anerkannt']))
                # Modul aus JSON-Daten und Prüfungsleistung erstellen
                mod = Modul(mod_data['titel'], int(mod_data['ects']), pruefungsleistung)
                # Modul an Modul-Liste anhängen
                modul_liste.append(mod)
            # Modul-Liste an Semester anhängen
            semester_liste.append(Semester(sem_data['nummer'], modul_liste))
        # Start Datum lesen konvertieren
        start_datum = datetime.datetime.fromisoformat(daten['start_datum'])
        # Ziel-Daten lesen, Standard Werte nutzen, falls keine vorhanden und in ziele_dict eintragen
        ziele_daten = daten.get("ziele", {"zeit_tage": 2190, "noten_schnitt": 2.5})
        ziele_dict = {
            "zeit": ZeitZiel(int(ziele_daten["zeit_tage"])),
            "note": NotenZiel(float(ziele_daten["noten_schnitt"]))
        }
        logging.info("Studiengang aus JSON-Datei geladen.")
        # Studiengang erstellen und zurückgeben
        return Studiengang(daten['titel'],start_datum, semester_liste, ziele_dict)

    @staticmethod
    def serialisieren(studiengang: Studiengang):
        """ Serialisiert einen Studiengang zu einem Dictionary zur Speicherung als JSON """
        # JSON-String als Dictionary vorbereiten, Titel, Start Datum, Ziele und leere Semester Liste eintragen
        json_data = {
            "titel": studiengang.titel,
            "start_datum": studiengang.start_datum.isoformat(),
            "ziele": {
                "zeit_tage": studiengang.ziele['zeit'].zeitziel_in_tagen,
                "noten_schnitt": studiengang.ziele['note'].notendurchschnitt,
            },
            "semester": []
        }
        # Modul- und Semesterdaten in das Dictionary schreiben, dazu über Semester aus Studiengang Objekt iterieren
        for semester in studiengang.semester:
            # Daten aus Semester in Dictionary schreiben, Semester Nummer und leere Liste für Module
            semester_data = {"nummer": semester.nummer, "module": []}
            # Über Module aus dem Semester Objekt iterieren
            for modul in semester.module:
                # Dictionary erstellen und mit Daten des Moduls füllen
                modul_data = {
                    "titel": modul.titel,
                    "ects": modul.credits,
                    "note": modul.pruefungsleistung.note,
                    "anerkannt": modul.pruefungsleistung.modul_anerkannt,
                    "pruefungsleistung": modul.pruefungsleistung.pruefungsart
                }
                # Modul Daten an das Semester Dictionary anhängen
                semester_data["module"].append(modul_data)
            # Semester an das Dictionary anhängen
            json_data["semester"].append(semester_data)
        # JSON-String in Datei schreiben
        return json_data