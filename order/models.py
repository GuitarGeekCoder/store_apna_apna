from django.db import models
from store.models import Product
from account.models import User


# Create your models here.
class Order(models.Model):
    # Product = models.ManyToManyField(Product)
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        default="awaiting_confirmation",
        choices=[
            ("awaiting_confirmation", "Awaiting Confirmation"),
            ("order_confirmed", "Order Confirmed by Store"),
            ("in_transist", "In-Transist"),
            ("deliverd", "Deliverd"),
            ("cancel", "Cancel"),
            ("decline", "Decline"),
        ],
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id} - {self.order_date}"

    class Meta:
        db_table = "order"
        app_label = "order"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id} for Order {self.order.id}"

    class Meta:
        db_table = "order_item"
        app_label = "order"
