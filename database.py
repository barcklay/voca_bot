import json, os, random
from datetime import datetime

FILE = "words.json"
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

def load_words():
    with open(FILE) as f:
        return json.load(f)

def save_words(ws):
    with open(FILE, "w") as f:
        json.dump(ws, f, indent=2)

def add_word(word, tr):
    ws = load_words()
    ws.append({"word": word, "translation": tr, "added_at": datetime.now().isoformat()})
    save_words(ws)

def get_random_word():
    ws = load_words()
    if not ws:
        return ("No words yet", "")
    w = random.choice(ws)
    return (w["word"], w["translation"])

def get_test_words(n=5):
    ws = load_words()
    return [w["word"] for w in random.sample(ws, min(n, len(ws)))]
