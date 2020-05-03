# -*- coding: utf-8 -*-
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

from products.models import Ingredient, Product, Composition, CompositionTemp
from extras.composition_processing import process_composition


class CosdnaScraperPipeline(object):
    def __init__(self):
        self.compositions_for_processing = []

    def process_item(self, item, spider):
        if item['composition']:
            product = Product.objects.get(name=item['name'])
            composition, crated = CompositionTemp.objects.update_or_create(product=product,
                                                                           defaults={'ingredients': item['composition']})
            self.compositions_for_processing.append(composition)
        return item

    def close_spider(self, spider):
        process_composition(self.compositions_for_processing)
