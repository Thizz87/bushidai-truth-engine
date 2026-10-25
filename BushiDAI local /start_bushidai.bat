@echo off
title BushiDAI Local
echo.
echo  ========================================
echo   BushiDAI Local - Starten...
echo  ========================================
echo.

REM Controleer of Docker draait
docker info >nul 2>&1
if errorlevel 1 (
    echo  FOUT: Docker lijkt niet te draaien.
    echo  Start Docker Desktop en probeer opnieuw.
    echo.
    pause
    exit /b 1
)

echo  Containers starten...
docker compose up --build -d

if errorlevel 1 (
    echo.
    echo  FOUT bij het starten. Zie bovenstaande melding.
    pause
    exit /b 1
)

echo.
echo  Controleren of het model aanwezig is...
docker exec bushidai-ollama ollama list | findstr /i "qwen2.5:14b" >nul
if errorlevel 1 (
    echo.
    echo  Model qwen2.5:14b nog niet aanwezig. Downloaden...
    echo  Dit kan even duren de eerste keer.
    docker exec bushidai-ollama ollama pull qwen2.5:14b
)

echo.
echo  ========================================
echo   BushiDAI is klaar!
echo   Open: http://localhost:8501
echo  ========================================
echo.
echo  Druk op een toets om te stoppen en containers af te sluiten...
pause >nul

echo.
echo  Containers stoppen...
docker compose down
echo  Gestopt.
pause