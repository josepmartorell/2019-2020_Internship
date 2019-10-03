#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# url to be scratched: https://sfbay.craigslist.org/search/sfc/sof
# This spider is programmed to track information about software job offers in San Francisco Bay.
# standalone commands:
# username@hostname$ scrapy runspider spider_1.py -o craigs.csv -t csv

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapybot.items import ScrapybotItem


class MySpider1(CrawlSpider):
    name = 'sanFranciscoCrawler'
    allowed_domains = ['sfbay.craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/search/sfc/sof']

# implementing rules. Instead "parse_items" callbacks with "parse" should invoke directly scrapybot engine.
# parameter follow is set to true to keep the same rules for the next items.

    rules = (
        Rule(LinkExtractor(allow=(),
             restrict_xpaths=('//li[@class="result-row"]',)),
             callback="parse_items", follow=True),
    )

    @staticmethod
    def parse_items(response):
        hxs = Selector(response)
        titles = hxs.xpath('//ul[@class="rows"]')
        items = []
        for title in titles:
            item = ScrapybotItem()
            item['url'] = response.url
            item['job_title'] = title.select('//p/a/text()').extract()
            item['link'] = title.xpath('//li[@class="result-row"]/p/a/@href').extract()
            items.append(item)
        return items


