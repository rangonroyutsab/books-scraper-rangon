from pathlib import Path

import scrapy

ALLOWED_DOMAINS = ["books.toscrape.com"]
START_URLS = ["https://books.toscrape.com/index.html"]


class BookSpider(scrapy.Spider):
    name = "book"

    # allowed_domains = ALLOWED_DOMAINS
    # start_urls = START_URLS

    async def start(self):
        for url in START_URLS:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
