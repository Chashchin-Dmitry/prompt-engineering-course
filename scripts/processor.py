#!/usr/bin/env python3
"""
Processor — Слой 2: очистка, структурирование, чанкинг, дедупликация.
Читает content/raw/*.md → пишет content/processed/*.json + content/chunks/*.json
"""

import os
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

REPO_PATH      = Path(os.getenv("REPO_PATH", Path(__file__).parent.parent))
RAW_DIR        = REPO_PATH / "content" / "raw"
PROCESSED_DIR  = REPO_PATH / "content" / "processed"
CHUNKS_DIR     = REPO_PATH / "content" / "chunks"
INDEX_FILE     = REPO_PATH / "content" / "index.json"

CHUNK_SIZE     = 500    # токенов (~2000 символов)
CHUNK_OVERLAP  = 50     # overlap между чанками

# Маппинг тегов → модули курса
TAG_MODULE_MAP = {
    "foundation": "01-foundations",
    "basic": "01-foundations",
    "introduction": "01-foundations",
    "chain-of-thought": "02-core-techniques",
    "few-shot": "02-core-techniques",
    "zero-shot": "02-core-techniques",
    "role-prompting": "02-core-techniques",
    "system-prompt": "02-core-techniques",
    "RAG": "03-advanced",
    "agent": "03-advanced",
    "multi-agent": "03-advanced",
    "fine-tuning": "03-advanced",
    "embedding": "03-advanced",
    "ChatGPT": "04-tools",
    "Claude": "04-tools",
    "Gemini": "04-tools",
    "Cursor": "04-tools",
    "LangChain": "04-tools",
    "Copilot": "04-tools",
    "developer": "05-use-cases",
    "marketing": "05-use-cases",
    "product": "05-use-cases",
    "best-practice": "06-best-practices",
    "checklist": "06-best-practices",
    "template": "06-best-practices",
}


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def content_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def parse_raw_md(path: Path) -> dict:
    """Парсим raw markdown → структурированный dict."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    meta = {}
    content_lines = []
    in_content = False

    for line in lines:
        if line.startswith("# ") and "title" not in meta:
            meta["title"] = line[2:].strip()
        elif line.startswith("**Source:**"):
            meta["url"] = re.search(r'https?://\S+', line)
            meta["url"] = meta["url"].group() if meta["url"] else ""
            meta["url"] = meta["url"].rstrip(")")
        elif line.startswith("**Author:**"):
            meta["author"] = line.replace("**Author:**", "").strip()
        elif line.startswith("**Published:**"):
            meta["published"] = line.replace("**Published:**", "").strip()
        elif line.startswith("**Scraped:**"):
            meta["scraped"] = line.replace("**Scraped:**", "").strip()
        elif line == "---" and not in_content:
            in_content = True
        elif in_content and not line.startswith("*Auto-collected"):
            content_lines.append(line)

    content = "\n".join(content_lines).strip()
    return {**meta, "content": content, "source_file": path.name}


def clean_text(text: str) -> str:
    """Базовая очистка текста."""
    # Убираем лишние пробелы и пустые строки
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    # Убираем типичный Medium-мусор
    text = re.sub(r'Sign up\s+Sign in.*?$', '', text, flags=re.MULTILINE)
    text = re.sub(r'Follow\s+\d+ Followers.*?$', '', text, flags=re.MULTILINE)
    return text.strip()


def extract_tags(text: str, title: str) -> list:
    """Автоматические теги по содержанию."""
    combined = (title + " " + text[:3000]).lower()
    tags = []

    keyword_tags = {
        "prompt engineering": "prompt-engineering",
        "chain of thought": "chain-of-thought",
        "few-shot": "few-shot",
        "zero-shot": "zero-shot",
        "system prompt": "system-prompt",
        "role prompt": "role-prompting",
        "rag": "RAG",
        "retrieval": "RAG",
        "agent": "agent",
        "langchain": "LangChain",
        "chatgpt": "ChatGPT",
        "claude": "Claude",
        "gemini": "Gemini",
        "cursor": "Cursor",
        "copilot": "Copilot",
        "fine-tun": "fine-tuning",
        "embedding": "embedding",
        "developer": "developer",
        "best practice": "best-practice",
        "template": "template",
        "checklist": "checklist",
    }

    for keyword, tag in keyword_tags.items():
        if keyword in combined and tag not in tags:
            tags.append(tag)

    return tags or ["prompt-engineering"]


def assign_module(tags: list) -> str:
    """Определяем модуль курса по тегам."""
    for tag in tags:
        if tag in TAG_MODULE_MAP:
            return TAG_MODULE_MAP[tag]
    return "01-foundations"


def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> list:
    """Разбиваем текст на чанки для RAG."""
    # Простая разбивка по словам
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i + chunk_size]
        chunks.append(" ".join(chunk_words))
        i += chunk_size - overlap
    return chunks


def load_index() -> dict:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {"total_articles": 0, "total_chunks": 0, "last_updated": "", "article_ids": []}


def save_index(index: dict):
    index["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2))


def process():
    log("=" * 60)
    log("🔧 Запуск процессора")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    index = load_index()
    raw_files = sorted(RAW_DIR.glob("*.md"))
    log(f"📂 Найдено raw файлов: {len(raw_files)}")

    new_articles = 0
    new_chunks = 0

    for raw_path in raw_files:
        try:
            # Парсим raw
            data = parse_raw_md(raw_path)
            content = clean_text(data.get("content", ""))

            if len(content) < 300:
                log(f"⏭️  Пропуск (мало текста): {raw_path.name}")
                continue

            # Дедупликация по hash
            art_id = content_hash(content)
            if art_id in index.get("article_ids", []):
                continue

            # Теги и модуль
            tags = extract_tags(content, data.get("title", ""))
            module = assign_module(tags)

            # Сохраняем processed JSON
            processed = {
                "id": art_id,
                "title": data.get("title", ""),
                "source": "medium",
                "url": data.get("url", ""),
                "author": data.get("author", ""),
                "published": data.get("published", ""),
                "scraped": data.get("scraped", ""),
                "tags": tags,
                "module": module,
                "word_count": len(content.split()),
                "content": content,
            }

            proc_path = PROCESSED_DIR / f"{art_id}.json"
            proc_path.write_text(json.dumps(processed, ensure_ascii=False, indent=2))

            # Чанкинг
            chunks = chunk_text(content)
            chunks_data = []
            for i, chunk in enumerate(chunks):
                chunk_obj = {
                    "article_id": art_id,
                    "article_title": data.get("title", ""),
                    "article_url": data.get("url", ""),
                    "module": module,
                    "tags": tags,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "text": chunk,
                }
                chunks_data.append(chunk_obj)

            chunks_path = CHUNKS_DIR / f"{art_id}.json"
            chunks_path.write_text(json.dumps(chunks_data, ensure_ascii=False, indent=2))

            # Обновляем индекс
            index.setdefault("article_ids", []).append(art_id)
            new_articles += 1
            new_chunks += len(chunks)
            log(f"✅ [{new_articles}] '{data['title'][:50]}' → {module} ({len(chunks)} чанков)")

        except Exception as e:
            log(f"❌ {raw_path.name}: {e}")

    index["total_articles"] = len(index.get("article_ids", []))
    index["total_chunks"] = index.get("total_chunks", 0) + new_chunks
    save_index(index)

    log(f"\n✅ Готово: +{new_articles} статей, +{new_chunks} чанков")
    log(f"📊 Всего: {index['total_articles']} статей, {index['total_chunks']} чанков")


if __name__ == "__main__":
    process()
