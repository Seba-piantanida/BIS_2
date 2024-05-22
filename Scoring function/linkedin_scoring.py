import json
import csv
from pathlib import Path
import pandas as pd
from tqdm import tqdm

with open("data/keywords.json", 'r') as file:
    data = json.load(file)
    keywords = {category: values["keywords"] for category, values in data.items()}
    weights = {category: values["weight"] for category, values in data.items()}

# Occurrences of words in a text
def count_words(text, words):
    count = 0
    for word, weight in words.items():
        count += text.lower().count(word.lower()) * weight
    return count

# Process a profile in JSON file and count occurrences of words in each key
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
        esg_count = counts['ESG']
        gender_count = counts['GENDER EQUALITY']
        volley_count = counts['VOLLEYBALL']
        score = ((esg_count / (total_words + 1))*weights['ESG'] + (gender_count / (total_words + 1))*weights['GENDER EQUALITY'] + (volley_count / (total_words + 1))*weights['VOLLEYBALL'])*30
        score = round(score, 2)
        return name, total_words, score, counts

# Process each JSON file and save the results to a CSV file
def process_json_files(folder_path, output_file):
    files = list(folder_path.glob('*.json'))
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'total_words', 'score'] + list(keywords.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file_path in tqdm(files, desc="Processing profiles"):
            name, total_words, score, counts = process_profile(file_path)
            writer.writerow({'name': name, 'total_words': total_words, **counts, 'score': score})

folder_path = Path("profiles_json/")
output_file = "data/linkedin_scoring_employee.csv"

def main():
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
        df1.to_csv('data/linkedin_scoring_employee.csv', index=False)

if __name__ == '__main__':
    main()
