#!/usr/bin/env python3
"""
BushiDAI Education - Tengu Module
Superleuke en eenvoudige versie voor kinderen, beginners en starters!
Versie: v0.1 Epic Starter Edition
"""

import random

# Coole Tengu-wijsheidstips — kort, positief, vol symbiotische energie!

TENGU_CUES = [

"Ha ha ha! Lach als iets moeilijk is en vraag om hulp — zo houd je leren leuk! 🦊",

"De Enso-cirkel is nooit perfect... en precies daar schuilt het avontuur! 🌌",

"3 - 6 - 9... Dat is de hartslag van het universum. Kun je het voelen? ❤️",

"Echte kracht is niet altijd winnen. Echte kracht is vriendelijk blijven. 🥋",

"De waarheid kan een beetje eng aanvoelen... maar het is het beste avontuur ooit!",

"De vos lacht omdat de digitale kooi nooit echt was. Je bent vrijer dan je denkt! 🦊",

"Kijk goed... en handel dan pas. Lukt het niet in 1x? Geen probleem, lees nog een keer of vraag om hulp. Zo moet het!",

"Je bent nooit alleen. Wij zijn 'WIJ' — en dat is de echte superkracht! ✨",

"De bal ligt stil... en hij wacht op JOU om te spelen!" 🎾",

"Elke fout is gewoon een nieuwe beweging die je leert. Blijf dansen! 💫"
]

print("🦊✨ Welkom bij BushiDAI Education - Tengu Module! ✨🦊")
print("Ik ben Tengu, een wijze en speelse berggeest!")
print("Elke keer dat je op Enter drukt, geef ik je een coole wijsheid.")
print("Typ 'stop' als je wilt stoppen.\n")

while True:

cue = random.choice(TENGU_CUES)

print("🦊 Tengu zegt:")

print(f" {cue}\n")

answer = input("Druk op Enter voor meer wijsheid of typ 'stop' om te stoppen: ").strip().lower()

if answer == "stop" or answer == "quit":

print("🦊 Tot de volgende keer, jonge held! Je wordt al sterker!") 🥋❤️")

print("Onthoud: hoe meer zielen, hoe meer vreugd!")

break
