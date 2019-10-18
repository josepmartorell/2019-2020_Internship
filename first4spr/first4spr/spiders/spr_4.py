import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from bs4 import BeautifulSoup
from first4spr.items import First4SprItem


class LeMondeCrawler(CrawlSpider):
    name = 'LeMondeCrawler'
    allowed_domains = ['lemonde.fr']
    start_urls = ['https://www.lemonde.fr/international/']

    rules = (

        # horizontal crawling
        Rule(LinkExtractor(allow=r'/international/\d+'), follow=True),
        # vertical crawling
        Rule(LinkExtractor(allow=r'/international/article'), follow=True, callback='parse_items')
    )

    def parse(self, response):
        item = scrapy.loader.ItemLoader(First4SprItem(), response)
        # title
        item.add_xpath('title', '//h3/a[@class="teaser__link"]/text()')
        # we can not use xpath for the content because it is in another tag,
        # we must use beautiful soup instead
        soup = BeautifulSoup(response.body)
        article = soup.find(id='habillagepub')
        content = article.text
        item.add_value('content', content)
        yield item.load_item()