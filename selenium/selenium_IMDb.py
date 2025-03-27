import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 옵션 설정
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.imdb.com/chart/top/"
driver.get(url)

# 상세 정보 버튼 로딩 대기
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[aria-label^='See more information about']"))
)

info_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label^='See more information about']")

movies = []

# 영화 반복
for idx in range(min(250, len(info_buttons))):
    info_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label^='See more information about']")

    try:
        btn = info_buttons[idx]
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(0.5)
        btn.click()

        # 팝업 로딩 대기
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.prompt-title-text"))
        )
        time.sleep(0.5)

        # 제목
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h3.prompt-title-text").text
        except:
            title = "No Title"

        # 줄거리
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-3318d8db-2"))
            )
            desc = driver.find_element(By.CSS_SELECTOR, "div.sc-3318d8db-2").text
        except:
            desc = "No Description"

        # 장르
        try:
            genre_list = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='btp_gl'] li.ipc-inline-list__item")
            genre = ", ".join([g.text for g in genre_list if g.text.strip()])

        except:
            genre = "Unknown"

        # 평점 (팝업 내부에서 찾기)
        try:
            popup = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='promptable']"))
            )
            rating_element = popup.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating")
            rating = driver.execute_script("return arguments[0].textContent;", rating_element).strip()
        except:
            rating = "No Rating"

        # 감독
        try:
            people_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/name/']")
            director = people_links[0].text if people_links else "Unknown"
        except:
            director = "Unknown"

        # 영화 정보 저장
        movies.append({
            "title": title,
            "description": desc,
            "genre": genre,
            "rating": rating,
            "director": director
        })

    finally:
        # 팝업 닫기 처리
        try:
            close_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Close Prompt']"))
            )
            close_btn.click()
            WebDriverWait(driver, 7).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='promptable']"))
            )
            print("팝업 닫기 완료")
        except Exception as e:
            print(f"닫기 실패, ESC 시도 중: {e}")
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            try:
                WebDriverWait(driver, 5).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='promptable']"))
                )
                print("ESC로 팝업 닫기 성공")
            except:
                print("팝업 닫기 실패")

        time.sleep(1)

driver.quit()

# JSON 저장
with open("imdb_detailed_movies.json", "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=2)

# CSV 저장
with open("imdb_detailed_movies.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "description", "genre", "rating", "director"])
    writer.writeheader()
    writer.writerows(movies)
