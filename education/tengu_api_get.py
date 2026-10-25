#!/usr/bin/env python3
"""
BushiDAI Education — Tengu Lesson 2
De postbode (GET)
v0.1 — dezelfde filter, doos komt over HTTP
"""

import json
import urllib.request
from urllib.error import URLError, HTTPError

URL = "https://jsonplaceholder.typicode.com/users"


def haal_doos(url):
    print("🦊 Tengu stuurt de postbode.")
    print("   Brief: GET")
    print("   Adres:", url)
    print()
    verzoek = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(verzoek, timeout=15) as antwoord:
        status = antwoord.status
        ruw = antwoord.read().decode("utf-8")
    return status, json.loads(ruw)


def haal_alleen(naam, doos):
    zoek = naam.strip().lower()
    return [rij for rij in doos if rij.get("name", "").lower() == zoek]


def print_rij(rij):
    print("   id:     ", rij.get("id"))
    print("   naam:   ", rij.get("name"))
    print("   stad:   ", rij.get("address", {}).get("city"))
    print("   mail:   ", rij.get("email"))


def main():
    print()
    print("🦊 Tengu: les 1 was een doos op schijf.")
    print("   Les 2 is dezelfde doos. Alleen de postbode haalt hem.")
    print("   GET = vragen. 200 = 1. Rest = 0.")
    print()

    try:
        status, doos = haal_doos(URL)
    except HTTPError as e:
        print("🦊 Resultaat = 0. Server zei", e.code)
        return
    except URLError:
        print("🦊 Resultaat = 0. Postbode kwam niet aan.")
        print("   Check internet. Geen magie, gewoon een kabel.")
        return

    if status != 200:
        print("🦊 Resultaat = 0. Status", status)
        return

    print("🦊 Status", status, "= 1. Doos is er.")
    print("   Aantal rijen:", len(doos))
    print()
    print("🦊 Namen in de doos:")
    for rij in doos:
        print("   -", rij.get("name"))
    print()

    naam = input("🦊 Tengu: welke naam moet ik eruit halen? ").strip()
    if not naam:
        print("🦊 Resultaat = 0. Geen naam, geen filter.")
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
        print("🦊 Tengu: zie je? Zelfde opdracht als les 1.")
        print("   Alleen de doos kwam via GET.")
        print("   Dat is een API.")
    else:
        print("🦊 Resultaat = 0.")
        print("   Typ een naam uit de lijst hierboven.")
        print("   Tip: Leanne Graham")

    print()
    print("🦊 Tengu: knop UIT. De berg is stil.")
    print()


if __name__ == "__main__":
    main()
