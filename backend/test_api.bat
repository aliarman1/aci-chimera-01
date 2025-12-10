@echo off
echo.
echo ================================
echo  Testing Gemini API Models
echo ================================
echo.
cd /d "%~dp0"
call venv\Scripts\activate.bat
python test_models.py
echo.
pause
