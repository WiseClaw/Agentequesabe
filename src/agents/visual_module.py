
import subprocess
import json

class VisualOperator:
    def analyze_image(self, image_path, prompt="Descreve esta imagem para um sistema de agentes."):
        print(f"👁️ Analisando imagem: {image_path}")
        try:
            # Usando Moondream via Ollama para análise local
            cmd = ['ollama', 'run', 'moondream', f"{prompt} [IMAGE: {image_path}]"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Erro na análise visual: {e}"
