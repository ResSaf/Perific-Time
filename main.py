import os
from datetime import date, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from database import init_db, save_entry, get_entries, has_reported_this_week
from slack_bot import send_dm
from config import REPORTERS, APP_URL

START_WEEK = os.environ.get("START_WEEK", "2026-W16")

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    # Fredag 10:00 — första utskick till alla
    scheduler.add_job(remind_friday_morning, CronTrigger(day_of_week="fri", hour=10, minute=0), id="reminder_morning")
    # Fredag 15:00 — påminnelse till de som inte svarat
    scheduler.add_job(remind_friday_afternoon, CronTrigger(day_of_week="fri", hour=15, minute=0), id="reminder_afternoon")
    # Måndag 10:00 — påminnelse om missad förra veckan
    scheduler.add_job(remind_monday, CronTrigger(day_of_week="mon", hour=10, minute=0), id="reminder_monday")
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


class EntryIn(BaseModel):
    slack_id: str
    name: str
    week: str
    project: str
    category: str
    pct: float
    dev: float = 0
    support: float = 0
    admin: float = 0
    absence: float = 0


@app.post("/api/submit")
def submit(entry: EntryIn):
    if entry.pct <= 0:
        raise HTTPException(status_code=400, detail="Andel måste vara större än 0.")
    if entry.pct > 100:
        raise HTTPException(status_code=400, detail="Andel får inte överstiga 100%.")
    save_entry(entry)
    return {"ok": True}


@app.get("/api/entries")
def entries():
    return get_entries()


@app.get("/api/reporters")
def reporters():
    return {r["slack_id"]: r["name"] for r in REPORTERS}


@app.get("/api/test-dm/{slack_id}")
async def test_dm(slack_id: str):
    await send_dm(slack_id, "Hej! 👋 Detta är ett test av Perific Timrapport-boten. Om du ser detta funkar Slack-kopplingen! ✅")
    return {"ok": True}


# ── Schedulers ───────────────────────────────────────────────────────────────

async def remind_friday_morning():
    """Fredag 10:00 — första utskick till alla."""
    week = current_week()
    if week < START_WEEK:
        return
    for person in REPORTERS:
        if not has_reported_this_week(person["slack_id"], week):
            link = f"{APP_URL}?uid={person['slack_id']}&week={week}"
            week_label = f"v{week.split('-W')[1]}"
            await send_dm(person["slack_id"],
                f"Hej {person['name']}! 👋\n"
                f"Idag är det dags att fylla i veckans tidsrapport för *{week_label}*.\n"
                f"En snabb uppskattning av hur din tid fördelats mellan projekt och aktiviteter — ingen exakthet krävs.\n"
                f"Svaren används för kapacitetsplanering och arbetsbelastningsöversikt.\n"
                f"Du kan fylla i den redan nu eller senast kl 15:00.\n"
                f"👉 {link}\n\n"
                f"/ Tack, Perific"
            )


async def remind_friday_afternoon():
    """Fredag 15:00 — påminnelse till de som INTE svarat sedan 10:00."""
    week = current_week()
    if week < START_WEEK:
        return
    for person in REPORTERS:
        if not has_reported_this_week(person["slack_id"], week):
            link = f"{APP_URL}?uid={person['slack_id']}&week={week}"
            week_label = f"v{week.split('-W')[1]}"
            await send_dm(person["slack_id"],
                f"Hej {person['name']}! 👋\n"
                f"Nu är det dags att fylla i veckans tidsrapport för *{week_label}*.\n"
                f"En snabb uppskattning av hur din tid fördelats mellan projekt och aktiviteter.\n"
                f"Svaren används för kapacitetsplanering och arbetsbelastningsöversikt.\n"
                f"👉 {link}\n\n"
                f"/ Tack för den här veckan och trevlig helg! 🎉\n"
                f"Perific"
            )


async def remind_monday():
    """Måndag 10:00 — påminnelse om missad förra veckan."""
    last = last_week()
    if last < START_WEEK:
        return
    for person in REPORTERS:
        if not has_reported_this_week(person["slack_id"], last):
            link = f"{APP_URL}?uid={person['slack_id']}&week={last}"
            week_label = f"v{last.split('-W')[1]}"
            await send_dm(person["slack_id"],
                f"Hej {person['name']}! 📋\n"
                f"Tidsrapporten för *{week_label}* är fortfarande inte inskickad.\n"
                f"Du kan fortfarande fylla i den i efterhand här: {link}\n\n"
                f"/ Tack, Perific"
            )


def current_week() -> str:
    iso = date.today().isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"

def last_week() -> str:
    iso = (date.today() - timedelta(weeks=1)).isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    return FileResponse("static/index.html")
