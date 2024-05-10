import csv
import re

def extract_name(linkedin_url):
    # Rimuovi eventuale slash finale
    linkedin_url = linkedin_url.rstrip('/')
    # Estrai la parte del nome dall'URL di LinkedIn
    name = re.search(r'/in/(.*?)(?:,|/|$)', linkedin_url)
    if name:
        return name.group(1)
    else:
        return None

def main(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        with open(output_file, 'w') as output:
            for row in reader:
                # Ignora le righe vuote nel file CSV
                if not row:
                    continue
                linkedin_url = row[0]
                name = extract_name(linkedin_url)
                if name:
                    output.write(name + '\n')

if __name__ == "__main__":
    input_file = "file_a_filtered.csv"
    output_file = "output.txt"
    main(input_file, output_file)
