#!/usr/bin/env python3
"""
BushiDAI Education — Tengu Lesson 1
Mijn eerste algoritme
v0.1 — doos openen, naam filteren, AAN/UIT
"""

import json
from pathlib import Path

DOOS = Path(__file__).parent / "database.json"


def laad_doos():
    with open(DOOS, "r", encoding="utf-8") as f:
        return json.load(f)


def haal_alleen(naam, doos):
    zoek = naam.strip().lower()
    return [rij for rij in doos if rij["naam"].lower() == zoek]


def print_rij(rij):
    print("   id:     ", rij["id"])
    print("   naam:   ", rij["naam"])
    print("   rol:    ", rij["rol"])
    print("   status: ", rij["status"])
    if "plaats" in rij:
        print("   plaats: ", rij["plaats"])


def main():
    print()
    print("🦊 Tengu: Welkom in jullie eerste stapjes.")
    print("   Drie namen zitten erin. John. Jij. Jane.")
    print("   Een algoritme is geen magie, het zijn gewoon gegevens die opgevraagd worden.")
    print("   Het is 1=AAN of 0=UIT. nog korter: 1 of 0.")
    print()
    print("   Opdracht: zet JOUW naam in database.json")
    print("   tussen John en Jane. Daarna kom je terug.")
    print()

    doos = laad_doos()
    print("🦊 Tengu opent de algoritme doos:")
    for rij in doos:
        print(f"   - {rij['naam']}")
    print()

    naam = input("🦊 Tengu: welke naam moet ik eruit halen? ").strip()
    if not naam:
        print("🦊 Resultaat = 0. Geen naam, geen data.")
        return

    print()
    print("   Knop = AAN. Filter draait.")
    gevonden = haal_alleen(naam, doos)

    if gevonden:
        print("🦊 Resultaat = 1. Data beweegt:")
        print()
        for rij in gevonden:
            print_rij(rij)
        print()
        print("🦊 Tengu: zie je? Alleen jouw rij.")
        print("   John en Jane blijven in de doos.")
        print("   Dat is het hele algoritme.")
    else:
        print("🦊 Resultaat = 0.")
        print("   Die naam zit niet in de doos.")
        print("   Zet hem tussen John en Jane in database.json.")

    print()
    print("🦊 Tengu: nu is de knop 0= UIT. Het algoritme is stil.")
    print()


if __name__ == "__main__":
    main()
