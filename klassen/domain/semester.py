from dataclasses import dataclass, field

from klassen.domain.modul import Modul


@dataclass
class Semester:
    """ Semester des Studiengangs mit Modulen """
    nummer: int
    module: list[Modul] = field(default_factory=list) # Liste von Modulen - default_factory sorgt dafür, dass jede Instanz eine eigene Liste bekommt

    def hole_modul_noten(self):
        """ Trägt alle eingetragenen Noten der Module des Semesters zusammen """
        # listet alle Noten der Modul-Liste auf, sofern nicht None. Gibt Liste zurück
        return [n.pruefungsleistung.note for n in self.module if n.pruefungsleistung.note is not None]

    def berechne_modul_credits(self):
        """ Addiert die ECTS-Werte der Module des Semesters, wenn eine Note eingetragen oder anerkannt ist """
        erreichte_credits = 0
        # iteriert über Modul-Liste
        for n in self.module:
            # addiert ECTS-Werte aus der Modul-Liste sofern nicht None, oder grö0er 4.0, oder anerkannt True ist
            if (n.pruefungsleistung.note is not None and n.pruefungsleistung.note <= 4.0) or n.pruefungsleistung.modul_anerkannt:
                erreichte_credits += n.credits
        return erreichte_credits

    def hole_anerkannte_module(self):
        """ Trägt die anerkannten Module des Semesters zusammen """
        # listet anerkannte Module aus Modul-Liste auf und gibt diese zurück
        return [n.pruefungsleistung.modul_anerkannt for n in self.module if n.pruefungsleistung.modul_anerkannt]