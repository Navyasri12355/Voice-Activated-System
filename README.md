# Voice-Activated System

A powerful hands-free computer control system built with Python. It allows users to control their Windows OS through voice commands, supporting both internet-reliant and fully offline modes.

## ✨ Features

- **🗣️ Advanced Speech Recognition**:
  - **Online**: Uses Google Web Speech API for high accuracy.
  - **Offline**: Uses `Vosk` for private, local transcription.
- **🧠 Custom NLP Engine**:
  - Powered by `Spacy` with a custom-trained `TextCategorizer` and `NER` (Named Entity Recognition).
  - High robustness against noise and variations in speech.
- **💻 Desktop Control**:
  - **Applications**: Open and Close windows (e.g., "Open Chrome", "Close Notepad").
  - **Browsing**: Native browser control for searching and direct navigation.
- **🔊 System Mastery**:
  - **Volume**: Increase, Decrease, Mute, and Unmute.
  - **Media**: Play, Pause, Next, and Previous track controls.
  - **State**: Lock PC, Sleep, Restart, and Shut Down (with safety delay).

## 🚀 Getting Started

### Prerequisites
- Windows OS
- Python 3.8+
- Active Microphone

### Installation
1. Clone the repository and navigate to the directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Install dependencies:
   ```bash
   venv\Scripts\pip install -r requirements.txt
   ```

### 🛠️ Configuration (Offline Only)
To use the offline mode, you must first train the local Spacy model:
```bash
venv\Scripts\python train_spacy.py
```
*This will generate a model in `models/custom_spacy`.*

## 🎮 Usage

### Run Online Mode
```bash
venv\Scripts\python src\main.py
```

### Run Offline Mode
```bash
venv\Scripts\python src\main_offline.py
```

## 🗣️ Voice Commands

| Category | Commands |
| :--- | :--- |
| **Apps** | "Open [App Name]", "Close [App Name]", "Terminate [App Name]" |
| **Browsing** | "Go to [website.com]", "Browse [website]", "Search for [query]" |
| **Volume** | "Volume up", "Decrease volume", "Mute sound", "Unmute" |
| **Media** | "Play music", "Pause video", "Next track", "Previous song" |
| **System** | "Lock my computer", "Shutdown the pc", "Restart computer", "Sleep" |
| **Utility** | "What time is it?", "Exit application", "Goodbye" |

## 📁 Project Structure
- `src/`: Core source code.
  - `main.py`: Online entry point.
  - `main_offline.py`: Offline entry point.
  - `executor.py`: OS-level action logic.
  - `offline/`: Modules specific to the offline stack.
- `train_spacy.py`: Training script for the custom NLP model.
- `models/`: Location of the trained Spacy models (gitignored).
- `requirements.txt`: Project dependencies.

## ⚖️ License
MIT License