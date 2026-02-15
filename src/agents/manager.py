from .base import BaseAgent
from .coder import CoderAgent
from .sentinel import SentinelAgent
from .qa import QAAgent
import json
import re

class ManagerAgent(BaseAgent):
    def __init__(self, name="Manager", model="claude-3-5-sonnet-20240620"):
        super().__init__(name=name, role="Product Owner", model=model)
        self.coder = CoderAgent()
        self.sentinel = SentinelAgent()
        self.qa = QAAgent()
        self.system_prompt = (
            "You are the Product Owner and Orchestrator.\n"
            "You manage the lifecycle of tasks using the 'War Room' workflow.\n"
            "1. Delegate to Coder (TDD).\n"
            "2. Audit with Sentinel.\n"
            "3. Test with QA.\n"
            "4. Report results."
        )

    def execute_task(self, task: str) -> str:
        # 1. Coding Phase
        print(f"[Manager] Delegating to Coder: {task[:30]}...")
        coder_resp = self.coder.process(f"Implement this task using TDD (JSON output): {task}")
        
        # Parse JSON from Coder
        try:
            # Extract JSON block if wrapped in markdown
            json_match = re.search(r"```json\n(.*?)\n```", coder_resp, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(1))
            else:
                data = json.loads(coder_resp)
            
            code_content = data.get("code", "")
            test_content = data.get("test", "")
        except Exception as e:
            return f"❌ Coder Output Error: Could not parse JSON. {str(e)}\nRaw: {coder_resp[:100]}..."

        # 2. Security Audit
        print("[Manager] Requesting Security Audit...")
        audit = self.sentinel.audit_code(code_content)
        if audit['status'] == 'RISK':
            return f"❌ Security Audit Failed: {audit['report']}"
            
        # 3. QA Testing
        print("[Manager] Requesting QA Testing...")
        qa_result = self.qa.run_test_cycle(code_content, test_content)
        
        return f"✅ Task Completed.\n\nSecurity: {audit['status']}\nQA Result:\n{qa_result}"
