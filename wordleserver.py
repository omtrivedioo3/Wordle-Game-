import sys
import json
import random
import os

DICT_FILE = "sowpods.txt"
STATE_FILE = "state.json"

def get_words():
    """Loads 5-letter words from dictionary."""
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, "r", encoding='utf-8') as f:
            return [line.strip().upper() for line in f if len(line.strip()) == 5]
    return ["SNAKE", "APPLE", "TRAIN", "CLOUD", "BARYE", "ACTED"]

def create():
    """Initializes a new game state."""
    secret = random.choice(get_words())
    state = {
        "secret": secret, 
        "guesses_left": 6, 
        "status": "playing",
        "history": []
    }
    # ensure_ascii=False makes emojis look like hearts in the file, not codes
    with open(STATE_FILE, "w", encoding='utf-8') as f:
        json.dump(state, f, indent=4, ensure_ascii=False)
    print("Game created!")

def guess(word):
    """Processes a guess and updates state.json."""
    if not os.path.exists(STATE_FILE):
        print("Error: No game active. Run 'create' first.")
        return

    with open(STATE_FILE, "r", encoding='utf-8') as f:
        state = json.load(f)

    if state["status"] != "playing":
        print(f"out of guesses, please run python3 wordleserver create. The word was {state['secret']}")
        return

    secret = state["secret"]
    word = word.upper()
    
    # Wordle Feedback Logic
    feedback = ["🩶"] * 5
    s_list = list(secret)
    g_list = list(word)

    # Pass 1: Greens (Correct position)
    for i in range(5):
        if g_list[i] == s_list[i]:
            feedback[i] = "💚"
            s_list[i] = g_list[i] = None

    # Pass 2: Yellows (Wrong position)
    for i in range(5):
        if g_list[i] and g_list[i] in s_list:
            feedback[i] = "💛"
            s_list[s_list.index(g_list[i])] = None

    result_emojis = "".join(feedback)
    state["guesses_left"] -= 1
    state["history"].append({"guess": word, "result": result_emojis})
    
    if word == secret:
        state["status"] = "won"
    elif state["guesses_left"] <= 0:
        state["status"] = "lost"

    with open(STATE_FILE, "w", encoding='utf-8') as f:
        json.dump(state, f, indent=4, ensure_ascii=False)
    
    print(result_emojis)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 wordleserver.py create | guess [WORD]")
    elif sys.argv[1] == "create":
        create()
    elif sys.argv[1] == "guess":
        guess(sys.argv[2])