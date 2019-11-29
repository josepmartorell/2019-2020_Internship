# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'travelbot'
    allowed_domains = ['nautaliaviajes.com']
    start_urls = [
        'https://www.nautaliaviajes.com/',
    ]

    def parse(self, response):
        for element in response.xpath('//ul[@id="owl-carousel-caribe"]'):
            yield {
#               TODO: xpath suit to investigate domain topology...
#                'all-text-nodes': element.xpath('string(string(//body))').extract_first()
#                'document-nodes-order': element.xpath('following:: *').extract_first()
#                'node_test': element.xpath('//li/div/div[4]/p/node()').extract_first()
#                'positional_predicate': element.xpath('( //body//div ) [1]').extract()
#                'position_ranges': element.xpath('//body//div//li[position()>1 and position()<last()]').extract()
#                'location_path': element.xpath('//li/div/div[4]/p/text()').extract()
#                'top-caribe-star': element.xpath('//footer//div[3]/div/div/ul/li[1]/a/text()').extract()
                'paragraphs': element.xpath('count(//p)').extract_first(),
                'attributes': element.xpath('count(//@*)').extract_first(),
                'destination': element.xpath('//h3/a/text()').extract(),
                'top-caribe': element.xpath('//footer//div[3]//a/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
