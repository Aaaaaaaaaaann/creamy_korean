import datetime

from rest_framework import serializers
from django.utils import dateparse

from .models import Section, Product, IngredientsGroup, Ingredient, Composition, Shop, ProductInShop


class SectionSerializer(serializers.ModelSerializer):
    products_number = serializers.SerializerMethodField('get_products_number')
    subsections = serializers.SerializerMethodField('get_subsections')
    products_list = serializers.HyperlinkedIdentityField(view_name='products_list', lookup_field='slug')

    class Meta:
        model = Section
        fields = ['name', 'products_number', 'subsections', 'products_list']

    def get_products_number(self, instance):
        all_products = 0
        
        def collect_products(instance):
            children = Section.objects.get(pk=instance.pk).children.all()
            if children:
                for child in children:
                    collect_products(child)
            else:
                nonlocal all_products
                all_products += instance.products.filter(composition__isnull=False).count()

        collect_products(instance)
        return all_products
    
    def get_subsections(self, instance):
        return [child.name for child in Section.objects.filter(parent=instance)]


class ProductInShopSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    last_updated = serializers.SerializerMethodField('get_short_datetime')

    class Meta:
        model = ProductInShop
        fields = ['shop', 'current_price', 'link_to_product_page', 'last_updated']
    
    def get_short_datetime(self, instance):
        last_updated = dateparse.parse_datetime(str(ProductInShop.objects.get(product_id=instance.pk).last_updated))
        return last_updated.strftime('%d.%m.%Y %H:%M:%S')


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_detail')

    class Meta:
        model = Product
        fields = ['name', 'brand', 'volume', 'image', 'url']


class ProductDetailSerializer(ProductSerializer):
    section = serializers.SerializerMethodField('get_full_section')
    composition = serializers.StringRelatedField()
    available_in_shops = ProductInShopSerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['name', 'brand', 'volume', 'image', 'section', 'composition', 'available_in_shops']

    def get_full_section(self, instance):
        if instance.section:
            section = Section.objects.filter(pk=instance.section.pk)
            parent = section.parent
            if parent.parent:
                return f'{parent.parent.name} — {parent.name} — {section.name}'
            return f'{parent.name} — {section[0].name}'
        return None
