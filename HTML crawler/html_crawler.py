import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

input_file = 'complete_companies_list_with_urls_2.csv'
# Create a folder to store text files if it doesn't exist
folder_name = "webpages"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Function to scrape text from a webpage
def scrape_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(soup.stripped_strings)
            return text
        else:
            print(f"Failed to retrieve content from {url}")
            return None
    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return None

def scrape_text_with_selenium(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') 
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')  
        options.add_argument('--disable-dev-shm-usage')  
        
        driver = webdriver.Chrome( options=options)
        
        driver.get(url)
        driver.implicitly_wait(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = ' '.join(soup.stripped_strings)
        
        driver.quit()
        
        return text
    except Exception as e:
        print(f"An error occurred while scraping {url} with Selenium: {e}")
        return None
    
# Open the CSV file and iterate through each row
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  # Skip the header row
    for row in reader:
        company_name = row[0]
        links = row[1:]
        company_file = os.path.join(folder_name, f"{company_name}.txt")
        with open(company_file, 'w', encoding='utf-8') as f:
            for i, link in enumerate(links):
                text = scrape_text_with_selenium(link)
                if text:
                    f.write(text + '\n\n')
                    print(f"Saved text from {link} to {company_file}")