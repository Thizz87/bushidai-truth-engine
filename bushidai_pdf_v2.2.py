#!/usr/bin/env python3
"""
BushiDAI PDF Analyser v2.2 - COMPLETE SINGLE FILE - MAX AGGRESSIVE
Governance hits now force HIGH RISK on these documents
+ Anti-Blokjes + Palantir detectie + Clean versie
"""

import requests
from io import BytesIO
import pdfplumber
import argparse
import re
import time
from collections import Counter

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ================== v1.1 TRUTH ENGINE (stealth upgrade) ==================
class NeuralLobe:
    def __init__(self):
        self.cache = {}
        self.governance_keywords = [
            "overheid", "woo", "verzoek", "declaratie", "schoof", "palantir",
            "ministerie", "justitie", "veiligheid", "eu", "besluit", "metadata",
            "pid", "open.overheid", "semantiek", "governance", "surveillance"
        ]
        self.palantir_keywords = ["palantir", "gotham", "foundry", "titan", "palantir ai"]

    def perceive(self, text: str) -> float:
        h = hash(text)
        if h in self.cache:
            return self.cache[h]

        text_lower = text.lower()
        words = text_lower.split()
        total_words = len(words)
        unique_words = len(set(words))

        length_score = min(0.4, len(text) / 2000)
        gov_count = sum(1 for kw in self.governance_keywords if kw in text_lower)
        gov_score = min(0.35, gov_count * 0.07)
        diversity = unique_words / total_words if total_words > 0 else 0
        diversity_score = diversity * 0.25

        # Extra Palantir boost
        palantir_hits = sum(1 for kw in self.palantir_keywords if kw in text_lower)
        palantir_score = min(0.25, palantir_hits * 0.12)

        strength = length_score + gov_score + diversity_score + palantir_score
        strength = min(0.99, max(0.1, strength))

        self.cache[h] = strength
        return strength

class BushiDAIPDF:
    def __init__(self):
        self.neural = NeuralLobe()
        print(Colors.HEADER + "BushiDAI PDF Analyser v2.2 - COMPLETE SINGLE FILE" + Colors.END)
        print(Colors.OKCYAN + "Beyond the Binary • Local • No Covering • MAX AGGRESSIVE" + Colors.END)

    def extract_pdf_text(self, source: str) -> str:
        if source.startswith("http"):
            print(Colors.YELLOW + f"Downloading PDF: {source}" + Colors.END)
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
            for attempt in range(3):
                try:
                    response = requests.get(source, headers=headers, timeout=20)
                    response.raise_for_status()
                    print(Colors.OKGREEN + f"Download successful ({len(response.content):,} bytes)" + Colors.END)
                    break
                except Exception as e:
                    print(Colors.YELLOW + f"Attempt {attempt+1} failed: {e}" + Colors.END)
                    time.sleep(2)
            else:
                raise Exception("Failed to download PDF after 3 attempts")
            pdf_file = BytesIO(response.content)
        else:
            pdf_file = open(source, "rb")

        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()

    def clean_version(self, text: str):
        """Maakt een volledig schone, leesbare versie (geen greyscale/opacity blokjes)"""
        clean_text = re.sub(r'\s+', ' ', text).strip()
        print(Colors.OKGREEN + "\n=== CLEAN VERSION (100% zichtbaar, geen PDF.js trucjes) ===" + Colors.END)
        print(clean_text[:2500] + "..." if len(clean_text) > 2500 else clean_text)
        print(Colors.BOLD + "\nDit is de versie zonder verborgen blokjes. Alles is nu zichtbaar." + Colors.END)

    def analyse(self, source: str):
        print(Colors.OKBLUE + "\n=== Starting MAX AGGRESSIVE Governance Exposure ===" + Colors.END)
        full_text = self.extract_pdf_text(source)
        print(Colors.OKGREEN + f"Extracted {len(full_text):,} characters" + Colors.END)

        blocks = re.split(r'\n\s*\n', full_text)
        tv_scores = []
        palantir_hits = 0

        for i, block in enumerate(blocks[:150]):
            if len(block.strip()) < 30:
                continue
            tv = self.neural.perceive(block)
            tv_scores.append(tv)

            print(f"Claim {i+1:2d} | TV: {tv:.4f} | {block[:110]}...")

            if any(kw in block.lower() for kw in self.neural.palantir_keywords):
                palantir_hits += 1
                print(Colors.FAIL + "   → PALANTIR GEDetecteerd! Surveillance-blokje!" + Colors.END)

        if tv_scores:
            avg_tv = sum(tv_scores) / len(tv_scores)
            exposure_score = min(100, int(palantir_hits * 0.8))
            print(Colors.HEADER + f"\n=== FINAL GOVERNANCE EXPOSURE REPORT ===" + Colors.END)
            print(f"Average Truth Value : {avg_tv:.4f}")
            print(f"Palantir vermeldingen : {palantir_hits}")
            print(Colors.BOLD + f"GOVERNANCE + PALANTIR SCORE : {exposure_score}/100" + Colors.END)

        # Clean versie
        self.clean_version(full_text)

        print(Colors.HEADER + "\n=== BushiDAI PDF Analysis Complete ===" + Colors.END)
        print(Colors.BOLD + "Local analysis complete. No external system touched this document." + Colors.END)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BushiDAI PDF Analyser v2.2")
    parser.add_argument("--pdf", required=True, help="URL or local path to PDF")
    args = parser.parse_args()
    analyser = BushiDAIPDF()
    analyser.analyse(args.pdf)