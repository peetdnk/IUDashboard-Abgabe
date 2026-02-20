import logging

from klassen.domain.studiengang import Studiengang
from klassen.repository.interface import StudiengangRepository


class StudiengangManager:

    def __init__(self, speicher: StudiengangRepository, importer: StudiengangRepository):
        self.speicher = speicher
        self.importer = importer

    def studiengang_laden(self) -> Studiengang:
        """
        Versucht JSON zu laden - falls nicht vorhanden,
        wird aus CSV importiert oder leer erstellt und gespeichert.
        """

        studiengang = self.speicher.laden()
        if studiengang is None:
            logging.info("Kein JSON gefunden. Versuche aus CSV zu erstellen.")
            studiengang = self._studiengang_erstellen()
            self.speicher.speichern(studiengang)
        return studiengang

    def _studiengang_erstellen(self) -> Studiengang:
        """ Liest CSV ein oder erstellt einen leeren Studiengang, falls CSV fehlt."""
        return self.importer.laden()

    def studiengang_aktualisieren(self, studiengang):
        """ Weitergabe des Studiengangs an das Repo """
        self.speicher.speichern(studiengang)