@echo off
title Запуск ActWork (Backend + Frontend)

:: Запуск бэкенда в фоне (без окна)
start /B "Backend" uvicorn server:app --reload --port 8001 > backend.log 2>&1

:: Запуск фронтенда в фоне (без окна)
start /B "Frontend" npm start --prefix frontend > frontend.log 2>&1

echo Проект запущен! Проверьте логи в backend.log и frontend.log.
echo Чтобы остановить: taskkill /f /im uvicorn.exe /im node.exe
pause
:: открывается консоль - неудобно, если закрыть проект выключается.