import scrapy


class CosdnaScraperItem(scrapy.Item):
    name = scrapy.Field()
    composition = scrapy.Field()
