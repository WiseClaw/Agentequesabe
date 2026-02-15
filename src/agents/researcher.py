import json
import os
from .base import BaseAgent

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("Researcher", "Especialista em investigação profunda e síntese de dados via MCP Search.")

    def perform_search(self, query):
        """Interface para o Search MCP Server"""
        from src.mcp.search_server import web_search
        print(f"[Researcher] Iniciando pesquisa web para: {query}")
        results = web_search(query, max_results=3)
        return results

    def process(self, task):
        # Se a tarefa parecer uma pergunta de pesquisa, executa a busca
        if any(word in task.lower() for word in ["quem", "o que", "como", "pesquisa", "search"]):
            results = self.perform_search(task)
            summary = f"Resultados da pesquisa para '{task}':\n" + json.dumps(results, indent=2)
            return self.ask_brain("Research Synthesis", f"Sintetize estes resultados: {summary}")
        return self.ask_brain("Research", task)
