from klassen.domain.studiengang import Studiengang


class StudiengangService:
    """ Bereitet Daten des Studiengangs für das GUI auf """
    @staticmethod
    def credits_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der erreichten ECTS für das GUI """
        gesamt_credits = 0
        # iteriert über alle Module jeden Semesters und addiert die ECTS
        for semester in studiengang.semester:
            for modul in semester.module:
                gesamt_credits += modul.credits
        try:
            # teilt die schon erhaltenen ECTS durch die Gesamtanzahl, um einen Prozentwert zu erhalten
            fortschritt = studiengang.berechne_erreichte_credits() / gesamt_credits * 100
        # falls keine Module angelegt sind, wird der Fortschritt auf 0% gesetzt
        except ZeroDivisionError:
            fortschritt = 0
        return fortschritt

    @staticmethod
    def modul_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der abgeschlossenen Module für das GUI """
        gesamt_module = 0
        # iteriert über die Semester des Studiengangs und addiert die Anzahl der Module
        for semester in studiengang.semester:
            gesamt_module += len(semester.module)
        try:
            # teilt die abgeschlossenen Module durch die Gesamtanzahl Module
            fortschritt = studiengang.berechne_abgeschlossene_module() / gesamt_module * 100
        # falls keine Module angelegt sind, wird der Fortschritt auf 0% gesetzt
        except ZeroDivisionError:
            fortschritt = 0
        return fortschritt

    @staticmethod
    def zeit_fortschritt(studiengang: Studiengang):
        """ Berechnet den Prozentwert des Fortschrittbalkens der vergangenen Tage bezogen auf das ZeitZiel für das GUI """
        try:
            # berechnet Prozentwert für den Zeit-Fortschrittsbalken. min() sorgt dafür, dass der Wert nicht über 100 sein kann
            zeit_fortschritt = min(
                studiengang.berechne_vergangene_tage() / studiengang.ziele['zeit'].zeitziel_in_tagen * 100, 100)
            # falls Ergebnis negativ, 0 setzen - kommt vor, wenn Startdatum in der Zukunft liegt
            if zeit_fortschritt < 0:
                zeit_fortschritt = 0
        # falls ZeitZiel = 0
        except ZeroDivisionError:
            zeit_fortschritt = 0
        return zeit_fortschritt

    @staticmethod
    def ziel_fortschritt_farbe(ziel: str, studiengang: Studiengang):
        """ Gibt die Farbe des Zielbalkens an - erreicht=grün, nicht erreicht=rot - anwendbar auf alle Ziele"""
        # Farbe für die Ziel-Balken
        if not studiengang.ziele[ziel].ist_ziel_erreicht(studiengang):
            balken_farbe = "#ff6666" # rot wenn Ziel nicht erreicht
        else:
            balken_farbe = "#aaddaa" # grün wenn Ziel erreicht
        return balken_farbe