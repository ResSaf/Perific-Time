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
        {""},
        # Lägg till övriga 5 här ...
    ]
