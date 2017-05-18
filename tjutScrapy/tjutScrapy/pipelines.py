# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from tjutScrapy.MySql import MySql

class TjutscrapyPipeline(object):

    def __init__(self):
        self.mysql=MySql()
    
    def process_item(self, item, spider):
        if item['new_url']:
            self.mysql.insert(item)
        if item['update']:
            self.mysql.update(item)

