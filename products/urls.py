from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('sections/', views.SectionListView.as_view(), name='sections_list'),
    path('ingrs-groups/', views.IngredientsGroupListView.as_view(), name='ingrs_groups'),
    path('ingrs-groups/<int:pk>/', views.IngredientsGroupDetailView.as_view(), name='ingrs_groups_detail'),
    path('users/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),  # auth data only
    path('users/<int:pk>/favourites/', views.UserProfileView.as_view(), name='user_favourites'),
    path('users/<int:pk>/ingrs/', views.UserProfileView.as_view(), name='user_ingrs'),
]