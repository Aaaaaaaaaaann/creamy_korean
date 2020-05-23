from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('sections/', views.SectionListView.as_view(), name='sections_list'),
    path('sections/<int:pk>/', views.SectionDetailView.as_view(), name='section_detail'),
    path('sections/<int:pk>/products/', views.ProductListView.as_view(), name='products_by_section'),
]