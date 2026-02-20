from dataclasses import dataclass

from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_interface import Ziel


@dataclass
class NotenZiel(Ziel):
    """ Gibt den Ziel-Notenschnitt an """
    notendurchschnitt: float

    def ist_ziel_erreicht(self, studiengang: Studiengang):
        """ Prüft, ob das NotenZiel aktuell erreicht ist """
        return bool(studiengang.berechne_notendurchschnitt() <= self.notendurchschnitt)
