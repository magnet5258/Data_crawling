import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# 브라우저 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://quotes.toscrape.com/js/")  # 첫 페이지

all_quotes = []

while len(all_quotes) < 100:
    time.sleep(1.5)  # JS 렌더링 대기

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    quotes = soup.select('.quote')

    for q in quotes:
        text = q.select_one('.text').text
        author = q.select_one('.author').text
        all_quotes.append({"text": text, "author": author})
        if len(all_quotes) >= 100:
            break

    # 다음 페이지가 존재하면 클릭
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
        next_button.click()
    except NoSuchElementException:
        break  # 다음 버튼이 없으면 종료

driver.quit()

# CSV 저장
with open("quotes_100_click.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author"])
    writer.writeheader()
    writer.writerows(all_quotes)

# JSON 저장
with open("quotes_100_click.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, indent=2, ensure_ascii=False)
