# speech_engine.py
import pyttsx3

_engine = None

def _init_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine

def speak_text(text):
    engine = _init_engine()
    engine.say(text)
    engine.runAndWait()
