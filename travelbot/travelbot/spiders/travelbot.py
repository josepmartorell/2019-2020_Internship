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
#                'destination': element.xpath('./span[@class="text"]/text()').extract_first(),
#                'stay': element.xpath('.//small[@class="author"]/text()').extract_first(),
                'price': element.xpath('//li/div/div[4]/p/text()').extract()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

#       script: scrapy crawl travelbot