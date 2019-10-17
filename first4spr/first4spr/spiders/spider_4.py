#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
# url to be scratched: https://www.lemonde.fr/international/
# This is a simple vertical and horizontal crawling essay on a job search portal,
# extracting news content of the news crawling the pages vertically and horizontally
# using beautifoulsoup package.
# standalone commands: scrapy runspider spider_4.py



import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from bs4 import BeautifulSoup
from scrapybot.items import ScrapybotItem


# type of spider and mechanisms
class LeMondeCrawler(CrawlSpider):
    name = 'lemondecrawler'
    allowed_domains = ['lemonde.fr']
    start_urls = ['https://www.lemonde.fr/international/']

    rules = (

        # horizontal crawling
        # <allow=r'/example/\d+'> the r is the regular expresion
        Rule(LinkExtractor(allow=r'/international/\d+'), follow=True),
        # vertical crawling
        Rule(LinkExtractor(allow=r'/international/article'), follow=True, callback='parse_items')
    )

    def parse(self, response):
        item = scrapy.loader.ItemLoader(ScrapybotItem(), response)
        # title
        item.add_xpath('title', '//h3/a[@class="teaser__link"]/text()')

        # we can not use xpath for the content because it is in another tag,
        # we must use beautiful soup instead
        soup = BeautifulSoup(response.body)
        article = soup.find(id='habillagepub')
        content = article.text
        item.add_value('content', content)
        yield item.load_item()

# scrapy runspider spider_4.py -o lemonde.csv -t csv
