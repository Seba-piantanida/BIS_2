import pandas as pd
import csv

def merge_csv_files(input_files, output_file):
    # Open the output file in write mode
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Set to store unique rows
        unique_rows = set()
        
        # Iterate through each input file
        for file in input_files:
            # Open the input file
            with open(file, 'r', newline='') as infile:
                reader = csv.reader(infile)
                # Write each unique row from the input file to the set
                for row in reader:
                    row_key = tuple(row)
                    unique_rows.add(row_key)
                    
        # Write unique rows from the set to the output file
        for row in unique_rows:
            writer.writerow(row)
    
    print(f"Combined CSV file saved successfully to: {output_file}")
    
    # Read the merged CSV file into a DataFrame
    df = pd.read_csv(output_file)
    
    # Remove duplicates using pandas
    df.drop_duplicates(inplace=True)
    
    # Save the deduplicated DataFrame back to the output file
    df.to_csv(output_file, index=False)
    
    print(f"Deduplicated CSV file saved successfully to: {output_file}")

# Esempio di utilizzo
input_files = ["valid_linkedin_urls_0.csv", "valid_linkedin_urls_1.csv", "valid_linkedin_urls_2.csv", "valid_linkedin_urls_3.csv", "valid_linkedin_urls.csv", "valid_linkedin_urls_copy.csv"]
output_file = "merged_file.csv"
merge_csv_files(input_files, output_file)
