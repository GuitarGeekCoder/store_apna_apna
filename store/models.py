from django.db import models
from account.models import User, City
from django.core.exceptions import ValidationError


# Create your models here.
class Store(models.Model):
    # New category field for product-based categories
    PRODUCT_CATEGORIES = [
        ("electronics", "Electronics"),
        ("clothing_fashion", "Clothing and Fashion"),
        ("food_beverages", "Food and Beverages"),
        ("health_beauty", "Health and Beauty"),
        ("home_furniture", "Home and Furniture"),
        ("toys_games", "Toys and Games"),
        ("books_stationery", "Books and Stationery"),
        ("sports_outdoors", "Sports and Outdoors"),
        ("automotive", "Automotive"),
    ]
    name = models.CharField(max_length=300)
    gstin = models.CharField(max_length=100)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=[
            ("Active", "active"),
            ("pending_verification", "Pending in verification"),
            ("Deactive", "deactive"),
        ],
        default="pending_verification",
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    category = models.CharField(
        max_length=50,
        choices=PRODUCT_CATEGORIES,
        blank=False,  # Makes the field mandatory
        null=False,
    )
    delivery_charge_per_km = models.IntegerField(default=10,help_text="The delivery charge per kilometer. This amount will be multiplied by the distance (in kilometers) to calculate the total delivery charge for an order.")
    platform_fees = models.IntegerField(default=10,help_text="Percentage of the total order amount to be charged as platform fee for this store.")

    class Meta:
        db_table = "store"
        app_label = "store"

    def __str__(self):
        return self.name


class Product(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        UNAVAILABLE = "unavailable", "Unavailable"
        OUT_OF_STOCK = "out_of_stock", "Out of stock"

    name = models.CharField(max_length=500)
    price = models.FloatField()
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,  # Default value if none is provided
    )
    quantity = models.IntegerField(default=0)  # Quantity of the product
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically set status to "out_of_stock" when quantity is 0
        if self.quantity == 0:
            self.status = Product.Status.OUT_OF_STOCK
        super().save(*args, **kwargs)

    class Meta:
        db_table = "product"
        app_label = "store"

    def __str__(self):
        return self.name

def fetch_active_product(id):
    try:
        return Product.objects.filter(pk=id,status="available").first()
    except Exception as e:
        print("Exception in fetching active product:",str(e))
        return None
def fetch_store_by_id(id):
    try:
        return Store.objects.filter(pk=id).first()
    except Exception as e:
        print("Exception in getting the store:",str(e))
        return None    