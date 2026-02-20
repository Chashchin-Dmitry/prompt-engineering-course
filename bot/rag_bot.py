#!/usr/bin/env python3
"""
RAG Bot — умный ассистент по промт-инжинирингу.
Отвечает на вопросы опираясь на собранные статьи из Medium.

Использование:
  python bot/rag_bot.py                    # интерактивный CLI
  python bot/rag_bot.py "что такое RAG?"   # одиночный вопрос
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "scripts" / ".env")

REPO_PATH       = Path(os.getenv("REPO_PATH", Path(__file__).parent.parent))
EMBEDDINGS_DIR  = REPO_PATH / "embeddings"
SYSTEM_PROMPT   = Path(__file__).parent / "prompts" / "system.md"

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_KEY   = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODE        = os.getenv("LLM_MODE", "claude")   # "claude" | "openai" | "ollama"
EMBED_MODE      = os.getenv("EMBED_MODE", "openai")  # "openai" | "ollama"
COLLECTION_NAME = "prompt-engineering-course"
TOP_K           = 5  # сколько чанков брать для контекста


def load_system_prompt() -> str:
    if SYSTEM_PROMPT.exists():
        return SYSTEM_PROMPT.read_text()
    return """Ты эксперт по промт-инжинирингу и AI-инструментам.
Отвечай на вопросы опираясь ТОЛЬКО на предоставленный контекст из статей.
Всегда указывай источник (название статьи и URL).
Если информации нет в контексте — честно скажи об этом.
Отвечай на языке вопроса (русский или английский)."""


def get_collection():
    import chromadb
    client = chromadb.PersistentClient(path=str(EMBEDDINGS_DIR))
    return client.get_collection(COLLECTION_NAME)


def embed_query(text: str) -> list:
    if EMBED_MODE == "ollama":
        import requests
        resp = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": text}
        )
        return resp.json()["embedding"]
    else:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.embeddings.create(model="text-embedding-3-small", input=[text])
        return resp.data[0].embedding


def search(query: str, top_k=TOP_K) -> list:
    """Ищем релевантные чанки в ChromaDB."""
    collection = get_collection()
    query_embedding = embed_query(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        score = 1 - results["distances"][0][i]  # cosine similarity
        chunks.append({
            "text": doc,
            "title": meta.get("article_title", ""),
            "url": meta.get("article_url", ""),
            "module": meta.get("module", ""),
            "score": round(score, 3),
        })
    return chunks


def build_context(chunks: list) -> str:
    """Собираем контекст из найденных чанков."""
    parts = []
    seen_urls = set()
    for i, chunk in enumerate(chunks):
        url = chunk["url"]
        source_label = f"[{chunk['title']}]({url})" if url not in seen_urls else chunk["title"]
        seen_urls.add(url)
        parts.append(f"--- Источник {i+1}: {source_label} (релевантность: {chunk['score']}) ---\n{chunk['text']}")
    return "\n\n".join(parts)


def ask_claude(question: str, context: str, system: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        system=system,
        messages=[{
            "role": "user",
            "content": f"Контекст из статей:\n\n{context}\n\n---\n\nВопрос: {question}"
        }]
    )
    return response.content[0].text


def ask_openai(question: str, context: str, system: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Контекст:\n\n{context}\n\n---\n\nВопрос: {question}"}
        ]
    )
    return response.choices[0].message.content


def ask_ollama(question: str, context: str, system: str) -> str:
    import requests
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "system": system,
            "prompt": f"Контекст:\n\n{context}\n\n---\n\nВопрос: {question}",
            "stream": False
        }
    )
    return resp.json()["response"]


def answer(question: str) -> str:
    """Главная функция: вопрос → ответ через RAG."""
    print(f"\n🔍 Ищу релевантные статьи...")
    chunks = search(question)

    if not chunks:
        return "❌ В базе пока нет материалов по этой теме. Дождись следующего цикла сбора."

    print(f"📚 Найдено {len(chunks)} релевантных фрагментов:")
    for c in chunks:
        print(f"   • [{c['score']}] {c['title'][:60]}")

    context = build_context(chunks)
    system = load_system_prompt()

    print(f"\n🤖 Генерирую ответ ({LLM_MODE})...")
    if LLM_MODE == "claude":
        return ask_claude(question, context, system)
    elif LLM_MODE == "openai":
        return ask_openai(question, context, system)
    else:
        return ask_ollama(question, context, system)


def cli():
    """Интерактивный режим."""
    print("🧠 RAG-бот по Промт-Инжинирингу")
    print("   Задавай вопросы на русском или английском.")
    print("   Введи 'exit' для выхода.\n")

    while True:
        try:
            question = input("❓ Вопрос: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Пока!")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "выход"):
            print("👋 Пока!")
            break

        result = answer(question)
        print(f"\n💬 Ответ:\n{result}\n")
        print("─" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        print(answer(q))
    else:
        cli()
