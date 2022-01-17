from django.urls import path
from .views import *
# from rest_framework.routes import DefaultRouter 
urlpatterns = [
    path('all_products/',Product_List.as_view()),
    path('add_product/',Add_Product.as_view()),
    path('my_oders/',Allorder.as_view()),
    # path('my_order/',Allorder.as_view()),
    path('summary/<slug:product_slug>/',Summary.as_view()),
    path('product/<slug:category_slug>/',Category_Product.as_view()),
    path('product/<slug:category_slug>/<slug:product_slug>/',Single_Product.as_view()),
    path('product/<slug:category_slug>/<slug:product_slug>/order/',Order.as_view()),
    path('product/<slug:category_slug>/<slug:product_slug>/Cancel-order/',cancel_order.as_view()),
]
