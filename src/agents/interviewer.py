import os
from huggingface_hub import InferenceClient
from src.prompts.system_prompts import INTERVIEWER_PROMPT

class InterviewerAgent:
    def __init__(self, model_repo="meta-llama/Meta-Llama-3-8B-Instruct"):
        self.client = InferenceClient(
            model=model_repo,
            token=os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        )

    def generate_question(self, role: str, background: str, focus: str, history: str, feedback: str) -> str:
        prompt_content = INTERVIEWER_PROMPT.format(
            role=role,
            background=background,
            focus=focus,
            history=history,
            feedback=feedback if feedback else "None (Start of interview)"
        )
        
        messages = [
            {"role": "system", "content": prompt_content},
            {"role": "user", "content": "Please generate the next interview question based on the instructions."}
        ]
        
        response = self.client.chat_completion(
            messages=messages,
            max_tokens=256,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
