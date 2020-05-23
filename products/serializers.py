import datetime

from rest_framework import serializers
from rest_framework.reverse import reverse
from django.utils import dateparse
import drf_dynamic_fields

from .models import Section, Product, IngredientsGroup, Ingredient, Composition, Shop, ProductInShop, Price
from creamy_korean.settings import HOST


class SectionSerializer(serializers.ModelSerializer):
    products_number = serializers.SerializerMethodField('get_products_number')
    subsections = serializers.SerializerMethodField('get_subsections')

    class Meta:
        model = Section
        fields = ['id', 'name', 'products_number', 'subsections']

    def get_products_number(self, instance):
        subsections = instance.get_most_nested()
        return Product.objects.filter(composition__isnull=False, section_id__in=subsections).count()
    
    def get_subsections(self, instance):
        serializer = SectionSerializer(instance.children.all(), many=True)
        return serializer.data


class ProductInShopSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()

    class Meta:
        model = ProductInShop
        fields = ['shop', 'availability', 'current_price', 'link_to_product_page', 'last_updated']


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['highest', 'lowest']


class ProductSerializer(drf_dynamic_fields.DynamicFieldsMixin, serializers.ModelSerializer):
    composition = serializers.StringRelatedField()
    prices = PriceSerializer(read_only=True)
    available_in_shops = ProductInShopSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'volume', 'image', 'section_id', 'composition', 'prices', 'available_in_shops']
