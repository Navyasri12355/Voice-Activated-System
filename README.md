# Voice-Activated System

A hands-free computer control system that interprets voice commands to execute system actions, such as opening applications, searching the web, and checking the time. Built with Python, SpeechRecognition, and Spacy.

## Features

-   **Voice Recognition**: Converts speech to text using Google Speech Recognition.
-   **Natural Language Processing**: Uses `spaCy` for intent recognition, with a robust keyword fallback.
-   **System Control**: Opens applications (Notepad, Calculator, Chrome, etc.).
-   **Web Search**: Automatically performs Google searches.
-   **Voice Feedback**: Responds to the user using Text-to-Speech (`pyttsx3`).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Navyasri12355/Voice-Activated-System.git
    cd Voice-Activated-System
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Spacy Model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```
    *Note: If the download fails, you can try installing the wheel directly:*
    ```bash
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
    ```

## Usage

Run the main application:

```bash
python src/main.py
```

Wait for the "Listening..." prompt, then speak a command.

### Example Commands

-   "Open Notepad"
-   "Open Calculator"
-   "Search for Python tutorials"
-   "What time is it?"
-   "Exit"

## Project Structure

```
Voice-Activated-System/
├── src/
│   ├── main.py          # Entry point
│   ├── listener.py      # Speech-to-Text
│   ├── speaker.py       # Text-to-Speech
│   ├── commander.py     # NLP & Intent Parsing
│   └── executor.py      # Action Execution
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

## Troubleshooting

-   **"API unavailable"**: Check your internet connection (required for Google Speech Recognition).
-   **Microphone issues**: Ensure your default recording device is set correctly in OS settings.
-   **Spacy specific errors**: The system will fallback to simple keyword matching if Spacy fails to load, so basic commands will still work.