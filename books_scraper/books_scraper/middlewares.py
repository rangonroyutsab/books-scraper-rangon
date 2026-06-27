# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random


class RandomUserAgentMiddleware:
    """Middleware to set a random User-Agent for each request."""

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
    ]

    def process_request(self, request, spider):
        """Set a random User-Agent header for each request."""

        request.headers["User-Agent"] = random.choice(self.USER_AGENTS)
