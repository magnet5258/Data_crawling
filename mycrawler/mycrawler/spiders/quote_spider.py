class QuoteSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        # 현재 페이지 번호 추적
        page_num = response.meta.get('page_num', 1)

        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall()
            }

        # 다음 페이지가 있고, 페이지 수 제한 안 넘으면 계속 탐색
        if page_num < 3:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(
                    next_page, 
                    callback=self.parse, 
                    meta={'page_num': page_num + 1}
                )
