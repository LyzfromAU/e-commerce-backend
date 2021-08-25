from django.contrib import admin
from .models import Message, User, Item, OrderItem, Order
# Register your models here.
admin.site.register(User)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Message)