#!/usr/bin/env python3
"""
Medium Scraper — Prompt Engineering Course
Рекурсивный снежный ком: парсим статьи → извлекаем новые термины → расширяем базу.
"""

import os
import sys
import time
import random
import shutil
import subprocess
import json
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── Пути ──────────────────────────────────────────────────────────────────────
REPO_PATH       = Path(os.getenv("REPO_PATH", Path(__file__).parent.parent))
CONTENT_RAW     = REPO_PATH / "content" / "raw"
SCREENSHOTS_DIR = REPO_PATH / "content" / "screenshots"
KEYWORDS_FILE   = Path(__file__).parent / "keywords.json"
LOGS_DIR        = REPO_PATH / "logs"

CHROME_PROFILE_SRC = Path(os.getenv(
    "CHROME_PROFILE_PATH",
    os.path.expanduser("~/Library/Application Support/Google/Chrome/Default")
))
CHROME_PROFILE_TMP = REPO_PATH / "chrome-profile-copy"

# ── Настройки ─────────────────────────────────────────────────────────────────
MAX_ARTICLES    = int(os.getenv("MAX_ARTICLES_PER_RUN", 15))
QUERIES_PER_RUN = int(os.getenv("QUERIES_PER_RUN", 5))
MIN_DELAY       = float(os.getenv("MIN_DELAY", 2))
MAX_DELAY       = float(os.getenv("MAX_DELAY", 5))
AUTO_GIT_PUSH   = os.getenv("AUTO_GIT_PUSH", "true").lower() == "true"

# AI-термины для извлечения новых ключевых слов из статей
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


def human_delay(mn=None, mx=None):
    time.sleep(random.uniform(mn or MIN_DELAY, mx or MAX_DELAY))


def human_scroll(page, steps=5):
    for _ in range(steps):
        page.mouse.wheel(0, random.randint(200, 500))
        time.sleep(random.uniform(0.3, 0.8))


# ── Keywords DB ───────────────────────────────────────────────────────────────

def load_keywords():
    if KEYWORDS_FILE.exists():
        return json.loads(KEYWORDS_FILE.read_text())
    return {"queue": [], "done": [], "discovered": [], "last_updated": ""}


def save_keywords(db):
    db["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    KEYWORDS_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2))


def pick_queries(db, n=QUERIES_PER_RUN):
    """Берём n запросов из очереди, не повторяем уже использованные."""
    available = [q for q in db["queue"] if q not in db["done"]]
    picks = available[:n]
    # Если очередь кончается — берём снова с начала (актуальность важна)
    if len(picks) < n:
        db["done"] = []
        picks = db["queue"][:n]
    return picks


def add_discovered_keywords(db, text):
    """Извлекаем новые AI-термины из текста статьи и добавляем в очередь."""
    found = set(AI_TERMS_PATTERN.findall(text))
    new_terms = []
    for term in found:
        term = term.strip().lower()
        if (term not in [q.lower() for q in db["queue"]] and
                term not in [d.lower() for d in db["discovered"]] and
                len(term) > 4):
            db["discovered"].append(term)
            db["queue"].append(term)
            new_terms.append(term)
    if new_terms:
        log(f"  🔍 Новые термины: {', '.join(new_terms[:5])}{'...' if len(new_terms) > 5 else ''}")
    return len(new_terms)


# ── Chrome ────────────────────────────────────────────────────────────────────

def copy_chrome_profile():
    if CHROME_PROFILE_TMP.exists():
        shutil.rmtree(CHROME_PROFILE_TMP)
    CHROME_PROFILE_TMP.mkdir(parents=True, exist_ok=True)
    log("📋 Копирую Chrome профиль...")
    subprocess.run([
        "rsync", "-a", "--quiet",
        "--exclude=SingletonLock",
        "--exclude=SingletonCookie",
        "--exclude=GPUCache",
        "--exclude=*.log",
        f"{CHROME_PROFILE_SRC}/",
        f"{CHROME_PROFILE_TMP}/"
    ], capture_output=True)
    log("✅ Профиль скопирован")


def cleanup_chrome_profile():
    if CHROME_PROFILE_TMP.exists():
        shutil.rmtree(CHROME_PROFILE_TMP)
    log("🧹 Временный профиль удалён")


# ── Scraping ──────────────────────────────────────────────────────────────────

def get_article_links(page, query, max_links=5):
    url = f"https://medium.com/search?q={query.replace(' ', '%20')}&source=search_post---------0"
    log(f"🔍 Ищу: '{query}'")
    try:
        page.goto(url, timeout=20000)
        human_delay(3, 6)
        human_scroll(page, steps=4)

        links = page.evaluate("""() => {
            const links = new Set();
            document.querySelectorAll('a[href]').forEach(a => {
                const h = a.href;
                if (h && h.includes('medium.com') &&
                    (h.includes('/p/') || (h.match(/medium\\.com\\/@[^/]+\\/[^/?]+/))) &&
                    !h.includes('/search') && !h.includes('/tag/') &&
                    !h.includes('/m/signin') && !h.includes('?source=follow')) {
                    links.add(h.split('?')[0]);
                }
            });
            return Array.from(links).slice(0, 10);
        }""")
        return links[:max_links]
    except Exception as e:
        log(f"⚠️ Ошибка поиска '{query}': {e}")
        return []


def extract_article(page):
    try:
        page.wait_for_selector("article", timeout=12000)
        human_scroll(page, steps=8)
        human_delay(2, 4)

        data = page.evaluate("""() => {
            const article = document.querySelector('article');
            if (!article) return null;
            const unwanted = article.querySelectorAll('button, nav, [role="navigation"], script, style');
            unwanted.forEach(el => el.remove());
            const title = document.title.replace(/ \\| Medium$/, '').replace(/ \\| by .+$/, '').trim();
            const authorEl = document.querySelector('a[data-testid="authorName"], [rel="author"]');
            const dateEl = document.querySelector('time');
            return {
                title: title,
                content: article.innerText.trim(),
                author: authorEl ? authorEl.innerText.trim() : 'Unknown',
                published: dateEl ? dateEl.getAttribute('datetime') : null
            };
        }""")
        if data:
            data["url"] = page.url
        return data
    except Exception as e:
        log(f"⚠️ Ошибка извлечения: {e}")
        return None


def save_article(article, screenshot=None):
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

    if screenshot:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        (SCREENSHOTS_DIR / f"{fname}.png").write_bytes(screenshot)

    log(f"💾 Сохранено: {fname[:50]}")
    return fname


# ── Main ──────────────────────────────────────────────────────────────────────

def scrape():
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync

    log("=" * 60)
    log(f"🚀 Запуск скрапера")

    db = load_keywords()
    queries = pick_queries(db, QUERIES_PER_RUN)
    log(f"📋 Запросы: {', '.join(queries)}")
    log(f"📦 Лимит: {MAX_ARTICLES} статей | Ключей в базе: {len(db['queue'])}")

    copy_chrome_profile()

    scraped_count = 0
    scraped_urls = set()
    new_keywords_total = 0

    try:
        with sync_playwright() as p:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=str(CHROME_PROFILE_TMP),
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-extensions",
                ],
                slow_mo=random.randint(60, 140),
            )

            page = ctx.new_page()
            stealth_sync(page)
            page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})

            for query in queries:
                if scraped_count >= MAX_ARTICLES:
                    break

                db["done"].append(query)
                links = get_article_links(page, query, max_links=4)
                log(f"  → {len(links)} статей найдено")

                for url in links:
                    if scraped_count >= MAX_ARTICLES:
                        break
                    if url in scraped_urls:
                        continue
                    scraped_urls.add(url)

                    try:
                        log(f"\n📖 {url[:80]}")
                        page.goto(url, timeout=20000)
                        human_delay(4, 7)

                        screenshot = page.screenshot(full_page=True)
                        article = extract_article(page)

                        if article and len(article.get("content", "")) > 500:
                            save_article(article, screenshot)
                            # Рекурсивное расширение базы
                            nk = add_discovered_keywords(db, article["content"])
                            new_keywords_total += nk
                            scraped_count += 1
                            log(f"✅ [{scraped_count}/{MAX_ARTICLES}] '{article['title'][:50]}'")
                        else:
                            log("⏭️ Пропущено (мало контента или пейволл)")

                        human_delay(3, 6)

                    except Exception as e:
                        log(f"❌ {url}: {e}")
                        continue

            ctx.close()

    except Exception as e:
        log(f"❌ Критическая ошибка: {e}")
    finally:
        cleanup_chrome_profile()

    save_keywords(db)

    log(f"\n{'='*60}")
    log(f"✅ Готово: {scraped_count} статей | +{new_keywords_total} новых терминов")
    log(f"📚 База ключевых слов: {len(db['queue'])} запросов")

    if AUTO_GIT_PUSH and scraped_count > 0:
        git_push(scraped_count, new_keywords_total)


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


if __name__ == "__main__":
    scrape()
