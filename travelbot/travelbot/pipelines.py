# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#
# Item Pipeline can be used to validate scraped data, check duplicate data,
# or insert the data into databases such as Mysql, PostgreSQL or MongoDB.
import json

from scrapy.exceptions import DropItem


class TravelbotPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class PricePipeline(object):

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item.get('price'):
            if item.get('price_excludes_vat'):
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)


#class JsonWriterPipeline(object):

#    def open_spider(self, spider):
#        self.file = open('items.jl', 'w')

#    def close_spider(self, spider):
#        self.file.close()

#    def process_item(self, item, spider):
#        line = json.dumps(dict(item)) + "\n"
#        self.file.write(line)
#        return item

