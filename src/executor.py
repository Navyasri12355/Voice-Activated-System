import os
import webbrowser
import datetime
import speaker
import keyboard
import subprocess

def execute(intent):
    """Executes the action based on intent."""
    if not intent:
        return

    action = intent.get("action")
    target = intent.get("target")

    if action == "open":
        speaker.speak(f"Opening {target}")
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "chrome": "start chrome",
            "edge": "start msedge"
        }
        
        app_cmd = apps.get(target.lower(), None)
        if app_cmd:
            os.system(app_cmd)
        elif target:
            try:
                os.startfile(target)
            except:
                speaker.speak(f"Could not find application {target}")
        else:
             speaker.speak("I didn't hear an application name.")

    elif action == "close":
        speaker.speak(f"Closing {target}")
        # Use taskkill for Windows
        try:
            # We try to match by im (image name). 
            # This is a bit rough, but works for common apps.
            subprocess.run(["taskkill", "/F", "/IM", f"{target}.exe"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # Fallback: try common process names if target is "chrome" instead of "chrome.exe"
            common_processes = {
                "chrome": "chrome.exe",
                "notepad": "notepad.exe",
                "calculator": "CalculatorApp.exe", # Windows 10/11
                "edge": "msedge.exe"
            }
            proc = common_processes.get(target.lower())
            if proc:
                subprocess.run(["taskkill", "/F", "/IM", proc])
            else:
                speaker.speak(f"Could not close {target}")

    elif action == "search":
        speaker.speak(f"Searching for {target}")
        webbrowser.open(f"https://www.google.com/search?q={target}")

    elif action == "browse":
        speaker.speak(f"Going to {target}")
        url = target if "." in target else f"{target}.com"
        if not url.startswith("http"):
            url = f"https://{url}"
        webbrowser.open(url)

    elif action == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        speaker.speak(f"The time is {now}")

    elif action == "volume":
        if "up" in target or "increase" in target:
            keyboard.press_and_release("volume up")
            speaker.speak("Volume increased")
        elif "down" in target or "decrease" in target:
            keyboard.press_and_release("volume down")
            speaker.speak("Volume decreased")
        elif "mute" in target:
            keyboard.press_and_release("volume mute")
            speaker.speak("Sound toggled")
        elif "unmute" in target:
            # On Windows, mute is a toggle, but we can try to unmute by increasing?
            # Usually 'volume mute' is the key.
            keyboard.press_and_release("volume mute")

    elif action == "media":
        if "play" in target or "pause" in target:
            keyboard.press_and_release("play/pause media")
        elif "next" in target:
            keyboard.press_and_release("next track")
        elif "previous" in target:
            keyboard.press_and_release("previous track")

    elif action == "system":
        if "lock" in target:
            speaker.speak("Locking computer")
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif "shutdown" in target:
            speaker.speak("Shutting down in 10 seconds. Say stop to cancel.")
            os.system("shutdown /s /t 10")
        elif "restart" in target:
            speaker.speak("Restarting in 10 seconds.")
            os.system("shutdown /r /t 10")
        elif "sleep" in target:
            speaker.speak("Going to sleep")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif action == "exit":
        speaker.speak("Goodbye")
        exit()

    elif action == "unknown":
        speaker.speak("I didn't understand that command.")

