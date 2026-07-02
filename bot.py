"""Daily system-design article + hard quiz Telegram bot.

Flow:
  1. Decide whether it should send now (9 AM Cairo, once per day).
  2. Pick the freshest unseen article from the RSS feeds.
  3. Extract the article text and ask Gemini to build a hard quiz from it.
  4. Send the article intro + native Telegram quiz polls (self-scoring).
  5. Record the article and the send date so it is never repeated.

Runs on GitHub Actions (see .github/workflows/daily.yml) or locally.
"""

from __future__ import annotations

import html
import json
import os
import random
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import feedparser
import requests
from bs4 import BeautifulSoup

from feeds import FEEDS
from library import LIBRARY

ROOT = Path(__file__).parent
STATE_FILE = ROOT / "sent_articles.json"
TIMEZONE = ZoneInfo("Africa/Cairo")
SEND_HOUR = 9  # 9 AM local time
MAX_SEEN = 500
NUM_QUESTIONS = 5
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


# --------------------------------------------------------------------------- #
# Environment / config
# --------------------------------------------------------------------------- #
def load_dotenv() -> None:
    """Load a local .env file if present (no external dependency needed)."""
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #
def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_sent_date": None, "seen": []}


def save_state(state: dict) -> None:
    state["seen"] = state.get("seen", [])[-MAX_SEEN:]
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def should_send(state: dict) -> bool:
    if os.getenv("FORCE_SEND"):
        return True
    now = datetime.now(TIMEZONE)
    if state.get("last_sent_date") == now.date().isoformat():
        return False
    return now.hour >= SEND_HOUR


# --------------------------------------------------------------------------- #
# Article selection
# --------------------------------------------------------------------------- #
def entry_id(entry) -> str:
    return getattr(entry, "id", None) or getattr(entry, "link", "") or entry.get("title", "")


def entry_timestamp(entry) -> float:
    for key in ("published_parsed", "updated_parsed"):
        value = entry.get(key)
        if value:
            return time.mktime(value)
    return 0.0


# Titles matching these are product/marketing posts, not learning material.
PROMO_PATTERNS = re.compile(
    r"\b("
    r"announc|introduc|now available|now in|now supports|now live|"
    r"we'?re excited|we are excited|new ways to|new features?|what'?s new|"
    r"trends? from|reserve your spot|register now|join us|roadshow|webinar|"
    r"sessions? 20\d\d|hitec|available today|coming soon|sign ?up|"
    r"partner|sponsor|pricing update|changelog|release notes?|"
    r"is here|expanding|unveil|launch|ga release|general availability|"
    r"black friday|sale|discount|promo"
    r")\b",
    re.IGNORECASE,
)


def is_promotional(title: str, summary_html: str) -> bool:
    if PROMO_PATTERNS.search(title or ""):
        return True
    snippet = clean_text(summary_html or "")[:300]
    return bool(PROMO_PATTERNS.search(snippet))


def pick_article(seen: set[str]) -> dict | None:
    candidates = []
    feeds = FEEDS[:]
    random.shuffle(feeds)
    for url in feeds:
        try:
            parsed = feedparser.parse(url, request_headers={"User-Agent": USER_AGENT})
        except Exception:
            continue
        source = parsed.feed.get("title", url)
        for entry in parsed.entries:
            eid = entry_id(entry)
            if not eid or eid in seen or not entry.get("link"):
                continue
            title = entry.get("title", "Untitled")
            summary_html = entry.get("summary", "") or (
                entry.get("content", [{}])[0].get("value", "") if entry.get("content") else ""
            )
            if is_promotional(title, summary_html):
                continue
            candidates.append(
                {
                    "id": eid,
                    "title": title,
                    "link": entry.get("link"),
                    "source": source,
                    "ts": entry_timestamp(entry),
                    "summary_html": summary_html,
                }
            )
    if not candidates:
        return None
    # Prefer fresh content but keep some variety: choose randomly from the 8 newest.
    candidates.sort(key=lambda c: c["ts"], reverse=True)
    return random.choice(candidates[:8])


def clean_text(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all(["p", "li", "h2", "h3"])]
    text = "\n".join(p for p in paragraphs if len(p) > 30)
    if not text:
        text = soup.get_text(" ", strip=True)
    return text


def fetch_article_text(article: dict) -> str:
    text = clean_text(article.get("summary_html", ""))
    try:
        resp = requests.get(article["link"], headers={"User-Agent": USER_AGENT}, timeout=25)
        resp.raise_for_status()
        page_text = clean_text(resp.text)
        if len(page_text) > len(text):
            text = page_text
    except requests.RequestException:
        pass
    return text[:8000]


def pick_from_library(state: dict, seen: set[str]):
    """Return (article, content, next_index) for the next usable library item.

    Walks forward from the stored cursor, skipping already-seen or broken
    (paywalled / too-short) entries. Returns (None, "", None) when exhausted.
    """
    index = state.get("library_index", 0)
    while index < len(LIBRARY):
        item = LIBRARY[index]
        url = item["url"]
        if url in seen:
            index += 1
            continue
        article = {
            "id": url,
            "title": item["title"],
            "link": url,
            "source": item.get("source", "Curated"),
            "ts": 0.0,
            "summary_html": "",
        }
        content = fetch_article_text(article)
        if len(content) >= 400:
            return article, content, index + 1
        print(f"Skipping library item (no readable text): {item['title']}")
        index += 1
    return None, "", None


# --------------------------------------------------------------------------- #
# Quiz generation (Gemini)
# --------------------------------------------------------------------------- #
QUIZ_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {"type": "array", "items": {"type": "string"}},
            "correct_index": {"type": "integer"},
            "explanation": {"type": "string"},
        },
        "required": ["question", "options", "correct_index", "explanation"],
    },
}

QUIZ_PROMPT = """You are a senior software architecture interviewer.
Read the article below and create exactly {n} HARD quiz questions that test DEEP
understanding, trade-offs, edge cases and design reasoning — not trivia or wording.

Rules:
- Mix multiple-choice (3-4 options) and True/False questions.
- Questions must be answerable ONLY from understanding the article's concepts.
- Make wrong options plausible to a mid-level engineer.
- "correct_index" is the 0-based index of the correct option.
- "explanation" (max ~200 chars) must justify the answer and teach the concept.
- Keep each question under 280 chars and each option under 95 chars.

ARTICLE TITLE: {title}

ARTICLE CONTENT:
{content}
"""


def generate_quiz(api_key: str, title: str, content: str) -> list[dict]:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={api_key}"
    )
    payload = {
        "contents": [
            {"parts": [{"text": QUIZ_PROMPT.format(n=NUM_QUESTIONS, title=title, content=content)}]}
        ],
        "generationConfig": {
            "temperature": 0.7,
            "response_mime_type": "application/json",
            "response_schema": QUIZ_SCHEMA,
        },
    }
    resp = requests.post(url, json=payload, timeout=90)
    resp.raise_for_status()
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    questions = json.loads(text)
    return [q for q in questions if _valid_question(q)]


def _valid_question(q: dict) -> bool:
    opts = q.get("options")
    return (
        isinstance(opts, list)
        and 2 <= len(opts) <= 10
        and isinstance(q.get("correct_index"), int)
        and 0 <= q["correct_index"] < len(opts)
        and bool(q.get("question"))
    )


# --------------------------------------------------------------------------- #
# Telegram
# --------------------------------------------------------------------------- #
def tg_api(token: str, method: str, **params) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    last_exc: Exception | None = None
    for attempt in range(4):
        try:
            resp = requests.post(url, data=params, timeout=60)
            resp.raise_for_status()
            body = resp.json()
            if not body.get("ok"):
                raise RuntimeError(f"Telegram error on {method}: {body}")
            return body
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Telegram request '{method}' failed after retries: {last_exc}")


def sanitize(text: str) -> str:
    """Remove zero-width / invisible characters some blogs embed as watermarks."""
    return "".join(
        ch for ch in text
        if ch == "\n" or (ch.isprintable() and unicodedata.category(ch) != "Cf")
    ).strip()


def send_article(token: str, chat_id: str, article: dict) -> None:
    title = html.escape(sanitize(article["title"]))
    source = html.escape(sanitize(article["source"]))
    link = article["link"]
    text = (
        "📚 <b>Today's System Design read</b>\n\n"
        f"<b>{title}</b>\n"
        f"<i>{source}</i>\n\n"
        f'🔗 <a href="{link}">Open the article</a>\n\n'
        "Read it fully, then take the quiz below. Tap an answer to see if you're "
        "right and why. 💪"
    )
    tg_api(token, "sendMessage", chat_id=chat_id, text=text, parse_mode="HTML")


def send_quiz(token: str, chat_id: str, questions: list[dict]) -> None:
    total = len(questions)
    tg_api(
        token,
        "sendMessage",
        chat_id=chat_id,
        text=f"🧠 <b>Quiz time — {total} hard questions.</b>\nAnswer each one, then the next appears.",
        parse_mode="HTML",
    )
    time.sleep(1)
    for i, q in enumerate(questions, 1):
        question = f"Question {i}/{total} — {q['question']}"[:300]
        options = [str(o)[:100] for o in q["options"]][:10]
        explanation = (q.get("explanation") or "")[:200]
        tg_api(
            token,
            "sendPoll",
            chat_id=chat_id,
            question=question,
            options=json.dumps(options),
            type="quiz",
            correct_option_id=q["correct_index"],
            explanation=explanation,
            is_anonymous="false",
        )
        time.sleep(2)
    tg_api(
        token,
        "sendMessage",
        chat_id=chat_id,
        text="✅ <b>That's all for today.</b> Tally your score and keep leveling up! 🚀",
        parse_mode="HTML",
    )


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    load_dotenv()
    state = load_state()

    if not should_send(state):
        print("Not send time yet (or already sent today). Skipping.")
        return

    token = require_env("TELEGRAM_BOT_TOKEN")
    chat_id = require_env("TELEGRAM_CHAT_ID")
    gemini_key = require_env("GEMINI_API_KEY")

    seen = set(state.get("seen", []))

    # 1) Work through the curated library in order (mark complete -> next).
    article, content, next_library_index = pick_from_library(state, seen)

    # 2) Fall back to live RSS feeds once the library is exhausted.
    if article is None:
        article = pick_article(seen)
        if not article:
            print("No new article found in library or feeds today.")
            return
        print(f"Selected from feeds: {article['title']} ({article['source']})")
        content = fetch_article_text(article)
        if len(content) < 400:
            print("Article text too short to build a good quiz; skipping this one.")
            state.setdefault("seen", []).append(article["id"])
            save_state(state)
            return
    else:
        print(f"Selected from library: {article['title']} ({article['source']})")

    try:
        questions = generate_quiz(gemini_key, article["title"], content)
    except Exception as exc:  # network / API / parse failure
        sys.exit(f"Quiz generation failed: {exc}")

    if not questions:
        sys.exit("Gemini returned no valid questions.")

    send_article(token, chat_id, article)
    time.sleep(2)
    send_quiz(token, chat_id, questions)

    state.setdefault("seen", []).append(article["id"])
    if next_library_index is not None:
        state["library_index"] = next_library_index
    state["last_sent_date"] = datetime.now(TIMEZONE).date().isoformat()
    save_state(state)
    print(f"Sent article + {len(questions)} questions.")


if __name__ == "__main__":
    main()
