import datetime
from dataclasses import field, dataclass

from klassen.domain.semester import Semester

@dataclass
class Studiengang:
    """ Stellt den Studiengang mit Semestern und Modulen dar """
    titel: str
    start_datum: datetime.datetime # Beginn des Studiengangs
    # default_factory erzeugt bei jedem neuen Objekt eine neue Liste/Dict
    semester: list["Semester"] = field(default_factory=list) # Liste von Semestern
    ziele: dict = field(default_factory=dict) # Dictionary von Zielen

    def berechne_notendurchschnitt(self):
        """ Berechnet den Notendurchschnitt der eingetragenen Noten """
        notenliste = []
        notendurchschnitt = 0.0
        # trägt alle Noten der Module aus den Semestern in einer Liste zusammen
        for semester in self.semester:
            notenliste = notenliste + semester.hole_modul_noten()
        # versucht Notenschnitt zu berechnen, wenn keine Noten eingetragen sind, ist mit einer Division durch 0 zu rechnen da die Notenliste in diesem Fall leer ist
        try:
            # iteriert über zuvor erstellte Notenliste und addiert Noten
            for note in notenliste:
                notendurchschnitt += note
            # Division der addierten Noten durch die Länge der Notenliste
            notendurchschnitt = notendurchschnitt / len(notenliste)
            # gerundeten Wert zurückgeben
            return round(notendurchschnitt, 1)
        except ZeroDivisionError:
            # Wenn Notenliste leer dann 0.0 zurückgeben
            return 0.0

    def berechne_abgeschlossene_module(self):
        """ Berechnet wie viele Module abgeschlossen sind (Note eingetragen) """
        abgeschlossene_module = 0
        # iteriert über Semester-Liste
        for semester in self.semester:
            # iteriert über die Liste der Noten aus einem Semester
            for note in semester.hole_modul_noten():
                # wenn Note eingetragen und kleiner gleich 4 ist, wird abgeschlossene_module um 1 erhöht
                if note is not None and note <= 4:
                    abgeschlossene_module += 1
            # iteriert über anerkannte Module des Semesters, erhöht für jedes anerkannte Modul abgeschlossene_module um 1
            for _ in semester.hole_anerkannte_module():
                abgeschlossene_module += 1
        return abgeschlossene_module

    def berechne_erreichte_credits(self):
        """ Berechnet wie viele Credits durch abgeschlossene Module erreicht wurden """
        erreichte_credits = 0
        # iteriert über die Semester-Liste und addiert die ECTS-Werte der Module
        for semester in self.semester:
            erreichte_credits += semester.berechne_modul_credits()
        return erreichte_credits

    def berechne_vergangene_tage(self):
        """ Berechnet die Differenz in Tagen von Heute zum eingetragenem Studienbeginn """
        # berechnet die Differenz des aktuellen Datums und des Start-Datums
        return (datetime.datetime.now() - self.start_datum).days
