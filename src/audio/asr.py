import os
from faster_whisper import WhisperModel

class SpeechRecognizer:
    def __init__(self, model_size="tiny", device="cpu"):
        # You can change model_size to "base" or "small" for better accuracy, 
        # but "tiny" is faster for local CPU inference.
        # Download happens on first run automatically.
        self.model = WhisperModel(model_size, device=device, compute_type="int8")

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes the given audio file and returns the text.
        """
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        text = ""
        for segment in segments:
            text += segment.text + " "
            
        return text.strip()
