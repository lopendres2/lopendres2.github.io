@echo off
rem Запуск Telegram-бота магазина lopendres2
cd /d "%~dp0"
if not exist .env (
    echo Файл .env не найден. Скопируйте .env.example в .env и впишите BOT_TOKEN.
    pause
    exit /b 1
)
python -m pip install -r requirements.txt >nul 2>&1
python bot.py
pause
