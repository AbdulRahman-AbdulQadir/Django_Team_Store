from django.urls import path
from . import views

urlpatterns = [
    path('product_listing_page/', views.product_listing_page, name='product_listing_page'),
    path('product_detail_page/<int:pk>', views.product_detail_page, name='product_detail_page'),
    path('category/<str:categ>', views.category, name='category'),
    path('search/', views.search),
]