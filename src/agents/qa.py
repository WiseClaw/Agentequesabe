import subprocess
import os
from .base import BaseAgent

class QAAgent(BaseAgent):
    def __init__(self):
        super().__init__("QA", "Quality Assurance Engineer - Test Specialist.")
        self.sandbox_dir = "code_textbox"

    def process(self, code_context):
        self.ctx_mgr.log_decision("QA Agent starting test execution in sandbox.")
        
        test_file = os.path.join(self.sandbox_dir, "test_candidate.py")
        if not os.path.exists(test_file):
            return "QA Status: FAILED\nReport: test_candidate.py not found."

        try:
            result = subprocess.run(
                ["pytest", test_file],
                capture_output=True, text=True, timeout=30
            )
            status = "PASSED" if result.returncode == 0 else "FAILED"
            report = result.stdout + "\n" + result.stderr
        except Exception as e:
            status = "ERROR"
            report = str(e)

        self.ctx_mgr.update_state("last_qa_status", status)
        return f"QA Status: {status}\nReport:\n{report}"
