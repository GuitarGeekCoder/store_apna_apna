from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    # Override the get_form method to conditionally hide the user field
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            form.base_fields['store_amount'].disabled = True
            form.base_fields['user'].disabled = True
            form.base_fields['store'].disabled = True
            form.base_fields.pop("platform_amount",None)
        return form

    list_display = [
        "order_date",
        "status",
        "user",
        "store_amount"
    ]
admin.site.register(Order,OrderAdmin)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=[
        "order",
        "product",
        "quantity"
    ]
admin.site.register(OrderItem,OrderItemAdmin)