from rest_framework import serializers

from .models import Section, Product, IngredientsGroup, Ingredient, ProductInShop, Price


class DynamicFieldsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', None)
        if context:
            query_fields = context.pop('fields', None)
            super().__init__(*args, **kwargs)
            if query_fields:
                for field in set(self.fields) - set(query_fields):
                    self.fields.pop(field)


class SectionSerializer(serializers.ModelSerializer):
    products_number = serializers.SerializerMethodField('get_products_number')
    subsections = serializers.SerializerMethodField('get_subsections_data')

    class Meta:
        model = Section
        fields = ['id', 'name', 'products_number', 'subsections']

    def get_products_number(self, instance):
        subsections = instance.get_most_nested()
        return Product.objects.filter(composition__isnull=False, section_id__in=subsections).count()
    
    def get_subsections_data(self, instance):
        serializer = SectionSerializer(instance.children.all(), many=True)
        return serializer.data


class CompositionSerializer(serializers.RelatedField):

    def to_representation(self, instance):
        ingredients = instance.ingredients
        return ', '.join(Ingredient.objects.get(pk=ingr).name for ingr in ingredients)


class ProductInShopSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()

    class Meta:
        model = ProductInShop
        fields = ['shop', 'availability', 'current_price', 'link_to_product_page', 'last_updated']


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['highest', 'lowest']


class ProductSerializer(DynamicFieldsSerializer):
    section = serializers.StringRelatedField()
    composition = CompositionSerializer(read_only=True)
    prices = PriceSerializer(read_only=True, many=True)
    available_in_shops = ProductInShopSerializer(read_only=True, many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'volume', 'image', 'section', 'composition', 'prices', 'available_in_shops']


class IngredientsGroupSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField(many=True)

    class Meta:
        model = IngredientsGroup
        fields = ['id', 'name', 'kind', 'ingredients']