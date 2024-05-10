import pandas as pd

df = pd.read_csv('linkedin_scoring_employee.csv')
grouped_df = df.groupby('Company').agg({'name': 'count', 'total_words': 'sum', 'ESG': 'sum', 'GENDER EQUALITY': 'sum', 'VOLLEYBALL': 'sum'})
grouped_df.columns = ['N of Employees', 'Total Words', 'ESG', 'GENDER EQUALITY', 'VOLLEYBALL']
grouped_df_sorted = grouped_df.sort_values(by='VOLLEYBALL', ascending=False)
grouped_df_sorted.to_csv('linkedin_scoring_companies.csv')

