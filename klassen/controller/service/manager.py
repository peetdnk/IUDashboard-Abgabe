import logging

from klassen.domain.studiengang import Studiengang
from klassen.repository.interface import IStudiengangRepository


class StudiengangManager:

    def __init__(self, speicher: IStudiengangRepository, importer: IStudiengangRepository):
        self.speicher = speicher
        self.importer = importer

    def studiengang_laden(self) -> Studiengang:
        """
        Versucht JSON zu laden - falls nicht vorhanden,
        wird aus CSV importiert oder leer erstellt und gespeichert.
        """
        # Studiengang über Repository Interface laden
        studiengang = self.speicher.laden()
        if studiengang is None: # None bedeutet hier, dass keine JSON-Datei zum Laden gefunden wurde, also kein Studiengang existiert
            logging.info("Kein JSON gefunden. Versuche aus CSV zu erstellen.")
            # Studiengang neu erstellen und Daten aus CSV einlesen
            studiengang = self._studiengang_erstellen()
            # Über Repository Interface speichern
            self.speicher.speichern(studiengang)
        return studiengang

    def _studiengang_erstellen(self) -> Studiengang:
        """ Liest CSV ein oder erstellt einen leeren Studiengang, falls CSV fehlt."""
        # gibt vom Repository Interface erstellten Studiengang zurück
        return self.importer.laden()

    def studiengang_aktualisieren(self, studiengang):
        """ Weitergabe des Studiengangs an das Repo """
        # erhält einen Studiengang und reicht ihn an das Repository Interface zum Speichern weiter
        self.speicher.speichern(studiengang)