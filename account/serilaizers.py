from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self,data):
        username = data["username"]
        password = data["password"]
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid credentials")
            if not user.is_active:
                raise ValidationError("Your account is deactivate please contact admin")    
            data["user"] = user
            return data
        
        raise ValidationError("please provide valid username and password")   

    def create(self,validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }