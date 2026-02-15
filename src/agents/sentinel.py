from .base import BaseAgent
import json

class SentinelAgent(BaseAgent):
    def __init__(self):
        super().__init__("Sentinel", "Security Gatekeeper and Governance Auditor.")
    
    def process(self, task_to_audit):
        prompt = f"""
        Audit the following task/code for security risks (malicious commands, key leaks, unsafe operations):
        {task_to_audit}
        
        Output format:
        STATUS: [SAFE/BLOCK]
        REASON: [Explanation]
        """
        return self.ask_brain("Security Audit", prompt)
