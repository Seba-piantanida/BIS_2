import csv
from pathlib import Path
import json

with open("keywords.json", 'r') as file:
    keywords = json.load(file)

# Function to count occurrences of words in a text
def count_words(text, words):
    count = 0
    for word in words:
        count += text.lower().count(word.lower())
    return count

# Function to process a profile in a TXT file and count occurrences of words in each key
def process_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        name = Path(file_path).stem  # Use file name as the 'name' value
        content = file.read()
        total_words = len(content.split())
        counts = {key: count_words(content, words) for key, words in keywords.items()}
        return name, total_words, counts

# Process each TXT file in the folder and save the results to a CSV file
def process_txt_files(folder_path, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'total_words'] + list(keywords.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        data = []
        for file_path in folder_path.glob('*.txt'):
            name, total_words, counts = process_profile(file_path)
            data.append({'name': name, 'total_words': total_words, **counts})

        sorted_data = sorted(data, key=lambda x: x['VOLLEYBALL'], reverse=True)
        for row in sorted_data:
            writer.writerow(row)


folder_path = Path("/Users/seba/Desktop/HTML crawler/webpages")  
output_file = "webpages_scoring.csv"

process_txt_files(folder_path, output_file)
