import os
from slack_sdk.web.async_client import AsyncWebClient

_client = None

def _get_client() -> AsyncWebClient:
    global _client
    if _client is None:
        token = os.environ["SLACK_BOT_TOKEN"]
        _client = AsyncWebClient(token=token)
    return _client


async def send_dm(user_id: str, text: str):
    client = _get_client()
    try:
        # Öppna DM-kanal och skicka meddelande
        conv = await client.conversations_open(users=user_id)
        channel = conv["channel"]["id"]
        await client.chat_postMessage(channel=channel, text=text)
    except Exception as e:
        print(f"[slack] Kunde inte skicka DM till {user_id}: {e}")
