import os
import csv
import json
from tqdm import tqdm

def count_words_from_linkedin():
    with open("../Scoring function/data/keywords.json", "r") as keywords_file:
        keywords_json = keywords_file.read()

    keywords = json.loads(keywords_json)

    word_counts = {category: {word: 0 for word in keywords[category]["keywords"]} for category in keywords}

    folder_path = "../Scoring function/profiles_json"

    total_files = len([filename for filename in os.listdir(folder_path) if filename.endswith(".json")])

    with tqdm(total=total_files, desc="Processing LinkedIn profiles") as pbar:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as file:
                    data = json.load(file)
                    posts = data.get("posts", [])
                    for post in posts:
                        post_text = post.get("post", "")
                        for category in keywords:
                            for word in keywords[category]["keywords"]:
                                if word.lower() in post_text.lower():
                                    word_counts[category][word] += post_text.lower().count(word)
                pbar.update(1)

    return word_counts

def count_words_from_web():
    with open("../Scoring function/data/keywords.json", "r") as keywords_file:
        keywords_json = keywords_file.read()

    keywords = json.loads(keywords_json)

    word_counts = {category: {word: 0 for word in keywords[category]["keywords"]} for category in keywords}

    folder_path = "../Scoring function/webpages"

    total_files = len([filename for filename in os.listdir(folder_path) if filename.endswith(".txt")])

    with tqdm(total=total_files, desc="Processing webpages") as pbar:
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as file:
                    text = file.read()
                    for category in keywords:
                        for word in keywords[category]["keywords"]:
                            if word.lower() in text.lower():
                                word_counts[category][word] += text.lower().count(word)
                pbar.update(1)

    return word_counts

def combine_word_counts(table1, table2, output_file):
    combined_counts = {}
    for category in table1:
        combined_counts[category] = {word: table1[category].get(word, 0) + table2[category].get(word, 0) for word in set(table1[category]) | set(table2[category])}

    for category, word_counts in combined_counts.items():
        category_output_file = f"{output_file}_{category}.csv"
        with open(category_output_file, mode='w', newline='') as csvfile:
            fieldnames = ['Word', 'Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for word, count in word_counts.items():
                writer.writerow({'Word': word, 'Count': count})

        print(f"Combined word counts for {category} saved in {category_output_file}")

def main():
    choice = input("Enter 'w' for web, 'l' for LinkedIn, or 'g' for global: ")
    
    if choice == 'w':
        table_web = count_words_from_web()
        combine_word_counts({}, table_web, 'words_count_web')
    elif choice == 'l':
        table_linkedin = count_words_from_linkedin()
        combine_word_counts({}, table_linkedin, 'words_count_linkedin')
    elif choice == 'g':
        table_web = count_words_from_web()
        table_linkedin = count_words_from_linkedin()
        combine_word_counts(table_web, table_linkedin, 'words_count')
    else:
        print("Invalid choice. Please enter 'w', 'l', or 'g'.")

if __name__ == "__main__":
    main()
