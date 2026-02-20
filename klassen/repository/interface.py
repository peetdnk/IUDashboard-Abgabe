from abc import ABC, abstractmethod

from klassen.domain.studiengang import Studiengang


class StudiengangRepository(ABC):
    """ Interface zum Speicher und Laden von Daten"""
    @abstractmethod
    def speichern(self, studiengang: Studiengang) -> None:
        pass
    @abstractmethod
    def laden(self):
        pass
