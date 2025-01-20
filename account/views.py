from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from .serilaizers import LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
# Create your views here.
class AuthenticationViewSet(viewsets.GenericViewSet):
    # permission_classes = [AllowAny]
    def get_custom_serializer(self):
        if self.action=="login":
            return LoginSerializer
        return None

    @action(methods=["post"],detail=False,permission_classes=[AllowAny])
    def login(self,request):
        serializer_class = self.get_custom_serializer()
        if serializer_class:
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
               jwt_tokens = serializer.save()
               return Response(jwt_tokens, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    @action(methods=["post"],detail=False,permission_classes=[IsAuthenticated])

    def logout(self,request):
        print(request.data)
        pass
        

    
class GetUserProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    @action(methods=['get'],detail=False)
    def getuser(self,request):
        user = request.user
        print(user)
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        return Response(user_data)