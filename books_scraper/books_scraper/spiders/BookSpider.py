from pathlib import Path

import scrapy


class BookSpider(scrapy.Spider):
    name = "book"

    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    async def start(self):
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        categories = response.css("ul.nav.nav-list > li > ul > li").getall()

        
