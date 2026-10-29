@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\iniciar_local.ps1" -Modo apresentacao %*
if errorlevel 1 pause
