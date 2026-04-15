# Perific Timrapport

Veckovis tidsrapportering med automatiska Slack-påminnelser.

## Stack

- **Backend:** FastAPI + APScheduler
- **Databas:** PostgreSQL (Railway managed)
- **Notifikationer:** Slack Web API (DM)
- **Hosting:** Railway

---

## Deploy till Railway

### 1. Skapa Railway-projekt

```bash
npm install -g @railway/cli
railway login
railway init
```

### 2. Lägg till Postgres

I Railway-dashboarden: **New** → **Database** → **PostgreSQL**  
Railway sätter automatiskt `DATABASE_URL` som miljövariabel.

### 3. Miljövariabler att sätta

| Variabel          | Värde                                              |
|-------------------|----------------------------------------------------|
| `DATABASE_URL`    | Sätts automatiskt av Railway                       |
| `SLACK_BOT_TOKEN` | `xoxb-...` (se nedan)                              |
| `APP_URL`         | `https://ditt-projekt.up.railway.app`              |
| `REPORTERS_JSON`  | Se format nedan (optional — kan hårdkodas i config.py) |

**REPORTERS_JSON format:**
```json
[
  {"name": "Tomas Ö",  "slack_id": "U0123456"},
  {"name": "Erik L",   "slack_id": "U0234567"}
]
```

**Hitta Slack User ID:**  
Klicka på person i Slack → View profile → ⋯ → Copy member ID

### 4. Skapa Slack App

1. Gå till https://api.slack.com/apps → **Create New App** → From manifest
2. Klistra in detta manifest:

```yaml
display_information:
  name: Perific Timrapport
  description: Veckovis tidsrapportering
oauth_config:
  scopes:
    bot:
      - chat:write
      - im:write
      - users:read
settings:
  org_deploy_enabled: false
  socket_mode_enabled: false
```

3. **Install to workspace** → kopiera **Bot User OAuth Token** (`xoxb-...`)
4. Sätt som `SLACK_BOT_TOKEN` i Railway

### 5. Deploy

```bash
railway up
```

---

## Påminnelselogik

| Tid           | Händelse                                              |
|---------------|-------------------------------------------------------|
| Fredag 09:00  | DM till alla som inte rapporterat den veckan          |
| Fredag 14:00  | DM igen — men bara till de som fortfarande inte svarat |

Ingen som rapporterat får någon påminnelse alls.

---

## Personliga länkar

DM:en innehåller en personlig länk:
```
https://app.railway.app?uid=U0123456
```

Formuläret pre-fyller automatiskt namn och låser fältet.  
`slack_id` skickas med vid submit → används för att markera som rapporterad.

---

## Lokal utveckling

```bash
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:pass@localhost/timrapport"
export SLACK_BOT_TOKEN="xoxb-..."
export APP_URL="http://localhost:8000"
uvicorn main:app --reload
```
