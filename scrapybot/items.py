# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapybotItem(scrapy.Item):
# define the fields for your item here like:
#
    url = scrapy.Field()
    id = scrapy.Field()
    job_title = scrapy.Field()
#    location = scrapy.Field()
#    date = scrapy.Field()
    link = scrapy.Field()
#    job_attributes = scrapy.Field()
#    job_description = scrapy.Field()
#    course_title = scrapy.Field()

    pass
