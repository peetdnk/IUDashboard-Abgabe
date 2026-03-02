from dataclasses import dataclass

from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_interface import IZiel


@dataclass
class NotenZiel(IZiel):
    """ Gibt den Ziel-Notenschnitt an """
    notendurchschnitt: float

    def ist_ziel_erreicht(self, studiengang: Studiengang):
        """ Prüft, ob das NotenZiel aktuell erreicht ist """
        # prüft, ob der aktuelle Notenschnitt kleiner gleich dem Ziel Notenschnitt ist
        return bool(studiengang.berechne_notendurchschnitt() <= self.notendurchschnitt)
