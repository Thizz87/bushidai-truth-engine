# =============================================================================
# BUSHIDAI MAIN LAUNCHER
# Run any module from one place
# =============================================================================

import argparse

print("BushiDAI Launcher")
print("Choose module to run:\n")

parser = argparse.ArgumentParser()
parser.add_argument("--core", action="store_true", help="Run core simulator (v0.8.2)")
parser.add_argument("--pdf", help="Run PDF analyser with URL or path")
args = parser.parse_args()

if args.pdf:
    print("→ Launching PDF Analyser...")
    from bushidai_pdf import BushiDAIPDF
    analyser = BushiDAIPDF()
    analyser.analyse(args.pdf)

elif args.core:
    print("→ Launching Core Simulator...")
    import bushidai_core   # runs the original simulator

else:
    print("Usage:")
    print("  python3 main.py --core")
    print("  python3 main.py --pdf https://example.com/document.pdf")
