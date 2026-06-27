# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re
import sqlite3
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class CleanDataPipeline:
    """Clean and normalize scraped book data."""

    def process_item(self, item, spider):
        """Clean text, convert price to float, and normalize availability."""

        adapter = ItemAdapter(item)

        adapter["title"] = self._clean_text(adapter.get("title"))
        adapter["category"] = self._clean_text(adapter.get("category"))
        adapter["product_url"] = self._clean_text(adapter.get("product_url"))
        adapter["image_url"] = self._clean_text(adapter.get("image_url"))

        adapter["price"] = self._clean_price(adapter.get("price"))
        adapter["availability"] = self._clean_availability(adapter.get("availability"))

        return item

    @staticmethod
    def _clean_text(value):
        """Remove extra whitespace from text values."""

        if value is None:
            return ""

        return " ".join(str(value).split())

    @staticmethod
    def _clean_price(value):
        """Remove currency symbols and convert price to float."""

        if value is None:
            return 0.0

        cleaned_value = re.sub(r"[^\d.]", "", str(value))

        if not cleaned_value:
            return 0.0

        return float(cleaned_value)

    @staticmethod
    def _clean_availability(value):
        """Convert availability text into a boolean value."""

        if value is None:
            return False

        return "in stock" in str(value).strip().lower()


class ValidationPipeline:
    """Validate required fields before exporting or storing items."""

    required_fields = [
        "title",
        "price",
        "availability",
        "product_url",
        "image_url",
        "category",
    ]

    def process_item(self, item, spider):
        """Drop invalid items with missing required values."""

        adapter = ItemAdapter(item)

        for field in self.required_fields:
            if field not in adapter:
                raise DropItem(f"Missing field: {field}")

        if not adapter["title"]:
            raise DropItem("Missing book title")

        if not adapter["product_url"]:
            raise DropItem("Missing product URL")

        if not adapter["category"]:
            raise DropItem("Missing category")

        return item


class SQLiteStoragePipeline:
    """Store cleaned book data in a SQLite database."""

    def open_spider(self, spider):
        """Open database connection and prepare the books table."""

        db_path = Path(spider.settings.get("BOOKS_SQLITE_PATH"))
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        self.cursor.execute("DROP TABLE IF EXISTS books")

        self.cursor.execute(
            """
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                availability INTEGER NOT NULL,
                product_url TEXT NOT NULL,
                image_url TEXT NOT NULL,
                category TEXT NOT NULL,
                UNIQUE(product_url, category)
            )
            """
        )

        self.connection.commit()
        spider.logger.info("SQLite database initialized at %s", db_path)

    def process_item(self, item, spider):
        """Insert a cleaned book item into SQLite."""

        adapter = ItemAdapter(item)

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO books (
                title,
                price,
                availability,
                product_url,
                image_url,
                category
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                adapter["title"],
                adapter["price"],
                int(adapter["availability"]),
                adapter["product_url"],
                adapter["image_url"],
                adapter["category"],
            ),
        )

        self.connection.commit()
        return item

    def close_spider(self, spider):
        """Close the SQLite database connection."""

        self.connection.close()
        spider.logger.info("SQLite database connection closed")
