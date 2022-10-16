from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache
from .helper import get_model_fields
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
    # def __str__(self):
    #     return self.name
    # def get_absoulte_url(self):
    #     return f'/{self.slug}/'

class Product(models.Model):
    product_id = models.CharField(primary_key=True, max_length=60)
    user=models.CharField(null=False,max_length=60)
    category = models.ForeignKey(Category,on_delete=models.CASCADE, max_length=10)
    name = models.CharField(max_length=40)
    description=models.TextField(blank=True,null=True)
    price=models.IntegerField()
    avilable_units=models.IntegerField(default=0)
    is_disabled = models.IntegerField(default=0)
    tags = models.TextField(null=True)
    status = models.CharField(null=True, max_length=50, default='draft')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # images = models.ImageField(upload_to = "files/image",default="files/image/image0.png",blank=True,null=True) 
    url=models.CharField(max_length=40,null=True,blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis_utils=cache
        self.output_fields = get_model_fields(Product)

    def convert_to_output_format(qs_json):
        meta_fields = Product._meta.get_fields()
        fields = [f.name for f in meta_fields]
        primary_key_name = Product._meta.pk.name

        final_result = []

        for item in qs_json:
            entity_details = {}
            if item.get('fields') is None:
                continue
            for f in fields:
                entity_details[f] = item['fields'].get(f)
            entity_details[primary_key_name] = item.get('pk')
            for f in item.keys():
                if f == 'fields':
                    continue
                entity_details[f] = item.get(f)
            final_result.append(entity_details)
        return final_result
    


    # def get_absoulte_url(self):
    #     return 'http://127.0.0.1:8000/product'f'/{self.category.slug}/{self.slug}/' 

    # def get_image_url(self):
    #     return 'http://127.0.0.1:8000'+self.images.url

    # def oder_this_peoduct(self):
    #     return 'http://127.0.0.1:8000/product'f'/{self.category.slug}/{self.slug}/order' 

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

