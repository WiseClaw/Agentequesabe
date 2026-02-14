class ModelRouter:
    def __init__(self):
        # Prices per 1M tokens (Example based on current market)
        self.models = {
            "cheap": {"name": "gpt-4o-mini", "cost_input": 0.15, "cost_output": 0.60},
            "sota": {"name": "gpt-4o", "cost_input": 5.00, "cost_output": 15.00},
            "local": {"name": "llama-3-local", "cost_input": 0.00, "cost_output": 0.00}
        }

    def route(self, task_complexity: str, prompt_length: int):
        # Decides which model to use based on complexity and length.
        # complexity: 'low', 'medium', 'high'

        if task_complexity == 'low':
            selected = self.models['cheap']
            reason = "Task is simple, optimizing for cost."
        elif task_complexity == 'medium' and prompt_length < 2000:
            selected = self.models['cheap']
            reason = "Medium task but short context, fitting for cheaper model."
        else:
            selected = self.models['sota']
            reason = "Complex task or long context, requires SOTA reasoning."

        return {
            "model": selected['name'],
            "reason": reason,
            "estimated_cost_per_1M_tokens": f"${selected['cost_input']}"
        }

if __name__ == "__main__":
    # Test the logic
    router = ModelRouter()
    print(f"[ROUTER] Testing Logic:")
    print(f"1. Simple Summary: {router.route('low', 500)}")
    print(f"2. Complex Architecture: {router.route('high', 3000)}")
