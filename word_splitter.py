from PyPDF2 import PdfReader
import json

# Load the PDF file
pdf_path = 'LA Listening Blanks Spelling List.pdf'  # Replace with the path to your PDF file
reader = PdfReader(pdf_path)

# Extract text from all pages
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()

# Extract words from the text
words = full_text.split()

# Start from "Practice" and collect words until the end of the list
try:
    start_index = words.index("Practice")
    filtered_words = words[start_index:]  # Get words starting from "Practice"
except ValueError:
    raise ValueError("The word 'Practice' was not found in the document.")

# Filter out non-alphabetic or unrelated text
word_list = [word for word in filtered_words if word.isalpha()]

# Divide the words into sets of 30
word_sets = [word_list[i:i + 30] for i in range(0, len(word_list), 30)]

# Save the word sets to a JSON file
output_path = 'word_sets.json'
with open(output_path, 'w') as file:
    json.dump(word_sets, file)

print(f"Word sets have been saved to '{output_path}'.")

