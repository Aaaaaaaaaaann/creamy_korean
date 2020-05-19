# -*- coding: utf-8 -*-
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

import scrapy
from products.models import Product, Ingredient, Composition, CompositionTemp, SectionTemp, ProductInShop
from extras.composition_processing import process_composition


class DuplicatesFilter:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.names_seen:
            raise scrapy.exceptions.DropItem(f'Duplicate item found: {item["name"]}')
        self.names_seen.add(item['name'])
        self.sections.add(item['section'])
        return item

    # def close_spider(self, spider):
    #     all_products_sifo = ProductInShop.objects.filter(shop_id=1)
    #
    #     for product in all_products_sifo:
    #         if product not in self.names_seen:
    #             product.availability = False
    #             product.save()


class SifoModelsPipeline:
    def __init__(self):
        self.compositions_for_processing = []

    def process_item(self, item, spider):
        product, created = Product.objects.get_or_create(name=item['name'], defaults={'brand': item['brand'],
                                                                                      'volume': item['volume'],
                                                                                      'image': item['image']})
        SectionTemp.objects.get_or_create(product=product, defaults={'section': item['section']})
        ProductInShop.objects.update_or_create(shop_id=1, product=product,
                                               defaults={'link_to_product_page': item['link_to_product_page'],
                                                         'current_price': item['current_price']})
        processed_composition = Composition.objects.filter(product=product)
        if not processed_composition:
            composition, created = CompositionTemp.objects.get_or_create(product=product,
                                                                         defaults={'ingredients': item['composition']})
            if item['composition']:
                self.compositions_for_processing.append(composition)
        return item

    def close_spider(self, spider):
        process_composition(self.compositions_for_processing)
