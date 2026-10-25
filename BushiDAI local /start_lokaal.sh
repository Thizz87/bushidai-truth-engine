#!/bin/bash
# start_lokaal.sh
# Start BushiDAI Local (zonder Docker)

echo
echo " ========================================"
echo "  BushiDAI Local - Starten..."
echo " ========================================"
echo

# Check Python
if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
    echo " FOUT: Python niet gevonden."
    echo " Installeer Python 3.10+"
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)

# Check Ollama
echo " Controleren of Ollama draait..."
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo " Ollama lijkt niet te draaien."
    echo " Start Ollama handmatig: ollama serve"
    echo " Download: https://ollama.com"
    exit 1
fi

# Check model
echo " Controleren of model qwen2.5:14b aanwezig is..."
if ! ollama list 2>/dev/null | grep -q "qwen2.5:14b"; then
    echo " Model niet gevonden. Downloaden..."
    ollama pull qwen2.5:14b
fi

# Dependencies
echo " Controleren dependencies..."
$PYTHON -m pip install -q -r requirements.txt

# Start
echo
echo " ========================================"
echo "  BushiDAI start..."
echo "  Browser opent op http://localhost:8501"
echo " ========================================"
echo
streamlit run app.py