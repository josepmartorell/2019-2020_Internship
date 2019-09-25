#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapybot.items import ScrapybotItem



class NetacadSpider(Spider):

    name = 'netacadSpider'
    start_urls = ['https://www.netacad.com/']

    def parse(self, response):
        # first we create the selector, an then we set all 'div' with 'id' 'badge-collection'
        # if no into a wrapper dont need close the tag: eg.  './/div[@class="badge-collection"]/div'
        sel = Selector(response)
        courses = sel.xpath('.//div[@class="badge-collection"]')

        # iterate onto the questions
        for i, elem in enumerate(courses):
            item = ItemLoader(ScrapybotItem(), elem)
            item.add_xpath('course', 'a/@title')
            item.add_value('id', i + 1)
            yield item.load_item()

# $ scrapy runspider spider_2.py -o netacad.csv -t csv
