@echo off
echo.
echo ====================================
echo   Chimera AI - Quota Checker
echo ====================================
echo.

cd /d "%~dp0"
python check_quota.py

echo.
pause
