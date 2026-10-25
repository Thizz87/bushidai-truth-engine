#!/bin/bash
# start_bushidai.sh
# Start BushiDAI Local (Docker)

set -e

echo
echo " ========================================"
echo "  BushiDAI Local - Starten..."
echo " ========================================"
echo

# Controleer Docker
if ! docker info >/dev/null 2>&1; then
    echo " FOUT: Docker lijkt niet te draaien."
    echo " Start Docker en probeer opnieuw."
    exit 1
fi

echo " Containers starten..."
docker compose up --build -d

echo
echo " Controleren of het model aanwezig is..."
if ! docker exec bushidai-ollama ollama list 2>/dev/null | grep -q "qwen2.5:14b"; then
    echo
    echo " Model qwen2.5:14b nog niet aanwezig. Downloaden..."
    echo " Dit kan even duren de eerste keer."
    docker exec bushidai-ollama ollama pull qwen2.5:14b
fi

echo
echo " ========================================"
echo "  BushiDAI is klaar!"
echo "  Open: http://localhost:8501"
echo " ========================================"
echo
echo " Druk op Ctrl+C om te stoppen..."

# Wacht tot gebruiker stopt
trap 'echo; echo " Containers stoppen..."; docker compose down; echo " Gestopt."; exit 0' INT
while true; do sleep 1; done