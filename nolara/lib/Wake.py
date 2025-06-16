import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

# 🔁 Your wake word
WAKE_WORD = "Intelligence"

# 📞 Function to call
def on_wake_word():
    print("🧠 Wake word detected! Calling your function...")
    # Call your custom logic here
    # e.g., start_chat(), launch_app(), etc.

# 🧠 Load model
model = Model("vosk_models/vosk-model-small-en-us-0.15")  # Or your Hungarian model path
recognizer = KaldiRecognizer(model, 16000)

# 🎧 Audio input setup
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    q.put(bytes(indata))

def listen_for_wake_word():
    print(f"🎙️ Listening for '{WAKE_WORD}'...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if WAKE_WORD.lower() in text.lower():
                    on_wake_word()

if __name__ == "__main__":
    listen_for_wake_word()
