# 🕷️ Scrapy Project - 웹 크롤링 연습

이 프로젝트는 Scrapy 프레임워크를 사용하여 웹 데이터를 크롤링하는 연습용 프로젝트입니다.  
연습 대상 사이트는 [quotes.toscrape.com](https://quotes.toscrape.com/)입니다.

---

## 📦 프로젝트 구조

```
mycrawler/
├── mycrawler/
│   ├── items.py             # 크롤링 데이터 구조 정의
│   ├── pipelines.py         # 데이터 후처리 로직
│   ├── settings.py          # 크롤러 설정
│   └── spiders/             # 스파이더 코드 (크롤링 로직)
│				├── link_spider.py
│       ├── love_spider.py
│       └── quote_spider.py
├── scrapy.cfg               # Scrapy 설정 파일
├── requirements.txt         # 의존성 목록
└── README.md
```

---

## 🚀 실행 방법

### 1. 가상 환경 생성 (선택)
```bash
python -m venv venv
source venv/bin/activate       # 윈도우는 venv\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. Spider 실행

#### 📘 명언 수집 크롤러 (`quotes_spider`)
```bash
scrapy crawl quotes -o quotes.json
```

#### 🔗 전체 링크 구조 탐색 (`link_spider`)
```bash
scrapy runspider mycrawler/spiders/link_spider.py -o links.json \
  -s DEPTH_LIMIT=3 \
  -s CLOSESPIDER_PAGECOUNT=50 \
  -s CLOSESPIDER_TIMEOUT=30
```

#### 💖 Love 태그 명언 + 작가 정보 크롤러 (`love_spider`)
``` bash
scrapy crawl love_spider -o love_quotes.json
```

---

## ⚙️ 주요 옵션 설명

| 옵션 | 설명 |
|------|------|
| `DEPTH_LIMIT=3` | 크롤링 최대 깊이를 3으로 제한 |
| `CLOSESPIDER_PAGECOUNT=50` | 50페이지 크롤링 후 자동 종료 |
| `CLOSESPIDER_TIMEOUT=30` | 30초가 지나면 자동 종료 |

---

## 🧾 크롤링 대상 사이트

> ✅ [https://quotes.toscrape.com/](https://quotes.toscrape.com/)  
> 실습용으로 제공되는 크롤링 허용 사이트입니다.

---

## 🧪 스파이더 설명

- `quotes_spider.py`: 명언, 작가, 태그 수집
- `link_spider.py`: 내부 링크를 따라가며 전체 URL 구조 탐색 및 depth 기록
- `love_spider.py`: 'love' 태그의 작가, 명언, 생년월일 등을 수집

---
