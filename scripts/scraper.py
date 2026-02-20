#!/usr/bin/env python3
"""
Medium Scraper — Prompt Engineering Course
Использует curl-cffi (обход Cloudflare) + pycookiecheat (куки из Chrome).
Никакого браузера — быстро, стабильно, без детекции.
"""

import os
import re
import json
import time
import random
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── Пути ──────────────────────────────────────────────────────────────────────
REPO_PATH    = Path(os.getenv("REPO_PATH", Path(__file__).parent.parent))
CONTENT_RAW  = REPO_PATH / "content" / "raw"
LOGS_DIR     = REPO_PATH / "logs"
KEYWORDS_FILE = Path(__file__).parent / "keywords.json"

# ── Настройки ─────────────────────────────────────────────────────────────────
MAX_ARTICLES    = int(os.getenv("MAX_ARTICLES_PER_RUN", 15))
QUERIES_PER_RUN = int(os.getenv("QUERIES_PER_RUN", 5))
MIN_DELAY       = float(os.getenv("MIN_DELAY", 1.5))
MAX_DELAY       = float(os.getenv("MAX_DELAY", 4))
AUTO_GIT_PUSH   = os.getenv("AUTO_GIT_PUSH", "true").lower() == "true"

# AI-термины для расширения базы ключевых слов
AI_TERMS_PATTERN = re.compile(
    r'\b(prompt\s+\w+|RAG|LLM|GPT-?\d*|Claude\s*\w*|Gemini\s*\w*|Llama\s*\d*|'
    r'chain.of.thought|few.shot|zero.shot|fine.tun\w+|embedding\w*|vector\s+\w+|'
    r'LangChain|LlamaIndex|CrewAI|AutoGPT|Cursor\s*AI|Copilot|Perplexity|'
    r'ReAct|tree.of.thoughts|self.consistency|function.calling|'
    r'Mistral|Codex|Grok|Qwen|GLM|Falcon|Mixtral|Gemma|'
    r'agent\s+\w+|agentic\s+\w+|multi.agent|autonomous\s+AI|'
    r'context.window|temperature\s+\w+|system.prompt|prompt.injection|'
    r'hallucination\s+\w+|grounding|guardrail\w*)\b',
    re.IGNORECASE
)


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOGS_DIR.mkdir(exist_ok=True)
    with open(LOGS_DIR / "scraper.log", "a") as f:
        f.write(line + "\n")


def human_delay():
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))


# ── Keywords DB ───────────────────────────────────────────────────────────────

def load_keywords():
    if KEYWORDS_FILE.exists():
        return json.loads(KEYWORDS_FILE.read_text())
    return {"queue": [], "done": [], "discovered": [], "last_updated": ""}


def save_keywords(db):
    db["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    KEYWORDS_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2))


def pick_queries(db, n=QUERIES_PER_RUN):
    available = [q for q in db["queue"] if q not in db["done"]]
    picks = available[:n]
    if len(picks) < n:
        db["done"] = []
        picks = db["queue"][:n]
    return picks


def add_discovered_keywords(db, text):
    found = set(AI_TERMS_PATTERN.findall(text))
    added = 0
    for term in found:
        t = term.strip().lower()
        if t not in db["queue"] and t not in db.get("discovered", []):
            db["queue"].append(t)
            db.setdefault("discovered", []).append(t)
            added += 1
    return added


# ── HTTP Session ──────────────────────────────────────────────────────────────

def make_session():
    """Создаём сессию с куками из Chrome и Chrome TLS-отпечатком."""
    from curl_cffi import requests as cf_requests
    from pycookiecheat import chrome_cookies

    cookies = chrome_cookies('https://medium.com')
    session = cf_requests.Session(impersonate='chrome131')
    session.cookies.update(cookies)
    session.headers.update({
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://medium.com',
    })
    log(f"🍪 Куков загружено: {len(cookies)}")
    return session


# ── RSS Feed → Article Links ──────────────────────────────────────────────────

def get_article_links_rss(session, query, max_links=5):
    """Получаем ссылки на статьи через RSS — не требует JS-рендеринга."""
    from bs4 import BeautifulSoup

    # Конвертируем query в тег Medium
    tag = query.strip().lower().replace(' ', '-')
    url = f"https://medium.com/feed/tag/{tag}"
    log(f"🔍 RSS: '{query}' → {url}")

    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            log(f"⚠️ RSS вернул {r.status_code} для '{query}'")
            return []

        soup = BeautifulSoup(r.text, 'xml')
        items = soup.find_all('item')

        links = []
        for item in items[:max_links * 2]:
            link_el = item.find('link')
            guid_el = item.find('guid')
            url_art = (link_el.text if link_el else None) or (guid_el.text if guid_el else None)
            if url_art and 'medium.com' in url_art:
                links.append(url_art.split('?')[0])

        return links[:max_links]
    except Exception as e:
        log(f"⚠️ RSS ошибка '{query}': {e}")
        return []


# ── Article Fetcher ───────────────────────────────────────────────────────────

def fetch_article(session, url):
    """Скачиваем и парсим статью. Работает с member-only."""
    from bs4 import BeautifulSoup

    try:
        r = session.get(url, timeout=20)
        if r.status_code != 200:
            log(f"⚠️ HTTP {r.status_code}: {url[:60]}")
            return None

        soup = BeautifulSoup(r.text, 'lxml')
        article_el = soup.find('article')
        if not article_el:
            return None

        # Убираем лишнее
        for tag in article_el.find_all(['button', 'nav', 'script', 'style', 'svg']):
            tag.decompose()

        content = article_el.get_text(separator='\n', strip=True)
        if len(content) < 300:
            return None

        title = soup.title.text.replace(' | Medium', '').strip() if soup.title else 'Unknown'
        title = re.sub(r' \| by .+$', '', title).strip()

        author_el = soup.find('a', attrs={'data-testid': 'authorName'}) or \
                    soup.find('a', rel='author')
        author = author_el.get_text(strip=True) if author_el else 'Unknown'

        time_el = soup.find('time')
        published = time_el['datetime'] if time_el and time_el.get('datetime') else None

        return {
            'title': title,
            'content': content,
            'author': author,
            'published': published,
            'url': url,
        }
    except Exception as e:
        log(f"⚠️ Ошибка парсинга {url[:60]}: {e}")
        return None


# ── Save ──────────────────────────────────────────────────────────────────────

def save_article(article):
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe = re.sub(r'[^\w\s-]', '', article["title"])[:60].strip().replace(' ', '-')
    fname = f"{date_str}_{safe}"

    md = f"""# {article['title']}

**Source:** {article['url']}
**Author:** {article['author']}
**Published:** {article.get('published', 'unknown')}
**Scraped:** {date_str}

---

{article['content']}

---
*Auto-collected for Prompt Engineering Course*
"""
    CONTENT_RAW.mkdir(parents=True, exist_ok=True)
    (CONTENT_RAW / f"{fname}.md").write_text(md, encoding="utf-8")
    log(f"💾 Сохранено: {fname[:50]}")
    return fname


# ── Git Push ──────────────────────────────────────────────────────────────────

def git_push(count, new_kw):
    log("\n📤 Пушу в GitHub...")
    try:
        os.chdir(REPO_PATH)
        subprocess.run(["git", "add", "content/", "scripts/keywords.json"], check=True)
        msg = (f"feat: scrape {count} articles, +{new_kw} new keywords "
               f"[{datetime.now().strftime('%Y-%m-%d')}]")
        result = subprocess.run(["git", "commit", "-m", msg], capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(["git", "push"], check=True)
            log("✅ Запушено!")
        else:
            log("ℹ️ Нечего коммитить")
    except Exception as e:
        log(f"⚠️ Git push: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────

def scrape():
    log("=" * 60)
    log("🚀 Запуск скрапера (curl-cffi + pycookiecheat)")

    db = load_keywords()
    queries = pick_queries(db, QUERIES_PER_RUN)
    log(f"📋 Запросы: {', '.join(queries)}")
    log(f"📦 Лимит: {MAX_ARTICLES} статей | Ключей в базе: {len(db['queue'])}")

    session = make_session()

    scraped_count = 0
    scraped_urls = set()
    new_keywords_total = 0

    for query in queries:
        if scraped_count >= MAX_ARTICLES:
            break

        db["done"].append(query)
        links = get_article_links_rss(session, query, max_links=4)
        log(f"  → {len(links)} статей найдено")

        for url in links:
            if scraped_count >= MAX_ARTICLES:
                break
            if url in scraped_urls:
                continue
            scraped_urls.add(url)

            log(f"\n📖 {url[:80]}")
            article = fetch_article(session, url)

            if article:
                save_article(article)
                nk = add_discovered_keywords(db, article["content"])
                new_keywords_total += nk
                scraped_count += 1
                log(f"✅ [{scraped_count}/{MAX_ARTICLES}] '{article['title'][:50]}'")
            else:
                log("⏭️ Пропущено (мало контента / пейволл без аккаунта)")

            human_delay()

    save_keywords(db)

    log(f"\n{'='*60}")
    log(f"✅ Готово: {scraped_count} статей | +{new_keywords_total} новых терминов")
    log(f"📚 База ключевых слов: {len(db['queue'])} запросов")

    if AUTO_GIT_PUSH and scraped_count > 0:
        git_push(scraped_count, new_keywords_total)


if __name__ == "__main__":
    scrape()
