import sys
import os

# Ensure we can import from src
sys.path.append(os.path.join(os.getcwd(), 'src'))

from offline import listener
from offline import commander
import executor
import speaker

def main():
    print("Initializing Offline Voice-Activated System...")
    
    # Initialize offline components
    try:
        ear = listener.OfflineListener()
        brain = commander.OfflineCommander()
    except Exception as e:
        print(f"Failed to initialize offline components: {e}")
        return

    speaker.speak("Offline system ready. Listening...")
    
    while True:
        try:
            # Listen (Offline)
            text = ear.listen()
            if text:
                # Understand (Offline Spacy)
                intent = brain.parse_command(text)
                
                # Execute (Standard)
                if intent and intent.get("action") != "unknown":
                    executor.execute(intent)
                else:
                    speaker.speak("I didn't understand.")
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            speaker.speak("An error occurred.")

if __name__ == "__main__":
    main()
