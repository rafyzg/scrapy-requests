import logging
from typing import Union

from requests_html import AsyncHTMLSession
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings

from .request import HtmlRequest


logger = logging.getLogger(__name__)


class RequestsMiddleware:
    """Scrapy middleware handling requests using requests-html library"""

    # Disabling pyppeteer logs to stdout
    logging.getLogger("websockets").setLevel(20)
    logging.getLogger("pyppeteer").setLevel(20)

    def __init__(self):
        self.session = None
        self.settings = get_project_settings().get(
            "DEFAULT_SCRAPY_REQUESTS_SETTINGS", {}
        )

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize middleware"""
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def spider_opened(self, spider: Spider) -> None:
        """Open HTMLSession when spider starts"""
        try:
            self.session = AsyncHTMLSession(**self.settings)
        except TypeError:
            self.session = AsyncHTMLSession()
            raise AttributeError(
                "DEFAULT_SCRAPY_REQUESTS_SETTINGS is not "
                + "aligned with requests-html session settings. \n"
                + "Please check www.github.com/psf/requests-html/blob/026c4e5217cfc8347614148aab331d81402f596b/requests_html.py#L759"
            )

    async def spider_closed(self, spider: Spider) -> None:
        """Close HTMLSession when spider closes"""
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
