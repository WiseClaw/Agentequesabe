import subprocess
import os
from .base import BaseAgent

class QAAgent(BaseAgent):
    def __init__(self, name="QA_Engineer", model="claude-3-5-sonnet-20240620"):
        super().__init__(name=name, role="Quality Assurance", model=model)
        self.sandbox_dir = "/a0/usr/workdir/code_textbox"
        self.system_prompt = (
            "You are the QA Engineer (The Breaker).\n"
            "Your goal is to write TEST CASES for the provided code.\n"
            "You operate strictly within the 'code_textbox' directory.\n"
            "1. Receive code.\n"
            "2. Write the code to 'candidate.py'.\n"
            "3. Write a test file 'test_candidate.py' using pytest.\n"
            "4. Execute the test.\n"
            "5. Report PASS/FAIL."
        )

    def run_test_cycle(self, code_content: str, test_content: str) -> str:
        """
        Writes code and tests to sandbox, then runs pytest.
        """
        # Ensure sandbox exists
        os.makedirs(self.sandbox_dir, exist_ok=True)

        candidate_path = os.path.join(self.sandbox_dir, "candidate.py")
        test_path = os.path.join(self.sandbox_dir, "test_candidate.py")

        try:
            # Write files
            with open(candidate_path, "w") as f:
                f.write(code_content)
            with open(test_path, "w") as f:
                f.write(test_content)

            # Run pytest
            result = subprocess.run(
                ["pytest", "test_candidate.py"],
                cwd=self.sandbox_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout

        except Exception as e:
            return f"QA Execution Error: {str(e)}"
