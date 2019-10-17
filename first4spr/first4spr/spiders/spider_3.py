#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# url to be scratched: https://www.infoempleo.com/trabajo/
# This is a simple vertical and horizontal crawling essay on a job search portal.
# standalone commands: scrapy runspider spider_3.py --set=CLOSESPIDER_ITEMCOUNT=10
# WARNING: Be careful with the item requests, notice that at the end of the script we define the amount of items
# that we are going to take out, in order not to abuse making too many requests to the server due to the spider's high speed :(

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapybot.items import ScrapybotItem


class InfojobsCrawler(CrawlSpider):
    name = 'infoempleoCrawler'
    start_urls = ['https://www.infoempleo.com/trabajo/']
    allowed_domains = ['www.infoempleo.com']

    # crawl horizontally
    rules = (

        # regular expression of horizontal crawling
        Rule(LinkExtractor(allow=r'/*/')),
        # regular expression of vertical crawling
        Rule(LinkExtractor(allow=r'/*/'), callback='parse_items'),
    )

    # xml response parameter works into parse_items function
    def parse_items(self, response):
        item = ItemLoader(ScrapybotItem(), response)
        item.add_xpath('time', '//*ul/li/p[3]/text()')
        # by lambda we can extract a certain number of elements obtained through the text () method
        item.add_xpath('advertisements', '//*h2/a/text()', MapCompose(lambda l: 1[0]))
        yield item.load_item()

# scrapy runspider spider_3.py -o infojoempleo.csv -t csv --set=CLOSESPIDER_ITEMCOUNT=10
