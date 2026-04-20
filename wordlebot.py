import subprocess
import random
import os

def call_server(args):
    """Communicates with the server script via terminal commands."""
    cmd = ["python3", "wordleserver.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def filter_words(words, last_guess, feedback):
    """Eliminates words that don't match the feedback emojis."""
    new_list = []
    # Letters we KNOW are in the word
    confirmed = {last_guess[i] for i in range(5) if feedback[i] in ("💚", "💛")}

    for w in words:
        keep = True
        for i in range(5):
            letter = last_guess[i]
            if feedback[i] == "💚":
                if w[i] != letter: keep = False
            elif feedback[i] == "💛":
                if letter not in w or w[i] == letter: keep = False
            elif feedback[i] == "🩶":
                # Duplicate letter handling:
                if letter in confirmed:
                    if w[i] == letter: keep = False
                else:
                    if letter in w: keep = False
        if keep:
            new_list.append(w)
    return new_list

def attempt():
    """The bot's automated gameplay loop."""
    print(call_server(["create"]))
    
    # Load dictionary
    try:
        with open("sowpods.txt", "r", encoding='utf-8') as f:
            candidates = [line.strip().upper() for line in f if len(line.strip()) == 5]
    except FileNotFoundError:
        print("Error: sowpods.txt not found!")
        return

    for i in range(6):
        if not candidates:
            print("I used all 6 guesses and did not find the word (List empty).")
            return False

        # Strategy: Pick a random word from the surviving candidates
        my_guess = random.choice(candidates)
        print(f"I am going to guess {my_guess}")
        
        feedback = call_server(["guess", my_guess])
        print(f"I got the feedback: {feedback}")

        if feedback == "💚💚💚💚💚":
            print("I won!")
            return True
        
        if "out of guesses" in feedback:
            print("I lost.")
            return False
        
        # Refine the search based on emojis
        candidates = filter_words(candidates, my_guess, feedback)

    print("I used all 6 guesses and did not find the word.")
    return False

if __name__ == "__main__":
    attempt()
