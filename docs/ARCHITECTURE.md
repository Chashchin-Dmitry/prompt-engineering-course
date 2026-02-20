# 🏗️ Архитектура системы | System Architecture

## Философия: "Коробка передач"

> Система строится как универсальный конвейер: собираем сырьё → обрабатываем → храним структурированно → делаем умным через RAG → выдаём на выходе курс, бот, документацию.
> Каждый слой независим и заменяем. Можно менять источник (не только Medium), хранилище (не только файлы), модель (не только OpenAI).

---

## 🗺️ Общая схема

```
┌─────────────────────────────────────────────────────────────────┐
│                        ИСТОЧНИКИ ДАННЫХ                         │
│   Medium  │  YouTube  │  Twitter/X  │  Docs  │  Papers (arxiv) │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                     СЛОЙ 1: СБОР (Scraper)                      │
│  • Playwright + stealth (имитация человека)                     │
│  • Рекурсивное расширение ключевых слов                         │
│  • Cron: каждую ночь в 3:00                                     │
│  → Выход: content/raw/*.md + content/screenshots/*.png          │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   СЛОЙ 2: ОБРАБОТКА (Processor)                 │
│  • Очистка текста (убираем мусор, nav, ads)                     │
│  • Структурирование в JSON с метаданными                        │
│  • Чанкинг (разбивка на куски для RAG ~500 токенов)             │
│  • Теггинг (автоматические теги по содержанию)                  │
│  • Дедупликация (не сохраняем одно и то же дважды)              │
│  → Выход: content/processed/*.json + content/chunks/*.json      │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                  СЛОЙ 3: ХРАНИЛИЩЕ (Store)                      │
│                                                                 │
│  content/raw/          ← сырой markdown                         │
│  content/processed/    ← структурированный JSON                 │
│  content/chunks/       ← чанки для RAG                         │
│  content/screenshots/  ← скриншоты статей                       │
│  content/index.json    ← мастер-индекс всего контента           │
│  embeddings/           ← векторные эмбеддинги (ChromaDB)        │
│                                                                 │
│  GitHub ← версионирование всего кроме embeddings               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                СЛОЙ 4: ИНТЕЛЛЕКТ (RAG Engine)                   │
│                                                                 │
│  embedder.py → ChromaDB (локальная векторная БД)               │
│       │                                                         │
│       ▼                                                         │
│  rag_bot.py  ←→  Claude / GPT-4 / Ollama (local)              │
│                                                                 │
│  Умеет:                                                         │
│  • Отвечать на вопросы по собранному контенту                   │
│  • Находить лучшие статьи по теме                               │
│  • Генерировать разделы курса из контента                       │
│  • Сравнивать техники промтинга                                 │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   СЛОЙ 5: ВЫХОД (Output)                        │
│                                                                 │
│  modules/         ← структурированный курс (markdown)           │
│  bot/             ← RAG-бот (CLI / Telegram / Web)             │
│  exports/         ← PDF, GitBook, Notion                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Структура проекта

```
prompt-engineering-course/
│
├── CLAUDE.md                    # Инструкции для AI агентов
├── README.md                    # Обзор проекта
│
├── docs/
│   ├── ARCHITECTURE.md          # Этот файл
│   ├── PLAN.md                  # Рабочий план
│   └── ADR/                     # Architecture Decision Records
│       └── 001-storage.md
│
├── scripts/                     # Весь автоматизированный конвейер
│   ├── scraper.py               # Слой 1: сбор с Medium
│   ├── processor.py             # Слой 2: очистка + чанкинг
│   ├── embedder.py              # Слой 3: эмбеддинги → ChromaDB
│   ├── pipeline.py              # Запуск всего конвейера разом
│   ├── keywords.json            # База ключевых слов (растёт сама)
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                     # (не в git!)
│
├── content/
│   ├── raw/                     # Сырой markdown с Medium
│   ├── processed/               # Структурированный JSON
│   ├── chunks/                  # Чанки для RAG
│   ├── screenshots/             # Скриншоты статей
│   └── index.json               # Мастер-индекс
│
├── embeddings/                  # ChromaDB (не в git — большой)
│
├── bot/
│   ├── rag_bot.py               # RAG чат-бот
│   ├── prompts/
│   │   ├── system.md            # Системный промт бота
│   │   └── templates/           # Промты для генерации контента
│   └── README.md
│
├── modules/                     # Финальный курс
│   ├── 01-foundations/
│   ├── 02-core-techniques/
│   ├── 03-advanced/
│   ├── 04-tools/
│   ├── 05-use-cases/
│   └── 06-best-practices/
│
├── logs/                        # Логи (не в git)
│   └── scraper.log
│
└── .venv/                       # Python окружение (не в git)
```

---

## 🔄 Конвейер данных (Pipeline)

### Шаг 1 — Scraper (ежедневно, 3:00)
```
keywords.json → Medium Search → Article Pages
    → content/raw/YYYY-MM-DD_title.md
    → content/screenshots/YYYY-MM-DD_title.png
    → keywords.json (обновлён новыми терминами)
```

### Шаг 2 — Processor (после scraper)
```
content/raw/*.md
    → очистка текста
    → извлечение метаданных (автор, дата, теги, источник)
    → дедупликация (hash контента)
    → чанкинг (~500 токенов с overlap 50)
    → content/processed/*.json
    → content/chunks/*.json
    → content/index.json (обновлён)
```

### Шаг 3 — Embedder (после processor)
```
content/chunks/*.json
    → text-embedding-3-small (OpenAI) или nomic-embed (local)
    → ChromaDB (embeddings/)
    → готово к RAG-запросам
```

### Шаг 4 — RAG Bot (по запросу)
```
Вопрос пользователя
    → embed вопрос
    → найти топ-5 релевантных чанков в ChromaDB
    → собрать контекст
    → Claude/GPT: "Вот контекст из статей, ответь на вопрос"
    → ответ со ссылками на источники
```

---

## 🧩 Компоненты и зависимости

| Компонент | Технология | Зачем |
|-----------|-----------|-------|
| Scraper | Playwright + stealth | Человекоподобный парсинг Medium |
| Processor | Python + regex | Очистка, чанкинг, дедупликация |
| Embedder | OpenAI API / Ollama | Векторизация текста |
| Vector DB | ChromaDB (локально) | Хранение и поиск по эмбеддингам |
| RAG Bot | Claude API / GPT-4 | Умные ответы по контенту |
| Scheduler | cron (macOS) | Автозапуск ночью |
| Storage | GitHub | Версионирование контента |
| Monitoring | HEARTBEAT.md + logs | Я слежу, пишу если что-то сломалось |

---

## 🔌 Расширяемость

Система спроектирована как "коробка передач" — подключай любые компоненты:

```
Источники:     Medium → + YouTube → + arxiv → + Twitter → + Docs
Эмбеддинги:   OpenAI → или Ollama (локально, бесплатно)
LLM для RAG:  Claude → или GPT-4 → или Llama3 (локально)
Интерфейс:    CLI → или Telegram бот → или веб-интерфейс
Экспорт:      Markdown → или PDF → или GitBook → или Notion
```

---

## 📊 Форматы данных

### content/raw/*.md
```markdown
# Заголовок статьи
**Source:** URL
**Author:** Имя
**Published:** 2024-01-15
**Scraped:** 2026-02-20
---
Текст статьи...
```

### content/processed/*.json
```json
{
  "id": "sha256-hash",
  "title": "...",
  "source": "medium",
  "url": "...",
  "author": "...",
  "published": "2024-01-15",
  "scraped": "2026-02-20",
  "tags": ["prompt-engineering", "chain-of-thought"],
  "module": "02-core-techniques",
  "word_count": 1500,
  "content": "..."
}
```

### content/chunks/*.json
```json
{
  "article_id": "sha256-hash",
  "chunk_index": 0,
  "total_chunks": 8,
  "text": "...",
  "tokens": 487
}
```

### content/index.json
```json
{
  "total_articles": 142,
  "total_chunks": 1847,
  "last_updated": "2026-02-20",
  "articles": [...]
}
```

---

## 🚀 Порядок запуска

```bash
# 1. Первичная настройка (один раз)
cd scripts && ./setup.sh

# 2. Полный конвейер вручную
python pipeline.py

# 3. Только скрапинг
python scraper.py

# 4. Только обработка
python processor.py

# 5. Только эмбеддинги
python embedder.py

# 6. RAG бот
python bot/rag_bot.py

# 7. Автоматически (cron 3:00 ночи)
python pipeline.py  ← запускается сам
```

---

## 🛡️ Безопасность

- `.env` никогда не в git (API ключи, пути)
- Chrome профиль копируется во временную папку, удаляется после
- `embeddings/` в `.gitignore` (может быть большим)
- `logs/` в `.gitignore`
