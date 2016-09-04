# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    brewery = scrapy.Field()
    country = scrapy.Field()
    style = scrapy.Field()
    abv = scrapy.Field()
    ibu = scrapy.Field()
    volume = scrapy.Field()
    purchase_url = scrapy.Field()
