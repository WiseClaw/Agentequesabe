import os
import re
from .base import BaseAgent

class CoderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Coder", "Claude Code Engineer - TDD Specialist.")
        self.sandbox_dir = "code_textbox"
        os.makedirs(self.sandbox_dir, exist_ok=True)

    def _extract_code(self, text, filename):
        pattern = rf"(?:### {filename}|// {filename}|# {filename})\s*\n```(?:python)?\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            match = re.search(r"```(?:python)?\n(.*?)\n```", text, re.DOTALL)
        return match.group(1) if match else ""

    def process(self, task_description):
        prompt = f"""
        Task: {task_description}
        Environment: Sandbox directory '{self.sandbox_dir}'.
        
        Instructions:
        1. Write the implementation in a python block starting with '# candidate.py'.
        2. Write the pytest tests in a python block starting with '# test_candidate.py'.
        3. Ensure the tests import the function from candidate.py.
        """
        response = self.ask_brain("Coding", prompt)
        
        impl_code = self._extract_code(response, "candidate.py")
        test_code = self._extract_code(response, "test_candidate.py")
        
        if impl_code:
            with open(os.path.join(self.sandbox_dir, "candidate.py"), "w") as f: f.write(impl_code)
        if test_code:
            with open(os.path.join(self.sandbox_dir, "test_candidate.py"), "w") as f: f.write(test_code)
            
        self.ctx_mgr.log_decision(f"Coder wrote files to {self.sandbox_dir}.")
        return response
