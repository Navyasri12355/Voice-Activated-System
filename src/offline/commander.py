import spacy
import os

class OfflineCommander:
    def __init__(self, model_path="models/custom_spacy"):
        print(f"Loading offline NLP model from {model_path}...")
        try:
            self.nlp = spacy.load(model_path)
            print("Offline NLP model loaded successfully.")
        except Exception as e:
            print(f"Error loading offline model: {e}")
            print("Please run 'python train_spacy.py' first.")
            self.nlp = None

    def parse_command(self, text):
        """
        Parses text using the custom Spacy model.
        Returns {'action': str, 'target': str}
        """
        if not text or not self.nlp:
            return None

        doc = self.nlp(text)
        
        # Get highest scoring category
        cats = doc.cats
        if not cats:
             return {"action": "unknown", "text": text}

        intent = max(cats, key=cats.get)
        confidence = cats[intent]
        
        print(f"Intent: {intent} ({confidence:.2f})")
        
        # Stricter confidence interpretation
        # Lowering threshold slightly to handle STT variations
        if confidence < 0.2:
            return {"action": "unknown", "text": text}
        
        # If the intent is clear but NER fails, attempt a more robust fallback
        # or if the confidence is just "okay" (0.2-0.5), we still try to parse if entities exist

        # Extract entities
        target = ""
        for ent in doc.ents:
            if intent == "OPEN" and ent.label_ == "APP":
                target = ent.text
            elif intent == "CLOSE" and ent.label_ == "APP":
                target = ent.text
            elif intent == "SEARCH" and ent.label_ == "QUERY":
                target = ent.text
            elif intent == "BROWSE" and ent.label_ == "URL":
                target = ent.text
            elif intent == "VOLUME" and ent.label_ == "ACTION":
                target = ent.text
            elif intent == "MEDIA" and ent.label_ == "ACTION":
                target = ent.text
            elif intent == "SYSTEM" and ent.label_ == "STATE":
                target = ent.text
        
        # Basic fallback for target if NER fails but intent is clear
        if not target and confidence > 0.7:

            # Simple heuristic backup
            words = text.lower().split()
            if intent == "OPEN" and "open" in words:
                idx = words.index("open")
                if idx + 1 < len(words):
                    target = " ".join(words[idx+1:])
            elif intent == "SEARCH" and "for" in words:
                 idx = words.index("for")
                 if idx + 1 < len(words):
                    target = " ".join(words[idx+1:])

        return {"action": intent.lower(), "target": target}
