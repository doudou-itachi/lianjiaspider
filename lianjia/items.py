# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    resblock_price_url = scrapy.Field()
    resblock_name = scrapy.Field()
    resblock_type = scrapy.Field()
    resblock_status = scrapy.Field()
    resblock_location = scrapy.Field()
    resblock_room = scrapy.Field()
    resblock_area = scrapy.Field()
    resblock_tag = scrapy.Field()
    resblock_price = scrapy.Field()
    resblock_second = scrapy.Field()
    detail_url = scrapy.Field()



