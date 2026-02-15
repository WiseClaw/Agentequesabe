import os
import sys
import json
import time
from datetime import datetime

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from src.gateway.router import GatewayRouter
    from src.librarian.query import Librarian
    from src.memory.context_manager import get_live_context
except ImportError:
    GatewayRouter = None
    Librarian = None
    get_live_context = lambda: "" # Fallback

STATE_FILE = "data/system_state.json"

class BaseAgent:
    def __init__(self, name, role, model="gpt-4-turbo"):
        self.name = name
        self.role = role
        self.model = model
        self.router = GatewayRouter() if GatewayRouter else None
        self.librarian = Librarian() if Librarian else None

    def update_state(self, status, task="None"):
        """Updates the central system state JSON for the dashboard."""
        if not os.path.exists(STATE_FILE):
            return
        
        try:
            with open(STATE_FILE, "r+") as f:
                state = json.load(f)
                
                if "agents" not in state:
                    state["agents"] = {}
                
                if self.name not in state["agents"]:
                    state["agents"][self.name] = {}
                
                state["agents"][self.name].update({
                    "status": status,
                    "current_task": task,
                    "model": self.model,
                    "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Update global token usage (mock for now, real implementation later)
                # state["global_token_usage"] += 100 
                
                f.seek(0)
                json.dump(state, f, indent=4)
                f.truncate()
        except Exception as e:
            print(f"[STATE ERROR] Could not update state: {e}")

    def consult_memory(self, query, limit=3):
        self.update_state("Busy", f"Consulting memory: {query[:20]}...")
        if not self.librarian:
            self.update_state("Error", "Librarian missing")
            return "[MEMORY ERROR] Librarian not available."
        result = self.librarian.query(query, limit)
        self.update_state("Idle", "Memory consultation complete")
        return result

    def ask_brain(self, user_input, system_prompt, use_memory=False):
        self.update_state("Busy", f"Processing: {user_input[:30]}...")
        
        if not self.router:
            self.update_state("Error", "Router missing")
            return "[ERROR] Neural Link (Gateway) broken."

        # 1. Get Live Context (Short-Term Shared Memory)
        live_context = get_live_context()

        # 2. Determine Role & Caching Strategy
        role_key = "fast"
        use_caching = False

        if "Manager" in self.name:
            role_key = "manager"
            use_caching = True
        elif "Researcher" in self.name:
            role_key = "researcher"
        elif "Coder" in self.name:
            role_key = "coder"
            use_caching = True
        elif "Critic" in self.name or "Auditor" in self.name:
            role_key = "auditor"
        elif "Operator" in self.name:
            role_key = "operator"
            use_caching = True

        # 3. Construct Final System Prompt
        final_prompt = str(live_context) + "\n\n" + str(system_prompt)

        if use_memory:
            memory_context = self.consult_memory(user_input)
            final_prompt += "\n\n[LONG-TERM MEMORY CONTEXT]\n" + str(memory_context) + "\n[END MEMORY]"

        # Route the request
        response = self.router.route_request(user_input, system_prompt=final_prompt, role=role_key, use_caching=use_caching)
        
        self.update_state("Idle", "Task complete")
        return response

    def process(self, task):
        raise NotImplementedError("Subclasses must implement process()")

    def log(self, message):
        print(f"[{self.name}] {message}", flush=True)
