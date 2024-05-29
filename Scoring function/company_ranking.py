import pandas as pd

def main():
    # Read input CSV files
    linkedin_df = pd.read_csv('data/linkedin_scoring_companies.csv')
    webpage_df = pd.read_csv('data/webpages_scoring.csv')

    # Normalize scores
    linkedin_df['normalized_score'] = ((linkedin_df['score'] - linkedin_df['score'].min()) / 
                                       (linkedin_df['score'].max() - linkedin_df['score'].min())) * 3
    webpage_df['normalized_score'] = ((webpage_df['score'] - webpage_df['score'].min()) / 
                                      (webpage_df['score'].max() - webpage_df['score'].min())) * 3

    # Define weights
    linkedin_weight = 0.7
    webpage_weight = 0.3

    # Apply weights to normalized scores
    linkedin_df['weighted_score'] = linkedin_df['normalized_score'] * linkedin_weight
    webpage_df['weighted_score'] = webpage_df['normalized_score'] * webpage_weight

    # Merge dataframes, retaining necessary columns
    linkedin_df_renamed = linkedin_df[['Company', 'weighted_score', 'normalized_score', 'ESG', 'GENDER EQUALITY', 'VOLLEYBALL']]
    linkedin_df_renamed = linkedin_df_renamed.rename(columns={'normalized_score': 'l_score'})

    webpage_df_renamed = webpage_df[['name', 'weighted_score', 'normalized_score', 'ESG', 'GENDER EQUALITY', 'VOLLEYBALL']]
    webpage_df_renamed = webpage_df_renamed.rename(columns={'name': 'Company', 'normalized_score': 'w_score'})

    combined_df = pd.concat([linkedin_df_renamed, webpage_df_renamed])

    # Group by Company and sum scores
    combined_df = combined_df.groupby('Company', as_index=False).agg({
        'weighted_score': 'sum',
        'l_score': 'sum',
        'w_score': 'sum',
        'ESG': 'sum',
        'GENDER EQUALITY': 'sum',
        'VOLLEYBALL': 'sum'
    })

    # Calculate total words combined
    combined_df['total_words'] = combined_df['ESG'] + combined_df['GENDER EQUALITY'] + combined_df['VOLLEYBALL']

    # Adjust ESG, GENDER EQUALITY, and VOLLEYBALL values
    combined_df['ESG'] = (combined_df['ESG'] / combined_df['total_words']) * 2
    combined_df['GENDER EQUALITY'] = (combined_df['GENDER EQUALITY'] / combined_df['total_words']) * 3
    combined_df['VOLLEYBALL'] = (combined_df['VOLLEYBALL'] / combined_df['total_words']) * 1

    # Drop the total_words column
    combined_df = combined_df.drop(columns=['total_words'])

    # Sort by weighted score
    combined_df = combined_df.sort_values(by='weighted_score', ascending=False)

    # Round scores
    combined_df['weighted_score'] = combined_df['weighted_score'].round(2)
    combined_df['l_score'] = combined_df['l_score'].round(2)
    combined_df['w_score'] = combined_df['w_score'].round(2)
    combined_df['ESG'] = combined_df['ESG'].round(2)
    combined_df['GENDER EQUALITY'] = combined_df['GENDER EQUALITY'].round(2)
    combined_df['VOLLEYBALL'] = combined_df['VOLLEYBALL'].round(2)

    # Save to CSV
    combined_df.to_csv('data/combined_ranking.csv', index=False)

if __name__ == '__main__':
    main()
