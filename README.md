# Perific Time Report

Weekly time tracking with automatic Slack reminders.

## Live URL

[https://perific-time.up.railway.app](https://perific-time.up.railway.app)

## Stack

- **Backend:** FastAPI + APScheduler
- **Database:** PostgreSQL (Railway managed)
- **Notifications:** Slack Web API (DM)
- **Hosting:** Railway (enegic.app@gmail.com)

---

## How It Works

Developers receive a Slack DM every Friday with a personal link to the time report form. They distribute their week across projects and categories in percentages until they reach 100%, then submit. No login required.

### Reminder Schedule

| Time | Event |
|------|-------|
| Friday 10:00 | DM to everyone who hasn't reported that week |
| Friday 15:00 | Reminder DM — only to those who still haven't reported |
| Monday 10:00 | Reminder about last week — only to those who never submitted |

Anyone who has already submitted receives no further reminders.

### Personal Links

Each DM contains a personal link:
```
https://perific-time.up.railway.app?uid=UXXXXXXXX&week=2026-W16
```

The form pre-fills the name and locks the field. The correct week is pre-selected automatically.

---

## Environment Variables

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Set automatically by Railway (reference Postgres service) |
| `SLACK_BOT_TOKEN` | `xoxb-...` from Slack App → Install App → Bot User OAuth Token |
| `APP_URL` | `https://perific-time.up.railway.app` |
| `START_WEEK` | `2026-W16` — reminders are never sent for weeks before this |

---

## Reporters (config.py)

The list of developers who receive reminders is defined in `config.py`:

```python
REPORTERS = [
    {"name": "Tomas Ö",     "slack_id": "U0A5QA2BZ"},
    {"name": "Anders B",    "slack_id": "U3WBSPKPW"},
    {"name": "Muzaffer A",  "slack_id": "U06TB02GY4U"},
    {"name": "Guillaume L", "slack_id": "U04UJ5CGRQQ"},
    {"name": "Jonny S",     "slack_id": "U04M056CF29"},
    {"name": "Dennis L",    "slack_id": "U0450PC2Y9H"},
    {"name": "Simon G",     "slack_id": "U03G4KL4K8X"},
    {"name": "Oskar Ö",     "slack_id": "U02R46W57PA"},
]
```

To find a Slack User ID: click on a person in Slack → View profile → ··· → Copy member ID

---

## Slack App Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Name: `Perific Time-bot`, select the Perific workspace
3. Go to **OAuth & Permissions** → **Bot Token Scopes** → add:
   - `chat:write`
   - `im:write`
4. Click **Install to Workspace** → copy the **Bot User OAuth Token** (`xoxb-...`)
5. Set as `SLACK_BOT_TOKEN` in Railway

---

## Deploy to Railway

```bash
npm install -g @railway/cli
railway login
railway link        # select project + service
railway up
```

Add Postgres via Railway dashboard: **New** → **Database** → **PostgreSQL**

---

## Projects & Categories

### Projects
| Group | Options |
|-------|---------|
| Software | Shield, App, Admin / Webb, Flow / Värme 2.0 |
| Hardware | Floor, Thor Charger, Flow Gateway |
| Other | Möte, Intern, Infra / Backend |
| Absence | Ledigt, Sjuk, VAB |

### Categories
- Nyutveckling
- Support / Maint.
- Möten / Övrigt
- Ledighet (auto-selected when absence project is chosen)

---

## Overview (Hamburger Menu)

The ☰ menu opens a fullscreen view with two tabs:

- **📊 Veckoöversikt** — pivot table showing average % per project per person for a selected period, plus team average
- **📋 Detaljvy** — all submitted entries with CSV export

---

## Local Development

```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:pass@localhost/timrapport"
export SLACK_BOT_TOKEN="xoxb-..."
export APP_URL="http://localhost:8000"
export START_WEEK="2026-W16"
uvicorn main:app --reload
```
