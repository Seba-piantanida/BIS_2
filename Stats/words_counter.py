import os
import csv
import json
from tqdm import tqdm

def count_words_from_linkedin():
    with open("../Scoring function/keywords.json", "r") as keywords_file:
        keywords_json = keywords_file.read()

    keywords = json.loads(keywords_json)

    word_counts = {word: 0 for category in keywords for word in keywords[category]["keywords"]}

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
                                    word_counts[word] += post_text.lower().count(word)
                pbar.update(1)

    return word_counts

def count_words_from_web():
    with open("../Scoring function/keywords.json", "r") as keywords_file:
        keywords_json = keywords_file.read()

    keywords = json.loads(keywords_json)

    word_counts = {word: 0 for category in keywords for word in keywords[category]["keywords"]}

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
                                word_counts[word] += text.lower().count(word)
                pbar.update(1)

    return word_counts

def combine_word_counts(table1, table2, output_file):
    word_counts = {word: table1.get(word, 0) + table2.get(word, 0) for word in set(table1) | set(table2)}

    with open(output_file, mode='w', newline='') as csvfile:
        fieldnames = ['Word', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for word, count in word_counts.items():
            writer.writerow({'Word': word, 'Count': count})

    print("Combined word counts saved in", output_file)

def main():
    choice = input("Enter 'w' for web, 'l' for LinkedIn, or 'g' for global: ")
    
    if choice == 'w':
        table_web = count_words_from_web()
        combine_word_counts({}, table_web, 'words_count_web.csv')
    elif choice == 'l':
        table_linkedin = count_words_from_linkedin()
        combine_word_counts({}, table_linkedin, 'words_count_linkedin.csv')
    elif choice == 'g':
        table_web = count_words_from_web()
        table_linkedin = count_words_from_linkedin()
        combine_word_counts(table_web, table_linkedin, 'words_count.csv')
    else:
        print("Invalid choice. Please enter 'w', 'l', or 'g'.")

if __name__ == "__main__":
    main()
