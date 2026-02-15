import speech_recognition as sr

def listen():
    """
    Listens for audio input from the microphone and returns the recognized text.
    Returns None if no valid speech is detected.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # timeout: max time to wait for speech to start
            # phrase_time_limit: max time to listen after speech starts
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio)
            print(f"Heard: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            pass # No speech detected within timeout
        except sr.UnknownValueError:
            pass # Speech was unintelligible
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error in listener: {e}")
    return None

