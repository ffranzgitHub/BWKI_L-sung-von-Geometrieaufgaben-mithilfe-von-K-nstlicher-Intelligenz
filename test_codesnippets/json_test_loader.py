data = \
    [
        {"Text": "text1", "aufgabentyp": "aufgabe1"},
        {"Text": "text2", "aufgabentyp": "aufgabe2"},
        {"Text": "text3", "aufgabentyp": "aufgabe3"},
        {"Text": "text4", "aufgabentyp": "aufgabe1"},
        {"Text": "text5", "aufgabentyp": "aufgabe2"},
        {"Text": "text6", "aufgabentyp": "aufgabe3"},
    ]
classes = ["aufgabe1", "aufgabe2", "aufgabe3"]
sorted_data = {}

for aufgabe in classes:
    sorted_data[aufgabe] = []

for datapunkt in data:
    sorted_data[datapunkt["aufgabentyp"]].append(datapunkt["Text"])

print(sorted_data)