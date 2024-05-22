import pandas as pd

def main():
    df = pd.read_csv('data/linkedin_scoring_employee.csv')

    # Calculate the weighted average score based on the total number of words
    df['score'] = round((df['score'] * df['total_words']).groupby(df['Company']).transform('sum') / df.groupby('Company')['total_words'].transform('sum'), 2)

    grouped_df = df.groupby('Company').agg({'name': 'count', 'total_words': 'sum','score': 'first', 'ESG': 'sum', 'GENDER EQUALITY': 'sum', 'VOLLEYBALL': 'sum', })
    grouped_df.columns = ['N of Employees', 'Total Words','score', 'ESG', 'GENDER EQUALITY', 'VOLLEYBALL']
    grouped_df_sorted = grouped_df.sort_values(by='score', ascending=False)
    grouped_df_sorted.to_csv('data/linkedin_scoring_companies.csv')


if __name__ == '__main__':
    main()