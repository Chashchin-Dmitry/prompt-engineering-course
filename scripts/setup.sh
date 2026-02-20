#!/bin/bash
# Setup script — запусти один раз после клонирования репо

set -e

echo "🚀 Настройка Prompt Engineering Course Scraper"
echo "================================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python venv
echo "🐍 Создаю Python окружение..."
python3 -m venv "$SCRIPT_DIR/../.venv"
source "$SCRIPT_DIR/../.venv/bin/activate"

# Dependencies
echo "📦 Устанавливаю зависимости..."
pip install -q -r "$SCRIPT_DIR/requirements.txt"

# Playwright browsers
echo "🌐 Устанавливаю Playwright (Chrome)..."
playwright install chromium

# .env
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
    echo "⚙️  Создан .env файл — можешь отредактировать при необходимости"
fi

# Cron job (каждую ночь в 3:00)
CRON_CMD="0 3 * * * cd $SCRIPT_DIR && ../.venv/bin/python scraper.py >> ../logs/scraper.log 2>&1"
mkdir -p "$SCRIPT_DIR/../logs"

# Проверяем что такой cron ещё не добавлен
if ! crontab -l 2>/dev/null | grep -q "scraper.py"; then
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "⏰ Cron настроен: каждую ночь в 3:00"
else
    echo "⏰ Cron уже настроен"
fi

echo ""
echo "✅ Всё готово!"
echo ""
echo "Команды:"
echo "  Запустить вручную:  cd scripts && ../.venv/bin/python scraper.py"
echo "  Посмотреть логи:    tail -f logs/scraper.log"
echo "  Cron расписание:    crontab -l"
echo ""
