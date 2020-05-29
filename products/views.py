from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import ProductFilter
from .models import Product, Section, IngredientsGroup
from .serializers import ProductSerializer, SectionSerializer, IngredientsGroupSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.search.with_composition()
    serializer_class = ProductSerializer
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
    serializer_class = ProductSerializer


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.filter(parent=None)
    serializer_class = SectionSerializer


class IngredientsGroupView(generics.ListAPIView):
    serializer_class = IngredientsGroupSerializer
    queryset = IngredientsGroup.objects.all()