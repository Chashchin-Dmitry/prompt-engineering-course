# Scripts / Скрипты

## Быстрый старт / Quick Start

```bash
chmod +x setup.sh
./setup.sh
```

## Файлы / Files

| Файл | Описание |
|------|----------|
| `scraper.py` | Главный скрипт парсинга Medium |
| `setup.sh` | Установка + настройка cron |
| `requirements.txt` | Python зависимости |
| `.env.example` | Пример конфига |
| `.env` | Твой конфиг (не в git!) |

## Запуск вручную / Manual Run

```bash
cd scripts
../.venv/bin/python scraper.py
```

## Логи / Logs

```bash
tail -f ../logs/scraper.log
```

## Как работает / How it works

1. Копирует твой Chrome профиль во временную папку
2. Запускает Chrome через Playwright (с антидетект настройками)
3. Ищет статьи на Medium по заданным запросам
4. Скроллит и читает как человек (случайные паузы 2-5 сек)
5. Сохраняет markdown + скриншот в `content/`
6. Пушит в GitHub
7. Удаляет временный профиль

## Настройка запросов / Configuring Queries

Редактируй `MEDIUM_QUERIES` в `.env`:

```env
MEDIUM_QUERIES=prompt engineering 2024,Claude AI tips,LLM best practices,AI agent development
```
