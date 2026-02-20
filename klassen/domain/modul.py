from dataclasses import dataclass

from klassen.domain.pruefungsleistung import Pruefungsleistung

@dataclass
class Modul:
    """ Module des Semesters mit Prüfungsleistung """
    titel: str
    credits: int
    pruefungsleistung: Pruefungsleistung