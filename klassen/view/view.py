import logging

from flask import render_template, redirect, url_for, flash
from werkzeug.security import check_password_hash


class StudiengangAnsicht:
    @staticmethod
    def dashboard(manager, service):
        """ Gibt die Dashboard-Seite aus """
        studiengang = manager.studiengang_laden()

        return render_template(
            'dashboard.html',
            sg=manager.studiengang_laden(),
            tage_vergangen=studiengang.berechne_vergangene_tage(),
            tage_ziel=studiengang.ziele['zeit'].zeitziel_in_tagen,
            zeitbalken_fortschritt=service.zeit_fortschritt(studiengang),
            zeitbalken_farbe=service.ziel_fortschritt_farbe('zeit', studiengang),
            module_abgeschlossen=studiengang.berechne_abgeschlossene_module(),
            erreichte_credits=studiengang.berechne_erreichte_credits(),
            notendurchschnitt_aktuell=f"{studiengang.berechne_notendurchschnitt():.1f}".replace('.', ','),
            notendurchschnitt_ziel=f"{studiengang.ziele['note'].notendurchschnitt:.1f}".replace('.', ','),
            notenbalken_farbe=service.ziel_fortschritt_farbe('note', studiengang),
            credit_fortschritt=service.credits_fortschritt(studiengang),
            module_fortschritt=service.modul_fortschritt(studiengang)
        )

    @staticmethod
    def login(session, request, password):
        """ Login mit Passwortabfrage """
        error = None
        if request.method == 'POST':
            # Kennwortabfrage wenn "Login" gedrückt wird
            if check_password_hash(password, request.form['password']):
                # Wenn das eingegebene Kennwort mit dem Hash übereinstimmt, wird ein Session-Cookie gesetzt und an die Seite zum Bearbeiten weitergeleitet.
                session['logged_in'] = True
                logging.info("Benutzer erfolgreich eingeloggt.")
                return redirect(url_for('bearbeiten'))
            else:
                # Wenn Kennwort nicht stimmt, Variable error setzen und Fehler ausgeben.
                error = 'Falsches Passwort'
                logging.warning("Benutzer hat ein falsches Passwort verwendet.")
        return render_template('login.html', error=error)

    @staticmethod
    def logout(session):
        """ Logout """
        session.pop('logged_in', None)
        logging.info("Benutzer erfolgreich ausgeloggt.")
        return redirect(url_for('dashboard'))

    @staticmethod
    def bearbeiten(session, request, handler, manager):
        """ Dashboard-Daten bearbeiten """
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        # Studiengang laden
        studiengang = manager.studiengang_laden()
        if request.method == 'POST':
            # Nach drücken auf Speichern wird versucht den Studiengang aus den Formulardaten zu aktualisieren.
            # Tritt kein Fehler auf wird eine positive Meldung gespeichert und auf der Hauptseite angezeigt.
            try:
                handler.aktualisieren_aus_formular(studiengang, request.form, manager)
                flash("Änderungen erfolgreich gespeichert!", "success")
                return redirect(url_for('dashboard'))
            # Bei Fehler wird eine negative Meldung gespeichert und ausgegeben. Der Fehler wird in die Log-Datei geschrieben.
            except Exception as e:
                fehlermeldung = f"Speichern fehlgeschlagen: dashboard.log überprüfen."
                flash(fehlermeldung, 'danger')
                logging.error({str(e)})
                # erneutes ausgeben der bearbeiten.html mit den alten Werten.
                return render_template(
                    'bearbeiten.html',
                    sg=studiengang,
                    ziel_tage=studiengang.ziele['zeit'].zeitziel_in_tagen,
                    ziel_note=studiengang.ziele['note'].notendurchschnitt
                )
        return render_template(
            'bearbeiten.html',
            sg=studiengang,
            ziel_tage=studiengang.ziele['zeit'].zeitziel_in_tagen,
            ziel_note=studiengang.ziele['note'].notendurchschnitt
        )
