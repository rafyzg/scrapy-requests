import logging
from typing import Union

from requests_html import AsyncHTMLSession
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider

from .request import HtmlRequest

logger = logging.getLogger(__name__)


class RequestsMiddleware:
    """Scrapy middleware handling requests using requests-html library"""

    # Disabling pyppeteer logs to stdout
    logging.getLogger("websockets").setLevel(20)
    logging.getLogger("pyppeteer").setLevel(20)

    def __init__(self):
        self.session = None

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize middleware"""
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider: Spider) -> None:
        """Open HTMLSession when spider starts"""
        self.session = AsyncHTMLSession()

    async def spider_closed(self, spider: Spider) -> None:
        await self.session.close()

    async def process_request(
        self, request, spider: Spider
    ) -> Union[None, HtmlResponse]:
        """Process a request using requests-html if applicable"""

        if not isinstance(request, HtmlRequest):
            return None

        page = await self.session.get(request.url)

        request.meta.update({"page": page})

        render = getattr(request, "render", False)
        if not render:
            return HtmlResponse(
                url=request.url, body=page.html.html, request=request, encoding="utf-8"
            )

        params = getattr(request, "options", dict())

        await page.html.arender(**params)

        return HtmlResponse(
            url=request.url, body=page.html.html, request=request, encoding="utf-8"
        )
