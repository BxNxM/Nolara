import speech_recognition as sr
from gtts import gTTS
from gtts.lang import tts_langs
import os
import platform
import shutil
from pathlib import Path

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
AUDIO_CACHE_DIR = os.path.join(SCRIPT_DIR, "../.audio_cache")
AUDIO_OUT_CACHE_FILE = os.path.join(AUDIO_CACHE_DIR, "speach_audio.mp3")
# Check if the directory exists, and create it if it doesn't
if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)

try:
    from . import Config
except ImportError:
    import Config


def play_audio_mac(file_path):
    """Plays an audio file on macOS using osascript."""
    try:
        os.system(f"open '{file_path}'")  # Simplified osascript command
    except Exception as e:
        print(f"Error playing audio on macOS: {e}")

def play_audio_linux(file_path):
    """Plays an audio file on Linux using mpg321."""
    try:
        os.system(f"mpg321 '{file_path}'")
    except Exception as e:
        print(f"Error playing audio on Linux: {e}")

def play_audio_windows(file_path):
    """Plays an audio file on Windows using the default media player."""
    try:
        os.system(f"start '{file_path}'")  # Use start for Windows
    except Exception as e:
        print(f"Error playing audio on Windows: {e}")


def play_audio_cross_platform(file_path):
    """
    Plays an audio file based on the operating system.
    """
    os_name = platform.system()
    if os_name == "Darwin":
        play_audio_mac(file_path)
    elif os_name == "Linux":
        play_audio_linux(file_path)
    elif os_name == "Windows":
        play_audio_windows(file_path)
    else:
        print(f"Unsupported operating system: {os_name}")


def gtts_lang(language):
    return language.split("-")[0]


def speech_to_text(language):
    """
    Converts speech to text using Google's Speech-to-Text API.
    """

    text = ""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        print(f"Please speak in {language}:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language=language)
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return text


def text_to_speech(text, language=None):
    """
    Converts text to speech using Google's Text-to-Speech API.
    """
    if language is None:
        language = Config.get("language") or "en-US"  # Default to English
    # Text-to-Speech
    remove_chars = ["*"]
    for char in remove_chars:
        text = text.replace(char, "")
    tts = gTTS(text=text, lang=gtts_lang(language), slow=False)
    tts.save(AUDIO_OUT_CACHE_FILE)
    play_audio_cross_platform(AUDIO_OUT_CACHE_FILE)  # Use cross-platform playback


def delete_audio_cache():
    # Delete from os player cache
    target_dir = Path.home() / "Music/Music/Media.localized/Music/Unknown Artist/Unknown Album"
    if target_dir.exists() and target_dir.is_dir():
        print(f"Scanning for .mp3 files under: {target_dir}")
        deleted = 0
        for mp3_file in target_dir.rglob("*.mp3"):
            try:
                mp3_file.unlink()
                print(f"Deleted: {mp3_file}")
                deleted += 1
            except Exception as e:
                print(f"Failed to delete {mp3_file}: {e}")
        print(f"Done. {deleted} .mp3 file(s) deleted.")
    else:
        print(f"Target path does not exist or is not a directory: {target_dir}")

    # Delete from project cache
    if os.path.exists(AUDIO_CACHE_DIR):
        shutil.rmtree(AUDIO_CACHE_DIR)
        return True
    return False


def echo_speech(language=None):
    """
    Listens for speech input, echoes it back via TTS.
    """
    if language is None:
        language = Config.get("language") or "en-US"  # Default to English
    text = speech_to_text(language)
    if text:
        text_to_speech(text, language)


def list_languages():
    print("[TTS] Text-to-speech languages (gTTS):")
    languages = tts_langs()
    for code, name in languages.items():
        print(f"{code}: {name}")
    print("[STT] Voice recognition languages (speech_recognition):\n\thttps://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages")


if __name__ == "__main__":
    list_languages()
    text_to_speech("Nollara")

    #echo_speech(language="en-US")
    #echo_speech(language="hu-HU")