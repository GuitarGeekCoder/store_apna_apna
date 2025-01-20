from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from store.models import fetch_active_product,Product
from account.models import fetch_user,User
from order.models import Order,OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')

    class Meta:
        model = OrderItem
        fields = ['product_id', 'quantity']



class PlaceOrderSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['user', 'items']


    # def validate(self, data):
    #     user = data["user"]
    #     products = data["products"]
    #     if len(products) == 0:
    #       raise ValidationError("Please select product to order")
    #     instance_products = []
    #     for product in products:
    #         prod = fetch_active_product(product)
    #         if prod:
    #             instance_products.append(prod)
    #         else:
    #             raise ValidationError("Please order the available products only")
    #     user_instance = fetch_user(user)
        
    #     return {
    #         "user" : user_instance,
    #         "products" : instance_products
    #     }
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data["user"] = fetch_user(validated_data["user"])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order    