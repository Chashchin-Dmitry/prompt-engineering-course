#!/usr/bin/env python3
"""
Pipeline — запускает полный конвейер: scraper → processor → embedder → git push.
Это то что запускает cron каждую ночь.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
VENV_PYTHON = SCRIPTS_DIR.parent / ".venv" / "bin" / "python"


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


def run_step(name: str, script: str) -> bool:
    log(f"\n{'='*60}")
    log(f"▶️  {name}")
    result = subprocess.run(
        [str(VENV_PYTHON), str(SCRIPTS_DIR / script)],
        capture_output=False
    )
    if result.returncode != 0:
        log(f"❌ {name} завершился с ошибкой (код {result.returncode})")
        return False
    log(f"✅ {name} завершён")
    return True


def main():
    log("🚀 Запуск полного конвейера")
    start = datetime.now()

    steps = [
        ("1/3 — Scraper (сбор с Medium)", "scraper.py"),
        ("2/3 — Processor (очистка + чанкинг)", "processor.py"),
        ("3/3 — Embedder (векторизация)", "embedder.py"),
    ]

    for name, script in steps:
        ok = run_step(name, script)
        if not ok:
            log(f"⚠️  Конвейер остановлен на шаге: {name}")
            sys.exit(1)

    elapsed = (datetime.now() - start).seconds
    log(f"\n✅ Конвейер завершён за {elapsed}с")


if __name__ == "__main__":
    main()
