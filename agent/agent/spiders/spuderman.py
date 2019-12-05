#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector

class WebSampleItem(Item):
    title = Field()
    link = Field()

class AgentSpider(Spider):
    name = "agent"
    allowed_domains = ["finance.yahoo.com"]
    start_urls = ["http://finance.yahoo.com/quote/AAPL?p=AAPL"]

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.xpath("//table/thead/tr/th[@scope='col']")
        items = []
        for title in titles:
            item = WebSampleItem()
            item["title"] = title.xpath('a/text()').extract()
            item["link"] = title.xpath('a/@href').extract()
            items.append(item)
        return items




