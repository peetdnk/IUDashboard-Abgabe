from abc import ABC, abstractmethod

from klassen.domain.studiengang import Studiengang


class Ziel(ABC):
    """ Abstrakte Methode für Ziele """
    @abstractmethod
    def ist_ziel_erreicht(self, studiengang: Studiengang):
        pass


