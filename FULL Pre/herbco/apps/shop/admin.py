from django.contrib import admin

from shop.models import Item, ShoppingCart, Category, ItemExtra, Order

admin.site.register(Item)
admin.site.register(ShoppingCart)
admin.site.register(Category)
admin.site.register(ItemExtra)
admin.site.register(Order)
