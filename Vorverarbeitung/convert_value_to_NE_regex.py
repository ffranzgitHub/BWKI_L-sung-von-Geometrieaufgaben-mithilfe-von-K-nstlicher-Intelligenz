'''
für das NER System sollte es keine Rolle spielen wie eine Variable heißt, welchen Wert sie hat oder wie 
viele Leerzeichen zwischen dem Gleichzeichen sind

Das Programm ist dafür da Variablenzuweisungen (wie x1=10) als Named Entitys zu erkennen und alle auf ein gleiches Wort
herunterzubrechen, um vom NLP Verfahren wie BoW nicht als verschiedene Worte erkannt zu werden
(sozusagen Stemming für Variablenzuweisungen)
'''
import re

# TODO: Reinfolge mm -> m wichtig für regex, kann man das unabhängig machen
unit_to_cm = \
    {
        "mm": 0.1,
        "km": 100_000,
        "m": 100,
        "dm": 10,
        "cm": 1,
    }


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

        if named_entity_value != "?":
            # Änderung: Auflösung der Einheiten findet hier statt
            named_entity = [named_entity_name, float(named_entity_value)*unit_to_cm.get(named_entity_unit, 1)]
        else:
            # TODO: Einheiten handling bei ? implementieren
            named_entity = [named_entity_name, named_entity_value]

        # alle konkret unterschiedlichen Variablenzuweisungen werden hier zu einer gleichen Vokabel
        if named_entity_value != "?":
            string = '<Variablenzuweisung>'
        else:
            string = "<Unbekannte Variable>"

        self.named_entities += [named_entity]

        return string

#Änderung: zweite regex Funktion weggelassen

def variablenzuweisung_extrahieren(aufgabe: str):
    cmv = ConvertmitVariable()
    # Änderung: nur noch Formate, in denen die Variable links steht werden akzeptiert
    # Änderungen: die Einheit wird direkt hier erkannt und es ist kein neuer .sub() in einer neuen Funktion nötig
    # Änderungen: die Erkannten einheiten passen sich an die unterstützen Einheiten in unit_to_cm an
    eh = '('
    for i, e in enumerate(unit_to_cm.keys()):
        if i == 0:
            eh += e
        else:
            eh += "|"+e
    eh += ")?"
    angepasster_string = re.sub('([a-zA-Z]+\d*|\?+) *(=|ist gleich|gleich|:|mit dem Wert|entspricht) *(\?+|\d+,\d+|\d+) *' + eh, cmv.convert, aufgabe)

    return angepasster_string, cmv.named_entities


if __name__ == "__main__":
    angepasster_string, entities = variablenzuweisung_extrahieren(
        "Ein Dreieck hat die Hypotenuse a : 10km und b = 20mm")
    print()

#string1= ''' a = 10; b  =  20'''
#string2= ''' a = 10; b  =  20; 10=c; 200= a'''
# string3= ''' a = 10;
#b = 20
# c = 30  d=40
# alpa = 4,5 betha =  5,5
#
# asdflöjj.a = ?. 10,10  =  10,10
# '''
