import scrapy

class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ["http://quotes.toscrape.com/"]

    def __init__(self):
        self.visited_urls = set()
        self.url_count = 0
        self.max_urls = 1000

    def parse(self, response):
        # 중복 URL 제거
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)

        # 수집 수 제한
        if self.url_count >= self.max_urls:
            return
        self.url_count += 1

        # 현재 depth 추적
        current_depth = response.meta.get('depth', 0)

        # 현재 페이지 정보 저장
        yield {
            'depth': current_depth,
            'url': response.url,
            'referer': response.request.headers.get('Referer', None).decode() \
                if response.request.headers.get('Referer') else None
        }

        # 다음 페이지 링크 탐색 (depth 제한 + 내부 링크만)
        if current_depth < 4:
            urls = response.css("a::attr(href)").getall()
            for url in urls:
                if url.startswith("/"):  # 내부 링크만
                    yield response.follow(url, callback=self.parse)
