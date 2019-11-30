# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'travelbot'
    allowed_domains = ['nautaliaviajes.com']
    start_urls = [
        'https://www.nautaliaviajes.com/',
    ]

    def parse(self, response):
        #Remove XML namespaces
        response.selector.remove_namespaces()
        for element in response.xpath('//ul[@id="owl-carousel-caribe"]'):
            yield {
#               TODO:
#                ...the main functions...
#                The selectors have 4 methods:
#                xpath (): Returns a list of selectors, each representing the nodes by the xpath expression passed as an argument.
#                css (): Returns a list of selectors, each representing the nodes selected by the css () expression passed as an argument.
#                extract (): Returns a string (unicode) with the selected data (extract.first() only extracts the first date of the list).
#                re (): Returns a list of extracted strings when applying a regular expression passed as an argument.
#                ...check domain topology with xpath...
#                'all-text-nodes': element.xpath('string(string(//body))').extract_first()
#                'document-nodes-order': element.xpath('following:: *').extract_first()
#                'node_test': element.xpath('//li/div/div[4]/p/node()').extract_first()
#                'positional_predicate': element.xpath('( //body//div ) [1]').extract()
#                'position_ranges': element.xpath('//body//div//li[position()>1 and position()<last()]').extract()
#                'top-caribe-star': element.xpath('//footer//div[3]/div/div/ul/li[1]/a/text()').extract()
#                'location_path': element.xpath('//li/div/div[4]/p/text()').extract(), # sorted list, mixed targets!
#                'destination': element.xpath('//h3/a/text()').extract(),
#                'top-caribe': element.xpath('//footer//div[3]//a/text()').extract(),
#                ...check quantitative rates with count() function...
#                'paragraphs': element.xpath('count(//p)').extract_first(),
#                'attributes': element.xpath('count(//@*)').extract_first(),
#                ...paths found...
                'caribe_pack_destination': element.xpath('//li/div/h2/a/text()').extract_first(),
                'price': element.xpath('//li/div/div[4]/p[@class="frnv-price"]/text()').extract_first(),
#                'cruise_itinerary': element.css('body:nth-child(2)').extract(), # todo
                'port_of_destination': element.xpath('(//div[4]/p[2]/text())').extract_first(),
                'starting_price': element.xpath('string(//li/div/p)').extract_first(),
                'price': element.xpath('//li/div/p/text()').extract_first(),

            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

