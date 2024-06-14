# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def process_category(value):
        value = ",".join(value)
        return value

class ImagesItem(scrapy.Item):

        name = scrapy.Field()
        category = scrapy.Field()
        image_urls = scrapy.Field()
        images = scrapy.Field()


