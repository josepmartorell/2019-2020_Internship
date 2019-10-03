#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# url to be scratched: https://www.netacad.com/
# This spider is programmed to extract information about Cisco Networking Academy courses.
# standalone commands:
# username@hostname$ scrapy runspider spider_2.py -o netacad.csv -t csv

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapybot.items import ScrapybotItem



class NetacadSpider(Spider):

    name = 'netacadSpider'
    start_urls = ['https://www.netacad.com/']

# first we create the selector that we have named "sel", and then we set all 'div' with 'id' 'badge-collection'
# if no into a wrapper dont need close the tag like this: './/div[@class="badge-collection"]/div'

    def parse(self, response):
        sel = Selector(response)
        courses = sel.xpath('.//ul[@class="dropdown-menu"]')

# iterate onto the questions, and at the same time, in parallel we increase an integer variable to set it into id.

        for i, elem in enumerate(courses):
            item = ItemLoader(ScrapybotItem(), elem)
            item.add_xpath('course_title', 'a/@title')
            item.add_value('id', i + 1)
            yield item.load_item()

