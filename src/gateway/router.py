import os
from litellm import completion

class GatewayRouter:
    def __init__(self):
        self.models = {
            "fast": "gpt-4o-mini",
            "smart": "claude-3-5-sonnet-20240620",
            "research": "gemini/gemini-1.5-pro-latest",
            "creative": "gpt-4o"
        }

    def route_request(self, agent_role: str, prompt: str, **kwargs):
        model_id = self.models["fast"]

        # High Intelligence Roles -> Claude 3.5 Sonnet
        if agent_role in ["Manager", "Coder", "Architect", "QA_Engineer", "Operator"]:
            model_id = self.models["smart"]
        # Research Roles -> Gemini (High Context)
        elif agent_role in ["Researcher", "Librarian"]:
            model_id = self.models["research"]
        # Audit/Creative Roles -> GPT-4o
        elif agent_role in ["Critic", "Auditor", "Sentinel"]:
            model_id = self.models["creative"]

        if "model" in kwargs and kwargs["model"]:
            model_id = kwargs["model"]

        try:
            response = completion(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Gateway Error ({model_id}): {str(e)}"
