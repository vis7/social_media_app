from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FriendRequestViewSet

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = router.urls
