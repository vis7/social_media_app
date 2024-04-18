from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import FriendRequest
from .serializers import FriendRequestSerializer
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from accounts.serializers import UserSerializer
from accounts.models import User

class FriendRequestViewSet(viewsets.ViewSet):
    @method_decorator(cache_page(60))  # Cache for 60 seconds
    @action(detail=False, methods=['post'])
    def send_request(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        if not receiver_id:
            return Response({'error': 'Receiver ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        if sender.sent_friend_requests.filter(
                timestamp__gte=timezone.now() - timezone.timedelta(minutes=1)).count() >= 3:
            return Response({'error': 'You have reached the limit for sending friend requests'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        receiver = User.objects.filter(id=receiver_id).first()
        if not receiver:
            return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

        if sender == receiver:
            return Response({'error': 'You cannot send a friend request to yourself'},
                            status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({'error': 'Friend request already sent to this user'}, status=status.HTTP_400_BAD_REQUEST)

        FriendRequest.objects.create(sender=sender, receiver=receiver)
        return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        user = request.user
        friends = user.friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_pending_requests(self, request):
        user = request.user
        pending_requests = user.received_friend_requests.filter(status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def accept_request(self, request):
        user = request.user
        request_id = request.data.get('request_id')
        if not request_id:
            return Response({'error': 'Request ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.filter(receiver=user, id=request_id).first()
        if not friend_request:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'accepted'
        friend_request.save()
        user.friends.add(friend_request.sender)
        return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def reject_request(self, request):
        user = request.user
        request_id = request.data.get('request_id')
        if not request_id:
            return Response({'error': 'Request ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.filter(receiver=user, id=request_id).first()
        if not friend_request:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)
