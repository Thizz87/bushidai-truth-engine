@echo off
title BushiDAI Local
echo.
echo  ========================================
echo   BushiDAI Local - Starten...
echo  ========================================
echo.

REM --- Check Python ---
python --version >nul 2>&1
if errorlevel 1 (
    echo  FOUT: Python niet gevonden.
    echo  Installeer Python 3.10+ van https://www.python.org
    echo.
    pause
    exit /b 1
)

REM --- Check / start Ollama ---
echo  Controleren of Ollama draait...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo  Ollama lijkt niet te draaien. Probeer te starten...
    start "" ollama serve
    timeout /t 5 /nobreak >nul
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if errorlevel 1 (
        echo  FOUT: Ollama start niet. Start handmatig "ollama serve"
        echo  Download Ollama: https://ollama.com
        pause
        exit /b 1
    )
)

REM --- Check model ---
echo  Controleren of model qwen2.5:14b aanwezig is...
ollama list | findstr /i "qwen2.5:14b" >nul
if errorlevel 1 (
    echo  Model niet gevonden. Downloaden...
    ollama pull qwen2.5:14b
)

REM --- Install requirements if needed ---
if not exist "requirements.txt" (
    echo  requirements.txt niet gevonden.
    pause
    exit /b 1
)
echo  Controleren dependencies...
pip install -q -r requirements.txt

REM --- Start app ---
echo.
echo  ========================================
echo   BushiDAI start...
echo   Browser opent op http://localhost:8501
echo  ========================================
echo.
streamlit run app.py

pause