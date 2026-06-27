import random

import scrapy

from books_scraper.items import BookItem


class BookSpider(scrapy.Spider):
    """Spider for scraping selected books from every category on Books to Scrape."""

    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/index.html"]

    def parse(self, response):
        """Parse the main page and extract category links."""

        category_links = response.css(
            "div.side_categories ul.nav-list > li > ul > li > a"
        )

        self.logger.info(f"Found {len(category_links)} categories.")

        for category in category_links:
            category_name = category.css("::text").get().strip()
            category_url = category.css("::attr(href)").get()

            if not category_name or not category_url:
                self.logger.warning(f"Skipped invalid category: {category}")
                continue

            yield response.follow(
                category_url,
                callback=self.parse_category,
                meta={
                    "category": category_name,
                    "book_urls": [],
                },
            )

    def parse_category(self, response):
        """Parse a category page, extract book URLs, and follow pagination."""

        category = response.meta["category"]
        book_urls = response.meta["book_urls"]

        page_book_urls = self._extract_book_urls(response)
        book_urls.extend(page_book_urls)

        next_page_url = response.css("li.next a::attr(href)").get()

        if next_page_url:
            yield response.follow(
                next_page_url,
                callback=self.parse_category,
                meta={"category": category, "book_urls": book_urls},
            )
        else:
            # No more pages, yield the final list of book URLs
            yield from self.parse_books(response, category, book_urls)

        selected_book_urls = self._select_random_books(
            book_urls, count=5, category=category
        )

        self.logger.info(
            f"Selected {len(selected_book_urls)} out of {len(book_urls)} books from category '{category}'."
        )

        for book_url in selected_book_urls:
            yield scrapy.Request(
                url=book_url,
                callback=self.parse_book,
                meta={"category": category},
            )

    def parse_book(self, response):
        """Parse a book page and extract relevant information."""

        category = response.meta["category"]

        title = self._clean_text(response.css("div.product_main h1::text").get())
        price = self._clean_text(response.css("p.price_color::text").get())
        availability = self._clean_text(response.css("p.availability::text").get())
        product_url = response.url
        image_url = response.urljoin(
            response.css("div.carousel-inner img::attr(src)").get()
        )

        yield BookItem(
            title=title,
            price=price,
            availability=availability,
            product_url=product_url,
            image_url=image_url,
            category=category,
        )
        

    def _extract_book_urls(self, response):
        """Extract absolute product URLs from the current category page."""

        relative_urls = response.css("article.product_pod h3 a::attr(href)").getall()
        return [response.urljoin(url) for url in relative_urls]

    def _select_random_books(self, book_urls, count, category):
        """Select random book URLs from a category."""

        if not book_urls:
            self.logger.warning("Category '%s' has no books", category)
            return []

        if len(book_urls) < count:
            self.logger.warning(
                "Category '%s' has only %d books. Selecting all available books.",
                category,
                len(book_urls),
            )
            return book_urls

        return random.sample(book_urls, count)

    @staticmethod
    def _clean_text(value):
        """Normalize whitespace from a string or list of strings."""

        if value is None:
            return ""

        if isinstance(value, list):
            value = " ".join(text.strip() for text in value if text.strip())

        return " ".join(str(value).split())
