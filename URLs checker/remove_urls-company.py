import pandas as pd
from fuzzywuzzy import process


df_a = pd.read_csv("merged_file.csv", usecols=[0, 1], sep=',')
df_b = pd.read_csv("TOP 500_C-LEVEL.csv", usecols=[0, 1], sep=';')


df_a.columns = ["Name", "Company"]
df_b.columns = ["Dummy", "Company"] 


def fuzzy_match(company, company_list):
    if pd.isnull(company) or isinstance(company, float):  
        return None
    matched = process.extractOne(str(company), company_list)  
    if matched[1] >= 90:  
        return matched[0]
    else:
        return None


matched_companies = df_a["Company"].apply(fuzzy_match, args=(df_b["Company"].tolist(),))


df_filtered = df_a[matched_companies.notnull()]


df_filtered.to_csv("file_a_filtered.csv", index=False)
