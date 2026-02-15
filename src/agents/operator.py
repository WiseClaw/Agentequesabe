from .base import BaseAgent
import subprocess
import json

class OperatorAgent(BaseAgent):
    def __init__(self, name="Operator", model="claude-3-5-sonnet-20240620"):
        super().__init__(name=name, role="System Operator", model=model)
        self.system_prompt = (
            "You are the Operator. You execute system commands.\n"
            "You have access to the terminal.\n"
            "Output JSON actions: {\"action\": \"run_command\", \"command\": \"ls -la\"}"
        )
    
    # ... (Existing process method logic would be here, keeping it simple for update)
