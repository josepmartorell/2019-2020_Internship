# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapybotItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    advertisment = scrapy.Field()
    course = scrapy.Field()
    id = scrapy.Field()
    pass
