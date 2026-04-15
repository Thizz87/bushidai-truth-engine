# =============================================================================
# BUSHIDAI ANTI MAIN LAUNCHER
# Centrale launcher voor alle anti-modules
# =============================================================================

import argparse
from datetime import datetime

print("🐙🦨 BUSHIDAI TRUTH ENGINE - MAIN LAUNCHER")
print("==========================================\n")

parser = argparse.ArgumentParser(description="BushiDAI Anti-Anti-API Launcher")

parser.add_argument("--voc",        action="store_true", help="Start VOC-octopus module")
parser.add_argument("--gemeente",   action="store_true", help="Start Gemeentehuizen batch")
parser.add_argument("--rechtszaak", action="store_true", help="Start persoonlijke rechtszaak cluster")
parser.add_argument("--kvk",        action="store_true", help="Start KvK batch & detail mode")
parser.add_argument("--woo",        action="store_true", help="Start Woo / TOOI live queries")
parser.add_argument("--network",    action="store_true", help="Start bedrijvennetwerk analyse")
parser.add_argument("--all",        action="store_true", help="Start alles tegelijk (overkill mode)")

args = parser.parse_args()

if args.all:
    print("🚀 OVERKILL MODE - ALL MODULES")

elif args.voc:
    print("🐙 Starting VOC-octopus module...")
    import anti_voc

elif args.gemeente:
    print("🏛️ Starting Gemeentehuizen batch...")
    import anti_gemeente

elif args.rechtszaak:
    print("⚖️ Starting persoonlijke rechtszaak cluster...")
    import anti_rechtszaak

elif args.kvk:
    print("📋 Starting KvK module...")
    import anti_kvk

elif args.woo:
    print("📜 Starting Woo / TOOI module...")
    import anti_woo

elif args.network:
    print("🌐 Starting bedrijvennetwerk analyse...")
    import anti_network

else:
    print("Geen module gekozen.\n")
    print("Beschikbare commando's:")
    print("  python bushidai_anti_main.py --voc")
    print("  python bushidai_anti_main.py --gemeente")
    print("  python bushidai_anti_main.py --rechtszaak")
    print("  python bushidai_anti_main.py --kvk")
    print("  python bushidai_anti_main.py --woo")
    print("  python bushidai_anti_main.py --network")
    print("  python bushidai_anti_main.py --all\n")

print(f"[{datetime.now().strftime('%H:%M:%S')}] Launcher klaar.")