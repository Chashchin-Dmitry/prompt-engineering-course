#!/usr/bin/env python3
"""
Embedder — Слой 3: генерация эмбеддингов → ChromaDB.
Читает content/chunks/*.json → пишет в embeddings/ (ChromaDB).

Поддерживает два режима:
  - OpenAI (text-embedding-3-small) — лучше качество, нужен API ключ
  - Ollama (nomic-embed-text) — локально, бесплатно, чуть хуже
"""

import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

REPO_PATH      = Path(os.getenv("REPO_PATH", Path(__file__).parent.parent))
CHUNKS_DIR     = REPO_PATH / "content" / "chunks"
EMBEDDINGS_DIR = REPO_PATH / "embeddings"

EMBED_MODE     = os.getenv("EMBED_MODE", "openai")  # "openai" или "ollama"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
COLLECTION_NAME = "prompt-engineering-course"


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def get_chroma_client():
    import chromadb
    return chromadb.PersistentClient(path=str(EMBEDDINGS_DIR))


def get_collection(client):
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def embed_openai(texts: list) -> list:
    """Эмбеддинги через OpenAI API."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]


def embed_ollama(texts: list) -> list:
    """Эмбеддинги через Ollama (локально)."""
    import requests
    embeddings = []
    for text in texts:
        resp = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text}
        )
        embeddings.append(resp.json()["embedding"])
    return embeddings


def embed_texts(texts: list) -> list:
    if EMBED_MODE == "ollama":
        log(f"  🦙 Ollama embeddings ({len(texts)} текстов)")
        return embed_ollama(texts)
    else:
        log(f"  🤖 OpenAI embeddings ({len(texts)} текстов)")
        return embed_openai(texts)


def embed():
    log("=" * 60)
    log(f"🔢 Запуск эмбеддера (режим: {EMBED_MODE})")

    if EMBED_MODE == "openai" and not OPENAI_API_KEY:
        log("❌ OPENAI_API_KEY не задан в .env")
        log("   Альтернатива: установи Ollama и поставь EMBED_MODE=ollama")
        return

    EMBEDDINGS_DIR.mkdir(exist_ok=True)
    client = get_chroma_client()
    collection = get_collection(client)

    # Уже проиндексированные chunk id
    existing = set(collection.get()["ids"])
    log(f"📚 Уже в базе: {len(existing)} чанков")

    chunk_files = list(CHUNKS_DIR.glob("*.json"))
    log(f"📂 Файлов чанков: {len(chunk_files)}")

    new_total = 0
    BATCH = 50  # Пакетная обработка

    all_chunks = []
    for chunk_file in chunk_files:
        chunks = json.loads(chunk_file.read_text())
        for chunk in chunks:
            chunk_id = f"{chunk['article_id']}__{chunk['chunk_index']}"
            if chunk_id not in existing:
                all_chunks.append((chunk_id, chunk))

    log(f"🆕 Новых чанков для индексации: {len(all_chunks)}")

    for i in range(0, len(all_chunks), BATCH):
        batch = all_chunks[i:i + BATCH]
        ids = [c[0] for c in batch]
        texts = [c[1]["text"] for c in batch]
        metadatas = [{
            "article_id": c[1]["article_id"],
            "article_title": c[1]["article_title"],
            "article_url": c[1]["article_url"],
            "module": c[1]["module"],
            "tags": ", ".join(c[1]["tags"]),
            "chunk_index": c[1]["chunk_index"],
        } for c in batch]

        try:
            embeddings = embed_texts(texts)
            collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
            new_total += len(batch)
            log(f"  ✅ Пакет {i // BATCH + 1}: +{len(batch)} чанков")
        except Exception as e:
            log(f"  ❌ Ошибка пакета {i // BATCH + 1}: {e}")

    log(f"\n✅ Готово: +{new_total} чанков добавлено в ChromaDB")
    log(f"📊 Всего в базе: {collection.count()} чанков")


if __name__ == "__main__":
    embed()
