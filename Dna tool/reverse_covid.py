#!/usr/bin/env python3
"""
MULTI-VACCINE JOINT OPTIMIZATION SCANNER - CLINICAL DESKTOP INTERFACE
Production Grade Graphical System with Automated CSV & JSON Export Pipelines
"""

import sys
import json
import csv
from pathlib import Path
from math import exp, log
from typing import Tuple, Dict, Any, List

# Core Biopython Engine Dependencies
try:
    from Bio.Seq import Seq
except ImportError:
    print("[-] Operational Requirement Missing: Please run 'pip install biopython' first.")
    sys.exit(1)

# Interface Graphical Suite
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ========================== BIOINFORMATICS ENGINE CONSTANTS ==========================
HUMAN_CODON_USAGE = {
    'A': {'GCT': 0.26, 'GCC': 0.40, 'GCA': 0.23, 'GCG': 0.11}, 'C': {'TGT': 0.46, 'TGC': 0.54},
    'D': {'GAT': 0.46, 'GAC': 0.54}, 'E': {'GAA': 0.42, 'GAG': 0.58}, 'F': {'TTT': 0.46, 'TTC': 0.54},
    'G': {'GGT': 0.16, 'GGC': 0.34, 'GGA': 0.25, 'GGG': 0.25}, 'H': {'CAT': 0.42, 'CAC': 0.58},
    'I': {'ATT': 0.36, 'ATC': 0.47, 'ATA': 0.17}, 'K': {'AAA': 0.43, 'AAG': 0.57},
    'L': {'TTA': 0.08, 'TTG': 0.13, 'CTT': 0.13, 'CTC': 0.20, 'CTA': 0.07, 'CTG': 0.39},
    'M': {'ATG': 1.00}, 'N': {'AAT': 0.47, 'AAC': 0.53}, 'P': {'CCT': 0.29, 'CCC': 0.32, 'CCA': 0.28, 'CCG': 0.11},
    'Q': {'CAA': 0.27, 'CAG': 0.73}, 'R': {'CGT': 0.08, 'CGC': 0.18, 'CGA': 0.11, 'CGG': 0.20, 'AGA': 0.21, 'AGG': 0.22},
    'S': {'TCT': 0.18, 'TCC': 0.22, 'TCA': 0.15, 'TCG': 0.05, 'AGT': 0.15, 'AGC': 0.25},
    'T': {'ACT': 0.24, 'ACC': 0.36, 'ACA': 0.28, 'ACG': 0.12}, 'V': {'GTT': 0.18, 'GTC': 0.24, 'GTA': 0.11, 'GTG': 0.47},
    'W': {'TGG': 1.00}, 'Y': {'TAT': 0.44, 'TAC': 0.56}
}
CODON_TABLE = {k: v for k, v in HUMAN_CODON_USAGE.items() if k != '*'}
TWOP_SIGNATURE = "CCCCCC"

CRITICAL_VULNERABILITIES = {
    "AATAAA": "Canonical Polyadenylation Signal (Causes premature mRNA truncation)",
    "ATTAAA": "Alternative Polyadenylation Motifs (Leads to early transcription drop-off)",
    "TTTTTT": "Polyu-T Tracts (Triggers mechanical RNA Polymerase II termination)",
    "AAAAAA": "Internal Poly-A Slip Site (Induces structural translation frame-shifting)",
    "CAGGTAAG": "Consensus 5' Splice Site (Creates severe unintended splice variants)"
}

WUHAN_SPIKE_AA = "MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPRRARSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKWPWYIWLGFIAGLIAIVMVTIMLCCMTSCCSCLKGCCSCGSCCKFDEDDSEPVLKGVKLHYT"
PFIZER_BNT162b2_DNA = "ATGTTCGTGTTCCTGGTGCTGCTGCCTCTGGTGTCCAGCCAGTGTGTGAACCTGACCACCAGAACACAGCTGCCTCCAGCCTACACCAACAGCTTTACCAGAGGCGTGTACTACCCCGACAAGGTGTTCAGATCCAGCGTGCTGCACACTCTACCCAGGACCTGTTCCTGCCTTTCTTCAGCAACGTGACCTGGTTCCACGCCATCCACGTGTCCGGCACCAATGGCACCAAGAGATTCGACAACCCCCGTGCTGCCCTTCAACGACGGGGTGTACTTTGCCAGCACCGAGAAGTCCAACATCATCAGAGGCTGGATCTTCGGCACCACACTGGACAGCAAGACCCAGAGCCTGCTGATCGTGAACAACGCCACCAACGTGGTCATCAAAGTGTGCGAGTTCCAGTTCTGCAACGACCCCTTCCTGGGCGTCTACTACCACAAGAACAACAAGAGCTGGATGGAAAGCGAGTTCCGGGTGTACAGCAGCGCCAACAACTGCACCTTCGAGTACGTGTCCCAGCCTTTCCTGATGGACCTGGAAGGCAAGCAGGGCAACTTCAAGAACCTGCGCGAGTTCGTGTTTAAGAACATCGACGGCTACTTCAAGATCTACAGCAAGCACACCCCTATCAACCTCGTGCGGGATCTGCCTCAGGGCTTCTCTGCTCTGGAACCCCTGGTGGATCTGCCCATCGGCATCAACATCACCCGGTTTCAGACACTGCTGGCCCTGCACAGAAGCTACCTGACACCTGGCGATAGCAGCAGCGGATGGACAGCTGGTGCCGCCGCTTACTATGTGGGCTACCTGCAGCCTAGAACCTTCCTGCTGAAGTACAACGAGAACGGCACCATCACCGACGCCGTGGATTGTGCTCTGGATCCTCTGAGCGAGACAAAGTGCACCCTGAAGTCCTTCACCGTGGAAAAGGGCATCTACCAGACCAGCAACTTCCGGGTGCAGCCCACCGAATCCATCGTGCGGTTCCCCAATATCACCAATCTGTGCCCCTTCGGCGAGGTGTTCAATGCCACCAGATTCGCCTCTGTGTACGCCTGGAACCGGAAGCGGATCAGCAATTGCGTGGCCGACTACTCCGTGCTGTACAACTCCGCCAGCTTCAGCACCTTCAAGTGCTACGGCGTGTCCCCTACCAAGCTGAACGACCTGTGCTTCACAAACGTGTACGCCGACAGCTTCGTGATCCGGGGAGATGAAGTGCGGCAGATTGCCCCTGGACAGACAGGCAAGATCGCCGACTACAACTACAAGCTGCCCGACGACTTCACCGGCTGTGTGATTGCCTGGAACAGCAACAACCTGGACTCCAAAGTCGGCGGCAACTACAACTACCTGTACCGGCTGTTCCGGAAGTCCAATCTGAAGCCCTTCGAGCGGGACATCTCCACCGAGATCTATCAGGCCGGCAGCACCCCTTGTAACGGCGTGGAAGGCTTCAACTGCTACTTCCCACTGCAGTCCTACGGCTTTCAGCCCACAAATGGCGTGGGCTATCAGCCCTACAGAGTGGTGGTGCTGAGCTTCGAACTGCTGCATGCCCCTGCCACAGTGTGCGGCCCTAAGAAAAGCACCAATCTCGTGAAGAACAAATGCGTGAACTTCAACTTCAACGGCCTGACCGGCACCGGCGTGCTGACAGAGAGCAACAAGAAGTTCCTGCCATTCCAGCAGTTTGCCGGGATATCGCCGATACCACAGACGCCGTTAGAGATCCCCAGACACTGGAAATCCTGGACATCACCCCTTGCAGCTTCGGCGGAGTGTCTGTGATCACCCTGGCACCAACACCAGCAATCAGGTGGCAGTGCTGTACCAGGACGTGAACTGTACCGAAGTGCCCGTGGCCATTCACGCCGATCAGCTGACACCTACATGGCGGGTGTACTCCACCGGCAGCAATGTGTTTCAGACCAGAGCCGGCTGTCTGATCGGAGCCGAGCACGTGAACAATAGCTACGAGTGCGACATCCCCATCGGCGCTGGAATCTGCGCCAGCTACCAGACACAGACAAACAGCCCTCGGAGAGCCAGAAGCGTGGCCAGCCAGAGCATCATTGCCTACACAATGTCTCTGGGCGCCGAGAACAGCGTGGCCTACTCCAACAACTCTATCGCTATCCCCACCAACTTCACCATCAGCGTGACCACAGAGATCCTGCCTGTGTCCATGACCAAGACCAGCGTGGACTGCACCATGTACATCTGCGGCGATTCCACCGAGTGCTCCAACCTGCTGCTGCAGTACGGCAGCTTCTGCACCCAGCTGAATAGAGCCCTGACAGGGATCGCCGTGGAACAGGACAAGAACACCCAAGAGGTGTTCGCCCAAGTGAAGCAGATCTACAAGACCCCTCCTATCAAGGACTTCGGCGGCTTCAATTTCAGCCAGATTCTGCCCGATCCTAGCAAGCCCAGCAAGCGGAGCTTCATCGAGGACCTGCTGTTCAACAAAGTGACACTGGCCGACGCCGGCTTCATCAAGCAGTATGGCGATTGTCTGGGCGACATTGCCGCCAGGGATCTGATTTGCGCCCAGAAGTTTAACGGACTGACAGTGCTGCCTCCTCTGCTGACCGATGAGATGATCGCCCAGTACACATCTGCCCTGCTGGCCGGCACAATCACAAGCGGCTGGACATTTGGAGCAGGCGCCGCTCTGCAGATCCCCTTTGCTATGCAGATGGCCTACCGGTTCAACGGCATCGGAGTGACCCAGAATGTGCTGTACGAGAACCAGAAGCTGATCGCCAACCAGTTCAACAGCGCCATCGGCAAGATCCAGGACAGCCTGAGCAGCACAGCAAGCGCCCTGGGAAAGCTGCAGGACGTGGTCAACCAGAATGCCCAGGCACTGAACACCCTGGTCAAGCAGCTGTCCTCCAACTTCGGCGCCATCAGCTCTGTGCTGAACGATATCCTGAGCAGACTGGACCCTCCTGAGGCCGAGGTGCAGATCGACAGACTGATCACAGGCAGACTGCAGAGCCTCCAGACATACGTGACCCAGCAGCTGATCAGAGCCGCCGAGATTAGAGCCTCTGCCAATCTGGCCGCCACCAAGATGTCTGAGTGTGTGCTGGGCCAGAGCAAGAGAGTGGACTTTTGCGGCAAGGGCTACCACCTGATGAGCTTCCCTCAGTCTGCCCCTCACGGCGTGGTGTTTCTGCACGTGACATATGTGCCCGCTCAAGAGAAGAATTTCACCACCGCTCCAGCCATCTGCCACGACGGCAAAGCCCACTTTCCTAGAGAAGGCGTGTTCGTGTCCAACGGCACCCATTGGTTCGTGACACAGCGGAACTTCTACGAGCCCCAGATCATCACCACCGACAACACCTTCGTGTCTGGCAACTGCGACGTCGTGATCGGCATTGTGAACAATACCGTGTACGACCCTCTGCAGCCCGAGCTGGACAGCTTCAAAGAGGAACTGGACAAGTACTTTAAGAACCACACAAGCCCCGACGTGGACCTGGGCGATATCAGCGGAATCAATGCCAGCGTCGTGAACATCCAGAAAGAGATCGACCGGCTGAACGAGGTGGCCAAGAATCTGAACGAGAGCCTGATCGACCTGCAAGAACTGGGGAAGTACGAGCAGTACATCAAGTGGCCCTGGTACATCTGGCTGGGCTTTATCGCCGGACTGATTGCCATCGTGATGGTCACAATCATGCTGTGTTGCATGACCAGCTGCTGTAGCTGCCTGAAGGGCTGTTGTAGCTGTGGCAGCTGCTGCAAGTTCGACGAGGACGATTCTGAGCCCGTGCTGAAGGGCGTGAAACTGCACTACACATGA"

DEMO_VULNERABLE_DNA = "ATGTTCGTGTTCCTGGTGCTGCTGCCTCTGGTGTCCAGCCAGTGTGTGAACCTGACCACCAGAACACAGCTGCCTAATAAAGCCGCTACTTTTTTTGCCAGCACCGAGAAGTCCAACATCATCAGAGGCTGGATCTTCGGCACCACACTGGACAGCAAGACCCAGAGCCTGCTGATCGTGAACAACGCCACCAACGTGGTCATCAAAGTGTGCGAGTTCCAGTTCCAGGTAAGCCCTTCCTGGGCGTCTACTACCACAAGAACAACAAGAGCTGGATGGAAAGCGAGTTCCGGGTGTACAAAAAAAGCCAACAACTGCACCTTCGAGTACGTGTCCCAGCCTTTCCTGATGGACCTGGAAGGCAAGCAGGGCAACTTCAAGAACCTGCGCGAGTTCGTGTTTAAGAACATCGACGGCTACTTCAAGATCTACAGCAAGCACACCCCTATCAACCTCGTGCGGGATCTGCCTCAGGGCTTCTCTGCTCTGGAACCCCTGGTGGATCTGCCCATCGGCATCAACATCACCCGGTTT"

# ========================== ENGINE BACKEND METHODS ==========================
def calculate_cai(dna_seq: Seq) -> float:
    if len(dna_seq) % 3 != 0 or len(dna_seq) == 0: return 0.0
    cai_values = []
    for i in range(0, len(dna_seq), 3):
        codon = str(dna_seq[i:i+3])
        aa = next((aa for aa, codons in HUMAN_CODON_USAGE.items() if codon in codons), None)
        if not aa: continue
        max_freq = max(HUMAN_CODON_USAGE[aa].values())
        w = HUMAN_CODON_USAGE[aa].get(codon, 0) / max_freq if max_freq > 0 else 0
        if w > 0: cai_values.append(w)
    return round(exp(sum(log(w) for w in cai_values) / len(cai_values)), 4) if cai_values else 0.0

def analyze_gc_content(dna_seq: Seq) -> Tuple[float, List[Dict[str, Any]]]:
    if len(dna_seq) == 0: return 0.0, []
    total_gc = ((dna_seq.count('G') + dna_seq.count('C')) / len(dna_seq)) * 100
    vulnerable_windows = []
    for i in range(0, len(dna_seq) - 75 + 1, 15):
        window_seq = dna_seq[i:i + 75]
        win_gc = ((window_seq.count('G') + window_seq.count('C')) / 75) * 100
        if win_gc < 40.0:
            vulnerable_windows.append({"position": i, "gc": round(win_gc, 2)})
    return round(total_gc, 2), vulnerable_windows

def check_structural_vulnerabilities(dna_seq: Seq) -> List[Dict[str, Any]]:
    detected = []
    dna_str = str(dna_seq)
    for motif, risk in CRITICAL_VULNERABILITIES.items():
        pos = dna_str.find(motif)
        while pos != -1:
            detected.append({"position": pos, "motif": motif, "risk": risk})
            pos = dna_str.find(motif, pos + 1)
    return detected

def reverse_engineer_codons(aa_seq: str) -> Seq:
    return Seq(''.join(max(CODON_TABLE[aa], key=CODON_TABLE[aa].get) if aa in CODON_TABLE else 'NNN' for aa in aa_seq))

def get_vaccine_reference(vaccine: str) -> Seq:
    v = vaccine.lower()
    if v == "pfizer": return Seq(PFIZER_BNT162b2_DNA)
    if v == "moderna": return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("K986", "P986").replace("V987", "P987"))
    if v == "janssen": return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("R682", "S682").replace("R685", "G685").replace("K986", "P986").replace("V987", "P987"))
    if v == "novavax": return reverse_engineer_codons(WUHAN_SPIKE_AA.replace("RRAR", "QQAQ"))
    if v == "astrazeneca": return reverse_engineer_codons("MDAMKRGLCCVLLLCGAVFVSPS" + WUHAN_SPIKE_AA)
    return Seq("")

# ========================== DESKTOP GRAPHICAL USER INTERFACE ==========================
class VaccineDiagnosticApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Vaccine Joint Optimization Tracker")
        self.geometry("750x670")
        self.configure(bg="#2c3e50")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11, "bold"), background="#34495e", foreground="#ecf0f1")
        style.map("TButton", background=[("active", "#1abc9c")])

        banner = tk.Label(self, text="JOINT OPTIMIZATION METRICS DIAGNOSTIC SUITE", 
                          bg="#1abc9c", fg="#ffffff", font=("Helvetica", 14, "bold"), pady=12)
        banner.pack(fill=tk.X)

        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Select Target Vaccine Architecture Model Blueprint:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.vax_choice = ttk.Combobox(main_frame, values=["Pfizer", "Moderna", "Janssen", "Novavax", "AstraZeneca"], 
                                       state="readonly", width=25, font=("Helvetica", 11))
        self.vax_choice.set("Pfizer")
        self.vax_choice.grid(row=0, column=1, pady=5, sticky=tk.W)

        ttk.Label(main_frame, text="Patient Sequencing Input (Paste Text String below or Load File):").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(15, 2))
        
        self.dna_textbox = tk.Text(main_frame, height=8, width=85, font=("Courier", 10), bg="#ecf0f1", fg="#2c3e50")
        self.dna_textbox.grid(row=2, column=0, columnspan=2, pady=5)
        self.dna_textbox.insert(tk.END, DEMO_VULNERABLE_DNA)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.W)

        ttk.Button(btn_frame, text="📂 Load Sequence File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⚡ Run Molecular Scan", command=self.execute_diagnostics).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 Clear Data", command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        ttk.Label(main_frame, text="Calculated Biological Diagnostic Output Report Summary:").grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(15, 2))
        
        self.report_textbox = tk.Text(main_frame, height=14, width=85, font=("Courier", 10, "bold"), bg="#34495e", fg="#1abc9c", relief=tk.SUNKEN)
        self.report_textbox.grid(row=5, column=0, columnspan=2, pady=5)
        self.report_textbox.insert(tk.END, "[*] Scanner Ready. Press 'Run Molecular Scan' to evaluate sequence metrics.")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Genomic Records", "*.fasta *.fa *.txt *.fna *.gb")])
        if file_path:
            p = Path(file_path)
            raw_text = p.read_text(encoding="utf-8").strip()
            lines = [line.strip() for line in raw_text.splitlines() if not line.startswith(">")]
            clean_dna = ''.join(lines).replace(" ", "").upper()
            self.dna_textbox.delete("1.0", tk.END)
            self.dna_textbox.insert(tk.END, clean_dna)
            messagebox.showinfo("Asset Loaded", f"Successfully extracted sequence records from: {p.name}")

    def clear_fields(self):
        self.dna_textbox.delete("1.0", tk.END)
        self.report_textbox.delete("1.0", tk.END)

    def execute_diagnostics(self):
        raw_dna = self.dna_textbox.get("1.0", tk.END).strip().replace("\n", "").replace("\r", "").replace(" ", "").upper()
        if not raw_dna:
            messagebox.showerror("Execution Aborted", "Sequence context input screen cannot be empty.")
            return

        human_seq = Seq(raw_dna)
        vax_selection = self.vax_choice.get()
        ref_seq = get_vaccine_reference(vax_selection)

        cai = calculate_cai(human_seq)
        gc_pct, gc_drops = analyze_gc_content(human_seq)
        vulnerabilities = check_structural_vulnerabilities(human_seq)

        min_len = min(len(ref_seq), len(human_seq))
        mismatches = sum(1 for a, b in zip(ref_seq[:min_len], human_seq[:min_len])) + abs(len(ref_seq) - len(human_seq))
        drift = (mismatches / len(ref_seq)) * 100 if len(ref_seq) > 0 else 0.0
        has_2p = 'YES' if TWOP_SIGNATURE in str(human_seq) else 'NO'

        # ========================== PIPELINE DATA EXPORT MODULE ==========================
        out_dir = Path("diagnostic_reports")
        out_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Compile Dataset Payload
        structured_data = {
            "vaccine_target": vax_selection,
            "sequence_length_nt": len(human_seq),
            "metrics": {
                "codon_adaptation_index_cai": round(cai, 4),
                "total_gc_percentage": gc_pct,
                "mutational_base_mismatches": mismatches,
                "variant_drift_percentage": round(drift, 2),
                "prefusion_2p_present": has_2p
            },
            "anomalies": {
                "thermodynamic_gc_drops_count": len(gc_drops),
                "degradation_motifs_count": len(vulnerabilities),
                "mapped_vulnerabilities": vulnerabilities
            }
        }

        # 2. JSON Data Writer Pipeline
        json_file = out_dir / f"{vax_selection.lower()}_report.json"
        json_file.write_text(json.dumps(structured_data, indent=4), encoding="utf-8")

        # 3. CSV Tabular Writer Pipeline
        csv_file = out_dir / f"{vax_selection.lower()}_metrics.csv"
        with open(csv_file, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric Parameter Description", "Calculated Core Value"])
            writer.writerow(["Target Vaccine Architecture", vax_selection])
            writer.writerow(["Sequence Length (Bases)", len(human_seq)])
            writer.writerow(["Codon Adaptation Index (CAI)", f"{cai:.4f}"])
            writer.writerow(["Genomic GC Content Ratio", f"{gc_pct}%"])
            writer.writerow(["Absolute Base Mismatches", mismatches])
            writer.writerow(["Sequence Drift Percentage", f"{drift:.2f}%"])
            writer.writerow(["2P Prefusion Footprint Present", has_2p])
            writer.writerow(["Vulnerable GC Windows (<40%)", len(gc_drops)])
            writer.writerow(["Identified Hazardous Motifs", len(vulnerabilities)])

        # ========================== INTERFACE REPORT RENDERING ==========================
        self.report_textbox.delete("1.0", tk.END)
        r = []
        r.append(f"DIAGNOSTIC REPORT GENERATED SUCCESSFUL - FACT == FACT")
        r.append("="*70)
        r.append(f"Target Archetype Baseline Model : {vax_selection.upper()}")
        r.append(f"Patient Processing Input Length : {len(human_seq)} nucleotides")
        r.append("-" * 70)
        r.append(f"[+] TRANSLATIONAL ADAPTATION INDEX (CAI)  : {cai:.4f}")
        r.append(f"[+] TOTAL GENOMIC GC CONTENT RATIO       : {gc_pct}% (Ideal target: 57-62%)")
        r.append(f"[+] TOTAL ALIGNMENT SEQUENCE MISMATCHES  : {mismatches} bases ({drift:.2f}% variant drift)")
        r.append(f"[+] PREFUSION 2P PROLINE SIGNATURE SITE   : {'✅ IDENTIFIED' if has_2p == 'YES' else '❌ NOT PRESENT'}")
        r.append("-" * 70)
        r.append(f"[!] THERMODYNAMIC SLIDING WINDOW GC DROPS : {len(gc_drops)} warning zones mapped")
        r.append(f"[!] ENZYMATIC mRNA DEGRADATION RECOGNITION: {len(vulnerabilities)} high-risk spots discovered")
        
        if vulnerabilities:
            r.append("\n--- CRITICAL BREAKDOWN LOCATIONS IDENTIFIED ---")
            for item in vulnerabilities:
                r.append(f" -> Position {item['position']}: Found Motif [{item['motif']}] -> {item['risk']}")

        if len(human_seq) >= 60:
            r.append("\n--- CELLULAR RIBOSOME TRANSLATION COMPLEMENT PREVIEW ---")
            r.append(f"Predicted Protein Result (First 20 AA): {str(human_seq.translate()[:20])}...")

        r.append("\n" + "="*70)
        r.append(f"[✅] AUTOMATED RESEARCH METRICS EXPORT PIPELINES SECURED:")
        r.append(f"  -> Tabular Spreadsheet Export : {csv_file}")
        r.append(f"  -> Structured Dataset JSON    : {json_file}")

        self.report_textbox.insert(tk.END, '\n'.join(r))

if __name__ == "__main__":
    app = VaccineDiagnosticApp()
    app.mainloop()
