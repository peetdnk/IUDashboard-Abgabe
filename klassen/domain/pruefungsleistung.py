from dataclasses import dataclass
from enum import Enum


@dataclass
class Pruefungsleistung:
    """ Prüfung eines Moduls """
    pruefungsart: Enum
    note: float | None = None
    modul_anerkannt: bool | None = None

    def setze_note(self, note: float):
        """ Note für die Prüfung eintragen """
        self.note = note

    def setze_anerkannt(self, modul_anerkannt: bool):
        self.modul_anerkannt = modul_anerkannt