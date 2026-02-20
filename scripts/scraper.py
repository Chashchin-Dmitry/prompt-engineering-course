#!/usr/bin/env python3
"""
Medium Scraper for Prompt Engineering Course
Имитирует поведение реального пользователя через копию Chrome профиля.
"""

import os
import sys
import time
import random
import shutil
import subprocess
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# Config
REPO_PATH = Path(os.getenv("REPO_PATH", Path(__file__).parent.parent))
CONTENT_RAW = REPO_PATH / "content" / "raw"
SCREENSHOTS_DIR = REPO_PATH / "content" / "screenshots"
CHROME_PROFILE_SRC = Path(os.getenv(
    "CHROME_PROFILE_PATH",
    os.path.expanduser("~/Library/Application Support/Google/Chrome/Default")
))
CHROME_PROFILE_TMP = REPO_PATH / "chrome-profile-copy"
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES_PER_RUN", 15))
MIN_DELAY = float(os.getenv("MIN_DELAY", 2))
MAX_DELAY = float(os.getenv("MAX_DELAY", 5))
AUTO_GIT_PUSH = os.getenv("AUTO_GIT_PUSH", "true").lower() == "true"

QUERIES = [q.strip() for q in os.getenv(
    "MEDIUM_QUERIES",
    "prompt engineering,AI tools,LLM prompting,ChatGPT tips,Claude AI"
).split(",")]

MEDIUM_SEARCH_URL = "https://medium.com/search?q={query}&source=search_post---------0"


def human_delay(min_s=None, max_s=None):
    """Случайная пауза как у человека."""
    time.sleep(random.uniform(min_s or MIN_DELAY, max_s or MAX_DELAY))


def human_scroll(page, steps=5):
    """Плавный скролл вниз."""
    for _ in range(steps):
        page.mouse.wheel(0, random.randint(200, 500))
        time.sleep(random.uniform(0.3, 0.8))


def copy_chrome_profile():
    """Копируем профиль Chrome во временную папку."""
    if CHROME_PROFILE_TMP.exists():
        shutil.rmtree(CHROME_PROFILE_TMP)
    print(f"📋 Копирую Chrome профиль...")
    shutil.copytree(CHROME_PROFILE_SRC, CHROME_PROFILE_TMP, ignore_errors=True)
    print("✅ Профиль скопирован")


def cleanup_chrome_profile():
    """Удаляем временную копию после работы."""
    if CHROME_PROFILE_TMP.exists():
        shutil.rmtree(CHROME_PROFILE_TMP)
    print("🧹 Временный профиль удалён")


def extract_article_content(page):
    """Извлекаем текст и метаданные статьи."""
    try:
        # Ждём загрузки контента
        page.wait_for_selector("article", timeout=10000)
        human_scroll(page, steps=8)

        title = page.title().replace(" | Medium", "").replace(" | by", "").strip()

        # Извлекаем текст статьи
        content = page.evaluate("""() => {
            const article = document.querySelector('article');
            if (!article) return '';
            // Убираем кнопки и навигацию
            const unwanted = article.querySelectorAll('button, nav, [role="navigation"]');
            unwanted.forEach(el => el.remove());
            return article.innerText;
        }""")

        # Автор
        author = page.evaluate("""() => {
            const authorEl = document.querySelector('a[data-testid="authorName"]') ||
                           document.querySelector('[rel="author"]');
            return authorEl ? authorEl.innerText : 'Unknown';
        }""")

        return {
            "title": title,
            "content": content,
            "author": author,
            "url": page.url,
            "scraped_at": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"⚠️ Ошибка извлечения контента: {e}")
        return None


def save_article(article_data, screenshot_bytes=None):
    """Сохраняем статью в markdown и скриншот."""
    if not article_data:
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = "".join(c for c in article_data["title"] if c.isalnum() or c in " -_")[:60]
    safe_title = safe_title.strip().replace(" ", "-")
    filename = f"{date_str}_{safe_title}"

    # Markdown
    md_content = f"""# {article_data['title']}

**Source:** [{article_data['url']}]({article_data['url']})
**Author:** {article_data['author']}
**Date scraped:** {date_str}
**Tags:** prompt-engineering, AI, medium

---

{article_data['content']}

---

*Scraped automatically for Prompt Engineering Course*
"""
    md_path = CONTENT_RAW / f"{filename}.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"💾 Сохранено: {md_path.name}")

    # Скриншот
    if screenshot_bytes:
        ss_path = SCREENSHOTS_DIR / f"{filename}.png"
        ss_path.parent.mkdir(parents=True, exist_ok=True)
        ss_path.write_bytes(screenshot_bytes)
        print(f"📸 Скриншот: {ss_path.name}")

    return filename


def get_article_links(page, query, max_links=5):
    """Получаем ссылки на статьи по запросу."""
    url = MEDIUM_SEARCH_URL.format(query=query.replace(" ", "%20"))
    print(f"🔍 Ищу: '{query}'")
    page.goto(url)
    human_delay(3, 6)
    human_scroll(page, steps=4)

    links = page.evaluate("""() => {
        const links = [];
        document.querySelectorAll('a[href*="/p/"], a[href*="medium.com/@"]').forEach(a => {
            const href = a.href;
            if (href && href.includes('medium.com') && !href.includes('/search') && 
                !href.includes('/tag/') && !links.includes(href)) {
                links.push(href);
            }
        });
        return links.slice(0, 10);
    }""")

    return links[:max_links]


def scrape():
    """Главная функция скрапинга."""
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync

    print(f"\n🚀 Запуск скрапера | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 Запросы: {', '.join(QUERIES)}")
    print(f"📦 Лимит: {MAX_ARTICLES} статей")

    copy_chrome_profile()

    scraped_count = 0
    scraped_urls = set()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(CHROME_PROFILE_TMP),
                channel="chrome",
                headless=False,  # Видимый браузер — меньше риск бана
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
                slow_mo=random.randint(50, 150),
            )

            page = browser.new_page()
            stealth_sync(page)

            # Устанавливаем реалистичный user agent
            page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            })

            for query in QUERIES:
                if scraped_count >= MAX_ARTICLES:
                    break

                links = get_article_links(page, query, max_links=5)
                print(f"  → Найдено {len(links)} статей")

                for url in links:
                    if scraped_count >= MAX_ARTICLES:
                        break
                    if url in scraped_urls:
                        continue

                    scraped_urls.add(url)

                    try:
                        print(f"\n📖 Читаю: {url[:80]}...")
                        page.goto(url)
                        human_delay(4, 7)

                        # Скриншот всей страницы
                        screenshot = page.screenshot(full_page=True)

                        # Текст
                        article = extract_article_content(page)

                        if article:
                            save_article(article, screenshot)
                            scraped_count += 1
                            print(f"✅ Статья {scraped_count}/{MAX_ARTICLES}")

                        human_delay(3, 6)

                    except Exception as e:
                        print(f"❌ Ошибка на {url}: {e}")
                        continue

            browser.close()

    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
    finally:
        cleanup_chrome_profile()

    print(f"\n✅ Готово! Собрано {scraped_count} статей")

    # Git push
    if AUTO_GIT_PUSH and scraped_count > 0:
        git_push(scraped_count)


def git_push(count):
    """Коммитим и пушим новый контент."""
    print("\n📤 Пушу в GitHub...")
    try:
        os.chdir(REPO_PATH)
        subprocess.run(["git", "add", "content/"], check=True)
        msg = f"feat: scrape {count} new Medium articles [{datetime.now().strftime('%Y-%m-%d')}]"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Запушено в GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git push не удался: {e}")


if __name__ == "__main__":
    scrape()
