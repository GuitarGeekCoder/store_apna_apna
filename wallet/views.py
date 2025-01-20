from django.shortcuts import render
from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated
# import stripe
# from django.conf import settings
# from django.http import JsonResponse

# class PaymentViewSet(viewsets.GenericViewSet):

#     def get_serializer(self):
#         if self.action == "create_checkout_session":
#             return 
#         return None

#     @action(detail=False,methods=["post"],permission_classes=[IsAuthenticated])
#     def create_checkout_session(self,request):
#         YOUR_DOMAIN = "http://localhost:3000"  # Or your production URL
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=["card"],
#                 line_items=[
#                     {
#                         "price_data": {
#                             "currency": "inr",
#                             "product_data": {
#                                 "name": "Product Name",
#                             },
#                             "unit_amount": 1000,  # Amount in cents (1000 cents = 10.00 USD)
#                         },
#                         "quantity": 1,
#                     },
#                 ],
#                 mode="payment",
#                 success_url=YOUR_DOMAIN + "/success/",
#                 cancel_url=YOUR_DOMAIN + "/cancel/",
#             )
#             return JsonResponse({"id": checkout_session.id})

#         except Exception as e:
#             return JsonResponse({"error": str(e)})
