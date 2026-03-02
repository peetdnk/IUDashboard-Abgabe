from dataclasses import dataclass
from enum import Enum


@dataclass
class Pruefungsleistung:
    """ Prüfungsleistung eines Moduls """
    pruefungsart: Enum
    note: float | None = None # Entweder float oder None - Standardwert = None
    modul_anerkannt: bool | None = None # Entweder bool oder None - Standardwert = None

    def setze_note(self, note: float):
        """ Note für die Prüfungsleistung eintragen """
        self.note = note

    def setze_anerkannt(self, modul_anerkannt: bool):
        """ Deaktiviert eine Prüfungsleistung, wenn das Modul anerkannt wurde """
        self.modul_anerkannt = modul_anerkannt