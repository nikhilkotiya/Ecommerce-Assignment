from django.shortcuts import render
from .serializer import *
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse, Http404
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from time import time
from django.core.mail import EmailMessage
class Add_Product(APIView):
    def post(self,request,*args, **kwargs):
        user=request.user
        if user.is_authenticated:
            data=request.data
            date=datetime.now().date()
            slug=user.username+"-"f'{int(time())}'
            print(data)
            serializer=ProductSerializer(data=data,many=True)
            if serializer.is_valid():
                print(serializer.data)
                serializer.save(user=request.user,slug=slug)
                return Response("Your product is added")
            return Response(serializer.errors) 
        return Response("Login First")





class Product_List(APIView):
    def get(self,request,format=None):
        products=Product.objects.filter(avilable_units__gte=1)
        serializer = AllProductSerializer(products,many=True)
        return Response(serializer.data)


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

class Order(APIView):
    def get(self,request,category_slug,product_slug):
        product=Product.objects.get(slug=product_slug)
        print(product)
        user=request.user
        if user.is_authenticated:
            if product.avilable_units >= 1:
                serializer=AllProductSerializer(product)
                try:
                    order=OrderItem.objects.get(user=request.user,product__slug=product_slug)
                    return Response("You already order this Item")
                except OrderItem.DoesNotExist:
                    if serializer.is_valid:
                        return Response(serializer.data)
                    return Response(serializer.errors)
            return Response("Out of stock")
        return Response("Please Login")
    def post(self,request,category_slug,product_slug):
        try:
            order=OrderItem.objects.get(user=request.user,product__slug=product_slug)
            return Response("You already order this Item")
        except OrderItem.DoesNotExist:
            buy_product=request.data.get('count')
            if buy_product==0 or buy_product is None:
                return Response("Enter the count of Product you want to buy")
            product=Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
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
            
# class test(APIView):
#     def get_object(self,category_slug):
#         try:
#             return Category.objects.filter(slug=category_slug)
#         except Category.DoesNotExist:
#             raise Http404
#     def get(self,request,category_slug,format=None):
#         # print(self.category)
#         # print()
#         # print(category_slug)
#         c=self.get_object(category_slug)
#         # print(c)
#         # pass
#         # print(product)
#         data=C.objects.filter(category__slug=category_slug)
#         print(data)
#         s=ProductSerializer(data,many=True)
#         # serializer=CategorySerializer(c,many=True)
#         # print(serializer.data)
#         return Response(s.data) 

















# class PaymentView(APIView):
#     def post(self, request, *args, **kwargs):
#             user=request.user
#         if request.order
#         return Response(status=HTTP_200_OK)
#         except:
#             return Response("Error")
#         # except stripe.error.CardError as e:
#         #     body = e.json_body
#         #     err = body.get('error', {})
#         #     return Response({"message": f"{err.get('message')}"}, status=HTTP_400_BAD_REQUEST)

#         # except stripe.error.RateLimitError as e:
#         #     # Too many requests made to the API too quickly
#         #     messages.warning(self.request, "Rate limit error")
#         #     return Response({"message": "Rate limit error"}, status=HTTP_400_BAD_REQUEST)

#         # except stripe.error.InvalidRequestError as e:
#         #     print(e)
#         #     # Invalid parameters were supplied to Stripe's API
#         #     return Response({"message": "Invalid parameters"}, status=HTTP_400_BAD_REQUEST)

#         # except stripe.error.AuthenticationError as e:
#         #     # Authentication with Stripe's API failed
#         #     # (maybe you changed API keys recently)
#         #     return Response({"message": "Not authenticated"}, status=HTTP_400_BAD_REQUEST)

#         # except stripe.error.APIConnectionError as e:
#         #     # Network communication with Stripe failed
#         #     return Response({"message": "Network error"}, status=HTTP_400_BAD_REQUEST)

#         # except stripe.error.StripeError as e:
#         #     # Display a very generic error to the user, and maybe send
#         #     # yourself an email
#         #     return Response({"message": "Something went wrong. You were not charged. Please try again."}, status=HTTP_400_BAD_REQUEST)

#         # except Exception as e:
#         #     # send an email to ourselves
#         #     return Response({"message": "A serious error occurred. We have been notifed."}, status=HTTP_400_BAD_REQUEST)

#         # return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)

class Allorder(APIView):
    def get(self,request):
        user=request.user
        if user.is_authenticated:
            data=OrderItem.objects.filter(ordered=True,user=user)
            # serializer=OrderS(data,many=True)
            if data.exists():
                serializer=OrderS(data,many=True)
                return Response(serializer.data)
            return Response("No Order")
        else:
            return Response("Please Login")
def send_email(request,amount,product):
    email = EmailMessage({
        'User':request.user,
        'Amount':amount,
        'Canceled_product':product,
    })
    email.send()
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
            # serializer=Summary(data,many=True)
            # print("2")
            # if serializer.is_valid:
            #     return Response(serializer.data)
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