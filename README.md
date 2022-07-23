# BWKI_Lösung-von-Geometrieaufgaben-mithilfe-von-Künstlicher-Intelligenz

Dieses Projekt beschäftigt sich mit dem Einsatz von Künstlicher Intelligenz zum Lösen von Gemetrieaufgaben. Dabei nehmen wir an dem BWKI (Bundeswettbewerb Künstliche Intelligenz) teil.

## Regeln bei der Aufgabenstellung 
Diese Regeln werden mit der Verbesserung der KI mit der Zeit vermutlich gelockert, sind aber auch noch nicht fertiggestelllt
- Namen von Seitenlängen werden immer klein geschrieben
- Namen von Winkelgrößen bzw. Punkten werden immer Groß geschrieben

## Wie funktioniert die KI?
(Bei weitem nicht fertiggestellt)
Man gibt dem Programm einen Text über. Über diesen Text liest das Programm dann mit der Python Bibliothek "re" Werte aus dem Text heraus. Für diesen Teil wird erstmal keine KI benötigt. Dann allerdings wird eine KI verwendet um anhand der Aufgabenformulierung zu bestimmen um was für eine Aufgabe es sich handelt. Dabei wird sogenanntes "tokenizing" verwendet, welches die Texte mithilfe von One-Hot encoding für das einfacher zu verstehen macht. 