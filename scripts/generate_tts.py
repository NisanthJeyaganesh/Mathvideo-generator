import pyttsx3
import os

def generate_tts(text, audio_path):
    text = text.strip()
    if not text:
        raise ValueError("❗ Text for TTS is empty.")
    
    folder = os.path.dirname(audio_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    print(f"🗣️ Generating offline TTS for: '{text}'")

    engine = pyttsx3.init()
    engine.save_to_file(text, audio_path)
    engine.runAndWait()

    print(f"✅ Audio saved to: {audio_path}")
