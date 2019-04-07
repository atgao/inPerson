from friendship.models import Follow, Block
from rest_framework import serializers

from .models import FollowRequest

class FollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('followee', 'follower', 'created')

class FollowRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = "__all__"
