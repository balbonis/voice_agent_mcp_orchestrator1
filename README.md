
# Voice Agent Architecture (FastAPI + Redis + ElevenLabs)

A minimal, production-ready scaffold that implements the updated diagram:
Actor → List Channel → **API Gateway (FastAPI)** → **Agent Server** → **ElevenLabs**
and a centralized **Memory / Session DB** (Redis).

## Features
- FastAPI gateway with `/health` and `/sessions/{session_id}/message` endpoints
- Centralized session/state storage via Redis (with in-memory fallback)
- Pluggable Agent Server (simple rule/echo agent provided)
- Optional ElevenLabs TTS integration (stubbed if no API key)
- Dockerfile + docker-compose for one-command spin up
- MIT licensed and test scaffold included

## Quickstart

```bash
git clone <your-repo-url>
cd voice-agent-architecture
cp .env.example .env
# (optional) edit .env to set ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID
docker compose up --build
```

Then open: `http://localhost:8000/docs`

### Send a message

```bash
curl -X POST http://localhost:8000/sessions/demo/message   -H 'Content-Type: application/json'   -d '{"text":"Hello agent","voice":false}'
```

### With TTS output

```bash
curl -X POST http://localhost:8000/sessions/demo/message   -H 'Content-Type: application/json'   -d '{"text":"Speak this please","voice":true}'
```

## Project Layout
```
src/
  api/
    main.py            # FastAPI routes (API Gateway)
  agent/
    server.py          # AgentServer (business/AI logic)
  integrations/
    elevenlabs.py      # ElevenLabs client (optional)
  memory/
    store.py           # Redis-backed session/state store
tests/
  test_health.py
```

## Notes
- If `ELEVENLABS_API_KEY` is not set, the TTS call returns a stub with `audio: null`.
- Replace the simple Agent logic with your LLM/chain of choice.
- For persistence beyond Redis, add Postgres and extend `memory/store.py`.

## Security
- Add authentication (tokens/keys) on the API routes for production.
- Consider rate limiting and request validation.

---

© 2025 MIT License.
