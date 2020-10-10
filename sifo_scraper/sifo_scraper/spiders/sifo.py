# -*- coding: utf-8 -*-

import re

import scrapy
import langdetect
from langdetect.lang_detect_exception import LangDetectException

from . import sifo_data
from .. import items


def is_composition_in_en(composition):
    try:
        lang = langdetect.detect(composition)
    except LangDetectException:
        return False
    else:
        if lang == 'en':
            return True
        else:
            return False


class SifoSpider(scrapy.Spider):
    name = 'sifo'
    allowed_domains = ['sifo.ru']
    start_urls = sifo_data.urls

    def parse(self, response):
        products_links = response.css('.product-item a::attr(href)').getall()
        yield from response.follow_all(products_links, callback=self.parse_product_detail)

        pagination_links = response.css('.pagination a::attr(href)').getall()
        if pagination_links:
            yield from response.follow_all(pagination_links[:-2], callback=self.parse)

    def parse_product_detail(self, response):
        item = items.SifoItem()

        # product
        title = response.css('h1::text').extract()
        for word in sifo_data.stop_words:
            if title[0].lower().find(word) >= 0:
                return

        item['name'] = re.sub(r'\s{2,}', '', (re.sub(r'\([0-9-+. ]{2,}\)', '', (re.sub(r'\b[А-Яа-яё-]+\b', '', title[0]))))).strip()
        item['section'] = re.search(r'[А-Яа-яё- ]+', title[0]).group(0).strip()
        item['brand'] = response.css('[itemprop="brand"]::text').extract_first().strip()
        item['image'] = response.css('.thumbnail img::attr(src)').extract_first()
        possible_volume = response.css('#product').re(r'(Объем:\s)(\d+\s\w+)')
        another_possible_volume = response.css('#tab-description').re(r'\d{1,4}\s\w+\b')
        if possible_volume:
            item['volume'] = possible_volume[1]
        elif another_possible_volume:
            item['volume'] = another_possible_volume[0]
        else:
            item['volume'] = None

        # composition
        possible_composition = response.css('.ingr::text').extract()
        another_possible_composition = response.css('.Ingr::text').extract()

        # If there are compositions for a few products on the one page, don't process them.
        if len(possible_composition) > 1 or len(another_possible_composition) > 1:
            return
        if possible_composition and is_composition_in_en(possible_composition[0][8:-1]):
            item['composition'] = [re.sub(r'\*+', '', ingr).strip()
                                   for ingr in possible_composition[0][8:-1].lower().split(', ')]
        elif another_possible_composition and is_composition_in_en(another_possible_composition[0][8:-1]):
            item['composition'] = [re.sub(r'\*+', '', ingr).strip()
                                   for ingr in another_possible_composition[0][8:-1].lower().split(', ')]
        else:
            item['composition'] = None
            
        # shop
        item['current_price'] = int(response.css('.price-new').re(r'\d+')[0])
        item['link_to_product_page'] = response.request.url

        yield item
