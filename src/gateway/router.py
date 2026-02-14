import os
from litellm import completion

class GatewayRouter:
    def __init__(self):
        # 2026 SOTA Configuration
        self.models = {
            # Manager: Claude 3.5 Sonnet (Reliable & Fast)
            "manager": "claude-3-5-sonnet-20241022",

            # Coder: Claude 3.5 Sonnet (Best for Code)
            "coder": "claude-3-5-sonnet-20241022",

            # Researcher: GEMINI 3 PRO PREVIEW (The Beast)
            "researcher": "gemini/gemini-3-pro-preview",

            # Auditor: GPT-4o (Logic Check)
            "auditor": "gpt-4o",

            # Operator: Claude 3.5 Sonnet (Computer Use)
            "operator": "claude-3-5-sonnet-20241022",

            "fast": "gpt-4o-mini"
        }

    def route_request(self, user_prompt, system_prompt=None, role="fast", use_caching=False):
        # Select Model based on Role
        model = self.models.get(role, self.models["fast"])

        messages = []

        # Handle System Prompt & Caching (Anthropic Only)
        if system_prompt:
            if use_caching and "claude" in model:
                messages.append({
                    "role": "system",
                    "content": [
                        {
                            "type": "text", 
                            "text": system_prompt,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                })
            else:
                messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_prompt})

        # API Key Handling
        api_key = None
        if "claude" in model:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        elif "gemini" in model:
            api_key = os.getenv("GOOGLE_API_KEY")
        elif "gpt" in model:
            api_key = os.getenv("OPENAI_API_KEY")

        try:
            response = completion(
                model=model,
                messages=messages,
                api_key=api_key
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[GATEWAY ERROR] {str(e)}"
