import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=32, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        password = data['password']
        confirm_password = data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password not matched")

        # encrypt password before storing it
        data['password'] = make_password(password)

        return data

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return email
        else:
            raise serializers.ValidationError("Email format is invalid")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
