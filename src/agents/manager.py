import json
import os
from .base import BaseAgent
from .archivist import ArchivistAgent

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Manager", "Orquestrador Central do WiseClaw OS.")
        self.archivist = ArchivistAgent()

    def process(self, task):
        # Antes de processar, o Manager pede ao Archivist para mapear a intenção
        print(f"[Manager] Solicitando mapeamento de conhecimento para: {task}")
        self.archivist.update_graph("User_Task", task[:20], "Solicita")
        
        # Lógica de orquestração (simplificada para o exemplo)
        response = self.ask_brain("Orchestration", f"Como devemos resolver esta tarefa: {task}?")
        return response
