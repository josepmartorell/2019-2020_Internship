#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class InfojobsItem(Item):
    time = Field()
    advertisements = Field()


class InfojobsCrawler(CrawlSpider):
    name = "infoempleoCrawler"
    start_urls = ["https://www.infoempleo.com/trabajo/"]
    allowed_domains = ['www.infoempleo.com']

    # crawl horizontally
    rules = (

        # regular expression of horizontal crawling
        Rule(LinkExtractor(allow=r'/*/')),
        # regular expression of vertical crawling
        Rule(LinkExtractor(allow=r'/*/'), callback='parse_items'),
    )

    # xml response parameter
    def parse_items(self, response):
        item = ItemLoader(InfojobsItem(), response)
        item.add_xpath('time', '//*ul/li/p[3]/text()')
        item.add_xpath('advertisements', '//*h2/a/text()', MapCompose(lambda l: 1[0]))
        yield item.load_item()


"""
scrapy runspider sample_04.py -o infojoempleo.csv -t csv --set=
CLOSESPIDER_ITEMCOUNT=10
"""
