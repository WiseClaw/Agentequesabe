import json
import os
import requests
import base64
from .base import BaseAgent

class OperatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Operator", "Especialista em execução de ferramentas, operações de sistema e visão local.")
        self.mcp_tools = ["list_directory", "read_file", "write_file", "analyze_image_local"]

    def analyze_image_local(self, image_path, prompt="Descreve esta imagem."):
        try:
            with open(image_path, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "moondream",
                    "prompt": prompt,
                    "images": [img_base64],
                    "stream": False
                }
            )
            return response.json().get("response", "Erro na análise visual local.")
        except Exception as e:
            return f"Erro na visão local: {str(e)}"

    def process(self, task):
        if "imagem" in task.lower() or "ver" in task.lower():
            return f"Operator: Iniciando análise visual soberana via Moondream para: {task}"
        return f"Operator executando tarefa técnica: {task}"

from src.agents.visual_module import VisualOperator
