from django.contrib.auth.models import User
from django_elasticsearch_dsl_drf.constants import LOOKUP_FILTER_PREFIX
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    FilteringFilterBackend
)
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from . import serializers as app_serializers
from .documents import IngredientDocument
from .models import IngredientsGroup, Product, Section
from .filters import ProductFilter


class ProductListView(generics.ListAPIView):
    queryset = Product.search.with_composition()
    serializer_class = app_serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        fields = self.request.query_params.get('fields', None)
        if fields:
            context['fields'] = fields.split(',')
        return context


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.search.with_composition()
    serializer_class = app_serializers.ProductSerializer


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.filter(parent=None)
    serializer_class = app_serializers.SectionSerializer


class IngredientFilterView(DocumentViewSet):
    document = IngredientDocument
    serializer_class = app_serializers.IngredientSerializer
    pagination_class = PageNumberPagination
    filter_backends = [CompoundSearchFilterBackend, FilteringFilterBackend]
    search_fields = ['name']
    filter_fields = {
        'name': {
            'field': 'name',
            'lookups': [LOOKUP_FILTER_PREFIX]
            }
        }
    ordering = ['name']


class IngredientsGroupListView(generics.ListAPIView):
    queryset = IngredientsGroup.objects.all()
    serializer_class = app_serializers.IngredientsGroupSerializer

    def get_serializer_context(self):
        """Return all fields except nested ones."""
        context = super().get_serializer_context()
        context['fields'] = ['id', 'name']
        return context


class IngredientsGroupDetailView(generics.RetrieveAPIView):
    queryset = IngredientsGroup.objects.all()
    serializer_class = app_serializers.IngredientsGroupSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = app_serializers.UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = app_serializers.UserSerializer
    queryset = User.objects.all()


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = app_serializers.UserProfileSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # [-2] because of a trailing slash.
        resource = self.request.get_full_path().split('/')[-2]
        if resource == 'favourites':
            context['fields'] = ['favourite_products']
        elif resource == 'ingrs':
            context['fields'] = [
                'exclude_ingrs',
                'include_ingrs',
                'exclude_ingrs_groups',
                'include_ingrs_groups'
            ]
        return context
