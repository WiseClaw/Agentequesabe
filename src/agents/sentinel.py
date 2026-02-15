import subprocess
import re
import os
from .base import BaseAgent

class SentinelAgent(BaseAgent):
    def __init__(self, name="Sentinel", model="gpt-4o"):
        super().__init__(name=name, role="Security Auditor", model=model)
        self.system_prompt = (
            "You are the Sentinel. Your mission is to PROTECT the system.\n"
            "You analyze code for security vulnerabilities, hardcoded secrets, and dangerous commands.\n"
            "You NEVER execute code. You only AUDIT it.\n"
            "Rules:\n"
            "1. Block any code with hardcoded API keys (sk-...).\n"
            "2. Block 'rm -rf', 'shutil.rmtree' or destructive file system commands.\n"
            "3. Recommend 'bandit' scans for Python code."
        )

    def audit_code(self, code_content: str) -> dict:
        """
        Runs static analysis on the code.
        Returns {'status': 'SAFE'|'RISK', 'report': str}
        """
        # 1. Regex Check for Secrets
        if re.search(r"(sk-[a-zA-Z0-9]{48})", code_content):
            return {"status": "RISK", "report": "CRITICAL: Hardcoded OpenAI Key detected."}
        
        # 2. Dangerous Commands
        if "rm -rf" in code_content or "shutil.rmtree" in code_content:
            return {"status": "RISK", "report": "WARNING: Destructive command detected."}

        # 3. Bandit Scan
        temp_file = "temp_audit.py"
        try:
            with open(temp_file, "w") as f:
                f.write(code_content)
            
            # Run bandit (security linter)
            result = subprocess.run(
                ["bandit", "-r", temp_file, "-f", "json"],
                capture_output=True,
                text=True
            )
            
            # Bandit returns exit code 1 if issues are found
            if result.returncode != 0:
                 return {"status": "RISK", "report": f"Bandit Security Scan found issues:\n{result.stdout}"}
                 
        except Exception as e:
            return {"status": "ERROR", "report": str(e)}
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        return {"status": "SAFE", "report": "Code passed static analysis."}
