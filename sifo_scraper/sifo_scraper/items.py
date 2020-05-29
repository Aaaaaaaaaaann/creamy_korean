import scrapy


class SifoItem(scrapy.Item):
    name = scrapy.Field()
    section = scrapy.Field()
    brand = scrapy.Field()
    image = scrapy.Field()
    volume = scrapy.Field()
    composition = scrapy.Field()
    current_price = scrapy.Field()
    link_to_product_page = scrapy.Field()
