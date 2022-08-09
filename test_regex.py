import unittest
from Vorverarbeitung.convert_value_to_NE_regex import variablenzuweisung_extrahieren


class testRegex(unittest.TestCase):

    testaufgaben = \
        [   # Testen der verschiedenen Einheiten
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10km und b = 20km",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1_000_000], ["b", 2_000_000]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10m und b = 20m",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1_000], ["b", 2_000]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10dm und b = 20dm",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 100], ["b", 200]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10cm und b = 20cm",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 10], ["b", 20]]
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10mm und b = 20mm",
                "labeltext":  "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1], ["b", 2]]
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10 und b = 20",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1], ["b", 2]]
            },
            # float Zahlen
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10,111km und b = 20,222km",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1_011_100], ["b", 2_022_200]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10,111m und b = 20,222m",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1_011.1], ["b", 2_022.2]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10,111dm und b = 20,222dm",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 101.11], ["b", 202.22]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10,111cm und b = 20,222cm",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 10.111], ["b", 20.222]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10,111mm und b = 20,222mm",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 1.0111], ["b", 2.0222]],
            },
            {
                "text": "Ein Dreieck hat die Hypotenuse a : 10,111 und b = 20,222",
                "labeltext": "Ein Dreieck hat die Hypotenuse <Variablenzuweisung> und <Variablenzuweisung>",
                "label_nes": [["a", 10.111], ["b", 20.222]],
            },

            # # Zuweisung andersherum
            # {"text": "Ein Dreieck hat die Hypotenuse 10cm : a1 und 20 = a1", },
            # # Abgrenzung von anderen Situationen
            # {"text": "Ein Dreieck hat die Hypotenuse a : 10random und b = 20random", },
            # {"text": "Die Länge der Katheten: 10cm, 20cm. Berechne die Hypothenuse", },
            # {"text": "Ein Dreieck hat die Hypotenuse a : 10mm und b = 20mm.", },
        ]

    def test_regex(self):
        for testaufgabe in self.testaufgaben:
            testtext, test_nes = variablenzuweisung_extrahieren(testaufgabe.get("text"))
            self.assertEquals(testtext, testaufgabe.get("labeltext"))
            self.assertEquals(test_nes, testaufgabe.get("label_nes"))


if __name__ == "__main__":
    unittest.main()
