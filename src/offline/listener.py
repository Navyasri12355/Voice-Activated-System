import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import requests
import zipfile
import tqdm

class OfflineListener:
    def __init__(self, model_path="model"):
        self.model_path = model_path
        self.q = queue.Queue()
        self.samplerate = 16000
        self.model = self._load_model()
        self.rec = vosk.KaldiRecognizer(self.model, self.samplerate)

    def _load_model(self):
        if not os.path.exists(self.model_path):
            print(f"Model not found at {self.model_path}. Downloading...")
            self._download_model()
        
        try:
            return vosk.Model(self.model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")
            sys.exit(1)

    def _download_model(self):
        url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        
        zip_path = "model.zip"
        
        with open(zip_path, "wb") as f, tqdm.tqdm(
            desc="Downloading Model",
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                size = f.write(data)
                bar.update(size)
                
        print("Extracting model...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(".")
            
        # Rename extracted folder to 'model'
        extracted_folder = "vosk-model-small-en-us-0.15"
        if os.path.exists(extracted_folder):
            os.rename(extracted_folder, self.model_path)
            
        os.remove(zip_path)
        print("Model ready.")

    def _callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def listen(self):
        """Listens for audio and returns recognized text."""
        print("Offline Listener: Listening...")
        with sd.RawInputStream(samplerate=self.samplerate, blocksize=8000, device=None, dtype='int16',
                               channels=1, callback=self._callback):
            while True:
                data = self.q.get()
                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"Offline Heard: {text}")
                        return text
