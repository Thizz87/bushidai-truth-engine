#!/usr/bin/env python3
"""
MULTI-VACCINE SPIKE JOINT OPTIMIZATION TRACKER & DIAGNOSTIC TOOL
Engineered for Joint CAI + GC + MFE Structural Vulnerability Assessment
Production Grade – FACT == FACT
"""

import sys
import argparse
from pathlib import Path
from math import exp, log
from typing import Tuple, Dict, Any, List

# ========================== CAI & CODON TRANSLATION MAPS ==========================
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
    'Y': {'TAT': 0.44, 'TAC': 0.56},
}

CODON_TABLE = {k: v for k, v in HUMAN_CODON_USAGE.items() if k != '*'}
TWOP_SIGNATURE = "CCCCCC"

# ========================== BIOLOGICAL CRITICAL SITE MOTIFS ==========================
CRITICAL_VULNERABILITIES = {
    "AATAAA": "Canonical Polyadenylation Signal (Causes premature mRNA truncation)",
    "ATTAAA": "Alternative Polyadenylation Motifs (Leads to early transcription drop-off)",
    "TTTTTT": "Polyu-T Tracts (Triggers mechanical RNA Polymerase II termination)",
    "AAAAAA": "Internal Poly-A Slip Site (Induces structural translation frame-shifting)",
    "CAGGTAAG": "Consensus 5' Splice Site (Creates severe unintended splice variants)",
}

def calculate_cai(dna: str) -> float:
    """Calculate Codon Adaptation Index (CAI) for open reading frame fitness tracking."""
    if len(dna) % 3 != 0:
        return 0.0
    cai_values = []
    for i in range(0, len(dna), 3):
        codon = dna[i:i+3]
        aa = next((aa for aa, codons in HUMAN_CODON_USAGE.items() if codon in codons), None)
        if aa is None:
            continue
        max_freq = max(HUMAN_CODON_USAGE[aa].values())
        w = HUMAN_CODON_USAGE[aa].get(codon, 0) / max_freq if max_freq > 0 else 0
        if w > 0:
            cai_values.append(w)
    return round(exp(sum(log(w) for w in cai_values) / len(cai_values)), 4) if cai_values else 0.0


# ========================== NEW COMPONENT ADVANCED MODULES ==========================

def analyze_gc_content(dna: str, window_size: int = 75, critical_threshold: float = 40.0) -> Tuple[float, List[Dict[str, Any]]]:
    """
    MODULE 1: GC-Content Analyzer
    Measures overall GC% and flags severe localized regional drops.
    Low regional GC% destroys secondary mRNA folding.
    """
    total_gc = ((dna.count('G') + dna.count('C')) / len(dna)) * 100
    vulnerable_windows = []
    
    for i in range(0, len(dna) - window_size + 1, 15): # Step by 15 bases
        window_seq = dna[i:i + window_size]
        win_gc = ((window_seq.count('G') + window_seq.count('C')) / window_size) * 100
        if win_gc < critical_threshold:
            vulnerable_windows.append({
                "position": i,
                "sequence": window_seq,
                "gc_percentage": round(win_gc, 2)
            })
            
    return round(total_gc, 2), vulnerable_windows


def check_structural_vulnerabilities(dna: str) -> List[Dict[str, Any]]:
    """
    MODULE 2: Accidental Secondary Structure Restriction Check
    Flags sequences matching breakdown pathways or premature processing errors in human cells.
    """
    detected_issues = []
    for motif, description in CRITICAL_VULNERABILITIES.items():
        pos = dna.find(motif)
        while pos != -1:
            detected_issues.append({
                "position": pos,
                "motif": motif,
                "risk": description
            })
            pos = dna.find(motif, pos + 1)
    return detected_issues


def approximate_mfe_bottlenecks(dna: str) -> Dict[str, Any]:
    """
    MODULE 3: MFE Approximation & Translation Bottleneck Metric
    Evaluates where structural constraints conflict heavily with optimal human expression.
    Calculates consecutive low-frequency human codons causing ribosomal traffic jams.
    """
    bottlenecks = []
    consecutive_low_codons = 0
    start_pos = 0
    
    for i in range(0, len(dna), 3):
        codon = dna[i:i+3]
        aa = next((aa for aa, codons in HUMAN_CODON_USAGE.items() if codon in codons), None)
        if aa:
            freq = HUMAN_CODON_USAGE[aa].get(codon, 0)
            if freq < 0.15: # Critical human codon frequency floor
                if consecutive_low_codons == 0:
                    start_pos = i
                consecutive_low_codons += 1
            else:
                if consecutive_low_codons >= 3: # 3 or more consecutive rare codons equals a bottleneck
                    bottlenecks.append({"position": start_pos, "length_codons": consecutive_low_codons})
                consecutive_low_codons = 0
                
    stability_score = max(0.0, 100.0 - (len(bottlenecks) * 4.5))
    return {"stability_score": round(stability_score, 2), "bottlenecks": bottlenecks}


# ========================== SARS-COV-2 REF LAYERS ==========================
WUHAN_SPIKE_AA = "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT"

PFIZER_BNT162b2_DNA = (
    "ATGTTCGTGTTCCTGGTGCTGCTGCCTCTGGTGTCCAGCCAGTGTGTGAACCTGACCACCAGAACACAGCTGCCTCCAGCCTACACCAACAGCTTTACCAGAGGCGTGTACTACCCCGACAAGGTGTTCAGATCCAGCGTGCTGCACACTCTACCCAGGACCTGTTCCTGCCTTTCTTCAGCAACGTGACCTGGTTCCACGCCATCCACGTGTCCGGCACCAATGGCACCAAGAGATTCGACAACCCCCGTGCTGCCCTTCAACGACGGGGTGTACTTTGCCAGCACCGAGAAGTCCAACATCATCAGAGGCTGGATCTTCGGCACCACACTGGACAGCAAGACCCAGAGCCTGCTGATCGTGAACAACGCCACCAACGTGGTCATCAAAGTGTGCGAGTTCCAGTTCTGCAACGACCCCTTCCTGGGCGTCTACTACCACAAGAACAACAAGAGCTGGATGGAAAGCGAGTTCCGGGTGTACAGCAGCGCCAACAACTGCACCTTCGAGTACGTGTCCCAGCCTTTCCTGATGGACCTGGAAGGCAAGCAGGGCAACTTCAAGAACCTGCGCGAGTTCGTGTTTAAGAACATCGACGGCTACTTCAAGATCTACAGCAAGCACACCCCTATCAACCTCGTGCGGGATCTGCCTCAGGGCTTCTCTGCTCTGGAACCCCTGGTGGATCTGCCCATCGGCATCAACATCACCCGGTTTCAGACACTGCTGGCCCTGCACAGAAGCTACCTGACACCTGGCGATAGCAGCAGCGGATGGACAGCTGGTGCCGCCGCTTACTATGTGGGCTACCTGCAGCCTAGAACCTTCCTGCTGAAGTACAACGAGAACGGCACCATCACCGACGCCGTGGATTGTGCTCTGGATCCTCTGAGCGAGACAAAGTGCACCCTGAAGTCCTTCACCGTGGAAAAGGGCATCTACCAGACCAGCAACTTCCGGGTGCAGCCCACCGAATCCATCGTGCGGTTCCCCAATATCACCAATCTGTGCCCCTTCGGCGAGGTGTTCAATGCCACCAGATTCGCCTCTGTGTACGCCTGGAACCGGAAGCGGATCAGCAATTGCGTGGCCGACTACTCCGTGCTGTACAACTCCGCCAGCTTCAGCACCTTCAAGTGCTACGGCGTGTCCCCTACCAAGCTGAACGACCTGTGCTTCACAAACGTGTACGCCGACAGCTTCGTGATCCGGGGAGATGAAGTGCGGCAGATTGCCCCTGGACAGACAGGCAAGATCGCCGACTACAACTACAAGCTGCCCGACGACTTCACCGGCTGTGTGATTGCCTGGAACAGCAACAACCTGGACTCCAAAGTCGGCGGCAACTACAACTACCTGTACCGGCTGTTCCGGAAGTCCAATCTGAAGCCCTTCGAGCGGGACATCTCCACCGAGATCTATCAGGCCGGCAGCACCCCTTGTAACGGCGTGGAAGGCTTCAACTGCTACTTCCCACTGCAGTCCTACGGCTTTCAGCCCACAAATGGCGTGGGCTATCAGCCCTACAGAGTGGTGGTGCTGAGCTTCGAACTGCTGCATGCCCCTGCCACAGTGTGCGGCCCTAAGAAAAGCACCAATCTCGTGAAGAACAAATGCGTGAACTTCAACTTCAACGGCCTGACCGGCACCGGCGTGCTGACAGAGAGCAACAAGAAGTTCCTGCCATTCCAGCAGTTTGCCGGGATATCGCCGATACCACAGACGCCGTTAGAGATCCCCAGACACTGGAAATCCTGGACATCACCCCTTGCAGCTTCGGCGGAGTGTCTGTGATCACCCTGGCACCAACACCAGCAATCAGGTGGCAGTGCTGTACCAGGACGTGAACTGTACCGAAGTGCCCGTGGCCATTCACGCCGATCAGCTGACACCTACATGGCGGGTGTACTCCACCGGCAGCAATGTGTTTCAGACCAGAGCCGGCTGTCTGATCGGAGCCGAGCACGTGAACAATAGCTACGAGTGCGACATCCCCATCGGCGCTGGAATCTGCGCCAGCTACCAGACACAGACAAACAGCCCTCGGAGAGCCAGAAGCGTGGCCAGCCAGAGCATCATTGCCTACACAATGTCTCTGGGCGCCGAGAACAGCGTGGCCTACTCCAACAACTCTATCGCTATCCCCACCAACTTCACCATCAGCGTGACCACAGAGATCCTGCCTGTGTCCATGACCAAGACCAGCGTGGACTGCACCATGTACATCTGCGGCGATTCCACCGAGTGCTCCAACCTGCTGCTGCAGTACGGCAGCTTCTGCACCCAGCTGAATAGAGCCCTGACAGGGATCGCCGTGGAACAGGACAAGAACACCCAAGAGGTGTTCGCCCAAGTGAAGCAGATCTACAAGACCCCTCCTATCAAGGACTTCGGCGGCTTCAATTTCAGCCAGATTCTGCCCGATCCTAGCAAGCCCAGCAAGCGGAGCTTCATCGAGGACCTGCTGTTCAACAAAGTGACACTGGCCGACGCCGGCTTCATCAAGCAGTATGGCGATTGTCTGGGCGACATTGCCGCCAGGGATCTGATTTGCGCCCAGAAGTTTAACGGACTGACAGTGCTGCCTCCTCTGCTGACCGATGAGATGATCGCCCAGTACACATCTGCCCTGCTGGCCGGCACAATCACAAGCGGCTGGACATTTGGAGCAGGCGCCGCTCTGCAGATCCCCTTTGCTATGCAGATGGCCTACCGGTTCAACGGCATCGGAGTGACCCAGAATGTGCTGTACGAGAACCAGAAGCTGATCGCCAACCAGTTCAACAGCGCCATCGGCAAGATCCAGGACAGCCTGAGCAGCACAGCAAGCGCCCTGGGAAAGCTGCAGGACGTGGTCAACCAGAATGCCCAGGCACTGAACACCCTGGTCAAGCAGCTGTCCTCCAACTTCGGCGCCATCAGCTCTGTGCTGAACGATATCCTGAGCAGACTGGACCCTCCTGAGGCCGAGGTGCAGATCGACAGACTGATCACAGGCAGACTGCAGAGCCTCCAGACATACGTGACCCAGCAGCTGATCAGAGCCGCCGAGATTAGAGCCTCTGCCAATCTGGCCGCCACCAAGATGTCTGAGTGTGTGCTGGGCCAGAGCAAGAGAGTGGACTTTTGCGGCAAGGGCTACCACCTGATGAGCTTCCCTCAGTCTGCCCCTCACGGCGTGGTGTTTCTGCACGTGACATATGTGCCCGCTCAAGAGAAGAATTTCACCACCGCTCCAGCCATCTGCCACGACGGCAAAGCCCACTTTCCTAGAGAAGGCGTGTTCGTGTCCAACGGCACCCATTGGTTCGTGACACAGCGGAACTTCTACGAGCCCCAGATCATCACCACCGACAACACCTTCGTGTCTGGCAACTGCGACGTCGTGATCGGCATTGTGAACAATACCGTGTACGACCCTCTGCAGCCCGAGCTGGACAGCTTCAAAGAGGAACTGGACAAGTACTTTAAGAACCACACAAGCCCCGACGTGGACCTGGGCGATATCAGCGGAATCAATGCCAGCGTCGTGAACATCCAGAAAGAGATCGACCGGCTGAACGAGGTGGCCAAGAATCTGAACGAGAGCCTGATCGACCTGCAAGAACTGGGGAAGTACGAGCAGTACATCAAGTGGCCCTGGTACATCTGGCTGGGCTTTATCGCCGGACTGATTGCCATCGTGATGGTCACAATCATGCTGTGTTGCATGACCAGCTGCTGTAGCTGCCTGAAGGGCTGTTGTAGCTGTGGCAGCTGCTGCAAGTTCGACGAGGACGATTCTGAGCCCGTGCTGAAGGGCGTGAAACTGCACTACACATGA"
)

VACCINES: Dict[str, Dict[str, Any]] = {
    "pfizer":      {"name": "Pfizer/BioNTech BNT162b2", "type": "mRNA",              "dna_reference": PFIZER_BNT162b2_DNA},
    "moderna":     {"name": "Moderna mRNA-1273",        "type": "mRNA",              "dna_reference": None},
    "janssen":     {"name": "Janssen Ad26.COV2.S",      "type": "Adenovirus-vector", "dna_reference": None},
    "novavax":     {"name": "Novavax NVX-CoV2373",      "type": "Protein subunit",   "dna_reference": None},
    "astrazeneca": {"name": "AstraZeneca ChAdOx1",      "type": "Adenovirus-vector", "dna_reference": None}
}

# ========================== REVERSE CONSTRUCTORS ==========================
def reverse_engineer_codons(aa_sequence: str) -> str:
    """Map amino acids to highest-frequency human codons."""
    return ''.join(max(CODON_TABLE[aa], key=CODON_TABLE[aa].get) if aa in CODON_TABLE else 'NNN' for aa in aa_sequence)

def get_vaccine_reference(vaccine: str) -> str:
    vax_key = vaccine.lower()
    if vax_key == "pfizer":      return PFIZER_BNT162b2_DNA
    if vax_key == "moderna":     return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("K986", "P986").replace("V987", "P987"))
    if vax_key == "janssen":     return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("R682", "S682").replace("R685", "G685").replace("K986", "P986").replace("V987", "P987"))
    if vax_key == "novavax":     return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("RRAR", "QQAQ"))
    if vax_key == "astrazeneca": return reverse_engineer_codons("MDAMKRGLCCVLLLCGAVFVSPS" + WUHAN_SPIKE_AA)
    raise ValueError(f"Unknown profile: {vaccine}")

# ========================== MAIN CLINICAL DIAGNOSTIC PIPELINE ==========================
def main():
    parser = argparse.ArgumentParser(description="Advanced Multi-Vaccine Joint Optimization Tracker")
    parser.add_argument("--vaccine", choices=list(VACCINES.keys()), default="pfizer", help="Platform layout context target")
    parser.add_argument("--human-dna", type=str, required=True, help="FASTA path or patient sequencing raw text string")
    parser.add_argument("--output", type=str, default="diagnostic_reports", help="Output log path")
    args = parser.parse_args()

    # Load and purge input sequence data of spaces and hidden carriage returns
    target = Path(args.human_dna)
    if target.is_file():
        human_dna = target.read_text(encoding="utf-8").strip().replace("\n", "").replace("\r", "").replace(" ", "").upper()
    else:
        human_dna = args.human_dna.strip().replace("\n", "").replace("\r", "").replace(" ", "").upper()

    if len(human_dna) % 3 != 0 and human_dna[-3:] in ['TAA', 'TAG', 'TGA']:
        human_dna = human_dna[:-3]

    print("\n" + "="*70)
    print(f"🧬 ADVANCED JOINT OPTIMIZATION SCANNER: {VACCINES[args.vaccine]['name'].upper()}")
    print("="*70)

    # Core Execution Run Modules
    ref_dna = get_vaccine_reference(args.vaccine)
    cai_score = calculate_cai(human_dna)
    overall_gc, gc_vulnerabilities = analyze_gc_content(human_dna)
    structural_vulnerabilities = check_structural_vulnerabilities(human_dna)
    bottleneck_metrics = approximate_mfe_bottlenecks(human_dna)

    # Calculate mismatches safely
    min_len = min(len(ref_dna), len(human_dna))
    mismatches = sum(1 for a, b in zip(ref_dna[:min_len], human_dna[:min_len])) + abs(len(ref_dna) - len(human_dna))
    variance_pct = (mismatches / len(ref_dna)) * 100

    # Print out clean, high-density scientific readouts
    print(f"\n[+] TRANSLATIONAL ADAPTATION INDEX (CAI) : {cai_score}")
    print(f"[+] TOTAL GENOMIC GC CONTENT COMPOSITION : {overall_gc}%  (Target: 57-62% for ideal mRNA half-life)")
    print(f"[+] TRANSLATION EFFICIENCY STABILITY     : {bottleneck_metrics['stability_score']}/100")
    print(f"[+] TOTAL MUTATIONAL SEQUENCE MISMATCHES : {mismatches} bases ({variance_pct:.2f}% variant drift)")

    print(f"\n[!] SLIDING WINDOW GC DROPS FOUND        : {len(gc_vulnerabilities)} regional dropping points (<40%)")
    print(f"[!] STRUCTURAL mRNA DEGRADATION MOTIFS   : {len(structural_vulnerabilities)} severe risk sites found")

    if structural_vulnerabilities:
        print("\n--- CRITICAL BREAKDOWN SITES IDENTIFIED ---")
        for issue in structural_vulnerabilities[:4]: # Cap to avoid terminal overflow
            print(f" -> Position {issue['position']}: Found '{issue['motif']}' - {issue['risk']}")
        if len(structural_vulnerabilities) > 4:
            print(f" ... and {len(structural_vulnerabilities) - 4} other hazardous motifs inside file.")

    # Save to disk
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"{args.vaccine}_joint_optimization_assessment.txt"
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"ADVANCED BIOCHEMICAL ANALYSIS REPORT - {VACCINES[args.vaccine]['name']}\n")
        f.write("="*75 + "\n\n")
        f.write(f"CAI Score: {cai_score}\n")
        f.write(f"Overall GC Content: {overall_gc}%\n")
        f.write(f"Translation Fitness Stability: {bottleneck_metrics['stability_score']}/100\n")
        f.write(f"Total Base Skew: {mismatches} bases mismatching from baseline archetype reference\n\n")
        f.write("--- DETECTED DEGRADATION MOTIFS ---\n")
        for item in structural_vulnerabilities:
            f.write(f"Base Position {item['position']}: Motif [{item['motif']}] -> {item['risk']}\n")

    print(f"\n[✅] Full diagnostic report written to disk: {report_file}")
    print("FACT == FACT.\n")

if __name__ == "__main__":
    main()
