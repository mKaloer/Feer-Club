from django.contrib import admin
from .models import Beer, Order, OrderItem

admin.site.register(Beer)
admin.site.register(Order)
admin.site.register(OrderItem)
