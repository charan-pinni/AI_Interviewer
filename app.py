import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

from src.orchestrator import InterviewOrchestrator

st.set_page_config(page_title="AI Mock Interview Coach", page_icon="🎯", layout="wide")

@st.cache_resource
def get_audio_models():
    from src.audio.asr import SpeechRecognizer
    from src.audio.tts import TextToSpeech
    return SpeechRecognizer(), TextToSpeech()

def init_session_state():
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = InterviewOrchestrator()
    if "history" not in st.session_state:
        st.session_state.history = []  # List of dicts: {role: 'interviewer'/'user', content: str, evaluation: dict, audio_path: str}
    if "current_question" not in st.session_state:
        st.session_state.current_question = ""
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "turn_count" not in st.session_state:
        st.session_state.turn_count = 0
    if "final_feedback" not in st.session_state:
        st.session_state.final_feedback = ""

init_session_state()

st.title("🎯 AI Mock Interview Coach")

# Sidebar Configuration
with st.sidebar:
    st.header("Interview Setup")
    role = st.text_input("Target Role", value="Software Engineer", placeholder="e.g., Data Analyst, Product Manager")
    background = st.text_area("Background / Resume Summary", placeholder="e.g., 3 years of experience in Python, specialized in backend development.")
    focus = st.selectbox("Interview Focus", ["Technical", "Behavioral", "Mixed"])
    max_turns = st.slider("Number of Questions", 3, 10, 5)
    
    st.divider()
    audio_mode = st.toggle("Enable Audio Mode 🎙️", value=False, help="Use speech-to-text and text-to-speech.")

    if st.button("Start Interview"):
        st.session_state.history = []
        st.session_state.turn_count = 0
        st.session_state.final_feedback = ""
        st.session_state.interview_active = True
        
        with st.spinner("Generating opening question..."):
            first_q = st.session_state.orchestrator.generate_first_question(role, background, focus)
            st.session_state.current_question = first_q
            
            msg_data = {"role": "interviewer", "content": first_q}
            
            if audio_mode:
                _, tts = get_audio_models()
                audio_file = tts.generate_audio(first_q, output_path=f"q_0.mp3")
                msg_data["audio_path"] = audio_file
                
            st.session_state.history.append(msg_data)

# Main Chat Interface
if st.session_state.interview_active:
    st.markdown("### Interview Session")
    
    # Display Chat History
    for i, msg in enumerate(st.session_state.history):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
            if audio_mode and msg["role"] == "interviewer" and msg.get("audio_path"):
                is_last = (i == len(st.session_state.history) - 1)
                st.audio(msg["audio_path"], autoplay=is_last)
                
            # Display evaluation if it exists for user messages
            if msg["role"] == "user" and "evaluation" in msg and msg["evaluation"]:
                with st.expander("Evaluator Feedback (Internal)"):
                    st.json(msg["evaluation"])
                    
    # Handle User Input
    if st.session_state.turn_count < max_turns:
        user_answer = None
        
        if audio_mode:
            st.info("🎙️ Audio Mode: Please record your answer below.")
            audio_value = st.audio_input("Record Answer", key=f"audio_input_{st.session_state.turn_count}")
            
            if audio_value:
                with st.spinner("Transcribing your answer..."):
                    asr, _ = get_audio_models()
                    temp_audio_path = f"temp_user_{st.session_state.turn_count}.wav"
                    with open(temp_audio_path, "wb") as f:
                        f.write(audio_value.getbuffer())
                    
                    user_answer = asr.transcribe(temp_audio_path)
                    
                    if not user_answer:
                        st.warning("Could not hear you clearly. Please try again or use text.")
                        user_answer = None
        else:
            user_answer = st.chat_input("Type your answer here...")
            
        if user_answer:
            # Display user answer
            with st.chat_message("user"):
                st.write(user_answer)
                
            with st.spinner("Evaluating and generating next question..."):
                # Prepare history for orchestrator
                orch_history = []
                for i in range(0, len(st.session_state.history) - 1, 2):
                    if i + 1 < len(st.session_state.history):
                        q = st.session_state.history[i]["content"]
                        a = st.session_state.history[i+1]["content"]
                        eval_data = st.session_state.history[i+1].get("evaluation", {})
                        orch_history.append({"question": q, "answer": a, "evaluation": eval_data})

                # Process Turn
                next_q, evaluation = st.session_state.orchestrator.process_turn(
                    role=role,
                    background=background,
                    focus=focus,
                    question=st.session_state.current_question,
                    answer=user_answer,
                    history_list=orch_history
                )
                
                # Update history with answer and evaluation
                st.session_state.history.append({
                    "role": "user", 
                    "content": user_answer,
                    "evaluation": evaluation
                })
                
                st.session_state.turn_count += 1
                
                if st.session_state.turn_count < max_turns:
                    # Add next question
                    st.session_state.current_question = next_q
                    msg_data = {"role": "interviewer", "content": next_q}
                    
                    if audio_mode:
                        _, tts = get_audio_models()
                        audio_file = tts.generate_audio(next_q, output_path=f"q_{st.session_state.turn_count}.mp3")
                        msg_data["audio_path"] = audio_file
                        
                    st.session_state.history.append(msg_data)
                    st.rerun()
                else:
                    st.session_state.interview_active = False
                    st.rerun()

# End of Interview / Final Feedback
if not st.session_state.interview_active and st.session_state.turn_count >= max_turns:
    st.success("Interview Completed!")
    
    if not st.session_state.final_feedback:
        with st.spinner("Coach is preparing your final feedback report..."):
            orch_history = []
            for i in range(0, len(st.session_state.history) - 1, 2):
                if i + 1 < len(st.session_state.history):
                    q = st.session_state.history[i]["content"]
                    a = st.session_state.history[i+1]["content"]
                    eval_data = st.session_state.history[i+1].get("evaluation", {})
                    orch_history.append({"question": q, "answer": a, "evaluation": eval_data})
                    
            feedback = st.session_state.orchestrator.get_final_feedback(role, focus, orch_history)
            st.session_state.final_feedback = feedback
            
    st.markdown("### 🏆 Final Coach Report")
    st.markdown(st.session_state.final_feedback)
