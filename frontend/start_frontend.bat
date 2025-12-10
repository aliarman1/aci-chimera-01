@echo off
echo Starting Chimera Frontend...
echo.
echo Frontend will be available at http://localhost:3000
echo Make sure the backend is running on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
npm run dev
