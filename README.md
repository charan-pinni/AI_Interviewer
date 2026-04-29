# 🎯 AI Mock Interview Coach

The AI Mock Interview Coach is an intelligent, multi-agent conversational system built with Streamlit and powered by Hugging Face's Llama 3. It simulates realistic, adaptive mock interviews for any professional role and provides detailed feedback to help candidates improve.

## ✨ Features

- **Multi-Agent Architecture**: 
  - 🗣️ **Interviewer Agent**: Asks context-aware questions and dynamically adapts the difficulty based on your previous answers.
  - 📊 **Evaluator Agent**: Analyzes each response for clarity, technical depth, and confidence.
  - 🏆 **Coach Agent**: Generates a comprehensive final feedback report with actionable advice.
- **Audio Mode**: Speak naturally! Uses local `faster-whisper` for lightning-fast Speech-to-Text transcription and `gTTS` for Text-to-Speech, allowing you to conduct the interview hands-free.
- **Dynamic Progression**: Starts with foundational questions and increases complexity based on your performance.
- **Customizable Interviews**: Tailor the target role, provide a background summary, and choose the interview focus (Technical, Behavioral, or Mixed).

## 🔄 High-Level Flow

```text
User (Speech/Text)
   ↓
Speech-to-Text (ASR - Whisper)
   ↓
Orchestrator (Flow Controller)
   ↓
Multi-Agent System
   ├── 🎤 Interviewer Agent
   ├── 🧠 Evaluator Agent
   └── 🧑‍🏫 Coach Agent
   ↓
Response (Text)
   ↓
Text-to-Speech (TTS)
   ↓
Audio Output
```

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed on your machine.

### 1. Installation

Clone this repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory of the project and add your Hugging Face API token:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```
*(Note: Ensure you have access to `meta-llama/Meta-Llama-3-8B-Instruct` on Hugging Face).*

### 3. Run the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

## 🎙️ Using Audio Mode

1. Open the application in your browser (`http://localhost:8501`).
2. Configure your interview settings in the sidebar.
3. Toggle **Enable Audio Mode 🎙️** to ON.
4. Click **Start Interview**. The AI will speak its questions out loud.
5. Click the **Record Answer** microphone icon to speak your answer, and click it again to stop. The system will automatically transcribe your speech and continue the interview!

## 📁 Project Structure

```
AI_Interviewer/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not tracked)
├── src/
│   ├── orchestrator.py         # Manages the flow between agents
│   ├── agents/
│   │   ├── interviewer.py      # Generates questions
│   │   ├── evaluator.py        # Scores user answers
│   │   └── coach.py            # Generates final reports
│   ├── audio/
│   │   ├── asr.py              # Speech-to-Text (faster-whisper)
│   │   └── tts.py              # Text-to-Speech (gTTS)
│   └── prompts/
│       └── system_prompts.py   # Core instructions for the LLMs
```
