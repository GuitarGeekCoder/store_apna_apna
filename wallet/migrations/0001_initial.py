# Generated by Django 4.2.17 on 2025-04-04 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoreOwnersAccountsDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("razorpay_contact_id", models.CharField(max_length=255, unique=True)),
                ("razorpay_fund_id", models.CharField(max_length=255, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("account_number", models.CharField(max_length=20, unique=True)),
                ("ifsc", models.CharField(max_length=14)),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.store"
                    ),
                ),
            ],
            options={
                "db_table": "store_owners_accounts_details",
            },
        ),
        migrations.CreateModel(
            name="OrderPaymentTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("razorpay_order_id", models.CharField(max_length=255, unique=True)),
                (
                    "razorpay_payment_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "razorpay_signature",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("failed", "Failed"),
                            ("success", "Success"),
                            ("pending", "Pending"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
                (
                    "amount",
                    models.IntegerField(
                        help_text="amount will be divided by 100 for exact figure"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "order_payment_transaction",
            },
        ),
    ]
