@echo off
cd /d "%~dp0"
start "도전 四字成語 서버 (이 창을 닫으면 종료됩니다)" powershell -ExecutionPolicy Bypass -NoProfile -File ".claude\serve.ps1"
timeout /t 2 >nul
start "" http://localhost:8765/
