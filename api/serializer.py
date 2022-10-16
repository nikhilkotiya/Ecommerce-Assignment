from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField()
    class Meta:
        model=Product
        fields="__all__"
class AllProductSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField()
    class Meta:
        model=Product
        fields="__all__"


class Count_Of_order_item(serializers.Serializer):
    count=serializers.IntegerField()






class CategorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True,read_only=True)
    print(product.data)
    def get_Product(self):
        print(self.product.name)
        return self.product.name
    class Meta:
        model=Category
        fields=['id','name','slug','get_absoulte_url','product']


class OrderS(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'name',
            'ordered_date',
            'payment',
            'amount',
            'cancel_order',
            'number_of_items',
        )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'amount',
            'timestamp'
        )
class check(serializers.Serializer):
    field1 = serializers.BooleanField(default=False)
class OrderS(serializers.ModelSerializer):
    # d = serializers.SerializerMethodField()
    # field_2 = serializers.NullBooleanField()
    class Meta:
        model = OrderItem
        fields = (
                'name',
                'amount',
                'cancel_o',
                'cancel_order',
            )
class Orders_count_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Orders_count
        fields=(
            'product'
            'date'
            'selled'
        )

class Summary(serializers.Serializer):
    count=serializers.IntegerField(default=0)
    cancel_order=serializers.IntegerField(default=0)
    unit_sold=serializers.IntegerField(default=0)
    profit=serializers.IntegerField(default=0)
    Refund=serializers.IntegerField(default=0)
    income=serializers.IntegerField(default=0)
class PSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=(
            # "id",
            "name",
            # "user",
            # "get_absoulte_url",
            "description",
            # "category",
            "price",
            "avilable_units",
            # "get_image_url",
            # "oder_this_peoduct",
        )
