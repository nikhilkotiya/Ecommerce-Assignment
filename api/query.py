from .models import *
def get_all_vaid_product(): 
    return Product.objects.filter(avilable_units__gte=1)