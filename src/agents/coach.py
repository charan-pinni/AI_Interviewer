import os
from huggingface_hub import InferenceClient
from src.prompts.system_prompts import COACH_PROMPT

class CoachAgent:
    def __init__(self, model_repo="meta-llama/Meta-Llama-3-8B-Instruct"):
        self.client = InferenceClient(
            model=model_repo,
            token=os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        )

    def generate_feedback(self, role: str, focus: str, transcript: str) -> str:
        prompt_content = COACH_PROMPT.format(
            role=role,
            focus=focus,
            transcript=transcript
        )
        
        messages = [
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": "Please provide the final feedback report in Markdown format as requested."}
        ]

        response = self.client.chat_completion(
            messages=messages,
            max_tokens=512,
            temperature=0.6
        )
        
        return response.choices[0].message.content.strip()
