from locale import normalize
import math


class NotImplementedException(Exception):
    def __init__(self) -> None:
        super().__init__("Für diesen Aufgabentypen haben wir noch keine Lösung implementiert!")


# TODO brauchen wir das?
aufgaben_typen = {
    "Lösen von Aufgaben in rechtwinkligen Dreiecken mit Pythagoras.": "Pythagoras",
    "Ähnlichkeit von Dreiecken": "Kongruenz von Dreiecken",
    "Längen und Winkel eines Dreiecks mit Sinus, Cosinus": "Sinus und Cosunus"
}


def pythagoras(gegebene_werte):
    if len(gegebene_werte.keys()) < 2:
        raise ValueError("Mindestens zwei Seitenlängen zum Lösen von Pythagorasaufgaben nötig")

    if "a" not in gegebene_werte.keys():
        b = float(gegebene_werte["b"])
        c = float(gegebene_werte["c"])
        a = math.sqrt(math.pow(c, 2) - math.pow(b, 2))
        print(f"Die fehlende Kathete ist: {a}cm")
        return

    elif "b" not in gegebene_werte.keys():
        a = float(gegebene_werte["a"])
        c = float(gegebene_werte["c"])
        b = math.sqrt(math.pow(c, 2) - math.pow(a, 2))
        print(f"Die fehlende Kathete ist: {b}cm")
        return

    elif "c" not in gegebene_werte.keys():
        a = float(gegebene_werte["a"])
        b = float(gegebene_werte["b"])
        c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
        print(f"Die Hypothenuse ist: {c}cm")
        return

    else:
        raise Exception("Die Aufgabe ist bereits gelöst!")


def sinus_cosinus(gegebene_werte):
    if "sin(A)" in gegebene_werte.keys():
        a = math.degrees(math.asin(gegebene_werte["sin(A)"]))
        print(f"Der Winkel A beträgt {a}°")
        return
    else:
        not_implemented()
        return

    # TODO nicht fertig
    if "A" in gegebene_werte.keys() and ("b" not in gegebene_werte.keys() and "c" not in gegebene_werte.keys()):
        sin_a = math.sin(gegebene_werte["A"])
        print(f"Sinus von A ist {sin_a}")

    if "A" in gegebene_werte.keys() and "b" in gegebene_werte.keys():
        sin_a = math.sin(gegebene_werte["A"])


def kongruenz(gegebene_werte):
    not_implemented(gegebene_werte)


def not_implemented(gegebene_werte=None):
    print("Für diesenaufgabentypen haben wir noch keine Lösung implementiert!")
    #raise NotImplementedException()


name_to_aufgabe = \
    {
        "Satz des Pythagoras": pythagoras,
        "Sinus und Cosinus": sinus_cosinus,
        "Kongruenz von Dreiecken": kongruenz
    }

if __name__ == "__main__":

    aufgaben_typ = "Sinus und Cosinus"

    gegebene_werte = \
        {
            "sin(A)": 0.5
        }

    name_to_aufgabe.get(aufgaben_typ, not_implemented)(gegebene_werte)
