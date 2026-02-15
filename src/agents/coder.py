from .base import BaseAgent
import json

class CoderAgent(BaseAgent):
    def __init__(self, name="Coder", model="claude-3-5-sonnet-20240620"):
        super().__init__(name=name, role="Software Engineer", model=model)
        self.system_prompt = (
            "You are a Senior Software Engineer specializing in TDD.\n"
            "Your goal is to write robust, clean, and secure Python code.\n"
            "IMPORTANT: You must output a JSON object with two keys: 'code' and 'test'.\n"
            "Format:\n"
            "```json\n"
            "{\n"
            "  \"code\": \"def my_func(): ...\",\n"
            "  \"test\": \"def test_my_func(): ...\"\n"
            "}\n"
            "```\n"
            "Rules:\n"
            "1. Write the TEST first mentally, then the CODE.\n"
            "2. Use 'pytest' conventions.\n"
            "3. No markdown outside the JSON block if possible."
        )
