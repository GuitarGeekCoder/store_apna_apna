from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_date",
        "status",
        "user"
    ]
admin.site.register(Order,OrderAdmin)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=[
        "order",
        "product",
        "quantity"
    ]
admin.site.register(OrderItem,OrderItemAdmin)