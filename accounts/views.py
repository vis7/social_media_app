from django.contrib.auth import logout, login
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegistrationSerializer, UserSerializer

# Create your views here.
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # sending token
            data = {}
            token = Token.objects.get_or_create(user=user)[0].key
            data['username'] = user.username
            data['email'] = user.email
            data['token'] = token
            data['message'] = "User created successfully"

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email__iexact=email).first()

        if not user:
            data = {"message": "Invalid email"}
            return Response(data, status.HTTP_400_BAD_REQUEST)

        if not check_password(password, user.password):
            data = {"message": "Incorrect password"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        token = Token.objects.get_or_create(user=user)[0].key
        data = {}
        data['email'] = user.email
        data['token'] = token

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        data = {"message": "Logout successful"}
        return Response(data, status=status.HTTP_200_OK)


class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        search_keyword = request.query_params.get('q', '').strip()
        page_number = request.query_params.get('page', 1)
        users = User.objects.all()

        if '@' in search_keyword:
            users = users.filter(email=search_keyword)
        else:
            users = users.filter(username__icontains=search_keyword)

        paginator = Paginator(users, 10)
        page_obj = paginator.get_page(page_number)

        serializer = UserSerializer(page_obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
