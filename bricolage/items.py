# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

def remove_currency(value):
    return value.replace('\xa0 лв.', '')

def strip_text(value):
    return value.replace('\n', '').replace('\t', '')

class BricolageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field(input_processor = MapCompose(strip_text), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_currency, strip_text), output_processor = TakeFirst())
    pictures = scrapy.Field()
    characteristics = scrapy.Field()
    # stores = scrapy.Field()
    # link = scrapy.Field()
