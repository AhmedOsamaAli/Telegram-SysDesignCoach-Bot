# 📚 Daily System Design Bot

A personal Telegram bot that, **every day at 9 AM (Cairo time)**:

1. Fetches a fresh **system-design / software-engineering article** from top blogs
   (ByteByteGo, Netflix, Meta, AWS, Cloudflare, Martin Fowler, InfoQ, High Scalability, …).
2. Uses **Google Gemini** (free tier) to read the *actual* article and build a **hard quiz**
   (mix of multiple-choice and true/false) that tests deep understanding and trade-offs.
3. Sends it to you as **native Telegram quiz polls** — tap an answer and Telegram
   instantly shows if you're right, with an explanation that teaches the concept.

Everything runs on **GitHub Actions for free** — no server, no PC needs to stay on.

---

## What you need (all free)

| Thing | Where to get it |
| --- | --- |
| Telegram bot token | Message [@BotFather](https://t.me/BotFather) → `/newbot` |
| Your chat id | Message [@userinfobot](https://t.me/userinfobot) → it replies with your id |
| Gemini API key | [Google AI Studio → Get API key](https://aistudio.google.com/apikey) |
| GitHub account | [github.com](https://github.com) |

---

## Setup (10 minutes)

### 1. Create your bot
1. Open Telegram, message **@BotFather**, send `/newbot`, follow the prompts.
2. Copy the **bot token** it gives you.
3. **Send any message to your new bot** (e.g. "hi") so it is allowed to message you.
4. Message **@userinfobot** and copy your numeric **chat id**.

### 2. Get a Gemini key
Go to https://aistudio.google.com/apikey, click **Create API key**, copy it.

### 3. Put this project on GitHub
1. Create a **new repository** (it can be private).
2. Upload all files in this folder to it (or `git push`).

### 4. Add your secrets
In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**.
Add these three:

| Name | Value |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | your bot token |
| `TELEGRAM_CHAT_ID` | your chat id |
| `GEMINI_API_KEY` | your Gemini key |

### 5. Turn it on & test
1. Go to the **Actions** tab → allow workflows if prompted.
2. Open **Daily System Design Bot** → **Run workflow** to test right now.
   (Manual runs always send, ignoring the time check.)
3. You should get a message + quiz in Telegram within a minute. 🎉

After that it runs automatically every day at ~9 AM Cairo time.

---

## Run it locally (optional)

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env   # then edit .env with your tokens
$env:FORCE_SEND = "1"          # send immediately, ignoring the 9 AM check
python bot.py
```

---

## Customize

- **Change the sources:** edit the `FEEDS` list in [feeds.py](feeds.py).
- **Change the time:** edit the `cron:` lines in
  [.github/workflows/daily.yml](.github/workflows/daily.yml)
  (GitHub cron is in **UTC**; two entries are used so it stays at 9 AM through Egypt's
  daylight-saving change).
- **More/fewer questions:** change `NUM_QUESTIONS` in [bot.py](bot.py).
- **Different model:** set a `GEMINI_MODEL` secret/env (default `gemini-2.5-flash`).

---

## Curated library (read them in order)
The bot first works through a hand-picked, ordered list of top articles in
[library.py](library.py) — starting with Hello Interview's "System Design in a Hurry",
canonical classics (Dynamo, Microservices, CQRS, Event Sourcing), and more.

- **One per day, in order.** Each send marks the previous article complete and advances
  to the next (the cursor `library_index` lives in `sent_articles.json`).
- **Grow it toward hundreds:** just append more `{"title", "url", "source"}` entries to
  `LIBRARY`. Broken or paywalled links are skipped automatically, so add generously.
- **When the library runs out**, the bot automatically falls back to the live RSS feeds.

## Get more on demand
Want the next article right now instead of waiting for 9 AM? Open the **Actions** tab →
**Daily System Design Bot** → **Run workflow**. A manual run always sends the next item
and advances your progress.

---

## How repeats are avoided
Sent articles are recorded in `sent_articles.json`, which the workflow commits back to the
repo after each run, so you never get the same article twice.

## Notes
- Telegram quiz polls are self-scoring, so the bot only needs to run once a day — no
  always-on server required.
- Free-tier limits (Gemini, GitHub Actions minutes for public/private repos) are far more
  than one run per day needs.
