from django.contrib import admin

from .models import *

# # class VariationAdmin(admin.ModelAdmin):
# # 
# # admin.site.register(ItemVariation, ItemVariationAdmin)
# # admin.site.register(Variation, VariationAdmin)
admin.site.register(Product)
# # admin.site.register(OrderItem)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Orders_count)
admin.site.register(Category)
# # admin.site.register(Address, AddressAdmin)
admin.site.register(Canceld_order)
