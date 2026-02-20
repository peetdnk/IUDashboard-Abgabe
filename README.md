Das Programm ist darauf ausgelegt einen Studiengang über eine CSV-Datei auszulesen. Für den Studiengang B.Sc. Cybersecurity ist exemplarisch eine CSV-Datei beigefügt. Es besteht aber auch die
Möglichkeit einen leeren Studiengang zu erstellen, indem man auf die Bereitstellung der CSV-Datei verzichtet. Um einen eigenen Studiengang einzulesen, kann eine CSV-Datei mit folgenden Spaltenüberschriften 
anhand eines Studienablaufplans nach diesem Beispiel erstellt werden:
```
Semester,Modul,ECTS,Pruefungsleistung
2,Projekt: Objektorientierte und funktionale Programmierung mit Python,5,Portfolio
```
Der restliche Teil der Anleitung setzt eine funktionierende Python3 Installation vorraus.

# Installation über Terminal mit GIT
1. Terminal bzw. Eingabeaufforderung öffnen und zu einem geeignetem Pfad wechseln. Anschließend folgende Befehle ausführen:
```
clone https://github.com/peetdnk/IUDashboard-Abgabe.git
cd IUDashboard
pip install -r requirements.txt
python3 .\app.py
```
3. Browser öffnen und http://127.0.0.1 in die Adressleiste eingeben. Das Dashboard sollte nun sichtbar sein.

   
# Installation nach Download des archivierten Projektes
1. Archiv entpacken
2. In den entpackten Ordner wechseln
3. (Windows) Shift+Rechtsklick -> In Terminal öffnen. Oder im Terminal zu dem Pfad navigieren.
4. Folgende Befehle ausführen:
```
pip install -r requirements.txt
python3 .\app.py
```
6. Browser öffnen und http://127.0.0.1 in die Adressleiste eingeben. Das Dashboard sollte nun sichtbar sein.
