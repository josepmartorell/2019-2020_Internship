# -*- coding: utf-8 -*-
import scrapy
from squezz.items import SquezzItem


class SquezzSpuder(scrapy.Spider):
    name = 'squezz'
    allowed_domains = ['viajesloreto.com']
    start_urls = ['https://viajesloreto.com/']

    def parse(self, response):
        item = SquezzItem()
        item['link'] = response.xpath('string(//h2/a/@href)').extract()
#        item['price'] = response.css('.package-price::text').extract()
        item['price'] = response.css('.package-price::text').extract()

        return item
