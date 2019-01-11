# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo as pymongo


class GushiciPipeline(object):
    def process_item(self, item, spider):
        # print('=> ', item['content'])
        return item

class InputMongodbPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        db = self.client['gushici_db']
        self.post = db['shiwen6']

    def __del__(self):
        self.client.close()
        print("InputMongodbPipeline.__del__")

    def process_item(self, item, spider):
        postItem = dict(item)
        self.post.insert(postItem)
        return item