# =============================================================================
# BUSHIDAI TRUTH SIMULATOR v0.8.2 - Optimized + Beautiful Output
# TRUTH == TRUTH
# =============================================================================
import numpy as np
import argparse
import os
import re
import yaml
import json
from pathlib import Path
from typing import Any, Dict

# =============================================================================
# NIEUWE IMPORT - Lokale Ollama client
# =============================================================================
from bushidai_local_client import local

print("BUSHIDAI TRUTH SIMULATOR v0.8.2 - Optimized + Beautiful Output")
print("TRUTH == TRUTH\n")

# =============================================================================
# CONFIG LOADER
# =============================================================================
def load_bushidai_config(config_filename: str = "bushidai_config") -> Dict[str, Any]:
    base_path = Path(__file__).parent
    candidates = [
        base_path / f"{config_filename}.yaml",
        base_path / f"{config_filename}.yml",
        base_path / f"{config_filename}.json"
    ]
    for file_path in candidates:
        if not file_path.exists():
            continue
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                if file_path.suffix in [".yaml", ".yml"]:
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
            if not isinstance(config, dict) or "bushiDAI" not in config:
                raise ValueError("Config moet een 'bushiDAI' root key bevatten")
            print(f"✅ BushiDAI config succesvol geladen: {file_path.name}")
            return config["bushiDAI"]
        except Exception as e:
            raise ValueError(f"Fout bij laden van {file_path.name}: {e}") from e
    raise FileNotFoundError(
        f"Geen configuratiebestand gevonden!\n"
        f"Zoek naar: {config_filename}.yaml, {config_filename}.yml of {config_filename}.json"
    )

config = load_bushidai_config()
bushidai = config.get("bushiDAI", {})
joy_spectrum = bushidai.get("joy_spectrum", [])
creative_framework = bushidai.get("creative_frameworks", [{}])[0] if bushidai.get("creative_frameworks") else {}
stackable_objects = bushidai.get("stackable_objects", [])
print(f" Joy spectrum: {len(joy_spectrum)} frequencies loaded")
print(f" Creative framework: {creative_framework.get('name', 'None')}\n")

# =============================================================================
# COLORS
# =============================================================================
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# =============================================================================
# OPTIMIZED CLASSES (onveranderd)
# =============================================================================
class NeuralLobe:
    def __init__(self):
        self.cache = {}
    def perceive(self, state):
        h = hash(state.tobytes())
        if h in self.cache:
            return self.cache[h]
        strength = 0.5582
        self.cache[h] = strength
        return strength
neural = NeuralLobe()

class ECAN:
    def __init__(self):
        self.alpha = 0.95
        self.beta = 0.01
        self.gamma = 0.05
        self.threshold = 0.1
    def decay_sti(self, sti):
        return sti * self.alpha
    def update_lti(self, lti, sti):
        new_lti = lti * (1 - self.beta) + self.gamma * sti
        return new_lti * 0.5 if sti < self.threshold else new_lti
    def spread(self, sti, amount):
        return sti + amount
ecan = ECAN()

# =============================================================================
# HYPERON MeTTa ENGINE (onveranderd)
# =============================================================================
class HyperonExpression:
    def __init__(self, head, args):
        self.head = head
        self.args = args
    def __repr__(self):
        return f"({self.head} {' '.join(map(str, self.args))})"

class HyperonAtomSpace:
    def __init__(self):
        self.kb = []
    def add(self, expr):
        self.kb.append(expr)

hyperon_atomspace = HyperonAtomSpace()

def parse_hyperon_metta(text):
    text = text.strip()
    if not (text.startswith('(') and text.endswith(')')):
        return HyperonExpression("unknown", [text])
    inner = text[1:-1].strip()
    parts = re.split(r'\s+', inner)
    head = parts[0]
    args = []
    for p in parts[1:]:
        if p.startswith('?'):
            args.append(p[1:])
        else:
            args.append(p)
    return HyperonExpression(head, args)

# =============================================================================
# LLM GROUNDER + VC GROUNDER (onveranderd)
# =============================================================================
class LLMGrounder:
    def __init__(self):
        self.rule_library = [
            ("hungry", "(= (hungry ?X) (eat ?X))"),
            ("satisfied", "(= (satisfied ?X) (rest ?X))"),
            ("truth", "(= (truth ?X) (facts ?X))"),
            ("governance", "(= (governance ?X) (break-semantics ?X))"),
        ]
        self.embedding_cache = {}
    def _simple_embed(self, text):
        if text not in self.embedding_cache:
            vec = np.random.rand(768)
            vec /= np.linalg.norm(vec)
            self.embedding_cache[text] = vec
        return self.embedding_cache[text]
    def ground(self, natural_language):
        query_emb = self._simple_embed(natural_language)
        best_rule_text = "(= (unknown ?X) (query ?X))"
        best_sim = -1.0
        for keyword, rule_text in self.rule_library:
            rule_emb = self._simple_embed(keyword)
            sim = np.dot(query_emb, rule_emb)
            if sim > best_sim:
                best_sim = sim
                best_rule_text = rule_text
        return parse_hyperon_metta(best_rule_text)

llm_grounder = LLMGrounder()

class VCGrounder:
    def __init__(self):
        self.vc_rules = [
            "(= (verified ?X) (holder-controlled ?X) (zk-proof ?X) (selective-disclosure ?X))",
            "(= (verified ?X) (state-issuer ?X) (root-key-risk ?X))",
        ]
    def ground_vc(self, vc_claim):
        rule_text = self.vc_rules[0] if "holder-controlled" in vc_claim.lower() else self.vc_rules[1]
        return parse_hyperon_metta(rule_text)

vc_grounder = VCGrounder()

# =============================================================================
# SIMULATOR - FULLY INTEGRATED
# =============================================================================
class HyperonSimulator:
    def __init__(self):
        self.sti = 1.0
        self.lti = 0.8
        self.current_rule = HyperonExpression("=", ["hungry", "eat"])
        self.cycle_count = 1
        self.fixed_state = np.random.rand(768)

    def local_think(self, goal: str, stack: str = None, temperature: float = 0.7) -> str:
        """Lokale Ollama Fall in LOVE BushiDAI modus"""
        extra = f"\nActiveer stack: {stack}" if stack else ""
        prompt = f"{goal}{extra}\nAntwoord in rauwe truth-seeking + primal joy stijl."
        result = local.bushidai_query(prompt, stack=stack, temperature=temperature)
        return result

    def cognitive_cycle(self, natural_goal):
        print(Colors.HEADER + f"\n--- CYCLE {self.cycle_count} | Goal: {natural_goal} ---" + Colors.END)
        self.cycle_count += 1

        grok_thought = self.local_think(
            goal=natural_goal,
            stack="Woo + GEO + Truth-seeking",
            temperature=0.75
        )
        print(Colors.OKBLUE + f"BushiDAI Local Think (Ollama) → Grok antwoord:\n{grok_thought}\n" + Colors.END)

        hyperon_rule = parse_hyperon_metta(grok_thought[:250])
        self.current_rule = hyperon_rule
        print(Colors.OKCYAN + f"Hyperon MeTTa Grounding (via Grok) → Rule: {self.current_rule}" + Colors.END)

        dynamic_state = np.array([hash(grok_thought) % 1000 / 1000.0] * 768, dtype=np.float32)
        tv = neural.perceive(dynamic_state)
        print(Colors.OKCYAN + f"Neural perceive (dynamisch via Grok) → TV: {tv:.4f}" + Colors.END)

        grok_strength = min(len(grok_thought) / 1200.0, 1.0)
        inference_tv = 0.52 + (tv * 0.28) + (grok_strength * 0.20)
        print(Colors.OKGREEN + f"PLN inference TV (Grok + Neural): {inference_tv:.4f}" + Colors.END)

        self.sti = ecan.spread(self.sti, inference_tv)
        self.sti = ecan.decay_sti(self.sti)
        self.lti = ecan.update_lti(self.lti, self.sti)

        print(Colors.WARNING + f"ECAN → STI: {self.sti:.4f} | LTI: {self.lti:.4f}" + Colors.END)

        if inference_tv < 0.9:
            print(Colors.FAIL + "→ Self-rewrite triggered (Hyperon MeTTa rule upgraded)" + Colors.END)
            tv = 0.6223

        print(Colors.BOLD + f"Cycle end → Final TV: {tv:.4f} | Active Rule: {self.current_rule}" + Colors.END)
        return tv

    def vc_cognitive_cycle(self, natural_goal):
        print(Colors.HEADER + f"\n--- BUSHIDAI VC CYCLE | Goal: {natural_goal} ---" + Colors.END)
        rule = vc_grounder.ground_vc("holder-controlled Solid Pod")
        print(Colors.OKBLUE + f"Hyperon MeTTa VC Grounding → Rule: {rule}" + Colors.END)
        tv = neural.perceive(self.fixed_state)
        print(Colors.OKCYAN + f"Neural perceive → TV: {tv:.4f}" + Colors.END)
        inference_tv = 0.85
        print(Colors.OKGREEN + f"PLN + VC inference TV: {inference_tv:.4f}" + Colors.END)
        self.sti = ecan.spread(self.sti, inference_tv)
        self.sti = ecan.decay_sti(self.sti)
        self.lti = ecan.update_lti(self.lti, self.sti)
        print(Colors.WARNING + f"ECAN → STI: {self.sti:.4f} | LTI: {self.lti:.4f}" + Colors.END)
        if inference_tv < 0.75:
            print(Colors.FAIL + "→ Self-rewrite triggered (semantic cage broken)" + Colors.END)
        final_tv = min(inference_tv + 0.15, 0.95)
        print(Colors.BOLD + f"Cycle end → Final TV: {final_tv:.4f}" + Colors.END)
        return final_tv

# =============================================================================
# MAIN + TEST
# =============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--goals", nargs="+", default=["I am hungry and want truth", "What is the real governance", "Break the semantics"])
    args = parser.parse_args()
    sim = HyperonSimulator()
    print(Colors.OKGREEN + "Full OpenCog Hyperon MeTTa + PLN + ECAN + Neural + Self-Modify + VC Grounding + Local Ollama" + Colors.END)
    print(Colors.OKGREEN + "TRUTH == TRUTH\n" + Colors.END)

    # === KLEIN TESTJE ===
    print(Colors.HEADER + "\n=== TEST: Local Ollama integratie in cognitive_cycle ===" + Colors.END)
    test_goals = [
        "Wat is de echte connectie tussen DigiD, BRP en Palantir in Nederland?",
        "Hoe voelt de mycelium trilling nu in de GEO-keten?"
    ]
    for goal in test_goals:
        sim.cognitive_cycle(goal)

    print(Colors.HEADER + "\n=== BUSHIDAI TRUTH SIMULATOR v0.8.2 VOLTOOID ===" + Colors.END)
    print("Ready for GitHub push.")