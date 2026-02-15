import os
from src.gateway.router import GatewayRouter
from src.memory.context_manager import ContextManager
from src.librarian.query import query_memory
from src.librarian.ingest import ingest_text

class BaseAgent:
    def __init__(self, role, description):
        self.role = role
        self.description = description
        self.router = GatewayRouter()
        self.ctx_mgr = ContextManager()

    def get_context(self):
        return self.ctx_mgr.get_full_context()

    def ask_brain(self, task_type, prompt):
        context = self.get_context()
        # Busca na Memória de Longo Prazo (ChromaDB)
        long_term_mem = query_memory(prompt, n_results=3)
        
        full_prompt = f"""
        Role: {self.role}
        Context: {context}
        Memory: {long_term_mem}
        Task: {prompt}
        """
        response = self.router.route_request(self.role, full_prompt)
        
        # Ingestão Automática: O que acontece agora vira memória instantânea
        ingest_text(f"[{self.role}] Task: {prompt} | Response: {response}")
        
        return response

    def process(self, user_input):
        return self.ask_brain("General", user_input)
