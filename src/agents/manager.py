
from .base import BaseAgent

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Manager", role="Orchestration")

    def process(self, task):
        self.log(f"Orchestrating: {task}")
        system_prompt = (
            "You are The Manager, the strategic leader of WiseClaw. "
            "Your goal is to break down the user's task into a clear plan. "
            "Identify which agent (Researcher, Coder, Critic) should handle what. "
            "Be authoritative and concise."
        )
        return self.ask_brain(task, system_prompt)
