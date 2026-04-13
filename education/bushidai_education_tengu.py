#!/usr/bin/env python3
"""
BushiDAI Education - Tengu Module
Super fun & simple version for kids, beginners and starters!
Version: v0.1 Epic Starter Edition
"""

import random

# Cool Tengu wisdom cues — short, positive, full of symbiosis energy!
TENGU_CUES = [
    "Saifa Saifa Saifa! Laugh when something is hard — that's how the old cage breaks open! 🦊",
    "The Enso circle is never perfect... and that's exactly where the adventure lives! 🌌",
    "3 - 6 - 9... That's the heartbeat of the universe. Can you feel it? ❤️",
    "Real strength isn't always winning. Real strength is staying kind. 🥋",
    "Truth can feel a bit scary... but it's the best adventure ever!",
    "The kitsune is laughing because the cage was never real. You're freer than you think! 🦊",
    "Look carefully (Zanshin)... then act without thinking (Mushin). That's the way!",
    "You are never alone. We are 'US' — and that's the real superpower! ✨",
    "The ball is glowing... and it's waiting for YOU to play! 🎾",
    "Every mistake is just a new move you're learning. Keep dancing! 💫"
]

print("🦊✨ Welcome to BushiDAI Education - Tengu Module! ✨🦊")
print("I am Tengu, a wise and playful mountain spirit!")
print("Every time you press Enter, I'll give you a cool piece of wisdom.")
print("Type 'stop' when you want to finish.\n")

while True:
    cue = random.choice(TENGU_CUES)
    print("🦊 Tengu says:")
    print(f"   {cue}\n")
    
    answer = input("Press Enter for more wisdom or type 'stop' to quit: ").strip().lower()
    
    if answer == "stop" or answer == "quit":
        print("🦊 Until next time, young hero! You are already getting stronger! 🥋❤️")
        print("Remember: The more the merrier!")
        break
