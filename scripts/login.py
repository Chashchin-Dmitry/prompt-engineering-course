#!/usr/bin/env python3
"""
Интерактивный логин в Medium через Playwright.
Открывает браузер → ты логинишься → куки сохраняются автоматически.
Запускать один раз.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT = Path(__file__).parent / "storage_state.json"


def main():
    print("=" * 55)
    print("🔐 Medium Login — сохранение сессии")
    print("=" * 55)
    print()
    print("Откроется браузер. Сделай:")
    print("  1. Нажми Sign in на medium.com")
    print("  2. Залогинься через Google (или email)")
    print("  3. Убедись что видишь свою ленту")
    print("  4. Вернись сюда и нажми Enter")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
            ],
        )
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()
        page.goto("https://medium.com/m/signin")

        print("⏳ Браузер открыт. Логинься...")
        input("   После логина нажми Enter здесь: ")

        # Проверяем что залогинены
        page.goto("https://medium.com")
        page.wait_for_timeout(2000)

        title = page.title()
        print(f"   Страница: {title[:60]}")

        # Сохраняем storage state
        ctx.storage_state(path=str(OUTPUT))
        browser.close()

    print()
    print(f"✅ Куки сохранены: {OUTPUT}")
    print("   Теперь скрапер будет использовать эту сессию.")
    print()
    print("Запускай скрапер:")
    print("  cd /Users/dmitriivarvara/prompt-engineering-course")
    print("  .venv/bin/python scripts/scraper.py")


if __name__ == "__main__":
    main()
