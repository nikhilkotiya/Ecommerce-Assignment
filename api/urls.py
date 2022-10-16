from ast import Add
from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'product', Product_List, basename='novels')

perform_create=Product_List.as_view({
    'post' : 'perform_create'
})

get_product=Product_List.as_view({
    'get' : 'List'
})

delete_pro=Product_List.as_view({
    'get':'destroy'
})

product_details=Product_List.as_view({
    'get':'product_details'
})
urlpatterns = [
    # path('',faker),
    path('all_products/',get_product),
    path('add_product/',perform_create),
    path('delete_pro/<int:pk>',delete_pro),
    path('my_oders/',Allorder.as_view()),
    path('product/<int:pk>',product_details)
    # path('my_order/',Allorder.as_view()),
    # path('summary/<slug:product_slug>/',Summary.as_view()),
    # path('product/<slug:category_slug>/',Category_Product.as_view()),
    # path('product/<slug:category_slug>/<slug:product_slug>/',Single_Product.as_view()),
    # path('product/<slug:category_slug>/<slug:product_slug>/order/',Order.as_view()),
    # path('product/<slug:category_slug>/<slug:product_slug>/Cancel-order/',cancel_order.as_view()),
]
