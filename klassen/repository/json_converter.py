import datetime
import logging

from klassen.domain.modul import Modul
from klassen.domain.pruefungsleistung import Pruefungsleistung
from klassen.domain.semester import Semester
from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_note import NotenZiel
from klassen.domain.ziel_zeit import ZeitZiel


class StudiengangJSONConverter:
    @staticmethod
    def deserialisieren(daten):
        # Semester Liste erstellen
        semester_liste = []
        # Durch Semester-Liste aus JSON Daten iterieren
        for sem_data in daten['semester']:
            # Modul-Liste erstellen
            modul_liste = []
            # Durch Modul-Liste innerhalb der Semester-Liste aus JSON Daten iterieren
            for mod_data in sem_data['module']:
                # Objekte anlegen und an Modul-Liste anhängen
                pruefungsleistung = Pruefungsleistung(mod_data['pruefungsleistung'])
                if mod_data['note'] is not None:
                    pruefungsleistung.setze_note(float(mod_data['note']))
                else:
                    pruefungsleistung.setze_note(mod_data['note'])
                if mod_data['anerkannt'] is not None:
                    pruefungsleistung.setze_anerkannt(bool(mod_data['anerkannt']))
                else:
                    pruefungsleistung.setze_anerkannt(False)
                mod = Modul(mod_data['titel'], int(mod_data['ects']), pruefungsleistung)
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
        return Studiengang(daten['titel'], semester_liste, start_datum, ziele_dict)

    @staticmethod
    def serialisieren(studiengang: Studiengang):
        # JSON-String vorbereiten
        data = {
            "titel": studiengang.titel,
            "start_datum": studiengang.start_datum.isoformat(),
            "ziele": {
                "zeit_tage": studiengang.ziele['zeit'].zeitziel_in_tagen,
                "noten_schnitt": studiengang.ziele['note'].notendurchschnitt,
            },
            "semester": []
        }
        # Modul- und Semesterdaten in den JSON-String schreiben
        for semester in studiengang.semester:
            semester_data = {"nummer": semester.nummer, "module": []}
            for modul in semester.module:
                modul_data = {
                    "titel": modul.titel,
                    "ects": modul.credits,
                    "note": modul.pruefungsleistung.note,
                    "anerkannt": modul.pruefungsleistung.modul_anerkannt,
                    "pruefungsleistung": modul.pruefungsleistung.pruefungsart
                }
                semester_data["module"].append(modul_data)
            data["semester"].append(semester_data)
        # JSON-String in Datei schreiben
        return data