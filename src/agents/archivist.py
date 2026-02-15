import json
import os
from .base import BaseAgent

class ArchivistAgent(BaseAgent):
    def __init__(self):
        super().__init__("Archivist", "Especialista em gestão de conhecimento e grafos de memória.")
        self.graph_path = "data/knowledge_graph.json"

    def update_graph(self, source, target, relation):
        if not os.path.exists(self.graph_path):
            data = {"nodes": [], "edges": []}
        else:
            with open(self.graph_path, 'r') as f:
                data = json.load(f)

        # Adicionar nós se não existirem
        node_ids = [n['id'] for n in data['nodes']]
        if source not in node_ids:
            data['nodes'].append({"id": source, "label": source, "group": "concept"})
        if target not in node_ids:
            data['nodes'].append({"id": target, "label": target, "group": "concept"})

        # Adicionar aresta
        data['edges'].append({"from": source, "to": target, "label": relation})

        with open(self.graph_path, 'w') as f:
            json.dump(data, f, indent=4)
        return f"Grafo atualizado: {source} --({relation})--> {target}"

    def process(self, task):
        # Lógica simplificada para extrair relações (em produção usaria LLM)
        return f"Archivist processando: {task}. Relações mapeadas no Grafo de Conhecimento."
