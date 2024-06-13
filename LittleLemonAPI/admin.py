from django.contrib import admin
from . models import User, MenuItem, Cart, Order, OrderItem

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
