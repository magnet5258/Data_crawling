class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ["http://quotes.toscrape.com/"]

    def __init__(self):
        self.visited_urls = set()
        self.url_count = 0
        self.max_urls = 1000  # 수집 제한

    def parse(self, response):
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)

        if self.url_count >= self.max_urls:
            return
        self.url_count += 1

        current_depth = response.meta.get('depth', 0)
        yield {
            'depth': current_depth,
            'url': response.url,
        }

        if current_depth < 3:
            urls = response.css("a::attr(href)").getall()
            for url in urls:
                if url.startswith("/"):  # 내부 링크만
                    yield response.follow(url, callback=self.parse)
