# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class First4SprItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    job  = scrapy.Field()
    link = scrapy.Field()
    courses = scrapy.Field()
    offer = scrapy.Field()
    jobs = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass
