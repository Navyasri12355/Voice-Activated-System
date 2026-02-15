import pyttsx3

try:
    engine = pyttsx3.init()
    # Set properties (optional)
    engine.setProperty('rate', 170)  # Speed percent (can go over 100)
    engine.setProperty('volume', 1.0)  # Volume 0-1
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    engine = None

def speak(text):
    """Speaks the given text using pyttsx3."""
    if not text or not engine:
        return
    
    print(f"System: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speaker: {text} - {e}")

