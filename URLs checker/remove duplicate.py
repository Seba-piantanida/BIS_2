import pandas as pd

# Leggi i dati dal file CSV in un DataFrame
df = pd.read_csv("valid_linkedin_urls.csv", header=None)

# Rimuovi i duplicati
df.drop_duplicates(inplace=True)

# Salva il DataFrame senza duplicati in un nuovo file CSV
df.to_csv("valid_linkedin_urls.csv", index=False, header=False)
