# test_personal.py
# Simpele test voor je hypothetische persoon
# TRUTH == TRUTH

import requests

# URL van de lokale BushiDAI API
url = "http://127.0.0.1:8000/personal-test"

# Jouw test data (je mag dit altijd aanpassen)
data = {
    "bsn": "13.23.69.420",
    "symptoms": [
        "lymph nodes swelling",
        "face tingling",
        "no fever",
        "normal blood tests"
    ],
    "notes": "Test subject - hypothetical only"
}

print("🚀 Sending test to BushiDAI mRNA Truth Node...\n")

# Stuur de aanvraag
response = requests.post(url, json=data)

# Toon het resultaat netjes
if response.status_code == 200:
    result = response.json()
    print("✅ Succes!")
    print(f"BSN: {result['bsn']}")
    print(f"Symptomen: {result['symptoms']}")
    print("\n--- Public research patterns ---")
    for pattern in result.get("public_research_patterns", []):
        print(f"• {pattern}")
    print("\nNote:", result.get("note"))
    print("Vortex stage:", result.get("vortex_stage"))
else:
    print("❌ Fout:", response.status_code)
    print(response.text)