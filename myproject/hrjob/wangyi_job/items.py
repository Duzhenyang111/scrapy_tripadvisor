# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

    
class BarDetailItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    cuisine = scrapy.Field()
    phone = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    rating = scrapy.Field()
    reviews_nr = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    website = scrapy.Field()