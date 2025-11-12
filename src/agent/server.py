
from typing import Tuple, Dict, Any

class AgentServer:
    """Simple demo agent.

    Replace this with your LLM or tool-using agent. The interface returns
    a tuple of (reply_text, updated_memory_dict).
    """
    def __init__(self, store):
        self.store = store

    async def handle(self, session_id: str, text: str, memory: Dict[str, Any] | None, metadata: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        memory = memory or {}
        history = memory.get("history", [])
        history.append({"role": "user", "text": text})
        # Simple rule: if user says hello, respond nicely, otherwise echo
        if "hello" in text.lower():
            reply = "Hi! I'm your agent. How can I help?"
        else:
            reply = f"You said: {text}"
        history.append({"role": "agent", "text": reply})
        memory["history"] = history
        # Example counter
        memory["turns"] = memory.get("turns", 0) + 1
        return reply, memory
