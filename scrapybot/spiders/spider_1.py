#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule # just "Rule" is to implement scrapy rules
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor # to implement scrapy rules
from scrapybot.items import ScrapybotItem


class MySpider(CrawlSpider):
    name = 'craigsCrawler'
    allowed_domains = ['sfbay.craigslist.org']
    start_urls = ['http://sfbay.craigslist.org/search/npo']

    # implementing scrapy rules
#    rules = (
#        Rule(LinkExtractor(allow=(),
#             restrict_xpaths=('//a[@class="button next"]',)),
#             callback="parse_items", follow=True),
#    )

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.xpath('//ul[@class="rows"]')
        items = []
        for title in titles:
            item = ScrapybotItem()
            item['title'] = title.select('li/p/a/text()').extract()
            item['link'] = title.xpath('li[@class="result-row"]/a/@href').extract()
            items.append(item)
        return items

# $ scrapy runspider spider_1.py -o craigs.csv -t csv
