# Changelog — Perific Timrapport

## v1.5.0 — 2026-04-17
- Support / Maint. delad i två separata kategorier: Support och Maintenance
- Flow Gateway omdöpt till Flow / Gateway

## v1.4.0 — 2026-04-17 (current)
- Added help button (?) with pop-up guide in Swedish
- Added SW / Backend för HW as project option (replaces Intern)
- Timezone fix: scheduler now runs on Europe/Stockholm
- Manual trigger endpoint for Slack reminders (/api/trigger-morning)

## v1.3.0 — 2026-04-15
- Three distinct Slack reminder messages:
  - Friday 10:00 — first reminder to all
  - Friday 15:00 — nudge to those who haven't reported
  - Monday 10:00 — reminder about missed last week
- Personal links include correct week (?uid=&week=)
- START_WEEK environment variable — no reminders sent before go-live week
- Slack App configured with chat:write + im:write scopes

## v1.2.0 — 2026-04-14
- Fullscreen overview via hamburger menu (☰)
  - 📊 Veckoöversikt — pivot table with team average, heat colors
  - 📋 Detaljvy — all entries with CSV export
- Sticky name column in pivot table
- Confirmation screen after submit showing only your own rows
- No log table visible on main form — privacy by default

## v1.1.0 — 2026-04-14
- Multi-row form: add one row at a time until 100%
- Progress bar filling up to 100%
- Save button only appears when total reaches 100%
- Absence projects (Ledigt/Sjuk/VAB) auto-select Ledighet category
- Ledighet category hidden for non-absence projects
- Revised project list:
  - Software: Shield, App, Admin/Webb, Flow/Värme 2.0
  - Hardware: Floor, Thor Charger, Flow Gateway
  - Övrigt: Möte, SW/Backend för HW, Infra/Backend
  - Frånvaro: Ledigt, Sjuk, VAB
- % instead of hours
- Autocomplete on name field from reporter list

## v1.0.0 — 2026-04-13
- Initial deploy on Railway
- FastAPI backend + PostgreSQL
- Weekly time report form (Gustav's original design)
- Slack DM reminders via APScheduler
- Personal links with ?uid= pre-filling name
- CSV export
- Reporter list with Slack User IDs in config.py
