from django.contrib.auth.models import User
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import IngredientDocument
from .models import (
    Section,
    Product,
    IngredientsGroup,
    Ingredient,
    ProductInShop,
    Price,
    UserProfile
)
from extras.users import ProfileHandler


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
        return Product.objects.filter(
            composition__isnull=False, 
            section_id__in=subsections).count()
    
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
        fields = ['shop', 'availability', 'current_price',
                  'link_to_product_page', 'last_updated']


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
        fields = ['id', 'name', 'brand', 'volume', 'image', 'section', 
                  'composition', 'prices', 'available_in_shops']


class IngredientSerializer(DocumentSerializer):

    class Meta:
        document = IngredientDocument
        fields = ['id', 'name']


class IngredientsGroupSerializer(DynamicFieldsSerializer):
    ingredients = serializers.StringRelatedField(many=True)

    class Meta:
        fields = ['id', 'name', 'ingredients']
        model = IngredientsGroup


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True
        )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        new_user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            )
        new_user.set_password(validated_data['password'])
        new_user.save()

        # Create an entry in the related table as well (without data).
        UserProfile.objects.create(user=new_user)

        return new_user
        
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        if new_pass := validated_data.get('password', None):
            instance.set_password(new_pass)
        instance.save()
        return instance


class UserProfileSerializer(DynamicFieldsSerializer):
    favourite_products = serializers.DictField()
    exclude_ingrs = serializers.DictField()
    include_ingrs = serializers.DictField()
    exclude_ingrs_groups = serializers.DictField()
    include_ingrs_groups = serializers.DictField()

    class Meta:
        model = UserProfile
        fields = ['favourite_products', 'exclude_ingrs', 'include_ingrs', 
                  'exclude_ingrs_groups', 'include_ingrs_groups']

    def to_representation(self, instance):
        output = {}

        # The representation for /users/{id}/favourites.
        # It this request, 'self.fields' contain only 'favourite_products' field.
        if 'favourite_products' in self.fields:
            output['favourite_products'] = ProfileHandler.get_values(
                instance.profile.favourite_products, Product)
        
        # The representation for /users/{id}/ingrs.
        # In this request, 'self.fields' contain the rest of fields.
        elif 'exclude_ingrs' in self.fields:
            output['exclude_ingrs'] = ProfileHandler.get_values(
                instance.profile.exclude_ingrs, Ingredient)
        
            output['include_ingrs'] = ProfileHandler.get_values(
                instance.profile.include_ingrs, Ingredient)

            output['exclude_ingrs_groups'] = ProfileHandler.get_values(
                instance.profile.exclude_ingrs_groups, IngredientsGroup)

            output['include_ingrs_groups'] = ProfileHandler.get_values(
                instance.profile.exclude_ingrs_groups, IngredientsGroup)

        return output
    
    def update(self, instance, validated_data):
        profile = User.objects.get(pk=instance.pk)

        if favourites_json := validated_data.get('favourite_products', None):
            ProfileHandler.make_action(
                context=favourites_json,
                field=profile.favourite_products,
                model=Product
            )
            
        if exclude_json := validated_data.get('exclude_ingrs', None):
            ProfileHandler.make_action(
                context=exclude_json,
                field=profile.exclude_ingrs,
                model=Ingredient
            )

        if include_json := validated_data.get('include_ingrs', None):
            ProfileHandler.make_action(
                context=include_json,
                field=profile.include_ingrs,
                model=Ingredient
            )
            
        if exclude_groups_json := validated_data.get('exclude_ingrs_groups', None):
            ProfileHandler.make_action(
                context=exclude_groups_json,
                field=profile.exclude_ingrs_groups,
                model=Ingredient
            )
            
        if include_groups_json := validated_data.get('include_ingrs_groups', None):
            ProfileHandler.make_action(
                context=include_groups_json,
                field=profile.include_ingrs_groups,
                model=Ingredient
            )

        profile.save()
