## BIS 2
# SPONSOR ANALYSIS

This repository contains three main functionalities, organized into separate folders. Below are detailed descriptions and instructions for each functionality.

## Scoring Functions

This module calculates the scores of companies based on their web pages and LinkedIn profiles.

### Directory Structure

- `profiles_json`: Save the JSON files of LinkedIn profiles in this folder.

- `webpages`: Save the text files of web pages in this folder.

### How to Execute

1\. Ensure you have the LinkedIn JSON profiles saved in the `profiles_json` folder.

2\. Ensure you have the web page text files saved in the `webpages` folder.

3\. Execute the main script to calculate the scores.

4\. The results will be available in the `data` folder as:

   - `combined_ranking.csv`: Final ranking using LinkedIn and web pages.

   - `webpages_score.csv`: Scores of the web pages.

   - `linkedin_scoring_companies.csv`: Scores of LinkedIn profiles.

### Customizing Weights

To modify the weights of words and categories, edit the `keywords.json` file according to your requirements.

## HTML Crawler

This module contains a Python script that crawls web pages.

### How to Execute

1\. Ensure you have a CSV file containing the URLs to be crawled.

2\. Execute the `html-crawler.py` script.

3\. The content of each URL will be saved in the `webpages` folder as `company_name.txt` files.

## Stats

This module contains a word counter for counting keywords in different categories.

### How to Execute

1\. Run the script and choose the desired command:

   - `g` for global (counts keywords in both LinkedIn and web pages).

   - `l` for LinkedIn (counts keywords in LinkedIn profiles).

   - `w` for web pages (counts keywords in web pages).

2\. The results will be produced as CSV files based on the selected command.

## Summary of Files and Folders

- `Scoring functions/`: Contains the main scoring functionality.

  - `profiles_json/`: Save LinkedIn profile JSON files here.

  - `webpages/`: Save web page text files here.

  - `data/`: Output folder for results.

  - `keywords.json`: Configuration file for modifying weights.

- `HTML Crawler/`: Contains the HTML crawler script.

  - `html-crawler.py`: Python script for crawling web pages.

- `Stats/`: Contains the word counter functionality.

By following the above instructions, you can effectively use the functionalities provided in this repository. Feel free to customize the configuration files as needed to suit your specific requirements.
