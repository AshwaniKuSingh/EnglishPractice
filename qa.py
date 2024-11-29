import pyttsx3
import json
import time

# Load the word sets from the JSON file
word_sets_file = 'word_sets.json'  # Ensure this is the path to your saved JSON file
with open(word_sets_file, 'r') as file:
    word_sets = json.load(file)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak_words(set_number):
    """Speak the words in the specified set number."""
    # Validate the set number
    if set_number < 1 or set_number > len(word_sets):
        print(f"Invalid set number. Please choose a number between 1 and {len(word_sets)}.")
        return
    
    # Retrieve the word set (convert to zero-based index)
    word_list = word_sets[set_number - 1]
    
    # Speak each word with a pause
    print(f"Speaking words from set {set_number}:")
    for word in word_list:
        print(f"Word: {word}")  # Display the word for reference
        engine.say(word)
        engine.runAndWait()
        time.sleep(2)  # Pause for 2 seconds between words

# Input: Set number
try:
    set_number = int(input("Enter the set number to speak: "))
    speak_words(set_number)
except ValueError:
    print("Invalid input. Please enter a valid set number.")
