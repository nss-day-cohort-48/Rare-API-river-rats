"""View module for handling requests about park areas"""
from django.contrib.auth.models import User #pylint:disable=imported-auth-user
# from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser


class Profile(ViewSet):
    """Rare Rare_users"""

    def list(self, request):
        """Handle GET requests to rare_users resource
        
        Returns JSON serialized list of rare_users
        """
        rare_users = RareUser.objects.all()
        serializer = RareUserSerializer(
            rare_users, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'is_staff']

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = UserSerializer(many=False)

    class Meta:
        model = RareUser
        fields = ['id', 'user', 'profile_image_url', 'bio']