from dataclasses import dataclass

from klassen.domain.studiengang import Studiengang
from klassen.domain.ziel_interface import IZiel


@dataclass
class ZeitZiel(IZiel):
    """ Gibt die Ziel-Zeit in Tagen an """
    zeitziel_in_tagen: int

    def ist_ziel_erreicht(self, studiengang: Studiengang):
        """ Prüft, ob das ZeitZiel aktuell erreicht ist """
        # prüft, ob die seit dem Beginn des Studiengangs vergangenen Tage kleiner gleich dem Ziel in Tagen ist
        return bool(studiengang.berechne_vergangene_tage() <= self.zeitziel_in_tagen)
