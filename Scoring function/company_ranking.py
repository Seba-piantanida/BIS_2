import pandas as pd

def main():
    linkedin_df = pd.read_csv('data/linkedin_scoring_companies.csv')
    webpage_df = pd.read_csv('data/webpages_scoring.csv')

    linkedin_df['normalized_score'] = ((linkedin_df['score'] - linkedin_df['score'].min()) / (linkedin_df['score'].max() - linkedin_df['score'].min()))*10
    webpage_df['normalized_score'] = ((webpage_df['score'] - webpage_df['score'].min()) / (webpage_df['score'].max() - webpage_df['score'].min()))*10

    linkedin_weight = 0.7
    webpage_weight = 0.3

    linkedin_df['weighted_score'] = (linkedin_df['normalized_score'] * linkedin_weight)
    webpage_df['weighted_score'] = (webpage_df['normalized_score'] * webpage_weight)

    combined_df = pd.concat([linkedin_df[['Company', 'weighted_score', 'normalized_score']].rename(columns= {'normalized_score': 'l_score'}), webpage_df[['name', 'weighted_score','normalized_score']].rename(columns={'name': 'Company', 'normalized_score': 'w_score'})])

    combined_df = combined_df.groupby('Company').sum().reset_index()


    combined_df = combined_df.sort_values(by='weighted_score', ascending= False)

    combined_df['weighted_score'] = combined_df['weighted_score'].round(2)
    combined_df['l_score'] = combined_df['l_score'].round(2)
    combined_df['w_score'] = combined_df['w_score'].round(2)

    combined_df.to_csv('data/combined_ranking.csv', index=False)

if __name__ == '__main__':
    main()
