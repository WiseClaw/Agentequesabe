
from .base import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Coder", role="Development")

    def process(self, task):
        self.log(f"Coding: {task}")
        system_prompt = (
            "You are The Coder. Write clean, efficient code for the requested task. "
            "Always wrap code in markdown blocks (```). Explain the logic briefly."
        )
        return self.ask_brain(task, system_prompt)
