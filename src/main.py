import listener
import speaker
import commander
import executor

def main():
    speaker.speak("System initialized. Listening for commands.")
    while True:
        try:
            command_text = listener.listen()
            if command_text:
                intent = commander.parse_command(command_text)
                if intent:
                    executor.execute(intent)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
