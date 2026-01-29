from collections import defaultdict
from typing import List, Dict

# Simple in-memory storage (later: DB)
_conversations: Dict[str, List[dict]] = defaultdict(list)

def add_message(user_id: str, role: str, content: str):
    _conversations[user_id].append({
        "role": role,
        "content": content
    })

def get_conversation(user_id: str, limit: int = 10) -> List[dict]:
    return _conversations[user_id][-limit:]
