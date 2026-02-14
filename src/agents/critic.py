
from .base import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Critic", role="QA")

    def process(self, task):
        self.log(f"Auditing: {task}")
        system_prompt = (
            "You are The Critic. Review the input for security flaws, logic errors, or risks. "
            "Be harsh but constructive."
        )
        return self.ask_brain(task, system_prompt)
