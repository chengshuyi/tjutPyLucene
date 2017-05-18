# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TjutscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    _id = scrapy.Field()

    update=scrapy.Field()
    new_url=scrapy.Field()

    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    keyword = scrapy.Field()
    last_modified = scrapy.Field()
    next_scrawl_time=scrapy.Field()
