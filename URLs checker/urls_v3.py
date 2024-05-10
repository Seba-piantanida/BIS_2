from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import random

scroll_script = """
var scrollStep = 250; // Define scroll step
var delay = 100; // Define delay between steps

function scrollDown() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop < document.body.scrollHeight - window.innerHeight) {
        window.scrollBy(0, scrollStep);
        setTimeout(scrollDown, delay);
    }
}

scrollDown();
"""

def print_valid(urls, num):
    with open(f"valid_linkedin_urls_{num}.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for valid_url, text_after_dash in urls:
            writer.writerow((valid_url, text_after_dash))

def save_done_urls(urls, index):
    return

def extract_text_after_dash(element):
    try:
        anchor_element = element.find_element(By.TAG_NAME, 'h3')
        if anchor_element:
            text = anchor_element.text
            parts = text.split("-")
            if len(parts) > 1:
                print(parts[1].strip())
                return parts[1].strip()
            
        return ""
    except Exception as e:
        print(e)
        return ''

def check_captcha(driver: webdriver):
    if 'google.com/sorry' in driver.current_url:
        print('captcha detected solve to continue')
        while(True):
            if 'google.com/sorry' in driver.current_url:
                time.sleep(5)
            else:
                break

def check_URLS(driver: webdriver):
    driver.get("https://www.google.com")
    
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "L2AGLb"))
        )
        button.click()
    except:
        input("Check the Google page and press enter")

    valid_urls = []
    with open("URL_short_google.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        urls = [row[0] for row in reader]
    
    file_num = int(input('enter file output number: '))
    start_line = int(input("Enter the start line number: "))
    end_line = int(input("Enter the end line number: "))

    # Limit the range of lines to check
    urls_to_check = urls[start_line:end_line]

    index = 0
    for url in urls_to_check:
        try:
            search_box = driver.find_element(By.NAME, "q")
            search_box.clear()
            search_box.send_keys(f'https://www.linkedin.com/{url}/')
            search_box.submit()
            
            check_captcha(driver)
            
            time.sleep(random.uniform(20, 50))
            
            try:
                elements = driver.find_elements(By.XPATH, f'//a[@jsname="UWckNb"]')
                
                print(f'{index}-checking {url} :')
                
                for element in elements:
                    href = element.get_attribute("href")
                    if url in href:
                        text_after_dash = extract_text_after_dash(element)
                        valid_urls.append((href, text_after_dash)) 
                
                elements[0].click()
                driver.execute_script(scroll_script)
                time.sleep(random.uniform(100, 200))  
            except:
                print("Element not found.")
                print_valid(valid_urls, file_num)
                valid_urls = []
        except Exception as e:
            print(f"Error: {e}")
            print_valid(valid_urls, file_num)
            save_done_urls(urls, index)
            valid_urls = []
            input('Error detected. Press enter to resume after fixing.')

        # Navigate back to Google search results
        driver.execute_script("window.history.go(-1)")
        
        index += 1
        
        # Emulate human behavior by taking breaks
        if index % 13 == 0:
            print('coffee break')
            time.sleep(random.uniform(300, 600))
            print_valid(valid_urls, file_num)
            save_done_urls(urls, index)
            valid_urls = []
        
        if index % 50 == 0:
            print('coffee break')
            time.sleep(random.uniform(600, 700))
            print_valid(valid_urls, file_num)
            save_done_urls(urls, index)
            valid_urls = []

        if index >= end_line - start_line:
            break

    print_valid(valid_urls, file_num)
    save_done_urls(urls, index)

driver = webdriver.Chrome()


check_URLS(driver)
print('done!')
# Close the browser
input()
driver.quit()


