Das Programm ist darauf ausgelegt die Module eines Studiengangs über eine CSV-Datei einzulesen.
Für den Studiengang B.Sc. Cybersecurity ist exemplarisch eine CSV-Datei beigefügt. Es besteht
auch die Möglichkeit einen leeren Studiengang zu erstellen, indem man auf die Bereitstellung der
CSV-Datei verzichtet. Um einen eigenen Studiengang einzulesen, kann eine CSV-Datei mit folgen-
den Spaltenüberschriften anhand eines Studienablaufplans erstellt werden, Zeile 2 zeigt ein Beispiel-
Modul:
```
Semester,Modul,ECTS,Pruefungsleistung
2,Projekt: Objektorientierte und funktionale Programmierung mit Python,5,Portfolio
```
Der restliche Teil der Anleitung setzt eine funktionierende Python3 Installation vorraus.

# Installation (Windows)
1. PowerShell öffnen und zu einem geeignetem Pfad wechseln. Anschließend folgende Befehle
ausführen:
```
git clone https://github.com/peetdnk/IUDashboard-Abgabe.git
cd IUDashboard-Abgabe
```
2. Alternativ das Archiv entpacken, in den entpackten Ordner wechseln und per Shift+Rechtsklick
-> ”In Terminal öffnen” PowerShell öffnen.
3. Mit den folgenden Befehlen, wird eine virtuelle Umgebung erstellt, darin die benötigten Pakete
installiert und das Programm gestartet. ”Set-ExecutionPolicy...” sorgt dafür, dass dem aktuellen
PowerShell Fenster erlaubt wird lokale Skripte auszuführen.
```
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\app.py
```
4. Browser öffnen und http://127.0.0.1:5000 in die Adressleiste eingeben. Das Dashboard sollte nun sichtbar sein.
5. Befehl zum deaktivieren der virtuellen Umgebung:
```
deactivate
```
