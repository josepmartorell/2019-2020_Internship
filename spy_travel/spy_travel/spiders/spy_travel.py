import scrapy
from spy_travel.items import SpyTravelItem

class SpyTravel(scrapy.Spider):
    name = 'spy_travel'
    allowed_domains = ['nautaliaviajes.com']
    start_urls = ['https://www.nautaliaviajes.com/']

    def start_requests(self):
        yield scrapy.Request('https://www.nautaliaviajes.com/viajes', self.parse)
        yield scrapy.Request('https://www.nautaliaviajes.com/cruceros', self.parse)
        yield scrapy.Request('https://www.nautaliaviajes.com/viajes-caribe', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').getall():
            yield SpyTravelItem(title=h3)

        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse)