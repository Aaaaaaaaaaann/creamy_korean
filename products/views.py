from rest_framework import generics
from rest_framework import pagination

from .models import Product, Section
from .serializers import ProductSerializer, SectionSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        section = self.kwargs['pk']
        if section:
            subsections = Section.objects.get(pk=section).get_most_nested()
            return Product.objects.filter(composition__isnull=False, section_id__in=subsections)
        return Product.objects.filter(composition__isnull=False)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(composition__isnull=False)
    serializer_class = ProductSerializer


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.filter(parent=None)
    serializer_class = SectionSerializer


class SectionDetailView(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
