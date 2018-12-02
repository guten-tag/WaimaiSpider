# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Waimai.items import WaimaiItem
from Waimai.items import RateItem
from Waimai.items import TypeItem
import codecs
import json

class WaimaiPipeline(object):
    def __init__(self):
        self.file = codecs.open("ShopInfo.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        if isinstance(item, WaimaiItem):
            lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(lines)
            return item

    def spider_closed(self, spider):
        self.file.close()

class RatePipeline(object):
    def __init__(self):
        self.file = codecs.open("ShopRate.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        if isinstance(item, RateItem):
            lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(lines)
            return item

    def spider_closed(self, spider):
        self.file.close()

class TypePipeline(object):
    def __init__(self):
        self.file = codecs.open("ShopType.json", "w", encoding="utf-8")

    def process_item(self, item, spider):
        if isinstance(item, TypeItem):
            lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(lines)
            return item

    def spider_closed(self, spider):
        self.file.close()