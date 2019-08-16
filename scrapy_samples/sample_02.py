#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import Spider
from scrapy.selector import Selector

class WebSampleItem(Item):
    title = Field()
    link = Field()

class MitreAttackSpider(Spider):
    name = "mitreAttack"
    allowed_domains = ["attack.mitre.org"]
    start_urls = ["https://attack.mitre.org/"]

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

# $ scrapy runspider sample_07.py -o mitreAttack.csv -t csv

