import os
from gtts import gTTS

class TextToSpeech:
    def __init__(self):
        pass

    def generate_audio(self, text: str, output_path: str = "temp_response.mp3") -> str:
        """
        Converts text to speech and saves it as an MP3 file.
        Returns the path to the generated audio file.
        """
        if not text:
            return ""
            
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        return output_path
