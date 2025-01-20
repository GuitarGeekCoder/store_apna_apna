from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializer import PlaceOrderSerializer
from rest_framework import viewsets


# Create your views here.
class Orders(viewsets.GenericViewSet):
    def get_serializer(self):
        if self.action == "place_order":
            return PlaceOrderSerializer
        return None
    @action(methods=["post"],detail=False,permission_classes=[IsAuthenticated])
    def place_order(self,request):
        serializer = self.get_serializer()
        if serializer:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                # serializer.validate_data
                data = serializer.save()
                if data:
                    return Response({"msg":"Order placed successfully"},status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)