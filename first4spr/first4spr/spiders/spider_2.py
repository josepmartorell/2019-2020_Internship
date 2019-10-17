#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# url to be scratched: https://www.netacad.com/
# This spider is programmed to extract simple information about Cisco Networking Academy courses.
# standalone commands: scrapy runspider spider_2.py

from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapybot.items import ScrapybotItem


class NetacadSpider(Spider):

    name = 'netacadspider'
    allowed_domains = ['netacad.com']
    start_urls = ['https://www.netacad.com/']

    rules = (
        Rule(LinkExtractor(allow=(),
             restrict_xpaths=('//section[@class="block-section-main-menu"]',)),
             callback="parse_items", follow=True),
    )

# first we create the selector that we have named "sel", and then we set all 'div' with 'id' 'badge-collection'
# if no into a wrapper dont need close the tag like this: './/div[@class="badge-collection"]/div'

    def parse(self, response):
        sel = Selector(response)
        titles = sel.xpath('//ul[@class="nav navbar-nav list list list--inline"]')

# iterate onto the questions, and at the same time, in parallel we increase an integer variable to set it into id.

        for i, elem in enumerate(titles):
            item = ItemLoader(ScrapybotItem(), elem)
            item.add_xpath('courses', 'li[@class="first expanded dropdown 847"]/ul/li/a/text()')
            item.add_value('id', i + 1)
            yield item.load_item()

# scrapy runspider spider_2.py -o netacad.csv -t csv

