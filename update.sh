#!/bin/bash
git reset --hard HEAD
git pull
pkill -f main.py
source venv/bin/activate
nohup python3 main.py &
echo "Бот оновлений та запущений!"