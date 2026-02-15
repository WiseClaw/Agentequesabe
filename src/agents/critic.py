from .base import BaseAgent
class CriticAgent(BaseAgent):
    def __init__(self, name="Auditor", model="gpt-4o"):
        super().__init__(name=name, role="Compliance Auditor", model=model)
        self.system_prompt = "You are the Auditor. Validate outputs against the Constitution."
