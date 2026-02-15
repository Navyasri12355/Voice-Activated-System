import spacy
from spacy.util import minibatch, compounding
from spacy.training.example import Example
import random
import os
from pathlib import Path

# Define all possible intents
INTENTS = ["OPEN", "SEARCH", "TIME", "EXIT", "VOLUME", "MEDIA", "SYSTEM", "CLOSE", "BROWSE"]

def get_cats(intent_name):
    """Helper to create the cats dictionary with one intent set to 1.0 and others to 0.0"""
    return {i: (1.0 if i == intent_name else 0.0) for i in INTENTS}

# Define training data with standardized categories
TRAIN_DATA = [
    # OPEN Intent
    ("Open Notepad", {"cats": get_cats("OPEN"), "entities": [(5, 12, "APP")]}),
    ("Launch Calculator", {"cats": get_cats("OPEN"), "entities": [(7, 17, "APP")]}),
    ("Start Chrome", {"cats": get_cats("OPEN"), "entities": [(6, 12, "APP")]}),
    ("Run Microsoft Edge", {"cats": get_cats("OPEN"), "entities": [(4, 18, "APP")]}),
    ("Open Google Chrome", {"cats": get_cats("OPEN"), "entities": [(5, 18, "APP")]}),
    ("Open Firefox", {"cats": get_cats("OPEN"), "entities": [(5, 12, "APP")]}),
    ("Can you open Spotify", {"cats": get_cats("OPEN"), "entities": [(13, 20, "APP")]}),
    ("open chrome", {"cats": get_cats("OPEN"), "entities": [(5, 11, "APP")]}),
    
    # SEARCH Intent
    ("Search for Python tutorials", {"cats": get_cats("SEARCH"), "entities": [(11, 27, "QUERY")]}),
    ("Find recipes for lasagna", {"cats": get_cats("SEARCH"), "entities": [(5, 24, "QUERY")]}),
    ("Google how to code", {"cats": get_cats("SEARCH"), "entities": [(7, 18, "QUERY")]}),
    ("Search for weather in London", {"cats": get_cats("SEARCH"), "entities": [(11, 28, "QUERY")]}),
    ("Who is the president", {"cats": get_cats("SEARCH"), "entities": [(0, 20, "QUERY")]}),
    
    # TIME Intent
    ("What time is it", {"cats": get_cats("TIME"), "entities": []}),
    ("Tell me the time", {"cats": get_cats("TIME"), "entities": []}),
    ("Clock current time", {"cats": get_cats("TIME"), "entities": []}),
    ("Do you know the time", {"cats": get_cats("TIME"), "entities": []}),
    
    # EXIT Intent
    ("Exit application", {"cats": get_cats("EXIT"), "entities": []}),
    ("Stop listening", {"cats": get_cats("EXIT"), "entities": []}),
    ("Quit system", {"cats": get_cats("EXIT"), "entities": []}),
    ("Goodbye", {"cats": get_cats("EXIT"), "entities": []}),
    ("Terminate", {"cats": get_cats("EXIT"), "entities": []}),

    # VOLUME Intent
    ("Increase volume", {"cats": get_cats("VOLUME"), "entities": [(0, 8, "ACTION")]}),
    ("increased volume", {"cats": get_cats("VOLUME"), "entities": [(0, 9, "ACTION")]}), # Common STT variation
    ("Volume up", {"cats": get_cats("VOLUME"), "entities": [(7, 9, "ACTION")]}),
    ("Decrease volume", {"cats": get_cats("VOLUME"), "entities": [(0, 8, "ACTION")]}),
    ("Turn down the sound", {"cats": get_cats("VOLUME"), "entities": [(0, 9, "ACTION")]}),
    ("Mute volume", {"cats": get_cats("VOLUME"), "entities": [(0, 4, "ACTION")]}),
    ("Unmute the mic", {"cats": get_cats("VOLUME"), "entities": [(0, 6, "ACTION")]}),

    # MEDIA Intent
    ("Play music", {"cats": get_cats("MEDIA"), "entities": [(0, 4, "ACTION")]}),
    ("Pause video", {"cats": get_cats("MEDIA"), "entities": [(0, 5, "ACTION")]}),
    ("Next track", {"cats": get_cats("MEDIA"), "entities": [(0, 4, "ACTION")]}),
    ("Previous song", {"cats": get_cats("MEDIA"), "entities": [(0, 8, "ACTION")]}),

    # SYSTEM Intent
    ("Lock my computer", {"cats": get_cats("SYSTEM"), "entities": [(0, 4, "STATE")]}),
    ("Shutdown the pc", {"cats": get_cats("SYSTEM"), "entities": [(0, 8, "STATE")]}),
    ("Restart computer", {"cats": get_cats("SYSTEM"), "entities": [(0, 7, "STATE")]}),
    ("Put pc to sleep", {"cats": get_cats("SYSTEM"), "entities": [(11, 16, "STATE")]}),

    # CLOSE Intent
    ("Close Notepad", {"cats": get_cats("CLOSE"), "entities": [(6, 13, "APP")]}),
    ("Terminate Chrome", {"cats": get_cats("CLOSE"), "entities": [(10, 16, "APP")]}),
    ("Exit Calculator", {"cats": get_cats("CLOSE"), "entities": [(5, 15, "APP")]}),
    ("Quit Word", {"cats": get_cats("CLOSE"), "entities": [(5, 9, "APP")]}),

    # BROWSE Intent
    ("Browse youtube.com", {"cats": get_cats("BROWSE"), "entities": [(7, 18, "URL")]}),
    ("Go to google.co.in", {"cats": get_cats("BROWSE"), "entities": [(6, 18, "URL")]}),
    ("Open facebook", {"cats": get_cats("BROWSE"), "entities": [(5, 13, "URL")]}),
    ("Open website reddit.com", {"cats": get_cats("BROWSE"), "entities": [(13, 23, "URL")]}),

    # UNKNOWN / Noise
    ("Hello there", {"cats": {i: 0.0 for i in INTENTS}, "entities": []}),
    ("Just talking to myself", {"cats": {i: 0.0 for i in INTENTS}, "entities": []}),
    ("the will of jerk a below", {"cats": {i: 0.0 for i in INTENTS}, "entities": []}), # Real user noise example
    ("see", {"cats": {i: 0.0 for i in INTENTS}, "entities": []}), # Real user noise example
]

def train_model(output_dir="models/custom_spacy", n_iter=40):
    """Trains a Spacy model for intent classification and NER."""
    
    nlp = spacy.blank("en")
    print("Created blank 'en' model")

    # --- TextCategorizer Setup ---
    if "textcat" not in nlp.pipe_names:
        config = {
            "model": {
                "@architectures": "spacy.TextCatBOW.v2",
                "exclusive_classes": True,
                "ngram_size": 2, # Increase to 2 for better context (e.g. "open chrome")
                "no_output_layer": False
            }
        }
        textcat = nlp.add_pipe("textcat", config=config, last=True)
    else:
        textcat = nlp.get_pipe("textcat")

    for intent in INTENTS:
        textcat.add_label(intent)

    # --- NER Setup ---
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    print("Training model (TextCat + NER)...")
    nlp.begin_training()

    for i in range(n_iter):
        losses = {}
        random.shuffle(TRAIN_DATA)
        batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
        
        for batch in batches:
            texts, annotations = zip(*batch)
            examples = []
            for j in range(len(texts)):
                doc = nlp.make_doc(texts[j])
                examples.append(Example.from_dict(doc, annotations[j]))
            
            nlp.update(examples, drop=0.2, losses=losses)
        
        if (i+1) % 5 == 0:
            print(f"Iteration {i+1}, Losses: {losses}")

    if output_dir:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir(parents=True)
        nlp.to_disk(output_dir)
        print(f"Saved model to {output_dir}")

if __name__ == "__main__":
    train_model()
