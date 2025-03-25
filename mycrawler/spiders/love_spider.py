import scrapy

class LoveQuoteSpider(scrapy.Spider):
    name = "love_spider"
    start_urls = ["https://quotes.toscrape.com/tag/love/"]

    def parse(self, response):
        quotes = response.css('div.quote')

        for quote in quotes:
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            author_link = quote.css('span a::attr(href)').get()
            
            # 작가 페이지로 이동하며 meta로 quote 정보 전달
            yield response.follow(
                author_link,
                callback=self.parse_author,
                meta={'text': text, 'author': author}
            )

        # love 태그도 여러 페이지가 있을 수 있으므로 next 처리
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        # 이전 페이지에서 전달받은 정보
        text = response.meta['text']
        author = response.meta['author']

        # 작가 상세 정보 추출
        born_date = response.css('.author-born-date::text').get()
        born_location = response.css('.author-born-location::text').get()
        description = response.css('.author-description::text').get()

        yield {
            'text': text,
            'author': author,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }
