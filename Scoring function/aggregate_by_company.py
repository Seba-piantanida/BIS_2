import pandas as pd

df = pd.read_csv('linkedin_scoring_employee.csv')

# Calculate the weighted average score based on the total number of words
df['Weighted Avg Score'] = round((df['score'] * df['total_words']).groupby(df['Company']).transform('sum') / df.groupby('Company')['total_words'].transform('sum'), 2)

grouped_df = df.groupby('Company').agg({'name': 'count', 'total_words': 'sum', 'ESG': 'sum', 'GENDER EQUALITY': 'sum', 'VOLLEYBALL': 'sum', 'Weighted Avg Score': 'first'})  # Use the first value of Weighted Avg Score
grouped_df.columns = ['N of Employees', 'Total Words', 'ESG', 'GENDER EQUALITY', 'VOLLEYBALL', 'Weighted Avg Score']
grouped_df_sorted = grouped_df.sort_values(by='Weighted Avg Score', ascending=False)
grouped_df_sorted.to_csv('linkedin_scoring_companies.csv')
