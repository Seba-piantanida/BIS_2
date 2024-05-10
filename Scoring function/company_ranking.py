import pandas as pd

linkedin_df = pd.read_csv('/Users/seba/Desktop/BIS_2/Scoring function/linkedin_scoring_companies.csv')
webpage_df = pd.read_csv('/Users/seba/Desktop/BIS_2/Scoring function/webpages_scoring.csv')

linkedin_df['normalized_score'] = ((linkedin_df['score'] - linkedin_df['score'].min()) / (linkedin_df['score'].max() - linkedin_df['score'].min()))
webpage_df['normalized_score'] = ((webpage_df['score'] - webpage_df['score'].min()) / (webpage_df['score'].max() - webpage_df['score'].min()))

linkedin_weight = 0.6
webpage_weight = 0.4  

linkedin_df['weighted_score'] = (linkedin_df['normalized_score'] * linkedin_weight * 10)
webpage_df['weighted_score'] = (webpage_df['normalized_score'] * webpage_weight * 10)

combined_df = pd.concat([linkedin_df[['Company', 'weighted_score']], webpage_df[['name', 'weighted_score']].rename(columns={'name': 'Company'})])
combined_df = combined_df.groupby('Company').sum().reset_index()

combined_df['RANK'] = combined_df['weighted_score'].rank(ascending=False)

combined_df = combined_df.sort_values(by='RANK')

combined_df['weighted_score'] = combined_df['weighted_score'].round(2)

combined_df.to_csv('combined_ranking.csv', index=False)
