import os
import json
import re
from huggingface_hub import InferenceClient
from src.prompts.system_prompts import EVALUATOR_PROMPT

class EvaluatorAgent:
    def __init__(self, model_repo="meta-llama/Meta-Llama-3-8B-Instruct"):
        self.client = InferenceClient(
            model=model_repo,
            token=os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        )

    def evaluate(self, role: str, question: str, answer: str) -> dict:
        prompt_content = EVALUATOR_PROMPT.format(
            role=role,
            question=question,
            answer=answer
        )
        
        messages = [
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": "Please evaluate the candidate's answer and return the EXACT JSON object."}
        ]

        response = self.client.chat_completion(
            messages=messages,
            max_tokens=256,
            temperature=0.1
        )
        
        return self._parse_json(response.choices[0].message.content)

    def _parse_json(self, text: str) -> dict:
        # Try to find JSON block using regex if there's surrounding text
        match = re.search(r'\{.*\}', text.strip(), re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            json_str = text.strip()
            
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback structure if parsing fails completely
            return {
                "clarity": 5,
                "technical_depth": 5,
                "confidence": 5,
                "feedback": "Failed to parse evaluator response."
            }
