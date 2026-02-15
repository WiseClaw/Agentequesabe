from .base import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("Critic", "Compliance Auditor & Strategic Critic - Challenges assumptions.")

    def process(self, proposal):
        prompt = f"""
        Critique the following proposal/plan. Identify risks, logical fallacies, and compliance issues with the Constitution.
        Proposal: {proposal}
        
        Provide a 'Red Team' perspective to improve the final result.
        """
        return self.ask_brain("Critique", prompt)
