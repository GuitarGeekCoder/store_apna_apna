# Generated by Django 4.2.17 on 2025-01-24 12:55

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
            name="Order",
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
                ("order_date", models.DateField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("awaiting_confirmation", "Awaiting Confirmation"),
                            ("order_confirmed", "Order Confirmed by Store"),
                            ("in_transist", "In-Transist"),
                            ("deliverd", "Deliverd"),
                            ("cancel", "Cancel"),
                            ("decline", "Decline"),
                        ],
                        default="awaiting_confirmation",
                        max_length=30,
                    ),
                ),
                (
                    "store_amount",
                    models.FloatField(
                        help_text="Amount received by the store owner including delivery charges."
                    ),
                ),
                (
                    "platform_amount",
                    models.FloatField(help_text="Amount received by the platform."),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.store"
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
                "db_table": "order",
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="order.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="store.product",
                    ),
                ),
            ],
            options={
                "db_table": "order_item",
            },
        ),
    ]
