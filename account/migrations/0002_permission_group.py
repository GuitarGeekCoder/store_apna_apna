# your_app_name/migrations/XXXX_create_store_group.py

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from store.models import Store, Product
from order.models import Order,OrderItem
def create_store_group(apps, schema_editor):
    # Define the group name
    group_name = 'Store Group'
    
    # Create the group if it doesn't exist
    group, created = Group.objects.get_or_create(name=group_name)
    
    # Get the permissions for Store and Product models
    store_content_type = ContentType.objects.get_for_model(Store)
    product_content_type = ContentType.objects.get_for_model(Product)
    order_content_type = ContentType.objects.get_for_model(Order)
    order_item_content_type = ContentType.objects.get_for_model(OrderItem)

    # Define the required permissions for Store and Product
    store_permissions = [
        Permission.objects.get_or_create(
            codename='add_store',
            name='Can add store',
            content_type=store_content_type
        ),
        Permission.objects.get_or_create(
            codename='change_store',
            name='Can change store',
            content_type=store_content_type
        ),
        Permission.objects.get_or_create(
            codename='delete_store',
            name='Can delete store',
            content_type=store_content_type
        ),
        Permission.objects.get_or_create(
            codename='view_store',
            name='Can view store',
            content_type=store_content_type
        ),
    ]
    
    product_permissions = [
        Permission.objects.get_or_create(
            codename='add_product',
            name='Can add product',
            content_type=product_content_type
        ),
        Permission.objects.get_or_create(
            codename='change_product',
            name='Can change product',
            content_type=product_content_type
        ),
        Permission.objects.get_or_create(
            codename='delete_product',
            name='Can delete product',
            content_type=product_content_type
        ),
        Permission.objects.get_or_create(
            codename='view_product',
            name='Can view product',
            content_type=product_content_type
        ),
    ]
    order_permissions = [
        Permission.objects.get_or_create(
            codename='change_order',
            name='Can change order',
            content_type=order_content_type
        ),
        Permission.objects.get_or_create(
            codename='view_order',
            name='Can view order',
            content_type=order_content_type
        ),
    ]
    order_item_permissions = [
        Permission.objects.get_or_create(
            codename='view_order_item',
            name='Can view order item',
            content_type=order_item_content_type
        ),
    ]
    
    # Add permissions to the group
    for permission in store_permissions + product_permissions + order_permissions + order_item_permissions:
        group.permissions.add(permission[0])

def remove_store_group(apps, schema_editor):
    # Cleanup the group in case the migration is rolled back
    Group.objects.filter(name='Store Group').delete()

class Migration(migrations.Migration):

    dependencies = [
        # Define your dependencies here, e.g., the last migration
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_store_group, remove_store_group),
    ]
