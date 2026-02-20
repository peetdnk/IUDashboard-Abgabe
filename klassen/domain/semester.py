from dataclasses import dataclass, field

from klassen.domain.modul import Modul


@dataclass
class Semester:
    """ Semester des Studiengangs mit Modulen """
    nummer: int
    module: list[Modul] = field(default_factory=list)

    def hole_modul_noten(self):
        """ Trägt alle eingetragenen Noten der Module des Semesters zusammen """
        return [n.pruefungsleistung.note for n in self.module if n.pruefungsleistung.note is not None]

    def berechne_modul_credits(self):
        """ Addiert die ECTS-Werte der Module des Semesters, wenn eine Note eingetragen ist """
        erreichte_credits = 0
        for n in self.module:
            if (n.pruefungsleistung.note is not None and n.pruefungsleistung.note <= 4.0) or n.pruefungsleistung.modul_anerkannt:
                erreichte_credits += n.credits
        return erreichte_credits

    def hole_anerkannte_module(self):
        """ Trägt die anerkannten Module des Semesters zusammen """
        return [n.pruefungsleistung.modul_anerkannt for n in self.module if n.pruefungsleistung.modul_anerkannt]