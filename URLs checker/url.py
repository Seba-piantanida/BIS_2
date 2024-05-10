from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv

user = "lordgiaruz@gmail.com"
pw = "trota2001"

def check_urls(driver, num):
    interval_time = 5
    valid_urls = []
    num_limits = num

    try:
        
        if "https://www.linkedin.com/" not in driver.current_url:
                
            driver.get("https://www.linkedin.com/")
            
            input("Please log in to LinkedIn manually. Once logged in, press Enter to continue...")
        
        driver.delete_all_cookies()
        with open("URL_short_google.csv", "r+") as csvfile:
            reader = csv.reader(csvfile)

            lines = list(reader)
            csvfile.seek(0)

            with open("valid_linkedin_urls.csv", "a", newline="") as outputfile:
                writer = csv.writer(outputfile)
                index = 0
                for row in lines:
                    if index >= int(num_limits):
                        break
                    url = row[0].strip()
                    

                    driver.get(url)
                    time.sleep(interval_time)

                    if url in driver.current_url:
                        valid_urls.append(driver.current_url)
                        writer.writerow([driver.current_url]) 
                    elif  "https://www.linkedin.com/404/" in driver.current_url:
                        print(f"Invalid URL: {url} current index: {index}")
                    else:
                        res = input("Linkedin disconnected, fix and press enter to restart (press q to stop)")
                        if res == 'q':
                            break
                        
                    index += 1

                with open("LinkedIn_URLs_Only.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    for row in lines[index:]:  
                        writer.writerow(row)

    except Exception as e:
        print("An error occurred:", str(e))
        with open("LinkedIn_URLs_Only.csv", "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    for row in lines[index:]:  
                        writer.writerow(row)
    
#options = Options()
#options.add_argument("user-data-dir=/Users/seba/Library/Application Support/Google/Chrome/")
#driver = webdriver.Chrome(options=options)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)
while True:
    
    
    num_to_check = input("how many to check? ") 
    check_urls(driver, num_to_check)
    restart = input("restart the check? y/n ")
    if restart != 'y':
        break
    
    

