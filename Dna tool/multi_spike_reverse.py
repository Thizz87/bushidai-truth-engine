#!/usr/bin/env python3
"""
MULTI-VACCINE JOINT OPTIMIZATION SCANNER
Clean Base Engine + Refined GUI Integration
TRUTH == TRUTH
"""

import sys
import json
import csv
from pathlib import Path
from math import exp, log
from typing import Tuple, Dict, Any, List

try:
    from Bio.Seq import Seq
except ImportError:
    print("[-] Missing dependency: pip install biopython")
    sys.exit(1)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ========================== CODON & VULNERABILITY TABLES ==========================
HUMAN_CODON_USAGE = {
    'A': {'GCT': 0.26, 'GCC': 0.40, 'GCA': 0.23, 'GCG': 0.11},
    'C': {'TGT': 0.46, 'TGC': 0.54},
    'D': {'GAT': 0.46, 'GAC': 0.54},
    'E': {'GAA': 0.42, 'GAG': 0.58},
    'F': {'TTT': 0.46, 'TTC': 0.54},
    'G': {'GGT': 0.16, 'GGC': 0.34, 'GGA': 0.25, 'GGG': 0.25},
    'H': {'CAT': 0.42, 'CAC': 0.58},
    'I': {'ATT': 0.36, 'ATC': 0.47, 'ATA': 0.17},
    'K': {'AAA': 0.43, 'AAG': 0.57},
    'L': {'TTA': 0.08, 'TTG': 0.13, 'CTT': 0.13, 'CTC': 0.20, 'CTA': 0.07, 'CTG': 0.39},
    'M': {'ATG': 1.00},
    'N': {'AAT': 0.47, 'AAC': 0.53},
    'P': {'CCT': 0.29, 'CCC': 0.32, 'CCA': 0.28, 'CCG': 0.11},
    'Q': {'CAA': 0.27, 'CAG': 0.73},
    'R': {'CGT': 0.08, 'CGC': 0.18, 'CGA': 0.11, 'CGG': 0.20, 'AGA': 0.21, 'AGG': 0.22},
    'S': {'TCT': 0.18, 'TCC': 0.22, 'TCA': 0.15, 'TCG': 0.05, 'AGT': 0.15, 'AGC': 0.25},
    'T': {'ACT': 0.24, 'ACC': 0.36, 'ACA': 0.28, 'ACG': 0.12},
    'V': {'GTT': 0.18, 'GTC': 0.24, 'GTA': 0.11, 'GTG': 0.47},
    'W': {'TGG': 1.00},
    'Y': {'TAT': 0.44, 'TAC': 0.56}
}
CODON_TABLE = {k: v for k, v in HUMAN_CODON_USAGE.items()}

CRITICAL_VULNERABILITIES = {
    "AATAAA": "Canonical Polyadenylation Signal (premature mRNA truncation)",
    "ATTAAA": "Alternative Polyadenylation Motif",
    "TTTTTT": "Poly-U Tract (RNA Polymerase II termination)",
    "AAAAAA": "Internal Poly-A Slip Site (frameshift risk)",
    "CAGGTAAG": "Consensus 5' Splice Site"
}

WUHAN_SPIKE_AA = "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT"

# ========================== DEMO SEQUENCE ==========================
DEMO_VULNERABLE_DNA = "ATGTTCGTGTTCCTGGTGCTGCTGCCTCTGGTGTCCAGCCAGTGTGTGAACCTGACCACCAGAACACAGCTGCCTAATAAAGCCGCTACTTTTTTTGCCAGCACCGAGAAGTCCAACATCATCAGAGGCTGGATCTTCGGCACCACACTGGACAGCAAGACCCAGAGCCTGCTGATCGTGAACAACGCCACCAACGTGGTCATCAAAGTGTGCGAGTTCCAGTTCCAGGTAAGCCCTTCCTGGGCGTCTACTACCACAAGAACAACAAGAGCTGGATGGAAAGCGAGTTCCGGGTGTACAAAAAAAGCCAACAACTGCACCTTCGAGTACGTGTCCCAGCCTTTCCTGATGGACCTGGAAGGCAAGCAGGGCAACTTCAAGAACCTGCGCGAGTTCGTGTTTAAGAACATCGACGGCTACTTCAAGATCTACAGCAAGCACACCCCTATCAACCTCGTGCGGGATCTGCCTCAGGGCTTCTCTGCTCTGGAACCCCTGGTGGATCTGCCCATCGGCATCAACATCACCCGGTTT"

# ========================== PFIZER ==========================
PFIZER_BNT162b2_DNA = "ATGTTCGTGTTCCTGGTGCTGCTGCCTCTGGTGTCCAGCCAGTGTGTGAACCTGACCACCAGAACACAGCTGCCTCCAGCCTACACCAACAGCTTTACCAGAGGCGTGTACTACCCCGACAAGGTGTTCAGATCCAGCGTGCTGCACACTCTACCCAGGACCTGTTCCTGCCTTTCTTCAGCAACGTGACCTGGTTCCACGCCATCCACGTGTCCGGCACCAATGGCACCAAGAGATTCGACAACCCCGTGCTGCCCTTCAACGACGGGGTGTACTTTGCCAGCACCGAGAAGTCCAACATCATCAGAGGCTGGATCTTCGGCACCACACTGGACAGCAAGACCCAGAGCCTGCTGATCGTGAACAACGCCACCAACGTGGTCATCAAAGTGTGCGAGTTCCAGTTCTGCAACGACCCCTTCCTGGGCGTCTACTACCACAAGAACAACAAGAGCTGGATGGAAAGCGAGTTCCGGGTGTACAGCAGCGCCAACAACTGCACCTTCGAGTACGTGTCCCAGCCTTTCCTGATGGACCTGGAAGGCAAGCAGGGCAACTTCAAGAACCTGCGCGAGTTCGTGTTTAAGAACATCGACGGCTACTTCAAGATCTACAGCAAGCACACCCCTATCAACCTCGTGCGGGATCTGCCTCAGGGCTTCTCTGCTCTGGAACCCCTGGTGGATCTGCCCATCGGCATCAACATCACCCGGTTTCAGACACTGCTGGCCCTGCACAGAAGCTACCTGACACCTGGCGATAGCAGCAGCGGATGGACAGCTGGTGCCGCCGCTTACTATGTGGGCTACCTGCAGCCTAGAACCTTCCTGCTGAAGTACAACGAGAACGGCACCATCACCGACGCCGTGGATTGTGCTCTGGATCCTCTGAGCGAGACAAAGTGCACCCTGAAGTCCTTCACCGTGGAAAAGGGCATCTACCAGACCAGCAACTTCCGGGTGCAGCCCACCGAATCCATCGTGCGGTTCCCCAATATCACCAATCTGTGCCCCTTCGGCGAGGTGTTCAATGCCACCAGATTCGCCTCTGTGTACGCCTGGAACCGGAAGCGGATCAGCAATTGCGTGGCCGACTACTCCGTGCTGTACAACTCCGCCAGCTTCAGCACCTTCAAGTGCTACGGCGTGTCCCCTACCAAGCTGAACGACCTGTGCTTCACAAACGTGTACGCCGACAGCTTCGTGATCCGGGGAGATGAAGTGCGGCAGATTGCCCCTGGACAGACAGGCAAGATCGCCGACTACAACTACAAGCTGCCCGACGACTTCACCGGCTGTGTGATTGCCTGGAACAGCAACAACCTGGACTCCAAAGTCGGCGGCAACTACAATTACCTGTACCGGCTGTTCCGGAAGTCCAATCTGAAGCCCTTCGAGCGGGACATCTCCACCGAGATCTATCAGGCCGGCAGCACCCCTTGTAACGGCGTGGAAGGCTTCAACTGCTACTTCCCACTGCAGTCCTACGGCTTTCAGCCCACAAATGGCGTGGGCTATCAGCCCTACAGAGTGGTGGTGCTGAGCTTCGAACTGCTGCATGCCCCTGCCACAGTGTGCGGCCCTAAGAAAAGCACCAATCTCGTGAAGAACAAATGCGTGAACTTCAACTTCAACGGCCTGACCGGCACCGGCGTGCTGACAGAGAGCAACAAGAAGTTCCTGCCATTCCAGCAGTTCGGCCGGGATATCGCCGATACCACAGACGCCGTTAGAGATCCCCAGACACTGGAAATCCTGGACATCACCCCTTGCAGCTTCGGCGGAGTGTCTGTGATCACCCCTGGCACCAACACCAGCAATCAGGTGGCAGTGCTGTACCAGGACGTGAACTGTACCGAAGTGCCCGTGGCCATTCACGCCGATCAGCTGACACCTACATGGCGGGTGTACTCCACCGGCAGCAATGTGTTTCAGACCAGAGCCGGCTGTCTGATCGGAGCCGAGCACGTGAACAATAGCTACGAGTGCGACATCCCCATCGGCGCTGGAATCTGCGCCAGCTACCAGACACAGACAAACAGCCCTCGGAGAGCCAGAAGCGTGGCCAGCCAGAGCATCATTGCCTACACAATGTCTCTGGGCGCCGAGAACAGCGTGGCCTACTCCAACAACTCTATCGCTATCCCCACCAACTTCACCATCAGCGTGACCACAGAGATCCTGCCTGTGTCCATGACCAAGACCAGCGTGGACTGCACCATGTACATCTGCGGCGATTCCACCGAGTGCTCCAACCTGCTGCTGCAGTACGGCAGCTTCTGCACCCAGCTGAATAGAGCCCTGACAGGGATCGCCGTGGAACAGGACAAGAACACCCAAGAGGTGTTCGCCCAAGTGAAGCAGATCTACAAGACCCCTCCTATCAAGGACTTCGGCGGCTTCAATTTCAGCCAGATTCTGCCCGATCCTAGCAAGCCCAGCAAGCGGAGCTTCATCGAGGACCTGCTGTTCAACAAAGTGACACTGGCCGACGCCGGCTTCATCAAGCAGTATGGCGATTGTCTGGGCGACATTGCCGCCAGGGATCTGATTTGCGCCCAGAAGTTTAACGGACTGACAGTGCTGCCTCCTCTGCTGACCGATGAGATGATCGCCCAGTACACATCTGCCCTGCTGGCCGGCACAATCACAAGCGGCTGGACATTTGGAGCAGGCGCCGCTCTGCAGATCCCCTTTGCTATGCAGATGGCCTACCGGTTCAACGGCATCGGAGTGACCCAGAATGTGCTGTACGAGAACCAGAAGCTGATCGCCAACCAGTTCAACAGCGCCATCGGCAAGATCCAGGACAGCCTGAGCAGCACAGCAAGCGCCCTGGGAAAGCTGCAGGACGTGGTCAACCAGAATGCCCAGGCACTGAACACCCTGGTCAAGCAGCTGTCCTCCAACTTCGGCGCCATCAGCTCTGTGCTGAACGATATCCTGAGCAGACTGGACCCTCCTGAGGCCGAGGTGCAGATCGACAGACTGATCACAGGCAGACTGCAGAGCCTCCAGACATACGTGACCCAGCAGCTGATCAGAGCCGCCGAGATTAGAGCCTCTGCCAATCTGGCCGCCACCAAGATGTCTGAGTGTGTGCTGGGCCAGAGCAAGAGAGTGGACTTTTGCGGCAAGGGCTACCACCTGATGAGCTTCCCTCAGTCTGCCCCTCACGGCGTGGTGTTTCTGCACGTGACATATGTGCCCGCTCAAGAGAAGAATTTCACCACCGCTCCAGCCATCTGCCACGACGGCAAAGCCCACTTTCCTAGAGAAGGCGTGTTCGTGTCCAACGGCACCCATTGGTTCGTGACACAGCGGAACTTCTACGAGCCCCAGATCATCACCACCGACAACACCTTCGTGTCTGGCAACTGCGACGTCGTGATCGGCATTGTGAACAATACCGTGTACGACCCTCTGCAGCCCGAGCTGGACAGCTTCAAAGAGGAACTGGACAAGTACTTTAAGAACCACACAAGCCCCGACGTGGACCTGGGCGATATCAGCGGAATCAATGCCAGCGTCGTGAACATCCAGAAAGAGATCGACCGGCTGAACGAGGTGGCCAAGAATCTGAACGAGAGCCTGATCGACCTGCAAGAACTGGGGAAGTACGAGCAGTACATCAAGTGGCCCTGGTACATCTGGCTGGGCTTTATCGCCGGACTGATTGCCATCGTGATGGTCACAATCATGCTGTGTTGCATGACCAGCTGCTGTAGCTGCCTGAAGGGCTGTTGTAGCTGTGGCAGCTGCTGCAAGTTCGACGAGGACGATTCTGAGCCCGTGCTGAAGGGCGTGAAACTGCACTACACATGA"
PFIZER_5UTR = "GAAUAAACUAGUAUUCUUCUGGUCCCCACAGACUCAGAGAGAACCCGCCACC"
PFIZER_POLYA = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + "GCATATGACT" + "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
PFIZER_RESIDUAL_DNA = {
    "SV40": "Aanwezig in Pfizer plasmid",
    "ori": "Aanwezig",
    "source": "McKernan OSF 2023 + Speicher et al."
}

# ========================== MODERNA ==========================
MODERNA_MRNA1273_DNA = "ATGTTCGTGTTCCTGGTGCTGCTGCCCCTGGTGAGCAGCCAGTGCGTGAACCTGACCACCCGGACCCAGCTGCCACCAGCCTACACCAACAGCTTCACCCGGGGCGTCTACTACCCCGACAAGGTGTTCCGGAGCAGCGTCCTGCACAGCACCCAGGACCTGTTCCTGCCCTTCTTCAGCAACGTGACCTGGTTCCACGCCATCCACGTGAGCGGCACCAACGGCACCAAGCGGTTCGACAACCCCGTGCTGCCCTTCAACGACGGCGTGTACTTCGCCAGCACCGAGAAGAGCAACATCATCCGGGGCTGGATCTTCGGCACCACCCTGGACAGCAAGACCCAGAGCCTGCTGATCGTGAATAACGCCACCAACGTGGTGATCAAGGTGTGCGAGTTCCAGTTCTGCAACGACCCCTTCCTGGGCGTGTACTACCACAAGAACAACAAGAGCTGGATGGAGAGCGAGTTCCGGGTGTACAGCAGCGCCAACAACTGCACCTTCGAGTACGTGAGCCAGCCCTTCCTGATGGACCTGGAGGGCAAGCAGGGCAACTTCAAGAACCTGCGGGAGTTCGTGTTCAAGAACATCGACGGCTACTTCAAGATCTACAGCAAGCACACCCCAATCAACCTGGTGCGGGATCTGCCCCAGGGCTTCTCAGCCCTGGAGCCCCTGGTGGACCTGCCCATCGGCATCAACATCACCCGGTTCCAGACCCTGCTGGCCCTGCACCGGAGCTACCTGACCCCAGGCGACAGCAGCAGCGGGTGGACAGCAGGCGCGGCTGCTTACTACGTGGGCTACCTGCAGCCCCGGACCTTCCTGCTGAAGTACAACGAGAACGGCACCATCACCGACGCCGTGGACTGCGCCCTGGACCCTCTGAGCGAGACCAAGTGCACCCTGAAGAGCTTCACCGTGGAGAAGGGCATCTACCAGACCAGCAACTTCCGGGTGCAGCCCACCGAGAGCATCGTGCGGTTCCCCAACATCACCAACCTGTGCCCCTTCGGCGAGGTGTTCAACGCCACCCGGTTCGCCAGCGTGTACGCCTGGAACCGGAAGCGGATCAGCAACTGCGTGGCCGACTACAGCGTGCTGTACAACAGCGCCAGCTTCAGCACCTTCAAGTGCTACGGCGTGAGCCCCACCAAGCTGAACGACCTGTGCTTCACCAACGTGTACGCCGACAGCTTCGTGATCCGTGGCGACGAGGTGCGGCAGATCGCACCCGGCCAGACAGGCAAGATCGCCGACTACAACTACAAGCTGCCCGACGACTTCACCGGCTGCGTGATCGCCTGGAACAGCAACAACCTCGACAGCAAGGTGGGCGGCAACTACAACTACCTGTACCGGCTGTTCCGGAAGAGCAACCTGAAGCCCTTCGAGCGGGACATCAGCACCGAGATCTACCAAGCCGGCTCCACCCCTTGCAACGGCGTGGAGGGCTTCAACTGCTACTTCCCTCTGCAGAGCTACGGCTTCCAGCCCACCAACGGCGTGGGCTACCAGCCCTACCGGGTGGTGGTGCTGAGCTTCGAGCTGCTGCACGCCCCAGCCACCGTGTGTGGCCCCAAGAAGAGCACCAACCTGGTGAAGAACAAGTGCGTGAACTTCAACTTCAACGGCCTTACCGGCACCGGCGTGCTGACCGAGAGCAACAAGAAATTCCTGCCCTTTCAGCAGTTCGGCCGGGACATCGCCGACACCACCGACGCTGTGCGGGATCCCCAGACCCTGGAGATCCTGGACATCACCCCTTGCAGCTTCGGCGGCGTGAGCGTGATCACCCCAGGCACCAACACCAGCAACCAGGTGGCCGTGCTGTACCAGGACGTGAACTGCACCGAGGTGCCCGTGGCCATCCACGCCGACCAGCTGACACCCACCTGGCGGGTCTACAGCACCGGCAGCAACGTGTTCCAGACCCGGGCCGGTTGCCTGATCGGCGCCGAGCACGTGAACAACAGCTACGAGTGCGACATCCCCATCGGCGCCGGCATCTGTGCCAGCTACCAGACCCAGACCAATTCACCCCGGAGGGCAAGGAGCGTGGCCAGCCAGAGCATCATCGCCTACACCATGAGCCTGGGCGCCGAGAACAGCGTGGCCTACAGCAACAACAGCATCGCCATCCCCACCAACTTCACCATCAGCGTGACCACCGAGATTCTGCCCGTGAGCATGACCAAGACCAGCGTGGACTGCACCATGTACATCTGCGGCGACAGCACCGAGTGCAGCAACCTGCTGCTGCAGTACGGCAGCTTCTGCACCCAGCTGAACCGGGCCCTGACCGGCATCGCCGTGGAGCAGGACAAGAACACCCAGGAGGTGTTCGCCCAGGTGAAGCAGATCTACAAGACCCCTCCCATCAAGGACTTCGGCGGCTTCAACTTCAGCCAGATCCTGCCCGACCCCAGCAAGCCCAGCAAGCGGAGCTTCATCGAGGACCTGCTGTTCAACAAGGTGACCCTAGCCGACGCCGGCTTCATCAAGCAGTACGGCGACTGCCTCGGCGACATAGCCGCCCGGGACCTGATCTGCGCCCAGAAGTTCAACGGCCTGACCGTGCTGCCTCCCCTGCTGACCGACGAGATGATCGCCCAGTACACCAGCGCCCTGTTAGCCGGAACCATCACCAGCGGCTGGACTTTCGGCGCTGGAGCCGCTCTGCAGATCCCCTTCGCCATGCAGATGGCCTACCGGTTCAACGGCATCGGCGTGACCCAGAACGTGCTGTACGAGAACCAGAAGCTGATCGCCAACCAGTTCAACAGCGCCATCGGCAAGATCCAGGACAGCCTGAGCAGCACCGCTAGCGCCCTGGGCAAGCTGCAGGACGTGGTGAACCAGAACGCCCAGGCCCTGAACACCCTGGTGAAGCAGCTGAGCAGCAACTTCGGCGCCATCAGCAGCGTGCTGAACGACATCCTGAGCCGGCTGGACCCTCCCGAGGCCGAGGTGCAGATCGACCGGCTGATCACTGGCCGGCTGCAGAGCCTGCAGACCTACGTGACCCAGCAGCTGATCCGGGCCGCCGAGATTCGGGCCAGCGCCAACCTGGCCGCCACCAAGATGAGCGAGTGCGTGCTGGGCCAGAGCAAGCGGGTGGACTTCTGCGGCAAGGGCTACCACCTGATGAGCTTTCCCCAGAGCGCACCCCACGGAGTGGTGTTCCTGCACGTGACCTACGTGCCCGCCCAGGAGAAGAACTTCACCACCGCCCCAGCCATCTGCCACGACGGCAAGGCCCACTTTCCCCGGGAGGGCGTGTTCGTGAGCAACGGCACCCACTGGTTCGTGACCCAGCGGAACTTCTACGAGCCCCAGATCATCACCACCGACAACACCTTCGTGAGCGGCAACTGCGACGTGGTGATCGGCATCGTGAACAACACCGTGTACGATCCCCTGCAGCCCGAGCTGGACAGCTTCAAGGAGGAGCTGGACAAGTACTTCAAGAATCACACCAGCCCCGACGTGGACCTGGGCGACATCAGCGGCATCAACGCCAGCGTGGTGAACATCCAGAAGGAGATCGATCGGCTGAACGAGGTGGCCAAGAACCTGAACGAGAGCCTGATCGACCTGCAGGAGCTGGGCAAGTACGAGCAGTACATCAAGTGGCCCTGGTACATCTGGCTGGGCTTCATCGCCGGCCTGATCGCCATCGTGATGGTGACCATCATGCTGTGCTGCATGACCAGCTGCTGCAGCTGCCTGAAGGGCTGTTGCAGCTGCGGCAGCTGCTGCAAGTTCGACGAGGACGACAGCGAGCCCGTGCTGAAGGGCGTGAAGCTGCACTACACCTGATAATAG"
MODERNA_RESIDUAL_DNA = {
    "SV40": "Niet gedetecteerd",
    "ori": "Aanwezig",
    "source": "McKernan OSF 2023 + Speicher et al."
}

# ========================== JANSSEN / NOVAVAX / ASTRAZENECA ==========================
JANSSEN_RESIDUAL_DNA = {
    "type": "Viral vector (Ad26)",
    "SV40": "Niet van toepassing",
    "source": "EMA/FDA assessment reports"
}
NOVAVAX_RESIDUAL_DNA = {
    "type": "Recombinant protein (baculovirus / Sf9)",
    "SV40": "Niet van toepassing",
    "source": "EMA/FDA assessment reports"
}
ASTRAZENECA_RESIDUAL_DNA = {
    "type": "Viral vector (ChAdOx1)",
    "SV40": "Niet van toepassing",
    "notes": "tPA leader sequence",
    "source": "EMA assessment report"
}

# ========================== ENGINE ==========================
def reverse_engineer_codons(aa_seq: str) -> Seq:
    return Seq(''.join(
        max(CODON_TABLE[aa], key=CODON_TABLE[aa].get) if aa in CODON_TABLE else 'NNN'
        for aa in aa_seq
    ))

def get_vaccine_reference(vaccine: str, mode: str = "real") -> Seq:
    v = vaccine.lower()
    mode = mode.lower()

    if v == "pfizer":
        return Seq(PFIZER_BNT162b2_DNA)
    if v == "moderna":
        if mode == "theoretical":
            return reverse_engineer_codons(
                WUHAN_SPIKE_AA.replace("K986", "P986").replace("V987", "P987")
            )
        return Seq(MODERNA_MRNA1273_DNA)
    if v == "janssen":
        return reverse_engineer_codons(
            WUHAN_SPIKE_AA
            .replace("R682", "S682").replace("R685", "G685")
            .replace("K986", "P986").replace("V987", "P987")
        )
    if v == "novavax":
        return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("RRAR", "QQAQ"))
    if v == "astrazeneca":
        return reverse_engineer_codons("MDAMKRGLCCVLLLCGAVFVSPS" + WUHAN_SPIKE_AA)
    return Seq("")

def get_residual_info(vaccine: str) -> dict:
    v = vaccine.lower()
    if v == "pfizer": return PFIZER_RESIDUAL_DNA
    if v == "moderna": return MODERNA_RESIDUAL_DNA
    if v == "janssen": return JANSSEN_RESIDUAL_DNA
    if v == "novavax": return NOVAVAX_RESIDUAL_DNA
    if v == "astrazeneca": return ASTRAZENECA_RESIDUAL_DNA
    return {}

def calculate_cai(dna_seq: Seq) -> float:
    if len(dna_seq) % 3 != 0 or len(dna_seq) == 0:
        return 0.0
    cai_values = []
    for i in range(0, len(dna_seq), 3):
        codon = str(dna_seq[i:i+3])
        aa = next((a for a, codons in HUMAN_CODON_USAGE.items() if codon in codons), None)
        if not aa: continue
        max_freq = max(HUMAN_CODON_USAGE[aa].values())
        w = HUMAN_CODON_USAGE[aa].get(codon, 0) / max_freq if max_freq > 0 else 0
        if w > 0: cai_values.append(w)
    return round(exp(sum(log(w) for w in cai_values) / len(cai_values)), 4) if cai_values else 0.0

def analyze_gc_content(dna_seq: Seq) -> Tuple[float, List[Dict[str, Any]]]:
    if len(dna_seq) == 0: return 0.0, []
    total_gc = ((dna_seq.count('G') + dna_seq.count('C')) / len(dna_seq)) * 100
    vulnerable = []
    for i in range(0, len(dna_seq) - 74, 15):
        window = dna_seq[i:i+75]
        win_gc = ((window.count('G') + window.count('C')) / 75) * 100
        if win_gc < 40.0:
            vulnerable.append({"position": i, "gc": round(win_gc, 2)})
    return round(total_gc, 2), vulnerable

def check_structural_vulnerabilities(dna_seq: Seq) -> List[Dict[str, Any]]:
    detected = []
    s = str(dna_seq)
    for motif, risk in CRITICAL_VULNERABILITIES.items():
        pos = s.find(motif)
        while pos != -1:
            detected.append({"position": pos, "motif": motif, "risk": risk})
            pos = s.find(motif, pos + 1)
    return detected

# ========================== GUI ==========================
class VaccineDiagnosticApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Vaccine Joint Optimization Tracker")
        self.geometry("780x720")
        self.configure(bg="#2c3e50")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11, "bold"), background="#34495e", foreground="#ecf0f1")
        style.map("TButton", background=[("active", "#1abc9c")])

        banner = tk.Label(self, text="JOINT OPTIMIZATION METRICS DIAGNOSTIC SUITE",
                          bg="#1abc9c", fg="#ffffff", font=("Helvetica", 14, "bold"), pady=12)
        banner.pack(fill=tk.X)

        main = ttk.Frame(self, padding=15)
        main.pack(fill=tk.BOTH, expand=True)

        # Vaccine choice
        ttk.Label(main, text="Target Vaccine:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.vax_choice = ttk.Combobox(main, values=["Pfizer", "Moderna", "Janssen", "Novavax", "AstraZeneca"],
                                       state="readonly", width=22)
        self.vax_choice.set("Pfizer")
        self.vax_choice.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.vax_choice.bind("<<ComboboxSelected>>", self.on_vaccine_change)

        # Mode (only relevant for Moderna)
        ttk.Label(main, text="Reference Mode:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.mode_choice = ttk.Combobox(main, values=["real", "theoretical"], state="readonly", width=12)
        self.mode_choice.set("real")
        self.mode_choice.grid(row=0, column=3, sticky=tk.W)

        # Input
        ttk.Label(main, text="Sequence Input (paste or load file):").grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(15, 2))
        self.dna_textbox = tk.Text(main, height=8, width=90, font=("Courier", 10), bg="#ecf0f1", fg="#2c3e50")
        self.dna_textbox.grid(row=2, column=0, columnspan=4, pady=5)    
        self.dna_textbox.insert(tk.END, DEMO_VULNERABLE_DNA)


        # Buttons
        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky=tk.W)

        ttk.Button(btn_frame, text="📂 Load File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⚡ Run Scan", command=self.execute_diagnostics).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="ℹ️ Residual DNA Info", command=self.show_residual).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        # Report
        ttk.Label(main, text="Diagnostic Report:").grid(row=4, column=0, columnspan=4, sticky=tk.W, pady=(15, 2))
        self.report_textbox = tk.Text(main, height=16, width=90, font=("Courier", 10, "bold"),
                                      bg="#34495e", fg="#1abc9c", relief=tk.SUNKEN)
        self.report_textbox.grid(row=5, column=0, columnspan=4, pady=5)
        self.report_textbox.insert(tk.END, "[*] Ready. Select vaccine and press Run Scan.")

        self.on_vaccine_change()  # initial state

    def on_vaccine_change(self, event=None):
        vax = self.vax_choice.get().lower()
        if vax == "moderna":
            self.mode_choice.configure(state="readonly")
        else:
            self.mode_choice.set("real")
            self.mode_choice.configure(state="disabled")

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Sequence files", "*.fasta *.fa *.txt *.fna")])
        if path:
            text = Path(path).read_text(encoding="utf-8")
            clean = "".join(line.strip() for line in text.splitlines() if not line.startswith(">")).upper()
            self.dna_textbox.delete("1.0", tk.END)
            self.dna_textbox.insert(tk.END, clean)
            messagebox.showinfo("Loaded", f"Sequence loaded from {Path(path).name}")

    def clear_fields(self):
        self.dna_textbox.delete("1.0", tk.END)
        self.report_textbox.delete("1.0", tk.END)

    def show_residual(self):
        vax = self.vax_choice.get()
        info = get_residual_info(vax)
        msg = "\n".join(f"{k}: {v}" for k, v in info.items())
        messagebox.showinfo(f"Residual DNA – {vax}", msg or "No residual DNA data available.")

    def execute_diagnostics(self):
        raw = self.dna_textbox.get("1.0", tk.END).strip().replace("\n", "").replace(" ", "").upper()
        if not raw:
            messagebox.showerror("Error", "Sequence input is empty.")
            return

        human_seq = Seq(raw)
        vax = self.vax_choice.get()
        mode = self.mode_choice.get()
        ref_seq = get_vaccine_reference(vax, mode=mode)

        cai = calculate_cai(human_seq)
        gc_pct, gc_drops = analyze_gc_content(human_seq)
        vulnerabilities = check_structural_vulnerabilities(human_seq)

        min_len = min(len(ref_seq), len(human_seq))
        mismatches = sum(1 for a, b in zip(ref_seq[:min_len], human_seq[:min_len])) + abs(len(ref_seq) - len(human_seq))
        drift = (mismatches / len(ref_seq) * 100) if len(ref_seq) > 0 else 0.0

        # Export
        out_dir = Path("diagnostic_reports")
        out_dir.mkdir(exist_ok=True)

        data = {
            "vaccine": vax,
            "mode": mode,
            "length_nt": len(human_seq),
            "cai": cai,
            "gc_percent": gc_pct,
            "mismatches": mismatches,
            "drift_percent": round(drift, 2),
            "gc_drops": len(gc_drops),
            "vulnerabilities": vulnerabilities
        }

        json_path = out_dir / f"{vax.lower()}_{mode}_report.json"
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        csv_path = out_dir / f"{vax.lower()}_{mode}_metrics.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Metric", "Value"])
            for k, v in data.items():
                if k != "vulnerabilities":
                    w.writerow([k, v])

        # Report
        self.report_textbox.delete("1.0", tk.END)
        lines = [
            "DIAGNOSTIC REPORT – FACT == FACT",
            "=" * 70,
            f"Vaccine          : {vax}  (mode: {mode})",
            f"Input length     : {len(human_seq)} nt",
            f"Reference length : {len(ref_seq)} nt",
            "-" * 70,
            f"CAI              : {cai:.4f}",
            f"GC content       : {gc_pct}%",
            f"Mismatches       : {mismatches}  ({drift:.2f}% drift)",
            f"GC drop windows  : {len(gc_drops)}",
            f"Risk motifs      : {len(vulnerabilities)}",
        ]
        if vulnerabilities:
            lines.append("\n--- Detected motifs ---")
            for item in vulnerabilities:
                lines.append(f"  pos {item['position']}: {item['motif']} → {item['risk']}")

        lines += [
            "",
            "=" * 70,
            f"JSON export : {json_path}",
            f"CSV export  : {csv_path}"
        ]
        self.report_textbox.insert(tk.END, "\n".join(lines))

if __name__ == "__main__":
    app = VaccineDiagnosticApp()
    app.mainloop()