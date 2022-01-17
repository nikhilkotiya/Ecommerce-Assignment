from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.conf import settings
from time import time
DEMO_CHOICES =(
    ("P", "Phone"),
    ("L", "Laptop"),
    ("TV", "Television"),
    ("EP", "Earphone"),
)
class Category(models.Model):
    name=models.CharField(max_length=255,choices = DEMO_CHOICES)
    slug=models.SlugField()

    # class Meta:
    #     ordering=('name',)
    def __str__(self):
        return self.name
    def get_absoulte_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, max_length=10)
    name = models.CharField(max_length=40)
    slug=models.SlugField()
    description=models.TextField(blank=True,null=True)
    price=models.IntegerField()
    avilable_units=models.IntegerField(default=0)
    # active = models.BooleanField(default = False)
    images = models.ImageField(upload_to = "files/image",default="files/image/image0.png",blank=True,null=True) 
    # date = models.DateField() 
    actual_value=models.IntegerField()
    def __str__(self):
        return self.name
    def get_absoulte_url(self):
        return 'http://127.0.0.1:8000/product'f'/{self.category.slug}/{self.slug}/' 

    def get_image_url(self):
        return 'http://127.0.0.1:8000'+self.images.url

    def oder_this_peoduct(self):
        return 'http://127.0.0.1:8000/product'f'/{self.category.slug}/{self.slug}/order' 

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered_date = models.DateField(auto_now_add=True)
    amount=models.IntegerField()
    number_of_items=models.IntegerField(default=0)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    cancel_o=models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    def name(self):
        return self.product.name
    def cancel_order(self):
        return 'http://127.0.0.1:8000/product'f'/{self.product.category.slug}/{self.product.slug}/Cancel-order'
    def __str__(self):
        return self.user.username

    
    # objects = models.Manager()

class Orders_count(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateField()
    selled=models.IntegerField(default=0)

class Canceld_order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateField()
    selled=models.IntegerField(default=0)

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

