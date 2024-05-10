from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import csv
import traceback
import random

def check_URLS(driver: webdriver):
    driver.get("https://www.google.com")
    input("check google page and press enter")
    valid_urls = []
    with open("URL_short_google.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        urls = [row[0] for row in reader]
    index = 0
    for url in urls:
        
        try:
            search_box = driver.find_element(By.NAME, "q")
            search_box.clear()
            search_box.send_keys(f'https://www.linkedin.com/{url}/')
            search_box.submit()
            time.sleep(random.uniform(3,6))
            try:
                captcha_element = driver.find_element(By.XPATH, '//*[contains(text(), "I nostri sistemi hanno rilevato un traffico insolito proveniente dalla rete del tuo computer.")]')
                print(captcha_element)
                print("CAPTCHA challenge detected!")
                input()
            except:
                print("No CAPTCHA challenge detected.")
            try:
                elements = driver.find_elements(By.XPATH, f'//a[@jsname="UWckNb"]')
                
                print(url)
                for element in elements:
                    if url in element.get_attribute("href"):
                        print(f"found URL: {url}!")
                        valid_urls.append(element.get_attribute("href"))
                
            except:
                print("Element not found.")
        except Exception as e:{
            input('error detected fix and press enter to resume')

        }
        index += 1
        if index >= 50:
            break

    with open("valid_linkedin_urls_copy.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for valid_url in valid_urls:
            writer.writerow([valid_url])



driver = webdriver.Chrome()


check_URLS(driver)
# Close the browser
input()
driver.quit()


