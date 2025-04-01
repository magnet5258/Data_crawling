from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os

# 필터 키워드 목록
FILTER_KEYWORDS = ["통나무집", "캠핑장", "최고의 전망", "저택"]

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 필요시 주석처리
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Airbnb 기본 검색 페이지로 이동
driver.get("https://www.airbnb.co.kr/")
time.sleep(5)

# 결과 저장 디렉토리
output_dir = "./Airbnb_results"
os.makedirs(output_dir, exist_ok=True)

# 스크롤 함수
def scroll_to_bottom(scroll_pause=2, max_scroll=20):
    prev_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == prev_height:
            print(f"⏹ 스크롤 멈춤 - 더 이상 로딩된 항목 없음 ({i+1}회)")
            break
        prev_height = new_height

# 카테고리 필터 순회
for keyword in FILTER_KEYWORDS:
    category_results = []

    try:
        filter_button = driver.find_element(By.XPATH, f"//*[text()='{keyword}']")
        driver.execute_script("arguments[0].scrollIntoView(true);", filter_button)
        time.sleep(1)
        filter_button.click()

        # 스크롤 반복
        scroll_to_bottom(scroll_pause=2, max_scroll=10)  # 횟수 조절 가능

        # 숙소 카드 수집
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="card-container"]')
        print(f"총 숙소 수: {len(cards)}")

        for card in cards:
            try:
                lines = card.text.strip().split('\n')

                location = "정보 없음"
                distance = "정보 없음"
                price = "정보 없음"
                rating = "정보 없음"
                guest_preferred = "없음"

                for line in lines:
                    if "게스트 선호" in line:
                        guest_preferred = "있음"
                    elif "km 거리" in line or "m 거리" in line:
                        distance = line
                    elif "★" in line or "점" in line:
                        rating = line
                    elif "₩" in line and "/박" in line:
                        price = line
                    elif location == "정보 없음" and not any(kw in line for kw in ["게스트", "거리", "점", "₩"]):
                        location = line

                url = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                if not url.startswith("http"):
                    url = "https://www.airbnb.co.kr" + url

                category_results.append({
                    "카테고리": keyword,
                    "위치": location,
                    "거리": distance,
                    "평점": rating,
                    "가격": price,
                    "게스트 선호": guest_preferred,
                    "URL": url
                })

            except Exception as inner_e:
                print(f"숙소 처리 중 에러: {inner_e}")
                continue

        # 저장
        df = pd.DataFrame(category_results)
        file_name = f"Airbnb_{keyword}.csv"
        file_path = os.path.join(output_dir, file_name)
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"저장 완료: {file_name} ({len(df)}개)")

    except Exception as e:
        print(f"'{keyword}' 필터 클릭 실패: {e}")
        continue

driver.quit()
print("\n모든 카테고리 크롤링 완료")
