@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\iniciar_local.ps1" -Modo local %*
if errorlevel 1 pause
