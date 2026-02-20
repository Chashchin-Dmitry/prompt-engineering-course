# CLAUDE.md — AI Agent Instructions

## Project Philosophy: "Universal Gearbox" 🔧

Этот проект — универсальная коробка передач. Один фреймворк промт-инжиниринга который вставляется в любой контекст и работает: фронт, бек, продукт, маркетинг, аналитика. Как нейтраль, 1-я, 2-я передача — логика одна, применение разное.

This project is a universal gearbox. One prompt engineering framework that plugs into any context and works: front-end, back-end, product, marketing, analytics. Like neutral, 1st, 2nd gear — same logic, different application.

---

## Project Structure

- `modules/` — Course content organized by topic. Each module has `README.md` (bilingual), examples, exercises.
- `content/raw/` — Raw scraped content from Medium. Do not edit manually.
- `content/processed/` — Cleaned, structured markdown ready for course integration.
- `content/screenshots/` — Screenshots of source articles for reference.
- `scripts/` — All automation scripts. See `scripts/README.md`.
- `docs/` — Project documentation, architecture decisions, research notes.

---

## Content Standards

### Every module must have:
- `README.md` — bilingual (RU + EN), clear structure
- Practical examples (not just theory)
- At least one real use case
- References to source articles

### Processed content format:
```markdown
# Article Title

**Source:** [URL](URL)
**Date scraped:** YYYY-MM-DD
**Language:** EN/RU
**Tags:** tag1, tag2

---

[Content here]

---

**Key Takeaways:**
- Point 1
- Point 2
```

---

## Scraping Rules

1. Respectful rate limiting — 2-5 second delays between requests
2. Human-like scrolling behavior
3. Run only during off-hours (03:00 local time via cron)
4. Max 20 articles per run to avoid detection
5. Always save both screenshot AND markdown

---

## Git Conventions

- Commit after every scraping run
- Use descriptive commits: `feat: add 5 articles on chain-of-thought prompting`
- Never commit `.env` or Chrome profile copies
- Branch `main` is always stable

---

## Modules Structure

```
01-foundations/     → What is prompting, basic concepts, mental models
02-core-techniques/ → Zero-shot, few-shot, CoT, role prompting
03-advanced/        → RAG, agents, multi-step, self-consistency
04-tools/           → ChatGPT, Claude, Gemini, Cursor, Perplexity, etc.
05-use-cases/       → Dev, product, marketing, data, creative
06-best-practices/  → Checklists, templates, anti-patterns
```
