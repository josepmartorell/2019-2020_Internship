#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector


class CraigslistSampleItem(Item):
    title = Field()
    link = Field()


class MySpider(CrawlSpider):
    name = "craigsCrawler"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = ["http://sfbay.craigslist.org/search/npo"]

    # implementing scrapy rules
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = Selector(response)
        titles = hxs.xpath('//ul[@class="rows"]')
        items = []
        for title in titles:
            item = CraigslistSampleItem()
            item["title"] = title.select('li/p/a/text()').extract()
            item["link"] = title.xpath("li[@class='result-row']/a/@href").extract()
            items.append(item)
        return(items)

# $ scrapy runspider sample_03.py -o craigs.csv -t csv
