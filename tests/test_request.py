import os
from contextlib import contextmanager

import nest_asyncio
import pytest
import scrapy
from scrapy.utils.reactor import install_reactor
from scrapy.utils.test import get_crawler

from scrapy_requests import HtmlRequest, RequestsMiddleware

# Installing Asyncio Selector
install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")


@contextmanager
def opened_middleware(crawler):
    mw = RequestsMiddleware.from_crawler(crawler)
    crawler.spider = crawler._create_spider("example")
    mw.spider_opened(crawler.spider)
    yield mw


def test_configured():
    crawler = get_crawler()
    mw = RequestsMiddleware.from_crawler(crawler)
    assert mw.session is None


@pytest.mark.asyncio
async def test_crawl():
    nest_asyncio.apply()  # Required for async tests
    crawler = get_crawler(
        settings_dict={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
        }
    )
    req1 = scrapy.Request(url="https://pythonclock.org/")
    req2 = HtmlRequest(url="https://pythonclock.org/", render=True)
    req3 = HtmlRequest(
        url="https://pythonclock.org/", render=True, options={"sleep": 1, "timeout": 12}
    )

    with opened_middleware(crawler) as mw:
        assert mw.session is not None
        output = scrapy.Request("https://pythonclock.org/")

        # No HtmlRequest
        res = await mw.process_request(req1, crawler.spider)
        assert res is None

        # render is True
        res = await mw.process_request(req2, crawler.spider)
        assert res.body != output.body

        # Render is True and assigned options
        res = await mw.process_request(req3, crawler.spider)
        count = res.xpath("//span[@class='countdown-amount']/text()").extract()[0]
        assert count == "0"

        await mw.spider_closed(crawler.spider)
