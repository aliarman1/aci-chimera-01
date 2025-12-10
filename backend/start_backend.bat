@echo off
echo Starting Chimera Backend Server...
echo.
echo Make sure you have set your GEMINI_API_KEY in the .env file!
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo.
echo Backend server starting on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python -m uvicorn app.main:app --reload --port 8000
