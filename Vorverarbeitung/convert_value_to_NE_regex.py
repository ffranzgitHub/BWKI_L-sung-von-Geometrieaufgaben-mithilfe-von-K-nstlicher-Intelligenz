'''
für das NER System sollte es keine Rolle spielen wie eine Variable heißt, welchen Wert sie hat oder wie 
viele Leerzeichen zwischen dem Gleichzeichen sind

Das Programm ist dafür da Variablenzuweisungen (wie x1=10) als Named Entitys zu erkennen und alle auf ein gleiches Wort
herunterzubrechen, um vom NLP Verfahren wie BoW nicht als verschiedene Worte erkannt zu werden
(sozusagen Stemming für Variablenzuweisungen)
'''
import re

# TODO: Einheiten richtig?
# TODO: Reinfolge mm -> m wichtig für regex, kann man das unabhängig machen
unit_to_cm = \
    {
        "mm": 0.1,
        "km": 100_000,
        "m": 100,
        "dm": 10,
        "cm": 1,
    }

# TODO: Testen in eine seperate Test Datei verschieben
testaufgaben = \
    [   # Testen der verschiedenen Einheiten
        "Ein Dreieck hat die Hypotenuse a : 10km und b = 20km",
        "Ein Dreieck hat die Hypotenuse a : 10dm und b = 20dm",
        "Ein Dreieck hat die Hypotenuse a : 10cm und b = 20cm",
        "Ein Dreieck hat die Hypotenuse a : 10mm und b = 20mm",
        "Ein Dreieck hat die Hypotenuse a : 10 und b = 20",
        # float Zahlen
        "Ein Dreieck hat die Hypotenuse a : 10,111km und b = 20,222km",
        "Ein Dreieck hat die Hypotenuse a : 10,111dm und b = 20,222dm",
        "Ein Dreieck hat die Hypotenuse a : 10,111cm und b = 20,222cm",
        "Ein Dreieck hat die Hypotenuse a : 10,111mm und b = 20,222mm",
        "Ein Dreieck hat die Hypotenuse a : 10,111 und b = 20,222",
        # Zuweisung andersherum
        "Ein Dreieck hat die Hypotenuse 10cm : a1 und 20 = a1",
        # Abgrenzung von anderen Situationen
        "Ein Dreieck hat die Hypotenuse a : 10random und b = 20random",
        "Die Länge der Katheten: 10cm, 20cm. Berechne die Hypothenuse",
        "Ein Dreieck hat die Hypotenuse a : 10mm und b = 20mm.",
    ]


class ConvertmitVariable():
    '''
    die Klasse ist eine Hilfsklasse welche die Hilfsfunktion convert enthält. Die Klasse ist dabei
    notwendig, um nicht nur die Variablenzuweisungen auszutauschen, sondern um alle Variablen und 
    deren Werte in named_entitys zu speichern und darauf zugreifen zu können
    '''

    def __init__(self):
        self.named_entities = []
        self.units = []
        self.string = ""

    def convert(self, match_obj):
        '''
        convert ist eine Hilfsfunktion, die bei einem Treffer der Regex aufgerufen wird
        Der zurückgegebene string ersetzt den gemachten Teil
        '''
        named_entity_name = match_obj.group(1)
        named_entity_value = match_obj.group(3)  # .group(2) wäre das istgleich
        # Änderung: Gruppe 4 enthält die Einheit
        named_entity_unit = match_obj.group(4)  # None wenn nicht gefunden
        # Änderung: if "?" not in string statt if string != "?" --> erlaubt auch mehrere Fragezeichen "???"
        if "?" not in named_entity_value:
            # Änderung: Auflösung der Einheiten findet hier statt
            named_entity_value = named_entity_value.replace(",", ".")
            named_entity = [named_entity_name, float(named_entity_value)*unit_to_cm.get(named_entity_unit, 1)]
        else:
            # TODO: Einheiten handling bei ? implementieren -> nicht unterstützt Fehler?
            named_entity = [named_entity_name, named_entity_value]
        # alle konkret unterschiedlichen Variablenzuweisungen werden hier zu einer gleichen Vokabel
        if "?" not in named_entity_value:
            string = '<Variablenzuweisung>'
        else:
            string = "<UnbekannteVariable>"

        self.named_entities += [named_entity]
        return string

# Änderung: zweite regex Funktion weggelassen

# TODO: soll die Funktion alle Aufgaben auf einmal als Liste übernehmen, ändern und zurückgeben oder so lassen?


def variablenzuweisung_extrahieren(aufgabe: str):
    cmv = ConvertmitVariable()
    # Änderung: nur noch Formate, in denen die Variable links steht werden akzeptiert
    # Änderungen: die Einheit wird direkt hier erkannt und es ist kein neuer .sub() in einer neuen Funktion nötig
    # Änderungen: die Erkannten einheiten passen sich an die unterstützen Einheiten in unit_to_cm an

    eh = '('
    eh += "|".join(unit_to_cm.keys())
    eh += ")?"

    angepasster_string = re.sub('([a-zA-Z]+\d*|\?+) *(=|ist gleich|gleich|:|mit dem Wert|entspricht) *(\?+|\d+,\d+|\d+) *' + eh, cmv.convert, aufgabe)

    return angepasster_string, cmv.named_entities


if __name__ == "__main__":

    # Änderung: es werden meherer Strings gleichzeigit getestet
    all_angepasste_strings = []
    all_entities = []

    for aufgabe in testaufgaben:
        neuer_string, entites = variablenzuweisung_extrahieren(aufgabe)
        all_angepasste_strings += [neuer_string]
        all_entities += [entites]

    print()
