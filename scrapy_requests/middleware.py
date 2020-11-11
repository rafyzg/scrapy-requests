from scrapy.http import HtmlResponse
from scrapy import signals

from requests_html import HTMLSession

from .request import HtmlRequest

logger = logging.getLogger(__name__)


class RequestsMiddleware:
    """Scrapy middleware handling requests using requests-html library"""

    def __init__(self):
        self.session = None

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize middleware"""
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened,
                                signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider: object) -> None:
        """Open HTMLSession when spider starts"""
        self.session = HTMLSession()

    def process_request(self, request, spider):
        """Process a request using requests-html if applicable"""

        if not isinstance(request, HtmlRequest):
            return None

        page = self.session.get(request.url)

        render = getattr(spider, 'render', False)
        if not render:
            return HtmlResponse(
                r.url,
                body=page.html.html,
                enconding='utf-8',
                request=request
            )

        params = getattr(spider, 'options', dict())

        page.html.render(**params)
        request.meta.update({'page': page})

        return HtmlResponse(
            r.url,
            body=page.html.html,
            request=request
        )
