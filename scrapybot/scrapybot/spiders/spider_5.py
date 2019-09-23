#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# extracting the title of the news and the content of the news
# from different tags to crawl the pages vertically and horizontally


import scrapy
from scrapy.item import Item
from scrapy.item import Field
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from bs4 import BeautifulSoup


# contents to extract
class LeMondeItem(Item):
    title = Field()
    content = Field()


# type of spider and mechanisms
class LeMondeCrawler(CrawlSpider):
    name = "leMondecrawler"
    allowed_domains = ['lemonde.fr']
    start_urls = ["https://www.lemonde.fr/international/"]

    rules = (

        # horizontal crawling
        # <allow=r'/example/\d+'> the r is the regular expresion
        Rule(LinkExtractor(allow=r'/international/\d+'), follow=True),
        # vertical crawling
        Rule(LinkExtractor(allow=r'/international/article'), follow=True, callback='parse_items')
    )

    def parse_items(self, response):
        item = scrapy.loader.ItemLoader(LeMondeItem(), response)
        # title
        item.add_xpath('title', '//h3/a[@class="teaser__link"]/text()')

        # we can not use xpath for the content because it is in another tag,
        # we must use beautiful soup instead
        soup = BeautifulSoup(response.body)
        article = soup.find(id="habillagepub")
        content = article.text
        item.add_value('content', content)

        yield item.load_item()


"""
scrapy runspider sample_05.py -o lemonde.csv -t csv
"""