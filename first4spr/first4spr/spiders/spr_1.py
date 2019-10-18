from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from first4spr.items import First4SprItem


class CraigsCrawler(CrawlSpider):
    name = 'CraigsCrawler'
    allowed_domains = ['sfbay.craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/search/sfc/sof']

    rules = (
        Rule(LinkExtractor(allow=(),
             restrict_xpaths=('//li[@class="result-row"]',)),
             callback="parse_items", follow=True),
    )

    @staticmethod
    def parse_items(response):
        hxs = Selector(response)
        titles = hxs.xpath('//ul[@class="rows"]')
        items = []
        for title in titles:
            item = First4SprItem()
            item['url'] = response.url
            item['job'] = title.select('//p/a/text()').extract()
            item['link'] = title.xpath('//li[@class="result-row"]/p/a/@href').extract()
            items.append(item)
        return items
