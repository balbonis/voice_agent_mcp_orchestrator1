
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from src.agent.server import AgentServer
from src.memory.store import get_store
from src.integrations.elevenlabs import synthesize_tts

load_dotenv()

app = FastAPI(title="API Gateway", version="0.1.0")

store = get_store(os.getenv("REDIS_URL"))
agent = AgentServer(store=store)

class MessageIn(BaseModel):
    text: str
    voice: bool = False
    metadata: dict | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sessions/{session_id}/message")
async def message(session_id: str, payload: MessageIn):
    if not payload.text:
        raise HTTPException(status_code=400, detail="text is required")
    # Get previous memory/context
    memory = await store.get_session(session_id)
    # Process via agent
    reply, updated_memory = await agent.handle(session_id, payload.text, memory, payload.metadata or {})
    await store.set_session(session_id, updated_memory)

    audio = None
    if payload.voice:
        audio = await synthesize_tts(reply)

    return {
        "session_id": session_id,
        "reply": reply,
        "memory": updated_memory,
        "audio": audio,  # base64 or None
    }
