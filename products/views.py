from rest_framework import generics

from .models import Product, Section
from .serializers import ProductSerializer, ProductDetailSerializer, SectionSerializer


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.filter(parent__isnull=True)
    serializer_class = SectionSerializer


class SubsectionListView(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        return Section.objects.filter(parent__slug=self.kwargs['slug'])


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        section = Section.objects.get(slug=self.kwargs['slug'])
        slugs = [section.slug]
        subsections = section.children.all()
        for instance in subsections:
            slugs.append(instance.slug)
            for entry in instance.children.all():
                slugs.append(entry.slug)
        return Product.objects.filter(composition__isnull=False, section__slug__in=slugs)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(composition__isnull=False)
    serializer_class = ProductDetailSerializer
