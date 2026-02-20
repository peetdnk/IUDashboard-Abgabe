import datetime
from dataclasses import field

from klassen.domain.semester import Semester


class Studiengang:
    """ Stellt den Studiengang mit Semestern und Modulen dar """
    def __init__(self, titel: str, semester: list[Semester], start_datum: datetime.datetime, ziele: dict = None):
        self.titel = titel
        self.semester = semester if semester else []
        self.start_datum = start_datum
        self.ziele = ziele if ziele is not None else {}

    ziele: dict = field(default_factory=dict)
    semester: list[Semester] = field(default_factory=list)

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
                if note is not None and note <= 4:
                    abgeschlossene_module += 1
            for _ in semester.hole_anerkannte_module():
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
