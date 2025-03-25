import scrapy

class QuoteSpider(scrapy.Spider):
    name = "quote_spider"
    start_urls = ['https://quotes.toscrape.com/']

    def __init__(self):
        self.seen_quotes = set()

    def parse(self, response):
        page_num = response.meta.get('page_num', 1)

        quotes = response.css('div.quote')
        for quote in quotes:
            text = quote.css('span.text::text').get()
            if text not in self.seen_quotes:
                self.seen_quotes.add(text)
                yield {
                    'text': text,
                    'author': quote.css('small.author::text').get(),
                    'tags': quote.css('div.tags a.tag::text').getall()
                }

        if page_num < 20:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(
                    next_page, 
                    callback=self.parse, 
                    meta={'page_num': page_num + 1}
                )
