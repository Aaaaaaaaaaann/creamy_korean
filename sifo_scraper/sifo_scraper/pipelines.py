# -*- coding: utf-8 -*-
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

import re
import logging
import os

import scrapy
from django.core.exceptions import ObjectDoesNotExist

from products.models import Product, Ingredient, Composition, CompositionTemp, SectionTemp, ProductInShop
from sifo_scraper.settings import SCRAPY_BASE_DIR


class DuplicatesFilter:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.names_seen:
            raise scrapy.exceptions.DropItem(f'Duplicate item found: {item["name"]}')
        self.names_seen.add(item['name'])
        return item

    def close_spider(self, spider):
        all_products_sifo = ProductInShop.objects.filter(shop_id=1)

        for product in all_products_sifo:
            if product not in self.names_seen:
                product.availability = False
                product.save()


class ModelsPipeline:
    def __init__(self):
        self.compositions_for_processing = []

    def add_to_log(self, /, ingredient, product):
        logging.basicConfig(filename=os.path.join(SCRAPY_BASE_DIR, 'ingredients.log'), level=logging.WARNING,
                            format='%(message)s')
        logging.warning(f'Not matched: {ingredient=}, {product=}')

    def process_item(self, item, spider):
        product, created = Product.objects.get_or_create(name=item['name'], defaults={'brand': item['brand'],
                                                                                      'volume': item['volume'],
                                                                                      'image': item['image']})
        SectionTemp.objects.get_or_create(product=product, defaults={'section': item['section']})
        ProductInShop.objects.update_or_create(shop_id=1, product=product,
                                               defaults={'link_to_product_page': item['link_to_product_page'],
                                                         'current_price': item['current_price']})
        if item['composition']:
            composition, created = CompositionTemp.objects.get_or_create(product=product,
                                                                         defaults={'ingredients': item['composition']})
            processed_composition = Composition.objects.filter(product=product)
            if not processed_composition:
                self.compositions_for_processing.append(composition)
        return item

    def close_spider(self, spider):
        for composition in self.compositions_for_processing:
            ingrs_ids = []
            ingredients = composition.ingredients
            product = composition.product
            for ingr in ingredients:
                try:
                    substance = Ingredient.objects.get(name__iexact=ingr)
                except ObjectDoesNotExist:
                    try:
                        substance = Ingredient.objects.get(
                            name__iexact=(re.sub(r'\s{2,}', ' ', (re.sub(r'\([0-9a-z- ]+\)', '', ingr))).strip()))
                    except ObjectDoesNotExist:
                        self.add_to_log(ingr, product.name)
                    else:
                        ingrs_ids.append(substance.pk)
                else:
                    ingrs_ids.append(substance.pk)
            if len(ingrs_ids) == len(ingredients):
                Composition.objects.create(product=product, ingredients=ingrs_ids)
                CompositionTemp.objects.filter(product=product).update(processed=True)
