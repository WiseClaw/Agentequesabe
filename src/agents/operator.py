import sys
import os
from .base import BaseAgent

class OperatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="The Operator", role="Action & Execution", model="claude-3-5-sonnet")

    def process(self, task):
        self.log(f"Engaging with task: {task}")

        # System Prompt with Context Caching enabled in BaseAgent
        system_prompt = (
            "You are The Operator, an elite AI agent capable of complex execution. "
            "You have access to advanced tools and a high-context memory. "
            "Your goal is to execute tasks with precision. "
            "\n\nCAPABILITIES:"
            "\n- Context Caching is ACTIVE: You remember extensive instructions efficiently."
            "\n- Model Context Protocol (MCP): You can connect to external tools standardly."
        )

        return self.ask_brain(task, system_prompt)
