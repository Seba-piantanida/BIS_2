import json
import csv
from pathlib import Path
import pandas as pd

with open("keywords.json", 'r') as file:
    keywords = json.load(file)

#occurrences of words in a text
def count_words(text, words):
    count = 0
    for word in words:
        count += text.lower().count(word.lower())
    return count

#process a profile in JSON file and count occurrences of words in each key
def process_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        name = data["name"]
        posts = data["posts"]
        total_words = 0
        counts = {key: 0 for key in keywords}
        for post in posts:
            post_text = post["post"]
            total_words += len(post_text.split())
            for key, words in keywords.items():
                counts[key] += count_words(post_text, words)
        return name, total_words, counts

# Process each JSON file and save the results to a CSV file
def process_json_files(folder_path, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'total_words'] + list(keywords.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        
        for file_path in folder_path.glob('*.json'):
            name, total_words, counts = process_profile(file_path)
            writer.writerow({'name': name, 'total_words': total_words, **counts})


folder_path = Path("profiles_json/")

output_file = "linkedin_scoring_employee.csv"


process_json_files(folder_path, output_file)

df1 = pd.read_csv(output_file)
df2 = None

try:
    
    df2 = pd.read_csv('TOP 500_C-LEVEL.csv', sep=';', header=None)
except pd.errors.ParserError as e:
    print("Tokenization error:", e)

if df2 is not None:
    
    executives_companies = {}
    for index, row in df2.iterrows():
        for executive in row.iloc[2:]:  
            if isinstance(executive, str):
                executives_companies[executive] = row.iloc[1]  

    def get_company(name):
        return executives_companies.get(name, 'Company not found')

   
    df1['Company'] = df1['name'].apply(get_company)
    df1.to_csv('linkedin_scoring_employee.csv', index=False)
