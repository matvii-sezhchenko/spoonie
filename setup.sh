#!/bin/bash

# Зупиняти скрипт, якщо якась команда завершиться помилкою
set -e

echo "=== 1. Оновлення системних пакетів та встановлення python3-venv ==="
sudo apt update
sudo apt install -y python3-venv python3-pip

echo "=== 2. Створення віртуального оточення ==="
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Віртуальне оточення створено."
else
    echo "Оточення venv вже існує."
fi

echo "=== 3. Оновлення менеджера пакетів pip ==="
./venv/bin/pip install --upgrade pip

echo "=== 4. Встановлення залежностей з requirements.txt ==="
if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install -r requirements.txt
    echo "Всі залежності успішно встановлені."
else
    exit 1
fi

echo "=== Ініціалізацію завершено успішно! ==="
echo "Для запуску бота виконай: source venv/bin/activate && python3 bot.py"