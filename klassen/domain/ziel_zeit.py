from dataclasses import dataclass

from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_interface import Ziel


@dataclass
class ZeitZiel(Ziel):
    """ Gibt die Ziel-Zeit in Tagen an """
    zeitziel_in_tagen: int

    def ist_ziel_erreicht(self, studiengang: Studiengang):
        """ Prüft, ob das ZeitZiel aktuell erreicht ist """
        return bool(studiengang.berechne_vergangene_tage() <= self.zeitziel_in_tagen)
