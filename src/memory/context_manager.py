import json
import os
from datetime import datetime

class ContextManager:
    def __init__(self, state_path="data/system_state.json", context_path="data/live_context.md"):
        self.state_path = state_path
        self.context_path = context_path

    def get_full_context(self):
        with open(self.context_path, 'r') as f:
            md_context = f.read()
        with open(self.state_path, 'r') as f:
            json_state = json.load(f)
        return f"{md_context}\n\nTechnical State: {json.dumps(json_state)}"

    def update_state(self, key, value):
        with open(self.state_path, 'r') as f:
            state = json.load(f)
        state[key] = value
        state["last_update"] = datetime.now().isoformat()
        with open(self.state_path, 'w') as f:
            json.dump(state, f, indent=2)

    def log_decision(self, decision):
        self.update_state("last_decision", decision)
        # Aqui poderíamos enviar para um webhook do Discord para o canal #audit-log
        print(f"[AUDIT LOG] {decision}")
