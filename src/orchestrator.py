import json
from src.agents.interviewer import InterviewerAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.coach import CoachAgent

class InterviewOrchestrator:
    def __init__(self):
        self.interviewer = InterviewerAgent()
        self.evaluator = EvaluatorAgent()
        self.coach = CoachAgent()

    def generate_first_question(self, role: str, background: str, focus: str) -> str:
        return self.interviewer.generate_question(
            role=role,
            background=background,
            focus=focus,
            history="",
            feedback=""
        )

    def process_turn(self, role: str, background: str, focus: str, question: str, answer: str, history_list: list) -> tuple:
        # 1. Evaluate the answer
        evaluation = self.evaluator.evaluate(role, question, answer)
        feedback_str = json.dumps(evaluation)

        # 2. Build history string for the interviewer
        history_str = ""
        for item in history_list:
            history_str += f"Interviewer: {item['question']}\nCandidate: {item['answer']}\n\n"
        
        # Add the current turn to history string
        history_str += f"Interviewer: {question}\nCandidate: {answer}\n\n"

        # 3. Generate next question
        next_question = self.interviewer.generate_question(
            role=role,
            background=background,
            focus=focus,
            history=history_str.strip(),
            feedback=feedback_str
        )

        return next_question, evaluation

    def get_final_feedback(self, role: str, focus: str, history_list: list) -> str:
        transcript = ""
        for item in history_list:
            transcript += f"Interviewer: {item['question']}\nCandidate: {item['answer']}\n"
            if 'evaluation' in item and item['evaluation']:
                transcript += f"Evaluator feedback: {json.dumps(item['evaluation'])}\n"
            transcript += "\n"
            
        return self.coach.generate_feedback(role, focus, transcript.strip())
