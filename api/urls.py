from ast import Add
from django.urls import path
from .views import *
from .import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# handle_404 = 'api.views.handle_404'
handler400 = 'api.views.handle_exception'
# def handle_404(request, exception):
#     return JsonResponse({'error': str(exception)}, status=400)

# handler404 = 'api.views.handle_404'


router.register(r'product', Product_Viewsets, basename='novels')

perform_create=Product_Viewsets.as_view({
    'post' : 'perform_create'
})

get_product=Product_Viewsets.as_view({
    'get' : 'List'
})

delete_pro=Product_Viewsets.as_view({
    'post':'destroy'
})

product_details=Product_Viewsets.as_view({
    'get':'product_details'
})
urlpatterns = [
    # path('',faker),
    path('all_products/',get_product),
    path('add_product/',perform_create),
    path('delete_pro/<str:pk>',delete_pro),
    # path('my_oders/',Allorder.as_view()),
    path('product/<int:pk>',product_details),
    path('send_email/',send_email_to_user),
    # path('summary/<slug:product_slug>/',Summary.as_view()),
    # path('product/<slug:category_slug>/',Category_Product.as_view()),
    # path('product/<slug:category_slug>/<slug:product_slug>/',Single_Product.as_view()),
    # path('product/<slug:category_slug>/<slug:product_slug>/order/',Order.as_view()),
    # path('product/<slug:category_slug>/<slug:product_slug>/Cancel-order/',cancel_order.as_view()),
]
