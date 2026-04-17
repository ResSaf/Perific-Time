import os
import json

# Railway-app URL (sätt som miljövariabel i Railway-dashboarden)
APP_URL = os.environ.get("APP_URL", "https://perific-timrapport.up.railway.app")

# REPORTERS kan antingen sättas som JSON-miljövariabel eller hårdkodas här.
# Miljövariabel (REPORTERS_JSON) har prioritet — bekvämt för att lägga till folk
# utan att deploya om.
#
# Format: [{"name": "Tomas Ö", "slack_id": "U0123456"}, ...]

_reporters_json = os.environ.get("REPORTERS_JSON")

if _reporters_json:
    REPORTERS: list[dict] = json.loads(_reporters_json)
else:
    # Hårdkodad fallback — uppdatera med riktiga Slack User IDs
    REPORTERS: list[dict] = [
        {"name": "Tomas Ö",    "slack_id": "U0A5QA2BZ"},
        {"name": "Anders B",     "slack_id": "U3WBSPKPW"},
        {"name": "Muzaffer A",     "slack_id": "U06TB02GY4U"},
        {"name": "Guillaume L",    "slack_id": "U04UJ5CGRQQ"},
        {"name": "Jonny S",     "slack_id": "U04M056CF29"},
        {"name": "Dennis L",     "slack_id": "U0450PC2Y9H"},
        {"name": "Simon G",    "slack_id": "U03G4KL4K8X"},
        {"name": "Oskar Ö",    "slack_id": "U02R46W57PA"},
        {"name": "Erik Å",    "slack_id": "U03G4KL9QDD"},
        # Lägg till övriga 5 här ...
    ]
