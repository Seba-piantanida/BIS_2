import csv
from pathlib import Path
import json
from tqdm import tqdm

with open("data/keywords.json", 'r') as file:
    data = json.load(file)
    keywords = {category: values["keywords"] for category, values in data.items()}
    weights = {category: values["weight"] for category, values in data.items()}

def count_words(text, words):
    count = 0
    for word, weight in words.items():
        count += text.lower().count(word.lower()) * weight
    return count

def process_profile(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        name = Path(file_path).stem 
        content = file.read()
        total_words = len(content.split())
        counts = {key: count_words(content, words) for key, words in keywords.items()}
        esg_count = counts['ESG']
        gender_count = counts['GENDER EQUALITY']
        volley_count = counts['VOLLEYBALL']
        score = ((esg_count / (total_words + 1))*weights['ESG'] + (gender_count / (total_words + 1))*weights['GENDER EQUALITY'] + (volley_count / (total_words + 1))*weights['VOLLEYBALL'])*30
        score = round(score, 2)
        return name, total_words, score, counts

def process_txt_files(folder_path, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'total_words', 'score'] + list(keywords.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        data = []
        files = list(folder_path.glob('*.txt'))
        for file_path in tqdm(files, desc="Processing webpages"):
            name, total_words, score, counts = process_profile(file_path)
            data.append({'name': name, 'total_words': total_words, **counts, 'score': score})

        sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)
        for row in sorted_data:
            writer.writerow(row)

folder_path = Path("webpages/")  
output_file = "data/webpages_scoring.csv"

def main():
    process_txt_files(folder_path, output_file)

if __name__ == '__main__':
    main()
