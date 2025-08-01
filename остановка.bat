@echo off
taskkill /f /im uvicorn.exe /im node.exe
echo Проект остановлен.
pause
@REM не тестировал