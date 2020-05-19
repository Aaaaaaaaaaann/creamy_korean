from django.urls import path

from . import views

urlpatterns = [
    path('sections/', views.SectionListView.as_view(), name='main_sections'),
    path('sections/<path:slug>/', views.SubsectionListView.as_view(), name='subsections_list'),
    path('products/<path:slug>/', views.ProductListView.as_view(), name='products_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]