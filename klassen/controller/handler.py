import datetime
import logging

from werkzeug.datastructures import MultiDict

from klassen.domain.modul import Modul
from klassen.domain.pruefungsleistung import Pruefungsleistung
from klassen.domain.semester import Semester
from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_note import NotenZiel
from klassen.domain.ziel_zeit import ZeitZiel


class StudiengangHandler:
    @staticmethod
    def aktualisieren_aus_formular(studiengang: Studiengang, form_data: MultiDict, manager):
        """Aktualisiert ein Studiengang-Objekt aus dem WebFormular"""
        # Werte aus dem Formular extrahieren und den einzelnen Objekten zuweisen
        studiengang.titel = form_data.get('studien_titel', studiengang.titel)
        start_datum_raw = form_data.get('start_datum')
        try:
            studiengang.start_datum = datetime.datetime.strptime(start_datum_raw, '%Y-%m-%d')
        except ValueError:
            logging.error(f"Datum konnte nicht gelesen werden: {start_datum_raw}")
        try:
            # Ziele lesen - Standardwerte, falls keine vorhanden und schreiben in Studiengang-Objekt
            neue_tage = int(form_data.get('ziel_tage', 0))
            neue_note = float(form_data.get('ziel_note', '0').replace(',', '.'))
            # Jahre in Tage umrechnen wenn Eingabe kleiner oder gleich 12
            if neue_tage <= 12:
                neue_tage = neue_tage * 365
            # Zeit-Ziel setzen
            studiengang.ziele['zeit'] = ZeitZiel(neue_tage)
            # prüfen, ob der neue Notenschnitt plausible Werte hat, wenn nicht Standardwert
            if neue_note >= 1.0 and neue_note <= 6.0:
                studiengang.ziele['note'] = NotenZiel(neue_note)
            else:
                studiengang.ziele['note'] = NotenZiel(0.0)
        except (ValueError, TypeError):
            logging.error("Fehler bei Konvertieren der Ziele.")

        # Module rekonstruieren - Listen für jede Spalte der Eingabefelder erstellen
        titel_liste = form_data.getlist('mod_titel')
        sem_liste = form_data.getlist('mod_semester')
        pruefung_liste = form_data.getlist('mod_pruefung')
        credits_liste = form_data.getlist('mod_credits')
        noten_liste = form_data.getlist('mod_note')
        check_liste = form_data.getlist('mod_check')
        # neues Dictionary anlegen
        neue_semester_struktur = {}
        # durch erstellte Listen auf Basis der Länge iterieren
        for i in range(len(titel_liste)):
            try:
                # einzelne Moduldaten aus Listen extrahieren
                titel = titel_liste[i]
                sem_num = int(sem_liste[i])
                mod_credits = int(credits_liste[i])
                pruefung_typ = pruefung_liste[i]

                # Note sicher verarbeiten - aus , wird . gemacht
                note_aus_form = noten_liste[i].strip().replace(',', '.')
                noten_wert = None
                if note_aus_form != "":
                    try:
                        # versuchen Wert in float zu wandeln und Fehler abfangen
                        noten_wert = float(note_aus_form)
                    except ValueError:
                        noten_wert = None

                # Prüfungsleistung und Modul zusammenbauen
                pl = Pruefungsleistung(pruefung_typ)
                pl.setze_anerkannt(False)
                if noten_wert is not None:
                    pl.setze_note(noten_wert)
                # Wenn im Formular "Anerk." angeklickt wurde Attribut anerkannt auf True setzen
                if check_liste[i] == "on":
                    pl.setze_anerkannt(True)
                modul = Modul(titel, mod_credits, pl)
                # Wenn Semester nicht im Dictionary vorhanden ist neu erstellen
                if sem_num not in neue_semester_struktur:
                    neue_semester_struktur[sem_num] = []
                # Modul an Semester anhängen
                neue_semester_struktur[sem_num].append(modul)
            # Fehler abfangen, wenn nicht alle Listen gleichgroß sind.
            except (IndexError, ValueError) as e:
                logging.error(f"Fehler bei Modul-Index {i}: {e}")
                continue

        # Semester dem Studiengang Objekt zuweisen - leere Liste erstellen
        neue_semester_liste = []
        # durch das Dictionary iterieren, Semester Objekte erstellen und der Liste hinzufügen
        for semester_num in sorted(neue_semester_struktur.keys()):
            neue_semester_liste.append(Semester(semester_num, neue_semester_struktur[semester_num]))
        # Semester-Liste dem Studiengang zuweisen und an die Speichern Methode übergeben
        studiengang.semester = neue_semester_liste
        # Weitergabe des Studiengang-Objekts an den Manager zum Aktualisieren über Interface
        manager.studiengang_aktualisieren(studiengang)