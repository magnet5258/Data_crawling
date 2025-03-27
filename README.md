# Data Crawling Pratice

## 🕷️ Scrapy Project - 웹 크롤링 연습

이 프로젝트는 Scrapy 프레임워크를 사용하여 웹 데이터를 크롤링하는 연습용 프로젝트입니다.  
연습 대상 사이트는 [quotes.toscrape.com](https://quotes.toscrape.com/)입니다.

---

### 📦 프로젝트 구조

```plaintext
mycrawler/
├── mycrawler/
│   ├── items.py             # 크롤링 데이터 구조 정의
│   ├── pipelines.py         # 데이터 후처리 로직
│   ├── settings.py          # 크롤러 설정
│   └── spiders/             # 스파이더 코드 (크롤링 로직)
│       ├── link_spider.py
│       ├── love_spider.py
│       └── quote_spider.py
├── scrapy.cfg               # Scrapy 설정 파일
├── requirements.txt         # 의존성 목록
└── README.md
```


---

### 🚀 실행 방법

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

### ⚙️ 주요 옵션 설명

| 옵션 | 설명 |
|------|------|
| `DEPTH_LIMIT=3` | 크롤링 최대 깊이를 3으로 제한 |
| `CLOSESPIDER_PAGE``COUNT=50` | 50페이지 크롤링 후 자동 종료 |
| `CLOSESPIDER_TIMEOUT=30` | 30초가 지나면 자동 종료 |

---

### 🧾 크롤링 대상 사이트

> ✅ [https://quotes.toscrape.com/](https://quotes.toscrape.com/)  
> 실습용으로 제공되는 크롤링 허용 사이트입니다.

---

### 🧪 스파이더 설명

- `quotes_spider.py`: 명언, 작가, 태그 수집
- `link_spider.py`: 내부 링크를 따라가며 전체 URL 구조 탐색 및 depth 기록
- `love_spider.py`: 'love' 태그의 작가, 명언, 생년월일 등을 수집

---

## 📌 동적 웹 페이지 vs 정적 웹 페이지

### 🔹 정적 웹 페이지 (Static Web Page)
- HTML 문서에 모든 데이터가 미리 포함되어 있어, 요청하면 그대로 클라이언트에 전달됨
- 브라우저가 별도의 자바스크립트 실행 없이 내용을 바로 렌더링
- 크롤링 시 별도 처리 없이 `requests`, `Scrapy` 등으로 바로 데이터 수집 가능

> 예시: `https://quotes.toscrape.com/`

---

### 🔹 동적 웹 페이지 (Dynamic Web Page)
- 초기 HTML 문서에는 데이터가 없고, 자바스크립트(JS)가 실행되면서 데이터가 렌더링됨
- 브라우저가 페이지 로드 후 JS를 통해 API 요청 또는 DOM 조작으로 콘텐츠를 채움
- 크롤링 시 `Selenium`이나 `Playwright`처럼 JS를 실행할 수 있는 도구 필요

> 예시: `https://quotes.toscrape.com/js/`, `https://www.imdb.com/chart/top/`

---

## 🔍 정적 vs 동적 웹 페이지 구분 방법

| 방법 | 설명 |
|------|------|
| 🔎 개발자 도구 (F12) → Network 탭 | 페이지 로드 시 HTML 내에 데이터가 존재하는지 확인 |
| 🔄 XHR 요청 확인 | JS로 비동기 요청을 보내고 데이터를 받아오는 경우 동적 페이지 가능성 ↑ |
| 🧪 View Page Source (`Ctrl+U`) | 페이지 소스에서 필요한 데이터가 보이면 정적, 없으면 동적 가능성 ↑ |
| ⚙️ 페이지 로딩 속도 | 일반적으로 정적 페이지가 더 빠름 (JS 실행 없음) |
| 🧠 요청 도구로 테스트 | `curl`, `requests`, `Scrapy` 등으로 수집했을 때 데이터가 보이면 정적 페이지 가능성 ↑ |

---

## ✅ 결론
- 정적 페이지: `Scrapy`로 충분히 처리 가능
- 동적 페이지: `Selenium` 등 JS 렌더링이 가능한 툴을 활용해야 함

