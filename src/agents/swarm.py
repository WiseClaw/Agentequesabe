import json
from .manager import ManagerAgent
from .researcher import ResearcherAgent
from .critic import CriticAgent
from .coder import CoderAgent

class SwarmOrchestrator:
    def __init__(self):
        self.manager = ManagerAgent()
        self.researcher = ResearcherAgent()
        self.critic = CriticAgent()
        self.coder = CoderAgent()

    def run_brainstorm(self, task):
        print(f"[Swarm] Iniciando Brainstorm para: {task}")
        
        # Passo 1: Pesquisa (Researcher)
        research = self.researcher.process(f"Pesquisa técnica sobre: {task}")
        
        # Passo 2: Proposta Inicial (Manager + Research)
        proposal = self.manager.ask_brain("Proposal", f"Com base nesta pesquisa: {research}, propõe uma solução para: {task}")
        
        # Passo 3: Crítica (Critic)
        critique = self.critic.ask_brain("Critique", f"Critica esta proposta de forma rigorosa: {proposal}")
        
        # Passo 4: Refinamento Final (Manager)
        final_plan = self.manager.ask_brain("Final Plan", f"Refina a proposta considerando a crítica: {critique}. Proposta original: {proposal}")
        
        return {
            "task": task,
            "research": research,
            "proposal": proposal,
            "critique": critique,
            "final_plan": final_plan
        }
