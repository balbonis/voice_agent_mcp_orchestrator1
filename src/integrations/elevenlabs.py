
import os
import base64
import httpx

ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
TTS_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"

async def synthesize_tts(text: str):
    """Return base64-encoded MP3 bytes or None when not configured."""
    if not ELEVEN_API_KEY:
        return None

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "accept": "audio/mpeg",
        "content-type": "application/json",
    }
    payload = {"text": text, "model_id": "eleven_multilingual_v2"}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(TTS_URL, headers=headers, json=payload)
        r.raise_for_status()
        b = r.content
        return base64.b64encode(b).decode("utf-8")
