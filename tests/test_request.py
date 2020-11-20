import os
from contextlib import contextmanager

import pytest
import scrapy
from scrapy.utils.test import get_crawler

from scrapy_requests import HtmlRequest, RequestsMiddleware


@contextmanager
def opened_middleware(crawler):
    mw = RequestsMiddleware.from_crawler(crawler)
    crawler.spider = crawler._create_spider('example')
    mw.spider_opened(crawler.spider)
    try:
        yield mw
    finally:
        mw.spider_closed(crawler.spider)


def test_configured():
    crawler = get_crawler()
    mw = RequestsMiddleware.from_crawler(crawler)
    assert mw.session is None


def test_crawl():
    crawler = get_crawler(settings_dict={})
    req1 = scrapy.Request(url='https://pythonclock.org/')
    req2 = HtmlRequest(url='https://pythonclock.org/', render=True)
    req3 = HtmlRequest(url='https://pythonclock.org/', render=True, options={
                       'sleep': 1, 'timeout': 12})

    with opened_middleware(crawler) as mw:
        assert mw.session is not None
        output = scrapy.Request('https://pythonclock.org/')

        # No HtmlRequest
        res = mw.process_request(req1, crawler.spider)
        assert res is None

        # render is True
        res = mw.process_request(req2, crawler.spider)
        assert res.body != output.body

        # Render is True and assigned options
        res = mw.process_request(req3, crawler.spider)
        count = res.xpath("//span[@class='countdown-amount']/text()").extract()[0]
        assert count == '0'
