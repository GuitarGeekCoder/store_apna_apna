import razorpay
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
class Payment(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    @action(methods=["post"],detail=False)
    def initialize_payment(self, request, *args, **kwargs):
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            amount = int(request.data.get("amount") * 100)
            currency = "INR"  # You can change this to other currencies if needed

            order = razorpay_client.order.create({
                "amount": amount,
                "currency": currency,
                "payment_capture": 1,  # Automatic payment capture
            })

            return JsonResponse({
                "orderId": order["id"],
                "currency": currency,
                "amount":amount
            },status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)  

 # Action to verify payment (verify Razorpay payment signature)
    @action(methods=["post"], detail=False)
    def verify_payment(self, request, *args, **kwargs):
        try:
            # Extract payment details from the request
            payment_id = request.data.get("razorpay_payment_id")
            order_id = request.data.get("razorpay_order_id")
            signature = request.data.get("razorpay_signature")

            if not all([payment_id, order_id, signature]):
                return JsonResponse({"error": "Missing required parameters"}, status=400)

            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Prepare parameters to verify the payment signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature using Razorpay's utility
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If signature is valid, confirm payment
            return JsonResponse({"msg": "Payment verified successfully!"}, status=200)

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Payment signature verification failed"}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
