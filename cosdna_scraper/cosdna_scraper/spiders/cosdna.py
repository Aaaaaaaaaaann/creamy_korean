# -*- coding: utf-8 -*-
import scrapy

from .. import items
from products.models import Product


class CosdnaSpider(scrapy.Spider):
    name = 'cosdna'
    allowed_domains = ['cosdna.com']
    current_product = None

    def start_requests(self):
        urls = []
        for entry in Product.objects.filter(composition_temp__processed=False):
            self.current_product = entry.name
            query = ''
            for word in entry.name.split():
                query += word + '+'
            urls.append(f'https://www.cosdna.com/eng/product.php?q={query[:-1]}&sort=featured')

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        product_link = response.css('.pl-0 a::attr(href)').get()
        if product_link:
            yield response.follow(product_link, callback=self.parse_product_composition)

    def parse_product_composition(self, response):
        item = items.CosdnaScraperItem()
        item['name'] = self.current_product
        item['composition'] = [ingr.lower() for ingr in response.css('.colors::text').getall()]
        yield item
