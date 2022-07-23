import math

aufgaben_typen = {
    "Lösen von Aufgaben in rechtwinkligen Dreiecken mit Pythagoras." : "Pythagoras",
    "Ähnlichkeit von Dreiecken" : "Ähnlihkeit",
    "Längen und Winkel eines Dreiecks mit Sinus, Cosinus" : "Längen und Winkel"
}


aufgaben_typ = "Pythagoras"
gegebene_werte = {
    "b": 4,
    "c": 5
}


if aufgaben_typ == "Pythagoras":
    if len(gegebene_werte.keys()) < 2:
        raise ValueError("Mindestens zwei Seitenlängen zum Lösen von Pythagorasaufgaben nötig")

    if "a" not in gegebene_werte.keys():
        b = gegebene_werte["b"]
        c = gegebene_werte["c"]
        a = math.sqrt(math.pow(c, 2) - math.pow(b, 2))
        print(f"Die fehlende Kathete ist: {a}")
    
    if "b" not in gegebene_werte.keys():
        a = gegebene_werte["a"]
        c = gegebene_werte["c"]
        b = math.sqrt(math.pow(c, 2) - math.pow(a, 2))
        print(f"Die fehlende Kathete ist: {b}")

    if "c" not in gegebene_werte.keys():
        a = gegebene_werte["a"]
        b = gegebene_werte["b"]
        c = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
        print(f"Die Hypothenuse ist: {c}")