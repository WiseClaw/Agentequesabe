import os
import time
from litellm import completion

class GatewayRouter:
    def __init__(self):
        # Limites Máximos (90% do real para evitar 429)
        self.limits = {
            "gemini-flash": {"rpm": 1800, "tpm": 900000},
            "gemini-pro": {"rpm": 4, "tpm": 900000},
            "claude-sonnet": {"rpm": 45, "tpm": 36000},
            "openrouter": {"rpm": 50, "tpm": 100000},
            "local": {"rpm": 9999, "tpm": 9999999},
            "vision-local": {"rpm": 9999, "tpm": 9999999}
        }

        self.usage = {
            "gemini-flash": {"req": 0, "tok": 0, "reset": time.time()},
            "gemini-pro": {"req": 0, "tok": 0, "reset": time.time()},
            "claude-sonnet": {"req": 0, "tok": 0, "reset": time.time()},
            "openrouter": {"req": 0, "tok": 0, "reset": time.time()}
        }

    def is_high_stakes(self, prompt):
        critical_keywords = ["code", "refactor", "security", "audit", "architect", "swarm", "critical", "fix"]
        return any(k in prompt.lower() for k in critical_keywords) or len(prompt) > 3000

    def check_quota(self, key):
        now = time.time()
        if now - self.usage[key]["reset"] > 60:
            self.usage[key]["req"] = 0
            self.usage[key]["tok"] = 0
            self.usage[key]["reset"] = now

        limit = self.limits[key]
        current = self.usage[key]
        return current["req"] < limit["rpm"] and current["tok"] < limit["tpm"]

    def route_request(self, role, prompt):
        needs_cloud = self.is_high_stakes(prompt)
        failures = []

        # 1. Claude 3.5 Sonnet
        if needs_cloud and self.check_quota("claude-sonnet"):
            res = self.call_api("claude-3-5-sonnet-20240620", prompt, "claude-sonnet")
            if res: return res
            failures.append("Claude 3.5 Sonnet")

        # 2. OpenRouter (DeepSeek V3)
        if needs_cloud and os.getenv("OPENROUTER_API_KEY") and self.check_quota("openrouter"):
            res = self.call_api("openrouter/deepseek/deepseek-chat", prompt, "openrouter")
            if res: 
                prefix = f"ℹ️ **[AVISO: Falha em {', '.join(failures)}. Recuperado via OpenRouter]**\n\n" if failures else ""
                return f"{prefix}{res}"
            failures.append("OpenRouter")

        # 3. Gemini 2.0 Flash
        if self.check_quota("gemini-flash"):
            res = self.call_api("gemini/gemini-2.0-flash", prompt, "gemini-flash")
            if res: 
                prefix = f"ℹ️ **[AVISO: Falha em {', '.join(failures)}. Recuperado via Gemini]**\n\n" if failures else ""
                return f"{prefix}{res}"
            failures.append("Gemini 2.0 Flash")

        # 4. Soberania Local (Ollama)
        print(f"[Router] Soberania Local Ativada: Processando via Ollama.")
        for model in ["ollama/llama3.1:8b", "ollama/qwen2.5:7b", "ollama/phi3:mini"]:
            res = self.call_api(model, prompt, "local")
            if res: 
                fail_msg = f" após falha em {', '.join(failures)}" if failures else ""
                return f"⚠️ **[MODO DE EMERGÊNCIA - MODELO LOCAL ({model}){fail_msg}]**\n\n{res}"

        return "🚨 ERRO CRÍTICO: Falha em todos os níveis de inteligência."

    def call_api(self, model, prompt, key):
        try:
            api_key = os.getenv("GOOGLE_API_KEY") if "gemini" in model else                       os.getenv("ANTHROPIC_API_KEY") if "claude" in model else                       os.getenv("OPENROUTER_API_KEY") if "openrouter" in model else None

            base_url = "http://localhost:11434" if "ollama" in model else None

            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                api_key=api_key,
                base_url=base_url,
                timeout=60
            )

            if key in self.usage:
                self.usage[key]["req"] += 1
                self.usage[key]["tok"] += response.usage.total_tokens

            return response.choices[0].message.content
        except Exception as e:
            print(f"[Router] Erro em {model}: {str(e)[:50]}")
            return None
