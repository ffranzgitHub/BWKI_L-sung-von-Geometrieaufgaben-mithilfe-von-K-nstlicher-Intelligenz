'''
für das NER System sollte es keine Rolle spielen wie eine Variable heißt, welchen Wert sie hat oder wie 
viele Leerzeichen zwischen dem Gleichzeichen sind

Das Programm ist dafür da Variablenzuweisungen (wie x1=10) als Named Entitys zu erkennen und alle auf ein gleiches Wort
herunterzubrechen, um vom NLP Verfahren wie BoW nicht als verschiedene Worte erkannt zu werden
(sozusagen Stemming für Variablenzuweisungen)
'''
import re


unit_to_cm = \
    {
        "km": 100_000,
        "m": 100,
        "dm": 10,
        "cm": 1,
        "mm": 0.1,
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
        # TODO: named_entity_name nimmt immer das erste Element. Aber was ist, wenn der Name nach dem "=" kommt z.b: 3=a
        named_entity_name = match_obj.group(1)
        named_entity_value = match_obj.group(3)  # .group(2) wäre das istgleich

        named_entity_value = re.sub(
            "(\d+)(\D+)", self.convert_units, named_entity_value)  # TODO: auch float erkennen

        # Name und Werte der Variablenzuweisung werden gespeichert
        named_entity = [named_entity_name, named_entity_value]

        # alle konkret unterschiedlichen Variablenzuweisungen werden hier zu einer gleichen Vokabel
        if named_entity_value != "?":
            string = '<Variablenzuweisung>'
        else:
            string = "<Unbekannte Variable>"

        self.named_entities += [named_entity]

        return string

    # TODO Namen der Funktion ändern
    # TODO Wenn keine Einheit angegeben wird, wird diese Funktion anscheinend nicht korrekt aufgerufen. Dagegen müssen wir etwas tun
    def convert_units(self, match_obj):
        named_entity_number = match_obj.group(1)

        named_entity_unit = match_obj.group(2)
        self.units.append(named_entity_unit)

        return named_entity_number


#beispiel_aufgabe= "Katheten: a=5cm und b   =   8cm Berechne die Hypothenuse"


# Der Coding Style hier ist sehr schlecht von mir. Wollte nur was testen
def named_entities(aufgabe: str):
    cmv = ConvertmitVariable()

    angepasster_string = re.sub(
        '(\d+,\d+|\w+|\?+) *(=|ist gleich|gleich|:|mit dem Wert|entspricht) *(\?+|\d+,\d+|\w+)', cmv.convert, aufgabe)

    # print('\n'+angepasster_string)
    # print('\nnamed entitys:\n'+str(cmv.named_entitys))

    entities = [[entity[0], float(entity[1]) * unit_to_cm.get(unit, 1)] 
                if entity[1]!="?" else [entity[0], entity[1]]
                for entity, unit in zip(cmv.named_entities, cmv.units)]

    return angepasster_string, entities


if __name__ == "__main__":
    angepasster_string, entities = named_entities("Ein Dreieck hat die Hypotenuse a : 10cm und b = 20cm")
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
