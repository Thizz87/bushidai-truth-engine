# 🧬 Multi-Vaccine Joint Optimization Tracker & Diagnostics

A precision desktop bioinformatics application designed for **Open Reading Frame (ORF) Stability Analytics** and mutational variant diagnostics. This tool enables clinical researchers to audit patient sequencing strings against commercial vaccine reference blueprints using native C-optimized **Biopython data engines**.

---

## 📁 Repository Structure

```text
Covid Check/
├── README.md                    <-- This documentation manual
├── multi_spike_tracker.py       <-- Main Desktop Application Script
├── docs/                        <-- Technical summary sheets, cheat sheets, and notes
└── diagnostic_reports/          <-- Auto-generated JSON & CSV analytical log dumps
```

---

## ⚡ Core Operational Features

*   **Translational Adaptation Index (CAI):** Computes precise host-expression synonymous codon bias, mapping ribosome kinetics down the open reading frame.
*   **Thermodynamic GC Sliding Window:** Slides a 75-nucleotide window to map local GC percentage drops below **40%**. Identifies structural vulnerability loops susceptible to rapid enzymatic degradation.
*   **Hazardous Motif Scanning:** Extracts hidden cellular transcription traps including premature polyadenylation flags (`AATAAA` / `ATTAAA`) and Poly-U slips (`TTTTTT`).
*   **Dual-Pipeline Auto-Export:** Every scan automatically pipes structured metrics to **JSON** datasets and formatting-ready **CSV** spreadsheets for immediate laboratory cross-analysis.

---

## 🚀 Getting Started

### 1. Installation & Prerequisites
The engine uses standard Python 3.8+ desktop packages along with the core **Biopython** processing layer. Run the following command in your terminal terminal:

```bash
pip install biopython
```

### 2. Execution Run
Launch the desktop workspace suite directly from your terminal using:

```bash
python3 multi_spike_tracker.py
```

---

## 📂 Laboratory File Interoperability

The interface uploader utilizes `Bio.SeqIO` to natively process standard clinical and database file formats:
*   **FASTA (`.fasta`, `.fa`, `.fna`):** Automatic header stripping (`>`) and clean open reading frame ingestion.
*   **GenBank (`.gb`, `.genbank`):** Isolates the raw nucleotide base sequence out of highly annotated portal records.
*   **Plain Text (`.txt`):** Auto-purges hidden carriage returns (`\r`), spaces, and string anomalies.

---

## 🛡️ Research Disclaimer
*This platform functions strictly as an open-source, informational sequence metric tracker for computational biology tracking and verification. It is not an alternative to professional clinical medical advice, top-tier clinical diagnostic assays, or personalized therapeutic diagnostics.*
