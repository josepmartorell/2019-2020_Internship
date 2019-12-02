# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'travelbot'
    allowed_domains = ['nautaliaviajes.com']
    start_urls = [
        'https://www.nautaliaviajes.com/',
    ]

    def parse(self, response):
        # Remove XML namespaces
        response.selector.remove_namespaces()
        for element in response.xpath('//ul[@id="owl-carousel-caribe"]'):
            yield {
                # </todo: "xpath matching results".
                # The selectors have 4 methods:
                # xpath (): Returns a list of selectors, each representing the nodes by the xpath
                # expression passed as an argument.
                # css (): Returns a list of selectors, each representing the nodes selected by the css ()
                # expression passed as an argument.
                # extract (): Returns a string (unicode) with the selected data.
                # re (): Returns a list of extracted strings when applying a regular expression passed as an argument.
                # set .extract() to extract_first() ones the xpath is found.

                # quantitative rates
                'paragraphs': element.xpath('count(//p)').extract_first(),
                'attributes': element.xpath('count(//@*)').extract_first(),

                # caribe
                'caribe_pack_destination': element.css('.dotted > a::text').extract_first(),
                'caribe_pack_price': element.xpath('//li/div/div[4]/p[@class="frnv-price"]/text()').extract_first(),

                # cruise
                # todo: "cruise_ininerary returns the eigth couple of first items with the estructure itinerary/origin".
                'cruise_itinerary': element.xpath('//div[4]/p[string(b)]/text()').extract_first(), # trace
                'cruise_port_of_destination': element.xpath('(//div[4]/p[2]/text())').extract_first(),
                'cruise_starting_price': element.xpath('string(//li/div/p)').extract_first(),
                'cruise_price': element.xpath('//li/div/p/text()').extract_first(),

                # travel
                'travel_destination': element.xpath('//li/div[1]/p[1]/a/text()').extract_first(),
                'travel_hotel': element.xpath('//li/div[1]/p[2]/text()').extract_first(),
                'travel_price': element.xpath('//li/p/text()').extract_first(),

                # organized
                # todo: "trips/price in range 1 to the 20 items missing new york 1 and portugal 10 with green tag".
                'organized_trips': element.xpath('//li/div[1]/div[2]/p[1]/text()').extract_first(), # trace
                'organized_price': element.xpath('//li/div/div[2]/div[2]/p[2]/text()').extract_first(),  # trace
                # stay in range from item 1 to the 20 NO missing new york at 1 and portugal at 10 with green tag".
                'organized_stay': element.xpath('//p[2]/span/text()').extract(),

                # journey
                'journey_destination': element.xpath('//li/div/div[3]/h3/a/text()').extract_first(),
                # todo: "journey_stay matches the last ten values of the returned list".
                'journey_stay': element.xpath('//div[4]/p[string(b)]/text()').extract_first(), # trace
                'journey_price': element.xpath('//li/div/div[4]/p[2]/span/text()').extract_first(),

                # beach
                # todo: "beach_destination in range from item 11 to the end "
                'beach_destination': element.xpath('//p/a/text()').extract_first(), # trace
                'beach_hotel': element.xpath('/li/div/div[2]/span').extract(), #
                #'beach_stars': element.xpath('').extract(), #
                #'beach_accommodation': element.xpath('').extract(), #
                #'beach_price': element.xpath('').extract(), #

                # hotel
                #'hotel_accommodation': element.xpath('//h3/a/text()').extract_first(),

            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

                # todo/>