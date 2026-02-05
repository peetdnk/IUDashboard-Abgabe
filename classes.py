import csv
import datetime
import json
import logging
import os
from abc import abstractmethod, ABCMeta
from werkzeug.datastructures import MultiDict


class Pruefungsleistung:
    """ Prüfung eines Moduls """
    def __init__(self, pruefungsart: str):
        self.pruefungsart = pruefungsart
        self.note = None

    def setze_note(self, note: float):
        """ Note für die Prüfung eintragen """
        self.note = note


class Modul:
    """ Module des Semesters mit Prüfungsleistung """
    def __init__(self, titel: str, modul_credits: int, pruefungsleistung: Pruefungsleistung):
        self.titel = titel
        self.credits = modul_credits
        self.pruefungsleistung = pruefungsleistung


class Semester:
    """ Semester des Studiengangs mit Modulen """
    def __init__(self, nummer: int, module: list[Modul]):
        self.nummer = nummer
        self.module = module

    def hole_modul_noten(self):
        """ Trägt alle eingetragenen Noten der Module des Semesters zusammen """
        return [n.pruefungsleistung.note for n in self.module if n.pruefungsleistung.note is not None]

    def berechne_modul_credits(self):
        """ Addiert die ECTS-Werte der Module des Semesters, wenn eine Note eingetragen ist """
        erreichte_credits = 0
        for n in self.module:
            if n.pruefungsleistung.note is not None:
                erreichte_credits += n.credits
        return erreichte_credits


class Studiengang:
    """ Stellt den Studiengang mit Semestern und Modulen dar """
    def __init__(self, titel: str, semester: list[Semester], start_datum: datetime.datetime, ziele: dict = None):
        self.titel = titel
        self.semester = semester
        self.start_datum = start_datum
        self.ziele = ziele if ziele is not None else {}

    def berechne_notendurchschnitt(self):
        """ Berechnet den Notendurchschnitt der eingetragenen Noten """
        notenliste = []
        notendurchschnitt = 0.0
        for semester in self.semester:
            notenliste = notenliste + semester.hole_modul_noten()
        try:
            for durchschnitt in notenliste:
                notendurchschnitt += durchschnitt
            notendurchschnitt = notendurchschnitt / len(notenliste)
            return round(notendurchschnitt, 1)
        except ZeroDivisionError:
            return 0.0

    def berechne_abgeschlossene_module(self):
        """ Berechnet wie viele Module abgeschlossen sind (Note eingetragen) """
        abgeschlossene_module = 0
        for semester in self.semester:
            for note in semester.hole_modul_noten():
                if note is not None:
                    abgeschlossene_module += 1
        return abgeschlossene_module

    def berechne_erreichte_credits(self):
        """ Berechnet wie viele Credits durch abgeschlossene Module erreicht wurden """
        erreichte_credits = 0
        for semester in self.semester:
            erreichte_credits += semester.berechne_modul_credits()
        return erreichte_credits

    def berechne_vergangene_tage(self):
        """ Berechnet die Tage seit eingetragenem Studienbeginn """
        return (datetime.datetime.now() - self.start_datum).days


class Ziel(metaclass=ABCMeta):
    """ Abstrakte Methode für Ziele """
    @abstractmethod
    def ist_ziel_erreicht(self, studiengang: Studiengang):
        pass


class ZeitZiel(Ziel):
    """ Gibt die Ziel-Zeit in Tagen an """
    def __init__(self, zeitziel_in_tagen: int):
        self.zeitziel_in_tagen = zeitziel_in_tagen

    def ist_ziel_erreicht(self, studiengang: Studiengang):
        """ Prüft, ob das ZeitZiel aktuell erreicht ist """
        return bool(studiengang.berechne_vergangene_tage() <= self.zeitziel_in_tagen)


class NotenZiel(Ziel):
    """ Gibt den Ziel-Notenschnitt an """
    def __init__(self, notenschnitt: float):
        self.notenschnitt = notenschnitt

    def ist_ziel_erreicht(self, studiengang: Studiengang):
        """ Prüft, ob das NotenZiel aktuell erreicht ist """
        return bool(studiengang.berechne_notendurchschnitt() <= self.notenschnitt)


class StudiengangUIHelfer:
    """ Bereitet Daten des Studiengangs für das GUI auf """
    @staticmethod
    def credits_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der erreichten ECTS für das GUI """
        gesamt_credits = 0
        for semester in studiengang.semester:
            for modul in semester.module:
                gesamt_credits += modul.credits
        try:
            fortschritt = studiengang.berechne_erreichte_credits() / gesamt_credits * 100
        except ZeroDivisionError:
            fortschritt = 0
        return fortschritt

    @staticmethod
    def modul_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der abgeschlossenen Module für das GUI """
        gesamt_module = 0
        for semester in studiengang.semester:
            gesamt_module += len(semester.module)
        try:
            fortschritt = studiengang.berechne_abgeschlossene_module() / gesamt_module * 100
        except ZeroDivisionError:
            fortschritt = 0
        return fortschritt

    @staticmethod
    def zeit_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der vergangenen Tage bezogen auf das ZeitZiel für das GUI """
        try:
            zeit_fortschritt = min(
                studiengang.berechne_vergangene_tage() / studiengang.ziele['zeit'].zeitziel_in_tagen * 100, 100)
            if zeit_fortschritt < 0:
                zeit_fortschritt = 0
        except ZeroDivisionError:
            zeit_fortschritt = 0
        return zeit_fortschritt

    @staticmethod
    def ziel_fortschritt_farbe(ziel: str, studiengang: Studiengang):
        """ Gibt die Farbe des Zielbalkens an - erreicht=grün, nicht erreicht=rot - anwendbar auf alle Ziele"""
        if not studiengang.ziele[ziel].ist_ziel_erreicht(studiengang):
            balken_farbe = "#ff6666"
        else:
            balken_farbe = "#aaddaa"
        return balken_farbe


class StudiengangManager:
    """ Übernimmt das Erstellen, Speichern und Laden eines Studiengangs """
    def __init__(self, json_file='data.json', csv_file='studienablaufplan.csv'):
        self.json_file = json_file
        self.csv_file = csv_file

    def hole_studiengang(self) -> Studiengang:
        """
        Haupteinstiegspunkt: Versucht JSON zu laden, falls nicht vorhanden,
        wird aus CSV importiert oder leer erstellt und gespeichert.
        """
        studiengang = self._laden_aus_json()
        if studiengang is None:
            studiengang = self._neu_erstellen()
            self.speichern_in_json(studiengang)
        return studiengang

    def speichern_in_json(self, studiengang: Studiengang):
        """ Serialisiert den Studiengang in JSON und speichert in eine Datei """

        # JSON-String vorbereiten
        data = {
            "titel": studiengang.titel,
            "start_datum": studiengang.start_datum.isoformat(),
            "ziele": {
                "zeit_tage": studiengang.ziele['zeit'].zeitziel_in_tagen,
                "noten_schnitt": studiengang.ziele['note'].notenschnitt,
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
                    "pruefungsleistung": modul.pruefungsleistung.pruefungsart
                }
                semester_data["module"].append(modul_data)
            data["semester"].append(semester_data)
        # JSON-String in Datei schreiben
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            logging.info("Studiengang in JSON-Datei gespeichert.")

    def _neu_erstellen(self) -> Studiengang:
        """Intern: Liest CSV ein oder erstellt einen leeren Studiengang, falls CSV fehlt."""
        logging.info("Kein JSON gefunden. Versuche aus CSV zu erstellen.")
        semester_dict = {}
        # Standardwerte
        start_datum = datetime.datetime.now()
        titel = "Neuer Studiengang"
        logging.info("Versuche CSV-Datei " + str(self.csv_file) + " einzulesen.")
        # Prüfen ob CSV-Datei existiert, wenn ja, öffnen und zeilenweise einlesen
        if os.path.exists(self.csv_file):
            with open(self.csv_file, newline='', encoding='utf-8') as csvfile:
                csv_read = csv.DictReader(csvfile)
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
        else:
            logging.info("CSV-Datei " + str(self.csv_file) + " nicht vorhanden. Erstelle einen leeren Studiengang.")
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

    def _laden_aus_json(self):
        """Intern: Lädt JSON und rekonstruiert Objekte."""
        # Prüfen ob JSON-Datei existiert, wenn nicht abbrechen und None zurückgeben
        if not os.path.exists(self.json_file):
            return None
        # JSON-Datei laden und inhalt in daten speichern
        with open(self.json_file, 'r', encoding='utf-8') as f:
            daten = json.load(f)
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

    def aktualisieren_aus_formular(self, studiengang: Studiengang, form_data: MultiDict):
        """Aktualisiert ein Studiengang-Objekt aus dem WebFormular und speichert es."""
        # Werte aus dem Formular extrahieren und den einzelnen Objekten zuweisen
        studiengang.titel = form_data.get('studien_titel', studiengang.titel)
        start_datum_raw = form_data.get('start_datum')
        if start_datum_raw:
            # Konvertierung des Datums
            try:
                studiengang.start_datum = datetime.datetime.strptime(start_datum_raw, '%Y-%m-%d')
            except ValueError:
                logging.error(f"Datum konnte nicht gelesen werden: {start_datum_raw}")

        try:
            # Ziele lesen - Standardwerte, falls keine vorhanden und schreiben in Studiengang-Objekt
            neue_tage = int(form_data.get('ziel_tage', 2190))
            neue_note = float(form_data.get('ziel_note', '2.5').replace(',', '.'))
            # Jahre in Tage umrechnen wenn Eingabe kleiner oder gleich 12
            if neue_tage <= 12:
                neue_tage = neue_tage * 365
            studiengang.ziele['zeit'] = ZeitZiel(neue_tage)
            # Prüfen, ob der neue Notenschnitt plausible Werte, wenn nicht Standardwert
            if 1.0 >= neue_note <= 6.0:
                studiengang.ziele['note'] = NotenZiel(neue_note)
            else:
                studiengang.ziele['note'] = NotenZiel(2.5)
        except (ValueError, TypeError):
            logging.error("Fehler beim Konvertieren der Ziele.")

        # Module rekonstruieren - Listen für jede Spalte der Eingabefelder erstellen
        titel_liste = form_data.getlist('mod_titel')
        sem_liste = form_data.getlist('mod_semester')
        pruefung_liste = form_data.getlist('mod_pruefung')
        credits_liste = form_data.getlist('mod_credits')
        noten_liste = form_data.getlist('mod_note')
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

                # Note sicher verarbeiten
                note_aus_form = noten_liste[i].strip().replace(',', '.')
                noten_wert = None
                if note_aus_form and note_aus_form != "":
                    try:
                        noten_wert = float(note_aus_form)
                    except ValueError:
                        noten_wert = None

                # Modul zusammenbauen
                pl = Pruefungsleistung(pruefung_typ)
                if noten_wert is not None:
                    pl.setze_note(noten_wert)

                modul = Modul(titel, mod_credits, pl)
                # Wenn Semester nicht im Dictionary, neu erstellen
                if sem_num not in neue_semester_struktur:
                    neue_semester_struktur[sem_num] = []
                # Modul an Semester anhängen
                neue_semester_struktur[sem_num].append(modul)

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
        self.speichern_in_json(studiengang)
