import os
import webbrowser
import datetime
import speaker

def execute(intent):
    """Executes the action based on intent."""
    if not intent:
        return

    action = intent.get("action")
    target = intent.get("target")

    if action == "open":
        speaker.speak(f"Opening {target}")
        # Basic mapping for common apps, else try generic start
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "chrome": "start chrome",
            "edge": "start msedge"
        }
        
        # Fuzzy match or direct lookup could go here. For now, direct or os.system
        app_cmd = apps.get(target, None)
        if app_cmd:
            os.system(app_cmd)
        else:
            # Try to start it as a generic command
            try:
                os.startfile(target)
            except:
                speaker.speak(f"Could not find application {target}")

    elif action == "search":
        speaker.speak(f"Searching for {target}")
        webbrowser.open(f"https://www.google.com/search?q={target}")

    elif action == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        speaker.speak(f"The time is {now}")

    elif action == "exit":
        speaker.speak("Goodbye")
        exit()

    elif action == "unknown":
        speaker.speak("I didn't understand that command.")

