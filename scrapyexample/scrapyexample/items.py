# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReleaseItem(scrapy.Item):
    name = scrapy.Field()
    version = scrapy.Field()
    link = scrapy.Field()
    summary = scrapy.Field()
