from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from first4spr.items import First4SprItem


class NetacadSpider(Spider):

    name = 'NetacadSpider'
    allowed_domains = ['netacad.com']
    start_urls = ['https://www.netacad.com/']

    rules = (
        Rule(LinkExtractor(allow=(),
             restrict_xpaths=('//section[@class="block-section-main-menu"]',)),
             callback="parse_items", follow=True),
    )

    def parse(self, response):
        sel = Selector(response)
        titles = sel.xpath('//ul[@class="nav navbar-nav list list list--inline"]')

        for i, elem in enumerate(titles):
            item = ItemLoader(First4SprItem(), elem)
            item.add_xpath('courses', 'li[@class="first expanded dropdown 847"]/ul/li/a/text()')
            item.add_value('id', i + 1)
            yield item.load_item()