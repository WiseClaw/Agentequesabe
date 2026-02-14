import os
import sys

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from src.gateway.router import GatewayRouter
except ImportError:
    GatewayRouter = None

class BaseAgent:
    def __init__(self, name, role, model="gpt-4-turbo"):
        self.name = name
        self.role = role
        self.router = GatewayRouter() if GatewayRouter else None

    def ask_brain(self, user_input, system_prompt):
        if not self.router:
            return "[ERROR] Neural Link (Gateway) broken."

        # Determine Role & Caching Strategy
        role_key = "fast"
        use_caching = False

        if "Manager" in self.name:
            role_key = "manager"
            use_caching = True # Cache project context
        elif "Researcher" in self.name:
            role_key = "researcher"
        elif "Coder" in self.name:
            role_key = "coder"
            use_caching = True # Cache coding standards/docs
        elif "Critic" in self.name or "Auditor" in self.name:
            role_key = "auditor"
        elif "Operator" in self.name:
            role_key = "operator"
            use_caching = True

        # Route the request
        return self.router.route_request(user_input, system_prompt=system_prompt, role=role_key, use_caching=use_caching)

    def process(self, task):
        raise NotImplementedError("Subclasses must implement process()")

    def log(self, message):
        print(f"[{self.name}] {message}", flush=True)
