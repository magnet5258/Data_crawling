import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

base_url = "https://quotes.toscrape.com/js/page/{}/"
all_quotes = []
page = 1

while len(all_quotes) < 100:
    driver.get(base_url.format(page))
    time.sleep(1.5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    quotes = soup.select('.quote')
    
    if not quotes:
        break

    for q in quotes:
        text = q.select_one('.text').text
        author = q.select_one('.author').text
        all_quotes.append({"text": text, "author": author})
        if len(all_quotes) >= 100:
            break

    page += 1

driver.quit()

# CSV 저장
with open("quotes_100.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author"])
    writer.writeheader()
    writer.writerows(all_quotes)

# JSON 저장
with open("quotes_100.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, indent=2, ensure_ascii=False)
