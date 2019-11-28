# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from squezz.items import SquezzItem


class SquezzSpuder(CrawlSpider):
    name = "squezz_spuder"
    allowed_domains = ["exprimeviajes.com"]
    start_urls = ['https://www.exprimeviajes.com/']

    # Pattern for entries that meet the desired format:
    rules = [Rule(LxmlLinkExtractor(allow=['']), callback='process_response')]
#    rules = [Rule(LxmlLinkExtractor(allow=['',], deny=('tarifas-error\.php',))),
#    Rule(LxmlLinkExtractor(allow=('item\.php',)), callback='process_response'),]

    def process_response(self, response):
        item = SquezzItem()
        print(response)
#        item['title'] = response.xpath("//h2/a/text()").extract()
#        item['title'] = response.xpath("//div[contains(@class, 'grid-100')]//h1/text()").extract()
        item['title'] = response.xpath("//header/h2/a/text()").extract()

        return item