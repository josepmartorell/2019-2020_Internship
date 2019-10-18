from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from first4spr.items import First4SprItem


class InfoempleoCrawler(CrawlSpider):
    name = 'InfoempleoCrawler'
    start_urls = ['https://www.infoempleo.com/trabajo/']
    allowed_domains = ['www.infoempleo.com']

    rules = (

        # regular expression of horizontal crawling
        Rule(LinkExtractor(allow=r'/*/')),
        # regular expression of vertical crawling
        Rule(LinkExtractor(allow=r'/*/'), callback='parse_items'),
    )

    # xml response parameter works into parse_items function
    def parse_items(self, response):
        item = ItemLoader(First4SprItem(), response)
        item.add_xpath('time', '//*ul/li/p[3]/text()')
        # by lambda we can extract a certain number of elements obtained through the text () method
        item.add_xpath('advertisements', '//*h2/a/text()', MapCompose(lambda l: 1[0]))
        yield item.load_item()

    # standalone commands: scrapy runspider spr_3.py --set=CLOSESPIDER_ITEMCOUNT=10
    # WARNING: Be careful with the item requests, notice that at the end of the script we define the amount of items
    # that we are going to take out, in order not to abuse making too many requests to the server due to the spider's
    # high speed :(

