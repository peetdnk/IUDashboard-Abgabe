from abc import ABC, abstractmethod

from klassen.domain.studiengang import Studiengang


class IZiel(ABC):
    """ Abstrakte Methode für Ziele """
    # Interface für Ziele des Studiengangs
    @abstractmethod
    def ist_ziel_erreicht(self, studiengang: Studiengang):
        pass


