from django.db import models
from account.models import User
from store.models import Store


# Create your models here.
class OrderPaymentTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[("failed", "Failed"), ("success", "Success"), ("pending", "Pending")],
        default="pending",
    )
    amount = models.IntegerField(
        help_text="amount will be divided by 100 for exact figure"
    )

    class Meta:
        db_table = "order_payment_transaction"
        app_label = "wallet"

    def __str__(self):
        return f"{self.user.id}:-{self.razorpay_order_id}"


class StoreOwnersAccountsDetails(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    razorpay_contact_id = models.CharField(max_length=255, unique=True)
    razorpay_fund_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, unique=True)
    ifsc = models.CharField(max_length=14)

    class Meta:
        db_table = "store_owners_accounts_details"
        app_label = "wallet"

    def __str__(self):
        return f"{self.name}:-{self.account_number}"
