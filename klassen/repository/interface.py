from abc import ABC, abstractmethod

from klassen.domain.studiengang import Studiengang


class IStudiengangRepository(ABC):
    """ Interface zum Speichern und Laden von Daten"""
    # Interface zum Speichern und Laden von Daten. Methoden müssen von Kindklasse überschrieben werden.
    @abstractmethod
    def speichern(self, studiengang: Studiengang) -> None:
        pass
    @abstractmethod
    def laden(self):
        pass
