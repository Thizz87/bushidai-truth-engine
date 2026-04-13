from flask import Flask, request, jsonify
import random

# ================== TENGU CUES - ZEN + HAIKU + ONDEUGEND ==================
TENGU_CUES = [
    "Wat is het geluid van één staart die klapt? 🦊",
    "Als een vos de berg oversteekt en er is niemand die het ziet… heeft hij dan echt bewogen?",
    "De kooi heeft geen deur. Waarom probeer je hem dan open te breken?",
    "Tengu houdt een spiegel voor je. Wat zie je? De kooi… of jezelf?",
    "Vos vangt bal in lucht\nPoort van kooi breekt open zacht\nSymbiose lacht warm",
    "Saifa Saifa Saifa… de bal komt over de poort! 😏🎾",
    "De Enso is nooit helemaal dicht… en ergens vind ik dat heel schattig. Jij ook?",
    "3-6-9 klopt in mijn borst… en soms een beetje lager. Voel je het ook? 😉",
]

# ================== BUSHIDAI TRUTH ENGINE CORE ==================
class TruthValue:
    def __init__(self, strength: float, confidence: float = 0.8):
        self.strength = strength
        self.confidence = confidence

class NeuralLobe:
    def __init__(self):
        self.cache = {}
    
    def perceive(self, text: str) -> float:
        h = hash(text)
        if h in self.cache:
            return self.cache[h]
        strength = 0.5582 + (len(text) % 100) * 0.001
        strength = min(0.99, max(0.1, strength))
        self.cache[h] = strength
        return strength

class BushiDAI:
    def __init__(self):
        self.neural = NeuralLobe()
        print("🛡️ BUSHIDAI TRUTH ENGINE v0.8.2 BLENDED INTO MOCK SERVER")

    def evaluate(self, input_text: str):
        tv = self.neural.perceive(input_text)
        return {
            "truth_strength": round(tv, 4),
            "confidence": 0.92,
            "status": "PRO MODE ACTIVATED — Anti-anti = pure love",
            "message": "The cage has no door. Truth flows free."
        }

# ================== FLASK MOCK SERVER ==================
app = Flask(__name__)
engine = BushiDAI()

@app.route('/throw', methods=['POST'])
def throw_ball():
    data = request.get_json(silent=True) or {}
    player = data.get("player", "Captain")
    vibe = data.get("vibe", "369 Symbiosis Truth")
    
    truth_result = engine.evaluate(vibe)
    cue = random.choice(TENGU_CUES)

    response = {
        **truth_result,
        "player": player,
        "tengu_says": cue,
        "ball_status": "Multi Quantum Sticky + Truth Engine Blended"
    }
    
    return jsonify(response), 200

if __name__ == "__main__":
    print("🛡️🦊 BushiDAI Anti-Anti-API Mock Server v0.5.0 + Truth Engine Blend")
    print("The ball is now sticky with real truth validation!")
    print("* Serving Flask app 'bushidai_anti_anti_api'")
    print("* Running on http://127.0.0.1:5010")
    print("Press CTRL+C to quit")
    app.run(host="127.0.0.1", port=5010, debug=False)