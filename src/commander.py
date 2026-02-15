import spacy
from fuzzywuzzy import process

NLP_MODEL = None
try:
    NLP_MODEL = spacy.load("en_core_web_sm")
    print("NLP model loaded.")
except Exception as e:
    print(f"Warning: Could not load Spacy model '{e}'. Falling back to simple keyword matching.")

def parse_command(text):
    """
    Parses text to identify intent.
    Returns a dictionary: {'action': str, 'target': str} or None.
    """
    if not text:
        return None
    
    cmd = text.lower().strip()
    
    # Simple keyword matching (Robust fallback)
    if "open" in cmd:
        target = cmd.replace("open", "").strip()
        return {"action": "open", "target": target}
    
    if "search for" in cmd or "search" in cmd:
        target = cmd.replace("search for", "").replace("search", "").strip()
        return {"action": "search", "target": target}
        
    if "time" in cmd:
        return {"action": "time", "target": ""}
        
    if "exit" in cmd or "quit" in cmd or "stop" in cmd:
        return {"action": "exit", "target": ""}

    return {"action": "unknown", "text": cmd}

