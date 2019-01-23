# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from . import dbsettings

class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    collection_name = 'threads'
    
   

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(dbsettings.CONNECT_STRING)
        self.db = self.client["misc"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'title':item['title']},dict(item),upsert=True)
        logging.debug("Inserted into MongoDB")
        return item