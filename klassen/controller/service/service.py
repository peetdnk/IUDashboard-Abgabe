from klassen.domain.studiengang import Studiengang


class StudiengangService:
    """ Bereitet Daten des Studiengangs für das GUI auf """
    @staticmethod
    def credits_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der erreichten ECTS für das GUI """
        gesamt_credits = 0
        for semester in studiengang.semester:
            for modul in semester.module:
                gesamt_credits += modul.credits
        try:
            fortschritt = studiengang.berechne_erreichte_credits() / gesamt_credits * 100
        except ZeroDivisionError:
            fortschritt = 0
        return fortschritt

    @staticmethod
    def modul_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der abgeschlossenen Module für das GUI """
        gesamt_module = 0
        for semester in studiengang.semester:
            gesamt_module += len(semester.module)
        try:
            fortschritt = studiengang.berechne_abgeschlossene_module() / gesamt_module * 100
        except ZeroDivisionError:
            fortschritt = 0
        return fortschritt

    @staticmethod
    def zeit_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der vergangenen Tage bezogen auf das ZeitZiel für das GUI """
        try:
            zeit_fortschritt = min(
                studiengang.berechne_vergangene_tage() / studiengang.ziele['zeit'].zeitziel_in_tagen * 100, 100)
            if zeit_fortschritt < 0:
                zeit_fortschritt = 0
        except ZeroDivisionError:
            zeit_fortschritt = 0
        return zeit_fortschritt

    @staticmethod
    def ziel_fortschritt_farbe(ziel: str, studiengang: Studiengang):
        """ Gibt die Farbe des Zielbalkens an - erreicht=grün, nicht erreicht=rot - anwendbar auf alle Ziele"""
        if not studiengang.ziele[ziel].ist_ziel_erreicht(studiengang):
            balken_farbe = "#ff6666"
        else:
            balken_farbe = "#aaddaa"
        return balken_farbe