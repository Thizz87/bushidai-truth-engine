#!/usr/bin/env python3
"""
BushiDAI Education — Tengu Lesson 3
Twee dozen, één nummer
v0.1 — dezelfde id opent de tweede doos
"""

import json
from pathlib import Path

MAP = Path(__file__).parent
DOOS_A = MAP / "box_a.json"
DOOS_B = MAP / "box_b.json"


def laad(pad):
    with open(pad, "r", encoding="utf-8") as f:
        return json.load(f)


def zoek_id(doos, nummer):
    for rij in doos:
        if rij.get("id") == nummer:
            return rij
    return None


def main():
    print()
    print("🦊 Tengu: les 1 = één doos. Les 2 = postbode.")
    print("   Les 3 = twee dozen. Zelfde nummer.")
    print("   Dat is geen magie. Dat is koppelen.")
    print()

    a = laad(DOOS_A)
    b = laad(DOOS_B)

    print("🦊 Doos A (namen):")
    for rij in a:
        print(f"   id {rij['id']} → {rij['naam']}")
    print()
    print("🦊 Doos B (dossiers):")
    for rij in b:
        print(f"   id {rij['id']} → {rij['status']}")
    print()

    raw = input("🦊 Tengu: welk id moet ik in beide dozen zoeken? ").strip()
    try:
        nummer = int(raw)
    except ValueError:
        print("🦊 Resultaat = 0. Een id is een getal.")
        return

    print()
    print("   Knop = AAN. Twee filters, één nummer.")
    persoon = zoek_id(a, nummer)
    dossier = zoek_id(b, nummer)

    if persoon and dossier:
        print("🦊 Resultaat = 1. De dozen raken elkaar:")
        print()
        print("   uit A:", persoon["naam"], "/", persoon["rol"])
        print("   uit B:", dossier["status"], "/", dossier["plaats"], "/ score", dossier["score"])
        print()
        print("🦊 Tengu: één id. Twee verhalen.")
        print("   Zo werkt een register ook.")
        print("   Niet omdat het slim is. Omdat het nummer hetzelfde is.")
    elif persoon and not dossier:
        print("🦊 Resultaat = 0. Naam gevonden, dossier niet.")
    elif dossier and not persoon:
        print("🦊 Resultaat = 0. Dossier gevonden, naam niet.")
    else:
        print("🦊 Resultaat = 0. Dit id zit in geen van beide dozen.")
        print("   Zet eerst jouw naam in box_a.json op id 2.")

    print()
    print("🦊 Tengu: knop UIT. De berg is stil.")
    print()


if __name__ == "__main__":
    main()
