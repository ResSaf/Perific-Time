import os
import psycopg2
from psycopg2.extras import RealDictCursor

_raw_url = os.environ.get("DATABASE_URL", "")
DATABASE_URL = _raw_url.replace("postgres://", "postgresql://", 1)


def get_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id         SERIAL PRIMARY KEY,
                    slack_id   TEXT NOT NULL,
                    name       TEXT NOT NULL,
                    week       TEXT NOT NULL,
                    project    TEXT NOT NULL,
                    category   TEXT NOT NULL DEFAULT '',
                    pct        NUMERIC NOT NULL DEFAULT 0,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
            """)
            # Lägg till kolumner om de saknas (migrering)
            for col, typedef in [("category", "TEXT NOT NULL DEFAULT ''"), ("pct", "NUMERIC NOT NULL DEFAULT 0")]:
                cur.execute(f"""
                    ALTER TABLE entries ADD COLUMN IF NOT EXISTS {col} {typedef}
                """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_entries_week_slack
                ON entries (week, slack_id)
            """)
        conn.commit()


def save_entry(entry):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO entries (slack_id, name, week, project, category, pct)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                entry.slack_id,
                entry.name,
                entry.week,
                entry.project,
                entry.category,
                entry.pct,
            ))
        conn.commit()


def get_entries() -> list:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, week, project, category, pct,
                       to_char(created_at, 'YYYY-MM-DD HH24:MI') AS created_at
                FROM entries
                ORDER BY created_at DESC
            """)
            return [dict(row) for row in cur.fetchall()]


def has_reported_this_week(slack_id: str, week: str) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM entries WHERE slack_id = %s AND week = %s LIMIT 1",
                (slack_id, week),
            )
            return cur.fetchone() is not None
