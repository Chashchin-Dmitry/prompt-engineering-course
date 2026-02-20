#!/bin/bash
# run_scraper.sh — проверяет авторизацию перед запуском скрапера

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG="$REPO_DIR/logs/scraper.log"
PYTHON="$REPO_DIR/.venv/bin/python3"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

mkdir -p "$REPO_DIR/logs"

log "============================================================"
log "🔎 Предстартовая проверка..."

# Проверяем: есть ли куки Medium + доступен ли бесплатный контент
CHECK=$($PYTHON - <<'EOF'
from pycookiecheat import chrome_cookies
import curl_cffi.requests as requests
import sys

try:
    cookies = chrome_cookies('https://medium.com')
    sid = cookies.get('sid', '')
    uid = cookies.get('uid', '')

    if not sid or not uid:
        print("NO_AUTH")
        sys.exit(1)

    # Тестируем бесплатную статью
    TEST_URL = "https://medium.com/feed/tag/prompt-engineering"
    r = requests.get(TEST_URL, cookies=cookies, impersonate='chrome131', timeout=10)

    if r.status_code == 200 and len(r.text) > 1000:
        print("OK")
    else:
        print("NO_MEDIUM")
except Exception as e:
    print(f"ERROR:{e}")
EOF
)

if [ "$CHECK" = "OK" ]; then
    log "✅ Авторизация OK — запускаем полный конвейер"
    cd "$REPO_DIR"
    $PYTHON "$SCRIPT_DIR/pipeline.py"
elif [ "$CHECK" = "NO_AUTH" ]; then
    log "⛔ Chrome не залогинен в Google/Medium — пропускаем запуск"
    exit 1
elif [ "$CHECK" = "NO_MEDIUM" ]; then
    log "⛔ Medium недоступен или пейвол — пропускаем запуск"
    exit 1
else
    log "⛔ Ошибка проверки: $CHECK — пропускаем запуск"
    exit 1
fi
