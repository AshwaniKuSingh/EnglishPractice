import tkinter as tk
from tkinter import messagebox
import os
import json

# Load the word sets from the JSON file
word_sets_file = 'word_sets.json'  # Ensure this is the path to your saved JSON file
with open(word_sets_file, 'r') as file:
    word_sets = json.load(file)

def speak(word):
    """Use macOS's built-in text-to-speech."""
    os.system(f'say {word}')

class SpellingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spelling Practice")
        self.root.geometry("800x600")  # Default size
        self.root.configure(bg="#f2f2f2")  # Light background color
        self.root.bind("<F11>", self.toggle_fullscreen)  # Bind F11 to toggle fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)  # Bind Escape to exit fullscreen
        
        self.word_set = []
        self.current_index = 0
        self.current_word = None  # Store the current word for repeating
        self.is_fullscreen = False  # Track fullscreen state
        
        # Title and Instructions
        self.title_label = tk.Label(root, text="Welcome to Spelling Practice", font=("Arial", 24, "bold"), bg="#f2f2f2", fg="#333")
        self.title_label.pack(pady=20)
        
        self.instruction_label = tk.Label(root, text="Enter a set number and start practicing!", font=("Arial", 14), bg="#f2f2f2", fg="#555")
        self.instruction_label.pack(pady=10)
        
        # Input for Set Number
        self.input_frame = tk.Frame(root, bg="#f2f2f2")
        self.input_frame.pack(pady=10)
        
        self.set_label = tk.Label(self.input_frame, text="Set Number:", font=("Arial", 16), bg="#f2f2f2", fg="#333")
        self.set_label.grid(row=0, column=0, padx=5)
        
        self.set_entry = tk.Entry(self.input_frame, font=("Arial", 16), width=10)
        self.set_entry.grid(row=0, column=1, padx=5)
        
        self.submit_button = tk.Button(self.input_frame, text="Submit", font=("Arial", 14), bg="#4CAF50", fg="black", activebackground="#45a049", activeforeground="black", relief="raised", bd=2, command=self.load_set)
        self.submit_button.grid(row=0, column=2, padx=5)
        
        # Buttons for Interaction
        self.button_frame = tk.Frame(root, bg="#f2f2f2")
        self.button_frame.pack(pady=20)
        
        self.next_button = tk.Button(self.button_frame, text="Next", font=("Arial", 14), bg="#2196F3", fg="black", activebackground="#1e88e5", activeforeground="black", relief="raised", bd=2, command=self.speak_next_word, state=tk.DISABLED, width=10)
        self.next_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.repeat_button = tk.Button(self.button_frame, text="Repeat", font=("Arial", 14), bg="#FF9800", fg="black", activebackground="#fb8c00", activeforeground="black", relief="raised", bd=2, command=self.repeat_word, state=tk.DISABLED, width=10)
        self.repeat_button.grid(row=0, column=1, padx=10, pady=10)

        self.show_word_button = tk.Button(self.button_frame, text="Show Word", font=("Arial", 14), bg="#9C27B0", fg="black", activebackground="#8e24aa", activeforeground="black", relief="raised", bd=2, command=self.show_word, state=tk.DISABLED, width=10)
        self.show_word_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.stop_button = tk.Button(self.button_frame, text="Stop", font=("Arial", 14), bg="#F44336", fg="black", activebackground="#e53935", activeforeground="black", relief="raised", bd=2, command=self.stop_program, width=10)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Word Display Box
        self.word_frame = tk.LabelFrame(root, text="Word Display", font=("Arial", 14, "bold"), bg="#f2f2f2", fg="#1E88E5", labelanchor="n", padx=10, pady=10)
        self.word_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.word_label = tk.Label(self.word_frame, text="", font=("Arial", 40, "bold"), bg="#f2f2f2", fg="#1E88E5")
        self.word_label.pack(expand=True)
    
    def load_set(self):
        """Load the selected set of words."""
        try:
            set_number = int(self.set_entry.get())
            if set_number < 1 or set_number > len(word_sets):
                raise ValueError
            self.word_set = word_sets[set_number - 1]
            self.current_index = 0
            self.word_label.config(text="Ready to start!")
            self.next_button.config(state=tk.NORMAL)
            self.repeat_button.config(state=tk.DISABLED)
            self.show_word_button.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Error", f"Invalid set number. Please enter a number between 1 and {len(word_sets)}.")
    
    def speak_next_word(self):
        """Speak the next word in the set."""
        if self.current_index < len(self.word_set):
            self.current_word = self.word_set[self.current_index]
            self.word_label.config(text="")  # Hide the word initially
            speak(self.current_word)
            self.current_index += 1
            self.repeat_button.config(state=tk.NORMAL)
            self.show_word_button.config(state=tk.NORMAL)
        else:
            self.word_label.config(text="All words in the set are complete!")
            self.next_button.config(state=tk.DISABLED)
            self.repeat_button.config(state=tk.DISABLED)
            self.show_word_button.config(state=tk.DISABLED)
            continue_choice = messagebox.askyesno("Complete", "You have completed the set. Do you want to continue?")
            if continue_choice:
                self.reset_program()
            else:
                self.stop_program()
    
    def repeat_word(self):
        """Repeat the current word."""
        if self.current_word:
            speak(self.current_word)

    def show_word(self):
        """Show the current word in the word display box."""
        if self.current_word:
            self.word_label.config(text=f"{self.current_word}")
    
    def reset_program(self):
        """Reset the program to allow for a new set selection."""
        self.set_entry.delete(0, tk.END)
        self.word_label.config(text="")
        self.next_button.config(state=tk.DISABLED)
        self.repeat_button.config(state=tk.DISABLED)
        self.show_word_button.config(state=tk.DISABLED)
        self.current_word = None
    
    def stop_program(self):
        """Stop the program."""
        self.root.quit()
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode."""
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)

# Create the application
root = tk.Tk()
app = SpellingApp(root)
root.mainloop()
