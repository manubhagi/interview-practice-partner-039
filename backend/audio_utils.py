import whisper
from gtts import gTTS
import os
import uuid

# Load Whisper model (small is good balance of speed/accuracy)
# We use a global variable but load it lazily
model = None

def load_whisper():
    global model
    if model is None:
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        print("Whisper model loaded.")
    return model

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes audio file to text using Whisper.
    """
    try:
        # Ensure model is loaded
        _model = load_whisper()
        result = _model.transcribe(file_path)
        return result["text"].strip()
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""

def text_to_speech(text: str, output_path: str):
    """
    Converts text to speech using gTTS and saves to file.
    """
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
    except Exception as e:
        print(f"Error generating speech: {e}")
