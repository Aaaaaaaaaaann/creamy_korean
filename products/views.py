from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import ProductFilter
from .models import IngredientsGroup, Product, Section, UserProfile
from .serializers import ProductSerializer, SectionSerializer, \
    IngredientsGroupSerializer, UserProfileSerializer, UserSerializer


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


class IngredientsGroupListView(generics.ListAPIView):
    queryset = IngredientsGroup.objects.all()
    serializer_class = IngredientsGroupSerializer

    def get_serializer_context(self):
        """Ruturn all fields except nested ones."""
        context = super().get_serializer_context()
        context['fields'] = ['id', 'name']
        return context


class IngredientsGroupDetailView(generics.RetrieveAPIView):
    queryset = IngredientsGroup.objects.all()
    serializer_class = IngredientsGroupSerializer
    

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
