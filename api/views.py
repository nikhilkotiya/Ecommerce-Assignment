
from .helper import get_next_prev_url
from django.shortcuts import render,get_object_or_404
from .serializer import *
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse, Http404
from rest_framework import status
from django.core import serializers
from django.core.cache import cache
from django.forms.models import model_to_dict
from datetime import datetime
from django.utils import timezone
import time
from django.core.mail import EmailMessage
from .utils import RedisUtils
import json
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .helper import filter_dict_keys,get_hash_key

# from .faker import model_obj
# from d
# def delete_by_id(obj,id):
#     obj = get_object_or_404(obj,id)
#     obj.delete()

CACHE_TTL = getattr(settings, 'CACHE_TTL', 86400)

from django.http import HttpResponseBadRequest
from django.http import JsonResponse
def custom_400(request, exception=None):
    return JsonResponse({'error': str(exception)}, status=400)


def handle_exception(request, exception):
    # This view will be triggered by Django when the custom exception is raised
    return JsonResponse({'error': str(exception.message)}, status=400)

from rest_framework import exceptions

from rest_framework.exceptions import APIException

class CustomException(APIException):
    status_code = 400
    default_detail = 'Custom exception occurred'

def get_object_or_raise(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise CustomException({'error': f"{model.__name__} with {kwargs} does not exist"})

# def get_object_or_raise(model, **kwargs):
#     try:
#         return model.objects.get(**kwargs)
#     except model.DoesNotExist:
#         raise ObjectNotFoundException(model, kwargs)
def handle_exception(request, exception):
    if isinstance(exception, Http404):
        return JsonResponse({'error': 'Not found'}, status=400)

handler400 = 'api.views.handle_exception'

from .query import get_all_vaid_product
class Product_Viewsets(viewsets.ViewSet):
    serializer_class = ProductSerializer
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_utils=RedisUtils()
        self.product=Product()

    def List(self,request,format=None):
        new_data = request.query_params
        page_no = int(new_data.get("page_no",1))
        page_size = 10
        products = None
        # products=self.redis_utils.get("Product_List")
        if products == None:
            products=get_all_vaid_product()
            count=products.count()
            self.redis_utils.set("Product_List_count", count, timeout=30)
            qs_json = json.loads(serializers.serialize('json', products))
            products = self.product.convert_to_output_format(qs_json)
            self.redis_utils.set("Product_List", products, timeout=30)
        else:
            count=self.redis_utils.get("Product_List_count")
            if count==None:
                count=Product.objects.filter(avilable_units__gte=1).count()
                self.redis_utils.set("Product_List_count", count, timeout=30)
        offset = (page_no - 1) * page_size
        if offset >= count != 0 | count == 0:
            result = {
                    'novels': [],
                    'novel_count': 0,
                    'message' : 'Novels Not Found',
                    'status':200,
                    }
        else:
            data=[]
            products = products[offset:offset + page_size]
            data.append(products)
            count = count
            base_url = request.build_absolute_uri()
            next_, prev_ = get_next_prev_url(
                base_url,
                page_no,
                count,
                page_size
            )
            result={
                "count":count,
                "product_data":data,
                "prev_url":prev_,
                "next_url":next_,
                "status":200
            }

        return Response(result)

    def perform_create(self,request):
        # if value:
            # value = value.decode("utf-8")
        payload = request.data.dict()
        # payload=request.data
        print(payload)
        result = {}
        status = 400
        # print(payload)
        message="Product is not created"
        if payload:
            try:
                product_id = None
                if payload.get("product_id"):
                    product_id = payload.get("product_id")
                if product_id is None:
                    key = "testing" + str(time.time())
                    product_id = get_hash_key(key) 
                update_data = filter_dict_keys(payload, self.product.output_fields)
                if request.user.is_authenticated:
                    update_data["user"] = request.user.id
                else:
                    update_data["user"] = payload.get("user")
                    category_obj = Category.objects.get(id=update_data.get("category"))
                image_url = request.FILES.getlist('images')
                # for oneimage in image_url:
                    # serializer = ProductSerializer(data=image_url)
                    # if serializer.is_valid():
                        # update_data['images'] = serializer.data.get('image_url')
                update_data['category']=category_obj
                # import base64
                # update_data['images'] = base64.b64decode(update_data['images'])
                update_data["url"]="http://127.0.0.1:8000/product/"+str(product_id)
                obj, is_created = Product.objects.update_or_create(
                        product_id=product_id,
                        defaults=update_data
                    )
                # update_data.pop('images'
                novel_details = model_to_dict(obj)
                novel_details.pop('images')
                novel_details['images']="http://127.0.0.1:8000/media/files/image/Group_155_1f14it2.png"
                if is_created:
                    pass
                    # self.redis_utils.delete("Product_List")
                    # we need to add set add
                # else:
                    # self.redis_utils.delete("Product_List")
                result=novel_details
                print(novel_details)
                if is_created:
                    message="Product created Successfully"
                    status=200
                else:
                    message="Product updated Successfully"
                    status=200
            except Exception as e:
                message = e
                print(e)

            print(type(result))
            print(result)
            print(type(result)) 
        response = {
            'status': status,
            'message': message,
            'results': result
        }
        return Response(response,status=status)
    
    def destroy(self,request,pk=None):
        payload=request.data
        print("Jere")
        product_id = payload.get("Product_id",pk)
        status=404
        message="please send the product_id"
        if product_id==None:
            result={
                "status":status,
                "message":message
            }
            return Response(result,status=404)
        obj  = get_object_or_raise(Product,product_id = product_id , name="Nikhil Kotiya")
        obj.delete()
        self.redis_utils.delete("Product_List")
        message="product Deleted Succesfully"
        result={
            "status":200,
            "message":message
        }
        return Response(result,status=200)
    
    def product_details(self,request,pk=None):
        payload=request.data
        product={}
        id=payload.get("product_id",pk)
        if id==None:
            message="Someting went wrong"
            result={
                "status":'400',
                "message":message
            }
        key="product"+str(id) 
        data=self.redis_utils.get(key)
        if data is None or data==[]:
            try:
                data=Product.objects.get(product_id=id)  
                qs_json = model_to_dict(data)
                data=ProductSerializer(data)  
                data=data.data
                self.redis_utils.set(key,json.dumps(qs_json),timeout=30) 
            except Exception as e:
                print(e)
                message="Not found"
                result={
                    "status":'404',
                    "message":message
                }
                return Response(result,status=404)
        else:
            data=json.loads(data)
        result={
            "status":200,
            "message":"product fatch successfuly",
            'data':data
        }
        return Response(result)


class Order(APIView):
    def get(self,request):
        payload = json.loads(request.data)
        id = payload.get(id)
        try:
            product=Product.objects.get(id=id)
        except Product.DoesNotExist:
             return Response("Product don't Exists",status=400)
        user=request.user
        if user.is_authenticated:
            if product.avilable_units >= 1:
                serializer=AllProductSerializer(product)
                try:
                    order=OrderItem.objects.get(user=request.user,id=id)
                    return Response("You already order this Item")
                except OrderItem.DoesNotExist:
                    if serializer.is_valid:
                        return Response(serializer.data)
                    return Response(serializer.errors)
            return Response("Out of stock")
        return Response("Please Login")

    def post(self,request,category_slug,product_slug):
        user=request.user
        print(product)
        print(user)
        if user.is_authenticated:
            if product.avilable_units-buy_product >= 0:
                amount=product.price
                print(amount)
                amount=amount*buy_product
                payment = Payment.objects.create(
                    amount=amount,
                    user=request.user,
                )
                d = timezone.now()
                payment.save()
                Place_order = OrderItem()
                Place_order.ordered_date=timezone.now()
                Place_order.amount=amount
                Place_order.product=product
                Place_order.ordered=True
                Place_order.number_of_items=buy_product
                Place_order.payment=payment
                Place_order.user=user
                Place_order.save()
                print(buy_product)
                print(amount)
                date=datetime.now().date()
                count=Orders_count.objects.create(date=date,selled=buy_product,product=product)
                New_data=product.avilable_units
                New_data=New_data-buy_product
                product.avilable_units=New_data
                product.save()
                context={
                    "Product Name":product.name,
                    "Quantity":buy_product,
                    "Ammount":amount,
                    "Message":"Order Done"
                }
                return Response(context)
            else:
                if product.avilable_units == 0:
                    return Response("Out of stock")
                return Response("We have less product left")
        else:
            return Response("Please login to order")

    def list_all_orders(self,request):
        user=request.user
        if user.is_authenticated:
            data=OrderItem.objects.filter(ordered=True,user=user)
            if data.exists():
                serializer=OrderS(data,many=True)
                return Response(serializer.data)
            return Response("No Order")
        else:
            return Response("Please Login")

class Category_Product(APIView):
    def get(self,request,category_slug,format=None):
        data=Product.objects.filter(category__slug=category_slug)
        print(data)
        s=AllProductSerializer(data,many=True)
        if data.exists():
            return Response(s.data)
        return Response("No Product avilable")

class Single_Product(APIView):
    def get_object(self,category_slug,product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404  
    def get(self,request,category_slug,product_slug,format=None):
        product=self.get_object(category_slug,product_slug)
        serializer={}
        if product.user == request.user:
            serializer=ProductSerializer(product) 
        else:
            serializer=AllProductSerializer(product)
        return Response(serializer.data)
    
    
    
    def patch(self, request,category_slug,product_slug,format=None):
        product=self.get_object(category_slug,product_slug)
        print(product)
            # request.data.
        if product.user == request.user:
            serializer=ProductSerializer(product,data=request.data,partial=True)
            if serializer.is_valid():   
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response("You dont have permission to do changes in this product")


def send_email_to_user(request):
    import smtplib
    con = smtplib.SMTP("smtp.gmail.com",587)
    con.ehlo()
    con.starttls()
    admin_email = 'nikhilkotiya8@gmail.com'
    admin_password = 'kibuuihdslenrsrm'
    con.login(admin_email,admin_password)
    msg = "Otp is "
    con.sendmail("email",'nihkilkotiya8@gmail.com',"Subject:Password Reset \n\n"+msg)
    return HttpResponse("workd")
class cancel_order(APIView):
    def get(self,request,category_slug,product_slug):
        user=request.user
        if user.is_authenticated :
            try:
                order=OrderItem.objects.get(user=request.user,product__slug=product_slug)
            except OrderItem.DoesNotExist:
                order=None
            if order is not None and order.number_of_items>=1:
                # date=datetime.now().date()
                product=Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
                print(order)
                context={
                    "Product Name": product.name,
                    "Number of order Unit":order.number_of_items
                }
                return Response(context)
            else:
                return Response("No order found")
        return Response("Please login")

    def post(self,request,category_slug,product_slug):
        cancel_product=request.data.get('count')
        date=datetime.now().date()
        order=OrderItem.objects.get(user=request.user,product__slug=product_slug)
        if cancel_product==0 or cancel_product is None:
            return Response("None order has been cancel")
        if cancel_product>order.number_of_items:
            return Response("your cancel items number must be less than or quals to oder items number")
        product=Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        count=Canceld_order.objects.create(date=date,selled=cancel_product,product=product)
        new=order.number_of_items
        order.number_of_items =  new - cancel_product
        order.save()
        product.avilable_units += cancel_product
        product.save()
        if cancel_product-new ==0:
            order.delete()
            count.delete()
        if cancel_product != 0:
            amount=cancel_product* order.price
            refund=send_email(request,amount,product)
        return Response("Order canceled")

class Summary(APIView):
    def get(self,request,product_slug,*args, **kwargs):
        user=request.user
        if user.is_authenticated:
            data={}
            try:
                data=Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                return Response("No Product found")
            Net_value=data.actual_value
            # return Response("1")
            count=Orders_count.objects.filter(date__range=["2022-01-14", "2022-01-16"],product=data).count()
            print(count)
            cancel_order=Canceld_order.objects.filter(date__range=["2022-01-13", "2022-01-16"],product=data).count()
            unit_count = int(count)-int(cancel_order)
            profit = unit_count*(data.price-Net_value)
            # Refund = Refund(count,cancel_order)
            income = unit_count*(data.price)
            data={ 
                'count':count,
                'cancel_order' :cancel_order,
                'unit_sold' : unit_count,
                'profit': profit,
                'Refund': cancel_order,
                'income': income,
            }
            return Response(data)
            
        else:
            return Response("Plesae Login")

    def post(self,request,product_slug):
        data=request.data
        serializer=Summary(data,many=True)
        print("2")
        if serializer.is_valid():
            return Response(serializer.data)
        return Response("Errpr")

class AddCouponView(APIView):

    def post(self, request, *args, **kwargs):
        code = request.data.get('code', None)
        if code is None:
            return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
        order = Order.objects.get(
            user=self.request.user, ordered=False)
        coupon = get_object_or_404(Coupon, code=code)
        order.coupon = coupon
        order.save()
        return Response(status=HTTP_200_OK)