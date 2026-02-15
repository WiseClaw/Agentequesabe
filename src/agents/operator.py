from .base import BaseAgent
class OperatorAgent(BaseAgent):
    def __init__(self, name="Operator", model="claude-3-5-sonnet-20240620"):
        super().__init__(name=name, role="System Operator", model=model)
        self.system_prompt = "You are the Operator. You execute system commands via JSON actions."
