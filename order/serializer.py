from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from store.models import Product,fetch_store_by_id
from account.models import fetch_user
from order.models import Order,OrderItem
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']



class PlaceOrderSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    store = serializers.IntegerField(required=True)
    items = OrderItemSerializer(many=True)
    store_amount = serializers.FloatField(required=True)
    platform_amount = serializers.FloatField(required=True)
    class Meta:
        model = Order
        fields = ['store','user', 'items','store_amount','platform_amount']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data["user"] = fetch_user(validated_data["user"])
        validated_data["store"] = fetch_store_by_id(validated_data["store"])
        # Begin a transaction block
        with transaction.atomic():
            # Create the order, but defer saving until all items have been processed
            order = Order.objects.create(**validated_data)
            
            for item_data in items_data:
                product = item_data['product']  # Get the product instance
                quantity_to_deduct = item_data['quantity']  # Get the quantity to deduct from the product
                
                # Check if product has enough quantity
                if product.quantity < quantity_to_deduct:
                    raise ValidationError(f"Not enough stock for product: {product.name}. Available quantity: {product.quantity}, Required: {quantity_to_deduct}")

                # Subtract the quantity
                product.quantity -= quantity_to_deduct
                if product.quantity == 0:
                    product.status = "out_of_stock"
                # Save the updated product
                product.save()
                
                # Create the order item (but don't commit it yet if transaction fails)
                OrderItem.objects.create(order=order, **item_data)

            # If no error was raised, the order will be saved at this point
            return order 